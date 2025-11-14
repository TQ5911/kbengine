# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: message/mineBattleLog
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
        "name": "mineBattle_noRecord",
        "log": "近期暂无活动"
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "mineBattle_occupyRecord",
        "log": "经过浴血奋战，帮主<color=#F3D58F>{0}</color>率领帮众占领了<color=#038304>{1}</color>矿区"
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "mineBattle_flagDamageRecord1",
        "log": "<color=#038304>{0}</color>帮会的<color=#F3D58F>{1}</color>破坏了矿区荣誉旗帜，地面散落了众多宝箱”"
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "mineBattle_flagDamageRecord2",
        "log": "矿区荣誉旗帜被破坏，本周已被破坏<color=#038304>{0}/{1}</color>次，<color=#038304>{2}</color>帮会权威受到挑战"
    }),
    5: _tools.RODict({
        "ID": 5,
        "name": "mineBattle_flagDamageRecord3",
        "log": "矿区荣誉旗帜被破坏，本周已被破坏<color=#038304>{0}/{1}</color>次，<color=#038304>{2}</color>帮会颜面扫地，不再获得矿区额外收益"
    })
})
minKey = 1
maxKey = 5