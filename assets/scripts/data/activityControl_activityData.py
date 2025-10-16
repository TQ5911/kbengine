# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: activityControl/activityData
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab


datas = _tools.RODict({ 
    32000001: _tools.RODict({
        "ID": 32000001,
        "name": "首领讨伐",
        "membersRequire": 15,
        "isOpen": 1,
        "needTeam": 2,
        "refreshMode": 0,
        "activityTime": -1,
        "openLevel": 0,
        "openTimeCron": _tools.ROList([[[], [], [], [], [], []]]),
        "endTimeCron": _tools.ROList([[[], [], [], [], [], []]]),
        "activityTask": 0,
        "openGuildLevel": 1,
        "firstUnlockPush": 1
    }),
    32000002: _tools.RODict({
        "ID": 32000002,
        "name": "混沌回廊",
        "membersRequire": 0,
        "isOpen": 1,
        "needTeam": 0,
        "refreshMode": 0,
        "activityTime": -1,
        "openLevel": 0,
        "openTimeCron": _tools.ROList([[[], [], [], [], [], []]]),
        "endTimeCron": _tools.ROList([[[], [], [], [], [], []]]),
        "activityTask": 0,
        "openGuildLevel": 1,
        "firstUnlockPush": 1
    }),
    32000003: _tools.RODict({
        "ID": 32000003,
        "name": "试炼峰",
        "membersRequire": 0,
        "isOpen": 1,
        "needTeam": 0,
        "refreshMode": 0,
        "activityTime": -1,
        "openLevel": 0,
        "openTimeCron": _tools.ROList([[[0], [0], [], [], [], []]]),
        "endTimeCron": _tools.ROList([[[59], [23], [], [], [], []]]),
        "activityTask": 0,
        "openGuildLevel": 1,
        "firstUnlockPush": 1
    }),
    32000004: _tools.RODict({
        "ID": 32000004,
        "name": "普通讨伐",
        "membersRequire": 5,
        "isOpen": 1,
        "needTeam": 1,
        "refreshMode": 0,
        "activityTime": -1,
        "openLevel": 0,
        "openTimeCron": _tools.ROList([[[], [], [], [], [], []]]),
        "endTimeCron": _tools.ROList([[[], [], [], [], [], []]]),
        "activityTask": 0,
        "openGuildLevel": 1,
        "firstUnlockPush": 1
    })
})

taskId2actId = _tools.RODict({ 
})


unlockNotifyAct = _tools.RODict({ 
        32000001:0,
        32000002:0,
        32000003:0,
        32000004:0,
})


lv2ActId = _tools.RODict({
})
