# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: experience/exp
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
        "grade": 1,
        "expPlayer": 40,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 10000], [10001, 18000], [18001]),
        "idleIncome": (50, 55, 60)
    }),
    2: _tools.RODict({
        "ID": 2,
        "grade": 2,
        "expPlayer": 120,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 12000], [12001, 22000], [22001]),
        "idleIncome": (55, 60, 65)
    }),
    3: _tools.RODict({
        "ID": 3,
        "grade": 3,
        "expPlayer": 170,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 14000], [14001, 26000], [26001]),
        "idleIncome": (60, 65, 70)
    }),
    4: _tools.RODict({
        "ID": 4,
        "grade": 4,
        "expPlayer": 210,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 16000], [16001, 30000], [30001]),
        "idleIncome": (65, 70, 75)
    }),
    5: _tools.RODict({
        "ID": 5,
        "grade": 5,
        "expPlayer": 220,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 18000], [18001, 34000], [34001]),
        "idleIncome": (70, 75, 80)
    }),
    6: _tools.RODict({
        "ID": 6,
        "grade": 6,
        "expPlayer": 230,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 20000], [20001, 38000], [38001]),
        "idleIncome": (75, 80, 85)
    }),
    7: _tools.RODict({
        "ID": 7,
        "grade": 7,
        "expPlayer": 260,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 22000], [22001, 42000], [42001]),
        "idleIncome": (80, 85, 90)
    }),
    8: _tools.RODict({
        "ID": 8,
        "grade": 8,
        "expPlayer": 290,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 24000], [24001, 46000], [46001]),
        "idleIncome": (85, 90, 95)
    }),
    9: _tools.RODict({
        "ID": 9,
        "grade": 9,
        "expPlayer": 320,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 26000], [26001, 50000], [50001]),
        "idleIncome": (90, 95, 100)
    }),
    10: _tools.RODict({
        "ID": 10,
        "grade": 10,
        "expPlayer": 350,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 28000], [28001, 54000], [54001]),
        "idleIncome": (95, 100, 105)
    }),
    11: _tools.RODict({
        "ID": 11,
        "grade": 11,
        "expPlayer": 380,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 30000], [30001, 58000], [58001]),
        "idleIncome": (100, 105, 110)
    }),
    12: _tools.RODict({
        "ID": 12,
        "grade": 12,
        "expPlayer": 630,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 32000], [32001, 62000], [62001]),
        "idleIncome": (105, 110, 115)
    }),
    13: _tools.RODict({
        "ID": 13,
        "grade": 13,
        "expPlayer": 1140,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 34000], [34001, 66000], [66001]),
        "idleIncome": (110, 115, 120)
    }),
    14: _tools.RODict({
        "ID": 14,
        "grade": 14,
        "expPlayer": 2050,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 36000], [36001, 70000], [70001]),
        "idleIncome": (115, 120, 125)
    }),
    15: _tools.RODict({
        "ID": 15,
        "grade": 15,
        "expPlayer": 3700,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 38000], [38001, 74000], [74001]),
        "idleIncome": (120, 125, 130)
    }),
    16: _tools.RODict({
        "ID": 16,
        "grade": 16,
        "expPlayer": 6610,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 40000], [40001, 78000], [78001]),
        "idleIncome": (125, 130, 135)
    }),
    17: _tools.RODict({
        "ID": 17,
        "grade": 17,
        "expPlayer": 8751,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 42000], [42001, 82000], [82001]),
        "idleIncome": (130, 135, 140)
    }),
    18: _tools.RODict({
        "ID": 18,
        "grade": 18,
        "expPlayer": 11146,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 44000], [44001, 86000], [86001]),
        "idleIncome": (135, 140, 145)
    }),
    19: _tools.RODict({
        "ID": 19,
        "grade": 19,
        "expPlayer": 14113,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 46000], [46001, 90000], [90001]),
        "idleIncome": (140, 145, 150)
    }),
    20: _tools.RODict({
        "ID": 20,
        "grade": 20,
        "expPlayer": 17418,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 48000], [48001, 94000], [94001]),
        "idleIncome": (145, 150, 155)
    }),
    21: _tools.RODict({
        "ID": 21,
        "grade": 21,
        "expPlayer": 21060,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 50000], [50001, 98000], [98001]),
        "idleIncome": (150, 155, 160)
    }),
    22: _tools.RODict({
        "ID": 22,
        "grade": 22,
        "expPlayer": 25486,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 52000], [52001, 102000], [102001]),
        "idleIncome": (155, 160, 165)
    }),
    23: _tools.RODict({
        "ID": 23,
        "grade": 23,
        "expPlayer": 30333,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 54000], [54001, 106000], [106001]),
        "idleIncome": (160, 165, 170)
    }),
    24: _tools.RODict({
        "ID": 24,
        "grade": 24,
        "expPlayer": 36132,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 56000], [56001, 110000], [110001]),
        "idleIncome": (165, 170, 175)
    }),
    25: _tools.RODict({
        "ID": 25,
        "grade": 25,
        "expPlayer": 42438,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 58000], [58001, 114000], [114001]),
        "idleIncome": (170, 175, 180)
    }),
    26: _tools.RODict({
        "ID": 26,
        "grade": 26,
        "expPlayer": 52488,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 60000], [60001, 118000], [118001]),
        "idleIncome": (175, 180, 185)
    }),
    27: _tools.RODict({
        "ID": 27,
        "grade": 27,
        "expPlayer": 68429,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 62000], [62001, 122000], [122001]),
        "idleIncome": (180, 185, 190)
    }),
    28: _tools.RODict({
        "ID": 28,
        "grade": 28,
        "expPlayer": 87091,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 64000], [64001, 126000], [126001]),
        "idleIncome": (185, 190, 195)
    }),
    29: _tools.RODict({
        "ID": 29,
        "grade": 29,
        "expPlayer": 108864,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 66000], [66001, 130000], [130001]),
        "idleIncome": (190, 195, 200)
    }),
    30: _tools.RODict({
        "ID": 30,
        "grade": 30,
        "expPlayer": 132970,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 68000], [68001, 134000], [134001]),
        "idleIncome": (195, 200, 205)
    }),
    31: _tools.RODict({
        "ID": 31,
        "grade": 31,
        "expPlayer": 160704,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 70000], [70001, 138000], [138001]),
        "idleIncome": (200, 205, 210)
    }),
    32: _tools.RODict({
        "ID": 32,
        "grade": 32,
        "expPlayer": 196830,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 72000], [72001, 142000], [142001]),
        "idleIncome": (205, 210, 215)
    }),
    33: _tools.RODict({
        "ID": 33,
        "grade": 33,
        "expPlayer": 238140,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 74000], [74001, 146000], [146001]),
        "idleIncome": (210, 215, 220)
    }),
    34: _tools.RODict({
        "ID": 34,
        "grade": 34,
        "expPlayer": 285120,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 76000], [76001, 150000], [150001]),
        "idleIncome": (215, 220, 225)
    }),
    35: _tools.RODict({
        "ID": 35,
        "grade": 35,
        "expPlayer": 338256,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 78000], [78001, 154000], [154001]),
        "idleIncome": (220, 225, 230)
    }),
    36: _tools.RODict({
        "ID": 36,
        "grade": 36,
        "expPlayer": 400140,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 80000], [80001, 158000], [158001]),
        "idleIncome": (225, 230, 235)
    }),
    37: _tools.RODict({
        "ID": 37,
        "grade": 37,
        "expPlayer": 469476,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 82000], [82001, 162000], [162001]),
        "idleIncome": (230, 235, 240)
    }),
    38: _tools.RODict({
        "ID": 38,
        "grade": 38,
        "expPlayer": 549180,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 84000], [84001, 166000], [166001]),
        "idleIncome": (235, 240, 245)
    }),
    39: _tools.RODict({
        "ID": 39,
        "grade": 39,
        "expPlayer": 637632,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 86000], [86001, 170000], [170001]),
        "idleIncome": (240, 245, 250)
    }),
    40: _tools.RODict({
        "ID": 40,
        "grade": 40,
        "expPlayer": 764122,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 88000], [88001, 174000], [174001]),
        "idleIncome": (245, 250, 255)
    }),
    41: _tools.RODict({
        "ID": 41,
        "grade": 41,
        "expPlayer": 908237,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 90000], [90001, 178000], [178001]),
        "idleIncome": (250, 255, 260)
    }),
    42: _tools.RODict({
        "ID": 42,
        "grade": 42,
        "expPlayer": 1071533,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 92000], [92001, 182000], [182001]),
        "idleIncome": (255, 260, 265)
    }),
    43: _tools.RODict({
        "ID": 43,
        "grade": 43,
        "expPlayer": 1259194,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 94000], [94001, 186000], [186001]),
        "idleIncome": (260, 265, 270)
    }),
    44: _tools.RODict({
        "ID": 44,
        "grade": 44,
        "expPlayer": 1469664,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 96000], [96001, 190000], [190001]),
        "idleIncome": (265, 270, 275)
    }),
    45: _tools.RODict({
        "ID": 45,
        "grade": 45,
        "expPlayer": 1708646,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 98000], [98001, 194000], [194001]),
        "idleIncome": (270, 275, 280)
    }),
    46: _tools.RODict({
        "ID": 46,
        "grade": 46,
        "expPlayer": 1978474,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 100000], [100001, 198000], [198001]),
        "idleIncome": (275, 280, 285)
    }),
    47: _tools.RODict({
        "ID": 47,
        "grade": 47,
        "expPlayer": 2281478,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 102000], [102001, 202000], [202001]),
        "idleIncome": (280, 285, 290)
    }),
    48: _tools.RODict({
        "ID": 48,
        "grade": 48,
        "expPlayer": 2624918,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 104000], [104001, 206000], [206001]),
        "idleIncome": (285, 290, 295)
    }),
    49: _tools.RODict({
        "ID": 49,
        "grade": 49,
        "expPlayer": 3011904,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 106000], [106001, 210000], [210001]),
        "idleIncome": (290, 295, 300)
    }),
    50: _tools.RODict({
        "ID": 50,
        "grade": 50,
        "expPlayer": 3691656,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 108000], [108001, 214000], [214001]),
        "idleIncome": (295, 300, 305)
    }),
    51: _tools.RODict({
        "ID": 51,
        "grade": 51,
        "expPlayer": 4471200,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 110000], [110001, 218000], [218001]),
        "idleIncome": (300, 305, 310)
    }),
    52: _tools.RODict({
        "ID": 52,
        "grade": 52,
        "expPlayer": 5360256,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 112000], [112001, 222000], [222001]),
        "idleIncome": (305, 310, 315)
    }),
    53: _tools.RODict({
        "ID": 53,
        "grade": 53,
        "expPlayer": 6376320,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 114000], [114001, 226000], [226001]),
        "idleIncome": (310, 315, 320)
    }),
    54: _tools.RODict({
        "ID": 54,
        "grade": 54,
        "expPlayer": 7531056,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 116000], [116001, 230000], [230001]),
        "idleIncome": (315, 320, 325)
    }),
    55: _tools.RODict({
        "ID": 55,
        "grade": 55,
        "expPlayer": 8836128,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 118000], [118001, 234000], [234001]),
        "idleIncome": (320, 325, 330)
    }),
    56: _tools.RODict({
        "ID": 56,
        "grade": 56,
        "expPlayer": 11010816,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 120000], [120001, 238000], [238001]),
        "idleIncome": (325, 330, 335)
    }),
    57: _tools.RODict({
        "ID": 57,
        "grade": 57,
        "expPlayer": 13506912,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 122000], [122001, 242000], [242001]),
        "idleIncome": (330, 335, 340)
    }),
    58: _tools.RODict({
        "ID": 58,
        "grade": 58,
        "expPlayer": 16355520,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 124000], [124001, 246000], [246001]),
        "idleIncome": (335, 340, 345)
    }),
    59: _tools.RODict({
        "ID": 59,
        "grade": 59,
        "expPlayer": 19616256,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 126000], [126001, 250000], [250001]),
        "idleIncome": (340, 345, 350)
    }),
    60: _tools.RODict({
        "ID": 60,
        "grade": 60,
        "expPlayer": 23328000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 128000], [128001, 254000], [254001]),
        "idleIncome": (345, 350, 355)
    }),
    61: _tools.RODict({
        "ID": 61,
        "grade": 61,
        "expPlayer": 28605960,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 130000], [130001, 258000], [258001]),
        "idleIncome": (350, 355, 360)
    }),
    62: _tools.RODict({
        "ID": 62,
        "grade": 62,
        "expPlayer": 34642080,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 132000], [132001, 262000], [262001]),
        "idleIncome": (355, 360, 365)
    }),
    63: _tools.RODict({
        "ID": 63,
        "grade": 63,
        "expPlayer": 41527728,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 134000], [134001, 266000], [266001]),
        "idleIncome": (360, 365, 370)
    }),
    64: _tools.RODict({
        "ID": 64,
        "grade": 64,
        "expPlayer": 49385376,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 136000], [136001, 270000], [270001]),
        "idleIncome": (365, 370, 375)
    }),
    65: _tools.RODict({
        "ID": 65,
        "grade": 65,
        "expPlayer": 58327776,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 138000], [138001, 274000], [274001]),
        "idleIncome": (370, 375, 380)
    }),
    66: _tools.RODict({
        "ID": 66,
        "grade": 66,
        "expPlayer": 73366560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 140000], [140001, 278000], [278001]),
        "idleIncome": (375, 380, 385)
    }),
    67: _tools.RODict({
        "ID": 67,
        "grade": 67,
        "expPlayer": 88840800,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 142000], [142001, 282000], [282001]),
        "idleIncome": (380, 385, 390)
    }),
    68: _tools.RODict({
        "ID": 68,
        "grade": 68,
        "expPlayer": 106527960,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 144000], [144001, 286000], [286001]),
        "idleIncome": (385, 390, 395)
    }),
    69: _tools.RODict({
        "ID": 69,
        "grade": 69,
        "expPlayer": 126671040,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 146000], [146001, 290000], [290001]),
        "idleIncome": (390, 395, 400)
    }),
    70: _tools.RODict({
        "ID": 70,
        "grade": 70,
        "expPlayer": 149568120,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 148000], [148001, 294000], [294001]),
        "idleIncome": (395, 400, 405)
    }),
    71: _tools.RODict({
        "ID": 71,
        "grade": 71,
        "expPlayer": 169317540,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 150000], [150001, 298000], [298001]),
        "idleIncome": (400, 405, 410)
    }),
    72: _tools.RODict({
        "ID": 72,
        "grade": 72,
        "expPlayer": 191373840,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 152000], [152001, 302000], [302001]),
        "idleIncome": (405, 410, 415)
    }),
    73: _tools.RODict({
        "ID": 73,
        "grade": 73,
        "expPlayer": 216061020,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 154000], [154001, 306000], [306001]),
        "idleIncome": (410, 415, 420)
    }),
    74: _tools.RODict({
        "ID": 74,
        "grade": 74,
        "expPlayer": 243631800,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 156000], [156001, 310000], [310001]),
        "idleIncome": (415, 420, 425)
    }),
    75: _tools.RODict({
        "ID": 75,
        "grade": 75,
        "expPlayer": 274402080,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 158000], [158001, 314000], [314001]),
        "idleIncome": (420, 425, 430)
    }),
    76: _tools.RODict({
        "ID": 76,
        "grade": 76,
        "expPlayer": 308759040,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 160000], [160001, 318000], [318001]),
        "idleIncome": (425, 430, 435)
    }),
    77: _tools.RODict({
        "ID": 77,
        "grade": 77,
        "expPlayer": 347062320,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 162000], [162001, 322000], [322001]),
        "idleIncome": (430, 435, 440)
    }),
    78: _tools.RODict({
        "ID": 78,
        "grade": 78,
        "expPlayer": 389746080,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 164000], [164001, 326000], [326001]),
        "idleIncome": (435, 440, 445)
    }),
    79: _tools.RODict({
        "ID": 79,
        "grade": 79,
        "expPlayer": 437327100,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 166000], [166001, 330000], [330001]),
        "idleIncome": (440, 445, 450)
    }),
    80: _tools.RODict({
        "ID": 80,
        "grade": 80,
        "expPlayer": 490296240,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 168000], [168001, 334000], [334001]),
        "idleIncome": (445, 450, 455)
    }),
    81: _tools.RODict({
        "ID": 81,
        "grade": 81,
        "expPlayer": 549290160,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 170000], [170001, 338000], [338001]),
        "idleIncome": (450, 455, 460)
    }),
    82: _tools.RODict({
        "ID": 82,
        "grade": 82,
        "expPlayer": 614922840,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 172000], [172001, 342000], [342001]),
        "idleIncome": (455, 460, 465)
    }),
    83: _tools.RODict({
        "ID": 83,
        "grade": 83,
        "expPlayer": 687903840,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 174000], [174001, 346000], [346001]),
        "idleIncome": (460, 465, 470)
    }),
    84: _tools.RODict({
        "ID": 84,
        "grade": 84,
        "expPlayer": 769046400,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 176000], [176001, 350000], [350001]),
        "idleIncome": (465, 470, 475)
    }),
    85: _tools.RODict({
        "ID": 85,
        "grade": 85,
        "expPlayer": 859209120,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 178000], [178001, 354000], [354001]),
        "idleIncome": (470, 475, 480)
    }),
    86: _tools.RODict({
        "ID": 86,
        "grade": 86,
        "expPlayer": 959364000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 180000], [180001, 358000], [358001]),
        "idleIncome": (475, 480, 485)
    }),
    87: _tools.RODict({
        "ID": 87,
        "grade": 87,
        "expPlayer": 1070604540,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 182000], [182001, 362000], [362001]),
        "idleIncome": (480, 485, 490)
    }),
    88: _tools.RODict({
        "ID": 88,
        "grade": 88,
        "expPlayer": 1194082560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 184000], [184001, 366000], [366001]),
        "idleIncome": (485, 490, 495)
    }),
    89: _tools.RODict({
        "ID": 89,
        "grade": 89,
        "expPlayer": 1331154000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 186000], [186001, 370000], [370001]),
        "idleIncome": (490, 495, 500)
    }),
    90: _tools.RODict({
        "ID": 90,
        "grade": 90,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 188000], [188001, 374000], [374001]),
        "idleIncome": (495, 500, 505)
    }),
    91: _tools.RODict({
        "ID": 91,
        "grade": 91,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 190000], [190001, 378000], [378001]),
        "idleIncome": (500, 505, 510)
    }),
    92: _tools.RODict({
        "ID": 92,
        "grade": 92,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 192000], [192001, 382000], [382001]),
        "idleIncome": (505, 510, 515)
    }),
    93: _tools.RODict({
        "ID": 93,
        "grade": 93,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 194000], [194001, 386000], [386001]),
        "idleIncome": (510, 515, 520)
    }),
    94: _tools.RODict({
        "ID": 94,
        "grade": 94,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 196000], [196001, 390000], [390001]),
        "idleIncome": (515, 520, 525)
    }),
    95: _tools.RODict({
        "ID": 95,
        "grade": 95,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 198000], [198001, 394000], [394001]),
        "idleIncome": (520, 525, 530)
    }),
    96: _tools.RODict({
        "ID": 96,
        "grade": 96,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 200000], [200001, 398000], [398001]),
        "idleIncome": (525, 530, 535)
    }),
    97: _tools.RODict({
        "ID": 97,
        "grade": 97,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 202000], [202001, 402000], [402001]),
        "idleIncome": (530, 535, 540)
    }),
    98: _tools.RODict({
        "ID": 98,
        "grade": 98,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 204000], [204001, 406000], [406001]),
        "idleIncome": (535, 540, 545)
    }),
    99: _tools.RODict({
        "ID": 99,
        "grade": 99,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 206000], [206001, 410000], [410001]),
        "idleIncome": (540, 545, 550)
    }),
    100: _tools.RODict({
        "ID": 100,
        "grade": 100,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 208000], [208001, 414000], [414001]),
        "idleIncome": (545, 550, 555)
    }),
    101: _tools.RODict({
        "ID": 101,
        "grade": 101,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 210000], [210001, 418000], [418001]),
        "idleIncome": (550, 555, 560)
    }),
    102: _tools.RODict({
        "ID": 102,
        "grade": 102,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 212000], [212001, 422000], [422001]),
        "idleIncome": (555, 560, 565)
    }),
    103: _tools.RODict({
        "ID": 103,
        "grade": 103,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 214000], [214001, 426000], [426001]),
        "idleIncome": (560, 565, 570)
    }),
    104: _tools.RODict({
        "ID": 104,
        "grade": 104,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 216000], [216001, 430000], [430001]),
        "idleIncome": (565, 570, 575)
    }),
    105: _tools.RODict({
        "ID": 105,
        "grade": 105,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 218000], [218001, 434000], [434001]),
        "idleIncome": (570, 575, 580)
    }),
    106: _tools.RODict({
        "ID": 106,
        "grade": 106,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 220000], [220001, 438000], [438001]),
        "idleIncome": (575, 580, 585)
    }),
    107: _tools.RODict({
        "ID": 107,
        "grade": 107,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 222000], [222001, 442000], [442001]),
        "idleIncome": (580, 585, 590)
    }),
    108: _tools.RODict({
        "ID": 108,
        "grade": 108,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 224000], [224001, 446000], [446001]),
        "idleIncome": (585, 590, 595)
    }),
    109: _tools.RODict({
        "ID": 109,
        "grade": 109,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 226000], [226001, 450000], [450001]),
        "idleIncome": (590, 595, 600)
    }),
    110: _tools.RODict({
        "ID": 110,
        "grade": 110,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 228000], [228001, 454000], [454001]),
        "idleIncome": (595, 600, 605)
    }),
    111: _tools.RODict({
        "ID": 111,
        "grade": 111,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 230000], [230001, 458000], [458001]),
        "idleIncome": (600, 605, 610)
    }),
    112: _tools.RODict({
        "ID": 112,
        "grade": 112,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 232000], [232001, 462000], [462001]),
        "idleIncome": (605, 610, 615)
    }),
    113: _tools.RODict({
        "ID": 113,
        "grade": 113,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 234000], [234001, 466000], [466001]),
        "idleIncome": (610, 615, 620)
    }),
    114: _tools.RODict({
        "ID": 114,
        "grade": 114,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 236000], [236001, 470000], [470001]),
        "idleIncome": (615, 620, 625)
    }),
    115: _tools.RODict({
        "ID": 115,
        "grade": 115,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 238000], [238001, 474000], [474001]),
        "idleIncome": (620, 625, 630)
    }),
    116: _tools.RODict({
        "ID": 116,
        "grade": 116,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 240000], [240001, 478000], [478001]),
        "idleIncome": (625, 630, 635)
    }),
    117: _tools.RODict({
        "ID": 117,
        "grade": 117,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 242000], [242001, 482000], [482001]),
        "idleIncome": (630, 635, 640)
    }),
    118: _tools.RODict({
        "ID": 118,
        "grade": 118,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 244000], [244001, 486000], [486001]),
        "idleIncome": (635, 640, 645)
    }),
    119: _tools.RODict({
        "ID": 119,
        "grade": 119,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 246000], [246001, 490000], [490001]),
        "idleIncome": (640, 645, 650)
    }),
    120: _tools.RODict({
        "ID": 120,
        "grade": 120,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 248000], [248001, 494000], [494001]),
        "idleIncome": (645, 650, 655)
    }),
    121: _tools.RODict({
        "ID": 121,
        "grade": 121,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 250000], [250001, 498000], [498001]),
        "idleIncome": (650, 655, 660)
    }),
    122: _tools.RODict({
        "ID": 122,
        "grade": 122,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 252000], [252001, 502000], [502001]),
        "idleIncome": (655, 660, 665)
    }),
    123: _tools.RODict({
        "ID": 123,
        "grade": 123,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 254000], [254001, 506000], [506001]),
        "idleIncome": (660, 665, 670)
    }),
    124: _tools.RODict({
        "ID": 124,
        "grade": 124,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 256000], [256001, 510000], [510001]),
        "idleIncome": (665, 670, 675)
    }),
    125: _tools.RODict({
        "ID": 125,
        "grade": 125,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 258000], [258001, 514000], [514001]),
        "idleIncome": (670, 675, 680)
    }),
    126: _tools.RODict({
        "ID": 126,
        "grade": 126,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 260000], [260001, 518000], [518001]),
        "idleIncome": (675, 680, 685)
    }),
    127: _tools.RODict({
        "ID": 127,
        "grade": 127,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 262000], [262001, 522000], [522001]),
        "idleIncome": (680, 685, 690)
    }),
    128: _tools.RODict({
        "ID": 128,
        "grade": 128,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 264000], [264001, 526000], [526001]),
        "idleIncome": (685, 690, 695)
    }),
    129: _tools.RODict({
        "ID": 129,
        "grade": 129,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 266000], [266001, 530000], [530001]),
        "idleIncome": (690, 695, 700)
    }),
    130: _tools.RODict({
        "ID": 130,
        "grade": 130,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 268000], [268001, 534000], [534001]),
        "idleIncome": (695, 700, 705)
    }),
    131: _tools.RODict({
        "ID": 131,
        "grade": 131,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 270000], [270001, 538000], [538001]),
        "idleIncome": (700, 705, 710)
    }),
    132: _tools.RODict({
        "ID": 132,
        "grade": 132,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 272000], [272001, 542000], [542001]),
        "idleIncome": (705, 710, 715)
    }),
    133: _tools.RODict({
        "ID": 133,
        "grade": 133,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 274000], [274001, 546000], [546001]),
        "idleIncome": (710, 715, 720)
    }),
    134: _tools.RODict({
        "ID": 134,
        "grade": 134,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 276000], [276001, 550000], [550001]),
        "idleIncome": (715, 720, 725)
    }),
    135: _tools.RODict({
        "ID": 135,
        "grade": 135,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 278000], [278001, 554000], [554001]),
        "idleIncome": (720, 725, 730)
    }),
    136: _tools.RODict({
        "ID": 136,
        "grade": 136,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 280000], [280001, 558000], [558001]),
        "idleIncome": (725, 730, 735)
    }),
    137: _tools.RODict({
        "ID": 137,
        "grade": 137,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 282000], [282001, 562000], [562001]),
        "idleIncome": (730, 735, 740)
    }),
    138: _tools.RODict({
        "ID": 138,
        "grade": 138,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 284000], [284001, 566000], [566001]),
        "idleIncome": (735, 740, 745)
    }),
    139: _tools.RODict({
        "ID": 139,
        "grade": 139,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 286000], [286001, 570000], [570001]),
        "idleIncome": (740, 745, 750)
    }),
    140: _tools.RODict({
        "ID": 140,
        "grade": 140,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 288000], [288001, 574000], [574001]),
        "idleIncome": (745, 750, 755)
    }),
    141: _tools.RODict({
        "ID": 141,
        "grade": 141,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 290000], [290001, 578000], [578001]),
        "idleIncome": (750, 755, 760)
    }),
    142: _tools.RODict({
        "ID": 142,
        "grade": 142,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 292000], [292001, 582000], [582001]),
        "idleIncome": (755, 760, 765)
    }),
    143: _tools.RODict({
        "ID": 143,
        "grade": 143,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 294000], [294001, 586000], [586001]),
        "idleIncome": (760, 765, 770)
    }),
    144: _tools.RODict({
        "ID": 144,
        "grade": 144,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 296000], [296001, 590000], [590001]),
        "idleIncome": (765, 770, 775)
    }),
    145: _tools.RODict({
        "ID": 145,
        "grade": 145,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 298000], [298001, 594000], [594001]),
        "idleIncome": (770, 775, 780)
    }),
    146: _tools.RODict({
        "ID": 146,
        "grade": 146,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 300000], [300001, 598000], [598001]),
        "idleIncome": (775, 780, 785)
    }),
    147: _tools.RODict({
        "ID": 147,
        "grade": 147,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 302000], [302001, 602000], [602001]),
        "idleIncome": (780, 785, 790)
    }),
    148: _tools.RODict({
        "ID": 148,
        "grade": 148,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 304000], [304001, 606000], [606001]),
        "idleIncome": (785, 790, 795)
    }),
    149: _tools.RODict({
        "ID": 149,
        "grade": 149,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 306000], [306001, 610000], [610001]),
        "idleIncome": (790, 795, 800)
    }),
    150: _tools.RODict({
        "ID": 150,
        "grade": 150,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 308000], [308001, 614000], [614001]),
        "idleIncome": (795, 800, 805)
    }),
    151: _tools.RODict({
        "ID": 151,
        "grade": 151,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 310000], [310001, 618000], [618001]),
        "idleIncome": (800, 805, 810)
    }),
    152: _tools.RODict({
        "ID": 152,
        "grade": 152,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 312000], [312001, 622000], [622001]),
        "idleIncome": (805, 810, 815)
    }),
    153: _tools.RODict({
        "ID": 153,
        "grade": 153,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 314000], [314001, 626000], [626001]),
        "idleIncome": (810, 815, 820)
    }),
    154: _tools.RODict({
        "ID": 154,
        "grade": 154,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 316000], [316001, 630000], [630001]),
        "idleIncome": (815, 820, 825)
    }),
    155: _tools.RODict({
        "ID": 155,
        "grade": 155,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 318000], [318001, 634000], [634001]),
        "idleIncome": (820, 825, 830)
    }),
    156: _tools.RODict({
        "ID": 156,
        "grade": 156,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 320000], [320001, 638000], [638001]),
        "idleIncome": (825, 830, 835)
    }),
    157: _tools.RODict({
        "ID": 157,
        "grade": 157,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 322000], [322001, 642000], [642001]),
        "idleIncome": (830, 835, 840)
    }),
    158: _tools.RODict({
        "ID": 158,
        "grade": 158,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 324000], [324001, 646000], [646001]),
        "idleIncome": (835, 840, 845)
    }),
    159: _tools.RODict({
        "ID": 159,
        "grade": 159,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 326000], [326001, 650000], [650001]),
        "idleIncome": (840, 845, 850)
    }),
    160: _tools.RODict({
        "ID": 160,
        "grade": 160,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 328000], [328001, 654000], [654001]),
        "idleIncome": (845, 850, 855)
    }),
    161: _tools.RODict({
        "ID": 161,
        "grade": 161,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 330000], [330001, 658000], [658001]),
        "idleIncome": (850, 855, 860)
    }),
    162: _tools.RODict({
        "ID": 162,
        "grade": 162,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 332000], [332001, 662000], [662001]),
        "idleIncome": (855, 860, 865)
    }),
    163: _tools.RODict({
        "ID": 163,
        "grade": 163,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 334000], [334001, 666000], [666001]),
        "idleIncome": (860, 865, 870)
    }),
    164: _tools.RODict({
        "ID": 164,
        "grade": 164,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 336000], [336001, 670000], [670001]),
        "idleIncome": (865, 870, 875)
    }),
    165: _tools.RODict({
        "ID": 165,
        "grade": 165,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 338000], [338001, 674000], [674001]),
        "idleIncome": (870, 875, 880)
    }),
    166: _tools.RODict({
        "ID": 166,
        "grade": 166,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 340000], [340001, 678000], [678001]),
        "idleIncome": (875, 880, 885)
    }),
    167: _tools.RODict({
        "ID": 167,
        "grade": 167,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 342000], [342001, 682000], [682001]),
        "idleIncome": (880, 885, 890)
    }),
    168: _tools.RODict({
        "ID": 168,
        "grade": 168,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 344000], [344001, 686000], [686001]),
        "idleIncome": (885, 890, 895)
    }),
    169: _tools.RODict({
        "ID": 169,
        "grade": 169,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 346000], [346001, 690000], [690001]),
        "idleIncome": (890, 895, 900)
    }),
    170: _tools.RODict({
        "ID": 170,
        "grade": 170,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 348000], [348001, 694000], [694001]),
        "idleIncome": (895, 900, 905)
    }),
    171: _tools.RODict({
        "ID": 171,
        "grade": 171,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 350000], [350001, 698000], [698001]),
        "idleIncome": (900, 905, 910)
    }),
    172: _tools.RODict({
        "ID": 172,
        "grade": 172,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 352000], [352001, 702000], [702001]),
        "idleIncome": (905, 910, 915)
    }),
    173: _tools.RODict({
        "ID": 173,
        "grade": 173,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 354000], [354001, 706000], [706001]),
        "idleIncome": (910, 915, 920)
    }),
    174: _tools.RODict({
        "ID": 174,
        "grade": 174,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 356000], [356001, 710000], [710001]),
        "idleIncome": (915, 920, 925)
    }),
    175: _tools.RODict({
        "ID": 175,
        "grade": 175,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 358000], [358001, 714000], [714001]),
        "idleIncome": (920, 925, 930)
    }),
    176: _tools.RODict({
        "ID": 176,
        "grade": 176,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 360000], [360001, 718000], [718001]),
        "idleIncome": (925, 930, 935)
    }),
    177: _tools.RODict({
        "ID": 177,
        "grade": 177,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 362000], [362001, 722000], [722001]),
        "idleIncome": (930, 935, 940)
    }),
    178: _tools.RODict({
        "ID": 178,
        "grade": 178,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 364000], [364001, 726000], [726001]),
        "idleIncome": (935, 940, 945)
    }),
    179: _tools.RODict({
        "ID": 179,
        "grade": 179,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 366000], [366001, 730000], [730001]),
        "idleIncome": (940, 945, 950)
    }),
    180: _tools.RODict({
        "ID": 180,
        "grade": 180,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 368000], [368001, 734000], [734001]),
        "idleIncome": (945, 950, 955)
    }),
    181: _tools.RODict({
        "ID": 181,
        "grade": 181,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 370000], [370001, 738000], [738001]),
        "idleIncome": (950, 955, 960)
    }),
    182: _tools.RODict({
        "ID": 182,
        "grade": 182,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 372000], [372001, 742000], [742001]),
        "idleIncome": (955, 960, 965)
    }),
    183: _tools.RODict({
        "ID": 183,
        "grade": 183,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 374000], [374001, 746000], [746001]),
        "idleIncome": (960, 965, 970)
    }),
    184: _tools.RODict({
        "ID": 184,
        "grade": 184,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 376000], [376001, 750000], [750001]),
        "idleIncome": (965, 970, 975)
    }),
    185: _tools.RODict({
        "ID": 185,
        "grade": 185,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 378000], [378001, 754000], [754001]),
        "idleIncome": (970, 975, 980)
    }),
    186: _tools.RODict({
        "ID": 186,
        "grade": 186,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 380000], [380001, 758000], [758001]),
        "idleIncome": (975, 980, 985)
    }),
    187: _tools.RODict({
        "ID": 187,
        "grade": 187,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 382000], [382001, 762000], [762001]),
        "idleIncome": (980, 985, 990)
    }),
    188: _tools.RODict({
        "ID": 188,
        "grade": 188,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 384000], [384001, 766000], [766001]),
        "idleIncome": (985, 990, 995)
    }),
    189: _tools.RODict({
        "ID": 189,
        "grade": 189,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 386000], [386001, 770000], [770001]),
        "idleIncome": (990, 995, 1000)
    }),
    190: _tools.RODict({
        "ID": 190,
        "grade": 190,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 388000], [388001, 774000], [774001]),
        "idleIncome": (995, 1000, 1005)
    }),
    191: _tools.RODict({
        "ID": 191,
        "grade": 191,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 390000], [390001, 778000], [778001]),
        "idleIncome": (1000, 1005, 1010)
    }),
    192: _tools.RODict({
        "ID": 192,
        "grade": 192,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 392000], [392001, 782000], [782001]),
        "idleIncome": (1005, 1010, 1015)
    }),
    193: _tools.RODict({
        "ID": 193,
        "grade": 193,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 394000], [394001, 786000], [786001]),
        "idleIncome": (1010, 1015, 1020)
    }),
    194: _tools.RODict({
        "ID": 194,
        "grade": 194,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 396000], [396001, 790000], [790001]),
        "idleIncome": (1015, 1020, 1025)
    }),
    195: _tools.RODict({
        "ID": 195,
        "grade": 195,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 398000], [398001, 794000], [794001]),
        "idleIncome": (1020, 1025, 1030)
    }),
    196: _tools.RODict({
        "ID": 196,
        "grade": 196,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 400000], [400001, 798000], [798001]),
        "idleIncome": (1025, 1030, 1035)
    }),
    197: _tools.RODict({
        "ID": 197,
        "grade": 197,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 402000], [402001, 802000], [802001]),
        "idleIncome": (1030, 1035, 1040)
    }),
    198: _tools.RODict({
        "ID": 198,
        "grade": 198,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 404000], [404001, 806000], [806001]),
        "idleIncome": (1035, 1040, 1045)
    }),
    199: _tools.RODict({
        "ID": 199,
        "grade": 199,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 406000], [406001, 810000], [810001]),
        "idleIncome": (1040, 1045, 1050)
    }),
    200: _tools.RODict({
        "ID": 200,
        "grade": 200,
        "expPlayer": 1483171560,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 408000], [408001, 814000], [814001]),
        "idleIncome": (1045, 1050, 1055)
    })
})
minKey = 1
maxKey = 200