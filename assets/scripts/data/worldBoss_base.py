# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: worldBoss/base
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
        "localMapID": 1036,
        "localBossID": 10360001,
        "crossMapID": 1036,
        "crossBossID": 10360001,
        "isCross": 0
    }),
    2: _tools.RODict({
        "ID": 2,
        "localMapID": 1026,
        "localBossID": 10260001,
        "crossMapID": 5302,
        "crossBossID": 53020001,
        "isCross": 1
    }),
    3: _tools.RODict({
        "ID": 3,
        "localMapID": 1126,
        "localBossID": 11260001,
        "crossMapID": 5303,
        "crossBossID": 53030001,
        "isCross": 1
    })
})
minKey = 1
maxKey = 3


allLocal2CrossMap = _tools.RODict({
    1036 : 1036,
    1026 : 5302,
    1126 : 5303,
})
allCross2localMap = _tools.RODict({
    1036 : 1036,
    5302 : 1026,
    5303 : 1126,
})
allLocal2BossSId = _tools.RODict({
    1036 : 1,
    1026 : 2,
    1126 : 3,
})
allCross2BossSId = _tools.RODict({
    1036 : 1,
    5302 : 2,
    5303 : 3,
})
local2CrossMap = _tools.RODict({
    1026 : 5302,
    1126 : 5303,
})
cross2LocalMap = _tools.RODict({
    5302 : 1026,
    5303 : 1126,
})
local2BossSId = _tools.RODict({
    1026 : 2,
    1126 : 3,
})
cross2BossSId = _tools.RODict({
    5302 : 2,
    5303 : 3,
})