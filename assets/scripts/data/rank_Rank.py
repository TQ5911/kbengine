# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: rank/Rank
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
        "name": "等级",
        "isOpen": 1,
        "shoolFilter": 1,
        "topListMgrClassType": 1,
        "minLevel": 15,
        "displayNum": 100,
        "maxNum": 3000
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "战力",
        "isOpen": 1,
        "shoolFilter": 1,
        "topListMgrClassType": 1,
        "minLevel": 15,
        "displayNum": 100,
        "maxNum": 3000
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "帮会",
        "isOpen": 1,
        "shoolFilter": 0,
        "topListMgrClassType": 2,
        "minLevel": 0,
        "displayNum": 50,
        "maxNum": 100
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "成就点",
        "isOpen": 1,
        "shoolFilter": 0,
        "topListMgrClassType": 1,
        "minLevel": 15,
        "displayNum": 100,
        "maxNum": 3000
    })
})
minKey = 1
maxKey = 4