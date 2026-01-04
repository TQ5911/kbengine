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
        "dunID": 2201,
        "firstReward": 40038601,
        "clearReward": 40038801,
        "goldReward": 40039001,
    }),
    2: _tools.RODict({
        "ID": 2,
        "dunID": 2202,
        "firstReward": 40038602,
        "clearReward": 40038802,
        "goldReward": 40039002,
    }),
    3: _tools.RODict({
        "ID": 3,
        "dunID": 2203,
        "firstReward": 40038603,
        "clearReward": 40038803,
        "goldReward": 40039003,
    })
})
minKey = 1
maxKey = 3

fistPassRewardDic = {2201: 40038601, 2202: 40038602, 2203: 40038603}


clearPassRewardDic = {2201: 40038801, 2202: 40038802, 2203: 40038803}


goldPassRewardDic = {2201: 40039001, 2202: 40039002, 2203: 40039003}


dungeonIdxDic = {2201: 1, 2202: 2, 2203: 3}
