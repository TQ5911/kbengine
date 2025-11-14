# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: cityBattle/config
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "cityBattle_noPermission1": _tools.RODict({
        "ID": "cityBattle_noPermission1",
        "value": 54003000,
    }),
    "cityBattle_registered": _tools.RODict({
        "ID": "cityBattle_registered",
        "value": 54003001,
    }),
    "cityBattle_registerConfirm": _tools.RODict({
        "ID": "cityBattle_registerConfirm",
        "value": 54003002,
    }),
    "cityBattle_noFund": _tools.RODict({
        "ID": "cityBattle_noFund",
        "value": 54003003,
    }),
    "cityBattle_noProp": _tools.RODict({
        "ID": "cityBattle_noProp",
        "value": 54003004,
    }),
    "cityBattle_biddingTips": _tools.RODict({
        "ID": "cityBattle_biddingTips",
        "value": 54003005,
    }),
    "cityBattle_noQualification": _tools.RODict({
        "ID": "cityBattle_noQualification",
        "value": 54003006,
    }),
    "cityBattle_declared": _tools.RODict({
        "ID": "cityBattle_declared",
        "value": 54003007,
    }),
    "cityBattle_noPermission2": _tools.RODict({
        "ID": "cityBattle_noPermission2",
        "value": 54003008,
    }),
    "cityBattle_errorTime": _tools.RODict({
        "ID": "cityBattle_errorTime",
        "value": 54003009,
    }),
    "cityBattle_noEntryQualification": _tools.RODict({
        "ID": "cityBattle_noEntryQualification",
        "value": 54003010,
    }),
    "cityBattle_noStart": _tools.RODict({
        "ID": "cityBattle_noStart",
        "value": 54003011,
    }),
    "cityBattle_peopleMax": _tools.RODict({
        "ID": "cityBattle_peopleMax",
        "value": 54003012,
    }),
    "cityBattle_occupyTips1": _tools.RODict({
        "ID": "cityBattle_occupyTips1",
        "value": 54003013,
    }),
    "cityBattle_occupyTips2": _tools.RODict({
        "ID": "cityBattle_occupyTips2",
        "value": 54003014,
    }),
    "cityBattle_destroyGate1": _tools.RODict({
        "ID": "cityBattle_destroyGate1",
        "value": 54003015,
    }),
    "cityBattle_destroyGate2": _tools.RODict({
        "ID": "cityBattle_destroyGate2",
        "value": 54003016,
    }),
    "cityBattle_openSwitch": _tools.RODict({
        "ID": "cityBattle_openSwitch",
        "value": 54003017,
    }),
    "cityBattle_gateTips1": _tools.RODict({
        "ID": "cityBattle_gateTips1",
        "value": 54003018,
    }),
    "cityBattle_gateTips2": _tools.RODict({
        "ID": "cityBattle_gateTips2",
        "value": 54003019,
    }),
    "cityBattle_gateTips3": _tools.RODict({
        "ID": "cityBattle_gateTips3",
        "value": 54003020,
    }),
    "cityBattle_gateTips4": _tools.RODict({
        "ID": "cityBattle_gateTips4",
        "value": 54003021,
    }),
    "cityBattle_transmitLimit": _tools.RODict({
        "ID": "cityBattle_transmitLimit",
        "value": 54003022,
    }),
    "cityBattle_siegeEngines": _tools.RODict({
        "ID": "cityBattle_siegeEngines",
        "value": 54003023,
    }),
    "cityBattle_noPermission3": _tools.RODict({
        "ID": "cityBattle_noPermission3",
        "value": 54003024,
    }),
    "cityBattle_siegeEnginesStart": _tools.RODict({
        "ID": "cityBattle_siegeEnginesStart",
        "value": 54003025,
    }),
    "cityBattle_signDescribe": _tools.RODict({
        "ID": "cityBattle_signDescribe",
        "value": 54003026,
    }),
    "cityBattle_signTips": _tools.RODict({
        "ID": "cityBattle_signTips",
        "value": 54003027,
    }),
    "cityBattle_pointsTips1": _tools.RODict({
        "ID": "cityBattle_pointsTips1",
        "value": 54003028,
    }),
    "cityBattle_pointsTips2": _tools.RODict({
        "ID": "cityBattle_pointsTips2",
        "value": 54003029,
    }),
    "cityBattle_noPermission4": _tools.RODict({
        "ID": "cityBattle_noPermission4",
        "value": 54003030,
    }),
    "cityBattle_noCityFund": _tools.RODict({
        "ID": "cityBattle_noCityFund",
        "value": 54003035,
    }),
    "cityBattle_orderSuccess": _tools.RODict({
        "ID": "cityBattle_orderSuccess",
        "value": 54003036,
    }),
    "cityBattle_noPlayer": _tools.RODict({
        "ID": "cityBattle_noPlayer",
        "value": 54003037,
    }),
    "cityBattle_rewardSuccess": _tools.RODict({
        "ID": "cityBattle_rewardSuccess",
        "value": 54003038,
    }),
    "cityBattle_wantedSuccess": _tools.RODict({
        "ID": "cityBattle_wantedSuccess",
        "value": 54003039,
    }),
    "cityBattle_noPermission5": _tools.RODict({
        "ID": "cityBattle_noPermission5",
        "value": 54003040,
    }),
    "cityBattle_specialTime": _tools.RODict({
        "ID": "cityBattle_specialTime",
        "value": 54003041,
    }),
    "cityBattle_baseTips": _tools.RODict({
        "ID": "cityBattle_baseTips",
        "value": 54003042,
    }),
    "cityBattle_systemClose": _tools.RODict({
        "ID": "cityBattle_systemClose",
        "value": 54003043,
    }),
    "cityBattle_noBiddingPermission": _tools.RODict({
        "ID": "cityBattle_noBiddingPermission",
        "value": 54003044,
    }),
    "cityBattle_biddingProhibit": _tools.RODict({
        "ID": "cityBattle_biddingProhibit",
        "value": 54003045,
    }),
    "cityBattle_noSignTime": _tools.RODict({
        "ID": "cityBattle_noSignTime",
        "value": 54003054,
    }),
    "cityBattle_noSignUp": _tools.RODict({
        "ID": "cityBattle_noSignUp",
        "value": 54003055,
    }),
    "cityBattle_cityDefend": _tools.RODict({
        "ID": "cityBattle_cityDefend",
        "value": 54003056,
    }),
    "cityBattle_biddingEnd": _tools.RODict({
        "ID": "cityBattle_biddingEnd",
        "value": 54003065,
    }),
    "cityBattle_choiceConfirm": _tools.RODict({
        "ID": "cityBattle_choiceConfirm",
        "value": 54003067,
    }),
    "cityBattle_choiceConfirm2": _tools.RODict({
        "ID": "cityBattle_choiceConfirm2",
        "value": 54003068,
    }),
    "cityBattle_noCityLord": _tools.RODict({
        "ID": "cityBattle_noCityLord",
        "value": 54003078,
    }),
    "cityBattle_guildAlreadyBidding": _tools.RODict({
        "ID": "cityBattle_guildAlreadyBidding",
        "value": 54003079,
    }),
    "cityBattle_NotFoundInSearch": _tools.RODict({
        "ID": "cityBattle_NotFoundInSearch",
        "value": 54003082,
    }),
    "cityBattle_EnterCorrectNickname": _tools.RODict({
        "ID": "cityBattle_EnterCorrectNickname",
        "value": 54003083,
    }),
    "cityBattle_EnterCorrectNickname2": _tools.RODict({
        "ID": "cityBattle_EnterCorrectNickname2",
        "value": 54003084,
    }),
    "cityBattle_EnterCorrectNickname3": _tools.RODict({
        "ID": "cityBattle_EnterCorrectNickname3",
        "value": 54003085,
    }),
    "cityBattle_noPrivilegeTimes": _tools.RODict({
        "ID": "cityBattle_noPrivilegeTimes",
        "value": 54003086,
    }),
    "cityBattle_appointOneself": _tools.RODict({
        "ID": "cityBattle_appointOneself",
        "value": 54003087,
    }),
    "cityBattle_EnterCorrectNickname4": _tools.RODict({
        "ID": "cityBattle_EnterCorrectNickname4",
        "value": 54003088,
    }),
    "cityBattle_alreadyOpen": _tools.RODict({
        "ID": "cityBattle_alreadyOpen",
        "value": 54003091,
    }),
    "cityBattle_prohibitExit": _tools.RODict({
        "ID": "cityBattle_prohibitExit",
        "value": 54003092,
    }),
    "cityBattle_AppointSuccess": _tools.RODict({
        "ID": "cityBattle_AppointSuccess",
        "value": 54003093,
    }),
    "cityBattle_siegeEnginesPermission": _tools.RODict({
        "ID": "cityBattle_siegeEnginesPermission",
        "value": 54003095,
    }),
    "cityBattle_forbidLiftAlliance": _tools.RODict({
        "ID": "cityBattle_forbidLiftAlliance",
        "value": 54003096,
    }),
    "cityBattle_killMsg": _tools.RODict({
        "ID": "cityBattle_killMsg",
        "value": 54003097,
    }),
    "cityBattle_prohibitAlliance": _tools.RODict({
        "ID": "cityBattle_prohibitAlliance",
        "value": 54003098,
    }),
    "cityBattle_prohibitEnterBattle": _tools.RODict({
        "ID": "cityBattle_prohibitEnterBattle",
        "value": 54003099,
    }),
    "cityBattle_leaveConfirm": _tools.RODict({
        "ID": "cityBattle_leaveConfirm",
        "value": 54000319,
    }),
    "cityBattle_breakBallista": _tools.RODict({
        "ID": "cityBattle_breakBallista",
        "value": 54003101,
    }),
    "cityBattle_breakAllBallista": _tools.RODict({
        "ID": "cityBattle_breakAllBallista",
        "value": 54003102,
    }),
    "cityBattle_attack": _tools.RODict({
        "ID": "cityBattle_attack",
        "value": "攻城方",
    }),
    "cityBattle_defend": _tools.RODict({
        "ID": "cityBattle_defend",
        "value": "守城方",
    }),
    "cityBattle_activityDescribe": _tools.RODict({
        "ID": "cityBattle_activityDescribe",
        "value": "群雄逐鹿，谁与争锋？奉现任新元城主<color=#F3D58F>{0}</color>之命布告天下，凡自认实力超群者，皆可于接下来的<color=#038304>5天内</color>猎杀任意魔物，以获取<color=#038304>魔物灵核</color>。所得灵核可于5天后上缴至新元城府衙，上缴数量最多之帮派，便可获取本期城战的攻城凭证-新元攻城令。",
    }),
    "cityBattle_activityDescribe2": _tools.RODict({
        "ID": "cityBattle_activityDescribe2",
        "value": "活动期间，全体玩家击杀任意怪物概率掉落<color=#038304>魔物灵核</color>。击杀<color=#F3D58F>祖珂教主</color>，必定掉落大量<color=#038304>魔物灵核</color>。",
    }),
    "cityBattle_biddingButton": _tools.RODict({
        "ID": "cityBattle_biddingButton",
        "value": "竞价",
    }),
    "cityBattle_countdownLeave": _tools.RODict({
        "ID": "cityBattle_countdownLeave",
        "value": "{0}后自动离开",
    }),
    "cityBattle_waiting": _tools.RODict({
        "ID": "cityBattle_waiting",
        "value": "虚位以待",
    }),
    "cityBattle_specialTimeBlacklist": _tools.RODict({
        "ID": "cityBattle_specialTimeBlacklist",
        "value": _tools.ROList([918, 1213]),
    }),
    "cityBattle_flagAsset": _tools.RODict({
        "ID": "cityBattle_flagAsset",
        "value": "Assets/Res/art/scenes/assets/build/prefab/ty_qi02.prefab",
    }),
    "cityBattle_biddingDesc1": _tools.RODict({
        "ID": "cityBattle_biddingDesc1",
        "value": "竞拍倒计时：{0}",
    }),
    "cityBattle_biddingDesc2": _tools.RODict({
        "ID": "cityBattle_biddingDesc2",
        "value": "<color=#739cc9>{0}</color> <color=#e4dabd>{1}</color> <color=#9e9886>出价</color> <color=#038304>{2}</color> <color=#e4dabd>魔物灵核(帮)</color>",
    }),
    "cityBattle_biddingDesc3": _tools.RODict({
        "ID": "cityBattle_biddingDesc3",
        "value": "{0}",
    }),
    "cityBattle_biddingDesc4": _tools.RODict({
        "ID": "cityBattle_biddingDesc4",
        "value": "<color=#2f6caf>{0}</color><color=#8D4D01>{1}</color><color=#4F4536>出价</color><color=#038304>{2}</color><color=#8D4D01>魔物灵核(帮)</color>",
    }),
    "cityBattle_biddingDesc5": _tools.RODict({
        "ID": "cityBattle_biddingDesc5",
        "value": "最终成交价<color=#FFFBD7>{0}</color>",
    }),
    "cityBattle_biddingDesc6": _tools.RODict({
        "ID": "cityBattle_biddingDesc6",
        "value": "<color=#319832>持有倒计时：{0}</color>",
    }),
    "cityBattle_biddingDesc7": _tools.RODict({
        "ID": "cityBattle_biddingDesc7",
        "value": "持有：{0}",
    }),
    "cityBattle_biddingEndDes1": _tools.RODict({
        "ID": "cityBattle_biddingEndDes1",
        "value": "<color=#D69B4D>{0}</color> <color=#F3D58F>{1}</color> 获得新元城攻城令归属！",
    }),
    "cityBattle_startBattleDesc": _tools.RODict({
        "ID": "cityBattle_startBattleDesc",
        "value": "战场开启倒计时：{0}",
    }),
    "cityBattle_prepareTimeDes": _tools.RODict({
        "ID": "cityBattle_prepareTimeDes",
        "value": "剩余准备时间：{0}",
    }),
    "cityBattle_fightTimeDes": _tools.RODict({
        "ID": "cityBattle_fightTimeDes",
        "value": "剩余时间：{0}",
    }),
    "cityBattle_lastTimeDes": _tools.RODict({
        "ID": "cityBattle_lastTimeDes",
        "value": "距离离开：{0}",
    }),
    "cityBattle_declareWarTime": _tools.RODict({
        "ID": "cityBattle_declareWarTime",
        "value": "{0}",
    }),
    "cityBattle_NewCityLord": _tools.RODict({
        "ID": "cityBattle_NewCityLord",
        "value": "{0} {1} 成为新元城新的主人",
    }),
    "cityBattle_nextBiddingTime": _tools.RODict({
        "ID": "cityBattle_nextBiddingTime",
        "value": "距离下次竞标剩余<color=#b35b00>{0}</color>",
    }),
    "cityBattle_occupyTime": _tools.RODict({
        "ID": "cityBattle_occupyTime",
        "value": "占领{0}天",
    }),
    "cityBattle_platformDesc": _tools.RODict({
        "ID": "cityBattle_platformDesc",
        "value": "核心区域人数：{0}",
    }),
    "cityBattle_pointsText": _tools.RODict({
        "ID": "cityBattle_pointsText",
        "value": "积分{0}+",
    }),
    "cityBattle_WantedNums": _tools.RODict({
        "ID": "cityBattle_WantedNums",
        "value": "通缉次数：{0}",
    }),
    "cityBattle_activityTime": _tools.RODict({
        "ID": "cityBattle_activityTime",
        "value": "活动时间：{0}-{1}",
    }),
    "cityBattle_startTime": _tools.RODict({
        "ID": "cityBattle_startTime",
        "value": _tools.ROList([2100, 2200]),
    }),
    "cityBattle_pointObtain": _tools.RODict({
        "ID": "cityBattle_pointObtain",
        "value": _tools.ROList([40, 1000, 1000, 1000, 200, 200]),
    }),
    "cityBattle_biddingDelayed": _tools.RODict({
        "ID": "cityBattle_biddingDelayed",
        "value": _tools.ROList([1, 10, 360]),
    }),
    "cityBattle_biddingIncrease": _tools.RODict({
        "ID": "cityBattle_biddingIncrease",
        "value": 10,
    }),
    "cityBattle_attackNumber": _tools.RODict({
        "ID": "cityBattle_attackNumber",
        "value": 60,
    }),
    "cityBattle_defendNumber": _tools.RODict({
        "ID": "cityBattle_defendNumber",
        "value": 60,
    }),
    "cityBattle_prepareTime": _tools.RODict({
        "ID": "cityBattle_prepareTime",
        "value": 10,
    }),
    "cityBattle_fightTime": _tools.RODict({
        "ID": "cityBattle_fightTime",
        "value": 60,
    }),
    "cityBattle_lastTime": _tools.RODict({
        "ID": "cityBattle_lastTime",
        "value": 10,
    }),
    "cityBattle_lastTime2": _tools.RODict({
        "ID": "cityBattle_lastTime2",
        "value": 1,
    }),
    "cityBattle_increasePeople": _tools.RODict({
        "ID": "cityBattle_increasePeople",
        "value": 20,
    }),
    "cityBattle_siegeEnginesTime": _tools.RODict({
        "ID": "cityBattle_siegeEnginesTime",
        "value": 10,
    }),
    "cityBattle_catapultNumber": _tools.RODict({
        "ID": "cityBattle_catapultNumber",
        "value": 2,
    }),
    "cityBattle_biddingNpc": _tools.RODict({
        "ID": "cityBattle_biddingNpc",
        "value": 18000076,
    }),
    "cityBattle_declareNpc": _tools.RODict({
        "ID": "cityBattle_declareNpc",
        "value": 18000513,
    }),
    "cityBattle_systemSwitch": _tools.RODict({
        "ID": "cityBattle_systemSwitch",
        "value": 1,
    }),
    "cityBattle_FirstStartTime": _tools.RODict({
        "ID": "cityBattle_FirstStartTime",
        "value": 1,
    }),
    "cityBattle_serverTimeLimit": _tools.RODict({
        "ID": "cityBattle_serverTimeLimit",
        "value": 3,
    }),
    "cityBattle_biddingTime": _tools.RODict({
        "ID": "cityBattle_biddingTime",
        "value": 5,
    }),
    "cityBattle_BiddingStartTime": _tools.RODict({
        "ID": "cityBattle_BiddingStartTime",
        "value": 12,
    }),
    "cityBattle_BiddingEndTime": _tools.RODict({
        "ID": "cityBattle_BiddingEndTime",
        "value": 12,
    }),
    "cityBattle_countdownBattle": _tools.RODict({
        "ID": "cityBattle_countdownBattle",
        "value": 2,
    }),
    "cityBattle_biddingItem": _tools.RODict({
        "ID": "cityBattle_biddingItem",
        "value": 30000310,
    }),
    "cityBattle_biddingBasePrice": _tools.RODict({
        "ID": "cityBattle_biddingBasePrice",
        "value": 1000,
    }),
    "cityBattle_mailBiddingStart": _tools.RODict({
        "ID": "cityBattle_mailBiddingStart",
        "value": 37001004,
    }),
    "cityBattle_mailBiddingEnd": _tools.RODict({
        "ID": "cityBattle_mailBiddingEnd",
        "value": 37001005,
    }),
    "cityBattle_mailDeclare": _tools.RODict({
        "ID": "cityBattle_mailDeclare",
        "value": _tools.ROList([37001006, 37001015, 37001016]),
    }),
    "cityBattle_mailPointRank": _tools.RODict({
        "ID": "cityBattle_mailPointRank",
        "value": 37001007,
    }),
    "cityBattle_mailReward": _tools.RODict({
        "ID": "cityBattle_mailReward",
        "value": 37001008,
    }),
    "cityBattle_mailWanted": _tools.RODict({
        "ID": "cityBattle_mailWanted",
        "value": 37001009,
    }),
    "cityBattle_mailBattleEnd": _tools.RODict({
        "ID": "cityBattle_mailBattleEnd",
        "value": 37001010,
    }),
    "cityBattle_mailMvp": _tools.RODict({
        "ID": "cityBattle_mailMvp",
        "value": 37001011,
    }),
    "cityBattle_mailBiddingReturn": _tools.RODict({
        "ID": "cityBattle_mailBiddingReturn",
        "value": 37001012,
    }),
    "cityBattle_mailOfficial": _tools.RODict({
        "ID": "cityBattle_mailOfficial",
        "value": 37001013,
    }),
    "cityBattle_noBiddingGuild": _tools.RODict({
        "ID": "cityBattle_noBiddingGuild",
        "value": 37001014,
    }),
    "cityBattle_coreArea": _tools.RODict({
        "ID": "cityBattle_coreArea",
        "value": _tools.ROList([[513.6519, 824.2622], 30]),
    }),
    "cityBattle_monsterId": _tools.RODict({
        "ID": "cityBattle_monsterId",
        "value": 10260001,
    }),
    "cityBattle_biddingCost": _tools.RODict({
        "ID": "cityBattle_biddingCost",
        "value": _tools.ROList([30000007, 10000]),
    }),
    "cityBattle_siegeBossAttack": _tools.RODict({
        "ID": "cityBattle_siegeBossAttack",
        "value": 33,
    }),
    "cityBattle_defenceCrossbow": _tools.RODict({
        "ID": "cityBattle_defenceCrossbow",
        "value": 5,
    }),
    "cityBattle_gateMapID": _tools.RODict({
        "ID": "cityBattle_gateMapID",
        "value": _tools.ROList([60000005, 60000006]),
    }),
    "cityBattle_taxProportion": _tools.RODict({
        "ID": "cityBattle_taxProportion",
        "value": 5,
    }),
    "cityBattle_MapID": _tools.RODict({
        "ID": "cityBattle_MapID",
        "value": 6000,
    }),
    "cityBattle_MvpReward": _tools.RODict({
        "ID": "cityBattle_MvpReward",
        "value": 30000501,
    }),
    "cityBattle_RewardPanelText": _tools.RODict({
        "ID": "cityBattle_RewardPanelText",
        "value": ('奖励信息', '胜利帮会', '失败帮会'),
    }),
    "cityBattle_MoneyID": _tools.RODict({
        "ID": "cityBattle_MoneyID",
        "value": 30000015,
    }),
    "cityBattle_commissariatRes": _tools.RODict({
        "ID": "cityBattle_commissariatRes",
        "value": ('Assets/Res/art/scenes/assets/univ_field_xinyuancheng/prefab/xycz_qz01.prefab', 'Assets/Res/art/scenes/assets/univ_field_xinyuancheng/prefab/xycz_qz02.prefab', 'Assets/Res/art/scenes/assets/univ_field_xinyuancheng/prefab/xycz_qz01.prefab'),
    }),
    "cityBattle_commissariatRes2": _tools.RODict({
        "ID": "cityBattle_commissariatRes2",
        "value": ('Assets/Res/ui/texture/common/com_map_citybattle_map_legend13_icon.png', 'Assets/Res/ui/texture/common/com_map_citybattle_map_legend11_icon.png', 'Assets/Res/ui/texture/common/com_map_citybattle_map_legend12_icon.png'),
    }),
    "cityBattle_reward": _tools.RODict({
        "ID": "cityBattle_reward",
        "value": _tools.ROList([40020831, 1, 0]),
    }),
    "cityBattle_campBuffDemand": _tools.RODict({
        "ID": "cityBattle_campBuffDemand",
        "value": 15,
    }),
    "cityBattle_buffFirstRefresh": _tools.RODict({
        "ID": "cityBattle_buffFirstRefresh",
        "value": 15,
    }),
    "cityBattle_buffNumsOneTime": _tools.RODict({
        "ID": "cityBattle_buffNumsOneTime",
        "value": 20,
    }),
    "cityBattle_buffNumsRefreshGap": _tools.RODict({
        "ID": "cityBattle_buffNumsRefreshGap",
        "value": 10,
    }),
    "cityBattle_buffFirstRefreshMsg": _tools.RODict({
        "ID": "cityBattle_buffFirstRefreshMsg",
        "value": 54003105,
    }),
    "cityBattle_buffRefreshMsg": _tools.RODict({
        "ID": "cityBattle_buffRefreshMsg",
        "value": 54003106,
    }),
    "cityBattle_buffObtainMsg": _tools.RODict({
        "ID": "cityBattle_buffObtainMsg",
        "value": 54003107,
    }),
    "cityBattle_campBuffMsg": _tools.RODict({
        "ID": "cityBattle_campBuffMsg",
        "value": 54003108,
    }),
    "cityBattle_prohibitTeam": _tools.RODict({
        "ID": "cityBattle_prohibitTeam",
        "value": 54003109,
    }),
    "cityBattle_buffPosition": _tools.RODict({
        "ID": "cityBattle_buffPosition",
        "value": _tools.ROList([(577.34, 47.46, 470.47), (557.51, 34.87, 401.95), (483.17, 44.74, 462.68), (438.37, 27.05, 316.68), (400.15, 32.54, 434.58), (594.68, 24.25, 347.78), (689.19, 36.62, 401.51), (731.03, 54.68, 510.65), (674.37, 53.04, 635.71), (657.11, 39.84, 647.12), (664.4, 27.19, 614.57), (649.48, 20.86, 662.53), (585.88, 23.43, 727.02), (637.18, 20.47, 732.81), (592.18, 20.74, 768.89), (577.53, 20.74, 783.65), (546.6, 28.36, 760.39), (477.95, 28.36, 760.39), (513.35, 52.32, 853.43), (431.71, 28.06, 749.83), (431.41, 20.86, 707.53), (435.56, 34.76, 720.35), (455.39, 33.05, 702.47), (380.4, 26.14, 709.73), (394.17, 15.01, 691.18), (379.39, 19.05, 630.68), (412.91, 27.58, 605.1), (463.41, 26.43, 619.42), (516.49, 27.96, 605.1), (584.72, 26.48, 605.1), (584.72, 21.9, 627.39), (516.22, 11.02, 517.68), (291.0, 29.22, 438.68), (340.64, 27.84, 499.51), (388.3, 35.67, 815.45), (342.94, 20.75, 755.3), (345.08, 40.17, 784.91), (326.91, 40.94, 743.04), (584.67, 38.07, 797.6), (624.11, 29.41, 809.54), (618.49, 20.74, 795.87), (614.41, 27.83, 845.47), (685.94, 20.74, 845.1)]),
    }),
    "cityBattle_campbuffActivate": _tools.RODict({
        "ID": "cityBattle_campbuffActivate",
        "value": _tools.ROList([64000097, 64000098, 64000099]),
    }),
    "cityBattle_declarationMaxLength": _tools.RODict({
        "ID": "cityBattle_declarationMaxLength",
        "value": 45,
    }),
    "cityBattle_occupyMapID": _tools.RODict({
        "ID": "cityBattle_occupyMapID",
        "value": _tools.ROList([1001]),
    }),
    "cityBattle_occupyMsg": _tools.RODict({
        "ID": "cityBattle_occupyMsg",
        "value": "欢迎来到[{0}]的帮会领地",
    }),
    "cityBattle_instrumentBelong": _tools.RODict({
        "ID": "cityBattle_instrumentBelong",
        "value": "当前归属：{0}",
    }),
    "cityBattle_neutrality": _tools.RODict({
        "ID": "cityBattle_neutrality",
        "value": "中立方",
    }),
    "cityBattle_instrumentState": _tools.RODict({
        "ID": "cityBattle_instrumentState",
        "value": "当前状态：{0}",
    }),
    "cityBattle_noAwake": _tools.RODict({
        "ID": "cityBattle_noAwake",
        "value": "未唤醒",
    }),
    "cityBattle_awaken": _tools.RODict({
        "ID": "cityBattle_awaken",
        "value": "已唤醒",
    }),
    "cityBattle_crossbowState": _tools.RODict({
        "ID": "cityBattle_crossbowState",
        "value": "{0}号守城弩：{1}",
    }),
    "cityBattle_noDamaged": _tools.RODict({
        "ID": "cityBattle_noDamaged",
        "value": "未损坏",
    }),
    "cityBattle_damaged": _tools.RODict({
        "ID": "cityBattle_damaged",
        "value": "已损坏",
    }),
    "cityBattle_targetDestroyed": _tools.RODict({
        "ID": "cityBattle_targetDestroyed",
        "value": 54003110,
    }),
    "cityBattle_durationHitEffect": _tools.RODict({
        "ID": "cityBattle_durationHitEffect",
        "value": 3,
    }),
    "cityBattle_labelResRoute": _tools.RODict({
        "ID": "cityBattle_labelResRoute",
        "value": ('Assets/Res/ui/texture/common/com_map_citybattle_mapmark01_icon.png', 'Assets/Res/ui/texture/common/com_map_citybattle_mapmark02_icon.png', 'Assets/Res/ui/texture/common/com_map_citybattle_mapmark03_icon.png', 'Assets/Res/ui/texture/common/com_map_citybattle_mapmark04_icon.png', 'Assets/Res/ui/texture/common/com_map_citybattle_mapmark05_icon.png', 'Assets/Res/ui/texture/common/com_map_citybattle_mapmark06_icon.png'),
    }),
    "cityBattle_SpecialEffectsResRoute1": _tools.RODict({
        "ID": "cityBattle_SpecialEffectsResRoute1",
        "value": ('Assets/Res/design/effect/c_chengzhan_guangshuhui.prefab', 'Assets/Res/design/effect/c_chengzhan_guangshuhong.prefab', 'Assets/Res/design/effect/c_chengzhan_guangshulan.prefab'),
    }),
    "cityBattle_SpecialEffectsResRoute2": _tools.RODict({
        "ID": "cityBattle_SpecialEffectsResRoute2",
        "value": "Assets/Res/design/effect/c_chengzhan_pingtaiguangshu.prefab",
    }),
    "cityBattle_campColorID": _tools.RODict({
        "ID": "cityBattle_campColorID",
        "value": _tools.ROList([24, 22]),
    }),
    "cityBattle_cityGatePassageArea": _tools.RODict({
        "ID": "cityBattle_cityGatePassageArea",
        "value": _tools.ROList([514.5, 10.5, 609.7, 10, 30, 12]),
    })
})