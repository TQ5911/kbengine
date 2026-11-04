# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: buyCredit/premiumGoods
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
        "name": "大月卡",
        "itemId": 0,
        "costItemFirst": (30000001, 380),
        "costItem": (30000001, 980),
        "activateItem": 30000317,
        "reward": 40000156,
        "dailyReward": 40000157,
        "passGroupID": 0
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "小月卡",
        "itemId": 0,
        "costItemFirst": (30000001, 180),
        "costItem": (30000001, 380),
        "activateItem": 30000318,
        "reward": 40000193,
        "dailyReward": 40000194,
        "passGroupID": 0
    }),
    26090102: _tools.RODict({
        "ID": 26090102,
        "name": "26年9月战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000601,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 20260901
    }),
    26090103: _tools.RODict({
        "ID": 26090103,
        "name": "26年9月战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000602,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 20260901
    }),
    26100102: _tools.RODict({
        "ID": 26100102,
        "name": "26年10月战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000603,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 20261001
    }),
    26100103: _tools.RODict({
        "ID": 26100103,
        "name": "26年10月战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000604,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 20261001
    }),
    26110102: _tools.RODict({
        "ID": 26110102,
        "name": "26年11月战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000605,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 20261101
    }),
    26110103: _tools.RODict({
        "ID": 26110103,
        "name": "26年11月战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000606,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 20261101
    }),
    10001102: _tools.RODict({
        "ID": 10001102,
        "name": "新服第1期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000613,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100011
    }),
    10001103: _tools.RODict({
        "ID": 10001103,
        "name": "新服第1期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000614,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100011
    }),
    10001202: _tools.RODict({
        "ID": 10001202,
        "name": "新服第2期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000615,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100012
    }),
    10001203: _tools.RODict({
        "ID": 10001203,
        "name": "新服第2期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000616,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100012
    }),
    10001302: _tools.RODict({
        "ID": 10001302,
        "name": "新服第3期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000617,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100013
    }),
    10001303: _tools.RODict({
        "ID": 10001303,
        "name": "新服第3期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000618,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100013
    }),
    10001402: _tools.RODict({
        "ID": 10001402,
        "name": "新服第4期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000625,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100014
    }),
    10001403: _tools.RODict({
        "ID": 10001403,
        "name": "新服第4期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000626,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100014
    }),
    10001502: _tools.RODict({
        "ID": 10001502,
        "name": "新服第5期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000627,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100015
    }),
    10001503: _tools.RODict({
        "ID": 10001503,
        "name": "新服第5期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000628,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100015
    }),
    10001602: _tools.RODict({
        "ID": 10001602,
        "name": "新服第6期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000629,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100016
    }),
    10001603: _tools.RODict({
        "ID": 10001603,
        "name": "新服第6期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000630,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100016
    }),
    10001702: _tools.RODict({
        "ID": 10001702,
        "name": "新服第7期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000631,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100017
    }),
    10001703: _tools.RODict({
        "ID": 10001703,
        "name": "新服第7期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000632,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100017
    }),
    10001802: _tools.RODict({
        "ID": 10001802,
        "name": "新服第8期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000633,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100018
    }),
    10001803: _tools.RODict({
        "ID": 10001803,
        "name": "新服第8期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000634,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100018
    }),
    10001902: _tools.RODict({
        "ID": 10001902,
        "name": "新服第9期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000635,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100019
    }),
    10001903: _tools.RODict({
        "ID": 10001903,
        "name": "新服第9期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000636,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100019
    }),
    10002002: _tools.RODict({
        "ID": 10002002,
        "name": "新服第10期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000637,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100020
    }),
    10002003: _tools.RODict({
        "ID": 10002003,
        "name": "新服第10期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000638,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100020
    }),
    10002102: _tools.RODict({
        "ID": 10002102,
        "name": "新服第11期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000639,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100021
    }),
    10002103: _tools.RODict({
        "ID": 10002103,
        "name": "新服第11期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000640,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100021
    }),
    10002202: _tools.RODict({
        "ID": 10002202,
        "name": "新服第12期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000641,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100022
    }),
    10002203: _tools.RODict({
        "ID": 10002203,
        "name": "新服第12期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000642,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100022
    }),
    10002302: _tools.RODict({
        "ID": 10002302,
        "name": "新服第13期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000643,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100023
    }),
    10002303: _tools.RODict({
        "ID": 10002303,
        "name": "新服第13期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000644,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100023
    }),
    10002402: _tools.RODict({
        "ID": 10002402,
        "name": "新服第14期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000645,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100024
    }),
    10002403: _tools.RODict({
        "ID": 10002403,
        "name": "新服第14期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000646,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100024
    }),
    10002502: _tools.RODict({
        "ID": 10002502,
        "name": "新服第15期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000647,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100025
    }),
    10002503: _tools.RODict({
        "ID": 10002503,
        "name": "新服第15期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000648,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100025
    }),
    10002602: _tools.RODict({
        "ID": 10002602,
        "name": "新服第16期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000649,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100026
    }),
    10002603: _tools.RODict({
        "ID": 10002603,
        "name": "新服第16期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000650,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100026
    }),
    10002702: _tools.RODict({
        "ID": 10002702,
        "name": "新服第17期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000651,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100027
    }),
    10002703: _tools.RODict({
        "ID": 10002703,
        "name": "新服第17期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000652,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100027
    }),
    10002802: _tools.RODict({
        "ID": 10002802,
        "name": "新服第18期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000653,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100028
    }),
    10002803: _tools.RODict({
        "ID": 10002803,
        "name": "新服第18期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000654,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100028
    }),
    10002902: _tools.RODict({
        "ID": 10002902,
        "name": "新服第19期战令-中档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 680),
        "activateItem": 30000655,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100029
    }),
    10002903: _tools.RODict({
        "ID": 10002903,
        "name": "新服第19期战令-高档",
        "itemId": 0,
        "costItemFirst": None,
        "costItem": (30000001, 1280),
        "activateItem": 30000656,
        "reward": 0,
        "dailyReward": 0,
        "passGroupID": 100029
    })
})
minKey = 1
maxKey = 26110103