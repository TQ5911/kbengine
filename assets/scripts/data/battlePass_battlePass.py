# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: battlePass/battlePass
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    26090101: _tools.RODict({
        "ID": 26090101,
        "tier": 1,
        "passGroupID": 20260901,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    26090102: _tools.RODict({
        "ID": 26090102,
        "tier": 2,
        "passGroupID": 20260901,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    26090103: _tools.RODict({
        "ID": 26090103,
        "tier": 3,
        "passGroupID": 20260901,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    26100101: _tools.RODict({
        "ID": 26100101,
        "tier": 1,
        "passGroupID": 20261001,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    26100102: _tools.RODict({
        "ID": 26100102,
        "tier": 2,
        "passGroupID": 20261001,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    26100103: _tools.RODict({
        "ID": 26100103,
        "tier": 3,
        "passGroupID": 20261001,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    26110101: _tools.RODict({
        "ID": 26110101,
        "tier": 1,
        "passGroupID": 20261101,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    26110102: _tools.RODict({
        "ID": 26110102,
        "tier": 2,
        "passGroupID": 20261101,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    26110103: _tools.RODict({
        "ID": 26110103,
        "tier": 3,
        "passGroupID": 20261101,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    26092501: _tools.RODict({
        "ID": 26092501,
        "tier": 1,
        "passGroupID": 20260925,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    26092502: _tools.RODict({
        "ID": 26092502,
        "tier": 2,
        "passGroupID": 20260925,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    26092503: _tools.RODict({
        "ID": 26092503,
        "tier": 3,
        "passGroupID": 20260925,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001101: _tools.RODict({
        "ID": 10001101,
        "tier": 1,
        "passGroupID": 100011,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001102: _tools.RODict({
        "ID": 10001102,
        "tier": 2,
        "passGroupID": 100011,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001103: _tools.RODict({
        "ID": 10001103,
        "tier": 3,
        "passGroupID": 100011,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001201: _tools.RODict({
        "ID": 10001201,
        "tier": 1,
        "passGroupID": 100012,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001202: _tools.RODict({
        "ID": 10001202,
        "tier": 2,
        "passGroupID": 100012,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001203: _tools.RODict({
        "ID": 10001203,
        "tier": 3,
        "passGroupID": 100012,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001301: _tools.RODict({
        "ID": 10001301,
        "tier": 1,
        "passGroupID": 100013,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001302: _tools.RODict({
        "ID": 10001302,
        "tier": 2,
        "passGroupID": 100013,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001303: _tools.RODict({
        "ID": 10001303,
        "tier": 3,
        "passGroupID": 100013,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001401: _tools.RODict({
        "ID": 10001401,
        "tier": 1,
        "passGroupID": 100014,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001402: _tools.RODict({
        "ID": 10001402,
        "tier": 2,
        "passGroupID": 100014,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001403: _tools.RODict({
        "ID": 10001403,
        "tier": 3,
        "passGroupID": 100014,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001501: _tools.RODict({
        "ID": 10001501,
        "tier": 1,
        "passGroupID": 100015,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001502: _tools.RODict({
        "ID": 10001502,
        "tier": 2,
        "passGroupID": 100015,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001503: _tools.RODict({
        "ID": 10001503,
        "tier": 3,
        "passGroupID": 100015,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001601: _tools.RODict({
        "ID": 10001601,
        "tier": 1,
        "passGroupID": 100016,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001602: _tools.RODict({
        "ID": 10001602,
        "tier": 2,
        "passGroupID": 100016,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001603: _tools.RODict({
        "ID": 10001603,
        "tier": 3,
        "passGroupID": 100016,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001701: _tools.RODict({
        "ID": 10001701,
        "tier": 1,
        "passGroupID": 100017,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001702: _tools.RODict({
        "ID": 10001702,
        "tier": 2,
        "passGroupID": 100017,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001703: _tools.RODict({
        "ID": 10001703,
        "tier": 3,
        "passGroupID": 100017,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001801: _tools.RODict({
        "ID": 10001801,
        "tier": 1,
        "passGroupID": 100018,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001802: _tools.RODict({
        "ID": 10001802,
        "tier": 2,
        "passGroupID": 100018,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001803: _tools.RODict({
        "ID": 10001803,
        "tier": 3,
        "passGroupID": 100018,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10001901: _tools.RODict({
        "ID": 10001901,
        "tier": 1,
        "passGroupID": 100019,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10001902: _tools.RODict({
        "ID": 10001902,
        "tier": 2,
        "passGroupID": 100019,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10001903: _tools.RODict({
        "ID": 10001903,
        "tier": 3,
        "passGroupID": 100019,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002001: _tools.RODict({
        "ID": 10002001,
        "tier": 1,
        "passGroupID": 100020,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002002: _tools.RODict({
        "ID": 10002002,
        "tier": 2,
        "passGroupID": 100020,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002003: _tools.RODict({
        "ID": 10002003,
        "tier": 3,
        "passGroupID": 100020,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002101: _tools.RODict({
        "ID": 10002101,
        "tier": 1,
        "passGroupID": 100021,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002102: _tools.RODict({
        "ID": 10002102,
        "tier": 2,
        "passGroupID": 100021,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002103: _tools.RODict({
        "ID": 10002103,
        "tier": 3,
        "passGroupID": 100021,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002201: _tools.RODict({
        "ID": 10002201,
        "tier": 1,
        "passGroupID": 100022,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002202: _tools.RODict({
        "ID": 10002202,
        "tier": 2,
        "passGroupID": 100022,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002203: _tools.RODict({
        "ID": 10002203,
        "tier": 3,
        "passGroupID": 100022,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002301: _tools.RODict({
        "ID": 10002301,
        "tier": 1,
        "passGroupID": 100023,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002302: _tools.RODict({
        "ID": 10002302,
        "tier": 2,
        "passGroupID": 100023,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002303: _tools.RODict({
        "ID": 10002303,
        "tier": 3,
        "passGroupID": 100023,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002401: _tools.RODict({
        "ID": 10002401,
        "tier": 1,
        "passGroupID": 100024,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002402: _tools.RODict({
        "ID": 10002402,
        "tier": 2,
        "passGroupID": 100024,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002403: _tools.RODict({
        "ID": 10002403,
        "tier": 3,
        "passGroupID": 100024,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002501: _tools.RODict({
        "ID": 10002501,
        "tier": 1,
        "passGroupID": 100025,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002502: _tools.RODict({
        "ID": 10002502,
        "tier": 2,
        "passGroupID": 100025,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002503: _tools.RODict({
        "ID": 10002503,
        "tier": 3,
        "passGroupID": 100025,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002601: _tools.RODict({
        "ID": 10002601,
        "tier": 1,
        "passGroupID": 100026,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002602: _tools.RODict({
        "ID": 10002602,
        "tier": 2,
        "passGroupID": 100026,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002603: _tools.RODict({
        "ID": 10002603,
        "tier": 3,
        "passGroupID": 100026,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002701: _tools.RODict({
        "ID": 10002701,
        "tier": 1,
        "passGroupID": 100027,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002702: _tools.RODict({
        "ID": 10002702,
        "tier": 2,
        "passGroupID": 100027,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002703: _tools.RODict({
        "ID": 10002703,
        "tier": 3,
        "passGroupID": 100027,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002801: _tools.RODict({
        "ID": 10002801,
        "tier": 1,
        "passGroupID": 100028,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002802: _tools.RODict({
        "ID": 10002802,
        "tier": 2,
        "passGroupID": 100028,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002803: _tools.RODict({
        "ID": 10002803,
        "tier": 3,
        "passGroupID": 100028,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    }),
    10002901: _tools.RODict({
        "ID": 10002901,
        "tier": 1,
        "passGroupID": 100029,
        "rewardGroupID": 9001,
        "privilege": (0, 0, 0)
    }),
    10002902: _tools.RODict({
        "ID": 10002902,
        "tier": 2,
        "passGroupID": 100029,
        "rewardGroupID": 9002,
        "privilege": (0, 2, 5)
    }),
    10002903: _tools.RODict({
        "ID": 10002903,
        "tier": 3,
        "passGroupID": 100029,
        "rewardGroupID": 9003,
        "privilege": (0, 4, 10)
    })
})
minKey = 10001101
maxKey = 26110103