# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: teamDunChallenge/basicInfo
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
        "dunID": 2101,
        "firstReward": 40038001,
        "clearReward": 40038201,
        "goldReward": 40038401,
    }),
    2: _tools.RODict({
        "ID": 2,
        "dunID": 2102,
        "firstReward": 40038002,
        "clearReward": 40038202,
        "goldReward": 40038402,
    }),
    3: _tools.RODict({
        "ID": 3,
        "dunID": 2104,
        "firstReward": 40038003,
        "clearReward": 40038203,
        "goldReward": 40038403,
    })
})
minKey = 1
maxKey = 3

fistPassRewardDic = {2101: 40038001, 2102: 40038002, 2104: 40038003}


clearPassRewardDic = {2101: 40038201, 2102: 40038202, 2104: 40038203}


goldPassRewardDic = {2101: 40038401, 2102: 40038402, 2104: 40038403}


dungeonIdxDic = {2101: 1, 2102: 2, 2104: 3}
