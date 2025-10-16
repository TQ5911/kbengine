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
        "materials": _tools.ROList([[30000223, 5]]),
        "cost": _tools.ROList([[30000013, 1000], [30000100, 2000]]),
        "lucky": _tools.ROList([30000224, 1, 0.1, 0.1]),
        "unboundProb": 0.3,
        "isOpen": 1
    }),
    30000225: _tools.RODict({
        "ID": 30000225,
        "materials": _tools.ROList([[30000224, 6]]),
        "cost": _tools.ROList([[30000013, 1000], [30000100, 2001]]),
        "lucky": _tools.ROList([30000224, 2, 0.5, 0.2]),
        "unboundProb": 0.3,
        "isOpen": 1
    }),
    30000226: _tools.RODict({
        "ID": 30000226,
        "materials": _tools.ROList([[30000225, 7]]),
        "cost": _tools.ROList([[30000013, 1000], [30000100, 2002]]),
        "lucky": _tools.ROList([30000224, 3, 0.2, 0.2]),
        "unboundProb": 0.3,
        "isOpen": 1
    }),
    30000231: _tools.RODict({
        "ID": 30000231,
        "materials": _tools.ROList([[30000223, 10]]),
        "cost": _tools.ROList([[30000013, 1000], [30000100, 2003]]),
        "lucky": _tools.ROList([30000224, 4, 1, 0.2]),
        "unboundProb": 0.3,
        "isOpen": 1
    }),
    30000232: _tools.RODict({
        "ID": 30000232,
        "materials": _tools.ROList([[30000224, 5]]),
        "cost": _tools.ROList([[30000013, 1000], [30000100, 2004]]),
        "lucky": _tools.ROList([30000224, 5, 0.1, 0.2]),
        "unboundProb": 0.3,
        "isOpen": 1
    }),
    30000233: _tools.RODict({
        "ID": 30000233,
        "materials": _tools.ROList([[30000225, 10]]),
        "cost": _tools.ROList([[30000013, 1000], [30000100, 2005]]),
        "lucky": _tools.ROList([30000224, 6, 0.5, 0.2]),
        "unboundProb": 0.3,
        "isOpen": 0
    })
})
minKey = 30000224
maxKey = 30000233