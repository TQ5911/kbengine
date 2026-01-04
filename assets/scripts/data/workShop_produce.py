# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: workShop/produce
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    30000224: _tools.RODict({
        "ID": 30000224,
        "materials": _tools.ROList([[30000223, 10]]),
        "cost": _tools.ROList([[30000013, 1000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000225: _tools.RODict({
        "ID": 30000225,
        "materials": _tools.ROList([[30000224, 5]]),
        "cost": _tools.ROList([[30000013, 5000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000226: _tools.RODict({
        "ID": 30000226,
        "materials": _tools.ROList([[30000225, 2]]),
        "cost": _tools.ROList([[30000013, 15000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000267: _tools.RODict({
        "ID": 30000267,
        "materials": _tools.ROList([[30000263, 10]]),
        "cost": _tools.ROList([[30000002, 100]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000268: _tools.RODict({
        "ID": 30000268,
        "materials": _tools.ROList([[30000264, 10]]),
        "cost": _tools.ROList([[30000002, 100]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000269: _tools.RODict({
        "ID": 30000269,
        "materials": _tools.ROList([[30000265, 10]]),
        "cost": _tools.ROList([[30000002, 100]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000270: _tools.RODict({
        "ID": 30000270,
        "materials": _tools.ROList([[30000266, 10]]),
        "cost": _tools.ROList([[30000002, 100]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000271: _tools.RODict({
        "ID": 30000271,
        "materials": _tools.ROList([[30000267, 10]]),
        "cost": _tools.ROList([[30000002, 1000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000272: _tools.RODict({
        "ID": 30000272,
        "materials": _tools.ROList([[30000268, 10]]),
        "cost": _tools.ROList([[30000002, 1000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000273: _tools.RODict({
        "ID": 30000273,
        "materials": _tools.ROList([[30000269, 10]]),
        "cost": _tools.ROList([[30000002, 1000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000274: _tools.RODict({
        "ID": 30000274,
        "materials": _tools.ROList([[30000270, 10]]),
        "cost": _tools.ROList([[30000002, 1000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000275: _tools.RODict({
        "ID": 30000275,
        "materials": _tools.ROList([[30000271, 10]]),
        "cost": _tools.ROList([[30000002, 10000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000276: _tools.RODict({
        "ID": 30000276,
        "materials": _tools.ROList([[30000272, 10]]),
        "cost": _tools.ROList([[30000002, 10000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000277: _tools.RODict({
        "ID": 30000277,
        "materials": _tools.ROList([[30000273, 10]]),
        "cost": _tools.ROList([[30000002, 10000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000278: _tools.RODict({
        "ID": 30000278,
        "materials": _tools.ROList([[30000274, 10]]),
        "cost": _tools.ROList([[30000002, 10000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000280: _tools.RODict({
        "ID": 30000280,
        "materials": _tools.ROList([[30000279, 10]]),
        "cost": _tools.ROList([[30000002, 10000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000281: _tools.RODict({
        "ID": 30000281,
        "materials": _tools.ROList([[30000280, 10]]),
        "cost": _tools.ROList([[30000002, 100000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000282: _tools.RODict({
        "ID": 30000282,
        "materials": _tools.ROList([[30000281, 10]]),
        "cost": _tools.ROList([[30000002, 1000000]]),
        "lucky": None,
        "unboundProb": 0.0,
        "isOpen": 1
    }),
    30000287: _tools.RODict({
        "ID": 30000287,
        "materials": _tools.ROList([[30000283, 10]]),
        "cost": _tools.ROList([[30000013, 300]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000288: _tools.RODict({
        "ID": 30000288,
        "materials": _tools.ROList([[30000284, 10]]),
        "cost": _tools.ROList([[30000013, 300]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000289: _tools.RODict({
        "ID": 30000289,
        "materials": _tools.ROList([[30000285, 10]]),
        "cost": _tools.ROList([[30000013, 300]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000290: _tools.RODict({
        "ID": 30000290,
        "materials": _tools.ROList([[30000286, 10]]),
        "cost": _tools.ROList([[30000013, 300]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000291: _tools.RODict({
        "ID": 30000291,
        "materials": _tools.ROList([[30000287, 10]]),
        "cost": _tools.ROList([[30000013, 1000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000292: _tools.RODict({
        "ID": 30000292,
        "materials": _tools.ROList([[30000288, 10]]),
        "cost": _tools.ROList([[30000013, 1000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000293: _tools.RODict({
        "ID": 30000293,
        "materials": _tools.ROList([[30000289, 10]]),
        "cost": _tools.ROList([[30000013, 1000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000294: _tools.RODict({
        "ID": 30000294,
        "materials": _tools.ROList([[30000290, 10]]),
        "cost": _tools.ROList([[30000013, 1000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000295: _tools.RODict({
        "ID": 30000295,
        "materials": _tools.ROList([[30000291, 10]]),
        "cost": _tools.ROList([[30000013, 5000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000296: _tools.RODict({
        "ID": 30000296,
        "materials": _tools.ROList([[30000292, 10]]),
        "cost": _tools.ROList([[30000013, 5000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000297: _tools.RODict({
        "ID": 30000297,
        "materials": _tools.ROList([[30000293, 10]]),
        "cost": _tools.ROList([[30000013, 5000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    }),
    30000298: _tools.RODict({
        "ID": 30000298,
        "materials": _tools.ROList([[30000294, 10]]),
        "cost": _tools.ROList([[30000013, 5000]]),
        "lucky": None,
        "unboundProb": 0.1,
        "isOpen": 1
    })
})
minKey = 30000224
maxKey = 30000298