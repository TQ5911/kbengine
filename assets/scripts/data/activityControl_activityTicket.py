# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: activityControl/activityTicket
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab


import utils
import random
import math
datas = _tools.RODict({ 
    101: _tools.RODict({
        "ID": 101,
        "type": 1,
        "price": (30000021, 0),
        "newServePrice": None,
        "newPlayerPrice": None
    }),
    102: _tools.RODict({
        "ID": 102,
        "type": 1,
        "price": (30000021, 50),
        "newServePrice": None,
        "newPlayerPrice": (40, 30000021, 25)
    }),
    201: _tools.RODict({
        "ID": 201,
        "type": 2,
        "price": (30000021, 0),
        "newServePrice": None,
        "newPlayerPrice": None
    }),
    202: _tools.RODict({
        "ID": 202,
        "type": 2,
        "price": (30000021, 50),
        "newServePrice": None,
        "newPlayerPrice": (40, 30000021, 25)
    }),
    203: _tools.RODict({
        "ID": 203,
        "type": 2,
        "price": (30000021, 100),
        "newServePrice": None,
        "newPlayerPrice": (40, 30000021, 50)
    }),
    301: _tools.RODict({
        "ID": 301,
        "type": 3,
        "price": (30000021, 50),
        "newServePrice": (30, 30000021, 0),
        "newPlayerPrice": None
    }),
    302: _tools.RODict({
        "ID": 302,
        "type": 3,
        "price": (30000021, 50),
        "newServePrice": None,
        "newPlayerPrice": None
    }),
    401: _tools.RODict({
        "ID": 401,
        "type": 4,
        "price": (30000021, 0),
        "newServePrice": None,
        "newPlayerPrice": None
    }),
    402: _tools.RODict({
        "ID": 402,
        "type": 4,
        "price": (30000021, 0),
        "newServePrice": None,
        "newPlayerPrice": None
    }),
    403: _tools.RODict({
        "ID": 403,
        "type": 4,
        "price": (30000021, 50),
        "newServePrice": None,
        "newPlayerPrice": None
    }),
    501: _tools.RODict({
        "ID": 501,
        "type": 5,
        "price": (30000021, 0),
        "newServePrice": None,
        "newPlayerPrice": None
    }),
    502: _tools.RODict({
        "ID": 502,
        "type": 5,
        "price": (30000021, 50),
        "newServePrice": None,
        "newPlayerPrice": None
    })
})
minKey = 101
maxKey = 502


ticketIdDic = _tools.RODict({
    1 : _tools.ROList([
        101,
        102,
    ]),
    2 : _tools.ROList([
        201,
        202,
        203,
    ]),
    3 : _tools.ROList([
        301,
        302,
    ]),
    4 : _tools.ROList([
        401,
        402,
        403,
    ]),
    5 : _tools.ROList([
        501,
        502,
    ]),
})
freeTicketDic = _tools.RODict({
    1 : _tools.ROList([
        101,
    ]),
    2 : _tools.ROList([
        201,
    ]),
    3 : _tools.ROList([
    ]),
    4 : _tools.ROList([
        401,
        402,
    ]),
    5 : _tools.ROList([
        501,
    ]),
})
paidTicketDic = _tools.RODict({
    1 : _tools.ROList([
        102,
    ]),
    2 : _tools.ROList([
        202,
        203,
    ]),
    3 : _tools.ROList([
        301,
        302,
    ]),
    4 : _tools.ROList([
        403,
    ]),
    5 : _tools.ROList([
        502,
    ]),
})