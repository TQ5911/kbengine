# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: currencyExchange/exchange
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
        "currencyFrom": 30000001,
        "currencyTo": 30000002,
        "exchangeType": 0,
        "exchangeRate": 10000,
        "timeLimit": 20,
        "dailyLimit": -1
    }),
    2: _tools.RODict({
        "ID": 2,
        "currencyFrom": 30000021,
        "currencyTo": 30000002,
        "exchangeType": 0,
        "exchangeRate": 1000,
        "timeLimit": 100,
        "dailyLimit": 10000
    }),
    3: _tools.RODict({
        "ID": 3,
        "currencyFrom": 30000001,
        "currencyTo": 30000013,
        "exchangeType": 0,
        "exchangeRate": 1000,
        "timeLimit": 100,
        "dailyLimit": -1
    }),
    4: _tools.RODict({
        "ID": 4,
        "currencyFrom": 30000013,
        "currencyTo": 30000021,
        "exchangeType": 1,
        "exchangeRate": 1000,
        "timeLimit": -1,
        "dailyLimit": 50000000
    })
})
minKey = 1
maxKey = 4