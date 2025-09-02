# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/equipmentAssessment
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    2121: _tools.RODict({
        "ID": 2121,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2122: _tools.RODict({
        "ID": 2122,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2123: _tools.RODict({
        "ID": 2123,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2124: _tools.RODict({
        "ID": 2124,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2131: _tools.RODict({
        "ID": 2131,
        "consumedGear": ((80212001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2132: _tools.RODict({
        "ID": 2132,
        "consumedGear": ((80212002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2133: _tools.RODict({
        "ID": 2133,
        "consumedGear": ((80212003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2134: _tools.RODict({
        "ID": 2134,
        "consumedGear": ((80212004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2141: _tools.RODict({
        "ID": 2141,
        "consumedGear": ((80213001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2142: _tools.RODict({
        "ID": 2142,
        "consumedGear": ((80213002, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2143: _tools.RODict({
        "ID": 2143,
        "consumedGear": ((80213003, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2144: _tools.RODict({
        "ID": 2144,
        "consumedGear": ((80213004, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2221: _tools.RODict({
        "ID": 2221,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2222: _tools.RODict({
        "ID": 2222,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2223: _tools.RODict({
        "ID": 2223,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2224: _tools.RODict({
        "ID": 2224,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2231: _tools.RODict({
        "ID": 2231,
        "consumedGear": ((80222001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2232: _tools.RODict({
        "ID": 2232,
        "consumedGear": ((80222002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2233: _tools.RODict({
        "ID": 2233,
        "consumedGear": ((80222003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2234: _tools.RODict({
        "ID": 2234,
        "consumedGear": ((80222004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2241: _tools.RODict({
        "ID": 2241,
        "consumedGear": ((80223001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2242: _tools.RODict({
        "ID": 2242,
        "consumedGear": ((80223002, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2243: _tools.RODict({
        "ID": 2243,
        "consumedGear": ((80223003, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2244: _tools.RODict({
        "ID": 2244,
        "consumedGear": ((80223004, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2321: _tools.RODict({
        "ID": 2321,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2322: _tools.RODict({
        "ID": 2322,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2323: _tools.RODict({
        "ID": 2323,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2324: _tools.RODict({
        "ID": 2324,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    2331: _tools.RODict({
        "ID": 2331,
        "consumedGear": ((80232001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2332: _tools.RODict({
        "ID": 2332,
        "consumedGear": ((80232002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2333: _tools.RODict({
        "ID": 2333,
        "consumedGear": ((80232003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2334: _tools.RODict({
        "ID": 2334,
        "consumedGear": ((80232004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    2341: _tools.RODict({
        "ID": 2341,
        "consumedGear": ((80233001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2342: _tools.RODict({
        "ID": 2342,
        "consumedGear": ((80233002, 1),),
        "consumedItem": ((30000270, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2343: _tools.RODict({
        "ID": 2343,
        "consumedGear": ((80233003, 1),),
        "consumedItem": ((30000270, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    2344: _tools.RODict({
        "ID": 2344,
        "consumedGear": ((80233004, 1),),
        "consumedItem": ((30000270, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3121: _tools.RODict({
        "ID": 3121,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3122: _tools.RODict({
        "ID": 3122,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3123: _tools.RODict({
        "ID": 3123,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3124: _tools.RODict({
        "ID": 3124,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3131: _tools.RODict({
        "ID": 3131,
        "consumedGear": ((80312001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3132: _tools.RODict({
        "ID": 3132,
        "consumedGear": ((80312002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3133: _tools.RODict({
        "ID": 3133,
        "consumedGear": ((80312003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3134: _tools.RODict({
        "ID": 3134,
        "consumedGear": ((80312004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3141: _tools.RODict({
        "ID": 3141,
        "consumedGear": ((80313001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3142: _tools.RODict({
        "ID": 3142,
        "consumedGear": ((80313002, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3143: _tools.RODict({
        "ID": 3143,
        "consumedGear": ((80313003, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3144: _tools.RODict({
        "ID": 3144,
        "consumedGear": ((80313004, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3221: _tools.RODict({
        "ID": 3221,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3222: _tools.RODict({
        "ID": 3222,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3223: _tools.RODict({
        "ID": 3223,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3224: _tools.RODict({
        "ID": 3224,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3231: _tools.RODict({
        "ID": 3231,
        "consumedGear": ((80322001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3232: _tools.RODict({
        "ID": 3232,
        "consumedGear": ((80322002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3233: _tools.RODict({
        "ID": 3233,
        "consumedGear": ((80322003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3234: _tools.RODict({
        "ID": 3234,
        "consumedGear": ((80322004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3241: _tools.RODict({
        "ID": 3241,
        "consumedGear": ((80323001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3242: _tools.RODict({
        "ID": 3242,
        "consumedGear": ((80323002, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3243: _tools.RODict({
        "ID": 3243,
        "consumedGear": ((80323003, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3244: _tools.RODict({
        "ID": 3244,
        "consumedGear": ((80323004, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3321: _tools.RODict({
        "ID": 3321,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3322: _tools.RODict({
        "ID": 3322,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3323: _tools.RODict({
        "ID": 3323,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3324: _tools.RODict({
        "ID": 3324,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    3331: _tools.RODict({
        "ID": 3331,
        "consumedGear": ((80332001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3332: _tools.RODict({
        "ID": 3332,
        "consumedGear": ((80332002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3333: _tools.RODict({
        "ID": 3333,
        "consumedGear": ((80332003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3334: _tools.RODict({
        "ID": 3334,
        "consumedGear": ((80332004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    3341: _tools.RODict({
        "ID": 3341,
        "consumedGear": ((80333001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3342: _tools.RODict({
        "ID": 3342,
        "consumedGear": ((80333002, 1),),
        "consumedItem": ((30000270, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3343: _tools.RODict({
        "ID": 3343,
        "consumedGear": ((80333003, 1),),
        "consumedItem": ((30000270, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    3344: _tools.RODict({
        "ID": 3344,
        "consumedGear": ((80333004, 1),),
        "consumedItem": ((30000270, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4121: _tools.RODict({
        "ID": 4121,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4122: _tools.RODict({
        "ID": 4122,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4123: _tools.RODict({
        "ID": 4123,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4124: _tools.RODict({
        "ID": 4124,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4131: _tools.RODict({
        "ID": 4131,
        "consumedGear": ((80412001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4132: _tools.RODict({
        "ID": 4132,
        "consumedGear": ((80412002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4133: _tools.RODict({
        "ID": 4133,
        "consumedGear": ((80412003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4134: _tools.RODict({
        "ID": 4134,
        "consumedGear": ((80412004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4141: _tools.RODict({
        "ID": 4141,
        "consumedGear": ((80413001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4142: _tools.RODict({
        "ID": 4142,
        "consumedGear": ((80413002, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4143: _tools.RODict({
        "ID": 4143,
        "consumedGear": ((80413003, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4144: _tools.RODict({
        "ID": 4144,
        "consumedGear": ((80413004, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4221: _tools.RODict({
        "ID": 4221,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4222: _tools.RODict({
        "ID": 4222,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4223: _tools.RODict({
        "ID": 4223,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4224: _tools.RODict({
        "ID": 4224,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4231: _tools.RODict({
        "ID": 4231,
        "consumedGear": ((80422001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4232: _tools.RODict({
        "ID": 4232,
        "consumedGear": ((80422002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4233: _tools.RODict({
        "ID": 4233,
        "consumedGear": ((80422003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4234: _tools.RODict({
        "ID": 4234,
        "consumedGear": ((80422004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4241: _tools.RODict({
        "ID": 4241,
        "consumedGear": ((80423001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4242: _tools.RODict({
        "ID": 4242,
        "consumedGear": ((80423002, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4243: _tools.RODict({
        "ID": 4243,
        "consumedGear": ((80423003, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4244: _tools.RODict({
        "ID": 4244,
        "consumedGear": ((80423004, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4321: _tools.RODict({
        "ID": 4321,
        "consumedGear": None,
        "consumedItem": ((30000264, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4322: _tools.RODict({
        "ID": 4322,
        "consumedGear": None,
        "consumedItem": ((30000264, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4323: _tools.RODict({
        "ID": 4323,
        "consumedGear": None,
        "consumedItem": ((30000264, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4324: _tools.RODict({
        "ID": 4324,
        "consumedGear": None,
        "consumedItem": ((30000264, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    4331: _tools.RODict({
        "ID": 4331,
        "consumedGear": ((80432001, 1),),
        "consumedItem": ((30000267, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4332: _tools.RODict({
        "ID": 4332,
        "consumedGear": ((80432002, 1),),
        "consumedItem": ((30000267, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4333: _tools.RODict({
        "ID": 4333,
        "consumedGear": ((80432003, 1),),
        "consumedItem": ((30000267, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4334: _tools.RODict({
        "ID": 4334,
        "consumedGear": ((80432004, 1),),
        "consumedItem": ((30000267, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    4341: _tools.RODict({
        "ID": 4341,
        "consumedGear": ((80433001, 1),),
        "consumedItem": ((30000270, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4342: _tools.RODict({
        "ID": 4342,
        "consumedGear": ((80433002, 1),),
        "consumedItem": ((30000270, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4343: _tools.RODict({
        "ID": 4343,
        "consumedGear": ((80433003, 1),),
        "consumedItem": ((30000270, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    4344: _tools.RODict({
        "ID": 4344,
        "consumedGear": ((80433004, 1),),
        "consumedItem": ((30000270, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    5821: _tools.RODict({
        "ID": 5821,
        "consumedGear": None,
        "consumedItem": ((30000265, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    5822: _tools.RODict({
        "ID": 5822,
        "consumedGear": None,
        "consumedItem": ((30000265, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    5823: _tools.RODict({
        "ID": 5823,
        "consumedGear": None,
        "consumedItem": ((30000265, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    5824: _tools.RODict({
        "ID": 5824,
        "consumedGear": None,
        "consumedItem": ((30000265, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    5831: _tools.RODict({
        "ID": 5831,
        "consumedGear": ((80582001, 1),),
        "consumedItem": ((30000268, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    5832: _tools.RODict({
        "ID": 5832,
        "consumedGear": ((80582002, 1),),
        "consumedItem": ((30000268, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    5833: _tools.RODict({
        "ID": 5833,
        "consumedGear": ((80582003, 1),),
        "consumedItem": ((30000268, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    5834: _tools.RODict({
        "ID": 5834,
        "consumedGear": ((80582004, 1),),
        "consumedItem": ((30000268, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    5841: _tools.RODict({
        "ID": 5841,
        "consumedGear": ((80583001, 1),),
        "consumedItem": ((30000271, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    5842: _tools.RODict({
        "ID": 5842,
        "consumedGear": ((80583002, 1),),
        "consumedItem": ((30000271, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    5843: _tools.RODict({
        "ID": 5843,
        "consumedGear": ((80583003, 1),),
        "consumedItem": ((30000271, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    5844: _tools.RODict({
        "ID": 5844,
        "consumedGear": ((80583004, 1),),
        "consumedItem": ((30000271, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    5921: _tools.RODict({
        "ID": 5921,
        "consumedGear": None,
        "consumedItem": ((30000265, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    5922: _tools.RODict({
        "ID": 5922,
        "consumedGear": None,
        "consumedItem": ((30000265, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    5923: _tools.RODict({
        "ID": 5923,
        "consumedGear": None,
        "consumedItem": ((30000265, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    5924: _tools.RODict({
        "ID": 5924,
        "consumedGear": None,
        "consumedItem": ((30000265, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    5931: _tools.RODict({
        "ID": 5931,
        "consumedGear": ((80592001, 1),),
        "consumedItem": ((30000268, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    5932: _tools.RODict({
        "ID": 5932,
        "consumedGear": ((80592002, 1),),
        "consumedItem": ((30000268, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    5933: _tools.RODict({
        "ID": 5933,
        "consumedGear": ((80592003, 1),),
        "consumedItem": ((30000268, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    5934: _tools.RODict({
        "ID": 5934,
        "consumedGear": ((80592004, 1),),
        "consumedItem": ((30000268, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    5941: _tools.RODict({
        "ID": 5941,
        "consumedGear": ((80593001, 1),),
        "consumedItem": ((30000271, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    5942: _tools.RODict({
        "ID": 5942,
        "consumedGear": ((80593002, 1),),
        "consumedItem": ((30000271, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    5943: _tools.RODict({
        "ID": 5943,
        "consumedGear": ((80593003, 1),),
        "consumedItem": ((30000271, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    5944: _tools.RODict({
        "ID": 5944,
        "consumedGear": ((80593004, 1),),
        "consumedItem": ((30000271, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    6821: _tools.RODict({
        "ID": 6821,
        "consumedGear": None,
        "consumedItem": ((30000265, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    6822: _tools.RODict({
        "ID": 6822,
        "consumedGear": None,
        "consumedItem": ((30000265, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    6823: _tools.RODict({
        "ID": 6823,
        "consumedGear": None,
        "consumedItem": ((30000265, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    6824: _tools.RODict({
        "ID": 6824,
        "consumedGear": None,
        "consumedItem": ((30000265, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    6831: _tools.RODict({
        "ID": 6831,
        "consumedGear": ((80682001, 1),),
        "consumedItem": ((30000268, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    6832: _tools.RODict({
        "ID": 6832,
        "consumedGear": ((80682002, 1),),
        "consumedItem": ((30000268, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    6833: _tools.RODict({
        "ID": 6833,
        "consumedGear": ((80682003, 1),),
        "consumedItem": ((30000268, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    6834: _tools.RODict({
        "ID": 6834,
        "consumedGear": ((80682004, 1),),
        "consumedItem": ((30000268, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    6841: _tools.RODict({
        "ID": 6841,
        "consumedGear": ((80683001, 1),),
        "consumedItem": ((30000271, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    6842: _tools.RODict({
        "ID": 6842,
        "consumedGear": ((80683002, 1),),
        "consumedItem": ((30000271, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    6843: _tools.RODict({
        "ID": 6843,
        "consumedGear": ((80683003, 1),),
        "consumedItem": ((30000271, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    6844: _tools.RODict({
        "ID": 6844,
        "consumedGear": ((80683004, 1),),
        "consumedItem": ((30000271, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    6921: _tools.RODict({
        "ID": 6921,
        "consumedGear": None,
        "consumedItem": ((30000265, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    6922: _tools.RODict({
        "ID": 6922,
        "consumedGear": None,
        "consumedItem": ((30000265, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    6923: _tools.RODict({
        "ID": 6923,
        "consumedGear": None,
        "consumedItem": ((30000265, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    6924: _tools.RODict({
        "ID": 6924,
        "consumedGear": None,
        "consumedItem": ((30000265, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    6931: _tools.RODict({
        "ID": 6931,
        "consumedGear": ((80692001, 1),),
        "consumedItem": ((30000268, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    6932: _tools.RODict({
        "ID": 6932,
        "consumedGear": ((80692002, 1),),
        "consumedItem": ((30000268, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    6933: _tools.RODict({
        "ID": 6933,
        "consumedGear": ((80692003, 1),),
        "consumedItem": ((30000268, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    6934: _tools.RODict({
        "ID": 6934,
        "consumedGear": ((80692004, 1),),
        "consumedItem": ((30000268, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    6941: _tools.RODict({
        "ID": 6941,
        "consumedGear": ((80693001, 1),),
        "consumedItem": ((30000271, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    6942: _tools.RODict({
        "ID": 6942,
        "consumedGear": ((80693002, 1),),
        "consumedItem": ((30000271, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    6943: _tools.RODict({
        "ID": 6943,
        "consumedGear": ((80693003, 1),),
        "consumedItem": ((30000271, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    6944: _tools.RODict({
        "ID": 6944,
        "consumedGear": ((80693004, 1),),
        "consumedItem": ((30000271, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    7821: _tools.RODict({
        "ID": 7821,
        "consumedGear": None,
        "consumedItem": ((30000265, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    7822: _tools.RODict({
        "ID": 7822,
        "consumedGear": None,
        "consumedItem": ((30000265, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    7823: _tools.RODict({
        "ID": 7823,
        "consumedGear": None,
        "consumedItem": ((30000265, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    7824: _tools.RODict({
        "ID": 7824,
        "consumedGear": None,
        "consumedItem": ((30000265, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    7831: _tools.RODict({
        "ID": 7831,
        "consumedGear": ((80782001, 1),),
        "consumedItem": ((30000268, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    7832: _tools.RODict({
        "ID": 7832,
        "consumedGear": ((80782002, 1),),
        "consumedItem": ((30000268, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    7833: _tools.RODict({
        "ID": 7833,
        "consumedGear": ((80782003, 1),),
        "consumedItem": ((30000268, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    7834: _tools.RODict({
        "ID": 7834,
        "consumedGear": ((80782004, 1),),
        "consumedItem": ((30000268, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    7841: _tools.RODict({
        "ID": 7841,
        "consumedGear": ((80783001, 1),),
        "consumedItem": ((30000271, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    7842: _tools.RODict({
        "ID": 7842,
        "consumedGear": ((80783002, 1),),
        "consumedItem": ((30000271, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    7843: _tools.RODict({
        "ID": 7843,
        "consumedGear": ((80783003, 1),),
        "consumedItem": ((30000271, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    7844: _tools.RODict({
        "ID": 7844,
        "consumedGear": ((80783004, 1),),
        "consumedItem": ((30000271, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    7921: _tools.RODict({
        "ID": 7921,
        "consumedGear": None,
        "consumedItem": ((30000265, 1),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    7922: _tools.RODict({
        "ID": 7922,
        "consumedGear": None,
        "consumedItem": ((30000265, 2),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    7923: _tools.RODict({
        "ID": 7923,
        "consumedGear": None,
        "consumedItem": ((30000265, 3),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    7924: _tools.RODict({
        "ID": 7924,
        "consumedGear": None,
        "consumedItem": ((30000265, 4),),
        "spiritValue": 3,
        "consumedCoin": ((30000002, 200),),
        "consumedRune": ((30000312, 1),)
    }),
    7931: _tools.RODict({
        "ID": 7931,
        "consumedGear": ((80792001, 1),),
        "consumedItem": ((30000268, 1),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    7932: _tools.RODict({
        "ID": 7932,
        "consumedGear": ((80792002, 1),),
        "consumedItem": ((30000268, 2),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    7933: _tools.RODict({
        "ID": 7933,
        "consumedGear": ((80792003, 1),),
        "consumedItem": ((30000268, 3),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    7934: _tools.RODict({
        "ID": 7934,
        "consumedGear": ((80792004, 1),),
        "consumedItem": ((30000268, 4),),
        "spiritValue": 8,
        "consumedCoin": ((30000002, 500),),
        "consumedRune": ((30000312, 1),)
    }),
    7941: _tools.RODict({
        "ID": 7941,
        "consumedGear": ((80793001, 1),),
        "consumedItem": ((30000271, 1),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    7942: _tools.RODict({
        "ID": 7942,
        "consumedGear": ((80793002, 1),),
        "consumedItem": ((30000271, 2),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    7943: _tools.RODict({
        "ID": 7943,
        "consumedGear": ((80793003, 1),),
        "consumedItem": ((30000271, 3),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    }),
    7944: _tools.RODict({
        "ID": 7944,
        "consumedGear": ((80793004, 1),),
        "consumedItem": ((30000271, 4),),
        "spiritValue": 15,
        "consumedCoin": ((30000002, 1000),),
        "consumedRune": ((30000312, 1),)
    })
})
minKey = 2121
maxKey = 7944