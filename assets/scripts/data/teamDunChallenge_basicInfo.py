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
        "name": "深海禁地",
        "dunID": 2101,
        "firstReward": 40038001,
        "clearReward": 40038201,
        "goldReward": 40038401,
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "亡者之村",
        "dunID": 2104,
        "firstReward": 40038003,
        "clearReward": 40038203,
        "goldReward": 40038403,
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "深渊魔坛",
        "dunID": 2102,
        "firstReward": 40038002,
        "clearReward": 40038202,
        "goldReward": 40038402,
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "万毒虫窟",
        "dunID": 2103,
        "firstReward": 40038003,
        "clearReward": 40038203,
        "goldReward": 40038403,
    })
})
minKey = 1
maxKey = 4

fistPassRewardDic = {2101: 40038001, 2104: 40038003, 2102: 40038002, 2103: 40038003}


clearPassRewardDic = {2101: 40038201, 2104: 40038203, 2102: 40038202, 2103: 40038203}


goldPassRewardDic = {2101: 40038401, 2104: 40038403, 2102: 40038402, 2103: 40038403}


dungeonIdxDic = {2101: 1, 2104: 2, 2102: 3, 2103: 4}
