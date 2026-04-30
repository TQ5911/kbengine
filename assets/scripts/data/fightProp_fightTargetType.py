# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: fightProp/fightTargetType
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "None": _tools.RODict({
        "ID": "None",
        "value": None
    }),
    "Enemy": _tools.RODict({
        "ID": "Enemy",
        "value": ((0,), (2,), (1,), (0,))
    }),
    "Friend": _tools.RODict({
        "ID": "Friend",
        "value": ((0,), (2,), (2, 3), (0,))
    }),
    "Self": _tools.RODict({
        "ID": "Self",
        "value": ((0,), (2,), (2,), (0,))
    }),
    "Any": _tools.RODict({
        "ID": "Any",
        "value": ((0,), (2,), (0,), (0,))
    }),
    "FriendExGB": _tools.RODict({
        "ID": "FriendExGB",
        "value": ((1, 2, 6, 5), (2,), (2, 3), (0,))
    }),
    "AnyExGB": _tools.RODict({
        "ID": "AnyExGB",
        "value": ((1, 2, 6, 5), (2,), (0,), (0,))
    }),
    "FriendExS": _tools.RODict({
        "ID": "FriendExS",
        "value": ((0,), (2,), (3,), (0,))
    }),
    "CorpsePlayerExS": _tools.RODict({
        "ID": "CorpsePlayerExS",
        "value": ((1,), (1,), (3,), (0,))
    }),
    "Monster": _tools.RODict({
        "ID": "Monster",
        "value": ((2,), (2,), (0,), (0,))
    }),
    "CorpseEnemy": _tools.RODict({
        "ID": "CorpseEnemy",
        "value": ((0,), (1,), (1,), (0,))
    }),
    "FriendPlayerExS": _tools.RODict({
        "ID": "FriendPlayerExS",
        "value": ((1,), (2,), (3,), (0,))
    }),
    "PlayerExS": _tools.RODict({
        "ID": "PlayerExS",
        "value": ((1,), (2,), (1, 3), (0,))
    }),
    "PlayerEnemy": _tools.RODict({
        "ID": "PlayerEnemy",
        "value": ((1,), (2,), (1,), (0,))
    }),
    "EnemyExTarget": _tools.RODict({
        "ID": "EnemyExTarget",
        "value": ((0,), (2,), (5,), (0,))
    }),
    "AnyExs": _tools.RODict({
        "ID": "AnyExs",
        "value": ((0,), (2,), (1, 3), (0,))
    }),
    "CorpseFriend": _tools.RODict({
        "ID": "CorpseFriend",
        "value": ((0,), (0,), (2, 3), (0,))
    }),
    "PlayerExTarget": _tools.RODict({
        "ID": "PlayerExTarget",
        "value": ((0,), (2,), (1,), (0,))
    }),
    "TeamPlayer": _tools.RODict({
        "ID": "TeamPlayer",
        "value": ((1,), (2,), (2, 6), (0,))
    }),
    "TeamFriend": _tools.RODict({
        "ID": "TeamFriend",
        "value": ((1,), (0,), (2, 3), (1, 2, 3))
    }),
    "TeamExCorpse": _tools.RODict({
        "ID": "TeamExCorpse",
        "value": ((1,), (2,), (2, 3), (1, 2, 3))
    })
})