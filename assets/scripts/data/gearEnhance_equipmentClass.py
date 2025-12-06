# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/equipmentClass
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1101: _tools.RODict({
        "ID": 1101,
        "type": 1,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 1000),)
    }),
    1102: _tools.RODict({
        "ID": 1102,
        "type": 1,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 1500),)
    }),
    1103: _tools.RODict({
        "ID": 1103,
        "type": 1,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 2000),)
    }),
    1104: _tools.RODict({
        "ID": 1104,
        "type": 1,
        "quality": 1,
        "level": 4,
        "costCurrency": 0
    }),
    1201: _tools.RODict({
        "ID": 1201,
        "type": 1,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 20000),)
    }),
    1202: _tools.RODict({
        "ID": 1202,
        "type": 1,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 30000),)
    }),
    1203: _tools.RODict({
        "ID": 1203,
        "type": 1,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 40000),)
    }),
    1204: _tools.RODict({
        "ID": 1204,
        "type": 1,
        "quality": 2,
        "level": 4,
        "costCurrency": 0
    }),
    1301: _tools.RODict({
        "ID": 1301,
        "type": 1,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 400000),)
    }),
    1302: _tools.RODict({
        "ID": 1302,
        "type": 1,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 600000),)
    }),
    1303: _tools.RODict({
        "ID": 1303,
        "type": 1,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 800000),)
    }),
    1304: _tools.RODict({
        "ID": 1304,
        "type": 1,
        "quality": 3,
        "level": 4,
        "costCurrency": 0
    }),
    1401: _tools.RODict({
        "ID": 1401,
        "type": 1,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 10000000),)
    }),
    1402: _tools.RODict({
        "ID": 1402,
        "type": 1,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 15000000),)
    }),
    1403: _tools.RODict({
        "ID": 1403,
        "type": 1,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 20000000),)
    }),
    1404: _tools.RODict({
        "ID": 1404,
        "type": 1,
        "quality": 4,
        "level": 4,
        "costCurrency": 0
    }),
    2101: _tools.RODict({
        "ID": 2101,
        "type": 2,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 1000),)
    }),
    2102: _tools.RODict({
        "ID": 2102,
        "type": 2,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 1500),)
    }),
    2103: _tools.RODict({
        "ID": 2103,
        "type": 2,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 2000),)
    }),
    2104: _tools.RODict({
        "ID": 2104,
        "type": 2,
        "quality": 1,
        "level": 4,
        "costCurrency": 0
    }),
    2201: _tools.RODict({
        "ID": 2201,
        "type": 2,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 20000),)
    }),
    2202: _tools.RODict({
        "ID": 2202,
        "type": 2,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 30000),)
    }),
    2203: _tools.RODict({
        "ID": 2203,
        "type": 2,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 40000),)
    }),
    2204: _tools.RODict({
        "ID": 2204,
        "type": 2,
        "quality": 2,
        "level": 4,
        "costCurrency": 0
    }),
    2301: _tools.RODict({
        "ID": 2301,
        "type": 2,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 400000),)
    }),
    2302: _tools.RODict({
        "ID": 2302,
        "type": 2,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 600000),)
    }),
    2303: _tools.RODict({
        "ID": 2303,
        "type": 2,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 800000),)
    }),
    2304: _tools.RODict({
        "ID": 2304,
        "type": 2,
        "quality": 3,
        "level": 4,
        "costCurrency": 0
    }),
    2401: _tools.RODict({
        "ID": 2401,
        "type": 2,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 10000000),)
    }),
    2402: _tools.RODict({
        "ID": 2402,
        "type": 2,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 15000000),)
    }),
    2403: _tools.RODict({
        "ID": 2403,
        "type": 2,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 20000000),)
    }),
    2404: _tools.RODict({
        "ID": 2404,
        "type": 2,
        "quality": 4,
        "level": 4,
        "costCurrency": 0
    }),
    3101: _tools.RODict({
        "ID": 3101,
        "type": 3,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 1000),)
    }),
    3102: _tools.RODict({
        "ID": 3102,
        "type": 3,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 1500),)
    }),
    3103: _tools.RODict({
        "ID": 3103,
        "type": 3,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 2000),)
    }),
    3104: _tools.RODict({
        "ID": 3104,
        "type": 3,
        "quality": 1,
        "level": 4,
        "costCurrency": 0
    }),
    3201: _tools.RODict({
        "ID": 3201,
        "type": 3,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 20000),)
    }),
    3202: _tools.RODict({
        "ID": 3202,
        "type": 3,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 30000),)
    }),
    3203: _tools.RODict({
        "ID": 3203,
        "type": 3,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 40000),)
    }),
    3204: _tools.RODict({
        "ID": 3204,
        "type": 3,
        "quality": 2,
        "level": 4,
        "costCurrency": 0
    }),
    3301: _tools.RODict({
        "ID": 3301,
        "type": 3,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 400000),)
    }),
    3302: _tools.RODict({
        "ID": 3302,
        "type": 3,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 600000),)
    }),
    3303: _tools.RODict({
        "ID": 3303,
        "type": 3,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 800000),)
    }),
    3304: _tools.RODict({
        "ID": 3304,
        "type": 3,
        "quality": 3,
        "level": 4,
        "costCurrency": 0
    }),
    3401: _tools.RODict({
        "ID": 3401,
        "type": 3,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 10000000),)
    }),
    3402: _tools.RODict({
        "ID": 3402,
        "type": 3,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 15000000),)
    }),
    3403: _tools.RODict({
        "ID": 3403,
        "type": 3,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 20000000),)
    }),
    3404: _tools.RODict({
        "ID": 3404,
        "type": 3,
        "quality": 4,
        "level": 4,
        "costCurrency": 0
    }),
    4101: _tools.RODict({
        "ID": 4101,
        "type": 4,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 1000),)
    }),
    4102: _tools.RODict({
        "ID": 4102,
        "type": 4,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 1500),)
    }),
    4103: _tools.RODict({
        "ID": 4103,
        "type": 4,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 2000),)
    }),
    4104: _tools.RODict({
        "ID": 4104,
        "type": 4,
        "quality": 1,
        "level": 4,
        "costCurrency": 0
    }),
    4201: _tools.RODict({
        "ID": 4201,
        "type": 4,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 20000),)
    }),
    4202: _tools.RODict({
        "ID": 4202,
        "type": 4,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 30000),)
    }),
    4203: _tools.RODict({
        "ID": 4203,
        "type": 4,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 40000),)
    }),
    4204: _tools.RODict({
        "ID": 4204,
        "type": 4,
        "quality": 2,
        "level": 4,
        "costCurrency": 0
    }),
    4301: _tools.RODict({
        "ID": 4301,
        "type": 4,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 400000),)
    }),
    4302: _tools.RODict({
        "ID": 4302,
        "type": 4,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 600000),)
    }),
    4303: _tools.RODict({
        "ID": 4303,
        "type": 4,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 800000),)
    }),
    4304: _tools.RODict({
        "ID": 4304,
        "type": 4,
        "quality": 3,
        "level": 4,
        "costCurrency": 0
    }),
    4401: _tools.RODict({
        "ID": 4401,
        "type": 4,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 10000000),)
    }),
    4402: _tools.RODict({
        "ID": 4402,
        "type": 4,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 15000000),)
    }),
    4403: _tools.RODict({
        "ID": 4403,
        "type": 4,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 20000000),)
    }),
    4404: _tools.RODict({
        "ID": 4404,
        "type": 4,
        "quality": 4,
        "level": 4,
        "costCurrency": 0
    }),
    5101: _tools.RODict({
        "ID": 5101,
        "type": 5,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 1000),)
    }),
    5102: _tools.RODict({
        "ID": 5102,
        "type": 5,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 1500),)
    }),
    5103: _tools.RODict({
        "ID": 5103,
        "type": 5,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 2000),)
    }),
    5104: _tools.RODict({
        "ID": 5104,
        "type": 5,
        "quality": 1,
        "level": 4,
        "costCurrency": 0
    }),
    5201: _tools.RODict({
        "ID": 5201,
        "type": 5,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 20000),)
    }),
    5202: _tools.RODict({
        "ID": 5202,
        "type": 5,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 30000),)
    }),
    5203: _tools.RODict({
        "ID": 5203,
        "type": 5,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 40000),)
    }),
    5204: _tools.RODict({
        "ID": 5204,
        "type": 5,
        "quality": 2,
        "level": 4,
        "costCurrency": 0
    }),
    5301: _tools.RODict({
        "ID": 5301,
        "type": 5,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 400000),)
    }),
    5302: _tools.RODict({
        "ID": 5302,
        "type": 5,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 600000),)
    }),
    5303: _tools.RODict({
        "ID": 5303,
        "type": 5,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 800000),)
    }),
    5304: _tools.RODict({
        "ID": 5304,
        "type": 5,
        "quality": 3,
        "level": 4,
        "costCurrency": 0
    }),
    5401: _tools.RODict({
        "ID": 5401,
        "type": 5,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 10000000),)
    }),
    5402: _tools.RODict({
        "ID": 5402,
        "type": 5,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 15000000),)
    }),
    5403: _tools.RODict({
        "ID": 5403,
        "type": 5,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 20000000),)
    }),
    5404: _tools.RODict({
        "ID": 5404,
        "type": 5,
        "quality": 4,
        "level": 4,
        "costCurrency": 0
    }),
    6101: _tools.RODict({
        "ID": 6101,
        "type": 6,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 1000),)
    }),
    6102: _tools.RODict({
        "ID": 6102,
        "type": 6,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 1500),)
    }),
    6103: _tools.RODict({
        "ID": 6103,
        "type": 6,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 2000),)
    }),
    6104: _tools.RODict({
        "ID": 6104,
        "type": 6,
        "quality": 1,
        "level": 4,
        "costCurrency": 0
    }),
    6201: _tools.RODict({
        "ID": 6201,
        "type": 6,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 20000),)
    }),
    6202: _tools.RODict({
        "ID": 6202,
        "type": 6,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 30000),)
    }),
    6203: _tools.RODict({
        "ID": 6203,
        "type": 6,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 40000),)
    }),
    6204: _tools.RODict({
        "ID": 6204,
        "type": 6,
        "quality": 2,
        "level": 4,
        "costCurrency": 0
    }),
    6301: _tools.RODict({
        "ID": 6301,
        "type": 6,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 400000),)
    }),
    6302: _tools.RODict({
        "ID": 6302,
        "type": 6,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 600000),)
    }),
    6303: _tools.RODict({
        "ID": 6303,
        "type": 6,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 800000),)
    }),
    6304: _tools.RODict({
        "ID": 6304,
        "type": 6,
        "quality": 3,
        "level": 4,
        "costCurrency": 0
    }),
    6401: _tools.RODict({
        "ID": 6401,
        "type": 6,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 10000000),)
    }),
    6402: _tools.RODict({
        "ID": 6402,
        "type": 6,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 15000000),)
    }),
    6403: _tools.RODict({
        "ID": 6403,
        "type": 6,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 20000000),)
    }),
    6404: _tools.RODict({
        "ID": 6404,
        "type": 6,
        "quality": 4,
        "level": 4,
        "costCurrency": 0
    }),
    7101: _tools.RODict({
        "ID": 7101,
        "type": 7,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 1000),)
    }),
    7102: _tools.RODict({
        "ID": 7102,
        "type": 7,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 1500),)
    }),
    7103: _tools.RODict({
        "ID": 7103,
        "type": 7,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 2000),)
    }),
    7104: _tools.RODict({
        "ID": 7104,
        "type": 7,
        "quality": 1,
        "level": 4,
        "costCurrency": 0
    }),
    7201: _tools.RODict({
        "ID": 7201,
        "type": 7,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 20000),)
    }),
    7202: _tools.RODict({
        "ID": 7202,
        "type": 7,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 30000),)
    }),
    7203: _tools.RODict({
        "ID": 7203,
        "type": 7,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 40000),)
    }),
    7204: _tools.RODict({
        "ID": 7204,
        "type": 7,
        "quality": 2,
        "level": 4,
        "costCurrency": 0
    }),
    7301: _tools.RODict({
        "ID": 7301,
        "type": 7,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 400000),)
    }),
    7302: _tools.RODict({
        "ID": 7302,
        "type": 7,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 600000),)
    }),
    7303: _tools.RODict({
        "ID": 7303,
        "type": 7,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 800000),)
    }),
    7304: _tools.RODict({
        "ID": 7304,
        "type": 7,
        "quality": 3,
        "level": 4,
        "costCurrency": 0
    }),
    7401: _tools.RODict({
        "ID": 7401,
        "type": 7,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 10000000),)
    }),
    7402: _tools.RODict({
        "ID": 7402,
        "type": 7,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 15000000),)
    }),
    7403: _tools.RODict({
        "ID": 7403,
        "type": 7,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 20000000),)
    }),
    7404: _tools.RODict({
        "ID": 7404,
        "type": 7,
        "quality": 4,
        "level": 4,
        "costCurrency": 0
    }),
    8101: _tools.RODict({
        "ID": 8101,
        "type": 8,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 1000),)
    }),
    8102: _tools.RODict({
        "ID": 8102,
        "type": 8,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 1500),)
    }),
    8103: _tools.RODict({
        "ID": 8103,
        "type": 8,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 2000),)
    }),
    8104: _tools.RODict({
        "ID": 8104,
        "type": 8,
        "quality": 1,
        "level": 4,
        "costCurrency": 0
    }),
    8201: _tools.RODict({
        "ID": 8201,
        "type": 8,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 20000),)
    }),
    8202: _tools.RODict({
        "ID": 8202,
        "type": 8,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 30000),)
    }),
    8203: _tools.RODict({
        "ID": 8203,
        "type": 8,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 40000),)
    }),
    8204: _tools.RODict({
        "ID": 8204,
        "type": 8,
        "quality": 2,
        "level": 4,
        "costCurrency": 0
    }),
    8301: _tools.RODict({
        "ID": 8301,
        "type": 8,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 400000),)
    }),
    8302: _tools.RODict({
        "ID": 8302,
        "type": 8,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 600000),)
    }),
    8303: _tools.RODict({
        "ID": 8303,
        "type": 8,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 800000),)
    }),
    8304: _tools.RODict({
        "ID": 8304,
        "type": 8,
        "quality": 3,
        "level": 4,
        "costCurrency": 0
    }),
    8401: _tools.RODict({
        "ID": 8401,
        "type": 8,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 10000000),)
    }),
    8402: _tools.RODict({
        "ID": 8402,
        "type": 8,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 15000000),)
    }),
    8403: _tools.RODict({
        "ID": 8403,
        "type": 8,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 20000000),)
    }),
    8404: _tools.RODict({
        "ID": 8404,
        "type": 8,
        "quality": 4,
        "level": 4,
        "costCurrency": 0
    })
})
minKey = 1101
maxKey = 8404