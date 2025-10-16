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
        "name": "精灵召唤",
        "poolGroupId": 101,
        "timeLimit": 0,
        "startTime": "",
        "endTime": "",
        "1rollCost": ((30000235, 1),),
        "10rollCost": ((30000235, 10),),
        "100rollCost": ((30000235, 100),),
        "1rollReward": 40020672,
        "10rollReward": 40020673,
        "dailyLimit": 300,
        "pityPullCount": 30,
        "pityReset": (1, 0, 3),
        "pityReward": 30000330,
        "pityInfo": 29
    }),
    201: _tools.RODict({
        "ID": 201,
        "name": "传说精灵召唤",
        "poolGroupId": 1,
        "timeLimit": 0,
        "startTime": "20250922000000",
        "endTime": "20250928235959",
        "1rollCost": ((30000320, 1),),
        "10rollCost": ((30000320, 10),),
        "100rollCost": ((30000320, 100),),
        "1rollReward": 40020675,
        "10rollReward": 40020676,
        "dailyLimit": 500,
        "pityPullCount": 200,
        "pityReset": (1, 0, 4),
        "pityReward": 30000330,
        "pityInfo": 29
    }),
    202: _tools.RODict({
        "ID": 202,
        "name": "传说精灵召唤",
        "poolGroupId": 1,
        "timeLimit": 0,
        "startTime": "20250929000000",
        "endTime": "20251005235959",
        "1rollCost": ((30000320, 1),),
        "10rollCost": ((30000320, 10),),
        "100rollCost": ((30000320, 100),),
        "1rollReward": 40020675,
        "10rollReward": 40020676,
        "dailyLimit": 500,
        "pityPullCount": 200,
        "pityReset": (1, 0, 4),
        "pityReward": 30000330,
        "pityInfo": 29
    }),
    301: _tools.RODict({
        "ID": 301,
        "name": "限时精灵召唤",
        "poolGroupId": 301,
        "timeLimit": 1,
        "startTime": "20250901000000",
        "endTime": "20250930235959",
        "1rollCost": ((30000320, 1),),
        "10rollCost": ((30000320, 10),),
        "100rollCost": ((30000320, 100),),
        "1rollReward": 40020675,
        "10rollReward": 40020676,
        "dailyLimit": 500,
        "pityPullCount": 200,
        "pityReset": (1, 0, 4),
        "pityReward": 30000330,
        "pityInfo": 29
    })
})
minKey = 101
maxKey = 301