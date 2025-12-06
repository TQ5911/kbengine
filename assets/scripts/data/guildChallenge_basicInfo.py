# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guildChallenge/basicInfo
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
        "yanWuGeLvReq": 1,
        "name": "普通",
        "dunID": 2301,
        "bossID": 11226001,
        "minScore": 5900,
        "guildCoinCost": 2000,
        "guildMoneyCost": 1000,
        "firstReward": 40020541,
    }),
    2: _tools.RODict({
        "ID": 2,
        "yanWuGeLvReq": 2,
        "name": "精英",
        "dunID": 2302,
        "bossID": 11226001,
        "minScore": 8300,
        "guildCoinCost": 4000,
        "guildMoneyCost": 2000,
        "firstReward": 40020542,
    }),
    3: _tools.RODict({
        "ID": 3,
        "yanWuGeLvReq": 3,
        "name": "困难",
        "dunID": 2303,
        "bossID": 11226001,
        "minScore": 12000,
        "guildCoinCost": 8000,
        "guildMoneyCost": 4000,
        "firstReward": 40020543,
    })
})
minKey = 1
maxKey = 3

dungeonIdxDic = {2301: 1, 2302: 2, 2303: 3}


fistPassRewardDic = {2301: 40020541, 2302: 40020542, 2303: 40020543}
