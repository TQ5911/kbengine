# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: soul/soulLevel
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "level": 1,
        "range": (1, 4),
        "probability": (1250, 167),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 1000,
        "consume3": 1000
    }),
    2: _tools.RODict({
        "level": 2,
        "range": (1, 2, 5),
        "probability": (2000, 1250, 167),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 1000,
        "consume3": 1000
    }),
    3: _tools.RODict({
        "level": 3,
        "range": (1, 2, 3, 6),
        "probability": (3500, 2000, 1250, 167),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 1000,
        "consume3": 1000
    }),
    4: _tools.RODict({
        "level": 4,
        "range": (1, 2, 3, 4, 7),
        "probability": (2000, 3500, 2000, 1250, 167),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 1000,
        "consume3": 1000
    }),
    5: _tools.RODict({
        "level": 5,
        "range": (1, 2, 3, 4, 5, 8),
        "probability": (1000, 2000, 3500, 2000, 1250, 167),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 1000,
        "consume3": 1000
    }),
    6: _tools.RODict({
        "level": 6,
        "range": (1, 2, 3, 4, 5, 6, 9),
        "probability": (600, 1500, 2000, 3500, 2000, 333, 67),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 2000,
        "consume3": 2000
    }),
    7: _tools.RODict({
        "level": 7,
        "range": (2, 3, 4, 5, 6, 7, 10),
        "probability": (600, 1500, 2000, 3500, 2000, 333, 67),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 2000,
        "consume3": 2000
    }),
    8: _tools.RODict({
        "level": 8,
        "range": (3, 4, 5, 6, 7, 8, 11),
        "probability": (600, 1500, 2000, 3500, 2000, 333, 67),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 2000,
        "consume3": 2000
    }),
    9: _tools.RODict({
        "level": 9,
        "range": (4, 5, 6, 7, 8, 9, 12),
        "probability": (600, 1500, 2000, 3500, 2000, 333, 67),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 2000,
        "consume3": 2000
    }),
    10: _tools.RODict({
        "level": 10,
        "range": (5, 6, 7, 8, 9, 10, 13),
        "probability": (600, 1500, 2000, 3500, 2000, 333, 67),
        "atkBlessWeight": (0, 0),
        "loseWeight": 900000,
        "atkBlessWeight2": (0, 0),
        "loseWeight2": 900000,
        "consume1": 0,
        "consume2": 2000,
        "consume3": 2000
    }),
    11: _tools.RODict({
        "level": 11,
        "range": (6, 7, 8, 9, 10, 11, 14),
        "probability": (760, 1500, 2000, 3500, 2000, 200, 40),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (400, 27),
        "loseWeight2": 900000,
        "consume1": 30,
        "consume2": 3000,
        "consume3": 3000
    }),
    12: _tools.RODict({
        "level": 12,
        "range": (7, 8, 9, 10, 11, 12, 15),
        "probability": (760, 1500, 2000, 3500, 2000, 200, 40),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (400, 27),
        "loseWeight2": 900000,
        "consume1": 30,
        "consume2": 3000,
        "consume3": 3000
    }),
    13: _tools.RODict({
        "level": 13,
        "range": (8, 9, 10, 11, 12, 13, 16),
        "probability": (760, 1500, 2000, 3500, 2000, 200, 40),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (400, 27),
        "loseWeight2": 900000,
        "consume1": 30,
        "consume2": 3000,
        "consume3": 3000
    }),
    14: _tools.RODict({
        "level": 14,
        "range": (9, 10, 11, 12, 13, 14, 17),
        "probability": (760, 1500, 2000, 3500, 2000, 200, 40),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (400, 27),
        "loseWeight2": 900000,
        "consume1": 30,
        "consume2": 3000,
        "consume3": 3000
    }),
    15: _tools.RODict({
        "level": 15,
        "range": (10, 11, 12, 13, 14, 15, 18),
        "probability": (760, 1500, 2000, 3500, 2000, 200, 40),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (400, 27),
        "loseWeight2": 900000,
        "consume1": 30,
        "consume2": 3000,
        "consume3": 3000
    }),
    16: _tools.RODict({
        "level": 16,
        "range": (11, 12, 13, 14, 15, 16, 21),
        "probability": (840, 1500, 2000, 3500, 2000, 133, 27),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    }),
    17: _tools.RODict({
        "level": 17,
        "range": (12, 13, 14, 15, 16, 17, 21),
        "probability": (840, 1500, 2000, 3500, 2000, 133, 27),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    }),
    18: _tools.RODict({
        "level": 18,
        "range": (13, 14, 15, 16, 17, 18, 21),
        "probability": (840, 1500, 2000, 3500, 2000, 133, 27),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    }),
    19: _tools.RODict({
        "level": 19,
        "range": (13, 14, 15, 16, 17, 18, 24),
        "probability": (840, 1500, 2000, 3500, 2000, 133, 27),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    }),
    20: _tools.RODict({
        "level": 20,
        "range": (13, 14, 15, 16, 17, 18, 24),
        "probability": (840, 1500, 2000, 3500, 2000, 133, 27),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    }),
    21: _tools.RODict({
        "level": 21,
        "range": (14, 15, 16, 17, 18, 21, 24),
        "probability": (840, 1500, 2000, 3500, 2000, 133, 27),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    }),
    22: _tools.RODict({
        "level": 22,
        "range": (14, 15, 16, 17, 18, 21, 24),
        "probability": (840, 1500, 2000, 3500, 2000, 133, 27),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    }),
    23: _tools.RODict({
        "level": 23,
        "range": (14, 15, 16, 17, 18, 21, 24),
        "probability": (840, 1500, 2000, 3500, 2000, 133, 27),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    }),
    24: _tools.RODict({
        "level": 24,
        "range": (15, 16, 17, 18, 21, 24),
        "probability": (840, 1500, 2000, 3500, 2000, 160),
        "atkBlessWeight": (800, 80),
        "loseWeight": 900000,
        "atkBlessWeight2": (1000, 67),
        "loseWeight2": 900000,
        "consume1": 60,
        "consume2": 6000,
        "consume3": 6000
    })
})
minKey = 1
maxKey = 24