# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: worldMonsterRefresh/entitykRefreshGroup
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
        "refreshNum": 1,
        "refreshTime": 10,
        "entityID": ((16000048, 56), (16000049, 40), (16000050, 4), (16000051, 0))
    }),
    2: _tools.RODict({
        "ID": 2,
        "refreshNum": 1,
        "refreshTime": 10,
        "entityID": ((16000052, 56), (16000053, 40), (16000054, 4), (16000055, 0))
    }),
    10010001: _tools.RODict({
        "ID": 10010001,
        "refreshNum": 20,
        "refreshTime": 800,
        "entityID": ((16001001, 56), (16001002, 40), (16001003, 4), (16001004, 0))
    }),
    10020001: _tools.RODict({
        "ID": 10020001,
        "refreshNum": 20,
        "refreshTime": 800,
        "entityID": ((16001001, 56), (16001002, 40), (16001003, 4), (16001004, 0))
    }),
    10100001: _tools.RODict({
        "ID": 10100001,
        "refreshNum": 20,
        "refreshTime": 800,
        "entityID": ((16001009, 47), (16001010, 45), (16001011, 7), (16001012, 1))
    }),
    10240001: _tools.RODict({
        "ID": 10240001,
        "refreshNum": 20,
        "refreshTime": 800,
        "entityID": ((16001009, 47), (16001010, 45), (16001011, 7), (16001012, 1))
    }),
    10300001: _tools.RODict({
        "ID": 10300001,
        "refreshNum": 20,
        "refreshTime": 800,
        "entityID": ((16001001, 56), (16001002, 40), (16001003, 4), (16001004, 0))
    }),
    11230001: _tools.RODict({
        "ID": 11230001,
        "refreshNum": 20,
        "refreshTime": 800,
        "entityID": ((16001009, 47), (16001010, 45), (16001011, 7), (16001012, 1))
    }),
    10350001: _tools.RODict({
        "ID": 10350001,
        "refreshNum": 18,
        "refreshTime": 800,
        "entityID": ((16001033, 18), (16001034, 60), (16001035, 16), (16001036, 6))
    }),
    10350002: _tools.RODict({
        "ID": 10350002,
        "refreshNum": 20,
        "refreshTime": 800,
        "entityID": ((16001037, 18), (16001038, 60), (16001039, 16), (16001040, 6))
    }),
    10350003: _tools.RODict({
        "ID": 10350003,
        "refreshNum": 14,
        "refreshTime": 800,
        "entityID": ((16001037, 18), (16001038, 60), (16001039, 16), (16001040, 6))
    }),
    10350004: _tools.RODict({
        "ID": 10350004,
        "refreshNum": 11,
        "refreshTime": 800,
        "entityID": ((16001033, 18), (16001034, 60), (16001035, 16), (16001036, 6))
    }),
    10350005: _tools.RODict({
        "ID": 10350005,
        "refreshNum": 12,
        "refreshTime": 800,
        "entityID": ((16001033, 18), (16001034, 60), (16001035, 16), (16001036, 6))
    }),
    31180001: _tools.RODict({
        "ID": 31180001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001020, 100),)
    }),
    31180002: _tools.RODict({
        "ID": 31180002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001019, 100),)
    }),
    31180003: _tools.RODict({
        "ID": 31180003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001019, 100),)
    }),
    31180004: _tools.RODict({
        "ID": 31180004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001017, 38), (16001018, 50), (16001019, 10), (16001020, 2))
    }),
    31180005: _tools.RODict({
        "ID": 31180005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001017, 38), (16001018, 50), (16001019, 10), (16001020, 2))
    }),
    31180006: _tools.RODict({
        "ID": 31180006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001017, 38), (16001018, 50), (16001019, 10), (16001020, 2))
    }),
    31180007: _tools.RODict({
        "ID": 31180007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001017, 38), (16001018, 50), (16001019, 10), (16001020, 2))
    }),
    31190001: _tools.RODict({
        "ID": 31190001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001024, 100),)
    }),
    31190002: _tools.RODict({
        "ID": 31190002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001023, 100),)
    }),
    31190003: _tools.RODict({
        "ID": 31190003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001023, 100),)
    }),
    31190004: _tools.RODict({
        "ID": 31190004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001021, 38), (16001022, 50), (16001023, 10), (16001024, 2))
    }),
    31190005: _tools.RODict({
        "ID": 31190005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001021, 38), (16001022, 50), (16001023, 10), (16001024, 2))
    }),
    31190006: _tools.RODict({
        "ID": 31190006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001021, 38), (16001022, 50), (16001023, 10), (16001024, 2))
    }),
    31190007: _tools.RODict({
        "ID": 31190007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001021, 38), (16001022, 50), (16001023, 10), (16001024, 2))
    }),
    32180001: _tools.RODict({
        "ID": 32180001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001028, 100),)
    }),
    32180002: _tools.RODict({
        "ID": 32180002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001027, 100),)
    }),
    32180003: _tools.RODict({
        "ID": 32180003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001027, 100),)
    }),
    32180004: _tools.RODict({
        "ID": 32180004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001025, 28), (16001026, 55), (16001027, 13), (16001028, 4))
    }),
    32180005: _tools.RODict({
        "ID": 32180005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001025, 28), (16001026, 55), (16001027, 13), (16001028, 4))
    }),
    32180006: _tools.RODict({
        "ID": 32180006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001025, 28), (16001026, 55), (16001027, 13), (16001028, 4))
    }),
    32180007: _tools.RODict({
        "ID": 32180007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001025, 28), (16001026, 55), (16001027, 13), (16001028, 4))
    }),
    32190001: _tools.RODict({
        "ID": 32190001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001032, 100),)
    }),
    32190002: _tools.RODict({
        "ID": 32190002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001031, 100),)
    }),
    32190003: _tools.RODict({
        "ID": 32190003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001031, 100),)
    }),
    32190004: _tools.RODict({
        "ID": 32190004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001029, 28), (16001030, 55), (16001031, 13), (16001032, 4))
    }),
    32190005: _tools.RODict({
        "ID": 32190005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001029, 28), (16001030, 55), (16001031, 13), (16001032, 4))
    }),
    32190006: _tools.RODict({
        "ID": 32190006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001029, 28), (16001030, 55), (16001031, 13), (16001032, 4))
    }),
    32190007: _tools.RODict({
        "ID": 32190007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001029, 28), (16001030, 55), (16001031, 13), (16001032, 4))
    }),
    33180001: _tools.RODict({
        "ID": 33180001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001036, 100),)
    }),
    33180002: _tools.RODict({
        "ID": 33180002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001035, 100),)
    }),
    33180003: _tools.RODict({
        "ID": 33180003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001035, 100),)
    }),
    33180004: _tools.RODict({
        "ID": 33180004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001033, 18), (16001034, 60), (16001035, 16), (16001036, 6))
    }),
    33180005: _tools.RODict({
        "ID": 33180005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001033, 18), (16001034, 60), (16001035, 16), (16001036, 6))
    }),
    33180006: _tools.RODict({
        "ID": 33180006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001033, 18), (16001034, 60), (16001035, 16), (16001036, 6))
    }),
    33180007: _tools.RODict({
        "ID": 33180007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001033, 18), (16001034, 60), (16001035, 16), (16001036, 6))
    }),
    33190001: _tools.RODict({
        "ID": 33190001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001040, 100),)
    }),
    33190002: _tools.RODict({
        "ID": 33190002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001039, 100),)
    }),
    33190003: _tools.RODict({
        "ID": 33190003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001039, 100),)
    }),
    33190004: _tools.RODict({
        "ID": 33190004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001037, 18), (16001038, 60), (16001039, 16), (16001040, 6))
    }),
    33190005: _tools.RODict({
        "ID": 33190005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001037, 18), (16001038, 60), (16001039, 16), (16001040, 6))
    }),
    33190006: _tools.RODict({
        "ID": 33190006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001037, 18), (16001038, 60), (16001039, 16), (16001040, 6))
    }),
    33190007: _tools.RODict({
        "ID": 33190007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001037, 18), (16001038, 60), (16001039, 16), (16001040, 6))
    }),
    34180001: _tools.RODict({
        "ID": 34180001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001044, 100),)
    }),
    34180002: _tools.RODict({
        "ID": 34180002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001043, 100),)
    }),
    34180003: _tools.RODict({
        "ID": 34180003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001043, 100),)
    }),
    34180004: _tools.RODict({
        "ID": 34180004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001041, 13), (16001042, 60), (16001043, 19), (16001044, 8))
    }),
    34180005: _tools.RODict({
        "ID": 34180005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001041, 13), (16001042, 60), (16001043, 19), (16001044, 8))
    }),
    34180006: _tools.RODict({
        "ID": 34180006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001041, 13), (16001042, 60), (16001043, 19), (16001044, 8))
    }),
    34180007: _tools.RODict({
        "ID": 34180007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001041, 13), (16001042, 60), (16001043, 19), (16001044, 8))
    }),
    34190001: _tools.RODict({
        "ID": 34190001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001048, 100),)
    }),
    34190002: _tools.RODict({
        "ID": 34190002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001047, 100),)
    }),
    34190003: _tools.RODict({
        "ID": 34190003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001047, 100),)
    }),
    34190004: _tools.RODict({
        "ID": 34190004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001045, 13), (16001046, 60), (16001047, 19), (16001048, 8))
    }),
    34190005: _tools.RODict({
        "ID": 34190005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001045, 13), (16001046, 60), (16001047, 19), (16001048, 8))
    }),
    34190006: _tools.RODict({
        "ID": 34190006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001045, 13), (16001046, 60), (16001047, 19), (16001048, 8))
    }),
    34190007: _tools.RODict({
        "ID": 34190007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001045, 13), (16001046, 60), (16001047, 19), (16001048, 8))
    }),
    35180001: _tools.RODict({
        "ID": 35180001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001052, 100),)
    }),
    35180002: _tools.RODict({
        "ID": 35180002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001051, 100),)
    }),
    35180003: _tools.RODict({
        "ID": 35180003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001051, 100),)
    }),
    35180004: _tools.RODict({
        "ID": 35180004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001049, 8), (16001050, 60), (16001051, 22), (16001052, 10))
    }),
    35180005: _tools.RODict({
        "ID": 35180005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001049, 8), (16001050, 60), (16001051, 22), (16001052, 10))
    }),
    35180006: _tools.RODict({
        "ID": 35180006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001049, 8), (16001050, 60), (16001051, 22), (16001052, 10))
    }),
    35180007: _tools.RODict({
        "ID": 35180007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001049, 8), (16001050, 60), (16001051, 22), (16001052, 10))
    }),
    35190001: _tools.RODict({
        "ID": 35190001,
        "refreshNum": 1,
        "refreshTime": 1500,
        "entityID": ((16001056, 100),)
    }),
    35190002: _tools.RODict({
        "ID": 35190002,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001055, 100),)
    }),
    35190003: _tools.RODict({
        "ID": 35190003,
        "refreshNum": 1,
        "refreshTime": 1200,
        "entityID": ((16001055, 100),)
    }),
    35190004: _tools.RODict({
        "ID": 35190004,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001053, 8), (16001054, 60), (16001055, 22), (16001056, 10))
    }),
    35190005: _tools.RODict({
        "ID": 35190005,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001053, 8), (16001054, 60), (16001055, 22), (16001056, 10))
    }),
    35190006: _tools.RODict({
        "ID": 35190006,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001053, 8), (16001054, 60), (16001055, 22), (16001056, 10))
    }),
    35190007: _tools.RODict({
        "ID": 35190007,
        "refreshNum": 5,
        "refreshTime": 900,
        "entityID": ((16001053, 8), (16001054, 60), (16001055, 22), (16001056, 10))
    })
})
minKey = 1
maxKey = 35190007