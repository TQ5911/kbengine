# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: raidBossChallenge/basicInfo
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "ID": 1,
        "name": "弃天战狂",
        "dunID": 2204,
        "firstReward": 40038601,
        "clearReward": 40038801,
        "goldReward": 40039001,
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "阴阳鬼判",
        "dunID": 2201,
        "firstReward": 40038602,
        "clearReward": 40038802,
        "goldReward": 40039002,
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "双生海妖",
        "dunID": 2202,
        "firstReward": 40038603,
        "clearReward": 40038803,
        "goldReward": 40039003,
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "熔岩三头蛟",
        "dunID": 2203,
        "firstReward": 40038604,
        "clearReward": 40038804,
        "goldReward": 40039004,
    })
})
minKey = 1
maxKey = 4

fistPassRewardDic = {2204: 40038601, 2201: 40038602, 2202: 40038603, 2203: 40038604}


clearPassRewardDic = {2204: 40038801, 2201: 40038802, 2202: 40038803, 2203: 40038804}


goldPassRewardDic = {2204: 40039001, 2201: 40039002, 2202: 40039003, 2203: 40039004}


dungeonIdxDic = {2204: 1, 2201: 2, 2202: 3, 2203: 4}
