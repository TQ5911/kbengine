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
        "name": "流沙客",
        "hudname": "<流沙客>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000004: _tools.RODict({
        "ID": 25000004,
        "name": "孤勇者",
        "hudname": "<孤勇者>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000005: _tools.RODict({
        "ID": 25000005,
        "name": "石窟探客",
        "hudname": "<石窟探客>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000006: _tools.RODict({
        "ID": 25000006,
        "name": "归心之人",
        "hudname": "<归心之人>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000007: _tools.RODict({
        "ID": 25000007,
        "name": "天煞孤星",
        "hudname": "<天煞孤星>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000008: _tools.RODict({
        "ID": 25000008,
        "name": "同道殊途",
        "hudname": "<同道殊途>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000009: _tools.RODict({
        "ID": 25000009,
        "name": "异乡人",
        "hudname": "<异乡人>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000010: _tools.RODict({
        "ID": 25000010,
        "name": "溯魔求真",
        "hudname": "<溯魔求真>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000011: _tools.RODict({
        "ID": 25000011,
        "name": "此生不渝",
        "hudname": "<此生不渝>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000012: _tools.RODict({
        "ID": 25000012,
        "name": "驱魔人",
        "hudname": "<驱魔人>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000013: _tools.RODict({
        "ID": 25000013,
        "name": "暗流行者",
        "hudname": "<暗流行者>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000014: _tools.RODict({
        "ID": 25000014,
        "name": "智勇双全",
        "hudname": "<智勇双全>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000015: _tools.RODict({
        "ID": 25000015,
        "name": "全村的希望",
        "hudname": "<全村的希望>",
        "type": 0,
        "subType": 0,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000016: _tools.RODict({
        "ID": 25000016,
        "name": "初入江湖",
        "hudname": "<初入江湖>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000017: _tools.RODict({
        "ID": 25000017,
        "name": "侠风隐现",
        "hudname": "<侠风隐现>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000018: _tools.RODict({
        "ID": 25000018,
        "name": "一方好手",
        "hudname": "<一方好手>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000019: _tools.RODict({
        "ID": 25000019,
        "name": "名震一方",
        "hudname": "<名震一方>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000020: _tools.RODict({
        "ID": 25000020,
        "name": "威震八方",
        "hudname": "<威震八方>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000021: _tools.RODict({
        "ID": 25000021,
        "name": "独步天下",
        "hudname": "<独步天下>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000022: _tools.RODict({
        "ID": 25000022,
        "name": "自在行者",
        "hudname": "<自在行者>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000023: _tools.RODict({
        "ID": 25000023,
        "name": "一代宗师",
        "hudname": "<一代宗师>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000024: _tools.RODict({
        "ID": 25000024,
        "name": "剑不离手",
        "hudname": "<剑不离手>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000025: _tools.RODict({
        "ID": 25000025,
        "name": "全勤达人",
        "hudname": "<全勤达人>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000026: _tools.RODict({
        "ID": 25000026,
        "name": "风雨同舟",
        "hudname": "<风雨同舟>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000027: _tools.RODict({
        "ID": 25000027,
        "name": "义结金兰",
        "hudname": "<义结金兰>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000028: _tools.RODict({
        "ID": 25000028,
        "name": "八方来朋",
        "hudname": "<八方来朋>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000029: _tools.RODict({
        "ID": 25000029,
        "name": "一呼百应",
        "hudname": "<一呼百应>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000030: _tools.RODict({
        "ID": 25000030,
        "name": "江湖初现",
        "hudname": "<江湖初现>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000031: _tools.RODict({
        "ID": 25000031,
        "name": "法外狂徒",
        "hudname": "<法外狂徒>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000032: _tools.RODict({
        "ID": 25000032,
        "name": "江湖公敌",
        "hudname": "<江湖公敌>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000033: _tools.RODict({
        "ID": 25000033,
        "name": "孔雀东南飞",
        "hudname": "<孔雀东南飞>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000034: _tools.RODict({
        "ID": 25000034,
        "name": "初入门道",
        "hudname": "<初入门道>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000035: _tools.RODict({
        "ID": 25000035,
        "name": "技艺非凡",
        "hudname": "<技艺非凡>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000036: _tools.RODict({
        "ID": 25000036,
        "name": "神功大成",
        "hudname": "<神功大成>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000037: _tools.RODict({
        "ID": 25000037,
        "name": "采矿达人",
        "hudname": "<采矿达人>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000038: _tools.RODict({
        "ID": 25000038,
        "name": "黄金矿工",
        "hudname": "<黄金矿工>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000039: _tools.RODict({
        "ID": 25000039,
        "name": "矿业大亨",
        "hudname": "<矿业大亨>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000040: _tools.RODict({
        "ID": 25000040,
        "name": "大巧不工",
        "hudname": "<大巧不工>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000041: _tools.RODict({
        "ID": 25000041,
        "name": "千锤百炼",
        "hudname": "<千锤百炼>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000042: _tools.RODict({
        "ID": 25000042,
        "name": "神装天成",
        "hudname": "<神装天成>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000043: _tools.RODict({
        "ID": 25000043,
        "name": "好运降临",
        "hudname": "<好运降临>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000044: _tools.RODict({
        "ID": 25000044,
        "name": "神器语者",
        "hudname": "<神器语者>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000045: _tools.RODict({
        "ID": 25000045,
        "name": "神光乍现",
        "hudname": "<神光乍现>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000046: _tools.RODict({
        "ID": 25000046,
        "name": "符文战士",
        "hudname": "<符文战士>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000047: _tools.RODict({
        "ID": 25000047,
        "name": "断金刻玉",
        "hudname": "<断金刻玉>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000048: _tools.RODict({
        "ID": 25000048,
        "name": "武道至尊",
        "hudname": "<武道至尊>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000049: _tools.RODict({
        "ID": 25000049,
        "name": "滴恩涌报",
        "hudname": "<滴恩涌报>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000050: _tools.RODict({
        "ID": 25000050,
        "name": "忠肝义胆",
        "hudname": "<忠肝义胆>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000051: _tools.RODict({
        "ID": 25000051,
        "name": "开帮元勋",
        "hudname": "<开帮元勋>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000052: _tools.RODict({
        "ID": 25000052,
        "name": "揭榜人",
        "hudname": "<揭榜人>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000053: _tools.RODict({
        "ID": 25000053,
        "name": "赏金常客",
        "hudname": "<赏金常客>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000054: _tools.RODict({
        "ID": 25000054,
        "name": "镇守一方",
        "hudname": "<镇守一方>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000055: _tools.RODict({
        "ID": 25000055,
        "name": "能征善战",
        "hudname": "<能征善战>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000056: _tools.RODict({
        "ID": 25000056,
        "name": "浴血狩魔",
        "hudname": "<浴血狩魔>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000057: _tools.RODict({
        "ID": 25000057,
        "name": "六合八荒",
        "hudname": "<六合八荒>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000058: _tools.RODict({
        "ID": 25000058,
        "name": "技高一筹",
        "hudname": "<技高一筹>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000059: _tools.RODict({
        "ID": 25000059,
        "name": "名震四海",
        "hudname": "<名震四海>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000060: _tools.RODict({
        "ID": 25000060,
        "name": "笑傲江湖",
        "hudname": "<笑傲江湖>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000061: _tools.RODict({
        "ID": 25000061,
        "name": "初入混沌",
        "hudname": "<初入混沌>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000062: _tools.RODict({
        "ID": 25000062,
        "name": "时空旅者",
        "hudname": "<时空旅者>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000063: _tools.RODict({
        "ID": 25000063,
        "name": "神游太虚",
        "hudname": "<神游太虚>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000064: _tools.RODict({
        "ID": 25000064,
        "name": "寻宝者",
        "hudname": "<寻宝者>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000065: _tools.RODict({
        "ID": 25000065,
        "name": "历劫百转",
        "hudname": "<历劫百转>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000066: _tools.RODict({
        "ID": 25000066,
        "name": "天劫渡厄",
        "hudname": "<天劫渡厄>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000067: _tools.RODict({
        "ID": 25000067,
        "name": "锐不可当",
        "hudname": "<锐不可当>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000068: _tools.RODict({
        "ID": 25000068,
        "name": "雄踞山河",
        "hudname": "<雄踞山河>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000069: _tools.RODict({
        "ID": 25000069,
        "name": "无上尊者",
        "hudname": "<无上尊者>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 4,
        "levelRequirement": 0,
        "color": 223
    }),
    25000070: _tools.RODict({
        "ID": 25000070,
        "name": "精良之战",
        "hudname": "<精良之战>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000071: _tools.RODict({
        "ID": 25000071,
        "name": "史诗之躯",
        "hudname": "<史诗之躯>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000072: _tools.RODict({
        "ID": 25000072,
        "name": "传说之体",
        "hudname": "<传说之体>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 4,
        "levelRequirement": 0,
        "color": 223
    }),
    25000073: _tools.RODict({
        "ID": 25000073,
        "name": "精锻有方",
        "hudname": "<精锻有方>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000074: _tools.RODict({
        "ID": 25000074,
        "name": "气运之子",
        "hudname": "<气运之子>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 4,
        "levelRequirement": 0,
        "color": 223
    }),
    25000075: _tools.RODict({
        "ID": 25000075,
        "name": "百灵之友",
        "hudname": "<百灵之友>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000076: _tools.RODict({
        "ID": 25000076,
        "name": "千灵之契",
        "hudname": "<千灵之契>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000077: _tools.RODict({
        "ID": 25000077,
        "name": "万灵之主",
        "hudname": "<万灵之主>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000078: _tools.RODict({
        "ID": 25000078,
        "name": "生意人",
        "hudname": "<生意人>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000079: _tools.RODict({
        "ID": 25000079,
        "name": "金玉盈室",
        "hudname": "<金玉盈室>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000080: _tools.RODict({
        "ID": 25000080,
        "name": "富可敌国",
        "hudname": "<富可敌国>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 4,
        "levelRequirement": 0,
        "color": 223
    }),
    25000081: _tools.RODict({
        "ID": 25000081,
        "name": "拾遗客",
        "hudname": "<拾遗客>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000082: _tools.RODict({
        "ID": 25000082,
        "name": "格物致知",
        "hudname": "<格物致知>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000083: _tools.RODict({
        "ID": 25000083,
        "name": "博览万象",
        "hudname": "<博览万象>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    }),
    25000084: _tools.RODict({
        "ID": 25000084,
        "name": "四兽之尊",
        "hudname": "<四兽之尊>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 1,
        "levelRequirement": 0,
        "color": 215
    }),
    25000085: _tools.RODict({
        "ID": 25000085,
        "name": "北斗七乘",
        "hudname": "<北斗七乘>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 2,
        "levelRequirement": 0,
        "color": 217
    }),
    25000086: _tools.RODict({
        "ID": 25000086,
        "name": "十方御主",
        "hudname": "<十方御主>",
        "type": 0,
        "subType": 1,
        "class": 0,
        "quality": 3,
        "levelRequirement": 0,
        "color": 222
    })
})
minKey = 25000001
maxKey = 25000086