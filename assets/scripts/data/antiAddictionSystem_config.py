# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: antiAddictionSystem/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "userAge": _tools.RODict({
        "ID": "userAge",
        "value": 18,
    }),
    "dailyMaxDuration": _tools.RODict({
        "ID": "dailyMaxDuration",
        "value": 60,
    }),
    "allowedPeriodStart": _tools.RODict({
        "ID": "allowedPeriodStart",
        "value": _tools.ROList([[[0], [20], [], [], [], []]]),
    }),
    "allowedPeriodEnd": _tools.RODict({
        "ID": "allowedPeriodEnd",
        "value": _tools.ROList([[[0], [21], [], [], [], []]]),
    }),
    "allowedPeriodDayStart": _tools.RODict({
        "ID": "allowedPeriodDayStart",
        "value": _tools.ROList([[[0], [20], [], [], [0, 5, 6], []]]),
    }),
    "allowedPeriodDayEnd": _tools.RODict({
        "ID": "allowedPeriodDayEnd",
        "value": _tools.ROList([[[0], [21], [], [], [0, 5, 6], []]]),
    }),
    "reminderTime": _tools.RODict({
        "ID": "reminderTime",
        "value": 15,
    }),
    "reminderTimeMsg": _tools.RODict({
        "ID": "reminderTimeMsg",
        "value": 54002013,
    }),
    "antiAddictForbiddenTime": _tools.RODict({
        "ID": "antiAddictForbiddenTime",
        "value": 54002002,
    }),
    "antiAddictForceLogout": _tools.RODict({
        "ID": "antiAddictForceLogout",
        "value": 54002003,
    }),
    "antiAddictAgeUnder18": _tools.RODict({
        "ID": "antiAddictAgeUnder18",
        "value": 54002014,
    }),
    "antiAddictSwitchAge18": _tools.RODict({
        "ID": "antiAddictSwitchAge18",
        "value": 0,
    })
})