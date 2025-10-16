# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: skill/specialMonsterAI
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    305001: _tools.RODict({
        "ID": 305001,
        "name": "虫卵8012_11",
        "bornAnimation": "born",
        "bornAnimationTime": 1.8,
        "resetAnimation": "",
        "resetAnimationTime": 0.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 11981205,
        "summonCD": 3.0,
        "summonLimit": 3
    }),
    305101: _tools.RODict({
        "ID": 305101,
        "name": "沙虫8003_00",
        "bornAnimation": "born",
        "bornAnimationTime": 1.33,
        "resetAnimation": "reset",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 5.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305201: _tools.RODict({
        "ID": 305201,
        "name": "雕塑7001_90",
        "bornAnimation": "born1",
        "bornAnimationTime": 2.1,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305202: _tools.RODict({
        "ID": 305202,
        "name": "雕塑7001_90",
        "bornAnimation": "born2",
        "bornAnimationTime": 1.8,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305203: _tools.RODict({
        "ID": 305203,
        "name": "雕塑7001_91",
        "bornAnimation": "born1",
        "bornAnimationTime": 1.767,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305204: _tools.RODict({
        "ID": 305204,
        "name": "雕塑7001_91",
        "bornAnimation": "born2",
        "bornAnimationTime": 1.967,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305205: _tools.RODict({
        "ID": 305205,
        "name": "雕塑7001_92",
        "bornAnimation": "born1",
        "bornAnimationTime": 1.767,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305206: _tools.RODict({
        "ID": 305206,
        "name": "雕塑7001_92",
        "bornAnimation": "born2",
        "bornAnimationTime": 1.933,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305207: _tools.RODict({
        "ID": 305207,
        "name": "雕塑7002_90",
        "bornAnimation": "born1",
        "bornAnimationTime": 2.0,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305208: _tools.RODict({
        "ID": 305208,
        "name": "雕塑7002_90",
        "bornAnimation": "born2",
        "bornAnimationTime": 1.733,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305209: _tools.RODict({
        "ID": 305209,
        "name": "雕塑7002_91",
        "bornAnimation": "born1",
        "bornAnimationTime": 2.133,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305210: _tools.RODict({
        "ID": 305210,
        "name": "雕塑7002_91",
        "bornAnimation": "born2",
        "bornAnimationTime": 2.133,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305211: _tools.RODict({
        "ID": 305211,
        "name": "雕塑7002_92",
        "bornAnimation": "born1",
        "bornAnimationTime": 2.133,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305212: _tools.RODict({
        "ID": 305212,
        "name": "雕塑7002_92",
        "bornAnimation": "born2",
        "bornAnimationTime": 2.1,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305213: _tools.RODict({
        "ID": 305213,
        "name": "雕塑7003_90",
        "bornAnimation": "born1",
        "bornAnimationTime": 1.667,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305214: _tools.RODict({
        "ID": 305214,
        "name": "雕塑7003_90",
        "bornAnimation": "born2",
        "bornAnimationTime": 1.767,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305215: _tools.RODict({
        "ID": 305215,
        "name": "雕塑7003_91",
        "bornAnimation": "born1",
        "bornAnimationTime": 2.1,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305216: _tools.RODict({
        "ID": 305216,
        "name": "雕塑7003_91",
        "bornAnimation": "born2",
        "bornAnimationTime": 1.733,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305217: _tools.RODict({
        "ID": 305217,
        "name": "雕塑7003_92",
        "bornAnimation": "born1",
        "bornAnimationTime": 2.1,
        "resetAnimation": "reset1",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    }),
    305218: _tools.RODict({
        "ID": 305218,
        "name": "雕塑7003_92",
        "bornAnimation": "born2",
        "bornAnimationTime": 1.767,
        "resetAnimation": "reset2",
        "resetAnimationTime": 1.0,
        "resetCdAfterCombat": 0.0,
        "summonID": 0,
        "summonCD": 0.0,
        "summonLimit": 0
    })
})
minKey = 305001
maxKey = 305218