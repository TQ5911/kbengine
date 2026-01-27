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
        "idleIncome": (156, 165, 173)
    }),
    2: _tools.RODict({
        "ID": 2,
        "grade": 2,
        "expPlayer": 150,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3161], [3162, 3494], [3495]),
        "idleIncome": (156, 165, 173)
    }),
    3: _tools.RODict({
        "ID": 3,
        "grade": 3,
        "expPlayer": 250,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3693], [3694, 4082], [4083]),
        "idleIncome": (156, 165, 173)
    }),
    4: _tools.RODict({
        "ID": 4,
        "grade": 4,
        "expPlayer": 500,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3976], [3977, 4395], [4396]),
        "idleIncome": (156, 165, 173)
    }),
    5: _tools.RODict({
        "ID": 5,
        "grade": 5,
        "expPlayer": 650,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 4508], [4509, 4983], [4984]),
        "idleIncome": (156, 165, 173)
    }),
    6: _tools.RODict({
        "ID": 6,
        "grade": 6,
        "expPlayer": 2000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 8116], [8117, 8971], [8972]),
        "idleIncome": (156, 165, 173)
    }),
    7: _tools.RODict({
        "ID": 7,
        "grade": 7,
        "expPlayer": 4000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 8529], [8530, 9426], [9427]),
        "idleIncome": (156, 165, 173)
    }),
    8: _tools.RODict({
        "ID": 8,
        "grade": 8,
        "expPlayer": 7000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 9158], [9159, 10122], [10123]),
        "idleIncome": (156, 165, 173)
    }),
    9: _tools.RODict({
        "ID": 9,
        "grade": 9,
        "expPlayer": 11000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 9676], [9677, 10695], [10696]),
        "idleIncome": (156, 165, 173)
    }),
    10: _tools.RODict({
        "ID": 10,
        "grade": 10,
        "expPlayer": 15000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 11216], [11217, 12397], [12398]),
        "idleIncome": (156, 165, 173)
    }),
    11: _tools.RODict({
        "ID": 11,
        "grade": 11,
        "expPlayer": 16000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 12136], [12137, 13413], [13414]),
        "idleIncome": (156, 165, 173)
    }),
    12: _tools.RODict({
        "ID": 12,
        "grade": 12,
        "expPlayer": 18000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 12481], [12482, 13794], [13795]),
        "idleIncome": (156, 165, 173)
    }),
    13: _tools.RODict({
        "ID": 13,
        "grade": 13,
        "expPlayer": 20000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 13013], [13014, 14382], [14383]),
        "idleIncome": (156, 165, 173)
    }),
    14: _tools.RODict({
        "ID": 14,
        "grade": 14,
        "expPlayer": 22000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 13357], [13358, 14763], [14764]),
        "idleIncome": (156, 165, 173)
    }),
    15: _tools.RODict({
        "ID": 15,
        "grade": 15,
        "expPlayer": 24000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 14240], [14241, 15739], [15740]),
        "idleIncome": (156, 165, 173)
    }),
    16: _tools.RODict({
        "ID": 16,
        "grade": 16,
        "expPlayer": 26000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 15514], [15515, 17147], [17148]),
        "idleIncome": (156, 165, 173)
    }),
    17: _tools.RODict({
        "ID": 17,
        "grade": 17,
        "expPlayer": 28000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 16074], [16075, 17767], [17768]),
        "idleIncome": (156, 165, 173)
    }),
    18: _tools.RODict({
        "ID": 18,
        "grade": 18,
        "expPlayer": 30000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 16435], [16436, 18166], [18167]),
        "idleIncome": (156, 165, 173)
    }),
    19: _tools.RODict({
        "ID": 19,
        "grade": 19,
        "expPlayer": 36000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 16954], [16955, 18739], [18740]),
        "idleIncome": (156, 165, 173)
    }),
    20: _tools.RODict({
        "ID": 20,
        "grade": 20,
        "expPlayer": 48000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 19965], [19966, 22066], [22067]),
        "idleIncome": (156, 165, 173)
    }),
    21: _tools.RODict({
        "ID": 21,
        "grade": 21,
        "expPlayer": 64000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 20881], [20882, 23080], [23081]),
        "idleIncome": (167, 176, 184)
    }),
    22: _tools.RODict({
        "ID": 22,
        "grade": 22,
        "expPlayer": 80000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 21527], [21528, 23794], [23795]),
        "idleIncome": (179, 189, 198)
    }),
    23: _tools.RODict({
        "ID": 23,
        "grade": 23,
        "expPlayer": 96000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 22082], [22083, 24407], [24408]),
        "idleIncome": (191, 202, 212)
    }),
    24: _tools.RODict({
        "ID": 24,
        "grade": 24,
        "expPlayer": 112000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 23099], [23100, 25530], [25531]),
        "idleIncome": (205, 216, 226)
    }),
    25: _tools.RODict({
        "ID": 25,
        "grade": 25,
        "expPlayer": 148000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 26443], [26444, 29226], [29227]),
        "idleIncome": (219, 231, 242)
    }),
    26: _tools.RODict({
        "ID": 26,
        "grade": 26,
        "expPlayer": 184000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 27779], [27780, 30704], [30705]),
        "idleIncome": (235, 248, 260)
    }),
    27: _tools.RODict({
        "ID": 27,
        "grade": 27,
        "expPlayer": 220000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 28670], [28671, 31687], [31688]),
        "idleIncome": (251, 265, 278)
    }),
    28: _tools.RODict({
        "ID": 28,
        "grade": 28,
        "expPlayer": 280000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 29634], [29635, 32753], [32754]),
        "idleIncome": (268, 283, 297)
    }),
    29: _tools.RODict({
        "ID": 29,
        "grade": 29,
        "expPlayer": 340000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 30153], [30154, 33327], [33328]),
        "idleIncome": (287, 303, 318)
    }),
    30: _tools.RODict({
        "ID": 30,
        "grade": 30,
        "expPlayer": 460000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 36376], [36377, 40205], [40206]),
        "idleIncome": (308, 325, 341)
    }),
    31: _tools.RODict({
        "ID": 31,
        "grade": 31,
        "expPlayer": 580000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 38294], [38295, 42325], [42326]),
        "idleIncome": (329, 347, 364)
    }),
    32: _tools.RODict({
        "ID": 32,
        "grade": 32,
        "expPlayer": 700000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 40212], [40213, 44445], [44446]),
        "idleIncome": (353, 372, 390)
    }),
    33: _tools.RODict({
        "ID": 33,
        "grade": 33,
        "expPlayer": 900000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 42130], [42131, 46565], [46566]),
        "idleIncome": (378, 398, 417)
    }),
    34: _tools.RODict({
        "ID": 34,
        "grade": 34,
        "expPlayer": 1100000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 44047], [44048, 48684], [48685]),
        "idleIncome": (404, 426, 447)
    }),
    35: _tools.RODict({
        "ID": 35,
        "grade": 35,
        "expPlayer": 1500000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 45965], [45966, 50804], [50805]),
        "idleIncome": (433, 456, 478)
    }),
    36: _tools.RODict({
        "ID": 36,
        "grade": 36,
        "expPlayer": 1900000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 47883], [47884, 52924], [52925]),
        "idleIncome": (462, 487, 511)
    }),
    37: _tools.RODict({
        "ID": 37,
        "grade": 37,
        "expPlayer": 2300000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 49801], [49802, 55044], [55045]),
        "idleIncome": (495, 522, 548)
    }),
    38: _tools.RODict({
        "ID": 38,
        "grade": 38,
        "expPlayer": 2800000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 51719], [51720, 57164], [57165]),
        "idleIncome": (530, 558, 585)
    }),
    39: _tools.RODict({
        "ID": 39,
        "grade": 39,
        "expPlayer": 3500000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 53637], [53638, 59284], [59285]),
        "idleIncome": (567, 597, 626)
    }),
    40: _tools.RODict({
        "ID": 40,
        "grade": 40,
        "expPlayer": 4400000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 55556], [55557, 61404], [61405]),
        "idleIncome": (607, 639, 670)
    }),
    41: _tools.RODict({
        "ID": 41,
        "grade": 41,
        "expPlayer": 5500000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 56885], [56886, 62872], [62873]),
        "idleIncome": (649, 684, 718)
    }),
    42: _tools.RODict({
        "ID": 42,
        "grade": 42,
        "expPlayer": 6800000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 58214], [58215, 64341], [64342]),
        "idleIncome": (695, 732, 768)
    }),
    43: _tools.RODict({
        "ID": 43,
        "grade": 43,
        "expPlayer": 8100000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 59543], [59544, 65810], [65811]),
        "idleIncome": (743, 783, 822)
    }),
    44: _tools.RODict({
        "ID": 44,
        "grade": 44,
        "expPlayer": 9500000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 60872], [60873, 67279], [67280]),
        "idleIncome": (796, 838, 879)
    }),
    45: _tools.RODict({
        "ID": 45,
        "grade": 45,
        "expPlayer": 12000000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 62201], [62202, 68748], [68749]),
        "idleIncome": (852, 897, 941)
    }),
    46: _tools.RODict({
        "ID": 46,
        "grade": 46,
        "expPlayer": 14000000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 63530], [63531, 70217], [70218]),
        "idleIncome": (911, 959, 1006)
    }),
    47: _tools.RODict({
        "ID": 47,
        "grade": 47,
        "expPlayer": 17000000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 64860], [64861, 71687], [71688]),
        "idleIncome": (975, 1027, 1078)
    }),
    48: _tools.RODict({
        "ID": 48,
        "grade": 48,
        "expPlayer": 20000000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 66189], [66190, 73156], [73157]),
        "idleIncome": (1043, 1098, 1152)
    }),
    49: _tools.RODict({
        "ID": 49,
        "grade": 49,
        "expPlayer": 22000000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 67518], [67519, 74625], [74626]),
        "idleIncome": (1116, 1175, 1233)
    }),
    50: _tools.RODict({
        "ID": 50,
        "grade": 50,
        "expPlayer": 24200000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 68847], [68848, 76094], [76095]),
        "idleIncome": (1195, 1258, 1320)
    }),
    51: _tools.RODict({
        "ID": 51,
        "grade": 51,
        "expPlayer": 26600000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 70585], [70586, 78015], [78016]),
        "idleIncome": (1278, 1346, 1413)
    }),
    52: _tools.RODict({
        "ID": 52,
        "grade": 52,
        "expPlayer": 29300000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 72322], [72323, 79935], [79936]),
        "idleIncome": (1368, 1440, 1512)
    }),
    53: _tools.RODict({
        "ID": 53,
        "grade": 53,
        "expPlayer": 32200000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 74060], [74061, 81855], [81856]),
        "idleIncome": (1463, 1541, 1618)
    }),
    54: _tools.RODict({
        "ID": 54,
        "grade": 54,
        "expPlayer": 35400000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 75797], [75798, 83776], [83777]),
        "idleIncome": (1566, 1649, 1731)
    }),
    55: _tools.RODict({
        "ID": 55,
        "grade": 55,
        "expPlayer": 38900000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 77535], [77536, 85696], [85697]),
        "idleIncome": (1675, 1764, 1852)
    }),
    56: _tools.RODict({
        "ID": 56,
        "grade": 56,
        "expPlayer": 42800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 79272], [79273, 87617], [87618]),
        "idleIncome": (1793, 1888, 1982)
    }),
    57: _tools.RODict({
        "ID": 57,
        "grade": 57,
        "expPlayer": 47100000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 81010], [81011, 89537], [89538]),
        "idleIncome": (1919, 2020, 2121)
    }),
    58: _tools.RODict({
        "ID": 58,
        "grade": 58,
        "expPlayer": 51800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 82747], [82748, 91458], [91459]),
        "idleIncome": (2052, 2161, 2269)
    }),
    59: _tools.RODict({
        "ID": 59,
        "grade": 59,
        "expPlayer": 54900000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 84485], [84486, 93378], [93379]),
        "idleIncome": (2197, 2313, 2428)
    }),
    60: _tools.RODict({
        "ID": 60,
        "grade": 60,
        "expPlayer": 58700000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 86222], [86223, 95299], [95300]),
        "idleIncome": (2351, 2475, 2598)
    }),
    61: _tools.RODict({
        "ID": 61,
        "grade": 61,
        "expPlayer": 62800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 87697], [87698, 96928], [96929]),
        "idleIncome": (2515, 2648, 2780)
    }),
    62: _tools.RODict({
        "ID": 62,
        "grade": 62,
        "expPlayer": 67200000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 89172], [89173, 98559], [98560]),
        "idleIncome": (2691, 2833, 2974)
    }),
    63: _tools.RODict({
        "ID": 63,
        "grade": 63,
        "expPlayer": 71900000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 90647], [90648, 100188], [100189]),
        "idleIncome": (2880, 3032, 3183)
    }),
    64: _tools.RODict({
        "ID": 64,
        "grade": 64,
        "expPlayer": 76900000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 92121], [92122, 101818], [101819]),
        "idleIncome": (3081, 3244, 3406)
    }),
    65: _tools.RODict({
        "ID": 65,
        "grade": 65,
        "expPlayer": 82300000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 93596], [93597, 103449], [103450]),
        "idleIncome": (3297, 3471, 3644)
    }),
    66: _tools.RODict({
        "ID": 66,
        "grade": 66,
        "expPlayer": 88100000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 95071], [95072, 105078], [105079]),
        "idleIncome": (3528, 3714, 3899)
    }),
    67: _tools.RODict({
        "ID": 67,
        "grade": 67,
        "expPlayer": 94300000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 96545], [96546, 106708], [106709]),
        "idleIncome": (3775, 3974, 4172)
    }),
    68: _tools.RODict({
        "ID": 68,
        "grade": 68,
        "expPlayer": 100900000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 98021], [98022, 108339], [108340]),
        "idleIncome": (4039, 4252, 4464)
    }),
    69: _tools.RODict({
        "ID": 69,
        "grade": 69,
        "expPlayer": 108000000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 99495], [99496, 109968], [109969]),
        "idleIncome": (4322, 4550, 4777)
    }),
    70: _tools.RODict({
        "ID": 70,
        "grade": 70,
        "expPlayer": 115600000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 100970], [100971, 111599], [111600]),
        "idleIncome": (4624, 4868, 5111)
    }),
    71: _tools.RODict({
        "ID": 71,
        "grade": 71,
        "expPlayer": 123700000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 102684], [102685, 113493], [113494]),
        "idleIncome": (4948, 5209, 5469)
    }),
    72: _tools.RODict({
        "ID": 72,
        "grade": 72,
        "expPlayer": 132400000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 104399], [104400, 115388], [115389]),
        "idleIncome": (5295, 5574, 5852)
    }),
    73: _tools.RODict({
        "ID": 73,
        "grade": 73,
        "expPlayer": 141700000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 106114], [106115, 117283], [117284]),
        "idleIncome": (5665, 5964, 6262)
    }),
    74: _tools.RODict({
        "ID": 74,
        "grade": 74,
        "expPlayer": 151600000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 107828], [107829, 119179], [119180]),
        "idleIncome": (6062, 6382, 6701)
    }),
    75: _tools.RODict({
        "ID": 75,
        "grade": 75,
        "expPlayer": 162200000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 109542], [109543, 121073], [121074]),
        "idleIncome": (6486, 6828, 7169)
    }),
    76: _tools.RODict({
        "ID": 76,
        "grade": 76,
        "expPlayer": 173600000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 111257], [111258, 122968], [122969]),
        "idleIncome": (6941, 7307, 7672)
    }),
    77: _tools.RODict({
        "ID": 77,
        "grade": 77,
        "expPlayer": 185800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 112972], [112973, 124863], [124864]),
        "idleIncome": (7427, 7818, 8208)
    }),
    78: _tools.RODict({
        "ID": 78,
        "grade": 78,
        "expPlayer": 198800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 114686], [114687, 126759], [126760]),
        "idleIncome": (7946, 8365, 8783)
    }),
    79: _tools.RODict({
        "ID": 79,
        "grade": 79,
        "expPlayer": 212700000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 116400], [116401, 128653], [128654]),
        "idleIncome": (8503, 8951, 9398)
    }),
    80: _tools.RODict({
        "ID": 80,
        "grade": 80,
        "expPlayer": 227600000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 118115], [118116, 130548], [130549]),
        "idleIncome": (9098, 9577, 10055)
    }),
    81: _tools.RODict({
        "ID": 81,
        "grade": 81,
        "expPlayer": 243500000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 121046], [121047, 133787], [133788]),
        "idleIncome": (9735, 10248, 10760)
    }),
    82: _tools.RODict({
        "ID": 82,
        "grade": 82,
        "expPlayer": 260500000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 123975], [123976, 137026], [137027]),
        "idleIncome": (10416, 10965, 11513)
    }),
    83: _tools.RODict({
        "ID": 83,
        "grade": 83,
        "expPlayer": 278700000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 126906], [126907, 140265], [140266]),
        "idleIncome": (11146, 11733, 12319)
    }),
    84: _tools.RODict({
        "ID": 84,
        "grade": 84,
        "expPlayer": 298200000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 129837], [129838, 143504], [143505]),
        "idleIncome": (11926, 12554, 13181)
    }),
    85: _tools.RODict({
        "ID": 85,
        "grade": 85,
        "expPlayer": 319100000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 132768], [132769, 146743], [146744]),
        "idleIncome": (12761, 13433, 14104)
    }),
    86: _tools.RODict({
        "ID": 86,
        "grade": 86,
        "expPlayer": 341400000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 135698], [135699, 149982], [149983]),
        "idleIncome": (13654, 14373, 15091)
    }),
    87: _tools.RODict({
        "ID": 87,
        "grade": 87,
        "expPlayer": 365300000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 138628], [138629, 153221], [153222]),
        "idleIncome": (14611, 15380, 16149)
    }),
    88: _tools.RODict({
        "ID": 88,
        "grade": 88,
        "expPlayer": 390900000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 141559], [141560, 156460], [156461]),
        "idleIncome": (15633, 16456, 17278)
    }),
    89: _tools.RODict({
        "ID": 89,
        "grade": 89,
        "expPlayer": 418300000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 144489], [144490, 159698], [159699]),
        "idleIncome": (16727, 17608, 18488)
    }),
    90: _tools.RODict({
        "ID": 90,
        "grade": 90,
        "expPlayer": 447600000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    91: _tools.RODict({
        "ID": 91,
        "grade": 91,
        "expPlayer": 478900000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    92: _tools.RODict({
        "ID": 92,
        "grade": 92,
        "expPlayer": 512400000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    93: _tools.RODict({
        "ID": 93,
        "grade": 93,
        "expPlayer": 548300000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    94: _tools.RODict({
        "ID": 94,
        "grade": 94,
        "expPlayer": 586700000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    95: _tools.RODict({
        "ID": 95,
        "grade": 95,
        "expPlayer": 627800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    96: _tools.RODict({
        "ID": 96,
        "grade": 96,
        "expPlayer": 671700000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    97: _tools.RODict({
        "ID": 97,
        "grade": 97,
        "expPlayer": 718700000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    98: _tools.RODict({
        "ID": 98,
        "grade": 98,
        "expPlayer": 769000000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    99: _tools.RODict({
        "ID": 99,
        "grade": 99,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    100: _tools.RODict({
        "ID": 100,
        "grade": 100,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    101: _tools.RODict({
        "ID": 101,
        "grade": 101,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    102: _tools.RODict({
        "ID": 102,
        "grade": 102,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    103: _tools.RODict({
        "ID": 103,
        "grade": 103,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    104: _tools.RODict({
        "ID": 104,
        "grade": 104,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    105: _tools.RODict({
        "ID": 105,
        "grade": 105,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    106: _tools.RODict({
        "ID": 106,
        "grade": 106,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    107: _tools.RODict({
        "ID": 107,
        "grade": 107,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    108: _tools.RODict({
        "ID": 108,
        "grade": 108,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    109: _tools.RODict({
        "ID": 109,
        "grade": 109,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    110: _tools.RODict({
        "ID": 110,
        "grade": 110,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    111: _tools.RODict({
        "ID": 111,
        "grade": 111,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    112: _tools.RODict({
        "ID": 112,
        "grade": 112,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    113: _tools.RODict({
        "ID": 113,
        "grade": 113,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    114: _tools.RODict({
        "ID": 114,
        "grade": 114,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    115: _tools.RODict({
        "ID": 115,
        "grade": 115,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    116: _tools.RODict({
        "ID": 116,
        "grade": 116,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    117: _tools.RODict({
        "ID": 117,
        "grade": 117,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    118: _tools.RODict({
        "ID": 118,
        "grade": 118,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    119: _tools.RODict({
        "ID": 119,
        "grade": 119,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    120: _tools.RODict({
        "ID": 120,
        "grade": 120,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    121: _tools.RODict({
        "ID": 121,
        "grade": 121,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    122: _tools.RODict({
        "ID": 122,
        "grade": 122,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    123: _tools.RODict({
        "ID": 123,
        "grade": 123,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    124: _tools.RODict({
        "ID": 124,
        "grade": 124,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    125: _tools.RODict({
        "ID": 125,
        "grade": 125,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    126: _tools.RODict({
        "ID": 126,
        "grade": 126,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    127: _tools.RODict({
        "ID": 127,
        "grade": 127,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    128: _tools.RODict({
        "ID": 128,
        "grade": 128,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    129: _tools.RODict({
        "ID": 129,
        "grade": 129,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    130: _tools.RODict({
        "ID": 130,
        "grade": 130,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    131: _tools.RODict({
        "ID": 131,
        "grade": 131,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    132: _tools.RODict({
        "ID": 132,
        "grade": 132,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    133: _tools.RODict({
        "ID": 133,
        "grade": 133,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    134: _tools.RODict({
        "ID": 134,
        "grade": 134,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    135: _tools.RODict({
        "ID": 135,
        "grade": 135,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    136: _tools.RODict({
        "ID": 136,
        "grade": 136,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    137: _tools.RODict({
        "ID": 137,
        "grade": 137,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    138: _tools.RODict({
        "ID": 138,
        "grade": 138,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    139: _tools.RODict({
        "ID": 139,
        "grade": 139,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    140: _tools.RODict({
        "ID": 140,
        "grade": 140,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    141: _tools.RODict({
        "ID": 141,
        "grade": 141,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    142: _tools.RODict({
        "ID": 142,
        "grade": 142,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    143: _tools.RODict({
        "ID": 143,
        "grade": 143,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    144: _tools.RODict({
        "ID": 144,
        "grade": 144,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    145: _tools.RODict({
        "ID": 145,
        "grade": 145,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    146: _tools.RODict({
        "ID": 146,
        "grade": 146,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    147: _tools.RODict({
        "ID": 147,
        "grade": 147,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    148: _tools.RODict({
        "ID": 148,
        "grade": 148,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    149: _tools.RODict({
        "ID": 149,
        "grade": 149,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    150: _tools.RODict({
        "ID": 150,
        "grade": 150,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    151: _tools.RODict({
        "ID": 151,
        "grade": 151,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    152: _tools.RODict({
        "ID": 152,
        "grade": 152,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    153: _tools.RODict({
        "ID": 153,
        "grade": 153,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    154: _tools.RODict({
        "ID": 154,
        "grade": 154,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    155: _tools.RODict({
        "ID": 155,
        "grade": 155,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    156: _tools.RODict({
        "ID": 156,
        "grade": 156,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    157: _tools.RODict({
        "ID": 157,
        "grade": 157,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    158: _tools.RODict({
        "ID": 158,
        "grade": 158,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    159: _tools.RODict({
        "ID": 159,
        "grade": 159,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    160: _tools.RODict({
        "ID": 160,
        "grade": 160,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    161: _tools.RODict({
        "ID": 161,
        "grade": 161,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    162: _tools.RODict({
        "ID": 162,
        "grade": 162,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    163: _tools.RODict({
        "ID": 163,
        "grade": 163,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    164: _tools.RODict({
        "ID": 164,
        "grade": 164,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    165: _tools.RODict({
        "ID": 165,
        "grade": 165,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    166: _tools.RODict({
        "ID": 166,
        "grade": 166,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    167: _tools.RODict({
        "ID": 167,
        "grade": 167,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    168: _tools.RODict({
        "ID": 168,
        "grade": 168,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    169: _tools.RODict({
        "ID": 169,
        "grade": 169,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    170: _tools.RODict({
        "ID": 170,
        "grade": 170,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    171: _tools.RODict({
        "ID": 171,
        "grade": 171,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    172: _tools.RODict({
        "ID": 172,
        "grade": 172,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    173: _tools.RODict({
        "ID": 173,
        "grade": 173,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    174: _tools.RODict({
        "ID": 174,
        "grade": 174,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    175: _tools.RODict({
        "ID": 175,
        "grade": 175,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    176: _tools.RODict({
        "ID": 176,
        "grade": 176,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    177: _tools.RODict({
        "ID": 177,
        "grade": 177,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    178: _tools.RODict({
        "ID": 178,
        "grade": 178,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    179: _tools.RODict({
        "ID": 179,
        "grade": 179,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    180: _tools.RODict({
        "ID": 180,
        "grade": 180,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    181: _tools.RODict({
        "ID": 181,
        "grade": 181,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    182: _tools.RODict({
        "ID": 182,
        "grade": 182,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    183: _tools.RODict({
        "ID": 183,
        "grade": 183,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    184: _tools.RODict({
        "ID": 184,
        "grade": 184,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    185: _tools.RODict({
        "ID": 185,
        "grade": 185,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    186: _tools.RODict({
        "ID": 186,
        "grade": 186,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    187: _tools.RODict({
        "ID": 187,
        "grade": 187,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    188: _tools.RODict({
        "ID": 188,
        "grade": 188,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    189: _tools.RODict({
        "ID": 189,
        "grade": 189,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    190: _tools.RODict({
        "ID": 190,
        "grade": 190,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    191: _tools.RODict({
        "ID": 191,
        "grade": 191,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    192: _tools.RODict({
        "ID": 192,
        "grade": 192,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    193: _tools.RODict({
        "ID": 193,
        "grade": 193,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    194: _tools.RODict({
        "ID": 194,
        "grade": 194,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    195: _tools.RODict({
        "ID": 195,
        "grade": 195,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    196: _tools.RODict({
        "ID": 196,
        "grade": 196,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    197: _tools.RODict({
        "ID": 197,
        "grade": 197,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    198: _tools.RODict({
        "ID": 198,
        "grade": 198,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    199: _tools.RODict({
        "ID": 199,
        "grade": 199,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    }),
    200: _tools.RODict({
        "ID": 200,
        "grade": 200,
        "expPlayer": 822800000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (17898, 18841, 19783)
    })
})
minKey = 1
maxKey = 200