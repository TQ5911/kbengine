# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: worldBoss/onlinePlayersEffect
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab


import utils
import random
import math
datas = _tools.RODict({ 
    0: _tools.RODict({
        "onlinePlayers": 0,
        "chestSpawnRate": 0.2,
        "lightSpawnRate": 0.2
    }),
    500: _tools.RODict({
        "onlinePlayers": 500,
        "chestSpawnRate": 0.3,
        "lightSpawnRate": 0.3
    }),
    1000: _tools.RODict({
        "onlinePlayers": 1000,
        "chestSpawnRate": 0.5,
        "lightSpawnRate": 0.5
    }),
    1500: _tools.RODict({
        "onlinePlayers": 1500,
        "chestSpawnRate": 1.0,
        "lightSpawnRate": 1.0
    }),
    2000: _tools.RODict({
        "onlinePlayers": 2000,
        "chestSpawnRate": 1.0,
        "lightSpawnRate": 1.0
    }),
    2500: _tools.RODict({
        "onlinePlayers": 2500,
        "chestSpawnRate": 1.5,
        "lightSpawnRate": 1.5
    }),
    3000: _tools.RODict({
        "onlinePlayers": 3000,
        "chestSpawnRate": 1.5,
        "lightSpawnRate": 1.5
    })
})
minKey = 0
maxKey = 3000


onlineNumList = _tools.ROList([
    0,
    500,
    1000,
    1500,
    2000,
    2500,
    3000,
])