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
        "costCurrency": ((30000013, 40),)
    }),
    1102: _tools.RODict({
        "ID": 1102,
        "type": 1,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    1103: _tools.RODict({
        "ID": 1103,
        "type": 1,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    1104: _tools.RODict({
        "ID": 1104,
        "type": 1,
        "quality": 1,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    1105: _tools.RODict({
        "ID": 1105,
        "type": 1,
        "quality": 1,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    1201: _tools.RODict({
        "ID": 1201,
        "type": 1,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    1202: _tools.RODict({
        "ID": 1202,
        "type": 1,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    1203: _tools.RODict({
        "ID": 1203,
        "type": 1,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    1204: _tools.RODict({
        "ID": 1204,
        "type": 1,
        "quality": 2,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    1205: _tools.RODict({
        "ID": 1205,
        "type": 1,
        "quality": 2,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    1301: _tools.RODict({
        "ID": 1301,
        "type": 1,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    1302: _tools.RODict({
        "ID": 1302,
        "type": 1,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    1303: _tools.RODict({
        "ID": 1303,
        "type": 1,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    1304: _tools.RODict({
        "ID": 1304,
        "type": 1,
        "quality": 3,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    1305: _tools.RODict({
        "ID": 1305,
        "type": 1,
        "quality": 3,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    1401: _tools.RODict({
        "ID": 1401,
        "type": 1,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    1402: _tools.RODict({
        "ID": 1402,
        "type": 1,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    1403: _tools.RODict({
        "ID": 1403,
        "type": 1,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    1404: _tools.RODict({
        "ID": 1404,
        "type": 1,
        "quality": 4,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    1405: _tools.RODict({
        "ID": 1405,
        "type": 1,
        "quality": 4,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    2101: _tools.RODict({
        "ID": 2101,
        "type": 2,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    2102: _tools.RODict({
        "ID": 2102,
        "type": 2,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    2103: _tools.RODict({
        "ID": 2103,
        "type": 2,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    2104: _tools.RODict({
        "ID": 2104,
        "type": 2,
        "quality": 1,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    2105: _tools.RODict({
        "ID": 2105,
        "type": 2,
        "quality": 1,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    2201: _tools.RODict({
        "ID": 2201,
        "type": 2,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    2202: _tools.RODict({
        "ID": 2202,
        "type": 2,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    2203: _tools.RODict({
        "ID": 2203,
        "type": 2,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    2204: _tools.RODict({
        "ID": 2204,
        "type": 2,
        "quality": 2,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    2205: _tools.RODict({
        "ID": 2205,
        "type": 2,
        "quality": 2,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    2301: _tools.RODict({
        "ID": 2301,
        "type": 2,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    2302: _tools.RODict({
        "ID": 2302,
        "type": 2,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    2303: _tools.RODict({
        "ID": 2303,
        "type": 2,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    2304: _tools.RODict({
        "ID": 2304,
        "type": 2,
        "quality": 3,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    2305: _tools.RODict({
        "ID": 2305,
        "type": 2,
        "quality": 3,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    2401: _tools.RODict({
        "ID": 2401,
        "type": 2,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    2402: _tools.RODict({
        "ID": 2402,
        "type": 2,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    2403: _tools.RODict({
        "ID": 2403,
        "type": 2,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    2404: _tools.RODict({
        "ID": 2404,
        "type": 2,
        "quality": 4,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    2405: _tools.RODict({
        "ID": 2405,
        "type": 2,
        "quality": 4,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    3101: _tools.RODict({
        "ID": 3101,
        "type": 3,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    3102: _tools.RODict({
        "ID": 3102,
        "type": 3,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    3103: _tools.RODict({
        "ID": 3103,
        "type": 3,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    3104: _tools.RODict({
        "ID": 3104,
        "type": 3,
        "quality": 1,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    3105: _tools.RODict({
        "ID": 3105,
        "type": 3,
        "quality": 1,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    3201: _tools.RODict({
        "ID": 3201,
        "type": 3,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    3202: _tools.RODict({
        "ID": 3202,
        "type": 3,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    3203: _tools.RODict({
        "ID": 3203,
        "type": 3,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    3204: _tools.RODict({
        "ID": 3204,
        "type": 3,
        "quality": 2,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    3205: _tools.RODict({
        "ID": 3205,
        "type": 3,
        "quality": 2,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    3301: _tools.RODict({
        "ID": 3301,
        "type": 3,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    3302: _tools.RODict({
        "ID": 3302,
        "type": 3,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    3303: _tools.RODict({
        "ID": 3303,
        "type": 3,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    3304: _tools.RODict({
        "ID": 3304,
        "type": 3,
        "quality": 3,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    3305: _tools.RODict({
        "ID": 3305,
        "type": 3,
        "quality": 3,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    3401: _tools.RODict({
        "ID": 3401,
        "type": 3,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    3402: _tools.RODict({
        "ID": 3402,
        "type": 3,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    3403: _tools.RODict({
        "ID": 3403,
        "type": 3,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    3404: _tools.RODict({
        "ID": 3404,
        "type": 3,
        "quality": 4,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    3405: _tools.RODict({
        "ID": 3405,
        "type": 3,
        "quality": 4,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    4101: _tools.RODict({
        "ID": 4101,
        "type": 4,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    4102: _tools.RODict({
        "ID": 4102,
        "type": 4,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    4103: _tools.RODict({
        "ID": 4103,
        "type": 4,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    4104: _tools.RODict({
        "ID": 4104,
        "type": 4,
        "quality": 1,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    4105: _tools.RODict({
        "ID": 4105,
        "type": 4,
        "quality": 1,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    4201: _tools.RODict({
        "ID": 4201,
        "type": 4,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    4202: _tools.RODict({
        "ID": 4202,
        "type": 4,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    4203: _tools.RODict({
        "ID": 4203,
        "type": 4,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    4204: _tools.RODict({
        "ID": 4204,
        "type": 4,
        "quality": 2,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    4205: _tools.RODict({
        "ID": 4205,
        "type": 4,
        "quality": 2,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    4301: _tools.RODict({
        "ID": 4301,
        "type": 4,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    4302: _tools.RODict({
        "ID": 4302,
        "type": 4,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    4303: _tools.RODict({
        "ID": 4303,
        "type": 4,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    4304: _tools.RODict({
        "ID": 4304,
        "type": 4,
        "quality": 3,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    4305: _tools.RODict({
        "ID": 4305,
        "type": 4,
        "quality": 3,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    4401: _tools.RODict({
        "ID": 4401,
        "type": 4,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    4402: _tools.RODict({
        "ID": 4402,
        "type": 4,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    4403: _tools.RODict({
        "ID": 4403,
        "type": 4,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    4404: _tools.RODict({
        "ID": 4404,
        "type": 4,
        "quality": 4,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    4405: _tools.RODict({
        "ID": 4405,
        "type": 4,
        "quality": 4,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    5101: _tools.RODict({
        "ID": 5101,
        "type": 5,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    5102: _tools.RODict({
        "ID": 5102,
        "type": 5,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    5103: _tools.RODict({
        "ID": 5103,
        "type": 5,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    5104: _tools.RODict({
        "ID": 5104,
        "type": 5,
        "quality": 1,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    5105: _tools.RODict({
        "ID": 5105,
        "type": 5,
        "quality": 1,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    5201: _tools.RODict({
        "ID": 5201,
        "type": 5,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    5202: _tools.RODict({
        "ID": 5202,
        "type": 5,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    5203: _tools.RODict({
        "ID": 5203,
        "type": 5,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    5204: _tools.RODict({
        "ID": 5204,
        "type": 5,
        "quality": 2,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    5205: _tools.RODict({
        "ID": 5205,
        "type": 5,
        "quality": 2,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    5301: _tools.RODict({
        "ID": 5301,
        "type": 5,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    5302: _tools.RODict({
        "ID": 5302,
        "type": 5,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    5303: _tools.RODict({
        "ID": 5303,
        "type": 5,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    5304: _tools.RODict({
        "ID": 5304,
        "type": 5,
        "quality": 3,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    5305: _tools.RODict({
        "ID": 5305,
        "type": 5,
        "quality": 3,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    5401: _tools.RODict({
        "ID": 5401,
        "type": 5,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    5402: _tools.RODict({
        "ID": 5402,
        "type": 5,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    5403: _tools.RODict({
        "ID": 5403,
        "type": 5,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    5404: _tools.RODict({
        "ID": 5404,
        "type": 5,
        "quality": 4,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    5405: _tools.RODict({
        "ID": 5405,
        "type": 5,
        "quality": 4,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    6101: _tools.RODict({
        "ID": 6101,
        "type": 6,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    6102: _tools.RODict({
        "ID": 6102,
        "type": 6,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    6103: _tools.RODict({
        "ID": 6103,
        "type": 6,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    6104: _tools.RODict({
        "ID": 6104,
        "type": 6,
        "quality": 1,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    6105: _tools.RODict({
        "ID": 6105,
        "type": 6,
        "quality": 1,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    6201: _tools.RODict({
        "ID": 6201,
        "type": 6,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    6202: _tools.RODict({
        "ID": 6202,
        "type": 6,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    6203: _tools.RODict({
        "ID": 6203,
        "type": 6,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    6204: _tools.RODict({
        "ID": 6204,
        "type": 6,
        "quality": 2,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    6205: _tools.RODict({
        "ID": 6205,
        "type": 6,
        "quality": 2,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    6301: _tools.RODict({
        "ID": 6301,
        "type": 6,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    6302: _tools.RODict({
        "ID": 6302,
        "type": 6,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    6303: _tools.RODict({
        "ID": 6303,
        "type": 6,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    6304: _tools.RODict({
        "ID": 6304,
        "type": 6,
        "quality": 3,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    6305: _tools.RODict({
        "ID": 6305,
        "type": 6,
        "quality": 3,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    6401: _tools.RODict({
        "ID": 6401,
        "type": 6,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    6402: _tools.RODict({
        "ID": 6402,
        "type": 6,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    6403: _tools.RODict({
        "ID": 6403,
        "type": 6,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    6404: _tools.RODict({
        "ID": 6404,
        "type": 6,
        "quality": 4,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    6405: _tools.RODict({
        "ID": 6405,
        "type": 6,
        "quality": 4,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    7101: _tools.RODict({
        "ID": 7101,
        "type": 7,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    7102: _tools.RODict({
        "ID": 7102,
        "type": 7,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    7103: _tools.RODict({
        "ID": 7103,
        "type": 7,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    7104: _tools.RODict({
        "ID": 7104,
        "type": 7,
        "quality": 1,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    7105: _tools.RODict({
        "ID": 7105,
        "type": 7,
        "quality": 1,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    7201: _tools.RODict({
        "ID": 7201,
        "type": 7,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    7202: _tools.RODict({
        "ID": 7202,
        "type": 7,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    7203: _tools.RODict({
        "ID": 7203,
        "type": 7,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    7204: _tools.RODict({
        "ID": 7204,
        "type": 7,
        "quality": 2,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    7205: _tools.RODict({
        "ID": 7205,
        "type": 7,
        "quality": 2,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    7301: _tools.RODict({
        "ID": 7301,
        "type": 7,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    7302: _tools.RODict({
        "ID": 7302,
        "type": 7,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    7303: _tools.RODict({
        "ID": 7303,
        "type": 7,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    7304: _tools.RODict({
        "ID": 7304,
        "type": 7,
        "quality": 3,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    7305: _tools.RODict({
        "ID": 7305,
        "type": 7,
        "quality": 3,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    7401: _tools.RODict({
        "ID": 7401,
        "type": 7,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    7402: _tools.RODict({
        "ID": 7402,
        "type": 7,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    7403: _tools.RODict({
        "ID": 7403,
        "type": 7,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    7404: _tools.RODict({
        "ID": 7404,
        "type": 7,
        "quality": 4,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    7405: _tools.RODict({
        "ID": 7405,
        "type": 7,
        "quality": 4,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    8101: _tools.RODict({
        "ID": 8101,
        "type": 8,
        "quality": 1,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    8102: _tools.RODict({
        "ID": 8102,
        "type": 8,
        "quality": 1,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    8103: _tools.RODict({
        "ID": 8103,
        "type": 8,
        "quality": 1,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    8104: _tools.RODict({
        "ID": 8104,
        "type": 8,
        "quality": 1,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    8105: _tools.RODict({
        "ID": 8105,
        "type": 8,
        "quality": 1,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    8201: _tools.RODict({
        "ID": 8201,
        "type": 8,
        "quality": 2,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    8202: _tools.RODict({
        "ID": 8202,
        "type": 8,
        "quality": 2,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    8203: _tools.RODict({
        "ID": 8203,
        "type": 8,
        "quality": 2,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    8204: _tools.RODict({
        "ID": 8204,
        "type": 8,
        "quality": 2,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    8205: _tools.RODict({
        "ID": 8205,
        "type": 8,
        "quality": 2,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    8301: _tools.RODict({
        "ID": 8301,
        "type": 8,
        "quality": 3,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    8302: _tools.RODict({
        "ID": 8302,
        "type": 8,
        "quality": 3,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    8303: _tools.RODict({
        "ID": 8303,
        "type": 8,
        "quality": 3,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    8304: _tools.RODict({
        "ID": 8304,
        "type": 8,
        "quality": 3,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    8305: _tools.RODict({
        "ID": 8305,
        "type": 8,
        "quality": 3,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    }),
    8401: _tools.RODict({
        "ID": 8401,
        "type": 8,
        "quality": 4,
        "level": 1,
        "costCurrency": ((30000013, 40),)
    }),
    8402: _tools.RODict({
        "ID": 8402,
        "type": 8,
        "quality": 4,
        "level": 2,
        "costCurrency": ((30000013, 100),)
    }),
    8403: _tools.RODict({
        "ID": 8403,
        "type": 8,
        "quality": 4,
        "level": 3,
        "costCurrency": ((30000013, 200),)
    }),
    8404: _tools.RODict({
        "ID": 8404,
        "type": 8,
        "quality": 4,
        "level": 4,
        "costCurrency": ((30000013, 400),)
    }),
    8405: _tools.RODict({
        "ID": 8405,
        "type": 8,
        "quality": 4,
        "level": 5,
        "costCurrency": ((30000013, 1200),)
    })
})
minKey = 1101
maxKey = 8405