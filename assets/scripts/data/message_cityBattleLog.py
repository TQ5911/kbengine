# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: message/cityBattleLog
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
        "name": "cityBattle_appointOfficial",
        "log": "<color=#F3D58F>{0}</color>任命<color=#F3D58F>{1}</color>为<color=#038304><link cityBattle job={2}></color>"
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "cityBattle_issueOrder",
        "log": "<color=#F3D58F>{0}</color>颁发了敕令<color=#038304><link cityBattle privilege={1}></color>"
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "cityBattle_rewardTips",
        "log": "<color=#F3D58F>{0}</color>奖赏了<color=#F3D58F>{1}</color><color=#038304><link cityBattle privilege={2}></color>"
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "cityBattle_wantedTips",
        "log": "<color=#F3D58F>{0}</color>对<color=#F3D58F>{1}</color>进行了通缉"
    }),
    5: _tools.RODict({
        "ID": 5,
        "name": "cityBattle_noRecord",
        "log": "近期暂无活动"
    }),
    6: _tools.RODict({
        "ID": 6,
        "name": "cityBattle_orderRecord",
        "log": "<color=#F3D58F>{0}</color>颁发了敕令<color=#038304><link cityBattle privilege={1}></color>,消耗城池元宝{2}"
    }),
    7: _tools.RODict({
        "ID": 7,
        "name": "cityBattle_rewardRecord",
        "log": "<color=#F3D58F>{0}</color>奖赏了<color=#F3D58F>{1}</color><color=#038304><link cityBattle privilege={2}></color>，消耗城池元宝{3}"
    }),
    8: _tools.RODict({
        "ID": 8,
        "name": "cityBattle_wantedRecord",
        "log": "<color=#F3D58F>{0}</color>对<color=#F3D58F>{1}</color>进行了通缉，消耗城池元宝{2}"
    }),
    9: _tools.RODict({
        "ID": 9,
        "name": "cityBattle_convertRecord",
        "log": "<color=#F3D58F>{0}</color>将{1}城池元宝转换为了{2}帮会元宝"
    })
})
minKey = 1
maxKey = 9