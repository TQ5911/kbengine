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
        "expPlayer": 15,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 2878], [2879, 3181], [3182]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    2: _tools.RODict({
        "ID": 2,
        "grade": 2,
        "expPlayer": 160,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3161], [3162, 3494], [3495]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    3: _tools.RODict({
        "ID": 3,
        "grade": 3,
        "expPlayer": 180,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3693], [3694, 4082], [4083]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    4: _tools.RODict({
        "ID": 4,
        "grade": 4,
        "expPlayer": 500,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3976], [3977, 4395], [4396]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    5: _tools.RODict({
        "ID": 5,
        "grade": 5,
        "expPlayer": 3000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 4508], [4509, 4983], [4984]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    6: _tools.RODict({
        "ID": 6,
        "grade": 6,
        "expPlayer": 3600,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 8116], [8117, 8971], [8972]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    7: _tools.RODict({
        "ID": 7,
        "grade": 7,
        "expPlayer": 4500,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 8529], [8530, 9426], [9427]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    8: _tools.RODict({
        "ID": 8,
        "grade": 8,
        "expPlayer": 5400,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 9158], [9159, 10122], [10123]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    9: _tools.RODict({
        "ID": 9,
        "grade": 9,
        "expPlayer": 6600,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 9676], [9677, 10695], [10696]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    10: _tools.RODict({
        "ID": 10,
        "grade": 10,
        "expPlayer": 7200,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 11216], [11217, 12397], [12398]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    11: _tools.RODict({
        "ID": 11,
        "grade": 11,
        "expPlayer": 15000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 12136], [12137, 13413], [13414]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    12: _tools.RODict({
        "ID": 12,
        "grade": 12,
        "expPlayer": 16200,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 12481], [12482, 13794], [13795]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    13: _tools.RODict({
        "ID": 13,
        "grade": 13,
        "expPlayer": 21600,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 13013], [13014, 14382], [14383]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    14: _tools.RODict({
        "ID": 14,
        "grade": 14,
        "expPlayer": 22800,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 13357], [13358, 14763], [14764]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    15: _tools.RODict({
        "ID": 15,
        "grade": 15,
        "expPlayer": 30000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 14240], [14241, 15739], [15740]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    16: _tools.RODict({
        "ID": 16,
        "grade": 16,
        "expPlayer": 30600,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 15514], [15515, 17147], [17148]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    17: _tools.RODict({
        "ID": 17,
        "grade": 17,
        "expPlayer": 32400,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 16074], [16075, 17767], [17768]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    18: _tools.RODict({
        "ID": 18,
        "grade": 18,
        "expPlayer": 36000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 16435], [16436, 18166], [18167]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    19: _tools.RODict({
        "ID": 19,
        "grade": 19,
        "expPlayer": 100000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 16954], [16955, 18739], [18740]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    20: _tools.RODict({
        "ID": 20,
        "grade": 20,
        "expPlayer": 150000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 19965], [19966, 22066], [22067]),
        "idleIncome": (855, 950, 997),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    21: _tools.RODict({
        "ID": 21,
        "grade": 21,
        "expPlayer": 175000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 20881], [20882, 23080], [23081]),
        "idleIncome": (900, 1000, 1050),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    22: _tools.RODict({
        "ID": 22,
        "grade": 22,
        "expPlayer": 250000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 21527], [21528, 23794], [23795]),
        "idleIncome": (945, 1050, 1102),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    23: _tools.RODict({
        "ID": 23,
        "grade": 23,
        "expPlayer": 600000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 22082], [22083, 24407], [24408]),
        "idleIncome": (990, 1100, 1155),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    24: _tools.RODict({
        "ID": 24,
        "grade": 24,
        "expPlayer": 700000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 23099], [23100, 25530], [25531]),
        "idleIncome": (1035, 1150, 1207),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    25: _tools.RODict({
        "ID": 25,
        "grade": 25,
        "expPlayer": 710000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 26443], [26444, 29226], [29227]),
        "idleIncome": (1080, 1200, 1260),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    26: _tools.RODict({
        "ID": 26,
        "grade": 26,
        "expPlayer": 720000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 27779], [27780, 30704], [30705]),
        "idleIncome": (1147, 1275, 1338),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    27: _tools.RODict({
        "ID": 27,
        "grade": 27,
        "expPlayer": 730000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 28670], [28671, 31687], [31688]),
        "idleIncome": (1192, 1325, 1391),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    28: _tools.RODict({
        "ID": 28,
        "grade": 28,
        "expPlayer": 900000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 29634], [29635, 32753], [32754]),
        "idleIncome": (1260, 1400, 1470),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    29: _tools.RODict({
        "ID": 29,
        "grade": 29,
        "expPlayer": 1100000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 30153], [30154, 33327], [33328]),
        "idleIncome": (1327, 1475, 1548),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    30: _tools.RODict({
        "ID": 30,
        "grade": 30,
        "expPlayer": 1400000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 36376], [36377, 40205], [40206]),
        "idleIncome": (1395, 1550, 1627),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    31: _tools.RODict({
        "ID": 31,
        "grade": 31,
        "expPlayer": 1800000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 38294], [38295, 42325], [42326]),
        "idleIncome": (1462, 1625, 1706),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    32: _tools.RODict({
        "ID": 32,
        "grade": 32,
        "expPlayer": 1900000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 40212], [40213, 44445], [44446]),
        "idleIncome": (1530, 1700, 1785),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    33: _tools.RODict({
        "ID": 33,
        "grade": 33,
        "expPlayer": 2000000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 42130], [42131, 46565], [46566]),
        "idleIncome": (1597, 1775, 1863),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    34: _tools.RODict({
        "ID": 34,
        "grade": 34,
        "expPlayer": 3000000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 44047], [44048, 48684], [48685]),
        "idleIncome": (1687, 1875, 1968),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    35: _tools.RODict({
        "ID": 35,
        "grade": 35,
        "expPlayer": 3500000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 45965], [45966, 50804], [50805]),
        "idleIncome": (1777, 1975, 2073),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    36: _tools.RODict({
        "ID": 36,
        "grade": 36,
        "expPlayer": 4000000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 47883], [47884, 52924], [52925]),
        "idleIncome": (1867, 2075, 2178),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    37: _tools.RODict({
        "ID": 37,
        "grade": 37,
        "expPlayer": 4250000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 49801], [49802, 55044], [55045]),
        "idleIncome": (1957, 2175, 2283),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    38: _tools.RODict({
        "ID": 38,
        "grade": 38,
        "expPlayer": 4500000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 51719], [51720, 57164], [57165]),
        "idleIncome": (2047, 2275, 2388),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    39: _tools.RODict({
        "ID": 39,
        "grade": 39,
        "expPlayer": 4750000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 53637], [53638, 59284], [59285]),
        "idleIncome": (2160, 2400, 2520),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    40: _tools.RODict({
        "ID": 40,
        "grade": 40,
        "expPlayer": 8090000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 55556], [55557, 61404], [61405]),
        "idleIncome": (2272, 2525, 2651),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    41: _tools.RODict({
        "ID": 41,
        "grade": 41,
        "expPlayer": 8530000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 56885], [56886, 62872], [62873]),
        "idleIncome": (2385, 2650, 2782),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    42: _tools.RODict({
        "ID": 42,
        "grade": 42,
        "expPlayer": 8940000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 58214], [58215, 64341], [64342]),
        "idleIncome": (2497, 2775, 2913),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    43: _tools.RODict({
        "ID": 43,
        "grade": 43,
        "expPlayer": 9450000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 59543], [59544, 65810], [65811]),
        "idleIncome": (2610, 2900, 3045),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    44: _tools.RODict({
        "ID": 44,
        "grade": 44,
        "expPlayer": 9950000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 60872], [60873, 67279], [67280]),
        "idleIncome": (2745, 3050, 3202),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    45: _tools.RODict({
        "ID": 45,
        "grade": 45,
        "expPlayer": 10780000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 62201], [62202, 68748], [68749]),
        "idleIncome": (2880, 3200, 3360),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    46: _tools.RODict({
        "ID": 46,
        "grade": 46,
        "expPlayer": 17050000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 63530], [63531, 70217], [70218]),
        "idleIncome": (3037, 3375, 3543),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    47: _tools.RODict({
        "ID": 47,
        "grade": 47,
        "expPlayer": 17990000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 64860], [64861, 71687], [71688]),
        "idleIncome": (3195, 3550, 3727),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    48: _tools.RODict({
        "ID": 48,
        "grade": 48,
        "expPlayer": 18900000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 66189], [66190, 73156], [73157]),
        "idleIncome": (3352, 3725, 3911),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    49: _tools.RODict({
        "ID": 49,
        "grade": 49,
        "expPlayer": 19970000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 67518], [67519, 74625], [74626]),
        "idleIncome": (3510, 3900, 4095),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    50: _tools.RODict({
        "ID": 50,
        "grade": 50,
        "expPlayer": 40990000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 68847], [68848, 76094], [76095]),
        "idleIncome": (3690, 4100, 4305),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    51: _tools.RODict({
        "ID": 51,
        "grade": 51,
        "expPlayer": 43380000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 70585], [70586, 78015], [78016]),
        "idleIncome": (3870, 4300, 4515),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    52: _tools.RODict({
        "ID": 52,
        "grade": 52,
        "expPlayer": 45670000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 72322], [72323, 79935], [79936]),
        "idleIncome": (4072, 4525, 4751),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    53: _tools.RODict({
        "ID": 53,
        "grade": 53,
        "expPlayer": 48090000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 74060], [74061, 81855], [81856]),
        "idleIncome": (4275, 4750, 4987),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    54: _tools.RODict({
        "ID": 54,
        "grade": 54,
        "expPlayer": 53670000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 75797], [75798, 83776], [83777]),
        "idleIncome": (4477, 4975, 5223),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    55: _tools.RODict({
        "ID": 55,
        "grade": 55,
        "expPlayer": 56780000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 77535], [77536, 85696], [85697]),
        "idleIncome": (4702, 5225, 5486),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    56: _tools.RODict({
        "ID": 56,
        "grade": 56,
        "expPlayer": 59780000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 79272], [79273, 87617], [87618]),
        "idleIncome": (4950, 5500, 5775),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    57: _tools.RODict({
        "ID": 57,
        "grade": 57,
        "expPlayer": 62940000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 81010], [81011, 89537], [89538]),
        "idleIncome": (5197, 5775, 6063),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    58: _tools.RODict({
        "ID": 58,
        "grade": 58,
        "expPlayer": 66240000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 82747], [82748, 91458], [91459]),
        "idleIncome": (5445, 6050, 6352),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    59: _tools.RODict({
        "ID": 59,
        "grade": 59,
        "expPlayer": 150030000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 84485], [84486, 93378], [93379]),
        "idleIncome": (5715, 6350, 6667),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    60: _tools.RODict({
        "ID": 60,
        "grade": 60,
        "expPlayer": 157340000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 86222], [86223, 95299], [95300]),
        "idleIncome": (6007, 6675, 7008),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    61: _tools.RODict({
        "ID": 61,
        "grade": 61,
        "expPlayer": 165560000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 87697], [87698, 96928], [96929]),
        "idleIncome": (6300, 7000, 7350),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    62: _tools.RODict({
        "ID": 62,
        "grade": 62,
        "expPlayer": 174010000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 89172], [89173, 98559], [98560]),
        "idleIncome": (6615, 7350, 7717),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    63: _tools.RODict({
        "ID": 63,
        "grade": 63,
        "expPlayer": 182860000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 90647], [90648, 100188], [100189]),
        "idleIncome": (6952, 7725, 8111),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    64: _tools.RODict({
        "ID": 64,
        "grade": 64,
        "expPlayer": 192450000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 92121], [92122, 101818], [101819]),
        "idleIncome": (7290, 8100, 8505),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    65: _tools.RODict({
        "ID": 65,
        "grade": 65,
        "expPlayer": 207780000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 93596], [93597, 103449], [103450]),
        "idleIncome": (7672, 8525, 8951),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    66: _tools.RODict({
        "ID": 66,
        "grade": 66,
        "expPlayer": 217650000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 95071], [95072, 105078], [105079]),
        "idleIncome": (8055, 8950, 9397),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    67: _tools.RODict({
        "ID": 67,
        "grade": 67,
        "expPlayer": 229160000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 96545], [96546, 106708], [106709]),
        "idleIncome": (8437, 9375, 9843),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    68: _tools.RODict({
        "ID": 68,
        "grade": 68,
        "expPlayer": 240790000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 98021], [98022, 108339], [108340]),
        "idleIncome": (8865, 9850, 10342),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    69: _tools.RODict({
        "ID": 69,
        "grade": 69,
        "expPlayer": 253540000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 99495], [99496, 109968], [109969]),
        "idleIncome": (9315, 10350, 10867),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    70: _tools.RODict({
        "ID": 70,
        "grade": 70,
        "expPlayer": 279770000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 100970], [100971, 111599], [111600]),
        "idleIncome": (9787, 10875, 11418),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    71: _tools.RODict({
        "ID": 71,
        "grade": 71,
        "expPlayer": 294500000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 102684], [102685, 113493], [113494]),
        "idleIncome": (10260, 11400, 11970),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    72: _tools.RODict({
        "ID": 72,
        "grade": 72,
        "expPlayer": 309260000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 104399], [104400, 115388], [115389]),
        "idleIncome": (10777, 11975, 12573),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    73: _tools.RODict({
        "ID": 73,
        "grade": 73,
        "expPlayer": 325320000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 106114], [106115, 117283], [117284]),
        "idleIncome": (11317, 12575, 13203),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    74: _tools.RODict({
        "ID": 74,
        "grade": 74,
        "expPlayer": 341950000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 107828], [107829, 119179], [119180]),
        "idleIncome": (11880, 13200, 13860),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    75: _tools.RODict({
        "ID": 75,
        "grade": 75,
        "expPlayer": 455170000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 109542], [109543, 121073], [121074]),
        "idleIncome": (12487, 13875, 14568),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    76: _tools.RODict({
        "ID": 76,
        "grade": 76,
        "expPlayer": 478630000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 111257], [111258, 122968], [122969]),
        "idleIncome": (13095, 14550, 15277),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    77: _tools.RODict({
        "ID": 77,
        "grade": 77,
        "expPlayer": 503140000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 112972], [112973, 124863], [124864]),
        "idleIncome": (13770, 15300, 16065),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    78: _tools.RODict({
        "ID": 78,
        "grade": 78,
        "expPlayer": 528220000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 114686], [114687, 126759], [126760]),
        "idleIncome": (14445, 16050, 16852),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    79: _tools.RODict({
        "ID": 79,
        "grade": 79,
        "expPlayer": 556030000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 116400], [116401, 128653], [128654]),
        "idleIncome": (15165, 16850, 17692),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    80: _tools.RODict({
        "ID": 80,
        "grade": 80,
        "expPlayer": 593290000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 118115], [118116, 130548], [130549]),
        "idleIncome": (15930, 17700, 18585),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    81: _tools.RODict({
        "ID": 81,
        "grade": 81,
        "expPlayer": 624910000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 121046], [121047, 133787], [133788]),
        "idleIncome": (16717, 18575, 19503),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    82: _tools.RODict({
        "ID": 82,
        "grade": 82,
        "expPlayer": 656120000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 123975], [123976, 137026], [137027]),
        "idleIncome": (17572, 19525, 20501),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    83: _tools.RODict({
        "ID": 83,
        "grade": 83,
        "expPlayer": 690340000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 126906], [126907, 140265], [140266]),
        "idleIncome": (18450, 20500, 21525),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    84: _tools.RODict({
        "ID": 84,
        "grade": 84,
        "expPlayer": 906020000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 129837], [129838, 143504], [143505]),
        "idleIncome": (19372, 21525, 22601),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    85: _tools.RODict({
        "ID": 85,
        "grade": 85,
        "expPlayer": 953070000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 132768], [132769, 146743], [146744]),
        "idleIncome": (20340, 22600, 23730),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    86: _tools.RODict({
        "ID": 86,
        "grade": 86,
        "expPlayer": 1000270000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 135698], [135699, 149982], [149983]),
        "idleIncome": (21352, 23725, 24911),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    87: _tools.RODict({
        "ID": 87,
        "grade": 87,
        "expPlayer": 1052630000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 138628], [138629, 153221], [153222]),
        "idleIncome": (22410, 24900, 26145),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    88: _tools.RODict({
        "ID": 88,
        "grade": 88,
        "expPlayer": 1104960000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 141559], [141560, 156460], [156461]),
        "idleIncome": (23535, 26150, 27457),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    89: _tools.RODict({
        "ID": 89,
        "grade": 89,
        "expPlayer": 1162680000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 144489], [144490, 159698], [159699]),
        "idleIncome": (24705, 27450, 28822),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    90: _tools.RODict({
        "ID": 90,
        "grade": 90,
        "expPlayer": 1221160000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    91: _tools.RODict({
        "ID": 91,
        "grade": 91,
        "expPlayer": 1282680000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    92: _tools.RODict({
        "ID": 92,
        "grade": 92,
        "expPlayer": 1346200000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    93: _tools.RODict({
        "ID": 93,
        "grade": 93,
        "expPlayer": 1413770000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    94: _tools.RODict({
        "ID": 94,
        "grade": 94,
        "expPlayer": 1484350000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    95: _tools.RODict({
        "ID": 95,
        "grade": 95,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    96: _tools.RODict({
        "ID": 96,
        "grade": 96,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    97: _tools.RODict({
        "ID": 97,
        "grade": 97,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    98: _tools.RODict({
        "ID": 98,
        "grade": 98,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    99: _tools.RODict({
        "ID": 99,
        "grade": 99,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    100: _tools.RODict({
        "ID": 100,
        "grade": 100,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    101: _tools.RODict({
        "ID": 101,
        "grade": 101,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    102: _tools.RODict({
        "ID": 102,
        "grade": 102,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    103: _tools.RODict({
        "ID": 103,
        "grade": 103,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    104: _tools.RODict({
        "ID": 104,
        "grade": 104,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    105: _tools.RODict({
        "ID": 105,
        "grade": 105,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    106: _tools.RODict({
        "ID": 106,
        "grade": 106,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    107: _tools.RODict({
        "ID": 107,
        "grade": 107,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    108: _tools.RODict({
        "ID": 108,
        "grade": 108,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    109: _tools.RODict({
        "ID": 109,
        "grade": 109,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    110: _tools.RODict({
        "ID": 110,
        "grade": 110,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    111: _tools.RODict({
        "ID": 111,
        "grade": 111,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    112: _tools.RODict({
        "ID": 112,
        "grade": 112,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    113: _tools.RODict({
        "ID": 113,
        "grade": 113,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    114: _tools.RODict({
        "ID": 114,
        "grade": 114,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    115: _tools.RODict({
        "ID": 115,
        "grade": 115,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    116: _tools.RODict({
        "ID": 116,
        "grade": 116,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    117: _tools.RODict({
        "ID": 117,
        "grade": 117,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    118: _tools.RODict({
        "ID": 118,
        "grade": 118,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    119: _tools.RODict({
        "ID": 119,
        "grade": 119,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    120: _tools.RODict({
        "ID": 120,
        "grade": 120,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    121: _tools.RODict({
        "ID": 121,
        "grade": 121,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    122: _tools.RODict({
        "ID": 122,
        "grade": 122,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    123: _tools.RODict({
        "ID": 123,
        "grade": 123,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    124: _tools.RODict({
        "ID": 124,
        "grade": 124,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    125: _tools.RODict({
        "ID": 125,
        "grade": 125,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    126: _tools.RODict({
        "ID": 126,
        "grade": 126,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    127: _tools.RODict({
        "ID": 127,
        "grade": 127,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    128: _tools.RODict({
        "ID": 128,
        "grade": 128,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    129: _tools.RODict({
        "ID": 129,
        "grade": 129,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    130: _tools.RODict({
        "ID": 130,
        "grade": 130,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    131: _tools.RODict({
        "ID": 131,
        "grade": 131,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    132: _tools.RODict({
        "ID": 132,
        "grade": 132,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    133: _tools.RODict({
        "ID": 133,
        "grade": 133,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    134: _tools.RODict({
        "ID": 134,
        "grade": 134,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    135: _tools.RODict({
        "ID": 135,
        "grade": 135,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    136: _tools.RODict({
        "ID": 136,
        "grade": 136,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    137: _tools.RODict({
        "ID": 137,
        "grade": 137,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    138: _tools.RODict({
        "ID": 138,
        "grade": 138,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    139: _tools.RODict({
        "ID": 139,
        "grade": 139,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    140: _tools.RODict({
        "ID": 140,
        "grade": 140,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    141: _tools.RODict({
        "ID": 141,
        "grade": 141,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    142: _tools.RODict({
        "ID": 142,
        "grade": 142,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    143: _tools.RODict({
        "ID": 143,
        "grade": 143,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    144: _tools.RODict({
        "ID": 144,
        "grade": 144,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    145: _tools.RODict({
        "ID": 145,
        "grade": 145,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    146: _tools.RODict({
        "ID": 146,
        "grade": 146,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    147: _tools.RODict({
        "ID": 147,
        "grade": 147,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    148: _tools.RODict({
        "ID": 148,
        "grade": 148,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    149: _tools.RODict({
        "ID": 149,
        "grade": 149,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    150: _tools.RODict({
        "ID": 150,
        "grade": 150,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    151: _tools.RODict({
        "ID": 151,
        "grade": 151,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    152: _tools.RODict({
        "ID": 152,
        "grade": 152,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    153: _tools.RODict({
        "ID": 153,
        "grade": 153,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    154: _tools.RODict({
        "ID": 154,
        "grade": 154,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    155: _tools.RODict({
        "ID": 155,
        "grade": 155,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    156: _tools.RODict({
        "ID": 156,
        "grade": 156,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    157: _tools.RODict({
        "ID": 157,
        "grade": 157,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    158: _tools.RODict({
        "ID": 158,
        "grade": 158,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    159: _tools.RODict({
        "ID": 159,
        "grade": 159,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    160: _tools.RODict({
        "ID": 160,
        "grade": 160,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    161: _tools.RODict({
        "ID": 161,
        "grade": 161,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    162: _tools.RODict({
        "ID": 162,
        "grade": 162,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    163: _tools.RODict({
        "ID": 163,
        "grade": 163,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    164: _tools.RODict({
        "ID": 164,
        "grade": 164,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    165: _tools.RODict({
        "ID": 165,
        "grade": 165,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    166: _tools.RODict({
        "ID": 166,
        "grade": 166,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    167: _tools.RODict({
        "ID": 167,
        "grade": 167,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    168: _tools.RODict({
        "ID": 168,
        "grade": 168,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    169: _tools.RODict({
        "ID": 169,
        "grade": 169,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    170: _tools.RODict({
        "ID": 170,
        "grade": 170,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    171: _tools.RODict({
        "ID": 171,
        "grade": 171,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    172: _tools.RODict({
        "ID": 172,
        "grade": 172,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    173: _tools.RODict({
        "ID": 173,
        "grade": 173,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    174: _tools.RODict({
        "ID": 174,
        "grade": 174,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    175: _tools.RODict({
        "ID": 175,
        "grade": 175,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    176: _tools.RODict({
        "ID": 176,
        "grade": 176,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    177: _tools.RODict({
        "ID": 177,
        "grade": 177,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    178: _tools.RODict({
        "ID": 178,
        "grade": 178,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    179: _tools.RODict({
        "ID": 179,
        "grade": 179,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    180: _tools.RODict({
        "ID": 180,
        "grade": 180,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    181: _tools.RODict({
        "ID": 181,
        "grade": 181,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    182: _tools.RODict({
        "ID": 182,
        "grade": 182,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    183: _tools.RODict({
        "ID": 183,
        "grade": 183,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    184: _tools.RODict({
        "ID": 184,
        "grade": 184,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    185: _tools.RODict({
        "ID": 185,
        "grade": 185,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    186: _tools.RODict({
        "ID": 186,
        "grade": 186,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    187: _tools.RODict({
        "ID": 187,
        "grade": 187,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    188: _tools.RODict({
        "ID": 188,
        "grade": 188,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    189: _tools.RODict({
        "ID": 189,
        "grade": 189,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    190: _tools.RODict({
        "ID": 190,
        "grade": 190,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    191: _tools.RODict({
        "ID": 191,
        "grade": 191,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    192: _tools.RODict({
        "ID": 192,
        "grade": 192,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    193: _tools.RODict({
        "ID": 193,
        "grade": 193,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    194: _tools.RODict({
        "ID": 194,
        "grade": 194,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    195: _tools.RODict({
        "ID": 195,
        "grade": 195,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    196: _tools.RODict({
        "ID": 196,
        "grade": 196,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    197: _tools.RODict({
        "ID": 197,
        "grade": 197,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    198: _tools.RODict({
        "ID": 198,
        "grade": 198,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    199: _tools.RODict({
        "ID": 199,
        "grade": 199,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    }),
    200: _tools.RODict({
        "ID": 200,
        "grade": 200,
        "expPlayer": 1558980000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (25942, 28825, 30266),
        "itemIncome": (50030101, 50030102, 50030103)
    })
})
minKey = 1
maxKey = 200