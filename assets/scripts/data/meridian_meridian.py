# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: meridian/meridian
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
        "prop": _tools.RODict({1001:52121021,1002:52121021,1003:52121001}),
        "needItems": _tools.ROList([[30000279, 10]]),
        "needCoins": _tools.ROList([30000013, 1000])
    }),
    2: _tools.RODict({
        "ID": 2,
        "prop": _tools.RODict({1001:52121022,1002:52121022,1003:52121002}),
        "needItems": _tools.ROList([[30000279, 20]]),
        "needCoins": _tools.ROList([30000013, 1200])
    }),
    3: _tools.RODict({
        "ID": 3,
        "prop": _tools.RODict({1001:52121023,1002:52121023,1003:52121003}),
        "needItems": _tools.ROList([[30000279, 40]]),
        "needCoins": _tools.ROList([30000013, 1400])
    }),
    4: _tools.RODict({
        "ID": 4,
        "prop": _tools.RODict({1001:52121024,1002:52121024,1003:52121004}),
        "needItems": _tools.ROList([[30000279, 60]]),
        "needCoins": _tools.ROList([30000013, 1700])
    }),
    5: _tools.RODict({
        "ID": 5,
        "prop": _tools.RODict({1001:52121025,1002:52121025,1003:52121005}),
        "needItems": _tools.ROList([[30000279, 80]]),
        "needCoins": _tools.ROList([30000013, 2000])
    }),
    6: _tools.RODict({
        "ID": 6,
        "prop": _tools.RODict({1001:52121026,1002:52121026,1003:52121006}),
        "needItems": _tools.ROList([[30000280, 10]]),
        "needCoins": _tools.ROList([30000013, 2400])
    }),
    7: _tools.RODict({
        "ID": 7,
        "prop": _tools.RODict({1001:52121027,1002:52121027,1003:52121007}),
        "needItems": _tools.ROList([[30000280, 20]]),
        "needCoins": _tools.ROList([30000013, 2900])
    }),
    8: _tools.RODict({
        "ID": 8,
        "prop": _tools.RODict({1001:52121028,1002:52121028,1003:52121008}),
        "needItems": _tools.ROList([[30000280, 40]]),
        "needCoins": _tools.ROList([30000013, 3500])
    }),
    9: _tools.RODict({
        "ID": 9,
        "prop": _tools.RODict({1001:52121029,1002:52121029,1003:52121009}),
        "needItems": _tools.ROList([[30000280, 60]]),
        "needCoins": _tools.ROList([30000013, 4200])
    }),
    10: _tools.RODict({
        "ID": 10,
        "prop": _tools.RODict({1001:52121030,1002:52121030,1003:52121010}),
        "needItems": _tools.ROList([[30000280, 80]]),
        "needCoins": _tools.ROList([30000013, 5000])
    }),
    11: _tools.RODict({
        "ID": 11,
        "prop": _tools.RODict({1001:52121031,1002:52121031,1003:52121011}),
        "needItems": _tools.ROList([[30000281, 10]]),
        "needCoins": _tools.ROList([30000013, 6000])
    }),
    12: _tools.RODict({
        "ID": 12,
        "prop": _tools.RODict({1001:52121032,1002:52121032,1003:52121012}),
        "needItems": _tools.ROList([[30000281, 20]]),
        "needCoins": _tools.ROList([30000013, 7200])
    }),
    13: _tools.RODict({
        "ID": 13,
        "prop": _tools.RODict({1001:52121033,1002:52121033,1003:52121013}),
        "needItems": _tools.ROList([[30000281, 40]]),
        "needCoins": _tools.ROList([30000013, 8600])
    }),
    14: _tools.RODict({
        "ID": 14,
        "prop": _tools.RODict({1001:52121034,1002:52121034,1003:52121014}),
        "needItems": _tools.ROList([[30000281, 60]]),
        "needCoins": _tools.ROList([30000013, 10300])
    }),
    15: _tools.RODict({
        "ID": 15,
        "prop": _tools.RODict({1001:52121035,1002:52121035,1003:52121015}),
        "needItems": _tools.ROList([[30000281, 80]]),
        "needCoins": _tools.ROList([30000013, 12400])
    }),
    16: _tools.RODict({
        "ID": 16,
        "prop": _tools.RODict({1001:52121036,1002:52121036,1003:52121016}),
        "needItems": _tools.ROList([[30000282, 10]]),
        "needCoins": _tools.ROList([30000013, 14900])
    }),
    17: _tools.RODict({
        "ID": 17,
        "prop": _tools.RODict({1001:52121037,1002:52121037,1003:52121017}),
        "needItems": _tools.ROList([[30000282, 20]]),
        "needCoins": _tools.ROList([30000013, 17900])
    }),
    18: _tools.RODict({
        "ID": 18,
        "prop": _tools.RODict({1001:52121038,1002:52121038,1003:52121018}),
        "needItems": _tools.ROList([[30000282, 40]]),
        "needCoins": _tools.ROList([30000013, 21500])
    }),
    19: _tools.RODict({
        "ID": 19,
        "prop": _tools.RODict({1001:52121039,1002:52121039,1003:52121019}),
        "needItems": _tools.ROList([[30000282, 60]]),
        "needCoins": _tools.ROList([30000013, 25800])
    }),
    20: _tools.RODict({
        "ID": 20,
        "prop": _tools.RODict({1001:52121040,1002:52121040,1003:52121020}),
        "needItems": _tools.ROList([[30000282, 80]]),
        "needCoins": _tools.ROList([30000013, 31000])
    })
})
minKey = 1
maxKey = 20