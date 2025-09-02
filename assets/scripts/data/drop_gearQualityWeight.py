# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: drop/gearQualityWeight
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    0: _tools.RODict({
        "ID": 0,
        "weight": 0,
        "Probability": lambda oWeight, qualityID, creepMD,creepLv:oWeight
    }),
    1: _tools.RODict({
        "ID": 1,
        "weight": 1500,
        "Probability": lambda oWeight, qualityID, creepMD,creepLv:oWeight
    }),
    2: _tools.RODict({
        "ID": 2,
        "weight": 350,
        "Probability": lambda oWeight, qualityID, creepMD,creepLv:oWeight*(1+creepMD*0.03)*max(1-max((creepLv-30),0)*4/20,1)
    }),
    3: _tools.RODict({
        "ID": 3,
        "weight": 110,
        "Probability": lambda oWeight, qualityID, creepMD,creepLv:oWeight*(1+creepMD*0.03)*max(1-max((creepLv-30),0)*4/20,1)
    }),
    4: _tools.RODict({
        "ID": 4,
        "weight": 40,
        "Probability": lambda oWeight, qualityID, creepMD,creepLv:oWeight*(1+creepMD*0.03)
    }),
    5: _tools.RODict({
        "ID": 5,
        "weight": 0,
        "Probability": lambda oWeight, qualityID, creepMD,creepLv:oWeight*(1+creepMD*0.03)
    })
})
minKey = 0
maxKey = 5