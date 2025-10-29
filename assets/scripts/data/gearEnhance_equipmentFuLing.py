# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/equipmentFuLing
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
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    2122: _tools.RODict({
        "ID": 2122,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    2123: _tools.RODict({
        "ID": 2123,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    2124: _tools.RODict({
        "ID": 2124,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    2131: _tools.RODict({
        "ID": 2131,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    2132: _tools.RODict({
        "ID": 2132,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    2133: _tools.RODict({
        "ID": 2133,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    2134: _tools.RODict({
        "ID": 2134,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    2141: _tools.RODict({
        "ID": 2141,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    2142: _tools.RODict({
        "ID": 2142,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    2143: _tools.RODict({
        "ID": 2143,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    2144: _tools.RODict({
        "ID": 2144,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    2151: _tools.RODict({
        "ID": 2151,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    2221: _tools.RODict({
        "ID": 2221,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    2222: _tools.RODict({
        "ID": 2222,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    2223: _tools.RODict({
        "ID": 2223,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    2224: _tools.RODict({
        "ID": 2224,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    2231: _tools.RODict({
        "ID": 2231,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    2232: _tools.RODict({
        "ID": 2232,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    2233: _tools.RODict({
        "ID": 2233,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    2234: _tools.RODict({
        "ID": 2234,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    2241: _tools.RODict({
        "ID": 2241,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    2242: _tools.RODict({
        "ID": 2242,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    2243: _tools.RODict({
        "ID": 2243,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    2244: _tools.RODict({
        "ID": 2244,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    2251: _tools.RODict({
        "ID": 2251,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    2321: _tools.RODict({
        "ID": 2321,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    2322: _tools.RODict({
        "ID": 2322,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    2323: _tools.RODict({
        "ID": 2323,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    2324: _tools.RODict({
        "ID": 2324,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    2331: _tools.RODict({
        "ID": 2331,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    2332: _tools.RODict({
        "ID": 2332,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    2333: _tools.RODict({
        "ID": 2333,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    2334: _tools.RODict({
        "ID": 2334,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    2341: _tools.RODict({
        "ID": 2341,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    2342: _tools.RODict({
        "ID": 2342,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    2343: _tools.RODict({
        "ID": 2343,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    2344: _tools.RODict({
        "ID": 2344,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    2351: _tools.RODict({
        "ID": 2351,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    3121: _tools.RODict({
        "ID": 3121,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    3122: _tools.RODict({
        "ID": 3122,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    3123: _tools.RODict({
        "ID": 3123,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    3124: _tools.RODict({
        "ID": 3124,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    3131: _tools.RODict({
        "ID": 3131,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    3132: _tools.RODict({
        "ID": 3132,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    3133: _tools.RODict({
        "ID": 3133,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    3134: _tools.RODict({
        "ID": 3134,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    3141: _tools.RODict({
        "ID": 3141,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    3142: _tools.RODict({
        "ID": 3142,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    3143: _tools.RODict({
        "ID": 3143,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    3144: _tools.RODict({
        "ID": 3144,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    3151: _tools.RODict({
        "ID": 3151,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    3221: _tools.RODict({
        "ID": 3221,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    3222: _tools.RODict({
        "ID": 3222,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    3223: _tools.RODict({
        "ID": 3223,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    3224: _tools.RODict({
        "ID": 3224,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    3231: _tools.RODict({
        "ID": 3231,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    3232: _tools.RODict({
        "ID": 3232,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    3233: _tools.RODict({
        "ID": 3233,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    3234: _tools.RODict({
        "ID": 3234,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    3241: _tools.RODict({
        "ID": 3241,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    3242: _tools.RODict({
        "ID": 3242,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    3243: _tools.RODict({
        "ID": 3243,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    3244: _tools.RODict({
        "ID": 3244,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    3251: _tools.RODict({
        "ID": 3251,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    3321: _tools.RODict({
        "ID": 3321,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    3322: _tools.RODict({
        "ID": 3322,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    3323: _tools.RODict({
        "ID": 3323,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    3324: _tools.RODict({
        "ID": 3324,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    3331: _tools.RODict({
        "ID": 3331,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    3332: _tools.RODict({
        "ID": 3332,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    3333: _tools.RODict({
        "ID": 3333,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    3334: _tools.RODict({
        "ID": 3334,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    3341: _tools.RODict({
        "ID": 3341,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    3342: _tools.RODict({
        "ID": 3342,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    3343: _tools.RODict({
        "ID": 3343,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    3344: _tools.RODict({
        "ID": 3344,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    3351: _tools.RODict({
        "ID": 3351,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    4121: _tools.RODict({
        "ID": 4121,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    4122: _tools.RODict({
        "ID": 4122,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    4123: _tools.RODict({
        "ID": 4123,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    4124: _tools.RODict({
        "ID": 4124,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    4131: _tools.RODict({
        "ID": 4131,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    4132: _tools.RODict({
        "ID": 4132,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    4133: _tools.RODict({
        "ID": 4133,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    4134: _tools.RODict({
        "ID": 4134,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    4141: _tools.RODict({
        "ID": 4141,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    4142: _tools.RODict({
        "ID": 4142,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    4143: _tools.RODict({
        "ID": 4143,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    4144: _tools.RODict({
        "ID": 4144,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    4151: _tools.RODict({
        "ID": 4151,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    4221: _tools.RODict({
        "ID": 4221,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    4222: _tools.RODict({
        "ID": 4222,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    4223: _tools.RODict({
        "ID": 4223,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    4224: _tools.RODict({
        "ID": 4224,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    4231: _tools.RODict({
        "ID": 4231,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    4232: _tools.RODict({
        "ID": 4232,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    4233: _tools.RODict({
        "ID": 4233,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    4234: _tools.RODict({
        "ID": 4234,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    4241: _tools.RODict({
        "ID": 4241,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    4242: _tools.RODict({
        "ID": 4242,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    4243: _tools.RODict({
        "ID": 4243,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    4244: _tools.RODict({
        "ID": 4244,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    4251: _tools.RODict({
        "ID": 4251,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    4321: _tools.RODict({
        "ID": 4321,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    4322: _tools.RODict({
        "ID": 4322,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    4323: _tools.RODict({
        "ID": 4323,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    4324: _tools.RODict({
        "ID": 4324,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    4331: _tools.RODict({
        "ID": 4331,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    4332: _tools.RODict({
        "ID": 4332,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    4333: _tools.RODict({
        "ID": 4333,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    4334: _tools.RODict({
        "ID": 4334,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    4341: _tools.RODict({
        "ID": 4341,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    4342: _tools.RODict({
        "ID": 4342,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    4343: _tools.RODict({
        "ID": 4343,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    4344: _tools.RODict({
        "ID": 4344,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    4351: _tools.RODict({
        "ID": 4351,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    5821: _tools.RODict({
        "ID": 5821,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    5822: _tools.RODict({
        "ID": 5822,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    5823: _tools.RODict({
        "ID": 5823,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    5824: _tools.RODict({
        "ID": 5824,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    5831: _tools.RODict({
        "ID": 5831,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    5832: _tools.RODict({
        "ID": 5832,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    5833: _tools.RODict({
        "ID": 5833,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    5834: _tools.RODict({
        "ID": 5834,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    5841: _tools.RODict({
        "ID": 5841,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    5842: _tools.RODict({
        "ID": 5842,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    5843: _tools.RODict({
        "ID": 5843,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    5844: _tools.RODict({
        "ID": 5844,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    5851: _tools.RODict({
        "ID": 5851,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    5921: _tools.RODict({
        "ID": 5921,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    5922: _tools.RODict({
        "ID": 5922,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    5923: _tools.RODict({
        "ID": 5923,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    5924: _tools.RODict({
        "ID": 5924,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    5931: _tools.RODict({
        "ID": 5931,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    5932: _tools.RODict({
        "ID": 5932,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    5933: _tools.RODict({
        "ID": 5933,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    5934: _tools.RODict({
        "ID": 5934,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    5941: _tools.RODict({
        "ID": 5941,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    5942: _tools.RODict({
        "ID": 5942,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    5943: _tools.RODict({
        "ID": 5943,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    5944: _tools.RODict({
        "ID": 5944,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    5951: _tools.RODict({
        "ID": 5951,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    6821: _tools.RODict({
        "ID": 6821,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    6822: _tools.RODict({
        "ID": 6822,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    6823: _tools.RODict({
        "ID": 6823,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    6824: _tools.RODict({
        "ID": 6824,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    6831: _tools.RODict({
        "ID": 6831,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    6832: _tools.RODict({
        "ID": 6832,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    6833: _tools.RODict({
        "ID": 6833,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    6834: _tools.RODict({
        "ID": 6834,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    6841: _tools.RODict({
        "ID": 6841,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    6842: _tools.RODict({
        "ID": 6842,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    6843: _tools.RODict({
        "ID": 6843,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    6844: _tools.RODict({
        "ID": 6844,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    6851: _tools.RODict({
        "ID": 6851,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    6921: _tools.RODict({
        "ID": 6921,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    6922: _tools.RODict({
        "ID": 6922,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    6923: _tools.RODict({
        "ID": 6923,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    6924: _tools.RODict({
        "ID": 6924,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    6931: _tools.RODict({
        "ID": 6931,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    6932: _tools.RODict({
        "ID": 6932,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    6933: _tools.RODict({
        "ID": 6933,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    6934: _tools.RODict({
        "ID": 6934,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    6941: _tools.RODict({
        "ID": 6941,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    6942: _tools.RODict({
        "ID": 6942,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    6943: _tools.RODict({
        "ID": 6943,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    6944: _tools.RODict({
        "ID": 6944,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    6951: _tools.RODict({
        "ID": 6951,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    7821: _tools.RODict({
        "ID": 7821,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    7822: _tools.RODict({
        "ID": 7822,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    7823: _tools.RODict({
        "ID": 7823,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    7824: _tools.RODict({
        "ID": 7824,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    7831: _tools.RODict({
        "ID": 7831,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    7832: _tools.RODict({
        "ID": 7832,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    7833: _tools.RODict({
        "ID": 7833,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    7834: _tools.RODict({
        "ID": 7834,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    7841: _tools.RODict({
        "ID": 7841,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    7842: _tools.RODict({
        "ID": 7842,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    7843: _tools.RODict({
        "ID": 7843,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    7844: _tools.RODict({
        "ID": 7844,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    7851: _tools.RODict({
        "ID": 7851,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    7921: _tools.RODict({
        "ID": 7921,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    7922: _tools.RODict({
        "ID": 7922,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    7923: _tools.RODict({
        "ID": 7923,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    7924: _tools.RODict({
        "ID": 7924,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    7931: _tools.RODict({
        "ID": 7931,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    7932: _tools.RODict({
        "ID": 7932,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    7933: _tools.RODict({
        "ID": 7933,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    7934: _tools.RODict({
        "ID": 7934,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    7941: _tools.RODict({
        "ID": 7941,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    7942: _tools.RODict({
        "ID": 7942,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    7943: _tools.RODict({
        "ID": 7943,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    7944: _tools.RODict({
        "ID": 7944,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    7951: _tools.RODict({
        "ID": 7951,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    7031: _tools.RODict({
        "ID": 7031,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    7032: _tools.RODict({
        "ID": 7032,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    7033: _tools.RODict({
        "ID": 7033,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    7034: _tools.RODict({
        "ID": 7034,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    7035: _tools.RODict({
        "ID": 7035,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    7041: _tools.RODict({
        "ID": 7041,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    7042: _tools.RODict({
        "ID": 7042,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    7043: _tools.RODict({
        "ID": 7043,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    7051: _tools.RODict({
        "ID": 7051,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    8031: _tools.RODict({
        "ID": 8031,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    8032: _tools.RODict({
        "ID": 8032,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    8033: _tools.RODict({
        "ID": 8033,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    8034: _tools.RODict({
        "ID": 8034,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    8035: _tools.RODict({
        "ID": 8035,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    8041: _tools.RODict({
        "ID": 8041,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    8042: _tools.RODict({
        "ID": 8042,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    8043: _tools.RODict({
        "ID": 8043,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    8051: _tools.RODict({
        "ID": 8051,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    1121: _tools.RODict({
        "ID": 1121,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    1122: _tools.RODict({
        "ID": 1122,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    1123: _tools.RODict({
        "ID": 1123,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    1124: _tools.RODict({
        "ID": 1124,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    1131: _tools.RODict({
        "ID": 1131,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    1132: _tools.RODict({
        "ID": 1132,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    1133: _tools.RODict({
        "ID": 1133,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    1134: _tools.RODict({
        "ID": 1134,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    1135: _tools.RODict({
        "ID": 1135,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    1141: _tools.RODict({
        "ID": 1141,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    1142: _tools.RODict({
        "ID": 1142,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    1143: _tools.RODict({
        "ID": 1143,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    1151: _tools.RODict({
        "ID": 1151,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    1221: _tools.RODict({
        "ID": 1221,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    1222: _tools.RODict({
        "ID": 1222,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    1223: _tools.RODict({
        "ID": 1223,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    1224: _tools.RODict({
        "ID": 1224,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    1231: _tools.RODict({
        "ID": 1231,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    1232: _tools.RODict({
        "ID": 1232,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    1233: _tools.RODict({
        "ID": 1233,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    1234: _tools.RODict({
        "ID": 1234,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    1235: _tools.RODict({
        "ID": 1235,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    1241: _tools.RODict({
        "ID": 1241,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    1242: _tools.RODict({
        "ID": 1242,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    1243: _tools.RODict({
        "ID": 1243,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    1251: _tools.RODict({
        "ID": 1251,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    }),
    1321: _tools.RODict({
        "ID": 1321,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 2000),),
        "consumedRune": 0
    }),
    1322: _tools.RODict({
        "ID": 1322,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 4000),),
        "consumedRune": 0
    }),
    1323: _tools.RODict({
        "ID": 1323,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 6000),),
        "consumedRune": 0
    }),
    1324: _tools.RODict({
        "ID": 1324,
        "consumedItem": ((30000227, 1),),
        "consumedCoin": ((30000002, 8000),),
        "consumedRune": 0
    }),
    1331: _tools.RODict({
        "ID": 1331,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 10000),),
        "consumedRune": 0
    }),
    1332: _tools.RODict({
        "ID": 1332,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 12000),),
        "consumedRune": 0
    }),
    1333: _tools.RODict({
        "ID": 1333,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 14000),),
        "consumedRune": 0
    }),
    1334: _tools.RODict({
        "ID": 1334,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 16000),),
        "consumedRune": 0
    }),
    1335: _tools.RODict({
        "ID": 1335,
        "consumedItem": ((30000228, 1),),
        "consumedCoin": ((30000002, 18000),),
        "consumedRune": 0
    }),
    1341: _tools.RODict({
        "ID": 1341,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 20000),),
        "consumedRune": 0
    }),
    1342: _tools.RODict({
        "ID": 1342,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 22000),),
        "consumedRune": 0
    }),
    1343: _tools.RODict({
        "ID": 1343,
        "consumedItem": ((30000229, 1),),
        "consumedCoin": ((30000002, 24000),),
        "consumedRune": 0
    }),
    1351: _tools.RODict({
        "ID": 1351,
        "consumedItem": ((30000230, 1),),
        "consumedCoin": ((30000002, 26000),),
        "consumedRune": 0
    })
})
minKey = 1121
maxKey = 8051