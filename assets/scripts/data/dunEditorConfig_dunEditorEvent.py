# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: dunEditorConfig/dunEditorEvent
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
        "name": "基础/副本开始",
        "value": "dunStart",
        "param": "",
        "description": "副本开始事件，必须与state 1相连，无参数。"
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "基础/副本结束（成功）",
        "value": "dunEnd",
        "param": "1001,2205",
        "description": "副本结束，返回副本成功消息，参数为倒计时N秒后退出副本。"
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "基础/副本结束（失败）",
        "value": "dunFailed",
        "param": "1001",
        "description": "副本结束，返回副本失败消息，参数为倒计时N秒后退出副本。"
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "放出单位/放出怪物",
        "value": "createMonster",
        "param": "1011,1012,1013,1018,2401,2402,2403,2405,2407,1043",
        "description": "参数为地图编辑器中对应怪物的实例ID，即放出对应ID的怪物，支持填写多个实例ID，表示同时放出所有对应怪物，用逗号间隔；\n初始状态默认0，1表示石化状态，2表示虚影状态。"
    }),
    5: _tools.RODict({
        "ID": 5,
        "name": "回收单位/回收怪物",
        "value": "removeMonster",
        "param": "1011",
        "description": "参数为地图编辑器中对应怪物的实例ID，即回收（销毁）对应ID的怪物，支持填写多个实例ID，表示同时回收所有对应怪物，用逗号间隔。"
    }),
    6: _tools.RODict({
        "ID": 6,
        "name": "放出单位/放出NPC",
        "value": "createNPC",
        "param": "1011,1012,1013,2405",
        "description": "参数为地图编辑器中对应NPC的实例ID，即放出对应ID的NPC，支持填写多个实例ID，表示同时放出所有对应NPC，用逗号间隔。"
    }),
    7: _tools.RODict({
        "ID": 7,
        "name": "回收单位/回收NPC",
        "value": "removeNPC",
        "param": "1011",
        "description": "参数为地图编辑器中对应NPC的实例ID，即回收（销毁）对应ID的NPC，支持填写多个实例ID，表示同时回收所有对应NPC，用逗号间隔。"
    }),
    8: _tools.RODict({
        "ID": 8,
        "name": "放出单位/放出采集物",
        "value": "createCollection",
        "param": "1011,1012,3003,3004",
        "description": "参数为地图编辑器中对应采集物的实例ID，即放出对应ID的采集物，支持填写多个实例ID，表示同时放出所有对应采集物，用逗号间隔。"
    }),
    9: _tools.RODict({
        "ID": 9,
        "name": "回收单位/回收采集物",
        "value": "removeCollection",
        "param": "1011",
        "description": "参数为地图编辑器中对应采集物的实例ID，即回收（销毁）对应ID的采集物，支持填写多个实例ID，表示同时回收所有对应采集物，用逗号间隔。"
    }),
    10: _tools.RODict({
        "ID": 10,
        "name": "放出单位/放出空气墙",
        "value": "createAirWall",
        "param": "1011,1012",
        "description": "参数为地图编辑器中对应空气墙的实例ID，即放出对应ID的空气墙，支持填写多个实例ID，表示同时放出所有对应空气墙，用逗号间隔。"
    }),
    11: _tools.RODict({
        "ID": 11,
        "name": "回收单位/回收空气墙",
        "value": "removeAirWall",
        "param": "1011",
        "description": "参数为地图编辑器中对应空气墙的实例ID，即回收（销毁）对应ID的空气墙，支持填写多个实例ID，表示同时回收所有对应空气墙，用逗号间隔。"
    }),
    12: _tools.RODict({
        "ID": 12,
        "name": "放出单位/放出buff刷新点",
        "value": "createBuffPoint",
        "param": "1011,1012",
        "description": "参数为地图编辑器中对应buff刷新点的实例ID，即放出对应ID的buff刷新点，支持填写多个实例ID，表示同时放出所有对应buff刷新点，用逗号间隔。"
    }),
    13: _tools.RODict({
        "ID": 13,
        "name": "回收单位/回收buff刷新点",
        "value": "removeBuffPoint",
        "param": "1011",
        "description": "参数为地图编辑器中对应buff刷新点的实例ID，即回收（销毁）对应ID的buff刷新点，支持填写多个实例ID，表示同时回收所有对应buff刷新点，用逗号间隔。"
    }),
    14: _tools.RODict({
        "ID": 14,
        "name": "基础/循环执行",
        "value": "delayLoop",
        "param": "1021,1022,1023",
        "description": "参数为首次执行的延迟时间、每次循环执行的延迟时间以及循环执行的次数，循环执行从LOOP过渡引伸出去，相连的所有节点都执行完后才会继续下一次循环，全部循环结束后从FINISHED过渡出去；如果没有LOOP过渡，则表示直接执行延迟时间结束后直接从FINISHED过渡出去，相当于倒计时N秒执行下一个节点。"
    }),
    15: _tools.RODict({
        "ID": 15,
        "name": "检测条件/检测任务完成",
        "value": "taskFinished",
        "param": "1031,2202,2206",
        "description": "检测任务完成的消息（从该节点被触发后开始检测）；满足后触发下一节点，否则一直停留在该节点；参数为任务ID，是否立刻检测(可选参数)"
    }),
    16: _tools.RODict({
        "ID": 16,
        "name": "检测条件/检测任务失败",
        "value": "taskFailed",
        "param": "1031,2202,2206",
        "description": "检测任务失败的消息（从该节点被触发后开始检测）；满足后触发下一节点，否则一直停留在该节点；参数为任务ID，是否立刻检测(可选参数)"
    }),
    17: _tools.RODict({
        "ID": 17,
        "name": "检测条件/检测怪物血量",
        "value": "monsterHp",
        "param": "1041,1042,1043,2202,2206",
        "description": "检测副本中指定实例ID的怪物的血量（从该节点被触发开始计算）；所填实例ID对应地图编辑器中所有补位ID怪物中的第一个（策划确保该实例ID只刷一个怪）；满足后触发下一节点，否则一直停留在该节点；血量参数为对应怪物血量上限的百分比。"
    }),
    18: _tools.RODict({
        "ID": 18,
        "name": "检测条件/检测杀怪数量",
        "value": "killMonsterNum",
        "param": "1041,1042,1051,2203,2202,2206",
        "description": "检测副本中所击杀怪物数量（从该节点被触发开始计算），如果填了怪物ID（只能填1个，不支持多个），则表示检测对应ID的怪物的击杀数量；如果怪物ID填“-1”，则表示检测副本内所有怪物的击杀数量；满足后触发下一节点，否则一直停留在该节点。\n\n如果要检测原型数量，则在ID处填写原型ID，并在是否制定原型ID处填1。"
    }),
    19: _tools.RODict({
        "ID": 19,
        "name": "检测条件/检测怪物剩余数量",
        "value": "monsterRestNum",
        "param": "1041,1042,1061,2203,2202,2206",
        "description": "检测副本中所剩怪物数量（从该节点被触发开始计算），如果填了怪物ID（只能填1个，不支持多个），则表示检测对应ID的怪物的剩余数量；如果怪物ID填“-1”，则表示检测副本内剩余所有怪物的数量；满足后触发下一节点，否则一直停留在该节点。"
    }),
    20: _tools.RODict({
        "ID": 20,
        "name": "战斗相关/怪物释放技能",
        "value": "castSkill",
        "param": "1011,1081,1013,2406",
        "description": "指定ID的怪物释放技能，参数为地图编辑器中对应怪物的实例ID（只能填1个，不支持多个）、所释放的技能ID、技能等级。"
    }),
    21: _tools.RODict({
        "ID": 21,
        "name": "放出单位/指定位置创生物",
        "value": "createCreationInFixedPosition",
        "param": "1041,1011,1012",
        "description": "参数为地图编辑器中对应创生物的实例ID及数量，怪物ID填-1表示创建无主创生物"
    }),
    22: _tools.RODict({
        "ID": 22,
        "name": "放出单位/指定位置召唤怪物",
        "value": "summonMonsterInFixedPosition",
        "param": "1041,1011,1012,2201",
        "description": "参数为地图编辑器中对应创生物的实例ID及数量，怪物ID填-1表示创建无主召唤物，召唤物是否跟随被召唤者一起死亡(可选)"
    }),
    23: _tools.RODict({
        "ID": 23,
        "name": "战斗相关/怪物增加buff",
        "value": "addBuffToMonster",
        "param": "1041,1084,1013,1015,1016",
        "description": "给指定ID怪物身上的指定BUFF，参数是怪物实例ID，buffID，buff等级，buff最大等级限制(<0: buff不增加层数，==0，不显示等级，>0 限制等级)，buff持续时间(<0，读取配表默认值)"
    }),
    24: _tools.RODict({
        "ID": 24,
        "name": "战斗相关/怪物移除buff",
        "value": "removeBuffFromMonster",
        "param": "1041,1084",
        "description": "移除指定ID怪物身上的指定BUFF，参数是怪物实例ID，buffID"
    }),
    25: _tools.RODict({
        "ID": 25,
        "name": "战斗相关/副本内所有玩家增加buff",
        "value": "addBuffToAllPlayer",
        "param": "1084,1013,1089,1015,1016",
        "description": "给副本内所有玩家上的指定BUFF，参数是buffID，buff等级，messageID(可选参数)，buff最大等级限制(<0: buff不增加层数，==0，不显示等级，>0 限制等级)，buff持续时间(<0，读取配表默认值)"
    }),
    26: _tools.RODict({
        "ID": 26,
        "name": "战斗相关/副本内所有玩家移除buff",
        "value": "removeBuffFromAllPlayer",
        "param": "1084",
        "description": "移除副本内所有玩家身上的指定BUFF，参数是buffID"
    }),
    27: _tools.RODict({
        "ID": 27,
        "name": "基础/广播消息",
        "value": "broadcastMsg",
        "param": "1089",
        "description": "给副本内所有玩家广播消息，参数是msgID"
    }),
    28: _tools.RODict({
        "ID": 28,
        "name": "基础/清理副本",
        "value": "clearDungeon",
        "param": "",
        "description": "清除副本内所有的怪物、创生物、召唤物（非玩家的宠物和召唤物），无参数"
    }),
    29: _tools.RODict({
        "ID": 29,
        "name": "检测条件/检测剩余存活玩家数量",
        "value": "alivePlayer",
        "param": "1042,1012,2202,2206",
        "description": "检测副本内活着玩家的数量"
    }),
    30: _tools.RODict({
        "ID": 30,
        "name": "检测条件/检测指定怪物进战",
        "value": "monsterInBattle",
        "param": "1041,2202,2206",
        "description": "指定ID的怪物进入战斗，参数是怪物实例ID"
    }),
    31: _tools.RODict({
        "ID": 31,
        "name": "检测条件/检测指定怪物脱战",
        "value": "monsterLeaveBattle",
        "param": "1041,1021,1044,2202,2206",
        "description": "指定ID的怪物脱离战斗，即仇恨列表为空，此时销毁该怪物（由参数控制，默认销毁），参数是怪物实例ID和延时时间，主要用于boss战，boss脱战时候效果过多少秒重新刷出来（延迟配0不会重刷）"
    }),
    32: _tools.RODict({
        "ID": 32,
        "name": "基础/停止延迟事件",
        "value": "stopDelayEvent",
        "param": "2101",
        "description": "停止选定的延迟事件(e.g. delayLoop)，参数eventID填写所有需要停止的事件ID集合"
    }),
    33: _tools.RODict({
        "ID": 33,
        "name": "放出单位/在玩家位置创生物",
        "value": "createCreationInPlayerPosition",
        "param": "1041,1082,1090,1091,1012,1095,1096",
        "description": "在玩家周围创建创生物，参数是怪物ID，创生物ID，玩家类别，玩家选择范围，数量(可选)，玩家选择最小范围(可选)，仇恨排除top范围(可选)，ID填-1表示创建无主创生物"
    }),
    34: _tools.RODict({
        "ID": 34,
        "name": "放出单位/在怪物位置创生物",
        "value": "createCreationInMonsterPosition",
        "param": "1041,1082,1092,1091,1012",
        "description": "在怪物周围创建创生物，参数是怪物ID，创生物ID，目标怪物ID，怪物自身随机范围，ID填-1表示创建无主创生物"
    }),
    35: _tools.RODict({
        "ID": 35,
        "name": "战斗相关/向玩家使用技能",
        "value": "castSkillToPlayer",
        "param": "1041,1081,1090,1089,1012,1091,1095,1096",
        "description": "向指定玩家释放技能，参数是怪物ID，技能ID，选择玩家类别，广播消息编号，消息号填0是不会广播，如果填了则默认消息会传入两个参数，玩家的名字和技能名字"
    }),
    36: _tools.RODict({
        "ID": 36,
        "name": "战斗相关/指定玩家增加buff",
        "value": "addBuffToPlayer",
        "param": "1041,1090,1084,1013,1012,1089,1091,1095,1096,1015,1016",
        "description": "指定玩家增加buff，参数是玩家类别，buffID，buff等级，messageID(可选参数)，范围(可选)，最小范围(可选)，仇恨列表排除(可选)，buff最大等级限制(<0: buff不增加层数，==0，不显示等级，>0 限制等级)，buff持续时间(<0，读取配表默认值)"
    }),
    37: _tools.RODict({
        "ID": 37,
        "name": "检测条件/检测范围内创生物",
        "value": "haveCreationInRange",
        "param": "1041,1091,1082",
        "description": "检测指定怪物范围内，是否有指定ID创生物，参数是怪物ID，范围，创生物ID"
    }),
    38: _tools.RODict({
        "ID": 38,
        "name": "回收单位/移除创生物",
        "value": "removeCreation",
        "param": "1041,1091,1082",
        "description": "移除指定怪物范围内的指定ID的创生物，参数是怪物ID，范围，创生物ID"
    }),
    39: _tools.RODict({
        "ID": 39,
        "name": "基础/副本阶段设置",
        "value": "dunStageSet",
        "param": "2102",
        "description": "设置新的副本阶段，参数是副本阶段ID，从1开始"
    }),
    40: _tools.RODict({
        "ID": 40,
        "name": "行为事件/指定怪物、NPC等实体弹出气泡",
        "value": "showPopoverMsg",
        "param": "1011,1089",
        "description": "指定实体向AOI范围内玩家弹出气泡消息，参数是副本怪物实例ID，消息message表monsterPop"
    }),
    41: _tools.RODict({
        "ID": 41,
        "name": "行为事件/指定怪物、NPC等实体弹出消息",
        "value": "popupdialog",
        "param": "1011,1093",
        "description": "指定实体向AOI范围内玩家弹出消息，参数是副本怪物实例ID，dialog表popDialogID"
    }),
    42: _tools.RODict({
        "ID": 42,
        "name": "状态改变/副本内全部玩家任务强制完成",
        "value": "dungeonTaskForceComplete",
        "param": "1031",
        "description": "强制当前副本内玩家特定任务完成，参数是任务ID"
    }),
    43: _tools.RODict({
        "ID": 43,
        "name": "状态改变/副本内全部玩家任务强制失败",
        "value": "dungeonTaskForceFailed",
        "param": "1031",
        "description": "强制当前副本内玩家特定任务失败，参数是任务ID"
    }),
    44: _tools.RODict({
        "ID": 44,
        "name": "状态改变/副本NPC变为可战斗状态",
        "value": "changeDunNPCToBattle",
        "param": "1011,2405",
        "description": "将副本内特定NPC切换为可战斗状态，参数是实例ID"
    }),
    45: _tools.RODict({
        "ID": 45,
        "name": "状态改变/副本NPC变为中立",
        "value": "changeDunNPCToNeutral",
        "param": "1011,2905",
        "description": "将副本内特定NPC切换中立(不可攻击)状态，参数是实例ID"
    }),
    46: _tools.RODict({
        "ID": 46,
        "name": "检测条件/检测副本内任一玩家血量",
        "value": "dunAnyPlayerHP",
        "param": "1042,1043,2202,2206",
        "description": "将测副本中任一玩家血量满足条件，参数是比较符号，血量"
    }),
    47: _tools.RODict({
        "ID": 47,
        "name": "行为事件/为特定实例创建指向箭头",
        "value": "addEntityArrowTracker",
        "param": "1011,1094,2903",
        "description": "为当前场景(具有spaceMgr即可)所有玩家客户端创建一个指向特定实体的箭头，参数是实例ID(只能填一个)，优先级"
    }),
    48: _tools.RODict({
        "ID": 48,
        "name": "寻路移动相关/将副本内实体移动到指定位置",
        "value": "moveEntityToFixedPosition",
        "param": "1011,1085,1086,1087,1019,1020",
        "description": "将副本内某个实体(怪物/NPC等)移动到指定位置，参数是实体ID，X/Y/Z轴坐标，速度没有特殊需求填0即可，选择对应移动时所需要的动作（run01/run02，速度填0会自动根据所选动作读取modelRes对应配置的速度）"
    }),
    49: _tools.RODict({
        "ID": 49,
        "name": "战斗相关/副本内随机玩家创建玩家镜像",
        "value": "createAvatarMirrorFromRandomPlayer",
        "param": "1011,1014",
        "description": "副本内随机玩家创建玩家镜像，参数是实例ID(实例ID里面的原型ID(也叫EntityID)中配置怪物的势力，是否是被动怪，其他属性等参数)，比率(可选，默认1)简单控制怪物强度，1.0时强度和玩家当前强度一致，比率=0时取creepID的属性"
    }),
    50: _tools.RODict({
        "ID": 50,
        "name": "战斗相关/副本内清除Entity仇恨",
        "value": "clearEntityHate",
        "param": "1011",
        "description": "副本内清除选定Entity的仇恨，参数: EntityID(list)"
    }),
    51: _tools.RODict({
        "ID": 51,
        "name": "放出单位/在玩家位置创建召唤物",
        "value": "createSummonInPlayerPosition",
        "param": "1041,1082,1090,1091,1012,1095,1096,2201",
        "description": "在玩家周围创建召唤物，参数是怪物ID，召唤物ID，玩家类别，玩家选择范围，数量(可选)，玩家选择最小范围(可选)，仇恨排除top范围(可选)，召唤物是否跟随被召唤者一起死亡(可选)"
    }),
    52: _tools.RODict({
        "ID": 52,
        "name": "废弃/检测杀怪原型数量",
        "value": "killMonsterPrototypeNum",
        "param": "1097,1042,1051",
        "description": "检测副本中所击杀怪物数量（从该节点被触发开始计算），这里是检测怪物原型ID（只能填1个，不支持多个）；满足后触发下一节点，否则一直停留在该节点。"
    }),
    53: _tools.RODict({
        "ID": 53,
        "name": "基础/概率随机触发",
        "value": "randomTrigger",
        "param": "2404",
        "description": "有多个过渡（RANDOM），根据概率随机触发哪一个过渡，只会触发一次，每个过渡可以单独配置权重，概率=权重/权重总和"
    }),
    54: _tools.RODict({
        "ID": 54,
        "name": "回收单位/移除无主创生物",
        "value": "removeNoHostCreation",
        "param": "1011,2203",
        "description": "移除无主创生物, 参数位实例ID,是否使用原型ID, 如果使用原型ID, 实例ID为原型ID"
    }),
    55: _tools.RODict({
        "ID": 55,
        "name": "检测条件/采集物被采集事件",
        "value": "collBeCollected",
        "param": "1011,2203,2204,2202,2206",
        "description": "GID对应采集物被采集后触发事件, 参数是采集物GID(只支持一个或多个, 多个时检测任意一个触发), 是否监测原型ID,是否循环事件(0, 只触发一次, 1, 一直触发)"
    }),
    56: _tools.RODict({
        "ID": 56,
        "name": "战斗相关/强制选择目标",
        "value": "forceSelectEntityTarget",
        "param": "1011,1090,1091,1095,1096",
        "description": "随机选择一个目标并传入某个召唤怪物的AI, 参数是实体ID列表, 选择类型(可选),最大范围(可选),最小范围(可选),仇恨排除列表(可选)"
    }),
    57: _tools.RODict({
        "ID": 57,
        "name": "检测条件/触发器陷阱",
        "value": "trapBeTriggered",
        "param": "1011,2202,2206",
        "description": "特定陷阱被触发事件, 参数是实体ID(只支持一个ID)"
    }),
    58: _tools.RODict({
        "ID": 58,
        "name": "寻路移动相关/副本内传送至特定位置",
        "value": "teleportToPosition",
        "param": "1011,1085,1086,1087,1088",
        "description": "将副本内特定Entity传送至特定位置, 参数是实体ID, 位置X,Y,Z轴,角度"
    }),
    59: _tools.RODict({
        "ID": 59,
        "name": "基础/整合事件",
        "value": "integrationEvent",
        "param": "",
        "description": "整合事件，事件本身无逻辑，用于汇总触发的过渡，同时多份配置汇总导出时用该节点做连接事件"
    }),
    60: _tools.RODict({
        "ID": 60,
        "name": "基础/副本延迟结束(成功)",
        "value": "dunDelayEnd",
        "param": "1001,1002",
        "description": "在特定时间(会改变副本结束客户端时间)后副本结束，返回副本成功消息，参数为倒计时N秒后退出副本。"
    }),
    61: _tools.RODict({
        "ID": 61,
        "name": "基础/更改space变量",
        "value": "changeSpaceVar",
        "param": "2501,2502,2503",
        "description": "更改副本内Space变量的值, 参数格式为 varID[2501] = Formula[2502](varIDList[2503]), 其中formula函数定义必须为 def fnName(e): …, 取得一个ID的值`var1234Val = e[1234]`"
    }),
    62: _tools.RODict({
        "ID": 62,
        "name": "战斗相关/杀死副本内实体",
        "value": "killEntities",
        "param": "1011",
        "description": "杀死副本内对应ID的实体, 参数为EntityID,可以填多个"
    }),
    63: _tools.RODict({
        "ID": 63,
        "name": "战斗相关/副本内entity进入濒死节点",
        "value": "dungeonEntityImmuneDeath",
        "param": "1011",
        "description": "副本内entity进入濒死后触发, 参数为EntityID, 只能填1个"
    }),
    64: _tools.RODict({
        "ID": 64,
        "name": "战斗相关/副本内所有选定Entity濒死",
        "value": "ifAllSelectEntityImmuneDeath",
        "param": "1011",
        "description": "副本内所有选定Entity濒死后执行下面节点, 参数为EntityID, 可以填多个"
    }),
    65: _tools.RODict({
        "ID": 65,
        "name": "检测条件/检测变量",
        "value": "checkValue",
        "param": "2502,2503",
        "description": "判断公式返回true还是false，false则hold住，true判断通过执行后续节点"
    }),
    66: _tools.RODict({
        "ID": 66,
        "name": "放出单位/创建副本传送门",
        "value": "createDungeonTeleporter",
        "param": "1011,1098,1091",
        "description": "创建副本传送门, 参数为: 传送门ID(一般为creationID),目标EntityId,陷阱触发范围"
    }),
    67: _tools.RODict({
        "ID": 67,
        "name": "状态改变/指定怪物改变初始状态",
        "value": "monsterChangeInitState",
        "param": "1011,1018",
        "description": "指定实例ID的怪物改变初始状态，0表示正常怪物状态，1表示石化状态，2表示虚影状态，0不可变1、2"
    }),
    68: _tools.RODict({
        "ID": 68,
        "name": "战斗相关/指定ID怪物对副本内玩家增加仇恨",
        "value": "monsterAddHateValue",
        "param": "1011,2601,2602",
        "description": "指定实例ID的怪物对玩家增加仇恨"
    }),
    69: _tools.RODict({
        "ID": 69,
        "name": "行为事件/更改副本内NPC对话ID",
        "value": "changeDunNPCDialog",
        "param": "1011,1093",
        "description": "更改副本内NPC对话ID, 参数为NPCID, 新的对话ID"
    }),
    70: _tools.RODict({
        "ID": 70,
        "name": "状态改变/停止AI",
        "value": "stopAiTick",
        "param": "1011",
        "description": "停止指定实例的AI tick"
    }),
    71: _tools.RODict({
        "ID": 71,
        "name": "状态改变/开启AI",
        "value": "startAiTick",
        "param": "1011",
        "description": "开启指定实例的AI tick"
    }),
    72: _tools.RODict({
        "ID": 72,
        "name": "寻路移动相关/实体开始使用路点寻路",
        "value": "entityStartRouting",
        "param": "1011,1032,1019,1020,2603",
        "description": "实体开始进行路点寻路，参数为 实体ID（填一个）, 路径ID, 速度（速度没有特殊需求填0即可）, 护送距离（填0为不设置），选择对应移动时所需要的动作（run01/run02，速度填0会自动根据所选动作读取modelRes对应配置的速度）"
    }),
    73: _tools.RODict({
        "ID": 73,
        "name": "寻路移动相关/实体路点寻路完成",
        "value": "entityRouteFinished",
        "param": "1011,1032",
        "description": "实体路点寻路完成时触发, 参数为 实体ID (填一个，-1表示追踪所有)，pathID(填一个，-1表示追踪所有)"
    }),
    74: _tools.RODict({
        "ID": 74,
        "name": "寻路移动相关/实体路点寻路中附近没有护卫",
        "value": "entityRoutingMissingEscort",
        "param": "1011,1032,2204",
        "description": "实体路点寻路中附近没有护卫（玩家）时触发, 参数为 实体ID (填一个，-1表示追踪所有)，pathID(填一个，-1表示追踪所有)，是否无限循环"
    }),
    75: _tools.RODict({
        "ID": 75,
        "name": "检测条件/多个采集物全部被采集事件",
        "value": "multiCollAllBeCollected",
        "param": "1011,2204",
        "description": "GID对应采集物被采集后触发事件, 参数是一个/多个采集物GID, 是否循环事件(0, 只触发一次, 1, 一直触发)"
    }),
    76: _tools.RODict({
        "ID": 76,
        "name": "基础/播放剧情动画",
        "value": "castCinemaPlay",
        "param": "2701",
        "description": "播放指定ID的剧情动画"
    }),
    77: _tools.RODict({
        "ID": 77,
        "name": "基础/触发新手引导",
        "value": "triggerGuide",
        "param": "1101",
        "description": "触发新手引导，参数为引导ID，《tutorConst-新手常量表》-<触发引导流程表-triggerGuide>"
    }),
    78: _tools.RODict({
        "ID": 78,
        "name": "状态改变/改变副本天气",
        "value": "changeWeather",
        "param": "2901,2902",
        "description": "改变副本内天气"
    }),
    79: _tools.RODict({
        "ID": 79,
        "name": "行为事件/改变副本内所有玩家镜头状态",
        "value": "changeAllPlayerCameraStatus",
        "param": "1099",
        "description": "改变副本内玩家镜头状态，参数为镜头ID，不能和改变玩家镜头朝向同时执行"
    }),
    80: _tools.RODict({
        "ID": 80,
        "name": "行为事件/改变副本内所有玩家镜头朝向",
        "value": "changeAllPlayerCameraLookPos",
        "param": "1011",
        "description": "改变副本内玩家镜头朝向，参数为需要面向的实例ID，不能和改变玩家镜头状态同时执行"
    }),
    81: _tools.RODict({
        "ID": 81,
        "name": "行为事件/恢复副本内玩家的镜头状态",
        "value": "revertAllPlayerCameraStatus",
        "param": "",
        "description": "恢复副本内玩家的上一个镜头状态"
    }),
    82: _tools.RODict({
        "ID": 82,
        "name": "状态改变/改变副本内NPC交互状态",
        "value": "changeNPCSelectableStatus",
        "param": "1011,2904",
        "description": "改变副本内NPC交互状态, 参数为实例ID(支持多个), 是否可选择"
    }),
    83: _tools.RODict({
        "ID": 83,
        "name": "检测条件/检测对应任务正在进行中",
        "value": "taskInProgress",
        "param": "1031",
        "description": "检测指定ID的任务是否处于进行中的状态，即刻单次检测，如果没在进行中则该节点中止"
    }),
    84: _tools.RODict({
        "ID": 84,
        "name": "检测条件/检测副本内任意玩家跳过指定ID动画",
        "value": "jumpCinemaPlay",
        "param": "2701,1001",
        "description": "当检测到副本内任意玩家跳过指定ID的剧情时，该节点往下执行，否则等到倒计时之后自动进行"
    }),
    85: _tools.RODict({
        "ID": 85,
        "name": "状态改变/修改实体朝向",
        "value": "changeEntityDirection",
        "param": "1011,1088",
        "description": "修改副本内任意实体朝向, 参数为实体ID(可以填多个), 修改角度"
    }),
    86: _tools.RODict({
        "ID": 86,
        "name": "行为事件/为特定实例销毁指向箭头",
        "value": "removeEntityArrowTracker",
        "param": "1011,2903",
        "description": "当前场景(具有spaceMgr即可)所有玩家客户端销毁特定实体的箭头，参数是实例ID(只能填一个)，箭头类型"
    }),
    87: _tools.RODict({
        "ID": 87,
        "name": "状态改变/副本NPC变为友善",
        "value": "changeDunNPCToFriendly",
        "param": "1011,2905",
        "description": "将副本内特定NPC切换友善状态，参数是实例ID"
    }),
    88: _tools.RODict({
        "ID": 88,
        "name": "检测条件/检测剩余玩家数量",
        "value": "playerRestNum",
        "param": "1042,1012,2202,2206",
        "description": "检测副本内玩家的数量（不区分死活）"
    }),
    89: _tools.RODict({
        "ID": 89,
        "name": "行为事件/接取特定id任务",
        "value": "taskUndertake",
        "param": "1031",
        "description": "为玩家接取特定id的任务"
    }),
    90: _tools.RODict({
        "ID": 90,
        "name": "放出单位/放出复活点",
        "value": "createRebornPos",
        "param": "1011,1012",
        "description": "参数为地图编辑器中对应复活点的实例ID，即放出对应ID的复活点，支持填写多个实例ID，表示同时放出所有对应复活点，用逗号间隔。"
    }),
    91: _tools.RODict({
        "ID": 91,
        "name": "回收单位/回收复活点",
        "value": "removeRebornPos",
        "param": "1011",
        "description": "参数为地图编辑器中对应复活点的实例ID，即回收（销毁）对应ID的复活点，支持填写多个实例ID，表示同时回收所有对应复活点，用逗号间隔。"
    }),
    92: _tools.RODict({
        "ID": 92,
        "name": "传送后到指定地图指定位置",
        "value": "transferToTheDesignatedMap",
        "param": "3005,1085,1086,1087,1088",
        "description": "传送玩家到指定地图指定坐标"
    }),
    93: _tools.RODict({
        "ID": 93,
        "name": "通知开始战斗CD",
        "value": "notifyStartBattleCD",
        "param": "3006",
        "description": "副本阶段内，开始战斗倒计时"
    }),
    94: _tools.RODict({
        "ID": 94,
        "name": "放出单位/放出脱卡点",
        "value": "createBreakAwayStuckPos",
        "param": "1011,1012",
        "description": "参数为地图编辑器中对应脱卡点的实例ID，即放出对应ID的出生点，支持填写多个实例ID，表示同时放出所有对应脱卡点，用逗号间隔。"
    }),
    95: _tools.RODict({
        "ID": 95,
        "name": "改变副本内Entity阵营",
        "value": "changeEntityForce",
        "param": "1011,1017",
        "description": "改变副本内特定Entity阵营,参数为实体ID, 阵营ID"
    }),
    96: _tools.RODict({
        "ID": 96,
        "name": "检测条件/检测杀怪总数量",
        "value": "TotalNumberOfMonstersKilled",
        "param": "1041,1042,1051,2203,2202,2206",
        "description": "检测副本中所击杀怪物总数量（从该节点被触发开始计算，可以填多个怪物ID），则表示检测对应ID的怪物的击杀总数量\n如果要检测原型数量，则在ID处填写原型ID，并在是否制定原型ID处填1。"
    })
})
minKey = 1
maxKey = 96