# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: drop/drop_sub_package
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
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80792001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 900,
        "bindWeight": 5000
    }),
    2: _tools.RODict({
        "ID": 2,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80792002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 90,
        "bindWeight": 5000
    }),
    3: _tools.RODict({
        "ID": 3,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80792003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 90,
        "bindWeight": 5000
    }),
    4: _tools.RODict({
        "ID": 4,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80792004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 400,
        "bindWeight": 5000
    }),
    5: _tools.RODict({
        "ID": 5,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80793001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 5000
    }),
    6: _tools.RODict({
        "ID": 6,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80793002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 5000
    }),
    7: _tools.RODict({
        "ID": 7,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80793003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 5000
    }),
    8: _tools.RODict({
        "ID": 8,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80793004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 5000
    }),
    9: _tools.RODict({
        "ID": 9,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80793005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    10: _tools.RODict({
        "ID": 10,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80794001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    11: _tools.RODict({
        "ID": 11,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80794002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    12: _tools.RODict({
        "ID": 12,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80794003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 100,
        "bindWeight": 5000
    }),
    13: _tools.RODict({
        "ID": 13,
        "dropPackage": 10041,
        "dropCondition": None,
        "dropTarget": 80795001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 10,
        "bindWeight": 5000
    }),
    14: _tools.RODict({
        "ID": 14,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80703001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 900,
        "bindWeight": 5000
    }),
    15: _tools.RODict({
        "ID": 15,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80703002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 90,
        "bindWeight": 5000
    }),
    16: _tools.RODict({
        "ID": 16,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80703003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 90,
        "bindWeight": 5000
    }),
    17: _tools.RODict({
        "ID": 17,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80703004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 400,
        "bindWeight": 5000
    }),
    18: _tools.RODict({
        "ID": 18,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80703005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 5000
    }),
    19: _tools.RODict({
        "ID": 19,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80704001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 5000
    }),
    20: _tools.RODict({
        "ID": 20,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80704002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 5000
    }),
    21: _tools.RODict({
        "ID": 21,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80704003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 5000
    }),
    22: _tools.RODict({
        "ID": 22,
        "dropPackage": 10042,
        "dropCondition": None,
        "dropTarget": 80705002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    23: _tools.RODict({
        "ID": 23,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80111001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    24: _tools.RODict({
        "ID": 24,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80121001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    25: _tools.RODict({
        "ID": 25,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80131001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    26: _tools.RODict({
        "ID": 26,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80211001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    27: _tools.RODict({
        "ID": 27,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80221001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    28: _tools.RODict({
        "ID": 28,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80231001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    29: _tools.RODict({
        "ID": 29,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80311001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    30: _tools.RODict({
        "ID": 30,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80321001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    31: _tools.RODict({
        "ID": 31,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80331001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    32: _tools.RODict({
        "ID": 32,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80411001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    33: _tools.RODict({
        "ID": 33,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80421001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    34: _tools.RODict({
        "ID": 34,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80431001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    35: _tools.RODict({
        "ID": 35,
        "dropPackage": 1001,
        "dropCondition": None,
        "dropTarget": 80581001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    36: _tools.RODict({
        "ID": 36,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80111002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    37: _tools.RODict({
        "ID": 37,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80121002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    38: _tools.RODict({
        "ID": 38,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80131002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    39: _tools.RODict({
        "ID": 39,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80211002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    40: _tools.RODict({
        "ID": 40,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80221002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    41: _tools.RODict({
        "ID": 41,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80231002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    42: _tools.RODict({
        "ID": 42,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80311002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    43: _tools.RODict({
        "ID": 43,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80321002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    44: _tools.RODict({
        "ID": 44,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80331002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    45: _tools.RODict({
        "ID": 45,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80411002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    46: _tools.RODict({
        "ID": 46,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80421002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    47: _tools.RODict({
        "ID": 47,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80431002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    48: _tools.RODict({
        "ID": 48,
        "dropPackage": 1002,
        "dropCondition": None,
        "dropTarget": 80581002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    49: _tools.RODict({
        "ID": 49,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80111003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    50: _tools.RODict({
        "ID": 50,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80121003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    51: _tools.RODict({
        "ID": 51,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80131003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    52: _tools.RODict({
        "ID": 52,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80211003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    53: _tools.RODict({
        "ID": 53,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80221003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    54: _tools.RODict({
        "ID": 54,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80231003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    55: _tools.RODict({
        "ID": 55,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80311003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    56: _tools.RODict({
        "ID": 56,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80321003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    57: _tools.RODict({
        "ID": 57,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80331003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    58: _tools.RODict({
        "ID": 58,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80411003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    59: _tools.RODict({
        "ID": 59,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80421003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    60: _tools.RODict({
        "ID": 60,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80431003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    61: _tools.RODict({
        "ID": 61,
        "dropPackage": 1003,
        "dropCondition": None,
        "dropTarget": 80581003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    62: _tools.RODict({
        "ID": 62,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80112001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    63: _tools.RODict({
        "ID": 63,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80122001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    64: _tools.RODict({
        "ID": 64,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80132001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    65: _tools.RODict({
        "ID": 65,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80212001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    66: _tools.RODict({
        "ID": 66,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80222001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    67: _tools.RODict({
        "ID": 67,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80232001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    68: _tools.RODict({
        "ID": 68,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80312001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    69: _tools.RODict({
        "ID": 69,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80322001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    70: _tools.RODict({
        "ID": 70,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80332001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    71: _tools.RODict({
        "ID": 71,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80412001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    72: _tools.RODict({
        "ID": 72,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80422001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    73: _tools.RODict({
        "ID": 73,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80432001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    74: _tools.RODict({
        "ID": 74,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80582001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    75: _tools.RODict({
        "ID": 75,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80682001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    76: _tools.RODict({
        "ID": 76,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80692001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    77: _tools.RODict({
        "ID": 77,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80782001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    78: _tools.RODict({
        "ID": 78,
        "dropPackage": 1004,
        "dropCondition": None,
        "dropTarget": 80792001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    79: _tools.RODict({
        "ID": 79,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80112002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    80: _tools.RODict({
        "ID": 80,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80122002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    81: _tools.RODict({
        "ID": 81,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80132002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    82: _tools.RODict({
        "ID": 82,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80212002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    83: _tools.RODict({
        "ID": 83,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80222002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    84: _tools.RODict({
        "ID": 84,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80232002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    85: _tools.RODict({
        "ID": 85,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80312002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    86: _tools.RODict({
        "ID": 86,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80322002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    87: _tools.RODict({
        "ID": 87,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80332002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    88: _tools.RODict({
        "ID": 88,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80412002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    89: _tools.RODict({
        "ID": 89,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80422002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    90: _tools.RODict({
        "ID": 90,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80432002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    91: _tools.RODict({
        "ID": 91,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80582002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    92: _tools.RODict({
        "ID": 92,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80682002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    93: _tools.RODict({
        "ID": 93,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80692002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    94: _tools.RODict({
        "ID": 94,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80782002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    95: _tools.RODict({
        "ID": 95,
        "dropPackage": 1005,
        "dropCondition": None,
        "dropTarget": 80792002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    96: _tools.RODict({
        "ID": 96,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80112003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    97: _tools.RODict({
        "ID": 97,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80122003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    98: _tools.RODict({
        "ID": 98,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80132003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    99: _tools.RODict({
        "ID": 99,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80212003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    100: _tools.RODict({
        "ID": 100,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80222003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    101: _tools.RODict({
        "ID": 101,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80232003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    102: _tools.RODict({
        "ID": 102,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80312003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    103: _tools.RODict({
        "ID": 103,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80322003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    104: _tools.RODict({
        "ID": 104,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80332003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    105: _tools.RODict({
        "ID": 105,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80412003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    106: _tools.RODict({
        "ID": 106,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80422003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    107: _tools.RODict({
        "ID": 107,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80432003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    108: _tools.RODict({
        "ID": 108,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80582003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    109: _tools.RODict({
        "ID": 109,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80682003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    110: _tools.RODict({
        "ID": 110,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80692003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    111: _tools.RODict({
        "ID": 111,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80782003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    112: _tools.RODict({
        "ID": 112,
        "dropPackage": 1006,
        "dropCondition": None,
        "dropTarget": 80792003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    113: _tools.RODict({
        "ID": 113,
        "dropPackage": 1301,
        "dropCondition": None,
        "dropTarget": 30010021,
        "dropNumMin": 2,
        "dropNumMax": 6,
        "weight": 300,
        "bindWeight": 0
    }),
    114: _tools.RODict({
        "ID": 114,
        "dropPackage": 1301,
        "dropCondition": None,
        "dropTarget": 30010022,
        "dropNumMin": 2,
        "dropNumMax": 6,
        "weight": 300,
        "bindWeight": 0
    }),
    115: _tools.RODict({
        "ID": 115,
        "dropPackage": 1301,
        "dropCondition": None,
        "dropTarget": 30010023,
        "dropNumMin": 2,
        "dropNumMax": 6,
        "weight": 300,
        "bindWeight": 0
    }),
    116: _tools.RODict({
        "ID": 116,
        "dropPackage": 1301,
        "dropCondition": None,
        "dropTarget": 30010024,
        "dropNumMin": 2,
        "dropNumMax": 6,
        "weight": 300,
        "bindWeight": 0
    }),
    117: _tools.RODict({
        "ID": 117,
        "dropPackage": 1302,
        "dropCondition": None,
        "dropTarget": 30010021,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 300,
        "bindWeight": 0
    }),
    118: _tools.RODict({
        "ID": 118,
        "dropPackage": 1302,
        "dropCondition": None,
        "dropTarget": 30010022,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 300,
        "bindWeight": 0
    }),
    119: _tools.RODict({
        "ID": 119,
        "dropPackage": 1302,
        "dropCondition": None,
        "dropTarget": 30010023,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 300,
        "bindWeight": 0
    }),
    120: _tools.RODict({
        "ID": 120,
        "dropPackage": 1302,
        "dropCondition": None,
        "dropTarget": 30010024,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 300,
        "bindWeight": 0
    }),
    121: _tools.RODict({
        "ID": 121,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990135,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    122: _tools.RODict({
        "ID": 122,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990136,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    123: _tools.RODict({
        "ID": 123,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990137,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    124: _tools.RODict({
        "ID": 124,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990138,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    125: _tools.RODict({
        "ID": 125,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990139,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    126: _tools.RODict({
        "ID": 126,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990140,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    127: _tools.RODict({
        "ID": 127,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990141,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    128: _tools.RODict({
        "ID": 128,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990142,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    129: _tools.RODict({
        "ID": 129,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990143,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    130: _tools.RODict({
        "ID": 130,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990144,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    131: _tools.RODict({
        "ID": 131,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990145,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    132: _tools.RODict({
        "ID": 132,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990146,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    133: _tools.RODict({
        "ID": 133,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990147,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    134: _tools.RODict({
        "ID": 134,
        "dropPackage": 1303,
        "dropCondition": None,
        "dropTarget": 30990148,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 5000
    }),
    135: _tools.RODict({
        "ID": 135,
        "dropPackage": 1501,
        "dropCondition": None,
        "dropTarget": 30990121,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 100,
        "bindWeight": 5000
    }),
    136: _tools.RODict({
        "ID": 136,
        "dropPackage": 1501,
        "dropCondition": None,
        "dropTarget": 30990122,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    137: _tools.RODict({
        "ID": 137,
        "dropPackage": 1501,
        "dropCondition": None,
        "dropTarget": 30990123,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    138: _tools.RODict({
        "ID": 138,
        "dropPackage": 1501,
        "dropCondition": None,
        "dropTarget": 30990124,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    139: _tools.RODict({
        "ID": 139,
        "dropPackage": 1501,
        "dropCondition": None,
        "dropTarget": 30990125,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    140: _tools.RODict({
        "ID": 140,
        "dropPackage": 1501,
        "dropCondition": None,
        "dropTarget": 30990126,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 150,
        "bindWeight": 5000
    }),
    141: _tools.RODict({
        "ID": 141,
        "dropPackage": 1501,
        "dropCondition": None,
        "dropTarget": 30990127,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 150,
        "bindWeight": 5000
    }),
    142: _tools.RODict({
        "ID": 142,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000102,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    143: _tools.RODict({
        "ID": 143,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000103,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    144: _tools.RODict({
        "ID": 144,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000104,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    145: _tools.RODict({
        "ID": 145,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000105,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    146: _tools.RODict({
        "ID": 146,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000106,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    147: _tools.RODict({
        "ID": 147,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000107,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    148: _tools.RODict({
        "ID": 148,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000108,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    149: _tools.RODict({
        "ID": 149,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000109,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    150: _tools.RODict({
        "ID": 150,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000110,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    151: _tools.RODict({
        "ID": 151,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000111,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    152: _tools.RODict({
        "ID": 152,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000112,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    153: _tools.RODict({
        "ID": 153,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000113,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    154: _tools.RODict({
        "ID": 154,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000114,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    155: _tools.RODict({
        "ID": 155,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000141,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    156: _tools.RODict({
        "ID": 156,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000142,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    157: _tools.RODict({
        "ID": 157,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000143,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    158: _tools.RODict({
        "ID": 158,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000144,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    159: _tools.RODict({
        "ID": 159,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000145,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    160: _tools.RODict({
        "ID": 160,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000146,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    161: _tools.RODict({
        "ID": 161,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000147,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    162: _tools.RODict({
        "ID": 162,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000148,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    163: _tools.RODict({
        "ID": 163,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000149,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    164: _tools.RODict({
        "ID": 164,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000150,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    165: _tools.RODict({
        "ID": 165,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000151,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    166: _tools.RODict({
        "ID": 166,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000152,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    167: _tools.RODict({
        "ID": 167,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000153,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    168: _tools.RODict({
        "ID": 168,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000180,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    169: _tools.RODict({
        "ID": 169,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000181,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    170: _tools.RODict({
        "ID": 170,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000182,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    171: _tools.RODict({
        "ID": 171,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000183,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    172: _tools.RODict({
        "ID": 172,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000184,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    173: _tools.RODict({
        "ID": 173,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000185,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    174: _tools.RODict({
        "ID": 174,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000186,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    175: _tools.RODict({
        "ID": 175,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000187,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    176: _tools.RODict({
        "ID": 176,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000188,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    177: _tools.RODict({
        "ID": 177,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000189,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    178: _tools.RODict({
        "ID": 178,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000190,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    179: _tools.RODict({
        "ID": 179,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000191,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    180: _tools.RODict({
        "ID": 180,
        "dropPackage": 1502,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000192,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    181: _tools.RODict({
        "ID": 181,
        "dropPackage": 1503,
        "dropCondition": None,
        "dropTarget": 30000287,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    182: _tools.RODict({
        "ID": 182,
        "dropPackage": 1503,
        "dropCondition": None,
        "dropTarget": 30000288,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    183: _tools.RODict({
        "ID": 183,
        "dropPackage": 1503,
        "dropCondition": None,
        "dropTarget": 30000289,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    184: _tools.RODict({
        "ID": 184,
        "dropPackage": 1504,
        "dropCondition": None,
        "dropTarget": 30000290,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    185: _tools.RODict({
        "ID": 185,
        "dropPackage": 1504,
        "dropCondition": None,
        "dropTarget": 30000291,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    186: _tools.RODict({
        "ID": 186,
        "dropPackage": 1504,
        "dropCondition": None,
        "dropTarget": 30000292,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    187: _tools.RODict({
        "ID": 187,
        "dropPackage": 1505,
        "dropCondition": None,
        "dropTarget": 30000293,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    188: _tools.RODict({
        "ID": 188,
        "dropPackage": 1505,
        "dropCondition": None,
        "dropTarget": 30000294,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    189: _tools.RODict({
        "ID": 189,
        "dropPackage": 1505,
        "dropCondition": None,
        "dropTarget": 30000295,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    190: _tools.RODict({
        "ID": 190,
        "dropPackage": 1506,
        "dropCondition": None,
        "dropTarget": 30000296,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    191: _tools.RODict({
        "ID": 191,
        "dropPackage": 1506,
        "dropCondition": None,
        "dropTarget": 30000297,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    192: _tools.RODict({
        "ID": 192,
        "dropPackage": 1506,
        "dropCondition": None,
        "dropTarget": 30000298,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    193: _tools.RODict({
        "ID": 193,
        "dropPackage": 1507,
        "dropCondition": None,
        "dropTarget": 30990128,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 100,
        "bindWeight": 5000
    }),
    194: _tools.RODict({
        "ID": 194,
        "dropPackage": 1507,
        "dropCondition": None,
        "dropTarget": 30990129,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    195: _tools.RODict({
        "ID": 195,
        "dropPackage": 1507,
        "dropCondition": None,
        "dropTarget": 30990130,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    196: _tools.RODict({
        "ID": 196,
        "dropPackage": 1507,
        "dropCondition": None,
        "dropTarget": 30990131,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    197: _tools.RODict({
        "ID": 197,
        "dropPackage": 1507,
        "dropCondition": None,
        "dropTarget": 30990132,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    198: _tools.RODict({
        "ID": 198,
        "dropPackage": 1507,
        "dropCondition": None,
        "dropTarget": 30990133,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 150,
        "bindWeight": 5000
    }),
    199: _tools.RODict({
        "ID": 199,
        "dropPackage": 1507,
        "dropCondition": None,
        "dropTarget": 30990134,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 150,
        "bindWeight": 5000
    }),
    200: _tools.RODict({
        "ID": 200,
        "dropPackage": 1508,
        "dropCondition": None,
        "dropTarget": 30990135,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 100,
        "bindWeight": 5000
    }),
    201: _tools.RODict({
        "ID": 201,
        "dropPackage": 1508,
        "dropCondition": None,
        "dropTarget": 30990136,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    202: _tools.RODict({
        "ID": 202,
        "dropPackage": 1508,
        "dropCondition": None,
        "dropTarget": 30990137,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    203: _tools.RODict({
        "ID": 203,
        "dropPackage": 1508,
        "dropCondition": None,
        "dropTarget": 30990138,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    204: _tools.RODict({
        "ID": 204,
        "dropPackage": 1508,
        "dropCondition": None,
        "dropTarget": 30990139,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    205: _tools.RODict({
        "ID": 205,
        "dropPackage": 1508,
        "dropCondition": None,
        "dropTarget": 30990140,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 150,
        "bindWeight": 5000
    }),
    206: _tools.RODict({
        "ID": 206,
        "dropPackage": 1508,
        "dropCondition": None,
        "dropTarget": 30990141,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 150,
        "bindWeight": 5000
    }),
    207: _tools.RODict({
        "ID": 207,
        "dropPackage": 1509,
        "dropCondition": None,
        "dropTarget": 30990142,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 100,
        "bindWeight": 5000
    }),
    208: _tools.RODict({
        "ID": 208,
        "dropPackage": 1509,
        "dropCondition": None,
        "dropTarget": 30990143,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    209: _tools.RODict({
        "ID": 209,
        "dropPackage": 1509,
        "dropCondition": None,
        "dropTarget": 30990144,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    210: _tools.RODict({
        "ID": 210,
        "dropPackage": 1509,
        "dropCondition": None,
        "dropTarget": 30990145,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    211: _tools.RODict({
        "ID": 211,
        "dropPackage": 1509,
        "dropCondition": None,
        "dropTarget": 30990146,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    212: _tools.RODict({
        "ID": 212,
        "dropPackage": 1509,
        "dropCondition": None,
        "dropTarget": 30990147,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 150,
        "bindWeight": 5000
    }),
    213: _tools.RODict({
        "ID": 213,
        "dropPackage": 1509,
        "dropCondition": None,
        "dropTarget": 30990148,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 150,
        "bindWeight": 5000
    }),
    214: _tools.RODict({
        "ID": 214,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80113001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    215: _tools.RODict({
        "ID": 215,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80123001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    216: _tools.RODict({
        "ID": 216,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80133001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    217: _tools.RODict({
        "ID": 217,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80213001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    218: _tools.RODict({
        "ID": 218,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80223001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    219: _tools.RODict({
        "ID": 219,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80233001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    220: _tools.RODict({
        "ID": 220,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80313001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    221: _tools.RODict({
        "ID": 221,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80323001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    222: _tools.RODict({
        "ID": 222,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80333001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    223: _tools.RODict({
        "ID": 223,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80413001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    224: _tools.RODict({
        "ID": 224,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80423001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    225: _tools.RODict({
        "ID": 225,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80433001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    226: _tools.RODict({
        "ID": 226,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80583001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    227: _tools.RODict({
        "ID": 227,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80683001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    228: _tools.RODict({
        "ID": 228,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80693001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    229: _tools.RODict({
        "ID": 229,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80783001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    230: _tools.RODict({
        "ID": 230,
        "dropPackage": 1007,
        "dropCondition": None,
        "dropTarget": 80793001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    231: _tools.RODict({
        "ID": 231,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80113002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    232: _tools.RODict({
        "ID": 232,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80123002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    233: _tools.RODict({
        "ID": 233,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80133002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    234: _tools.RODict({
        "ID": 234,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80213002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    235: _tools.RODict({
        "ID": 235,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80223002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    236: _tools.RODict({
        "ID": 236,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80233002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    237: _tools.RODict({
        "ID": 237,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80313002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    238: _tools.RODict({
        "ID": 238,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80323002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    239: _tools.RODict({
        "ID": 239,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80333002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    240: _tools.RODict({
        "ID": 240,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80413002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    241: _tools.RODict({
        "ID": 241,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80423002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    242: _tools.RODict({
        "ID": 242,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80433002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    243: _tools.RODict({
        "ID": 243,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80583002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    244: _tools.RODict({
        "ID": 244,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80683002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    245: _tools.RODict({
        "ID": 245,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80693002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    246: _tools.RODict({
        "ID": 246,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80783002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    247: _tools.RODict({
        "ID": 247,
        "dropPackage": 1008,
        "dropCondition": None,
        "dropTarget": 80793002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    248: _tools.RODict({
        "ID": 248,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80113003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    249: _tools.RODict({
        "ID": 249,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80123003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    250: _tools.RODict({
        "ID": 250,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80133003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    251: _tools.RODict({
        "ID": 251,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80213003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    252: _tools.RODict({
        "ID": 252,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80223003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    253: _tools.RODict({
        "ID": 253,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80233003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    254: _tools.RODict({
        "ID": 254,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80313003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    255: _tools.RODict({
        "ID": 255,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80323003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    256: _tools.RODict({
        "ID": 256,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80333003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    257: _tools.RODict({
        "ID": 257,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80413003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    258: _tools.RODict({
        "ID": 258,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80423003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    259: _tools.RODict({
        "ID": 259,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80433003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    260: _tools.RODict({
        "ID": 260,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80583003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    261: _tools.RODict({
        "ID": 261,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80683003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    262: _tools.RODict({
        "ID": 262,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80693003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    263: _tools.RODict({
        "ID": 263,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80783003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    264: _tools.RODict({
        "ID": 264,
        "dropPackage": 1009,
        "dropCondition": None,
        "dropTarget": 80793003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    265: _tools.RODict({
        "ID": 265,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80113004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    266: _tools.RODict({
        "ID": 266,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80123004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    267: _tools.RODict({
        "ID": 267,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80133004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    268: _tools.RODict({
        "ID": 268,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80213004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    269: _tools.RODict({
        "ID": 269,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80223004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    270: _tools.RODict({
        "ID": 270,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80233004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    271: _tools.RODict({
        "ID": 271,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80313004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    272: _tools.RODict({
        "ID": 272,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80323004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    273: _tools.RODict({
        "ID": 273,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80333004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    274: _tools.RODict({
        "ID": 274,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80413004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    275: _tools.RODict({
        "ID": 275,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80423004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    276: _tools.RODict({
        "ID": 276,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80433004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    277: _tools.RODict({
        "ID": 277,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80583004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    278: _tools.RODict({
        "ID": 278,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80683004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    279: _tools.RODict({
        "ID": 279,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80693004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    280: _tools.RODict({
        "ID": 280,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80783004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    281: _tools.RODict({
        "ID": 281,
        "dropPackage": 1010,
        "dropCondition": None,
        "dropTarget": 80793004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    282: _tools.RODict({
        "ID": 282,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80113005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    283: _tools.RODict({
        "ID": 283,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80123005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    284: _tools.RODict({
        "ID": 284,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80133005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    285: _tools.RODict({
        "ID": 285,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80213005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    286: _tools.RODict({
        "ID": 286,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80223005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    287: _tools.RODict({
        "ID": 287,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80233005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    288: _tools.RODict({
        "ID": 288,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80313005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    289: _tools.RODict({
        "ID": 289,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80323005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    290: _tools.RODict({
        "ID": 290,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80333005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    291: _tools.RODict({
        "ID": 291,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80413005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    292: _tools.RODict({
        "ID": 292,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80423005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    293: _tools.RODict({
        "ID": 293,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80433005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    294: _tools.RODict({
        "ID": 294,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80583005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    295: _tools.RODict({
        "ID": 295,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80683005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    296: _tools.RODict({
        "ID": 296,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80693005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    297: _tools.RODict({
        "ID": 297,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80783005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    298: _tools.RODict({
        "ID": 298,
        "dropPackage": 1011,
        "dropCondition": None,
        "dropTarget": 80793005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    299: _tools.RODict({
        "ID": 299,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80114001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    300: _tools.RODict({
        "ID": 300,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80124001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    301: _tools.RODict({
        "ID": 301,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80134001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    302: _tools.RODict({
        "ID": 302,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80214001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    303: _tools.RODict({
        "ID": 303,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80224001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    304: _tools.RODict({
        "ID": 304,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80234001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    305: _tools.RODict({
        "ID": 305,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80314001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    306: _tools.RODict({
        "ID": 306,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80324001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    307: _tools.RODict({
        "ID": 307,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80334001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    308: _tools.RODict({
        "ID": 308,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80414001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    309: _tools.RODict({
        "ID": 309,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80424001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    310: _tools.RODict({
        "ID": 310,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80434001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    311: _tools.RODict({
        "ID": 311,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80584001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    312: _tools.RODict({
        "ID": 312,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80684001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    313: _tools.RODict({
        "ID": 313,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80694001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    314: _tools.RODict({
        "ID": 314,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80784001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    315: _tools.RODict({
        "ID": 315,
        "dropPackage": 1012,
        "dropCondition": None,
        "dropTarget": 80794001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    316: _tools.RODict({
        "ID": 316,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80114002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    317: _tools.RODict({
        "ID": 317,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80124002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    318: _tools.RODict({
        "ID": 318,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80134002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    319: _tools.RODict({
        "ID": 319,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80214002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    320: _tools.RODict({
        "ID": 320,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80224002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    321: _tools.RODict({
        "ID": 321,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80234002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    322: _tools.RODict({
        "ID": 322,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80314002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    323: _tools.RODict({
        "ID": 323,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80324002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    324: _tools.RODict({
        "ID": 324,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80334002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    325: _tools.RODict({
        "ID": 325,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80414002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    326: _tools.RODict({
        "ID": 326,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80424002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    327: _tools.RODict({
        "ID": 327,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80434002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    328: _tools.RODict({
        "ID": 328,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80584002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    329: _tools.RODict({
        "ID": 329,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80684002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    330: _tools.RODict({
        "ID": 330,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80694002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    331: _tools.RODict({
        "ID": 331,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80784002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    332: _tools.RODict({
        "ID": 332,
        "dropPackage": 1013,
        "dropCondition": None,
        "dropTarget": 80794002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    333: _tools.RODict({
        "ID": 333,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80114003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    334: _tools.RODict({
        "ID": 334,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80124003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    335: _tools.RODict({
        "ID": 335,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80134003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 5000
    }),
    336: _tools.RODict({
        "ID": 336,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80214003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    337: _tools.RODict({
        "ID": 337,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80224003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    338: _tools.RODict({
        "ID": 338,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80234003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    339: _tools.RODict({
        "ID": 339,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80314003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    340: _tools.RODict({
        "ID": 340,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80324003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    341: _tools.RODict({
        "ID": 341,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80334003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    342: _tools.RODict({
        "ID": 342,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80414003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    343: _tools.RODict({
        "ID": 343,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80424003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    344: _tools.RODict({
        "ID": 344,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80434003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    345: _tools.RODict({
        "ID": 345,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80584003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 5000
    }),
    346: _tools.RODict({
        "ID": 346,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80684003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    347: _tools.RODict({
        "ID": 347,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80694003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    348: _tools.RODict({
        "ID": 348,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80784003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    349: _tools.RODict({
        "ID": 349,
        "dropPackage": 1014,
        "dropCondition": None,
        "dropTarget": 80794003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 5000
    }),
    351: _tools.RODict({
        "ID": 351,
        "dropPackage": 11002,
        "dropCondition": None,
        "dropTarget": 30000227,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 899,
        "bindWeight": 10000
    }),
    352: _tools.RODict({
        "ID": 352,
        "dropPackage": 11002,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 100,
        "bindWeight": 10000
    }),
    353: _tools.RODict({
        "ID": 353,
        "dropPackage": 11002,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 10000
    }),
    355: _tools.RODict({
        "ID": 355,
        "dropPackage": 11003,
        "dropCondition": None,
        "dropTarget": 30000227,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 878,
        "bindWeight": 10000
    }),
    356: _tools.RODict({
        "ID": 356,
        "dropPackage": 11003,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 120,
        "bindWeight": 10000
    }),
    357: _tools.RODict({
        "ID": 357,
        "dropPackage": 11003,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2,
        "bindWeight": 10000
    }),
    359: _tools.RODict({
        "ID": 359,
        "dropPackage": 11004,
        "dropCondition": None,
        "dropTarget": 30000227,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 857,
        "bindWeight": 10000
    }),
    360: _tools.RODict({
        "ID": 360,
        "dropPackage": 11004,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 140,
        "bindWeight": 10000
    }),
    361: _tools.RODict({
        "ID": 361,
        "dropPackage": 11004,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 3,
        "bindWeight": 10000
    }),
    363: _tools.RODict({
        "ID": 363,
        "dropPackage": 11005,
        "dropCondition": None,
        "dropTarget": 30000227,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 836,
        "bindWeight": 10000
    }),
    364: _tools.RODict({
        "ID": 364,
        "dropPackage": 11005,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 160,
        "bindWeight": 10000
    }),
    365: _tools.RODict({
        "ID": 365,
        "dropPackage": 11005,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4,
        "bindWeight": 10000
    }),
    366: _tools.RODict({
        "ID": 366,
        "dropPackage": 11006,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 4,
        "dropNumMax": 6,
        "weight": 899,
        "bindWeight": 10000
    }),
    367: _tools.RODict({
        "ID": 367,
        "dropPackage": 11006,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 2,
        "dropNumMax": 3,
        "weight": 100,
        "bindWeight": 10000
    }),
    368: _tools.RODict({
        "ID": 368,
        "dropPackage": 11006,
        "dropCondition": None,
        "dropTarget": 30000230,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 10000
    }),
    369: _tools.RODict({
        "ID": 369,
        "dropPackage": 11007,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 4,
        "dropNumMax": 6,
        "weight": 878,
        "bindWeight": 10000
    }),
    370: _tools.RODict({
        "ID": 370,
        "dropPackage": 11007,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 2,
        "dropNumMax": 3,
        "weight": 120,
        "bindWeight": 10000
    }),
    371: _tools.RODict({
        "ID": 371,
        "dropPackage": 11007,
        "dropCondition": None,
        "dropTarget": 30000230,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2,
        "bindWeight": 10000
    }),
    372: _tools.RODict({
        "ID": 372,
        "dropPackage": 11008,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 4,
        "dropNumMax": 6,
        "weight": 857,
        "bindWeight": 10000
    }),
    373: _tools.RODict({
        "ID": 373,
        "dropPackage": 11008,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 2,
        "dropNumMax": 3,
        "weight": 140,
        "bindWeight": 10000
    }),
    374: _tools.RODict({
        "ID": 374,
        "dropPackage": 11008,
        "dropCondition": None,
        "dropTarget": 30000230,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 3,
        "bindWeight": 10000
    }),
    375: _tools.RODict({
        "ID": 375,
        "dropPackage": 11009,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 4,
        "dropNumMax": 6,
        "weight": 836,
        "bindWeight": 10000
    }),
    376: _tools.RODict({
        "ID": 376,
        "dropPackage": 11009,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 2,
        "dropNumMax": 3,
        "weight": 160,
        "bindWeight": 10000
    }),
    377: _tools.RODict({
        "ID": 377,
        "dropPackage": 11009,
        "dropCondition": None,
        "dropTarget": 30000230,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4,
        "bindWeight": 10000
    }),
    378: _tools.RODict({
        "ID": 378,
        "dropPackage": 11010,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 4,
        "dropNumMax": 6,
        "weight": 390,
        "bindWeight": 10000
    }),
    379: _tools.RODict({
        "ID": 379,
        "dropPackage": 11010,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 2,
        "dropNumMax": 3,
        "weight": 600,
        "bindWeight": 10000
    }),
    380: _tools.RODict({
        "ID": 380,
        "dropPackage": 11010,
        "dropCondition": None,
        "dropTarget": 30000230,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 10,
        "bindWeight": 10000
    }),
    381: _tools.RODict({
        "ID": 381,
        "dropPackage": 11011,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 4,
        "dropNumMax": 6,
        "weight": 330,
        "bindWeight": 10000
    }),
    382: _tools.RODict({
        "ID": 382,
        "dropPackage": 11011,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 2,
        "dropNumMax": 3,
        "weight": 650,
        "bindWeight": 10000
    }),
    383: _tools.RODict({
        "ID": 383,
        "dropPackage": 11011,
        "dropCondition": None,
        "dropTarget": 30000230,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 20,
        "bindWeight": 10000
    }),
    384: _tools.RODict({
        "ID": 384,
        "dropPackage": 11012,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 4,
        "dropNumMax": 6,
        "weight": 270,
        "bindWeight": 10000
    }),
    385: _tools.RODict({
        "ID": 385,
        "dropPackage": 11012,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 2,
        "dropNumMax": 3,
        "weight": 700,
        "bindWeight": 10000
    }),
    386: _tools.RODict({
        "ID": 386,
        "dropPackage": 11012,
        "dropCondition": None,
        "dropTarget": 30000230,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 30,
        "bindWeight": 10000
    }),
    387: _tools.RODict({
        "ID": 387,
        "dropPackage": 11013,
        "dropCondition": None,
        "dropTarget": 30000228,
        "dropNumMin": 4,
        "dropNumMax": 6,
        "weight": 210,
        "bindWeight": 10000
    }),
    388: _tools.RODict({
        "ID": 388,
        "dropPackage": 11013,
        "dropCondition": None,
        "dropTarget": 30000229,
        "dropNumMin": 2,
        "dropNumMax": 3,
        "weight": 750,
        "bindWeight": 10000
    }),
    389: _tools.RODict({
        "ID": 389,
        "dropPackage": 11013,
        "dropCondition": None,
        "dropTarget": 30000230,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    390: _tools.RODict({
        "ID": 390,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    391: _tools.RODict({
        "ID": 391,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    392: _tools.RODict({
        "ID": 392,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    393: _tools.RODict({
        "ID": 393,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    394: _tools.RODict({
        "ID": 394,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    395: _tools.RODict({
        "ID": 395,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001006,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    396: _tools.RODict({
        "ID": 396,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001007,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    397: _tools.RODict({
        "ID": 397,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001008,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    398: _tools.RODict({
        "ID": 398,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001009,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    399: _tools.RODict({
        "ID": 399,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001010,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    400: _tools.RODict({
        "ID": 400,
        "dropPackage": 99,
        "dropCondition": None,
        "dropTarget": 30001036,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    401: _tools.RODict({
        "ID": 401,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001011,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    402: _tools.RODict({
        "ID": 402,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001012,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    403: _tools.RODict({
        "ID": 403,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001013,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    404: _tools.RODict({
        "ID": 404,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001014,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    405: _tools.RODict({
        "ID": 405,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001015,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    406: _tools.RODict({
        "ID": 406,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001016,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    407: _tools.RODict({
        "ID": 407,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001017,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    408: _tools.RODict({
        "ID": 408,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001018,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    409: _tools.RODict({
        "ID": 409,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001019,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    410: _tools.RODict({
        "ID": 410,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001020,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    411: _tools.RODict({
        "ID": 411,
        "dropPackage": 98,
        "dropCondition": None,
        "dropTarget": 30001037,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    412: _tools.RODict({
        "ID": 412,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001021,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    413: _tools.RODict({
        "ID": 413,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001022,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    414: _tools.RODict({
        "ID": 414,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001023,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    415: _tools.RODict({
        "ID": 415,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001024,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    416: _tools.RODict({
        "ID": 416,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001025,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    417: _tools.RODict({
        "ID": 417,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001026,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    418: _tools.RODict({
        "ID": 418,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001027,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    419: _tools.RODict({
        "ID": 419,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001028,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    420: _tools.RODict({
        "ID": 420,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001029,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    421: _tools.RODict({
        "ID": 421,
        "dropPackage": 97,
        "dropCondition": None,
        "dropTarget": 30001038,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    422: _tools.RODict({
        "ID": 422,
        "dropPackage": 96,
        "dropCondition": None,
        "dropTarget": 30001030,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    423: _tools.RODict({
        "ID": 423,
        "dropPackage": 96,
        "dropCondition": None,
        "dropTarget": 30001031,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    424: _tools.RODict({
        "ID": 424,
        "dropPackage": 96,
        "dropCondition": None,
        "dropTarget": 30001032,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    425: _tools.RODict({
        "ID": 425,
        "dropPackage": 96,
        "dropCondition": None,
        "dropTarget": 30001033,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    426: _tools.RODict({
        "ID": 426,
        "dropPackage": 96,
        "dropCondition": None,
        "dropTarget": 30001034,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    427: _tools.RODict({
        "ID": 427,
        "dropPackage": 96,
        "dropCondition": None,
        "dropTarget": 30001035,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    428: _tools.RODict({
        "ID": 428,
        "dropPackage": 96,
        "dropCondition": None,
        "dropTarget": 30001039,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    429: _tools.RODict({
        "ID": 429,
        "dropPackage": 96,
        "dropCondition": None,
        "dropTarget": 30001040,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 10000
    }),
    430: _tools.RODict({
        "ID": 430,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000287,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 5000,
        "bindWeight": 5000
    }),
    431: _tools.RODict({
        "ID": 431,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000288,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 5000,
        "bindWeight": 5000
    }),
    432: _tools.RODict({
        "ID": 432,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000289,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 5000,
        "bindWeight": 5000
    }),
    433: _tools.RODict({
        "ID": 433,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000290,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2300,
        "bindWeight": 5000
    }),
    434: _tools.RODict({
        "ID": 434,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000291,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2300,
        "bindWeight": 5000
    }),
    435: _tools.RODict({
        "ID": 435,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000292,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2300,
        "bindWeight": 5000
    }),
    436: _tools.RODict({
        "ID": 436,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000293,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 500,
        "bindWeight": 5000
    }),
    437: _tools.RODict({
        "ID": 437,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000294,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 500,
        "bindWeight": 5000
    }),
    438: _tools.RODict({
        "ID": 438,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000295,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 500,
        "bindWeight": 5000
    }),
    439: _tools.RODict({
        "ID": 439,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000296,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 50,
        "bindWeight": 5000
    }),
    440: _tools.RODict({
        "ID": 440,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000297,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 50,
        "bindWeight": 5000
    }),
    441: _tools.RODict({
        "ID": 441,
        "dropPackage": 1510,
        "dropCondition": None,
        "dropTarget": 30000298,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 50,
        "bindWeight": 5000
    }),
    442: _tools.RODict({
        "ID": 442,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4000,
        "bindWeight": 10000
    }),
    443: _tools.RODict({
        "ID": 443,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003004,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4000,
        "bindWeight": 10000
    }),
    444: _tools.RODict({
        "ID": 444,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003009,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4000,
        "bindWeight": 10000
    }),
    445: _tools.RODict({
        "ID": 445,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003017,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4000,
        "bindWeight": 10000
    }),
    446: _tools.RODict({
        "ID": 446,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003019,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4000,
        "bindWeight": 10000
    }),
    447: _tools.RODict({
        "ID": 447,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003020,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4000,
        "bindWeight": 10000
    }),
    448: _tools.RODict({
        "ID": 448,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003021,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4000,
        "bindWeight": 10000
    }),
    449: _tools.RODict({
        "ID": 449,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003022,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 4000,
        "bindWeight": 10000
    }),
    450: _tools.RODict({
        "ID": 450,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    451: _tools.RODict({
        "ID": 451,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003007,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    452: _tools.RODict({
        "ID": 452,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003010,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    453: _tools.RODict({
        "ID": 453,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003012,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    454: _tools.RODict({
        "ID": 454,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003015,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    455: _tools.RODict({
        "ID": 455,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003033,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    456: _tools.RODict({
        "ID": 456,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003035,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    457: _tools.RODict({
        "ID": 457,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003037,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    458: _tools.RODict({
        "ID": 458,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003040,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    459: _tools.RODict({
        "ID": 459,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003044,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    460: _tools.RODict({
        "ID": 460,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003049,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    461: _tools.RODict({
        "ID": 461,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003050,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 700,
        "bindWeight": 10000
    }),
    462: _tools.RODict({
        "ID": 462,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    463: _tools.RODict({
        "ID": 463,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003005,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    464: _tools.RODict({
        "ID": 464,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003008,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    465: _tools.RODict({
        "ID": 465,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003011,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    466: _tools.RODict({
        "ID": 466,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003013,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    467: _tools.RODict({
        "ID": 467,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003016,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    468: _tools.RODict({
        "ID": 468,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003018,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    469: _tools.RODict({
        "ID": 469,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003027,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    470: _tools.RODict({
        "ID": 470,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003029,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    471: _tools.RODict({
        "ID": 471,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003038,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    472: _tools.RODict({
        "ID": 472,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003042,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    473: _tools.RODict({
        "ID": 473,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003045,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    474: _tools.RODict({
        "ID": 474,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003047,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 40,
        "bindWeight": 10000
    }),
    475: _tools.RODict({
        "ID": 475,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003023,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    476: _tools.RODict({
        "ID": 476,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003025,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    477: _tools.RODict({
        "ID": 477,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003034,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    478: _tools.RODict({
        "ID": 478,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003036,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    479: _tools.RODict({
        "ID": 479,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003039,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    480: _tools.RODict({
        "ID": 480,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003041,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    481: _tools.RODict({
        "ID": 481,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003043,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    482: _tools.RODict({
        "ID": 482,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003046,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    483: _tools.RODict({
        "ID": 483,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003048,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 14,
        "bindWeight": 0
    }),
    484: _tools.RODict({
        "ID": 484,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003006,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 0
    }),
    485: _tools.RODict({
        "ID": 485,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003014,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 0
    }),
    486: _tools.RODict({
        "ID": 486,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003024,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 0
    }),
    487: _tools.RODict({
        "ID": 487,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003026,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 0
    }),
    488: _tools.RODict({
        "ID": 488,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003028,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 0
    }),
    489: _tools.RODict({
        "ID": 489,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003030,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 0
    }),
    490: _tools.RODict({
        "ID": 490,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003031,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 0
    }),
    491: _tools.RODict({
        "ID": 491,
        "dropPackage": 2000,
        "dropCondition": None,
        "dropTarget": 30003032,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 0
    }),
    492: _tools.RODict({
        "ID": 492,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990121,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2000,
        "bindWeight": 5000
    }),
    493: _tools.RODict({
        "ID": 493,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990122,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2000,
        "bindWeight": 5000
    }),
    494: _tools.RODict({
        "ID": 494,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990123,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2000,
        "bindWeight": 5000
    }),
    495: _tools.RODict({
        "ID": 495,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990124,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2000,
        "bindWeight": 5000
    }),
    496: _tools.RODict({
        "ID": 496,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990125,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2000,
        "bindWeight": 5000
    }),
    497: _tools.RODict({
        "ID": 497,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990126,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2000,
        "bindWeight": 5000
    }),
    498: _tools.RODict({
        "ID": 498,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990127,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 2000,
        "bindWeight": 5000
    }),
    499: _tools.RODict({
        "ID": 499,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990128,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 240,
        "bindWeight": 5000
    }),
    500: _tools.RODict({
        "ID": 500,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990129,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 240,
        "bindWeight": 5000
    }),
    501: _tools.RODict({
        "ID": 501,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990130,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 240,
        "bindWeight": 5000
    }),
    502: _tools.RODict({
        "ID": 502,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990131,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 240,
        "bindWeight": 5000
    }),
    503: _tools.RODict({
        "ID": 503,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990132,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 240,
        "bindWeight": 5000
    }),
    504: _tools.RODict({
        "ID": 504,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990133,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 240,
        "bindWeight": 5000
    }),
    505: _tools.RODict({
        "ID": 505,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990134,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 240,
        "bindWeight": 5000
    }),
    506: _tools.RODict({
        "ID": 506,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990135,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 24,
        "bindWeight": 5000
    }),
    507: _tools.RODict({
        "ID": 507,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990136,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 24,
        "bindWeight": 5000
    }),
    508: _tools.RODict({
        "ID": 508,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990137,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 24,
        "bindWeight": 5000
    }),
    509: _tools.RODict({
        "ID": 509,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990138,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 24,
        "bindWeight": 5000
    }),
    510: _tools.RODict({
        "ID": 510,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990139,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 24,
        "bindWeight": 5000
    }),
    511: _tools.RODict({
        "ID": 511,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990140,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 24,
        "bindWeight": 5000
    }),
    512: _tools.RODict({
        "ID": 512,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990141,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 24,
        "bindWeight": 5000
    }),
    513: _tools.RODict({
        "ID": 513,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990142,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 5000
    }),
    514: _tools.RODict({
        "ID": 514,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990143,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 5000
    }),
    515: _tools.RODict({
        "ID": 515,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990144,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 5000
    }),
    516: _tools.RODict({
        "ID": 516,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990145,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 5000
    }),
    517: _tools.RODict({
        "ID": 517,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990146,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 5000
    }),
    518: _tools.RODict({
        "ID": 518,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990147,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 5000
    }),
    519: _tools.RODict({
        "ID": 519,
        "dropPackage": 1511,
        "dropCondition": None,
        "dropTarget": 30990148,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 1,
        "bindWeight": 5000
    }),
    520: _tools.RODict({
        "ID": 520,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010007,
        "dropNumMin": 20,
        "dropNumMax": 30,
        "weight": 2000,
        "bindWeight": 0
    }),
    521: _tools.RODict({
        "ID": 521,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010008,
        "dropNumMin": 20,
        "dropNumMax": 30,
        "weight": 2000,
        "bindWeight": 0
    }),
    522: _tools.RODict({
        "ID": 522,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010009,
        "dropNumMin": 1,
        "dropNumMax": 5,
        "weight": 1000,
        "bindWeight": 0
    }),
    523: _tools.RODict({
        "ID": 523,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010010,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 500,
        "bindWeight": 0
    }),
    524: _tools.RODict({
        "ID": 524,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010011,
        "dropNumMin": 1,
        "dropNumMax": 5,
        "weight": 1000,
        "bindWeight": 0
    }),
    525: _tools.RODict({
        "ID": 525,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010012,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 500,
        "bindWeight": 0
    }),
    526: _tools.RODict({
        "ID": 526,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010013,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 1000,
        "bindWeight": 0
    }),
    527: _tools.RODict({
        "ID": 527,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010014,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 2000,
        "bindWeight": 0
    }),
    528: _tools.RODict({
        "ID": 528,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010015,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 500,
        "bindWeight": 0
    }),
    529: _tools.RODict({
        "ID": 529,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010016,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 1000,
        "bindWeight": 0
    }),
    530: _tools.RODict({
        "ID": 530,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010017,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 2000,
        "bindWeight": 0
    }),
    531: _tools.RODict({
        "ID": 531,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010018,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 500,
        "bindWeight": 0
    }),
    532: _tools.RODict({
        "ID": 532,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010019,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 1000,
        "bindWeight": 0
    }),
    533: _tools.RODict({
        "ID": 533,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010020,
        "dropNumMin": 1,
        "dropNumMax": 3,
        "weight": 2000,
        "bindWeight": 0
    }),
    534: _tools.RODict({
        "ID": 534,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010021,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 10,
        "bindWeight": 0
    }),
    535: _tools.RODict({
        "ID": 535,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010022,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 10,
        "bindWeight": 0
    }),
    536: _tools.RODict({
        "ID": 536,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010023,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 50,
        "bindWeight": 0
    }),
    537: _tools.RODict({
        "ID": 537,
        "dropPackage": 9200,
        "dropCondition": None,
        "dropTarget": 30010024,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    538: _tools.RODict({
        "ID": 538,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80111001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 2000
    }),
    539: _tools.RODict({
        "ID": 539,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80121001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 2000
    }),
    540: _tools.RODict({
        "ID": 540,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80131001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 2000
    }),
    541: _tools.RODict({
        "ID": 541,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80211001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    542: _tools.RODict({
        "ID": 542,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80221001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    543: _tools.RODict({
        "ID": 543,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80231001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    544: _tools.RODict({
        "ID": 544,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80311001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    545: _tools.RODict({
        "ID": 545,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80321001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    546: _tools.RODict({
        "ID": 546,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80331001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    547: _tools.RODict({
        "ID": 547,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80411001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    548: _tools.RODict({
        "ID": 548,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80421001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    549: _tools.RODict({
        "ID": 549,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80431001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    550: _tools.RODict({
        "ID": 550,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80581001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 2000
    }),
    551: _tools.RODict({
        "ID": 551,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80111002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 1000
    }),
    552: _tools.RODict({
        "ID": 552,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80121002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 1000
    }),
    553: _tools.RODict({
        "ID": 553,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80131002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 1000
    }),
    554: _tools.RODict({
        "ID": 554,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80211002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    555: _tools.RODict({
        "ID": 555,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80221002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    556: _tools.RODict({
        "ID": 556,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80231002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    557: _tools.RODict({
        "ID": 557,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80311002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    558: _tools.RODict({
        "ID": 558,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80321002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    559: _tools.RODict({
        "ID": 559,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80331002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    560: _tools.RODict({
        "ID": 560,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80411002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    561: _tools.RODict({
        "ID": 561,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80421002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    562: _tools.RODict({
        "ID": 562,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80431002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    563: _tools.RODict({
        "ID": 563,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80581002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 1000
    }),
    564: _tools.RODict({
        "ID": 564,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80111003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 500
    }),
    565: _tools.RODict({
        "ID": 565,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80121003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 500
    }),
    566: _tools.RODict({
        "ID": 566,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80131003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 500
    }),
    567: _tools.RODict({
        "ID": 567,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80211003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    568: _tools.RODict({
        "ID": 568,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80221003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    569: _tools.RODict({
        "ID": 569,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80231003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    570: _tools.RODict({
        "ID": 570,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80311003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    571: _tools.RODict({
        "ID": 571,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80321003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    572: _tools.RODict({
        "ID": 572,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80331003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    573: _tools.RODict({
        "ID": 573,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80411003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    574: _tools.RODict({
        "ID": 574,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80421003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    575: _tools.RODict({
        "ID": 575,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80431003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    576: _tools.RODict({
        "ID": 576,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80581003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 500
    }),
    577: _tools.RODict({
        "ID": 577,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80112001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 200
    }),
    578: _tools.RODict({
        "ID": 578,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80122001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 200
    }),
    579: _tools.RODict({
        "ID": 579,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80132001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 200
    }),
    580: _tools.RODict({
        "ID": 580,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80212001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    581: _tools.RODict({
        "ID": 581,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80222001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    582: _tools.RODict({
        "ID": 582,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80232001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    583: _tools.RODict({
        "ID": 583,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80312001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    584: _tools.RODict({
        "ID": 584,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80322001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    585: _tools.RODict({
        "ID": 585,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80332001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    586: _tools.RODict({
        "ID": 586,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80412001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    587: _tools.RODict({
        "ID": 587,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80422001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    588: _tools.RODict({
        "ID": 588,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80432001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    589: _tools.RODict({
        "ID": 589,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80582001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 200
    }),
    590: _tools.RODict({
        "ID": 590,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80682001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 200
    }),
    591: _tools.RODict({
        "ID": 591,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80692001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 200
    }),
    592: _tools.RODict({
        "ID": 592,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80782001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 200
    }),
    593: _tools.RODict({
        "ID": 593,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80792001,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 200
    }),
    594: _tools.RODict({
        "ID": 594,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80112002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 100
    }),
    595: _tools.RODict({
        "ID": 595,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80122002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 100
    }),
    596: _tools.RODict({
        "ID": 596,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80132002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 100
    }),
    597: _tools.RODict({
        "ID": 597,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80212002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    598: _tools.RODict({
        "ID": 598,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80222002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    599: _tools.RODict({
        "ID": 599,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80232002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    600: _tools.RODict({
        "ID": 600,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80312002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    601: _tools.RODict({
        "ID": 601,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80322002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    602: _tools.RODict({
        "ID": 602,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80332002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    603: _tools.RODict({
        "ID": 603,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80412002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    604: _tools.RODict({
        "ID": 604,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80422002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    605: _tools.RODict({
        "ID": 605,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80432002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    606: _tools.RODict({
        "ID": 606,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80582002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 100
    }),
    607: _tools.RODict({
        "ID": 607,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80682002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 100
    }),
    608: _tools.RODict({
        "ID": 608,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80692002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 100
    }),
    609: _tools.RODict({
        "ID": 609,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80782002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 100
    }),
    610: _tools.RODict({
        "ID": 610,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80792002,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 100
    }),
    611: _tools.RODict({
        "ID": 611,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80112003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 50
    }),
    612: _tools.RODict({
        "ID": 612,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80122003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 50
    }),
    613: _tools.RODict({
        "ID": 613,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80132003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 50
    }),
    614: _tools.RODict({
        "ID": 614,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80212003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    615: _tools.RODict({
        "ID": 615,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80222003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    616: _tools.RODict({
        "ID": 616,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80232003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    617: _tools.RODict({
        "ID": 617,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80312003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    618: _tools.RODict({
        "ID": 618,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80322003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    619: _tools.RODict({
        "ID": 619,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80332003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    620: _tools.RODict({
        "ID": 620,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80412003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    621: _tools.RODict({
        "ID": 621,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80422003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    622: _tools.RODict({
        "ID": 622,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80432003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    623: _tools.RODict({
        "ID": 623,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80582003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 600,
        "bindWeight": 50
    }),
    624: _tools.RODict({
        "ID": 624,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80682003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 50
    }),
    625: _tools.RODict({
        "ID": 625,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80692003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 50
    }),
    626: _tools.RODict({
        "ID": 626,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80782003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 50
    }),
    627: _tools.RODict({
        "ID": 627,
        "dropPackage": 2001,
        "dropCondition": None,
        "dropTarget": 80792003,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 300,
        "bindWeight": 50
    }),
    628: _tools.RODict({
        "ID": 628,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000115,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    629: _tools.RODict({
        "ID": 629,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000116,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    630: _tools.RODict({
        "ID": 630,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000117,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    631: _tools.RODict({
        "ID": 631,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000118,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    632: _tools.RODict({
        "ID": 632,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000119,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    633: _tools.RODict({
        "ID": 633,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000120,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    634: _tools.RODict({
        "ID": 634,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000121,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    635: _tools.RODict({
        "ID": 635,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000122,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    636: _tools.RODict({
        "ID": 636,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000123,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    637: _tools.RODict({
        "ID": 637,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000124,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    638: _tools.RODict({
        "ID": 638,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000125,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    639: _tools.RODict({
        "ID": 639,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000126,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    640: _tools.RODict({
        "ID": 640,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1001)]),
        "dropTarget": 30000127,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    641: _tools.RODict({
        "ID": 641,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000154,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    642: _tools.RODict({
        "ID": 642,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000155,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    643: _tools.RODict({
        "ID": 643,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000156,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    644: _tools.RODict({
        "ID": 644,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000157,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    645: _tools.RODict({
        "ID": 645,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000158,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    646: _tools.RODict({
        "ID": 646,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000159,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    647: _tools.RODict({
        "ID": 647,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000160,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    648: _tools.RODict({
        "ID": 648,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000161,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    649: _tools.RODict({
        "ID": 649,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000162,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    650: _tools.RODict({
        "ID": 650,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000163,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    651: _tools.RODict({
        "ID": 651,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000164,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    652: _tools.RODict({
        "ID": 652,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000165,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    653: _tools.RODict({
        "ID": 653,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1002)]),
        "dropTarget": 30000166,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    654: _tools.RODict({
        "ID": 654,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000193,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    655: _tools.RODict({
        "ID": 655,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000194,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    656: _tools.RODict({
        "ID": 656,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000195,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    657: _tools.RODict({
        "ID": 657,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000196,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    658: _tools.RODict({
        "ID": 658,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000197,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    659: _tools.RODict({
        "ID": 659,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000198,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    660: _tools.RODict({
        "ID": 660,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000199,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    661: _tools.RODict({
        "ID": 661,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000200,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    662: _tools.RODict({
        "ID": 662,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000201,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    663: _tools.RODict({
        "ID": 663,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000202,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    664: _tools.RODict({
        "ID": 664,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000203,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    665: _tools.RODict({
        "ID": 665,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000204,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    666: _tools.RODict({
        "ID": 666,
        "dropPackage": 1512,
        "dropCondition": _tools.ROList([(2, 1003)]),
        "dropTarget": 30000205,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 200,
        "bindWeight": 0
    }),
    667: _tools.RODict({
        "ID": 667,
        "dropPackage": 1513,
        "dropCondition": None,
        "dropTarget": 30000287,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 5000,
        "bindWeight": 5000
    }),
    668: _tools.RODict({
        "ID": 668,
        "dropPackage": 1513,
        "dropCondition": None,
        "dropTarget": 30000288,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 5000,
        "bindWeight": 5000
    }),
    669: _tools.RODict({
        "ID": 669,
        "dropPackage": 1513,
        "dropCondition": None,
        "dropTarget": 30000289,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 5000,
        "bindWeight": 5000
    }),
    670: _tools.RODict({
        "ID": 670,
        "dropPackage": 1513,
        "dropCondition": None,
        "dropTarget": 30000290,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 500,
        "bindWeight": 5000
    }),
    671: _tools.RODict({
        "ID": 671,
        "dropPackage": 1513,
        "dropCondition": None,
        "dropTarget": 30000291,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 500,
        "bindWeight": 5000
    }),
    672: _tools.RODict({
        "ID": 672,
        "dropPackage": 1513,
        "dropCondition": None,
        "dropTarget": 30000292,
        "dropNumMin": 1,
        "dropNumMax": 1,
        "weight": 500,
        "bindWeight": 5000
    })
})
minKey = 1
maxKey = 672

dropPackageData = _tools.RODict({ 
        10041:[{'ID': 1, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80792001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 900, 'bindWeight': 5000}, {'ID': 2, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80792002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 90, 'bindWeight': 5000}, {'ID': 3, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80792003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 90, 'bindWeight': 5000}, {'ID': 4, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80792004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 400, 'bindWeight': 5000}, {'ID': 5, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80793001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 5000}, {'ID': 6, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80793002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 5000}, {'ID': 7, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80793003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 5000}, {'ID': 8, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80793004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 5000}, {'ID': 9, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80793005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 10, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80794001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}, {'ID': 11, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80794002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}, {'ID': 12, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80794003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 100, 'bindWeight': 5000}, {'ID': 13, 'dropPackage': 10041, 'dropCondition': None, 'dropTarget': 80795001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 10, 'bindWeight': 5000}],
        10042:[{'ID': 14, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80703001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 900, 'bindWeight': 5000}, {'ID': 15, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80703002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 90, 'bindWeight': 5000}, {'ID': 16, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80703003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 90, 'bindWeight': 5000}, {'ID': 17, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80703004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 400, 'bindWeight': 5000}, {'ID': 18, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80703005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 5000}, {'ID': 19, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80704001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 5000}, {'ID': 20, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80704002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 5000}, {'ID': 21, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80704003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 5000}, {'ID': 22, 'dropPackage': 10042, 'dropCondition': None, 'dropTarget': 80705002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}],
        1001:[{'ID': 23, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80111001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 24, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80121001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 25, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80131001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 26, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80211001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 27, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80221001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 28, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80231001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 29, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80311001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 30, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80321001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 31, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80331001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 32, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80411001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 33, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80421001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 34, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80431001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 35, 'dropPackage': 1001, 'dropCondition': None, 'dropTarget': 80581001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}],
        1002:[{'ID': 36, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80111002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 37, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80121002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 38, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80131002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 39, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80211002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 40, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80221002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 41, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80231002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 42, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80311002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 43, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80321002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 44, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80331002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 45, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80411002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 46, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80421002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 47, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80431002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 48, 'dropPackage': 1002, 'dropCondition': None, 'dropTarget': 80581002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}],
        1003:[{'ID': 49, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80111003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 50, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80121003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 51, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80131003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 52, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80211003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 53, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80221003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 54, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80231003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 55, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80311003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 56, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80321003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 57, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80331003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 58, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80411003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 59, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80421003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 60, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80431003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 61, 'dropPackage': 1003, 'dropCondition': None, 'dropTarget': 80581003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}],
        1004:[{'ID': 62, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80112001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 63, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80122001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 64, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80132001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 65, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80212001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 66, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80222001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 67, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80232001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 68, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80312001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 69, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80322001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 70, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80332001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 71, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80412001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 72, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80422001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 73, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80432001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 74, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80582001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 75, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80682001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 76, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80692001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 77, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80782001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 78, 'dropPackage': 1004, 'dropCondition': None, 'dropTarget': 80792001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1005:[{'ID': 79, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80112002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 80, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80122002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 81, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80132002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 82, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80212002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 83, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80222002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 84, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80232002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 85, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80312002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 86, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80322002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 87, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80332002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 88, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80412002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 89, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80422002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 90, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80432002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 91, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80582002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 92, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80682002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 93, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80692002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 94, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80782002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 95, 'dropPackage': 1005, 'dropCondition': None, 'dropTarget': 80792002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1006:[{'ID': 96, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80112003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 97, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80122003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 98, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80132003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 99, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80212003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 100, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80222003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 101, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80232003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 102, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80312003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 103, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80322003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 104, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80332003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 105, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80412003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 106, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80422003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 107, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80432003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 108, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80582003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 109, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80682003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 110, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80692003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 111, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80782003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 112, 'dropPackage': 1006, 'dropCondition': None, 'dropTarget': 80792003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1301:[{'ID': 113, 'dropPackage': 1301, 'dropCondition': None, 'dropTarget': 30010021, 'dropNumMin': 2, 'dropNumMax': 6, 'weight': 300, 'bindWeight': 0}, {'ID': 114, 'dropPackage': 1301, 'dropCondition': None, 'dropTarget': 30010022, 'dropNumMin': 2, 'dropNumMax': 6, 'weight': 300, 'bindWeight': 0}, {'ID': 115, 'dropPackage': 1301, 'dropCondition': None, 'dropTarget': 30010023, 'dropNumMin': 2, 'dropNumMax': 6, 'weight': 300, 'bindWeight': 0}, {'ID': 116, 'dropPackage': 1301, 'dropCondition': None, 'dropTarget': 30010024, 'dropNumMin': 2, 'dropNumMax': 6, 'weight': 300, 'bindWeight': 0}],
        1302:[{'ID': 117, 'dropPackage': 1302, 'dropCondition': None, 'dropTarget': 30010021, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 300, 'bindWeight': 0}, {'ID': 118, 'dropPackage': 1302, 'dropCondition': None, 'dropTarget': 30010022, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 300, 'bindWeight': 0}, {'ID': 119, 'dropPackage': 1302, 'dropCondition': None, 'dropTarget': 30010023, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 300, 'bindWeight': 0}, {'ID': 120, 'dropPackage': 1302, 'dropCondition': None, 'dropTarget': 30010024, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 300, 'bindWeight': 0}],
        1303:[{'ID': 121, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990135, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 122, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990136, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 123, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990137, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 124, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990138, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 125, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990139, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 126, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990140, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 127, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990141, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 128, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990142, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}, {'ID': 129, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990143, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}, {'ID': 130, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990144, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}, {'ID': 131, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990145, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}, {'ID': 132, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990146, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}, {'ID': 133, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990147, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}, {'ID': 134, 'dropPackage': 1303, 'dropCondition': None, 'dropTarget': 30990148, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 5000}],
        1501:[{'ID': 135, 'dropPackage': 1501, 'dropCondition': None, 'dropTarget': 30990121, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 100, 'bindWeight': 5000}, {'ID': 136, 'dropPackage': 1501, 'dropCondition': None, 'dropTarget': 30990122, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 137, 'dropPackage': 1501, 'dropCondition': None, 'dropTarget': 30990123, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 138, 'dropPackage': 1501, 'dropCondition': None, 'dropTarget': 30990124, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 139, 'dropPackage': 1501, 'dropCondition': None, 'dropTarget': 30990125, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 140, 'dropPackage': 1501, 'dropCondition': None, 'dropTarget': 30990126, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 150, 'bindWeight': 5000}, {'ID': 141, 'dropPackage': 1501, 'dropCondition': None, 'dropTarget': 30990127, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 150, 'bindWeight': 5000}],
        1502:[{'ID': 142, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000102, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 143, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000103, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 144, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000104, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 145, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000105, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 146, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000106, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 147, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000107, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 148, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000108, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 149, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000109, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 150, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000110, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 151, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000111, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 152, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000112, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 153, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000113, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 154, 'dropPackage': 1502, 'dropCondition': [(2, 1001)], 'dropTarget': 30000114, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 155, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000141, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 156, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000142, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 157, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000143, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 158, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000144, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 159, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000145, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 160, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000146, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 161, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000147, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 162, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000148, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 163, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000149, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 164, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000150, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 165, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000151, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 166, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000152, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 167, 'dropPackage': 1502, 'dropCondition': [(2, 1002)], 'dropTarget': 30000153, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 168, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000180, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 169, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000181, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 170, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000182, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 171, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000183, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 172, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000184, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 173, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000185, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 174, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000186, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 175, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000187, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 176, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000188, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 177, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000189, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 178, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000190, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 179, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000191, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 180, 'dropPackage': 1502, 'dropCondition': [(2, 1003)], 'dropTarget': 30000192, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}],
        1503:[{'ID': 181, 'dropPackage': 1503, 'dropCondition': None, 'dropTarget': 30000287, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 182, 'dropPackage': 1503, 'dropCondition': None, 'dropTarget': 30000288, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 183, 'dropPackage': 1503, 'dropCondition': None, 'dropTarget': 30000289, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}],
        1504:[{'ID': 184, 'dropPackage': 1504, 'dropCondition': None, 'dropTarget': 30000290, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 185, 'dropPackage': 1504, 'dropCondition': None, 'dropTarget': 30000291, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 186, 'dropPackage': 1504, 'dropCondition': None, 'dropTarget': 30000292, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}],
        1505:[{'ID': 187, 'dropPackage': 1505, 'dropCondition': None, 'dropTarget': 30000293, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 188, 'dropPackage': 1505, 'dropCondition': None, 'dropTarget': 30000294, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 189, 'dropPackage': 1505, 'dropCondition': None, 'dropTarget': 30000295, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}],
        1506:[{'ID': 190, 'dropPackage': 1506, 'dropCondition': None, 'dropTarget': 30000296, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 191, 'dropPackage': 1506, 'dropCondition': None, 'dropTarget': 30000297, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 192, 'dropPackage': 1506, 'dropCondition': None, 'dropTarget': 30000298, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}],
        1507:[{'ID': 193, 'dropPackage': 1507, 'dropCondition': None, 'dropTarget': 30990128, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 100, 'bindWeight': 5000}, {'ID': 194, 'dropPackage': 1507, 'dropCondition': None, 'dropTarget': 30990129, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 195, 'dropPackage': 1507, 'dropCondition': None, 'dropTarget': 30990130, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 196, 'dropPackage': 1507, 'dropCondition': None, 'dropTarget': 30990131, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 197, 'dropPackage': 1507, 'dropCondition': None, 'dropTarget': 30990132, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 198, 'dropPackage': 1507, 'dropCondition': None, 'dropTarget': 30990133, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 150, 'bindWeight': 5000}, {'ID': 199, 'dropPackage': 1507, 'dropCondition': None, 'dropTarget': 30990134, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 150, 'bindWeight': 5000}],
        1508:[{'ID': 200, 'dropPackage': 1508, 'dropCondition': None, 'dropTarget': 30990135, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 100, 'bindWeight': 5000}, {'ID': 201, 'dropPackage': 1508, 'dropCondition': None, 'dropTarget': 30990136, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 202, 'dropPackage': 1508, 'dropCondition': None, 'dropTarget': 30990137, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 203, 'dropPackage': 1508, 'dropCondition': None, 'dropTarget': 30990138, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 204, 'dropPackage': 1508, 'dropCondition': None, 'dropTarget': 30990139, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 205, 'dropPackage': 1508, 'dropCondition': None, 'dropTarget': 30990140, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 150, 'bindWeight': 5000}, {'ID': 206, 'dropPackage': 1508, 'dropCondition': None, 'dropTarget': 30990141, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 150, 'bindWeight': 5000}],
        1509:[{'ID': 207, 'dropPackage': 1509, 'dropCondition': None, 'dropTarget': 30990142, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 100, 'bindWeight': 5000}, {'ID': 208, 'dropPackage': 1509, 'dropCondition': None, 'dropTarget': 30990143, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 209, 'dropPackage': 1509, 'dropCondition': None, 'dropTarget': 30990144, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 210, 'dropPackage': 1509, 'dropCondition': None, 'dropTarget': 30990145, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 211, 'dropPackage': 1509, 'dropCondition': None, 'dropTarget': 30990146, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 212, 'dropPackage': 1509, 'dropCondition': None, 'dropTarget': 30990147, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 150, 'bindWeight': 5000}, {'ID': 213, 'dropPackage': 1509, 'dropCondition': None, 'dropTarget': 30990148, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 150, 'bindWeight': 5000}],
        1007:[{'ID': 214, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80113001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 215, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80123001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 216, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80133001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 217, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80213001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 218, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80223001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 219, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80233001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 220, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80313001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 221, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80323001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 222, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80333001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 223, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80413001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 224, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80423001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 225, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80433001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 226, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80583001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 227, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80683001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 228, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80693001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 229, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80783001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 230, 'dropPackage': 1007, 'dropCondition': None, 'dropTarget': 80793001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1008:[{'ID': 231, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80113002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 232, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80123002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 233, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80133002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 234, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80213002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 235, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80223002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 236, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80233002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 237, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80313002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 238, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80323002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 239, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80333002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 240, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80413002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 241, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80423002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 242, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80433002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 243, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80583002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 244, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80683002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 245, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80693002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 246, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80783002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 247, 'dropPackage': 1008, 'dropCondition': None, 'dropTarget': 80793002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1009:[{'ID': 248, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80113003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 249, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80123003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 250, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80133003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 251, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80213003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 252, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80223003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 253, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80233003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 254, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80313003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 255, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80323003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 256, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80333003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 257, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80413003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 258, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80423003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 259, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80433003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 260, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80583003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 261, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80683003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 262, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80693003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 263, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80783003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 264, 'dropPackage': 1009, 'dropCondition': None, 'dropTarget': 80793003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1010:[{'ID': 265, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80113004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 266, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80123004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 267, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80133004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 268, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80213004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 269, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80223004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 270, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80233004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 271, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80313004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 272, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80323004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 273, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80333004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 274, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80413004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 275, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80423004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 276, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80433004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 277, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80583004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 278, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80683004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 279, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80693004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 280, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80783004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 281, 'dropPackage': 1010, 'dropCondition': None, 'dropTarget': 80793004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1011:[{'ID': 282, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80113005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 283, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80123005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 284, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80133005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 285, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80213005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 286, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80223005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 287, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80233005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 288, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80313005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 289, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80323005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 290, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80333005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 291, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80413005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 292, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80423005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 293, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80433005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 294, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80583005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 295, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80683005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 296, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80693005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 297, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80783005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 298, 'dropPackage': 1011, 'dropCondition': None, 'dropTarget': 80793005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1012:[{'ID': 299, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80114001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 300, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80124001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 301, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80134001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 302, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80214001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 303, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80224001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 304, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80234001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 305, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80314001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 306, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80324001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 307, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80334001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 308, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80414001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 309, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80424001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 310, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80434001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 311, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80584001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 312, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80684001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 313, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80694001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 314, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80784001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 315, 'dropPackage': 1012, 'dropCondition': None, 'dropTarget': 80794001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1013:[{'ID': 316, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80114002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 317, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80124002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 318, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80134002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 319, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80214002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 320, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80224002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 321, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80234002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 322, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80314002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 323, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80324002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 324, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80334002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 325, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80414002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 326, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80424002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 327, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80434002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 328, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80584002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 329, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80684002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 330, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80694002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 331, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80784002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 332, 'dropPackage': 1013, 'dropCondition': None, 'dropTarget': 80794002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        1014:[{'ID': 333, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80114003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 334, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80124003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 335, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80134003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 5000}, {'ID': 336, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80214003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 337, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80224003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 338, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80234003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 339, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80314003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 340, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80324003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 341, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80334003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 342, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80414003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 343, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80424003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 344, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80434003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 345, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80584003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 5000}, {'ID': 346, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80684003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 347, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80694003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 348, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80784003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}, {'ID': 349, 'dropPackage': 1014, 'dropCondition': None, 'dropTarget': 80794003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 5000}],
        11002:[{'ID': 351, 'dropPackage': 11002, 'dropCondition': None, 'dropTarget': 30000227, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 899, 'bindWeight': 10000}, {'ID': 352, 'dropPackage': 11002, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 100, 'bindWeight': 10000}, {'ID': 353, 'dropPackage': 11002, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 10000}],
        11003:[{'ID': 355, 'dropPackage': 11003, 'dropCondition': None, 'dropTarget': 30000227, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 878, 'bindWeight': 10000}, {'ID': 356, 'dropPackage': 11003, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 120, 'bindWeight': 10000}, {'ID': 357, 'dropPackage': 11003, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2, 'bindWeight': 10000}],
        11004:[{'ID': 359, 'dropPackage': 11004, 'dropCondition': None, 'dropTarget': 30000227, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 857, 'bindWeight': 10000}, {'ID': 360, 'dropPackage': 11004, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 140, 'bindWeight': 10000}, {'ID': 361, 'dropPackage': 11004, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 3, 'bindWeight': 10000}],
        11005:[{'ID': 363, 'dropPackage': 11005, 'dropCondition': None, 'dropTarget': 30000227, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 836, 'bindWeight': 10000}, {'ID': 364, 'dropPackage': 11005, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 160, 'bindWeight': 10000}, {'ID': 365, 'dropPackage': 11005, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4, 'bindWeight': 10000}],
        11006:[{'ID': 366, 'dropPackage': 11006, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 4, 'dropNumMax': 6, 'weight': 899, 'bindWeight': 10000}, {'ID': 367, 'dropPackage': 11006, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 2, 'dropNumMax': 3, 'weight': 100, 'bindWeight': 10000}, {'ID': 368, 'dropPackage': 11006, 'dropCondition': None, 'dropTarget': 30000230, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 10000}],
        11007:[{'ID': 369, 'dropPackage': 11007, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 4, 'dropNumMax': 6, 'weight': 878, 'bindWeight': 10000}, {'ID': 370, 'dropPackage': 11007, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 2, 'dropNumMax': 3, 'weight': 120, 'bindWeight': 10000}, {'ID': 371, 'dropPackage': 11007, 'dropCondition': None, 'dropTarget': 30000230, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2, 'bindWeight': 10000}],
        11008:[{'ID': 372, 'dropPackage': 11008, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 4, 'dropNumMax': 6, 'weight': 857, 'bindWeight': 10000}, {'ID': 373, 'dropPackage': 11008, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 2, 'dropNumMax': 3, 'weight': 140, 'bindWeight': 10000}, {'ID': 374, 'dropPackage': 11008, 'dropCondition': None, 'dropTarget': 30000230, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 3, 'bindWeight': 10000}],
        11009:[{'ID': 375, 'dropPackage': 11009, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 4, 'dropNumMax': 6, 'weight': 836, 'bindWeight': 10000}, {'ID': 376, 'dropPackage': 11009, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 2, 'dropNumMax': 3, 'weight': 160, 'bindWeight': 10000}, {'ID': 377, 'dropPackage': 11009, 'dropCondition': None, 'dropTarget': 30000230, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4, 'bindWeight': 10000}],
        11010:[{'ID': 378, 'dropPackage': 11010, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 4, 'dropNumMax': 6, 'weight': 390, 'bindWeight': 10000}, {'ID': 379, 'dropPackage': 11010, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 2, 'dropNumMax': 3, 'weight': 600, 'bindWeight': 10000}, {'ID': 380, 'dropPackage': 11010, 'dropCondition': None, 'dropTarget': 30000230, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 10, 'bindWeight': 10000}],
        11011:[{'ID': 381, 'dropPackage': 11011, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 4, 'dropNumMax': 6, 'weight': 330, 'bindWeight': 10000}, {'ID': 382, 'dropPackage': 11011, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 2, 'dropNumMax': 3, 'weight': 650, 'bindWeight': 10000}, {'ID': 383, 'dropPackage': 11011, 'dropCondition': None, 'dropTarget': 30000230, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 20, 'bindWeight': 10000}],
        11012:[{'ID': 384, 'dropPackage': 11012, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 4, 'dropNumMax': 6, 'weight': 270, 'bindWeight': 10000}, {'ID': 385, 'dropPackage': 11012, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 2, 'dropNumMax': 3, 'weight': 700, 'bindWeight': 10000}, {'ID': 386, 'dropPackage': 11012, 'dropCondition': None, 'dropTarget': 30000230, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 30, 'bindWeight': 10000}],
        11013:[{'ID': 387, 'dropPackage': 11013, 'dropCondition': None, 'dropTarget': 30000228, 'dropNumMin': 4, 'dropNumMax': 6, 'weight': 210, 'bindWeight': 10000}, {'ID': 388, 'dropPackage': 11013, 'dropCondition': None, 'dropTarget': 30000229, 'dropNumMin': 2, 'dropNumMax': 3, 'weight': 750, 'bindWeight': 10000}, {'ID': 389, 'dropPackage': 11013, 'dropCondition': None, 'dropTarget': 30000230, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}],
        99:[{'ID': 390, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 391, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 392, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 393, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 394, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 395, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001006, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 396, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001007, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 397, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001008, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 398, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001009, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 399, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001010, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 400, 'dropPackage': 99, 'dropCondition': None, 'dropTarget': 30001036, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}],
        98:[{'ID': 401, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001011, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 402, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001012, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 403, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001013, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 404, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001014, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 405, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001015, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 406, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001016, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 407, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001017, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 408, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001018, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 409, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001019, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 410, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001020, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 411, 'dropPackage': 98, 'dropCondition': None, 'dropTarget': 30001037, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}],
        97:[{'ID': 412, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001021, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 413, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001022, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 414, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001023, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 415, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001024, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 416, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001025, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 417, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001026, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 418, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001027, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 419, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001028, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 420, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001029, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 421, 'dropPackage': 97, 'dropCondition': None, 'dropTarget': 30001038, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}],
        96:[{'ID': 422, 'dropPackage': 96, 'dropCondition': None, 'dropTarget': 30001030, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 423, 'dropPackage': 96, 'dropCondition': None, 'dropTarget': 30001031, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 424, 'dropPackage': 96, 'dropCondition': None, 'dropTarget': 30001032, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 425, 'dropPackage': 96, 'dropCondition': None, 'dropTarget': 30001033, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 426, 'dropPackage': 96, 'dropCondition': None, 'dropTarget': 30001034, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 427, 'dropPackage': 96, 'dropCondition': None, 'dropTarget': 30001035, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 428, 'dropPackage': 96, 'dropCondition': None, 'dropTarget': 30001039, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}, {'ID': 429, 'dropPackage': 96, 'dropCondition': None, 'dropTarget': 30001040, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 10000}],
        1510:[{'ID': 430, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000287, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 5000, 'bindWeight': 5000}, {'ID': 431, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000288, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 5000, 'bindWeight': 5000}, {'ID': 432, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000289, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 5000, 'bindWeight': 5000}, {'ID': 433, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000290, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2300, 'bindWeight': 5000}, {'ID': 434, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000291, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2300, 'bindWeight': 5000}, {'ID': 435, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000292, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2300, 'bindWeight': 5000}, {'ID': 436, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000293, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 500, 'bindWeight': 5000}, {'ID': 437, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000294, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 500, 'bindWeight': 5000}, {'ID': 438, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000295, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 500, 'bindWeight': 5000}, {'ID': 439, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000296, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 50, 'bindWeight': 5000}, {'ID': 440, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000297, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 50, 'bindWeight': 5000}, {'ID': 441, 'dropPackage': 1510, 'dropCondition': None, 'dropTarget': 30000298, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 50, 'bindWeight': 5000}],
        2000:[{'ID': 442, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4000, 'bindWeight': 10000}, {'ID': 443, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003004, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4000, 'bindWeight': 10000}, {'ID': 444, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003009, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4000, 'bindWeight': 10000}, {'ID': 445, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003017, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4000, 'bindWeight': 10000}, {'ID': 446, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003019, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4000, 'bindWeight': 10000}, {'ID': 447, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003020, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4000, 'bindWeight': 10000}, {'ID': 448, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003021, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4000, 'bindWeight': 10000}, {'ID': 449, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003022, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 4000, 'bindWeight': 10000}, {'ID': 450, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 451, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003007, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 452, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003010, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 453, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003012, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 454, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003015, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 455, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003033, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 456, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003035, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 457, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003037, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 458, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003040, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 459, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003044, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 460, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003049, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 461, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003050, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 700, 'bindWeight': 10000}, {'ID': 462, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 463, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003005, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 464, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003008, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 465, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003011, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 466, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003013, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 467, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003016, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 468, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003018, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 469, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003027, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 470, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003029, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 471, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003038, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 472, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003042, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 473, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003045, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 474, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003047, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 40, 'bindWeight': 10000}, {'ID': 475, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003023, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 476, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003025, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 477, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003034, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 478, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003036, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 479, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003039, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 480, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003041, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 481, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003043, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 482, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003046, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 483, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003048, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 14, 'bindWeight': 0}, {'ID': 484, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003006, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 0}, {'ID': 485, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003014, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 0}, {'ID': 486, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003024, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 0}, {'ID': 487, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003026, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 0}, {'ID': 488, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003028, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 0}, {'ID': 489, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003030, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 0}, {'ID': 490, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003031, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 0}, {'ID': 491, 'dropPackage': 2000, 'dropCondition': None, 'dropTarget': 30003032, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 0}],
        1511:[{'ID': 492, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990121, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2000, 'bindWeight': 5000}, {'ID': 493, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990122, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2000, 'bindWeight': 5000}, {'ID': 494, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990123, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2000, 'bindWeight': 5000}, {'ID': 495, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990124, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2000, 'bindWeight': 5000}, {'ID': 496, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990125, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2000, 'bindWeight': 5000}, {'ID': 497, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990126, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2000, 'bindWeight': 5000}, {'ID': 498, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990127, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 2000, 'bindWeight': 5000}, {'ID': 499, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990128, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 240, 'bindWeight': 5000}, {'ID': 500, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990129, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 240, 'bindWeight': 5000}, {'ID': 501, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990130, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 240, 'bindWeight': 5000}, {'ID': 502, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990131, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 240, 'bindWeight': 5000}, {'ID': 503, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990132, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 240, 'bindWeight': 5000}, {'ID': 504, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990133, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 240, 'bindWeight': 5000}, {'ID': 505, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990134, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 240, 'bindWeight': 5000}, {'ID': 506, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990135, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 24, 'bindWeight': 5000}, {'ID': 507, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990136, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 24, 'bindWeight': 5000}, {'ID': 508, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990137, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 24, 'bindWeight': 5000}, {'ID': 509, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990138, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 24, 'bindWeight': 5000}, {'ID': 510, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990139, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 24, 'bindWeight': 5000}, {'ID': 511, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990140, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 24, 'bindWeight': 5000}, {'ID': 512, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990141, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 24, 'bindWeight': 5000}, {'ID': 513, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990142, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 5000}, {'ID': 514, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990143, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 5000}, {'ID': 515, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990144, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 5000}, {'ID': 516, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990145, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 5000}, {'ID': 517, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990146, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 5000}, {'ID': 518, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990147, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 5000}, {'ID': 519, 'dropPackage': 1511, 'dropCondition': None, 'dropTarget': 30990148, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 1, 'bindWeight': 5000}],
        9200:[{'ID': 520, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010007, 'dropNumMin': 20, 'dropNumMax': 30, 'weight': 2000, 'bindWeight': 0}, {'ID': 521, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010008, 'dropNumMin': 20, 'dropNumMax': 30, 'weight': 2000, 'bindWeight': 0}, {'ID': 522, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010009, 'dropNumMin': 1, 'dropNumMax': 5, 'weight': 1000, 'bindWeight': 0}, {'ID': 523, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010010, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 500, 'bindWeight': 0}, {'ID': 524, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010011, 'dropNumMin': 1, 'dropNumMax': 5, 'weight': 1000, 'bindWeight': 0}, {'ID': 525, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010012, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 500, 'bindWeight': 0}, {'ID': 526, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010013, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 1000, 'bindWeight': 0}, {'ID': 527, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010014, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 2000, 'bindWeight': 0}, {'ID': 528, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010015, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 500, 'bindWeight': 0}, {'ID': 529, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010016, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 1000, 'bindWeight': 0}, {'ID': 530, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010017, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 2000, 'bindWeight': 0}, {'ID': 531, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010018, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 500, 'bindWeight': 0}, {'ID': 532, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010019, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 1000, 'bindWeight': 0}, {'ID': 533, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010020, 'dropNumMin': 1, 'dropNumMax': 3, 'weight': 2000, 'bindWeight': 0}, {'ID': 534, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010021, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 10, 'bindWeight': 0}, {'ID': 535, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010022, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 10, 'bindWeight': 0}, {'ID': 536, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010023, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 50, 'bindWeight': 0}, {'ID': 537, 'dropPackage': 9200, 'dropCondition': None, 'dropTarget': 30010024, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}],
        2001:[{'ID': 538, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80111001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 2000}, {'ID': 539, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80121001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 2000}, {'ID': 540, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80131001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 2000}, {'ID': 541, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80211001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 542, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80221001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 543, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80231001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 544, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80311001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 545, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80321001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 546, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80331001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 547, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80411001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 548, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80421001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 549, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80431001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 550, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80581001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 2000}, {'ID': 551, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80111002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 1000}, {'ID': 552, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80121002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 1000}, {'ID': 553, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80131002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 1000}, {'ID': 554, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80211002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 555, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80221002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 556, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80231002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 557, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80311002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 558, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80321002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 559, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80331002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 560, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80411002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 561, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80421002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 562, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80431002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 563, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80581002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 1000}, {'ID': 564, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80111003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 500}, {'ID': 565, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80121003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 500}, {'ID': 566, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80131003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 500}, {'ID': 567, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80211003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 568, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80221003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 569, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80231003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 570, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80311003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 571, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80321003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 572, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80331003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 573, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80411003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 574, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80421003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 575, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80431003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 576, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80581003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 500}, {'ID': 577, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80112001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 200}, {'ID': 578, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80122001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 200}, {'ID': 579, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80132001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 200}, {'ID': 580, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80212001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 581, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80222001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 582, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80232001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 583, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80312001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 584, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80322001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 585, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80332001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 586, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80412001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 587, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80422001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 588, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80432001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 589, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80582001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 200}, {'ID': 590, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80682001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 200}, {'ID': 591, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80692001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 200}, {'ID': 592, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80782001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 200}, {'ID': 593, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80792001, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 200}, {'ID': 594, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80112002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 100}, {'ID': 595, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80122002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 100}, {'ID': 596, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80132002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 100}, {'ID': 597, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80212002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 598, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80222002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 599, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80232002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 600, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80312002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 601, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80322002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 602, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80332002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 603, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80412002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 604, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80422002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 605, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80432002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 606, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80582002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 100}, {'ID': 607, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80682002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 100}, {'ID': 608, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80692002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 100}, {'ID': 609, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80782002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 100}, {'ID': 610, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80792002, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 100}, {'ID': 611, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80112003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 50}, {'ID': 612, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80122003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 50}, {'ID': 613, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80132003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 50}, {'ID': 614, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80212003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 615, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80222003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 616, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80232003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 617, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80312003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 618, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80322003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 619, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80332003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 620, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80412003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 621, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80422003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 622, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80432003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 623, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80582003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 600, 'bindWeight': 50}, {'ID': 624, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80682003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 50}, {'ID': 625, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80692003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 50}, {'ID': 626, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80782003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 50}, {'ID': 627, 'dropPackage': 2001, 'dropCondition': None, 'dropTarget': 80792003, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 300, 'bindWeight': 50}],
        1512:[{'ID': 628, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000115, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 629, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000116, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 630, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000117, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 631, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000118, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 632, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000119, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 633, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000120, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 634, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000121, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 635, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000122, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 636, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000123, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 637, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000124, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 638, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000125, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 639, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000126, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 640, 'dropPackage': 1512, 'dropCondition': [(2, 1001)], 'dropTarget': 30000127, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 641, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000154, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 642, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000155, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 643, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000156, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 644, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000157, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 645, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000158, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 646, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000159, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 647, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000160, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 648, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000161, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 649, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000162, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 650, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000163, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 651, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000164, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 652, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000165, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 653, 'dropPackage': 1512, 'dropCondition': [(2, 1002)], 'dropTarget': 30000166, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 654, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000193, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 655, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000194, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 656, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000195, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 657, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000196, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 658, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000197, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 659, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000198, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 660, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000199, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 661, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000200, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 662, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000201, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 663, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000202, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 664, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000203, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 665, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000204, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}, {'ID': 666, 'dropPackage': 1512, 'dropCondition': [(2, 1003)], 'dropTarget': 30000205, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 200, 'bindWeight': 0}],
        1513:[{'ID': 667, 'dropPackage': 1513, 'dropCondition': None, 'dropTarget': 30000287, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 5000, 'bindWeight': 5000}, {'ID': 668, 'dropPackage': 1513, 'dropCondition': None, 'dropTarget': 30000288, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 5000, 'bindWeight': 5000}, {'ID': 669, 'dropPackage': 1513, 'dropCondition': None, 'dropTarget': 30000289, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 5000, 'bindWeight': 5000}, {'ID': 670, 'dropPackage': 1513, 'dropCondition': None, 'dropTarget': 30000290, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 500, 'bindWeight': 5000}, {'ID': 671, 'dropPackage': 1513, 'dropCondition': None, 'dropTarget': 30000291, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 500, 'bindWeight': 5000}, {'ID': 672, 'dropPackage': 1513, 'dropCondition': None, 'dropTarget': 30000292, 'dropNumMin': 1, 'dropNumMax': 1, 'weight': 500, 'bindWeight': 5000}],
})
