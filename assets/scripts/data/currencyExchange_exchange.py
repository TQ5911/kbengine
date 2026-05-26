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
        "typeID": 1,
        "currencyFrom": 30000001,
        "currencyTo": 30000002,
        "exchangeType": 0,
        "exchangeRate": 10000,
        "timeLimit": 100,
        "dailyLimit": -1,
    }),
    2: _tools.RODict({
        "ID": 2,
        "typeID": 1,
        "currencyFrom": 30000021,
        "currencyTo": 30000002,
        "exchangeType": 0,
        "exchangeRate": 10000,
        "timeLimit": 100,
        "dailyLimit": -1,
    }),
    3: _tools.RODict({
        "ID": 3,
        "typeID": 2,
        "currencyFrom": 30000001,
        "currencyTo": 30000013,
        "exchangeType": 0,
        "exchangeRate": 100,
        "timeLimit": 100000,
        "dailyLimit": -1,
    }),
    4: _tools.RODict({
        "ID": 4,
        "typeID": 2,
        "currencyFrom": 30000021,
        "currencyTo": 30000013,
        "exchangeType": 0,
        "exchangeRate": 100,
        "timeLimit": 100000,
        "dailyLimit": -1,
    }),
    5: _tools.RODict({
        "ID": 5,
        "typeID": 3,
        "currencyFrom": 30000013,
        "currencyTo": 30000021,
        "exchangeType": 1,
        "exchangeRate": 125,
        "timeLimit": -1,
        "dailyLimit": -1,
    }),
    6: _tools.RODict({
        "ID": 6,
        "typeID": 4,
        "currencyFrom": 30000001,
        "currencyTo": 30000235,
        "exchangeType": 1,
        "exchangeRate": 100,
        "timeLimit": 100,
        "dailyLimit": -1,
    }),
    7: _tools.RODict({
        "ID": 7,
        "typeID": 5,
        "currencyFrom": 30000001,
        "currencyTo": 30000021,
        "exchangeType": 0,
        "exchangeRate": 1,
        "timeLimit": 1000,
        "dailyLimit": -1,
    })
})
minKey = 1
maxKey = 7