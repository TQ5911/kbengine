# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: appearance/ModelResource
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    100003002: _tools.RODict({
        "ID": 100003002,
        "part": 3,
        "appearanceId": 2,
        "name": "灵韵山海",
        "prop": _tools.ROList([['adjFullHp', 50], ['adjHit', 2], ['adjDodge', 2]]),
        "event": "Openinterface",
        "param": "UIPayStorePanel,2003,0",
        "isOpen": 1
    }),
    200003002: _tools.RODict({
        "ID": 200003002,
        "part": 3,
        "appearanceId": 2,
        "name": "灵韵山海(体验)",
        "prop": None,
        "event": "Openinterface",
        "param": "UIPayStorePanel,2003,0",
        "isOpen": 1
    }),
    100001001: _tools.RODict({
        "ID": 100001001,
        "part": 3,
        "appearanceId": 5,
        "name": "仲夏之梦",
        "prop": _tools.ROList([['adjFullHp', 100], ['adjHit', 5], ['adjDodge', 5]]),
        "event": "Openinterface",
        "param": "UIPayStorePanel,2003,0",
        "isOpen": 1
    })
})
minKey = 100001001
maxKey = 200003002

outfitId2appeId = {2: 100003002, 5: 100001001}
