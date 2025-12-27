# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: teamMatch/pointsRanking
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "dmg_level2Score5": _tools.RODict({
        "ID": "dmg_level2Score5",
        "value": ((1, 1, 80, 80), (2, 2, 70, 62), (3, 3, 60, 52), (4, 4, 50, 42), (5, 5, 40, 32)),
    }),
    "dmg_level2Score15": _tools.RODict({
        "ID": "dmg_level2Score15",
        "value": ((1, 3, 80, 80), (4, 6, 70, 62), (7, 9, 60, 52), (10, 12, 50, 42), (13, 15, 40, 32)),
    }),
    "addHp_level2Score_5": _tools.RODict({
        "ID": "addHp_level2Score_5",
        "value": ((1, 1, 20, 20), (2, 2, 10, 10), (3, 3, 5, 5), (4, 5, 0, 0)),
    }),
    "addHp_level2Score_15": _tools.RODict({
        "ID": "addHp_level2Score_15",
        "value": ((1, 3, 20, 20), (4, 6, 10, 10), (7, 9, 5, 5), (10, 15, 0, 0)),
    }),
    "hurt_level2Score_5": _tools.RODict({
        "ID": "hurt_level2Score_5",
        "value": ((1, 1, 20, 20), (2, 2, 10, 10), (3, 3, 5, 5), (4, 5, 0, 0)),
    }),
    "hurt_level2Score_15": _tools.RODict({
        "ID": "hurt_level2Score_15",
        "value": ((1, 3, 20, 20), (4, 6, 10, 10), (7, 9, 5, 5), (10, 15, 0, 0)),
    }),
    "playerDiedScore": _tools.RODict({
        "ID": "playerDiedScore",
        "value": -2,
    }),
    "upLevelValuePercent": _tools.RODict({
        "ID": "upLevelValuePercent",
        "value": 0.7,
    }),
    "scoreRank1": _tools.RODict({
        "ID": "scoreRank1",
        "value": ((999, 85), (84, 70), (69, 50), (49, 0)),
    }),
    "scoreRank2": _tools.RODict({
        "ID": "scoreRank2",
        "value": ('S', 'A', 'B', 'C'),
    })
})