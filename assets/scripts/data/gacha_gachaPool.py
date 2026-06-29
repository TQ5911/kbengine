# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gacha/gachaPool
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    101: _tools.RODict({
        "ID": 101,
        "name": "精英召唤",
        "poolGroupId": 101,
        "timeLimit": 0,
        "startTime": "",
        "endTime": "",
        "1rollCostCoin": None,
        "1rollCost": ((30000235, 1),),
        "10rollCost": ((30000235, 10),),
        "100rollCost": ((30000235, 100),),
        "1rollReward": 40020672,
        "10rollReward": 40020673,
        "ifPityWork": 1,
        "pityPullCount": 1000,
        "pityReset": (1, 0, 3),
        "pityReward": 30000330,
        "pityInfo": 29
    }),
    102: _tools.RODict({
        "ID": 102,
        "name": "普通召唤",
        "poolGroupId": 102,
        "timeLimit": 0,
        "startTime": "",
        "endTime": "",
        "1rollCostCoin": ((30000002, 10000),),
        "1rollCost": ((30000320, 1),),
        "10rollCost": ((30000320, 10),),
        "100rollCost": ((30000320, 100),),
        "1rollReward": 40020675,
        "10rollReward": 40020676,
        "ifPityWork": 0,
        "pityPullCount": 1000,
        "pityReset": (1, 0, 3),
        "pityReward": 30000330,
        "pityInfo": 71
    })
})
minKey = 101
maxKey = 102