# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: title/titleData
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    25000001: _tools.RODict({
        "ID": 25000001,
        "name": "<空>",
        "hudname": "",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 0,
        "levelRequirement": 0,
        "color": 217
    }),
    25000002: _tools.RODict({
        "ID": 25000002,
        "name": "炽焰先驱",
        "hudname": "<炽焰先驱>",
        "type": 1,
        "subType": 2,
        "class": 0,
        "quality": 4,
        "levelRequirement": 0,
        "color": 223
    }),
    25000003: _tools.RODict({
        "ID": 25000003,
        "name": "劳动模范",
        "hudname": "<劳动模范>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000004: _tools.RODict({
        "ID": 25000004,
        "name": "道德标兵",
        "hudname": "<道德标兵>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000005: _tools.RODict({
        "ID": 25000005,
        "name": "素质达人",
        "hudname": "<素质达人>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000006: _tools.RODict({
        "ID": 25000006,
        "name": "奇迹行者",
        "hudname": "<奇迹行者>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 4,
        "levelRequirement": 0,
        "color": 223
    }),
    25000007: _tools.RODict({
        "ID": 25000007,
        "name": "优秀员工",
        "hudname": "<优秀员工>",
        "type": 0,
        "subType": 2,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000008: _tools.RODict({
        "ID": 25000008,
        "name": "名动江湖",
        "hudname": "<名动江湖>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 3,
        "levelRequirement": 50,
        "color": 222
    }),
    25000009: _tools.RODict({
        "ID": 25000009,
        "name": "既寿永昌",
        "hudname": "<既寿永昌>",
        "type": 0,
        "subType": 2,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000010: _tools.RODict({
        "ID": 25000010,
        "name": "智勇双全",
        "hudname": "<智勇双全>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000011: _tools.RODict({
        "ID": 25000011,
        "name": "此生不渝",
        "hudname": "<此生不渝>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000012: _tools.RODict({
        "ID": 25000012,
        "name": "异乡人",
        "hudname": "<异乡人>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000013: _tools.RODict({
        "ID": 25000013,
        "name": "纸醉金迷",
        "hudname": "<纸醉金迷>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000014: _tools.RODict({
        "ID": 25000014,
        "name": "顺我者昌，逆我者亡",
        "hudname": "<顺我者昌，逆我者亡>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 5,
        "levelRequirement": 0,
        "color": 223
    }),
    25000015: _tools.RODict({
        "ID": 25000015,
        "name": "赏金猎人",
        "hudname": "<赏金猎人>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000016: _tools.RODict({
        "ID": 25000016,
        "name": "真假精灵王",
        "hudname": "<真假精灵王>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000017: _tools.RODict({
        "ID": 25000017,
        "name": "我有好酒，四海相邀",
        "hudname": "<我有好酒，四海相邀>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000018: _tools.RODict({
        "ID": 25000018,
        "name": "罪业有报",
        "hudname": "<罪业有报>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000019: _tools.RODict({
        "ID": 25000019,
        "name": "深海魔人",
        "hudname": "<深海魔人>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000020: _tools.RODict({
        "ID": 25000020,
        "name": "浴血奋战",
        "hudname": "<浴血奋战>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000021: _tools.RODict({
        "ID": 25000021,
        "name": "速通达人",
        "hudname": "<速通达人>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000022: _tools.RODict({
        "ID": 25000022,
        "name": "一刀999",
        "hudname": "<一刀999>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000023: _tools.RODict({
        "ID": 25000023,
        "name": "身价过亿",
        "hudname": "<身价过亿>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000024: _tools.RODict({
        "ID": 25000024,
        "name": "驯龙高手",
        "hudname": "<驯龙高手>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000025: _tools.RODict({
        "ID": 25000025,
        "name": "孤胆英雄",
        "hudname": "<孤胆英雄>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000026: _tools.RODict({
        "ID": 25000026,
        "name": "金色传说",
        "hudname": "<金色传说>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000027: _tools.RODict({
        "ID": 25000027,
        "name": "早上好尤其是你",
        "hudname": "<早上好尤其是你>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000028: _tools.RODict({
        "ID": 25000028,
        "name": "万赏风华",
        "hudname": "<万赏风华>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000029: _tools.RODict({
        "ID": 25000029,
        "name": "四牡翼翼",
        "hudname": "<四牡翼翼>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000030: _tools.RODict({
        "ID": 25000030,
        "name": "广纳贤才",
        "hudname": "<广纳贤才>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000031: _tools.RODict({
        "ID": 25000031,
        "name": "登峰造极",
        "hudname": "<登峰造极>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 5,
        "levelRequirement": 0,
        "color": 223
    }),
    25000032: _tools.RODict({
        "ID": 25000032,
        "name": "巅峰强者",
        "hudname": "<巅峰强者>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 5,
        "levelRequirement": 0,
        "color": 223
    }),
    25000033: _tools.RODict({
        "ID": 25000033,
        "name": "万赖神通",
        "hudname": "<万赖神通>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 5,
        "levelRequirement": 0,
        "color": 223
    }),
    25000034: _tools.RODict({
        "ID": 25000034,
        "name": "威霸一方",
        "hudname": "<威霸一方>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 5,
        "levelRequirement": 0,
        "color": 223
    }),
    25000035: _tools.RODict({
        "ID": 25000035,
        "name": "只此一刀",
        "hudname": "<只此一刀>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000036: _tools.RODict({
        "ID": 25000036,
        "name": "小试牛刀",
        "hudname": "<小试牛刀>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 20,
        "color": 215
    }),
    25000037: _tools.RODict({
        "ID": 25000037,
        "name": "侠风隐现",
        "hudname": "<侠风隐现>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 30,
        "color": 215
    }),
    25000038: _tools.RODict({
        "ID": 25000038,
        "name": "一方豪杰",
        "hudname": "<一方豪杰>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 40,
        "color": 217
    }),
    25000039: _tools.RODict({
        "ID": 25000039,
        "name": "传奇入世",
        "hudname": "<传奇入世>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 60,
        "color": 217
    }),
    25000040: _tools.RODict({
        "ID": 25000040,
        "name": "超凡显圣",
        "hudname": "<超凡显圣>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 70,
        "color": 222
    }),
    25000041: _tools.RODict({
        "ID": 25000041,
        "name": "宗门至尊",
        "hudname": "<宗门至尊>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 80,
        "color": 222
    }),
    25000042: _tools.RODict({
        "ID": 25000042,
        "name": "自在行者",
        "hudname": "<自在行者>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 5,
        "levelRequirement": 90,
        "color": 223
    }),
    25000043: _tools.RODict({
        "ID": 25000043,
        "name": "神话无双",
        "hudname": "<神话无双>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 5,
        "levelRequirement": 100,
        "color": 223
    }),
    25000044: _tools.RODict({
        "ID": 25000044,
        "name": "挂机仙人",
        "hudname": "<挂机仙人>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000045: _tools.RODict({
        "ID": 25000045,
        "name": "我就看看",
        "hudname": "<我就看看>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000046: _tools.RODict({
        "ID": 25000046,
        "name": "烽火鎏金",
        "hudname": "<烽火鎏金>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 5,
        "levelRequirement": 0,
        "color": 223
    }),
    25000047: _tools.RODict({
        "ID": 25000047,
        "name": "概率是你的谎言",
        "hudname": "<概率是你的谎言>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000048: _tools.RODict({
        "ID": 25000048,
        "name": "黄金矿工",
        "hudname": "<黄金矿工>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000049: _tools.RODict({
        "ID": 25000049,
        "name": "法外狂徒",
        "hudname": "<法外狂徒>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000050: _tools.RODict({
        "ID": 25000050,
        "name": "都是兄弟",
        "hudname": "<都是兄弟>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000051: _tools.RODict({
        "ID": 25000051,
        "name": "百折不挠",
        "hudname": "<百折不挠>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000052: _tools.RODict({
        "ID": 25000052,
        "name": "万物皆为我所用",
        "hudname": "<万物皆为我所用>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000053: _tools.RODict({
        "ID": 25000053,
        "name": "千锤百炼",
        "hudname": "<千锤百炼>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000054: _tools.RODict({
        "ID": 25000054,
        "name": "腰缠万贯",
        "hudname": "<腰缠万贯>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000055: _tools.RODict({
        "ID": 25000055,
        "name": "性情中人",
        "hudname": "<性情中人>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000056: _tools.RODict({
        "ID": 25000056,
        "name": "同源异命",
        "hudname": "<同源异命>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000057: _tools.RODict({
        "ID": 25000057,
        "name": "走不了一点",
        "hudname": "<走不了一点>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000058: _tools.RODict({
        "ID": 25000058,
        "name": "吾儿勇乎",
        "hudname": "<吾儿勇乎>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    })
})
minKey = 25000001
maxKey = 25000058