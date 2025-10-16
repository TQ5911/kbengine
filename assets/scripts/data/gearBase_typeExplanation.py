# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearBase/typeExplanation
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    11: _tools.RODict({
        "ID": 11,
        "type": 1,
        "SubType": 11,
        "Name": "道士武器",
        "RemindClass": 1001,
        "weight": 100,
        "slot": 1,
        "recommendClass": 1001
    }),
    12: _tools.RODict({
        "ID": 12,
        "type": 1,
        "SubType": 12,
        "Name": "法师武器",
        "RemindClass": 1002,
        "weight": 100,
        "slot": 1,
        "recommendClass": 1002
    }),
    13: _tools.RODict({
        "ID": 13,
        "type": 1,
        "SubType": 13,
        "Name": "战士武器",
        "RemindClass": 1003,
        "weight": 100,
        "slot": 1,
        "recommendClass": 1003
    }),
    21: _tools.RODict({
        "ID": 21,
        "type": 2,
        "SubType": 21,
        "Name": "道士衣服",
        "RemindClass": 1001,
        "weight": 100,
        "slot": 2,
        "recommendClass": 1001
    }),
    22: _tools.RODict({
        "ID": 22,
        "type": 2,
        "SubType": 22,
        "Name": "法师衣服",
        "RemindClass": 1002,
        "weight": 100,
        "slot": 2,
        "recommendClass": 1002
    }),
    23: _tools.RODict({
        "ID": 23,
        "type": 2,
        "SubType": 23,
        "Name": "战士衣服",
        "RemindClass": 1003,
        "weight": 100,
        "slot": 2,
        "recommendClass": 1003
    }),
    31: _tools.RODict({
        "ID": 31,
        "type": 3,
        "SubType": 31,
        "Name": "道士头盔",
        "RemindClass": 1001,
        "weight": 100,
        "slot": 3,
        "recommendClass": 1001
    }),
    32: _tools.RODict({
        "ID": 32,
        "type": 3,
        "SubType": 32,
        "Name": "法师头盔",
        "RemindClass": 1002,
        "weight": 100,
        "slot": 3,
        "recommendClass": 1002
    }),
    33: _tools.RODict({
        "ID": 33,
        "type": 3,
        "SubType": 33,
        "Name": "战士头盔",
        "RemindClass": 1003,
        "weight": 100,
        "slot": 3,
        "recommendClass": 1003
    }),
    41: _tools.RODict({
        "ID": 41,
        "type": 4,
        "SubType": 41,
        "Name": "道士鞋子",
        "RemindClass": 1001,
        "weight": 100,
        "slot": 4,
        "recommendClass": 1001
    }),
    42: _tools.RODict({
        "ID": 42,
        "type": 4,
        "SubType": 42,
        "Name": "法师鞋子",
        "RemindClass": 1002,
        "weight": 100,
        "slot": 4,
        "recommendClass": 1002
    }),
    43: _tools.RODict({
        "ID": 43,
        "type": 4,
        "SubType": 43,
        "Name": "战士鞋子",
        "RemindClass": 1003,
        "weight": 100,
        "slot": 4,
        "recommendClass": 1003
    }),
    58: _tools.RODict({
        "ID": 58,
        "type": 5,
        "SubType": 58,
        "Name": "项链",
        "RemindClass": 0,
        "weight": 40,
        "slot": 5,
        "recommendClass": (1001, 1002, 1003)
    }),
    59: _tools.RODict({
        "ID": 59,
        "type": 5,
        "SubType": 59,
        "Name": "法术项链",
        "RemindClass": 0,
        "weight": 40,
        "slot": 5,
        "recommendClass": (1001, 1002, 1003)
    }),
    68: _tools.RODict({
        "ID": 68,
        "type": 6,
        "SubType": 68,
        "Name": "物理戒指",
        "RemindClass": 0,
        "weight": 40,
        "slot": (6, 7),
        "recommendClass": (1001, 1002, 1003)
    }),
    69: _tools.RODict({
        "ID": 69,
        "type": 6,
        "SubType": 69,
        "Name": "法术戒指",
        "RemindClass": 0,
        "weight": 40,
        "slot": (6, 7),
        "recommendClass": (1001, 1002, 1003)
    }),
    70: _tools.RODict({
        "ID": 70,
        "type": 6,
        "SubType": 70,
        "Name": "道士戒指",
        "RemindClass": 0,
        "weight": 40,
        "slot": (6, 7),
        "recommendClass": (1001, 1002, 1003)
    }),
    78: _tools.RODict({
        "ID": 78,
        "type": 7,
        "SubType": 78,
        "Name": "物理手镯",
        "RemindClass": 0,
        "weight": 40,
        "slot": (8, 9),
        "recommendClass": (1001, 1002, 1003)
    }),
    79: _tools.RODict({
        "ID": 79,
        "type": 7,
        "SubType": 79,
        "Name": "法术手镯",
        "RemindClass": 0,
        "weight": 40,
        "slot": (8, 9),
        "recommendClass": (1001, 1002, 1003)
    }),
    80: _tools.RODict({
        "ID": 80,
        "type": 7,
        "SubType": 80,
        "Name": "防御手镯",
        "RemindClass": 0,
        "weight": 40,
        "slot": (8, 9),
        "recommendClass": (1001, 1002, 1003)
    }),
    81: _tools.RODict({
        "ID": 81,
        "type": 8,
        "SubType": 81,
        "Name": "道士腰带",
        "RemindClass": 1001,
        "weight": 100,
        "slot": 10,
        "recommendClass": 1001
    }),
    82: _tools.RODict({
        "ID": 82,
        "type": 8,
        "SubType": 82,
        "Name": "法师腰带",
        "RemindClass": 1002,
        "weight": 100,
        "slot": 10,
        "recommendClass": 1002
    }),
    83: _tools.RODict({
        "ID": 83,
        "type": 8,
        "SubType": 83,
        "Name": "战士腰带",
        "RemindClass": 1003,
        "weight": 100,
        "slot": 10,
        "recommendClass": 1003
    })
})
minKey = 11
maxKey = 83

dropTypeWeightList = {1001: [(11, 100), (21, 100), (31, 100), (41, 100), (81, 100)], 1002: [(12, 100), (22, 100), (32, 100), (42, 100), (82, 100)], 1003: [(13, 100), (23, 100), (33, 100), (43, 100), (83, 100)], 0: [(58, 40), (59, 40), (68, 40), (69, 40), (70, 40), (78, 40), (79, 40), (80, 40)]}



auctionDic = _tools.RODict({ 
        (1, 1001):[(1, 11)],
        (1, 1002):[(1, 12)],
        (1, 1003):[(1, 13)],
        (2, 1001):[(2, 21)],
        (2, 1002):[(2, 22)],
        (2, 1003):[(2, 23)],
        (3, 1001):[(3, 31)],
        (3, 1002):[(3, 32)],
        (3, 1003):[(3, 33)],
        (4, 1001):[(4, 41)],
        (4, 1002):[(4, 42)],
        (4, 1003):[(4, 43)],
        (5, 1001):[(5, 58), (5, 59)],
        (5, 1002):[(5, 58), (5, 59)],
        (5, 1003):[(5, 58), (5, 59)],
        (6, 1001):[(6, 68), (6, 69), (6, 70)],
        (6, 1002):[(6, 68), (6, 69), (6, 70)],
        (6, 1003):[(6, 68), (6, 69), (6, 70)],
        (7, 1001):[(7, 78), (7, 79), (7, 80)],
        (7, 1002):[(7, 78), (7, 79), (7, 80)],
        (7, 1003):[(7, 78), (7, 79), (7, 80)],
        (8, 1001):[(8, 81)],
        (8, 1002):[(8, 82)],
        (8, 1003):[(8, 83)],
})
