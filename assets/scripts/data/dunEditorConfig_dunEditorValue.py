# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: dunEditorConfig/dunEditorValue
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1001: _tools.RODict({
        "ID": 1001,
        "name": "倒计时",
        "value": "exitTime",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "5",
        "listValue": ""
    }),
    1002: _tools.RODict({
        "ID": 1002,
        "name": "前置剩余倒计时",
        "value": "preExitTime",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "120",
        "listValue": ""
    }),
    1011: _tools.RODict({
        "ID": 1011,
        "name": "实例ID",
        "value": "entityID",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1012: _tools.RODict({
        "ID": 1012,
        "name": "数量",
        "value": "num",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    1013: _tools.RODict({
        "ID": 1013,
        "name": "等级",
        "value": "lv",
        "valueType": 1,
        "Type": "string",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    1014: _tools.RODict({
        "ID": 1014,
        "name": "比率",
        "value": "ratio",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    1015: _tools.RODict({
        "ID": 1015,
        "name": "等级限制",
        "value": "lvlmt",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "-1",
        "listValue": ""
    }),
    1016: _tools.RODict({
        "ID": 1016,
        "name": "限时",
        "value": "duration",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "-1",
        "listValue": ""
    }),
    1017: _tools.RODict({
        "ID": 1017,
        "name": "阵营",
        "value": "force",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    1018: _tools.RODict({
        "ID": 1018,
        "name": "初始状态",
        "value": "initState",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    1019: _tools.RODict({
        "ID": 1019,
        "name": "速度",
        "value": "speed",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    1020: _tools.RODict({
        "ID": 1020,
        "name": "移动动作",
        "value": "moveAni",
        "valueType": 2,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": "run01,run02"
    }),
    1021: _tools.RODict({
        "ID": 1021,
        "name": "首次触发延迟",
        "value": "firstDelay",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    1022: _tools.RODict({
        "ID": 1022,
        "name": "每次循环间隔",
        "value": "loopDelay",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    1023: _tools.RODict({
        "ID": 1023,
        "name": "循环次数",
        "value": "loopNum",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    1031: _tools.RODict({
        "ID": 1031,
        "name": "任务ID",
        "value": "taskID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1032: _tools.RODict({
        "ID": 1032,
        "name": "路径ID",
        "value": "pathID",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    1041: _tools.RODict({
        "ID": 1041,
        "name": "怪物实例ID",
        "value": "monsterID",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1042: _tools.RODict({
        "ID": 1042,
        "name": "比较符号",
        "value": "compare",
        "valueType": 2,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": "等于,小于,大于,大于等于,小于等于"
    }),
    1043: _tools.RODict({
        "ID": 1043,
        "name": "血量百分比",
        "value": "hpPercent",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    1044: _tools.RODict({
        "ID": 1044,
        "name": "是否销毁怪物",
        "value": "ifDestroyMonster",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    1051: _tools.RODict({
        "ID": 1051,
        "name": "击杀数量",
        "value": "killNum",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    1061: _tools.RODict({
        "ID": 1061,
        "name": "剩余数量",
        "value": "restNum",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    1071: _tools.RODict({
        "ID": 1071,
        "name": "action",
        "value": "action",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1081: _tools.RODict({
        "ID": 1081,
        "name": "技能ID",
        "value": "skillID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1082: _tools.RODict({
        "ID": 1082,
        "name": "创生物ID",
        "value": "creationID",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1083: _tools.RODict({
        "ID": 1083,
        "name": "召唤物ID",
        "value": "summonID",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1084: _tools.RODict({
        "ID": 1084,
        "name": "buffID",
        "value": "buffID",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1085: _tools.RODict({
        "ID": 1085,
        "name": "X坐标",
        "value": "posX",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1086: _tools.RODict({
        "ID": 1086,
        "name": "Y坐标",
        "value": "posY",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1087: _tools.RODict({
        "ID": 1087,
        "name": "Z坐标",
        "value": "posZ",
        "valueType": 1,
        "Type": "float",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1088: _tools.RODict({
        "ID": 1088,
        "name": "角度",
        "value": "angle",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1089: _tools.RODict({
        "ID": 1089,
        "name": "消息ID",
        "value": "messageID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1090: _tools.RODict({
        "ID": 1090,
        "name": "玩家类型",
        "value": "playerChooseType",
        "valueType": 2,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": "指定怪物当前目标,指定怪物仇恨列表随机，怪物仇恨列表除前N个目标后随机，副本内所有玩家中随机"
    }),
    1091: _tools.RODict({
        "ID": 1091,
        "name": "范围",
        "value": "range",
        "valueType": 1,
        "Type": "int",
        "ifExport": 0,
        "defaultValue": "",
        "listValue": ""
    }),
    1092: _tools.RODict({
        "ID": 1092,
        "name": "目标怪物ID",
        "value": "targetMonsterID",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1093: _tools.RODict({
        "ID": 1093,
        "name": "dialogID",
        "value": "dialogID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1094: _tools.RODict({
        "ID": 1094,
        "name": "优先级",
        "value": "priority",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1095: _tools.RODict({
        "ID": 1095,
        "name": "最小范围",
        "value": "minRange",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1096: _tools.RODict({
        "ID": 1096,
        "name": "仇恨列表top排除数量",
        "value": "exceptHighestHate",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1097: _tools.RODict({
        "ID": 1097,
        "name": "怪物原型ID",
        "value": "monsterPrototypeID",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1098: _tools.RODict({
        "ID": 1098,
        "name": "目标EntityID",
        "value": "targetEntityId",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1099: _tools.RODict({
        "ID": 1099,
        "name": "镜头ID",
        "value": "cameraId",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1100: _tools.RODict({
        "ID": 1100,
        "name": "随机类型",
        "value": "randomType",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    1101: _tools.RODict({
        "ID": 1101,
        "name": "新手引导ID",
        "value": "triggerGuideID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    1102: _tools.RODict({
        "ID": 1102,
        "name": "变身ID",
        "value": "transPetID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2101: _tools.RODict({
        "ID": 2101,
        "name": "事件ID",
        "value": "eventID",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2102: _tools.RODict({
        "ID": 2102,
        "name": "副本阶段ID",
        "value": "stageID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2201: _tools.RODict({
        "ID": 2201,
        "name": "是否跟随主人死亡",
        "value": "dieWithHost",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2202: _tools.RODict({
        "ID": 2202,
        "name": "是否立刻触发检测",
        "value": "checkNow",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2203: _tools.RODict({
        "ID": 2203,
        "name": "是否指定原型ID",
        "value": "usePrototypeID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2204: _tools.RODict({
        "ID": 2204,
        "name": "事件循环注册",
        "value": "infLoop",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2205: _tools.RODict({
        "ID": 2205,
        "name": "副本是否成功",
        "value": "isDungeonDone",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    2206: _tools.RODict({
        "ID": 2206,
        "name": "是否只检测一次",
        "value": "checkOnce",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2401: _tools.RODict({
        "ID": 2401,
        "name": "血量(绝对值)",
        "value": "hp",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2402: _tools.RODict({
        "ID": 2402,
        "name": "最小攻击力",
        "value": "minAtk",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2403: _tools.RODict({
        "ID": 2403,
        "name": "最大攻击力",
        "value": "maxAtk",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2404: _tools.RODict({
        "ID": 2404,
        "name": "随机概率",
        "value": "randomArray",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2405: _tools.RODict({
        "ID": 2405,
        "name": "是否标记为BOSS",
        "value": "ifSetBoss",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2406: _tools.RODict({
        "ID": 2406,
        "name": "是否强制使用",
        "value": "forceToUse",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2407: _tools.RODict({
        "ID": 2407,
        "name": "AI",
        "value": "aiName",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2501: _tools.RODict({
        "ID": 2501,
        "name": "当前变量ID",
        "value": "varID",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2502: _tools.RODict({
        "ID": 2502,
        "name": "策划公式",
        "value": "formula",
        "valueType": 1,
        "Type": "string",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2503: _tools.RODict({
        "ID": 2503,
        "name": "变量ID列表",
        "value": "paramVarIDs",
        "valueType": 1,
        "Type": "python",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2601: _tools.RODict({
        "ID": 2601,
        "name": "生效玩家类型",
        "value": "chooseType",
        "valueType": 2,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": "副本内所有玩家,副本内玩家随机一名"
    }),
    2602: _tools.RODict({
        "ID": 2602,
        "name": "仇恨值",
        "value": "hateValue",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2603: _tools.RODict({
        "ID": 2603,
        "name": "护送距离",
        "value": "escortDistance",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2701: _tools.RODict({
        "ID": 2701,
        "name": "剧情动画ID",
        "value": "cinemaPlayID",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2801: _tools.RODict({
        "ID": 2801,
        "name": "战斗阶段",
        "value": "battleIdx",
        "valueType": 1,
        "Type": "int",
        "ifExport": 1,
        "defaultValue": "",
        "listValue": ""
    }),
    2901: _tools.RODict({
        "ID": 2901,
        "name": "天气类型",
        "value": "weatherType",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2902: _tools.RODict({
        "ID": 2902,
        "name": "天气增强时间",
        "value": "strongerTime",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2903: _tools.RODict({
        "ID": 2903,
        "name": "箭头类型",
        "value": "triggerType",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    2904: _tools.RODict({
        "ID": 2904,
        "name": "是否可选择",
        "value": "isSelectable",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    2905: _tools.RODict({
        "ID": 2905,
        "name": "是否重置位置",
        "value": "resetDir",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "1",
        "listValue": ""
    }),
    3001: _tools.RODict({
        "ID": 3001,
        "name": "近战怪数量",
        "value": "meleeNum",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    3002: _tools.RODict({
        "ID": 3002,
        "name": "远程怪数量",
        "value": "rangedNum",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    3003: _tools.RODict({
        "ID": 3003,
        "name": "刷新点随机数量",
        "value": "randomCollectionNum",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    3004: _tools.RODict({
        "ID": 3004,
        "name": "是否会重复刷新",
        "value": "checkHaveInFixed",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    }),
    3005: _tools.RODict({
        "ID": 3005,
        "name": "地图Id",
        "value": "mapId",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "1001",
        "listValue": ""
    }),
    3006: _tools.RODict({
        "ID": 3006,
        "name": "开始CD",
        "value": "cdTime",
        "valueType": 1,
        "Type": "uint",
        "ifExport": 1,
        "defaultValue": "0",
        "listValue": ""
    })
})
minKey = 1001
maxKey = 3006