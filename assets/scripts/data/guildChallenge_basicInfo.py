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
        "bossID": 11051001,
        "minScore": 17500,
        "guildCoinCost": 30000,
        "guildMoneyCost": 2000,
        "firstReward": 40015001,
    }),
    2: _tools.RODict({
        "ID": 2,
        "yanWuGeLvReq": 3,
        "name": "困难",
        "dunID": 2302,
        "bossID": 11051001,
        "minScore": 30000,
        "guildCoinCost": 45000,
        "guildMoneyCost": 3000,
        "firstReward": 40015001,
    }),
    3: _tools.RODict({
        "ID": 3,
        "yanWuGeLvReq": 5,
        "name": "噩梦",
        "dunID": 2303,
        "bossID": 11051001,
        "minScore": 45000,
        "guildCoinCost": 60000,
        "guildMoneyCost": 4000,
        "firstReward": 40015001,
    })
})
minKey = 1
maxKey = 3

dungeonIdxDic = {2301: 1, 2302: 2, 2303: 3}


fistPassRewardDic = {2301: 40015001, 2302: 40015001, 2303: 40015001}
