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
        "idleIncome": (749, 789, 828)
    }),
    2: _tools.RODict({
        "ID": 2,
        "grade": 2,
        "expPlayer": 150,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3161], [3162, 3494], [3495]),
        "idleIncome": (749, 789, 828)
    }),
    3: _tools.RODict({
        "ID": 3,
        "grade": 3,
        "expPlayer": 250,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3693], [3694, 4082], [4083]),
        "idleIncome": (749, 789, 828)
    }),
    4: _tools.RODict({
        "ID": 4,
        "grade": 4,
        "expPlayer": 500,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 3976], [3977, 4395], [4396]),
        "idleIncome": (749, 789, 828)
    }),
    5: _tools.RODict({
        "ID": 5,
        "grade": 5,
        "expPlayer": 650,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 4508], [4509, 4983], [4984]),
        "idleIncome": (749, 789, 828)
    }),
    6: _tools.RODict({
        "ID": 6,
        "grade": 6,
        "expPlayer": 2000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 8116], [8117, 8971], [8972]),
        "idleIncome": (749, 789, 828)
    }),
    7: _tools.RODict({
        "ID": 7,
        "grade": 7,
        "expPlayer": 4000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 8529], [8530, 9426], [9427]),
        "idleIncome": (749, 789, 828)
    }),
    8: _tools.RODict({
        "ID": 8,
        "grade": 8,
        "expPlayer": 7000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 9158], [9159, 10122], [10123]),
        "idleIncome": (749, 789, 828)
    }),
    9: _tools.RODict({
        "ID": 9,
        "grade": 9,
        "expPlayer": 11000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 9676], [9677, 10695], [10696]),
        "idleIncome": (749, 789, 828)
    }),
    10: _tools.RODict({
        "ID": 10,
        "grade": 10,
        "expPlayer": 15000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 11216], [11217, 12397], [12398]),
        "idleIncome": (749, 789, 828)
    }),
    11: _tools.RODict({
        "ID": 11,
        "grade": 11,
        "expPlayer": 16000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 12136], [12137, 13413], [13414]),
        "idleIncome": (749, 789, 828)
    }),
    12: _tools.RODict({
        "ID": 12,
        "grade": 12,
        "expPlayer": 27000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 12481], [12482, 13794], [13795]),
        "idleIncome": (749, 789, 828)
    }),
    13: _tools.RODict({
        "ID": 13,
        "grade": 13,
        "expPlayer": 42500,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 13013], [13014, 14382], [14383]),
        "idleIncome": (749, 789, 828)
    }),
    14: _tools.RODict({
        "ID": 14,
        "grade": 14,
        "expPlayer": 77500,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 13357], [13358, 14763], [14764]),
        "idleIncome": (749, 789, 828)
    }),
    15: _tools.RODict({
        "ID": 15,
        "grade": 15,
        "expPlayer": 100000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 14240], [14241, 15739], [15740]),
        "idleIncome": (749, 789, 828)
    }),
    16: _tools.RODict({
        "ID": 16,
        "grade": 16,
        "expPlayer": 150000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 15514], [15515, 17147], [17148]),
        "idleIncome": (749, 789, 828)
    }),
    17: _tools.RODict({
        "ID": 17,
        "grade": 17,
        "expPlayer": 200000,
        "fakeOnlineTime": 2,
        "score": 0,
        "powerRange": ([0, 16074], [16075, 17767], [17768]),
        "idleIncome": (749, 789, 828)
    }),
    18: _tools.RODict({
        "ID": 18,
        "grade": 18,
        "expPlayer": 250000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 16435], [16436, 18166], [18167]),
        "idleIncome": (749, 789, 828)
    }),
    19: _tools.RODict({
        "ID": 19,
        "grade": 19,
        "expPlayer": 300000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 16954], [16955, 18739], [18740]),
        "idleIncome": (749, 789, 828)
    }),
    20: _tools.RODict({
        "ID": 20,
        "grade": 20,
        "expPlayer": 450000,
        "fakeOnlineTime": 4,
        "score": 0,
        "powerRange": ([0, 19965], [19966, 22066], [22067]),
        "idleIncome": (749, 789, 828)
    }),
    21: _tools.RODict({
        "ID": 21,
        "grade": 21,
        "expPlayer": 500000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 20881], [20882, 23080], [23081]),
        "idleIncome": (771, 812, 852)
    }),
    22: _tools.RODict({
        "ID": 22,
        "grade": 22,
        "expPlayer": 750000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 21527], [21528, 23794], [23795]),
        "idleIncome": (795, 837, 878)
    }),
    23: _tools.RODict({
        "ID": 23,
        "grade": 23,
        "expPlayer": 1000000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 22082], [22083, 24407], [24408]),
        "idleIncome": (818, 862, 905)
    }),
    24: _tools.RODict({
        "ID": 24,
        "grade": 24,
        "expPlayer": 1100000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 23099], [23100, 25530], [25531]),
        "idleIncome": (843, 888, 932)
    }),
    25: _tools.RODict({
        "ID": 25,
        "grade": 25,
        "expPlayer": 1150000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 26443], [26444, 29226], [29227]),
        "idleIncome": (868, 914, 959)
    }),
    26: _tools.RODict({
        "ID": 26,
        "grade": 26,
        "expPlayer": 1400000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 27779], [27780, 30704], [30705]),
        "idleIncome": (894, 942, 989)
    }),
    27: _tools.RODict({
        "ID": 27,
        "grade": 27,
        "expPlayer": 1600000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 28670], [28671, 31687], [31688]),
        "idleIncome": (921, 970, 1018)
    }),
    28: _tools.RODict({
        "ID": 28,
        "grade": 28,
        "expPlayer": 1800000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 29634], [29635, 32753], [32754]),
        "idleIncome": (949, 999, 1048)
    }),
    29: _tools.RODict({
        "ID": 29,
        "grade": 29,
        "expPlayer": 2000000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 30153], [30154, 33327], [33328]),
        "idleIncome": (977, 1029, 1080)
    }),
    30: _tools.RODict({
        "ID": 30,
        "grade": 30,
        "expPlayer": 2200000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 36376], [36377, 40205], [40206]),
        "idleIncome": (1007, 1060, 1113)
    }),
    31: _tools.RODict({
        "ID": 31,
        "grade": 31,
        "expPlayer": 2400000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 38294], [38295, 42325], [42326]),
        "idleIncome": (1037, 1092, 1146)
    }),
    32: _tools.RODict({
        "ID": 32,
        "grade": 32,
        "expPlayer": 2600000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 40212], [40213, 44445], [44446]),
        "idleIncome": (1068, 1125, 1181)
    }),
    33: _tools.RODict({
        "ID": 33,
        "grade": 33,
        "expPlayer": 3600000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 42130], [42131, 46565], [46566]),
        "idleIncome": (1100, 1158, 1215)
    }),
    34: _tools.RODict({
        "ID": 34,
        "grade": 34,
        "expPlayer": 4300000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 44047], [44048, 48684], [48685]),
        "idleIncome": (1133, 1193, 1252)
    }),
    35: _tools.RODict({
        "ID": 35,
        "grade": 35,
        "expPlayer": 4500000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 45965], [45966, 50804], [50805]),
        "idleIncome": (1167, 1229, 1290)
    }),
    36: _tools.RODict({
        "ID": 36,
        "grade": 36,
        "expPlayer": 4700000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 47883], [47884, 52924], [52925]),
        "idleIncome": (1202, 1266, 1329)
    }),
    37: _tools.RODict({
        "ID": 37,
        "grade": 37,
        "expPlayer": 4800000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 49801], [49802, 55044], [55045]),
        "idleIncome": (1238, 1304, 1369)
    }),
    38: _tools.RODict({
        "ID": 38,
        "grade": 38,
        "expPlayer": 4900000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 51719], [51720, 57164], [57165]),
        "idleIncome": (1275, 1343, 1410)
    }),
    39: _tools.RODict({
        "ID": 39,
        "grade": 39,
        "expPlayer": 6437000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 53637], [53638, 59284], [59285]),
        "idleIncome": (1313, 1383, 1452)
    }),
    40: _tools.RODict({
        "ID": 40,
        "grade": 40,
        "expPlayer": 6857000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 55556], [55557, 61404], [61405]),
        "idleIncome": (1366, 1438, 1509)
    }),
    41: _tools.RODict({
        "ID": 41,
        "grade": 41,
        "expPlayer": 7165000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 56885], [56886, 62872], [62873]),
        "idleIncome": (1421, 1496, 1570)
    }),
    42: _tools.RODict({
        "ID": 42,
        "grade": 42,
        "expPlayer": 7470000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 58214], [58215, 64341], [64342]),
        "idleIncome": (1478, 1556, 1633)
    }),
    43: _tools.RODict({
        "ID": 43,
        "grade": 43,
        "expPlayer": 7804000,
        "fakeOnlineTime": 10,
        "score": 0,
        "powerRange": ([0, 59543], [59544, 65810], [65811]),
        "idleIncome": (1537, 1618, 1698)
    }),
    44: _tools.RODict({
        "ID": 44,
        "grade": 44,
        "expPlayer": 8136000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 60872], [60873, 67279], [67280]),
        "idleIncome": (1598, 1683, 1767)
    }),
    45: _tools.RODict({
        "ID": 45,
        "grade": 45,
        "expPlayer": 12750000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 62201], [62202, 68748], [68749]),
        "idleIncome": (1662, 1750, 1837)
    }),
    46: _tools.RODict({
        "ID": 46,
        "grade": 46,
        "expPlayer": 13293000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 63530], [63531, 70217], [70218]),
        "idleIncome": (1729, 1820, 1911)
    }),
    47: _tools.RODict({
        "ID": 47,
        "grade": 47,
        "expPlayer": 13887000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 64860], [64861, 71687], [71688]),
        "idleIncome": (1798, 1893, 1987)
    }),
    48: _tools.RODict({
        "ID": 48,
        "grade": 48,
        "expPlayer": 14477000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 66189], [66190, 73156], [73157]),
        "idleIncome": (1870, 1969, 2067)
    }),
    49: _tools.RODict({
        "ID": 49,
        "grade": 49,
        "expPlayer": 27250000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 67518], [67519, 74625], [74626]),
        "idleIncome": (1945, 2048, 2150)
    }),
    50: _tools.RODict({
        "ID": 50,
        "grade": 50,
        "expPlayer": 28409000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 68847], [68848, 76094], [76095]),
        "idleIncome": (2023, 2130, 2236)
    }),
    51: _tools.RODict({
        "ID": 51,
        "grade": 51,
        "expPlayer": 29677000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 70585], [70586, 78015], [78016]),
        "idleIncome": (2104, 2215, 2325)
    }),
    52: _tools.RODict({
        "ID": 52,
        "grade": 52,
        "expPlayer": 30938000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 72322], [72323, 79935], [79936]),
        "idleIncome": (2187, 2303, 2418)
    }),
    53: _tools.RODict({
        "ID": 53,
        "grade": 53,
        "expPlayer": 32318000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 74060], [74061, 81855], [81856]),
        "idleIncome": (2276, 2396, 2515)
    }),
    54: _tools.RODict({
        "ID": 54,
        "grade": 54,
        "expPlayer": 33690000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 75797], [75798, 83776], [83777]),
        "idleIncome": (2366, 2491, 2615)
    }),
    55: _tools.RODict({
        "ID": 55,
        "grade": 55,
        "expPlayer": 35192000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 77535], [77536, 85696], [85697]),
        "idleIncome": (2461, 2591, 2720)
    }),
    56: _tools.RODict({
        "ID": 56,
        "grade": 56,
        "expPlayer": 36686000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 79272], [79273, 87617], [87618]),
        "idleIncome": (2560, 2695, 2829)
    }),
    57: _tools.RODict({
        "ID": 57,
        "grade": 57,
        "expPlayer": 38320000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 81010], [81011, 89537], [89538]),
        "idleIncome": (2662, 2803, 2943)
    }),
    58: _tools.RODict({
        "ID": 58,
        "grade": 58,
        "expPlayer": 39946000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 82747], [82748, 91458], [91459]),
        "idleIncome": (2769, 2915, 3060)
    }),
    59: _tools.RODict({
        "ID": 59,
        "grade": 59,
        "expPlayer": 92629000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 84485], [84486, 93378], [93379]),
        "idleIncome": (2879, 3031, 3182)
    }),
    60: _tools.RODict({
        "ID": 60,
        "grade": 60,
        "expPlayer": 96558000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 86222], [86223, 95299], [95300]),
        "idleIncome": (2995, 3153, 3310)
    }),
    61: _tools.RODict({
        "ID": 61,
        "grade": 61,
        "expPlayer": 100854000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 87697], [87698, 96928], [96929]),
        "idleIncome": (3115, 3279, 3442)
    }),
    62: _tools.RODict({
        "ID": 62,
        "grade": 62,
        "expPlayer": 105130000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 89172], [89173, 98559], [98560]),
        "idleIncome": (3239, 3410, 3580)
    }),
    63: _tools.RODict({
        "ID": 63,
        "grade": 63,
        "expPlayer": 109804000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 90647], [90648, 100188], [100189]),
        "idleIncome": (3368, 3546, 3723)
    }),
    64: _tools.RODict({
        "ID": 64,
        "grade": 64,
        "expPlayer": 114458000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 92121], [92122, 101818], [101819]),
        "idleIncome": (3503, 3688, 3872)
    }),
    65: _tools.RODict({
        "ID": 65,
        "grade": 65,
        "expPlayer": 119543000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 93596], [93597, 103449], [103450]),
        "idleIncome": (3644, 3836, 4027)
    }),
    66: _tools.RODict({
        "ID": 66,
        "grade": 66,
        "expPlayer": 124609000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 95071], [95072, 105078], [105079]),
        "idleIncome": (3789, 3989, 4188)
    }),
    67: _tools.RODict({
        "ID": 67,
        "grade": 67,
        "expPlayer": 130141000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 96545], [96546, 106708], [106709]),
        "idleIncome": (3941, 4149, 4356)
    }),
    68: _tools.RODict({
        "ID": 68,
        "grade": 68,
        "expPlayer": 135654000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 98021], [98022, 108339], [108340]),
        "idleIncome": (4099, 4315, 4530)
    }),
    69: _tools.RODict({
        "ID": 69,
        "grade": 69,
        "expPlayer": 157414000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 99495], [99496, 109968], [109969]),
        "idleIncome": (4262, 4487, 4711)
    }),
    70: _tools.RODict({
        "ID": 70,
        "grade": 70,
        "expPlayer": 164080000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 100970], [100971, 111599], [111600]),
        "idleIncome": (4433, 4667, 4900)
    }),
    71: _tools.RODict({
        "ID": 71,
        "grade": 71,
        "expPlayer": 171355000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 102684], [102685, 113493], [113494]),
        "idleIncome": (4610, 4853, 5095)
    }),
    72: _tools.RODict({
        "ID": 72,
        "grade": 72,
        "expPlayer": 178608000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 104399], [104400, 115388], [115389]),
        "idleIncome": (4795, 5048, 5300)
    }),
    73: _tools.RODict({
        "ID": 73,
        "grade": 73,
        "expPlayer": 186523000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 106114], [106115, 117283], [117284]),
        "idleIncome": (4987, 5250, 5512)
    }),
    74: _tools.RODict({
        "ID": 74,
        "grade": 74,
        "expPlayer": 249963000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 107828], [107829, 119179], [119180]),
        "idleIncome": (5187, 5460, 5733)
    }),
    75: _tools.RODict({
        "ID": 75,
        "grade": 75,
        "expPlayer": 261033000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 109542], [109543, 121073], [121074]),
        "idleIncome": (5394, 5678, 5961)
    }),
    76: _tools.RODict({
        "ID": 76,
        "grade": 76,
        "expPlayer": 272074000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 111257], [111258, 122968], [122969]),
        "idleIncome": (5609, 5905, 6200)
    }),
    77: _tools.RODict({
        "ID": 77,
        "grade": 77,
        "expPlayer": 284116000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 112972], [112973, 124863], [124864]),
        "idleIncome": (5833, 6141, 6448)
    }),
    78: _tools.RODict({
        "ID": 78,
        "grade": 78,
        "expPlayer": 296129000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 114686], [114687, 126759], [126760]),
        "idleIncome": (6067, 6387, 6706)
    }),
    79: _tools.RODict({
        "ID": 79,
        "grade": 79,
        "expPlayer": 308553000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 116400], [116401, 128653], [128654]),
        "idleIncome": (6309, 6642, 6974)
    }),
    80: _tools.RODict({
        "ID": 80,
        "grade": 80,
        "expPlayer": 320895000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 118115], [118116, 130548], [130549]),
        "idleIncome": (6562, 6908, 7253)
    }),
    81: _tools.RODict({
        "ID": 81,
        "grade": 81,
        "expPlayer": 334357000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 121046], [121047, 133787], [133788]),
        "idleIncome": (6825, 7185, 7544)
    }),
    82: _tools.RODict({
        "ID": 82,
        "grade": 82,
        "expPlayer": 347731000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 123975], [123976, 137026], [137027]),
        "idleIncome": (7098, 7472, 7845)
    }),
    83: _tools.RODict({
        "ID": 83,
        "grade": 83,
        "expPlayer": 507244000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 126906], [126907, 140265], [140266]),
        "idleIncome": (7382, 7771, 8159)
    }),
    84: _tools.RODict({
        "ID": 84,
        "grade": 84,
        "expPlayer": 527533000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 129837], [129838, 143504], [143505]),
        "idleIncome": (7677, 8082, 8486)
    }),
    85: _tools.RODict({
        "ID": 85,
        "grade": 85,
        "expPlayer": 549660000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 132768], [132769, 146743], [146744]),
        "idleIncome": (7984, 8405, 8825)
    }),
    86: _tools.RODict({
        "ID": 86,
        "grade": 86,
        "expPlayer": 571646000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 135698], [135699, 149982], [149983]),
        "idleIncome": (8303, 8741, 9178)
    }),
    87: _tools.RODict({
        "ID": 87,
        "grade": 87,
        "expPlayer": 595620000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 138628], [138629, 153221], [153222]),
        "idleIncome": (8636, 9091, 9545)
    }),
    88: _tools.RODict({
        "ID": 88,
        "grade": 88,
        "expPlayer": 619445000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 141559], [141560, 156460], [156461]),
        "idleIncome": (8981, 9454, 9926)
    }),
    89: _tools.RODict({
        "ID": 89,
        "grade": 89,
        "expPlayer": 645422000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 144489], [144490, 159698], [159699]),
        "idleIncome": (9341, 9833, 10324)
    }),
    90: _tools.RODict({
        "ID": 90,
        "grade": 90,
        "expPlayer": 671239000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    91: _tools.RODict({
        "ID": 91,
        "grade": 91,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    92: _tools.RODict({
        "ID": 92,
        "grade": 92,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    93: _tools.RODict({
        "ID": 93,
        "grade": 93,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    94: _tools.RODict({
        "ID": 94,
        "grade": 94,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    95: _tools.RODict({
        "ID": 95,
        "grade": 95,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    96: _tools.RODict({
        "ID": 96,
        "grade": 96,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    97: _tools.RODict({
        "ID": 97,
        "grade": 97,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    98: _tools.RODict({
        "ID": 98,
        "grade": 98,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    99: _tools.RODict({
        "ID": 99,
        "grade": 99,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    100: _tools.RODict({
        "ID": 100,
        "grade": 100,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    101: _tools.RODict({
        "ID": 101,
        "grade": 101,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    102: _tools.RODict({
        "ID": 102,
        "grade": 102,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    103: _tools.RODict({
        "ID": 103,
        "grade": 103,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    104: _tools.RODict({
        "ID": 104,
        "grade": 104,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    105: _tools.RODict({
        "ID": 105,
        "grade": 105,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    106: _tools.RODict({
        "ID": 106,
        "grade": 106,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    107: _tools.RODict({
        "ID": 107,
        "grade": 107,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    108: _tools.RODict({
        "ID": 108,
        "grade": 108,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    109: _tools.RODict({
        "ID": 109,
        "grade": 109,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    110: _tools.RODict({
        "ID": 110,
        "grade": 110,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    111: _tools.RODict({
        "ID": 111,
        "grade": 111,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    112: _tools.RODict({
        "ID": 112,
        "grade": 112,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    113: _tools.RODict({
        "ID": 113,
        "grade": 113,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    114: _tools.RODict({
        "ID": 114,
        "grade": 114,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    115: _tools.RODict({
        "ID": 115,
        "grade": 115,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    116: _tools.RODict({
        "ID": 116,
        "grade": 116,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    117: _tools.RODict({
        "ID": 117,
        "grade": 117,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    118: _tools.RODict({
        "ID": 118,
        "grade": 118,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    119: _tools.RODict({
        "ID": 119,
        "grade": 119,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    120: _tools.RODict({
        "ID": 120,
        "grade": 120,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    121: _tools.RODict({
        "ID": 121,
        "grade": 121,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    122: _tools.RODict({
        "ID": 122,
        "grade": 122,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    123: _tools.RODict({
        "ID": 123,
        "grade": 123,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    124: _tools.RODict({
        "ID": 124,
        "grade": 124,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    125: _tools.RODict({
        "ID": 125,
        "grade": 125,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    126: _tools.RODict({
        "ID": 126,
        "grade": 126,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    127: _tools.RODict({
        "ID": 127,
        "grade": 127,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    128: _tools.RODict({
        "ID": 128,
        "grade": 128,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    129: _tools.RODict({
        "ID": 129,
        "grade": 129,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    130: _tools.RODict({
        "ID": 130,
        "grade": 130,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    131: _tools.RODict({
        "ID": 131,
        "grade": 131,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    132: _tools.RODict({
        "ID": 132,
        "grade": 132,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    133: _tools.RODict({
        "ID": 133,
        "grade": 133,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    134: _tools.RODict({
        "ID": 134,
        "grade": 134,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    135: _tools.RODict({
        "ID": 135,
        "grade": 135,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    136: _tools.RODict({
        "ID": 136,
        "grade": 136,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    137: _tools.RODict({
        "ID": 137,
        "grade": 137,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    138: _tools.RODict({
        "ID": 138,
        "grade": 138,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    139: _tools.RODict({
        "ID": 139,
        "grade": 139,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    140: _tools.RODict({
        "ID": 140,
        "grade": 140,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    141: _tools.RODict({
        "ID": 141,
        "grade": 141,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    142: _tools.RODict({
        "ID": 142,
        "grade": 142,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    143: _tools.RODict({
        "ID": 143,
        "grade": 143,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    144: _tools.RODict({
        "ID": 144,
        "grade": 144,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    145: _tools.RODict({
        "ID": 145,
        "grade": 145,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    146: _tools.RODict({
        "ID": 146,
        "grade": 146,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    147: _tools.RODict({
        "ID": 147,
        "grade": 147,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    148: _tools.RODict({
        "ID": 148,
        "grade": 148,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    149: _tools.RODict({
        "ID": 149,
        "grade": 149,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    150: _tools.RODict({
        "ID": 150,
        "grade": 150,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    151: _tools.RODict({
        "ID": 151,
        "grade": 151,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    152: _tools.RODict({
        "ID": 152,
        "grade": 152,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    153: _tools.RODict({
        "ID": 153,
        "grade": 153,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    154: _tools.RODict({
        "ID": 154,
        "grade": 154,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    155: _tools.RODict({
        "ID": 155,
        "grade": 155,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    156: _tools.RODict({
        "ID": 156,
        "grade": 156,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    157: _tools.RODict({
        "ID": 157,
        "grade": 157,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    158: _tools.RODict({
        "ID": 158,
        "grade": 158,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    159: _tools.RODict({
        "ID": 159,
        "grade": 159,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    160: _tools.RODict({
        "ID": 160,
        "grade": 160,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    161: _tools.RODict({
        "ID": 161,
        "grade": 161,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    162: _tools.RODict({
        "ID": 162,
        "grade": 162,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    163: _tools.RODict({
        "ID": 163,
        "grade": 163,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    164: _tools.RODict({
        "ID": 164,
        "grade": 164,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    165: _tools.RODict({
        "ID": 165,
        "grade": 165,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    166: _tools.RODict({
        "ID": 166,
        "grade": 166,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    167: _tools.RODict({
        "ID": 167,
        "grade": 167,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    168: _tools.RODict({
        "ID": 168,
        "grade": 168,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    169: _tools.RODict({
        "ID": 169,
        "grade": 169,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    170: _tools.RODict({
        "ID": 170,
        "grade": 170,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    171: _tools.RODict({
        "ID": 171,
        "grade": 171,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    172: _tools.RODict({
        "ID": 172,
        "grade": 172,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    173: _tools.RODict({
        "ID": 173,
        "grade": 173,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    174: _tools.RODict({
        "ID": 174,
        "grade": 174,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    175: _tools.RODict({
        "ID": 175,
        "grade": 175,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    176: _tools.RODict({
        "ID": 176,
        "grade": 176,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    177: _tools.RODict({
        "ID": 177,
        "grade": 177,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    178: _tools.RODict({
        "ID": 178,
        "grade": 178,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    179: _tools.RODict({
        "ID": 179,
        "grade": 179,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    180: _tools.RODict({
        "ID": 180,
        "grade": 180,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    181: _tools.RODict({
        "ID": 181,
        "grade": 181,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    182: _tools.RODict({
        "ID": 182,
        "grade": 182,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    183: _tools.RODict({
        "ID": 183,
        "grade": 183,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    184: _tools.RODict({
        "ID": 184,
        "grade": 184,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    185: _tools.RODict({
        "ID": 185,
        "grade": 185,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    186: _tools.RODict({
        "ID": 186,
        "grade": 186,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    187: _tools.RODict({
        "ID": 187,
        "grade": 187,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    188: _tools.RODict({
        "ID": 188,
        "grade": 188,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    189: _tools.RODict({
        "ID": 189,
        "grade": 189,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    190: _tools.RODict({
        "ID": 190,
        "grade": 190,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    191: _tools.RODict({
        "ID": 191,
        "grade": 191,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    192: _tools.RODict({
        "ID": 192,
        "grade": 192,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    193: _tools.RODict({
        "ID": 193,
        "grade": 193,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    194: _tools.RODict({
        "ID": 194,
        "grade": 194,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    195: _tools.RODict({
        "ID": 195,
        "grade": 195,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    196: _tools.RODict({
        "ID": 196,
        "grade": 196,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    197: _tools.RODict({
        "ID": 197,
        "grade": 197,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    198: _tools.RODict({
        "ID": 198,
        "grade": 198,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    199: _tools.RODict({
        "ID": 199,
        "grade": 199,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    }),
    200: _tools.RODict({
        "ID": 200,
        "grade": 200,
        "expPlayer": 698088000,
        "fakeOnlineTime": 20,
        "score": 0,
        "powerRange": ([0, 147420], [147421, 162937], [162938]),
        "idleIncome": (9714, 10226, 10737)
    })
})
minKey = 1
maxKey = 200