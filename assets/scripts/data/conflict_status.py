# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: conflict/status
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    0: _tools.RODict({
        "ID": 0,
        "varName": "idle",
        "statusName": "待机",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100003,
        "buffTag": 0,
        "popupIndex": 0
    }),
    1: _tools.RODict({
        "ID": 1,
        "varName": "Moving",
        "statusName": "移动中",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100005,
        "buffTag": 0,
        "popupIndex": 0
    }),
    2: _tools.RODict({
        "ID": 2,
        "varName": "Shifting",
        "statusName": "位移中",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100004,
        "buffTag": 0,
        "popupIndex": 0
    }),
    3: _tools.RODict({
        "ID": 3,
        "varName": "Fighting",
        "statusName": "战斗中",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100001,
        "buffTag": 0,
        "popupIndex": 0
    }),
    4: _tools.RODict({
        "ID": 4,
        "varName": "Death",
        "statusName": "阵亡",
        "clearOnline": 0,
        "clearTeleport": 0,
        "event": 29100006,
        "buffTag": 0,
        "popupIndex": 0
    }),
    5: _tools.RODict({
        "ID": 5,
        "varName": "Down",
        "statusName": "击倒",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100007,
        "buffTag": 0,
        "popupIndex": 25
    }),
    6: _tools.RODict({
        "ID": 6,
        "varName": "Stunned",
        "statusName": "眩晕",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100008,
        "buffTag": 0,
        "popupIndex": 24
    }),
    7: _tools.RODict({
        "ID": 7,
        "varName": "Slow",
        "statusName": "缓速",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100009,
        "buffTag": 0,
        "popupIndex": 28
    }),
    8: _tools.RODict({
        "ID": 8,
        "varName": "Silenced",
        "statusName": "沉默",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100010,
        "buffTag": 0,
        "popupIndex": 34
    }),
    9: _tools.RODict({
        "ID": 9,
        "varName": "Snare",
        "statusName": "定身",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100011,
        "buffTag": 0,
        "popupIndex": 27
    }),
    10: _tools.RODict({
        "ID": 10,
        "varName": "Frozen",
        "statusName": "冻结",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100012,
        "buffTag": 0,
        "popupIndex": 26
    }),
    11: _tools.RODict({
        "ID": 11,
        "varName": "PImmortal",
        "statusName": "物理免疫",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 0,
        "buffTag": 0,
        "popupIndex": 0
    }),
    12: _tools.RODict({
        "ID": 12,
        "varName": "MImmortal",
        "statusName": "法术免疫",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 0,
        "buffTag": 0,
        "popupIndex": 0
    }),
    13: _tools.RODict({
        "ID": 13,
        "varName": "generalSkill",
        "statusName": "普攻技能状态",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100015,
        "buffTag": 0,
        "popupIndex": 0
    }),
    14: _tools.RODict({
        "ID": 14,
        "varName": "UsingSkill",
        "statusName": "技能状态",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100016,
        "buffTag": 0,
        "popupIndex": 0
    }),
    15: _tools.RODict({
        "ID": 15,
        "varName": "Casting",
        "statusName": "吟唱",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100017,
        "buffTag": 0,
        "popupIndex": 0
    }),
    16: _tools.RODict({
        "ID": 16,
        "varName": "Channeling",
        "statusName": "引导",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100018,
        "buffTag": 0,
        "popupIndex": 0
    }),
    17: _tools.RODict({
        "ID": 17,
        "varName": "moveSkill",
        "statusName": "移动技能",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100019,
        "buffTag": 0,
        "popupIndex": 0
    }),
    18: _tools.RODict({
        "ID": 18,
        "varName": "moveChannel",
        "statusName": "移动引导",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100020,
        "buffTag": 0,
        "popupIndex": 0
    }),
    19: _tools.RODict({
        "ID": 19,
        "varName": "specialSkill",
        "statusName": "特殊技能状态",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100021,
        "buffTag": 0,
        "popupIndex": 0
    }),
    20: _tools.RODict({
        "ID": 20,
        "varName": "Dodging",
        "statusName": "闪避状态",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100022,
        "buffTag": 0,
        "popupIndex": 0
    }),
    21: _tools.RODict({
        "ID": 21,
        "varName": "Jump",
        "statusName": "跳跃",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100024,
        "buffTag": 0,
        "popupIndex": 0
    }),
    22: _tools.RODict({
        "ID": 22,
        "varName": "doubleJump",
        "statusName": "二段跳",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100025,
        "buffTag": 0,
        "popupIndex": 0
    }),
    23: _tools.RODict({
        "ID": 23,
        "varName": "Fall",
        "statusName": "下落",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100026,
        "buffTag": 0,
        "popupIndex": 0
    }),
    24: _tools.RODict({
        "ID": 24,
        "varName": "speedFall",
        "statusName": "千斤坠",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100027,
        "buffTag": 0,
        "popupIndex": 0
    }),
    25: _tools.RODict({
        "ID": 25,
        "varName": "clientPick",
        "statusName": "采集",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100028,
        "buffTag": 0,
        "popupIndex": 0
    }),
    26: _tools.RODict({
        "ID": 26,
        "varName": "Sprinting",
        "statusName": "疾跑中",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100029,
        "buffTag": 0,
        "popupIndex": 0
    }),
    27: _tools.RODict({
        "ID": 27,
        "varName": "teleporting",
        "statusName": "传送吟唱",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100030,
        "buffTag": 0,
        "popupIndex": 0
    }),
    28: _tools.RODict({
        "ID": 28,
        "varName": "Flying",
        "statusName": "飞行中",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100031,
        "buffTag": 0,
        "popupIndex": 0
    }),
    29: _tools.RODict({
        "ID": 29,
        "varName": "Invincibility",
        "statusName": "无敌",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100034,
        "buffTag": 0,
        "popupIndex": 0
    }),
    30: _tools.RODict({
        "ID": 30,
        "varName": "Bating",
        "statusName": "霸体",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100035,
        "buffTag": 0,
        "popupIndex": 0
    }),
    31: _tools.RODict({
        "ID": 31,
        "varName": "bePushed",
        "statusName": "被移动",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100033,
        "buffTag": 0,
        "popupIndex": 0
    }),
    32: _tools.RODict({
        "ID": 32,
        "varName": "TeamFollowing",
        "statusName": "队伍跟随",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100103,
        "buffTag": 0,
        "popupIndex": 0
    }),
    33: _tools.RODict({
        "ID": 33,
        "varName": "riding",
        "statusName": "骑乘",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100037,
        "buffTag": 0,
        "popupIndex": 0
    }),
    34: _tools.RODict({
        "ID": 34,
        "varName": "teleport",
        "statusName": "传送",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100036,
        "buffTag": 0,
        "popupIndex": 0
    }),
    35: _tools.RODict({
        "ID": 35,
        "varName": "relive",
        "statusName": "复活状态",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100039,
        "buffTag": 0,
        "popupIndex": 0
    }),
    36: _tools.RODict({
        "ID": 36,
        "varName": "autoCollect",
        "statusName": "自动采集",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100040,
        "buffTag": 0,
        "popupIndex": 0
    }),
    37: _tools.RODict({
        "ID": 37,
        "varName": "autoFight",
        "statusName": "自动战斗",
        "clearOnline": 1,
        "clearTeleport": 0,
        "event": 29100104,
        "buffTag": 0,
        "popupIndex": 0
    }),
    38: _tools.RODict({
        "ID": 38,
        "varName": "blazing",
        "statusName": "疾掠中",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100041,
        "buffTag": 0,
        "popupIndex": 0
    }),
    43: _tools.RODict({
        "ID": 43,
        "varName": "serverControl",
        "statusName": "服务器控制",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100105,
        "buffTag": 0,
        "popupIndex": 0
    }),
    44: _tools.RODict({
        "ID": 44,
        "varName": "duel",
        "statusName": "切磋",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100106,
        "buffTag": 0,
        "popupIndex": 0
    }),
    45: _tools.RODict({
        "ID": 45,
        "varName": "silenceImmunity",
        "statusName": "沉默免疫",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 0,
        "buffTag": 0,
        "popupIndex": 0
    }),
    46: _tools.RODict({
        "ID": 46,
        "varName": "unstuck",
        "statusName": "脱离卡死",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100111,
        "buffTag": 0,
        "popupIndex": 0
    }),
    47: _tools.RODict({
        "ID": 47,
        "varName": "posture",
        "statusName": "表情动作",
        "clearOnline": 1,
        "clearTeleport": 1,
        "event": 29100112,
        "buffTag": 0,
        "popupIndex": 0
    })
})
minKey = 0
maxKey = 47

eventToStateDic = _tools.RODict({ 
        "29100003":0,
        "29100005":1,
        "29100004":2,
        "29100001":3,
        "29100006":4,
        "29100007":5,
        "29100008":6,
        "29100009":7,
        "29100010":8,
        "29100011":9,
        "29100012":10,
        "29100015":13,
        "29100016":14,
        "29100017":15,
        "29100018":16,
        "29100019":17,
        "29100020":18,
        "29100021":19,
        "29100022":20,
        "29100024":21,
        "29100025":22,
        "29100026":23,
        "29100027":24,
        "29100028":25,
        "29100029":26,
        "29100030":27,
        "29100031":28,
        "29100034":29,
        "29100035":30,
        "29100033":31,
        "29100103":32,
        "29100037":33,
        "29100036":34,
        "29100039":35,
        "29100040":36,
        "29100104":37,
        "29100041":38,
        "29100105":43,
        "29100106":44,
        "29100111":46,
        "29100112":47,
})
