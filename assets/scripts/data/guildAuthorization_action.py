# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guildAuthorization/action
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
        "action": "guildDonateCoin",
        "describe": "捐赠铜币"
    }),
    2: _tools.RODict({
        "ID": 2,
        "action": "guildDonateMoney",
        "describe": "捐赠元宝"
    }),
    3: _tools.RODict({
        "ID": 3,
        "action": "guildHelp",
        "describe": "协助"
    }),
    4: _tools.RODict({
        "ID": 4,
        "action": "guildChallengeEnter",
        "describe": "进入帮会副本"
    })
})
minKey = 1
maxKey = 4

guildDonateCoin = 1
guildDonateMoney = 2
guildHelp = 3
guildChallengeEnter = 4