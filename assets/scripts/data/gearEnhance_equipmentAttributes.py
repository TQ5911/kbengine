# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/equipmentAttributes
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
        "equipmentID": 80111001,
        "strengthen": 1,
        "propID": 52012150
    }),
    2: _tools.RODict({
        "ID": 2,
        "equipmentID": 80111001,
        "strengthen": 2,
        "propID": 52012151
    }),
    3: _tools.RODict({
        "ID": 3,
        "equipmentID": 80111001,
        "strengthen": 3,
        "propID": 52012152
    }),
    4: _tools.RODict({
        "ID": 4,
        "equipmentID": 80111001,
        "strengthen": 4,
        "propID": 52012153
    }),
    5: _tools.RODict({
        "ID": 5,
        "equipmentID": 80112001,
        "strengthen": 1,
        "propID": 52012154
    }),
    6: _tools.RODict({
        "ID": 6,
        "equipmentID": 80112001,
        "strengthen": 2,
        "propID": 52012155
    }),
    7: _tools.RODict({
        "ID": 7,
        "equipmentID": 80112001,
        "strengthen": 3,
        "propID": 52012156
    }),
    8: _tools.RODict({
        "ID": 8,
        "equipmentID": 80112001,
        "strengthen": 4,
        "propID": 52012157
    }),
    9: _tools.RODict({
        "ID": 9,
        "equipmentID": 80113001,
        "strengthen": 1,
        "propID": 52012158
    }),
    10: _tools.RODict({
        "ID": 10,
        "equipmentID": 80113001,
        "strengthen": 2,
        "propID": 52012159
    }),
    11: _tools.RODict({
        "ID": 11,
        "equipmentID": 80113001,
        "strengthen": 3,
        "propID": 52012160
    }),
    12: _tools.RODict({
        "ID": 12,
        "equipmentID": 80113001,
        "strengthen": 4,
        "propID": 52012161
    }),
    13: _tools.RODict({
        "ID": 13,
        "equipmentID": 80114001,
        "strengthen": 1,
        "propID": 52012162
    }),
    14: _tools.RODict({
        "ID": 14,
        "equipmentID": 80114001,
        "strengthen": 2,
        "propID": 52012163
    }),
    15: _tools.RODict({
        "ID": 15,
        "equipmentID": 80114001,
        "strengthen": 3,
        "propID": 52012164
    }),
    16: _tools.RODict({
        "ID": 16,
        "equipmentID": 80114001,
        "strengthen": 4,
        "propID": 52012165
    }),
    177: _tools.RODict({
        "ID": 177,
        "equipmentID": 80121001,
        "strengthen": 1,
        "propID": 52012326
    }),
    178: _tools.RODict({
        "ID": 178,
        "equipmentID": 80121001,
        "strengthen": 2,
        "propID": 52012327
    }),
    179: _tools.RODict({
        "ID": 179,
        "equipmentID": 80121001,
        "strengthen": 3,
        "propID": 52012328
    }),
    180: _tools.RODict({
        "ID": 180,
        "equipmentID": 80121001,
        "strengthen": 4,
        "propID": 52012329
    }),
    181: _tools.RODict({
        "ID": 181,
        "equipmentID": 80122001,
        "strengthen": 1,
        "propID": 52012330
    }),
    182: _tools.RODict({
        "ID": 182,
        "equipmentID": 80122001,
        "strengthen": 2,
        "propID": 52012331
    }),
    183: _tools.RODict({
        "ID": 183,
        "equipmentID": 80122001,
        "strengthen": 3,
        "propID": 52012332
    }),
    184: _tools.RODict({
        "ID": 184,
        "equipmentID": 80122001,
        "strengthen": 4,
        "propID": 52012333
    }),
    185: _tools.RODict({
        "ID": 185,
        "equipmentID": 80123001,
        "strengthen": 1,
        "propID": 52012334
    }),
    186: _tools.RODict({
        "ID": 186,
        "equipmentID": 80123001,
        "strengthen": 2,
        "propID": 52012335
    }),
    187: _tools.RODict({
        "ID": 187,
        "equipmentID": 80123001,
        "strengthen": 3,
        "propID": 52012336
    }),
    188: _tools.RODict({
        "ID": 188,
        "equipmentID": 80123001,
        "strengthen": 4,
        "propID": 52012337
    }),
    189: _tools.RODict({
        "ID": 189,
        "equipmentID": 80124001,
        "strengthen": 1,
        "propID": 52012338
    }),
    190: _tools.RODict({
        "ID": 190,
        "equipmentID": 80124001,
        "strengthen": 2,
        "propID": 52012339
    }),
    191: _tools.RODict({
        "ID": 191,
        "equipmentID": 80124001,
        "strengthen": 3,
        "propID": 52012340
    }),
    192: _tools.RODict({
        "ID": 192,
        "equipmentID": 80124001,
        "strengthen": 4,
        "propID": 52012341
    }),
    353: _tools.RODict({
        "ID": 353,
        "equipmentID": 80131001,
        "strengthen": 1,
        "propID": 52012502
    }),
    354: _tools.RODict({
        "ID": 354,
        "equipmentID": 80131001,
        "strengthen": 2,
        "propID": 52012503
    }),
    355: _tools.RODict({
        "ID": 355,
        "equipmentID": 80131001,
        "strengthen": 3,
        "propID": 52012504
    }),
    356: _tools.RODict({
        "ID": 356,
        "equipmentID": 80131001,
        "strengthen": 4,
        "propID": 52012505
    }),
    357: _tools.RODict({
        "ID": 357,
        "equipmentID": 80132001,
        "strengthen": 1,
        "propID": 52012506
    }),
    358: _tools.RODict({
        "ID": 358,
        "equipmentID": 80132001,
        "strengthen": 2,
        "propID": 52012507
    }),
    359: _tools.RODict({
        "ID": 359,
        "equipmentID": 80132001,
        "strengthen": 3,
        "propID": 52012508
    }),
    360: _tools.RODict({
        "ID": 360,
        "equipmentID": 80132001,
        "strengthen": 4,
        "propID": 52012509
    }),
    361: _tools.RODict({
        "ID": 361,
        "equipmentID": 80133001,
        "strengthen": 1,
        "propID": 52012510
    }),
    362: _tools.RODict({
        "ID": 362,
        "equipmentID": 80133001,
        "strengthen": 2,
        "propID": 52012511
    }),
    363: _tools.RODict({
        "ID": 363,
        "equipmentID": 80133001,
        "strengthen": 3,
        "propID": 52012512
    }),
    364: _tools.RODict({
        "ID": 364,
        "equipmentID": 80133001,
        "strengthen": 4,
        "propID": 52012513
    }),
    365: _tools.RODict({
        "ID": 365,
        "equipmentID": 80134001,
        "strengthen": 1,
        "propID": 52012514
    }),
    366: _tools.RODict({
        "ID": 366,
        "equipmentID": 80134001,
        "strengthen": 2,
        "propID": 52012515
    }),
    367: _tools.RODict({
        "ID": 367,
        "equipmentID": 80134001,
        "strengthen": 3,
        "propID": 52012516
    }),
    368: _tools.RODict({
        "ID": 368,
        "equipmentID": 80134001,
        "strengthen": 4,
        "propID": 52012517
    }),
    529: _tools.RODict({
        "ID": 529,
        "equipmentID": 80211001,
        "strengthen": 1,
        "propID": 52012678
    }),
    530: _tools.RODict({
        "ID": 530,
        "equipmentID": 80211001,
        "strengthen": 2,
        "propID": 52012679
    }),
    531: _tools.RODict({
        "ID": 531,
        "equipmentID": 80211001,
        "strengthen": 3,
        "propID": 52012680
    }),
    532: _tools.RODict({
        "ID": 532,
        "equipmentID": 80211001,
        "strengthen": 4,
        "propID": 52012681
    }),
    533: _tools.RODict({
        "ID": 533,
        "equipmentID": 80212001,
        "strengthen": 1,
        "propID": 52012682
    }),
    534: _tools.RODict({
        "ID": 534,
        "equipmentID": 80212001,
        "strengthen": 2,
        "propID": 52012683
    }),
    535: _tools.RODict({
        "ID": 535,
        "equipmentID": 80212001,
        "strengthen": 3,
        "propID": 52012684
    }),
    536: _tools.RODict({
        "ID": 536,
        "equipmentID": 80212001,
        "strengthen": 4,
        "propID": 52012685
    }),
    537: _tools.RODict({
        "ID": 537,
        "equipmentID": 80213001,
        "strengthen": 1,
        "propID": 52012686
    }),
    538: _tools.RODict({
        "ID": 538,
        "equipmentID": 80213001,
        "strengthen": 2,
        "propID": 52012687
    }),
    539: _tools.RODict({
        "ID": 539,
        "equipmentID": 80213001,
        "strengthen": 3,
        "propID": 52012688
    }),
    540: _tools.RODict({
        "ID": 540,
        "equipmentID": 80213001,
        "strengthen": 4,
        "propID": 52012689
    }),
    541: _tools.RODict({
        "ID": 541,
        "equipmentID": 80214001,
        "strengthen": 1,
        "propID": 52012690
    }),
    542: _tools.RODict({
        "ID": 542,
        "equipmentID": 80214001,
        "strengthen": 2,
        "propID": 52012691
    }),
    543: _tools.RODict({
        "ID": 543,
        "equipmentID": 80214001,
        "strengthen": 3,
        "propID": 52012692
    }),
    544: _tools.RODict({
        "ID": 544,
        "equipmentID": 80214001,
        "strengthen": 4,
        "propID": 52012693
    }),
    705: _tools.RODict({
        "ID": 705,
        "equipmentID": 80221001,
        "strengthen": 1,
        "propID": 52012678
    }),
    706: _tools.RODict({
        "ID": 706,
        "equipmentID": 80221001,
        "strengthen": 2,
        "propID": 52012679
    }),
    707: _tools.RODict({
        "ID": 707,
        "equipmentID": 80221001,
        "strengthen": 3,
        "propID": 52012680
    }),
    708: _tools.RODict({
        "ID": 708,
        "equipmentID": 80221001,
        "strengthen": 4,
        "propID": 52012681
    }),
    709: _tools.RODict({
        "ID": 709,
        "equipmentID": 80222001,
        "strengthen": 1,
        "propID": 52012682
    }),
    710: _tools.RODict({
        "ID": 710,
        "equipmentID": 80222001,
        "strengthen": 2,
        "propID": 52012683
    }),
    711: _tools.RODict({
        "ID": 711,
        "equipmentID": 80222001,
        "strengthen": 3,
        "propID": 52012684
    }),
    712: _tools.RODict({
        "ID": 712,
        "equipmentID": 80222001,
        "strengthen": 4,
        "propID": 52012685
    }),
    713: _tools.RODict({
        "ID": 713,
        "equipmentID": 80223001,
        "strengthen": 1,
        "propID": 52012686
    }),
    714: _tools.RODict({
        "ID": 714,
        "equipmentID": 80223001,
        "strengthen": 2,
        "propID": 52012687
    }),
    715: _tools.RODict({
        "ID": 715,
        "equipmentID": 80223001,
        "strengthen": 3,
        "propID": 52012688
    }),
    716: _tools.RODict({
        "ID": 716,
        "equipmentID": 80223001,
        "strengthen": 4,
        "propID": 52012689
    }),
    717: _tools.RODict({
        "ID": 717,
        "equipmentID": 80224001,
        "strengthen": 1,
        "propID": 52012690
    }),
    718: _tools.RODict({
        "ID": 718,
        "equipmentID": 80224001,
        "strengthen": 2,
        "propID": 52012691
    }),
    719: _tools.RODict({
        "ID": 719,
        "equipmentID": 80224001,
        "strengthen": 3,
        "propID": 52012692
    }),
    720: _tools.RODict({
        "ID": 720,
        "equipmentID": 80224001,
        "strengthen": 4,
        "propID": 52012693
    }),
    881: _tools.RODict({
        "ID": 881,
        "equipmentID": 80231001,
        "strengthen": 1,
        "propID": 52012678
    }),
    882: _tools.RODict({
        "ID": 882,
        "equipmentID": 80231001,
        "strengthen": 2,
        "propID": 52012679
    }),
    883: _tools.RODict({
        "ID": 883,
        "equipmentID": 80231001,
        "strengthen": 3,
        "propID": 52012680
    }),
    884: _tools.RODict({
        "ID": 884,
        "equipmentID": 80231001,
        "strengthen": 4,
        "propID": 52012681
    }),
    885: _tools.RODict({
        "ID": 885,
        "equipmentID": 80232001,
        "strengthen": 1,
        "propID": 52012682
    }),
    886: _tools.RODict({
        "ID": 886,
        "equipmentID": 80232001,
        "strengthen": 2,
        "propID": 52012683
    }),
    887: _tools.RODict({
        "ID": 887,
        "equipmentID": 80232001,
        "strengthen": 3,
        "propID": 52012684
    }),
    888: _tools.RODict({
        "ID": 888,
        "equipmentID": 80232001,
        "strengthen": 4,
        "propID": 52012685
    }),
    889: _tools.RODict({
        "ID": 889,
        "equipmentID": 80233001,
        "strengthen": 1,
        "propID": 52012686
    }),
    890: _tools.RODict({
        "ID": 890,
        "equipmentID": 80233001,
        "strengthen": 2,
        "propID": 52012687
    }),
    891: _tools.RODict({
        "ID": 891,
        "equipmentID": 80233001,
        "strengthen": 3,
        "propID": 52012688
    }),
    892: _tools.RODict({
        "ID": 892,
        "equipmentID": 80233001,
        "strengthen": 4,
        "propID": 52012689
    }),
    893: _tools.RODict({
        "ID": 893,
        "equipmentID": 80234001,
        "strengthen": 1,
        "propID": 52012690
    }),
    894: _tools.RODict({
        "ID": 894,
        "equipmentID": 80234001,
        "strengthen": 2,
        "propID": 52012691
    }),
    895: _tools.RODict({
        "ID": 895,
        "equipmentID": 80234001,
        "strengthen": 3,
        "propID": 52012692
    }),
    896: _tools.RODict({
        "ID": 896,
        "equipmentID": 80234001,
        "strengthen": 4,
        "propID": 52012693
    }),
    1057: _tools.RODict({
        "ID": 1057,
        "equipmentID": 80311001,
        "strengthen": 1,
        "propID": 52012854
    }),
    1058: _tools.RODict({
        "ID": 1058,
        "equipmentID": 80311001,
        "strengthen": 2,
        "propID": 52012855
    }),
    1059: _tools.RODict({
        "ID": 1059,
        "equipmentID": 80311001,
        "strengthen": 3,
        "propID": 52012856
    }),
    1060: _tools.RODict({
        "ID": 1060,
        "equipmentID": 80311001,
        "strengthen": 4,
        "propID": 52012857
    }),
    1061: _tools.RODict({
        "ID": 1061,
        "equipmentID": 80312001,
        "strengthen": 1,
        "propID": 52012858
    }),
    1062: _tools.RODict({
        "ID": 1062,
        "equipmentID": 80312001,
        "strengthen": 2,
        "propID": 52012859
    }),
    1063: _tools.RODict({
        "ID": 1063,
        "equipmentID": 80312001,
        "strengthen": 3,
        "propID": 52012860
    }),
    1064: _tools.RODict({
        "ID": 1064,
        "equipmentID": 80312001,
        "strengthen": 4,
        "propID": 52012861
    }),
    1065: _tools.RODict({
        "ID": 1065,
        "equipmentID": 80313001,
        "strengthen": 1,
        "propID": 52012862
    }),
    1066: _tools.RODict({
        "ID": 1066,
        "equipmentID": 80313001,
        "strengthen": 2,
        "propID": 52012863
    }),
    1067: _tools.RODict({
        "ID": 1067,
        "equipmentID": 80313001,
        "strengthen": 3,
        "propID": 52012864
    }),
    1068: _tools.RODict({
        "ID": 1068,
        "equipmentID": 80313001,
        "strengthen": 4,
        "propID": 52012865
    }),
    1069: _tools.RODict({
        "ID": 1069,
        "equipmentID": 80314001,
        "strengthen": 1,
        "propID": 52012866
    }),
    1070: _tools.RODict({
        "ID": 1070,
        "equipmentID": 80314001,
        "strengthen": 2,
        "propID": 52012867
    }),
    1071: _tools.RODict({
        "ID": 1071,
        "equipmentID": 80314001,
        "strengthen": 3,
        "propID": 52012868
    }),
    1072: _tools.RODict({
        "ID": 1072,
        "equipmentID": 80314001,
        "strengthen": 4,
        "propID": 52012869
    }),
    1233: _tools.RODict({
        "ID": 1233,
        "equipmentID": 80321001,
        "strengthen": 1,
        "propID": 52012854
    }),
    1234: _tools.RODict({
        "ID": 1234,
        "equipmentID": 80321001,
        "strengthen": 2,
        "propID": 52012855
    }),
    1235: _tools.RODict({
        "ID": 1235,
        "equipmentID": 80321001,
        "strengthen": 3,
        "propID": 52012856
    }),
    1236: _tools.RODict({
        "ID": 1236,
        "equipmentID": 80321001,
        "strengthen": 4,
        "propID": 52012857
    }),
    1237: _tools.RODict({
        "ID": 1237,
        "equipmentID": 80322001,
        "strengthen": 1,
        "propID": 52012858
    }),
    1238: _tools.RODict({
        "ID": 1238,
        "equipmentID": 80322001,
        "strengthen": 2,
        "propID": 52012859
    }),
    1239: _tools.RODict({
        "ID": 1239,
        "equipmentID": 80322001,
        "strengthen": 3,
        "propID": 52012860
    }),
    1240: _tools.RODict({
        "ID": 1240,
        "equipmentID": 80322001,
        "strengthen": 4,
        "propID": 52012861
    }),
    1241: _tools.RODict({
        "ID": 1241,
        "equipmentID": 80323001,
        "strengthen": 1,
        "propID": 52012862
    }),
    1242: _tools.RODict({
        "ID": 1242,
        "equipmentID": 80323001,
        "strengthen": 2,
        "propID": 52012863
    }),
    1243: _tools.RODict({
        "ID": 1243,
        "equipmentID": 80323001,
        "strengthen": 3,
        "propID": 52012864
    }),
    1244: _tools.RODict({
        "ID": 1244,
        "equipmentID": 80323001,
        "strengthen": 4,
        "propID": 52012865
    }),
    1245: _tools.RODict({
        "ID": 1245,
        "equipmentID": 80324001,
        "strengthen": 1,
        "propID": 52012866
    }),
    1246: _tools.RODict({
        "ID": 1246,
        "equipmentID": 80324001,
        "strengthen": 2,
        "propID": 52012867
    }),
    1247: _tools.RODict({
        "ID": 1247,
        "equipmentID": 80324001,
        "strengthen": 3,
        "propID": 52012868
    }),
    1248: _tools.RODict({
        "ID": 1248,
        "equipmentID": 80324001,
        "strengthen": 4,
        "propID": 52012869
    }),
    1409: _tools.RODict({
        "ID": 1409,
        "equipmentID": 80331001,
        "strengthen": 1,
        "propID": 52012854
    }),
    1410: _tools.RODict({
        "ID": 1410,
        "equipmentID": 80331001,
        "strengthen": 2,
        "propID": 52012855
    }),
    1411: _tools.RODict({
        "ID": 1411,
        "equipmentID": 80331001,
        "strengthen": 3,
        "propID": 52012856
    }),
    1412: _tools.RODict({
        "ID": 1412,
        "equipmentID": 80331001,
        "strengthen": 4,
        "propID": 52012857
    }),
    1413: _tools.RODict({
        "ID": 1413,
        "equipmentID": 80332001,
        "strengthen": 1,
        "propID": 52012858
    }),
    1414: _tools.RODict({
        "ID": 1414,
        "equipmentID": 80332001,
        "strengthen": 2,
        "propID": 52012859
    }),
    1415: _tools.RODict({
        "ID": 1415,
        "equipmentID": 80332001,
        "strengthen": 3,
        "propID": 52012860
    }),
    1416: _tools.RODict({
        "ID": 1416,
        "equipmentID": 80332001,
        "strengthen": 4,
        "propID": 52012861
    }),
    1417: _tools.RODict({
        "ID": 1417,
        "equipmentID": 80333001,
        "strengthen": 1,
        "propID": 52012862
    }),
    1418: _tools.RODict({
        "ID": 1418,
        "equipmentID": 80333001,
        "strengthen": 2,
        "propID": 52012863
    }),
    1419: _tools.RODict({
        "ID": 1419,
        "equipmentID": 80333001,
        "strengthen": 3,
        "propID": 52012864
    }),
    1420: _tools.RODict({
        "ID": 1420,
        "equipmentID": 80333001,
        "strengthen": 4,
        "propID": 52012865
    }),
    1421: _tools.RODict({
        "ID": 1421,
        "equipmentID": 80334001,
        "strengthen": 1,
        "propID": 52012866
    }),
    1422: _tools.RODict({
        "ID": 1422,
        "equipmentID": 80334001,
        "strengthen": 2,
        "propID": 52012867
    }),
    1423: _tools.RODict({
        "ID": 1423,
        "equipmentID": 80334001,
        "strengthen": 3,
        "propID": 52012868
    }),
    1424: _tools.RODict({
        "ID": 1424,
        "equipmentID": 80334001,
        "strengthen": 4,
        "propID": 52012869
    }),
    1585: _tools.RODict({
        "ID": 1585,
        "equipmentID": 80411001,
        "strengthen": 1,
        "propID": 52013030
    }),
    1586: _tools.RODict({
        "ID": 1586,
        "equipmentID": 80411001,
        "strengthen": 2,
        "propID": 52013031
    }),
    1587: _tools.RODict({
        "ID": 1587,
        "equipmentID": 80411001,
        "strengthen": 3,
        "propID": 52013032
    }),
    1588: _tools.RODict({
        "ID": 1588,
        "equipmentID": 80411001,
        "strengthen": 4,
        "propID": 52013033
    }),
    1589: _tools.RODict({
        "ID": 1589,
        "equipmentID": 80412001,
        "strengthen": 1,
        "propID": 52013034
    }),
    1590: _tools.RODict({
        "ID": 1590,
        "equipmentID": 80412001,
        "strengthen": 2,
        "propID": 52013035
    }),
    1591: _tools.RODict({
        "ID": 1591,
        "equipmentID": 80412001,
        "strengthen": 3,
        "propID": 52013036
    }),
    1592: _tools.RODict({
        "ID": 1592,
        "equipmentID": 80412001,
        "strengthen": 4,
        "propID": 52013037
    }),
    1593: _tools.RODict({
        "ID": 1593,
        "equipmentID": 80413001,
        "strengthen": 1,
        "propID": 52013038
    }),
    1594: _tools.RODict({
        "ID": 1594,
        "equipmentID": 80413001,
        "strengthen": 2,
        "propID": 52013039
    }),
    1595: _tools.RODict({
        "ID": 1595,
        "equipmentID": 80413001,
        "strengthen": 3,
        "propID": 52013040
    }),
    1596: _tools.RODict({
        "ID": 1596,
        "equipmentID": 80413001,
        "strengthen": 4,
        "propID": 52013041
    }),
    1597: _tools.RODict({
        "ID": 1597,
        "equipmentID": 80414001,
        "strengthen": 1,
        "propID": 52013042
    }),
    1598: _tools.RODict({
        "ID": 1598,
        "equipmentID": 80414001,
        "strengthen": 2,
        "propID": 52013043
    }),
    1599: _tools.RODict({
        "ID": 1599,
        "equipmentID": 80414001,
        "strengthen": 3,
        "propID": 52013044
    }),
    1600: _tools.RODict({
        "ID": 1600,
        "equipmentID": 80414001,
        "strengthen": 4,
        "propID": 52013045
    }),
    1761: _tools.RODict({
        "ID": 1761,
        "equipmentID": 80421001,
        "strengthen": 1,
        "propID": 52013030
    }),
    1762: _tools.RODict({
        "ID": 1762,
        "equipmentID": 80421001,
        "strengthen": 2,
        "propID": 52013031
    }),
    1763: _tools.RODict({
        "ID": 1763,
        "equipmentID": 80421001,
        "strengthen": 3,
        "propID": 52013032
    }),
    1764: _tools.RODict({
        "ID": 1764,
        "equipmentID": 80421001,
        "strengthen": 4,
        "propID": 52013033
    }),
    1765: _tools.RODict({
        "ID": 1765,
        "equipmentID": 80422001,
        "strengthen": 1,
        "propID": 52013034
    }),
    1766: _tools.RODict({
        "ID": 1766,
        "equipmentID": 80422001,
        "strengthen": 2,
        "propID": 52013035
    }),
    1767: _tools.RODict({
        "ID": 1767,
        "equipmentID": 80422001,
        "strengthen": 3,
        "propID": 52013036
    }),
    1768: _tools.RODict({
        "ID": 1768,
        "equipmentID": 80422001,
        "strengthen": 4,
        "propID": 52013037
    }),
    1769: _tools.RODict({
        "ID": 1769,
        "equipmentID": 80423001,
        "strengthen": 1,
        "propID": 52013038
    }),
    1770: _tools.RODict({
        "ID": 1770,
        "equipmentID": 80423001,
        "strengthen": 2,
        "propID": 52013039
    }),
    1771: _tools.RODict({
        "ID": 1771,
        "equipmentID": 80423001,
        "strengthen": 3,
        "propID": 52013040
    }),
    1772: _tools.RODict({
        "ID": 1772,
        "equipmentID": 80423001,
        "strengthen": 4,
        "propID": 52013041
    }),
    1773: _tools.RODict({
        "ID": 1773,
        "equipmentID": 80424001,
        "strengthen": 1,
        "propID": 52013042
    }),
    1774: _tools.RODict({
        "ID": 1774,
        "equipmentID": 80424001,
        "strengthen": 2,
        "propID": 52013043
    }),
    1775: _tools.RODict({
        "ID": 1775,
        "equipmentID": 80424001,
        "strengthen": 3,
        "propID": 52013044
    }),
    1776: _tools.RODict({
        "ID": 1776,
        "equipmentID": 80424001,
        "strengthen": 4,
        "propID": 52013045
    }),
    1937: _tools.RODict({
        "ID": 1937,
        "equipmentID": 80431001,
        "strengthen": 1,
        "propID": 52013030
    }),
    1938: _tools.RODict({
        "ID": 1938,
        "equipmentID": 80431001,
        "strengthen": 2,
        "propID": 52013031
    }),
    1939: _tools.RODict({
        "ID": 1939,
        "equipmentID": 80431001,
        "strengthen": 3,
        "propID": 52013032
    }),
    1940: _tools.RODict({
        "ID": 1940,
        "equipmentID": 80431001,
        "strengthen": 4,
        "propID": 52013033
    }),
    1941: _tools.RODict({
        "ID": 1941,
        "equipmentID": 80432001,
        "strengthen": 1,
        "propID": 52013034
    }),
    1942: _tools.RODict({
        "ID": 1942,
        "equipmentID": 80432001,
        "strengthen": 2,
        "propID": 52013035
    }),
    1943: _tools.RODict({
        "ID": 1943,
        "equipmentID": 80432001,
        "strengthen": 3,
        "propID": 52013036
    }),
    1944: _tools.RODict({
        "ID": 1944,
        "equipmentID": 80432001,
        "strengthen": 4,
        "propID": 52013037
    }),
    1945: _tools.RODict({
        "ID": 1945,
        "equipmentID": 80433001,
        "strengthen": 1,
        "propID": 52013038
    }),
    1946: _tools.RODict({
        "ID": 1946,
        "equipmentID": 80433001,
        "strengthen": 2,
        "propID": 52013039
    }),
    1947: _tools.RODict({
        "ID": 1947,
        "equipmentID": 80433001,
        "strengthen": 3,
        "propID": 52013040
    }),
    1948: _tools.RODict({
        "ID": 1948,
        "equipmentID": 80433001,
        "strengthen": 4,
        "propID": 52013041
    }),
    1949: _tools.RODict({
        "ID": 1949,
        "equipmentID": 80434001,
        "strengthen": 1,
        "propID": 52013042
    }),
    1950: _tools.RODict({
        "ID": 1950,
        "equipmentID": 80434001,
        "strengthen": 2,
        "propID": 52013043
    }),
    1951: _tools.RODict({
        "ID": 1951,
        "equipmentID": 80434001,
        "strengthen": 3,
        "propID": 52013044
    }),
    1952: _tools.RODict({
        "ID": 1952,
        "equipmentID": 80434001,
        "strengthen": 4,
        "propID": 52013045
    }),
    2113: _tools.RODict({
        "ID": 2113,
        "equipmentID": 80581001,
        "strengthen": 1,
        "propID": 52013206
    }),
    2114: _tools.RODict({
        "ID": 2114,
        "equipmentID": 80581001,
        "strengthen": 2,
        "propID": 52013207
    }),
    2115: _tools.RODict({
        "ID": 2115,
        "equipmentID": 80581001,
        "strengthen": 3,
        "propID": 52013208
    }),
    2116: _tools.RODict({
        "ID": 2116,
        "equipmentID": 80581001,
        "strengthen": 4,
        "propID": 52013209
    }),
    2117: _tools.RODict({
        "ID": 2117,
        "equipmentID": 80582001,
        "strengthen": 1,
        "propID": 52013210
    }),
    2118: _tools.RODict({
        "ID": 2118,
        "equipmentID": 80582001,
        "strengthen": 2,
        "propID": 52013211
    }),
    2119: _tools.RODict({
        "ID": 2119,
        "equipmentID": 80582001,
        "strengthen": 3,
        "propID": 52013212
    }),
    2120: _tools.RODict({
        "ID": 2120,
        "equipmentID": 80582001,
        "strengthen": 4,
        "propID": 52013213
    }),
    2121: _tools.RODict({
        "ID": 2121,
        "equipmentID": 80583001,
        "strengthen": 1,
        "propID": 52013214
    }),
    2122: _tools.RODict({
        "ID": 2122,
        "equipmentID": 80583001,
        "strengthen": 2,
        "propID": 52013215
    }),
    2123: _tools.RODict({
        "ID": 2123,
        "equipmentID": 80583001,
        "strengthen": 3,
        "propID": 52013216
    }),
    2124: _tools.RODict({
        "ID": 2124,
        "equipmentID": 80583001,
        "strengthen": 4,
        "propID": 52013217
    }),
    2125: _tools.RODict({
        "ID": 2125,
        "equipmentID": 80584001,
        "strengthen": 1,
        "propID": 52013218
    }),
    2126: _tools.RODict({
        "ID": 2126,
        "equipmentID": 80584001,
        "strengthen": 2,
        "propID": 52013219
    }),
    2127: _tools.RODict({
        "ID": 2127,
        "equipmentID": 80584001,
        "strengthen": 3,
        "propID": 52013220
    }),
    2128: _tools.RODict({
        "ID": 2128,
        "equipmentID": 80584001,
        "strengthen": 4,
        "propID": 52013221
    }),
    2289: _tools.RODict({
        "ID": 2289,
        "equipmentID": 80591001,
        "strengthen": 1,
        "propID": 52013382
    }),
    2290: _tools.RODict({
        "ID": 2290,
        "equipmentID": 80591001,
        "strengthen": 2,
        "propID": 52013383
    }),
    2291: _tools.RODict({
        "ID": 2291,
        "equipmentID": 80591001,
        "strengthen": 3,
        "propID": 52013384
    }),
    2292: _tools.RODict({
        "ID": 2292,
        "equipmentID": 80591001,
        "strengthen": 4,
        "propID": 52013385
    }),
    2293: _tools.RODict({
        "ID": 2293,
        "equipmentID": 80592001,
        "strengthen": 1,
        "propID": 52013386
    }),
    2294: _tools.RODict({
        "ID": 2294,
        "equipmentID": 80592001,
        "strengthen": 2,
        "propID": 52013387
    }),
    2295: _tools.RODict({
        "ID": 2295,
        "equipmentID": 80592001,
        "strengthen": 3,
        "propID": 52013388
    }),
    2296: _tools.RODict({
        "ID": 2296,
        "equipmentID": 80592001,
        "strengthen": 4,
        "propID": 52013389
    }),
    2297: _tools.RODict({
        "ID": 2297,
        "equipmentID": 80593001,
        "strengthen": 1,
        "propID": 52013390
    }),
    2298: _tools.RODict({
        "ID": 2298,
        "equipmentID": 80593001,
        "strengthen": 2,
        "propID": 52013391
    }),
    2299: _tools.RODict({
        "ID": 2299,
        "equipmentID": 80593001,
        "strengthen": 3,
        "propID": 52013392
    }),
    2300: _tools.RODict({
        "ID": 2300,
        "equipmentID": 80593001,
        "strengthen": 4,
        "propID": 52013393
    }),
    2301: _tools.RODict({
        "ID": 2301,
        "equipmentID": 80594001,
        "strengthen": 1,
        "propID": 52013394
    }),
    2302: _tools.RODict({
        "ID": 2302,
        "equipmentID": 80594001,
        "strengthen": 2,
        "propID": 52013395
    }),
    2303: _tools.RODict({
        "ID": 2303,
        "equipmentID": 80594001,
        "strengthen": 3,
        "propID": 52013396
    }),
    2304: _tools.RODict({
        "ID": 2304,
        "equipmentID": 80594001,
        "strengthen": 4,
        "propID": 52013397
    }),
    2465: _tools.RODict({
        "ID": 2465,
        "equipmentID": 80681001,
        "strengthen": 1,
        "propID": 52013558
    }),
    2466: _tools.RODict({
        "ID": 2466,
        "equipmentID": 80681001,
        "strengthen": 2,
        "propID": 52013559
    }),
    2467: _tools.RODict({
        "ID": 2467,
        "equipmentID": 80681001,
        "strengthen": 3,
        "propID": 52013560
    }),
    2468: _tools.RODict({
        "ID": 2468,
        "equipmentID": 80681001,
        "strengthen": 4,
        "propID": 52013561
    }),
    2469: _tools.RODict({
        "ID": 2469,
        "equipmentID": 80682001,
        "strengthen": 1,
        "propID": 52013562
    }),
    2470: _tools.RODict({
        "ID": 2470,
        "equipmentID": 80682001,
        "strengthen": 2,
        "propID": 52013563
    }),
    2471: _tools.RODict({
        "ID": 2471,
        "equipmentID": 80682001,
        "strengthen": 3,
        "propID": 52013564
    }),
    2472: _tools.RODict({
        "ID": 2472,
        "equipmentID": 80682001,
        "strengthen": 4,
        "propID": 52013565
    }),
    2473: _tools.RODict({
        "ID": 2473,
        "equipmentID": 80683001,
        "strengthen": 1,
        "propID": 52013566
    }),
    2474: _tools.RODict({
        "ID": 2474,
        "equipmentID": 80683001,
        "strengthen": 2,
        "propID": 52013567
    }),
    2475: _tools.RODict({
        "ID": 2475,
        "equipmentID": 80683001,
        "strengthen": 3,
        "propID": 52013568
    }),
    2476: _tools.RODict({
        "ID": 2476,
        "equipmentID": 80683001,
        "strengthen": 4,
        "propID": 52013569
    }),
    2477: _tools.RODict({
        "ID": 2477,
        "equipmentID": 80684001,
        "strengthen": 1,
        "propID": 52013570
    }),
    2478: _tools.RODict({
        "ID": 2478,
        "equipmentID": 80684001,
        "strengthen": 2,
        "propID": 52013571
    }),
    2479: _tools.RODict({
        "ID": 2479,
        "equipmentID": 80684001,
        "strengthen": 3,
        "propID": 52013572
    }),
    2480: _tools.RODict({
        "ID": 2480,
        "equipmentID": 80684001,
        "strengthen": 4,
        "propID": 52013573
    }),
    2641: _tools.RODict({
        "ID": 2641,
        "equipmentID": 80691001,
        "strengthen": 1,
        "propID": 52013734
    }),
    2642: _tools.RODict({
        "ID": 2642,
        "equipmentID": 80691001,
        "strengthen": 2,
        "propID": 52013735
    }),
    2643: _tools.RODict({
        "ID": 2643,
        "equipmentID": 80691001,
        "strengthen": 3,
        "propID": 52013736
    }),
    2644: _tools.RODict({
        "ID": 2644,
        "equipmentID": 80691001,
        "strengthen": 4,
        "propID": 52013737
    }),
    2645: _tools.RODict({
        "ID": 2645,
        "equipmentID": 80692001,
        "strengthen": 1,
        "propID": 52013738
    }),
    2646: _tools.RODict({
        "ID": 2646,
        "equipmentID": 80692001,
        "strengthen": 2,
        "propID": 52013739
    }),
    2647: _tools.RODict({
        "ID": 2647,
        "equipmentID": 80692001,
        "strengthen": 3,
        "propID": 52013740
    }),
    2648: _tools.RODict({
        "ID": 2648,
        "equipmentID": 80692001,
        "strengthen": 4,
        "propID": 52013741
    }),
    2649: _tools.RODict({
        "ID": 2649,
        "equipmentID": 80693001,
        "strengthen": 1,
        "propID": 52013742
    }),
    2650: _tools.RODict({
        "ID": 2650,
        "equipmentID": 80693001,
        "strengthen": 2,
        "propID": 52013743
    }),
    2651: _tools.RODict({
        "ID": 2651,
        "equipmentID": 80693001,
        "strengthen": 3,
        "propID": 52013744
    }),
    2652: _tools.RODict({
        "ID": 2652,
        "equipmentID": 80693001,
        "strengthen": 4,
        "propID": 52013745
    }),
    2653: _tools.RODict({
        "ID": 2653,
        "equipmentID": 80694001,
        "strengthen": 1,
        "propID": 52013746
    }),
    2654: _tools.RODict({
        "ID": 2654,
        "equipmentID": 80694001,
        "strengthen": 2,
        "propID": 52013747
    }),
    2655: _tools.RODict({
        "ID": 2655,
        "equipmentID": 80694001,
        "strengthen": 3,
        "propID": 52013748
    }),
    2656: _tools.RODict({
        "ID": 2656,
        "equipmentID": 80694001,
        "strengthen": 4,
        "propID": 52013749
    }),
    2817: _tools.RODict({
        "ID": 2817,
        "equipmentID": 80781001,
        "strengthen": 1,
        "propID": 52013910
    }),
    2818: _tools.RODict({
        "ID": 2818,
        "equipmentID": 80781001,
        "strengthen": 2,
        "propID": 52013911
    }),
    2819: _tools.RODict({
        "ID": 2819,
        "equipmentID": 80781001,
        "strengthen": 3,
        "propID": 52013912
    }),
    2820: _tools.RODict({
        "ID": 2820,
        "equipmentID": 80781001,
        "strengthen": 4,
        "propID": 52013913
    }),
    2821: _tools.RODict({
        "ID": 2821,
        "equipmentID": 80782001,
        "strengthen": 1,
        "propID": 52013914
    }),
    2822: _tools.RODict({
        "ID": 2822,
        "equipmentID": 80782001,
        "strengthen": 2,
        "propID": 52013915
    }),
    2823: _tools.RODict({
        "ID": 2823,
        "equipmentID": 80782001,
        "strengthen": 3,
        "propID": 52013916
    }),
    2824: _tools.RODict({
        "ID": 2824,
        "equipmentID": 80782001,
        "strengthen": 4,
        "propID": 52013917
    }),
    2825: _tools.RODict({
        "ID": 2825,
        "equipmentID": 80783001,
        "strengthen": 1,
        "propID": 52013918
    }),
    2826: _tools.RODict({
        "ID": 2826,
        "equipmentID": 80783001,
        "strengthen": 2,
        "propID": 52013919
    }),
    2827: _tools.RODict({
        "ID": 2827,
        "equipmentID": 80783001,
        "strengthen": 3,
        "propID": 52013920
    }),
    2828: _tools.RODict({
        "ID": 2828,
        "equipmentID": 80783001,
        "strengthen": 4,
        "propID": 52013921
    }),
    2829: _tools.RODict({
        "ID": 2829,
        "equipmentID": 80784001,
        "strengthen": 1,
        "propID": 52013922
    }),
    2830: _tools.RODict({
        "ID": 2830,
        "equipmentID": 80784001,
        "strengthen": 2,
        "propID": 52013923
    }),
    2831: _tools.RODict({
        "ID": 2831,
        "equipmentID": 80784001,
        "strengthen": 3,
        "propID": 52013924
    }),
    2832: _tools.RODict({
        "ID": 2832,
        "equipmentID": 80784001,
        "strengthen": 4,
        "propID": 52013925
    }),
    2993: _tools.RODict({
        "ID": 2993,
        "equipmentID": 80791001,
        "strengthen": 1,
        "propID": 52014086
    }),
    2994: _tools.RODict({
        "ID": 2994,
        "equipmentID": 80791001,
        "strengthen": 2,
        "propID": 52014087
    }),
    2995: _tools.RODict({
        "ID": 2995,
        "equipmentID": 80791001,
        "strengthen": 3,
        "propID": 52014088
    }),
    2996: _tools.RODict({
        "ID": 2996,
        "equipmentID": 80791001,
        "strengthen": 4,
        "propID": 52014089
    }),
    2997: _tools.RODict({
        "ID": 2997,
        "equipmentID": 80792001,
        "strengthen": 1,
        "propID": 52014090
    }),
    2998: _tools.RODict({
        "ID": 2998,
        "equipmentID": 80792001,
        "strengthen": 2,
        "propID": 52014091
    }),
    2999: _tools.RODict({
        "ID": 2999,
        "equipmentID": 80792001,
        "strengthen": 3,
        "propID": 52014092
    }),
    3000: _tools.RODict({
        "ID": 3000,
        "equipmentID": 80792001,
        "strengthen": 4,
        "propID": 52014093
    }),
    3001: _tools.RODict({
        "ID": 3001,
        "equipmentID": 80793001,
        "strengthen": 1,
        "propID": 52014094
    }),
    3002: _tools.RODict({
        "ID": 3002,
        "equipmentID": 80793001,
        "strengthen": 2,
        "propID": 52014095
    }),
    3003: _tools.RODict({
        "ID": 3003,
        "equipmentID": 80793001,
        "strengthen": 3,
        "propID": 52014096
    }),
    3004: _tools.RODict({
        "ID": 3004,
        "equipmentID": 80793001,
        "strengthen": 4,
        "propID": 52014097
    }),
    3005: _tools.RODict({
        "ID": 3005,
        "equipmentID": 80794001,
        "strengthen": 1,
        "propID": 52014098
    }),
    3006: _tools.RODict({
        "ID": 3006,
        "equipmentID": 80794001,
        "strengthen": 2,
        "propID": 52014099
    }),
    3007: _tools.RODict({
        "ID": 3007,
        "equipmentID": 80794001,
        "strengthen": 3,
        "propID": 52014100
    }),
    3008: _tools.RODict({
        "ID": 3008,
        "equipmentID": 80794001,
        "strengthen": 4,
        "propID": 52014101
    }),
    3169: _tools.RODict({
        "ID": 3169,
        "equipmentID": 80811001,
        "strengthen": 1,
        "propID": 52014262
    }),
    3170: _tools.RODict({
        "ID": 3170,
        "equipmentID": 80811001,
        "strengthen": 2,
        "propID": 52014263
    }),
    3171: _tools.RODict({
        "ID": 3171,
        "equipmentID": 80811001,
        "strengthen": 3,
        "propID": 52014264
    }),
    3172: _tools.RODict({
        "ID": 3172,
        "equipmentID": 80811001,
        "strengthen": 4,
        "propID": 52014265
    }),
    3173: _tools.RODict({
        "ID": 3173,
        "equipmentID": 80812001,
        "strengthen": 1,
        "propID": 52014266
    }),
    3174: _tools.RODict({
        "ID": 3174,
        "equipmentID": 80812001,
        "strengthen": 2,
        "propID": 52014267
    }),
    3175: _tools.RODict({
        "ID": 3175,
        "equipmentID": 80812001,
        "strengthen": 3,
        "propID": 52014268
    }),
    3176: _tools.RODict({
        "ID": 3176,
        "equipmentID": 80812001,
        "strengthen": 4,
        "propID": 52014269
    }),
    3177: _tools.RODict({
        "ID": 3177,
        "equipmentID": 80813001,
        "strengthen": 1,
        "propID": 52014270
    }),
    3178: _tools.RODict({
        "ID": 3178,
        "equipmentID": 80813001,
        "strengthen": 2,
        "propID": 52014271
    }),
    3179: _tools.RODict({
        "ID": 3179,
        "equipmentID": 80813001,
        "strengthen": 3,
        "propID": 52014272
    }),
    3180: _tools.RODict({
        "ID": 3180,
        "equipmentID": 80813001,
        "strengthen": 4,
        "propID": 52014273
    }),
    3181: _tools.RODict({
        "ID": 3181,
        "equipmentID": 80814001,
        "strengthen": 1,
        "propID": 52014274
    }),
    3182: _tools.RODict({
        "ID": 3182,
        "equipmentID": 80814001,
        "strengthen": 2,
        "propID": 52014275
    }),
    3183: _tools.RODict({
        "ID": 3183,
        "equipmentID": 80814001,
        "strengthen": 3,
        "propID": 52014276
    }),
    3184: _tools.RODict({
        "ID": 3184,
        "equipmentID": 80814001,
        "strengthen": 4,
        "propID": 52014277
    }),
    3345: _tools.RODict({
        "ID": 3345,
        "equipmentID": 80821001,
        "strengthen": 1,
        "propID": 52014262
    }),
    3346: _tools.RODict({
        "ID": 3346,
        "equipmentID": 80821001,
        "strengthen": 2,
        "propID": 52014263
    }),
    3347: _tools.RODict({
        "ID": 3347,
        "equipmentID": 80821001,
        "strengthen": 3,
        "propID": 52014264
    }),
    3348: _tools.RODict({
        "ID": 3348,
        "equipmentID": 80821001,
        "strengthen": 4,
        "propID": 52014265
    }),
    3349: _tools.RODict({
        "ID": 3349,
        "equipmentID": 80822001,
        "strengthen": 1,
        "propID": 52014266
    }),
    3350: _tools.RODict({
        "ID": 3350,
        "equipmentID": 80822001,
        "strengthen": 2,
        "propID": 52014267
    }),
    3351: _tools.RODict({
        "ID": 3351,
        "equipmentID": 80822001,
        "strengthen": 3,
        "propID": 52014268
    }),
    3352: _tools.RODict({
        "ID": 3352,
        "equipmentID": 80822001,
        "strengthen": 4,
        "propID": 52014269
    }),
    3353: _tools.RODict({
        "ID": 3353,
        "equipmentID": 80823001,
        "strengthen": 1,
        "propID": 52014270
    }),
    3354: _tools.RODict({
        "ID": 3354,
        "equipmentID": 80823001,
        "strengthen": 2,
        "propID": 52014271
    }),
    3355: _tools.RODict({
        "ID": 3355,
        "equipmentID": 80823001,
        "strengthen": 3,
        "propID": 52014272
    }),
    3356: _tools.RODict({
        "ID": 3356,
        "equipmentID": 80823001,
        "strengthen": 4,
        "propID": 52014273
    }),
    3357: _tools.RODict({
        "ID": 3357,
        "equipmentID": 80824001,
        "strengthen": 1,
        "propID": 52014274
    }),
    3358: _tools.RODict({
        "ID": 3358,
        "equipmentID": 80824001,
        "strengthen": 2,
        "propID": 52014275
    }),
    3359: _tools.RODict({
        "ID": 3359,
        "equipmentID": 80824001,
        "strengthen": 3,
        "propID": 52014276
    }),
    3360: _tools.RODict({
        "ID": 3360,
        "equipmentID": 80824001,
        "strengthen": 4,
        "propID": 52014277
    }),
    3521: _tools.RODict({
        "ID": 3521,
        "equipmentID": 80831001,
        "strengthen": 1,
        "propID": 52014262
    }),
    3522: _tools.RODict({
        "ID": 3522,
        "equipmentID": 80831001,
        "strengthen": 2,
        "propID": 52014263
    }),
    3523: _tools.RODict({
        "ID": 3523,
        "equipmentID": 80831001,
        "strengthen": 3,
        "propID": 52014264
    }),
    3524: _tools.RODict({
        "ID": 3524,
        "equipmentID": 80831001,
        "strengthen": 4,
        "propID": 52014265
    }),
    3525: _tools.RODict({
        "ID": 3525,
        "equipmentID": 80832001,
        "strengthen": 1,
        "propID": 52014266
    }),
    3526: _tools.RODict({
        "ID": 3526,
        "equipmentID": 80832001,
        "strengthen": 2,
        "propID": 52014267
    }),
    3527: _tools.RODict({
        "ID": 3527,
        "equipmentID": 80832001,
        "strengthen": 3,
        "propID": 52014268
    }),
    3528: _tools.RODict({
        "ID": 3528,
        "equipmentID": 80832001,
        "strengthen": 4,
        "propID": 52014269
    }),
    3529: _tools.RODict({
        "ID": 3529,
        "equipmentID": 80833001,
        "strengthen": 1,
        "propID": 52014270
    }),
    3530: _tools.RODict({
        "ID": 3530,
        "equipmentID": 80833001,
        "strengthen": 2,
        "propID": 52014271
    }),
    3531: _tools.RODict({
        "ID": 3531,
        "equipmentID": 80833001,
        "strengthen": 3,
        "propID": 52014272
    }),
    3532: _tools.RODict({
        "ID": 3532,
        "equipmentID": 80833001,
        "strengthen": 4,
        "propID": 52014273
    }),
    3533: _tools.RODict({
        "ID": 3533,
        "equipmentID": 80834001,
        "strengthen": 1,
        "propID": 52014274
    }),
    3534: _tools.RODict({
        "ID": 3534,
        "equipmentID": 80834001,
        "strengthen": 2,
        "propID": 52014275
    }),
    3535: _tools.RODict({
        "ID": 3535,
        "equipmentID": 80834001,
        "strengthen": 3,
        "propID": 52014276
    }),
    3536: _tools.RODict({
        "ID": 3536,
        "equipmentID": 80834001,
        "strengthen": 4,
        "propID": 52014277
    })
})
minKey = 1
maxKey = 3536

attributeDic = {8011100101: 52012150, 8011100102: 52012151, 8011100103: 52012152, 8011100104: 52012153, 8011200101: 52012154, 8011200102: 52012155, 8011200103: 52012156, 8011200104: 52012157, 8011300101: 52012158, 8011300102: 52012159, 8011300103: 52012160, 8011300104: 52012161, 8011400101: 52012162, 8011400102: 52012163, 8011400103: 52012164, 8011400104: 52012165, 8012100101: 52012326, 8012100102: 52012327, 8012100103: 52012328, 8012100104: 52012329, 8012200101: 52012330, 8012200102: 52012331, 8012200103: 52012332, 8012200104: 52012333, 8012300101: 52012334, 8012300102: 52012335, 8012300103: 52012336, 8012300104: 52012337, 8012400101: 52012338, 8012400102: 52012339, 8012400103: 52012340, 8012400104: 52012341, 8013100101: 52012502, 8013100102: 52012503, 8013100103: 52012504, 8013100104: 52012505, 8013200101: 52012506, 8013200102: 52012507, 8013200103: 52012508, 8013200104: 52012509, 8013300101: 52012510, 8013300102: 52012511, 8013300103: 52012512, 8013300104: 52012513, 8013400101: 52012514, 8013400102: 52012515, 8013400103: 52012516, 8013400104: 52012517, 8021100101: 52012678, 8021100102: 52012679, 8021100103: 52012680, 8021100104: 52012681, 8021200101: 52012682, 8021200102: 52012683, 8021200103: 52012684, 8021200104: 52012685, 8021300101: 52012686, 8021300102: 52012687, 8021300103: 52012688, 8021300104: 52012689, 8021400101: 52012690, 8021400102: 52012691, 8021400103: 52012692, 8021400104: 52012693, 8022100101: 52012678, 8022100102: 52012679, 8022100103: 52012680, 8022100104: 52012681, 8022200101: 52012682, 8022200102: 52012683, 8022200103: 52012684, 8022200104: 52012685, 8022300101: 52012686, 8022300102: 52012687, 8022300103: 52012688, 8022300104: 52012689, 8022400101: 52012690, 8022400102: 52012691, 8022400103: 52012692, 8022400104: 52012693, 8023100101: 52012678, 8023100102: 52012679, 8023100103: 52012680, 8023100104: 52012681, 8023200101: 52012682, 8023200102: 52012683, 8023200103: 52012684, 8023200104: 52012685, 8023300101: 52012686, 8023300102: 52012687, 8023300103: 52012688, 8023300104: 52012689, 8023400101: 52012690, 8023400102: 52012691, 8023400103: 52012692, 8023400104: 52012693, 8031100101: 52012854, 8031100102: 52012855, 8031100103: 52012856, 8031100104: 52012857, 8031200101: 52012858, 8031200102: 52012859, 8031200103: 52012860, 8031200104: 52012861, 8031300101: 52012862, 8031300102: 52012863, 8031300103: 52012864, 8031300104: 52012865, 8031400101: 52012866, 8031400102: 52012867, 8031400103: 52012868, 8031400104: 52012869, 8032100101: 52012854, 8032100102: 52012855, 8032100103: 52012856, 8032100104: 52012857, 8032200101: 52012858, 8032200102: 52012859, 8032200103: 52012860, 8032200104: 52012861, 8032300101: 52012862, 8032300102: 52012863, 8032300103: 52012864, 8032300104: 52012865, 8032400101: 52012866, 8032400102: 52012867, 8032400103: 52012868, 8032400104: 52012869, 8033100101: 52012854, 8033100102: 52012855, 8033100103: 52012856, 8033100104: 52012857, 8033200101: 52012858, 8033200102: 52012859, 8033200103: 52012860, 8033200104: 52012861, 8033300101: 52012862, 8033300102: 52012863, 8033300103: 52012864, 8033300104: 52012865, 8033400101: 52012866, 8033400102: 52012867, 8033400103: 52012868, 8033400104: 52012869, 8041100101: 52013030, 8041100102: 52013031, 8041100103: 52013032, 8041100104: 52013033, 8041200101: 52013034, 8041200102: 52013035, 8041200103: 52013036, 8041200104: 52013037, 8041300101: 52013038, 8041300102: 52013039, 8041300103: 52013040, 8041300104: 52013041, 8041400101: 52013042, 8041400102: 52013043, 8041400103: 52013044, 8041400104: 52013045, 8042100101: 52013030, 8042100102: 52013031, 8042100103: 52013032, 8042100104: 52013033, 8042200101: 52013034, 8042200102: 52013035, 8042200103: 52013036, 8042200104: 52013037, 8042300101: 52013038, 8042300102: 52013039, 8042300103: 52013040, 8042300104: 52013041, 8042400101: 52013042, 8042400102: 52013043, 8042400103: 52013044, 8042400104: 52013045, 8043100101: 52013030, 8043100102: 52013031, 8043100103: 52013032, 8043100104: 52013033, 8043200101: 52013034, 8043200102: 52013035, 8043200103: 52013036, 8043200104: 52013037, 8043300101: 52013038, 8043300102: 52013039, 8043300103: 52013040, 8043300104: 52013041, 8043400101: 52013042, 8043400102: 52013043, 8043400103: 52013044, 8043400104: 52013045, 8058100101: 52013206, 8058100102: 52013207, 8058100103: 52013208, 8058100104: 52013209, 8058200101: 52013210, 8058200102: 52013211, 8058200103: 52013212, 8058200104: 52013213, 8058300101: 52013214, 8058300102: 52013215, 8058300103: 52013216, 8058300104: 52013217, 8058400101: 52013218, 8058400102: 52013219, 8058400103: 52013220, 8058400104: 52013221, 8059100101: 52013382, 8059100102: 52013383, 8059100103: 52013384, 8059100104: 52013385, 8059200101: 52013386, 8059200102: 52013387, 8059200103: 52013388, 8059200104: 52013389, 8059300101: 52013390, 8059300102: 52013391, 8059300103: 52013392, 8059300104: 52013393, 8059400101: 52013394, 8059400102: 52013395, 8059400103: 52013396, 8059400104: 52013397, 8068100101: 52013558, 8068100102: 52013559, 8068100103: 52013560, 8068100104: 52013561, 8068200101: 52013562, 8068200102: 52013563, 8068200103: 52013564, 8068200104: 52013565, 8068300101: 52013566, 8068300102: 52013567, 8068300103: 52013568, 8068300104: 52013569, 8068400101: 52013570, 8068400102: 52013571, 8068400103: 52013572, 8068400104: 52013573, 8069100101: 52013734, 8069100102: 52013735, 8069100103: 52013736, 8069100104: 52013737, 8069200101: 52013738, 8069200102: 52013739, 8069200103: 52013740, 8069200104: 52013741, 8069300101: 52013742, 8069300102: 52013743, 8069300103: 52013744, 8069300104: 52013745, 8069400101: 52013746, 8069400102: 52013747, 8069400103: 52013748, 8069400104: 52013749, 8078100101: 52013910, 8078100102: 52013911, 8078100103: 52013912, 8078100104: 52013913, 8078200101: 52013914, 8078200102: 52013915, 8078200103: 52013916, 8078200104: 52013917, 8078300101: 52013918, 8078300102: 52013919, 8078300103: 52013920, 8078300104: 52013921, 8078400101: 52013922, 8078400102: 52013923, 8078400103: 52013924, 8078400104: 52013925, 8079100101: 52014086, 8079100102: 52014087, 8079100103: 52014088, 8079100104: 52014089, 8079200101: 52014090, 8079200102: 52014091, 8079200103: 52014092, 8079200104: 52014093, 8079300101: 52014094, 8079300102: 52014095, 8079300103: 52014096, 8079300104: 52014097, 8079400101: 52014098, 8079400102: 52014099, 8079400103: 52014100, 8079400104: 52014101, 8081100101: 52014262, 8081100102: 52014263, 8081100103: 52014264, 8081100104: 52014265, 8081200101: 52014266, 8081200102: 52014267, 8081200103: 52014268, 8081200104: 52014269, 8081300101: 52014270, 8081300102: 52014271, 8081300103: 52014272, 8081300104: 52014273, 8081400101: 52014274, 8081400102: 52014275, 8081400103: 52014276, 8081400104: 52014277, 8082100101: 52014262, 8082100102: 52014263, 8082100103: 52014264, 8082100104: 52014265, 8082200101: 52014266, 8082200102: 52014267, 8082200103: 52014268, 8082200104: 52014269, 8082300101: 52014270, 8082300102: 52014271, 8082300103: 52014272, 8082300104: 52014273, 8082400101: 52014274, 8082400102: 52014275, 8082400103: 52014276, 8082400104: 52014277, 8083100101: 52014262, 8083100102: 52014263, 8083100103: 52014264, 8083100104: 52014265, 8083200101: 52014266, 8083200102: 52014267, 8083200103: 52014268, 8083200104: 52014269, 8083300101: 52014270, 8083300102: 52014271, 8083300103: 52014272, 8083300104: 52014273, 8083400101: 52014274, 8083400102: 52014275, 8083400103: 52014276, 8083400104: 52014277}

