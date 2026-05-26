# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: activityControl/activityNotice
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
    1: _tools.RODict({
        "ID": 1,
        "name": "世界首领",
        "isOpen": 1,
        "timeMode": "timedRefresh",
        "refresh": 1,
        "bossID": 11227001,
        "preShowTime": 10,
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "矿区争夺战",
        "isOpen": 1,
        "timeMode": "",
        "refresh": 0,
        "bossID": 0,
        "preShowTime": 0,
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "新元城战",
        "isOpen": 1,
        "timeMode": "",
        "refresh": 0,
        "bossID": 0,
        "preShowTime": 0,
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "世界首领",
        "isOpen": 0,
        "timeMode": "timedRefresh",
        "refresh": 1,
        "bossID": 11237001,
        "preShowTime": 10,
    })
})
minKey = 1
maxKey = 4

bossIDSet = _tools.ROSet({11227001, 11237001, })


bossID2AnnoId = _tools.RODict({ 
        11227001:1,
        11237001:4,
})
