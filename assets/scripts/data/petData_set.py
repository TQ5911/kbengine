# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: petData/set
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "petAOI": _tools.RODict({
        "ID": "petAOI",
        "value": 20,
    }),
    "petFollowMinDistance": _tools.RODict({
        "ID": "petFollowMinDistance",
        "value": 0.5,
    }),
    "petFollowMaxDistance": _tools.RODict({
        "ID": "petFollowMaxDistance",
        "value": 1.0,
    }),
    "petFollowArcAngle": _tools.RODict({
        "ID": "petFollowArcAngle",
        "value": 60.0,
    }),
    "petFollowInitialSpeed": _tools.RODict({
        "ID": "petFollowInitialSpeed",
        "value": 6.0,
    }),
    "petFollowAcceleration": _tools.RODict({
        "ID": "petFollowAcceleration",
        "value": 8.0,
    }),
    "petRotateAngle": _tools.RODict({
        "ID": "petRotateAngle",
        "value": 360.0,
    }),
    "petGearConfirm_msgID": _tools.RODict({
        "ID": "petGearConfirm_msgID",
        "value": 54000952,
    }),
    "petTeamNameLength": _tools.RODict({
        "ID": "petTeamNameLength",
        "value": 3,
    }),
    "petTeamNum": _tools.RODict({
        "ID": "petTeamNum",
        "value": 5,
    }),
    "petTeamSwitchCD": _tools.RODict({
        "ID": "petTeamSwitchCD",
        "value": 1,
    }),
    "petTeamSwitchCD_msgID": _tools.RODict({
        "ID": "petTeamSwitchCD_msgID",
        "value": 54000953,
    }),
    "petBagLimitText": _tools.RODict({
        "ID": "petBagLimitText",
        "value": "精灵背包（{0}/{1}）",
    }),
    "petBagCapacity": _tools.RODict({
        "ID": "petBagCapacity",
        "value": 350,
    }),
    "petBagFullMsg": _tools.RODict({
        "ID": "petBagFullMsg",
        "value": 54000011,
    }),
    "petBagFullMail": _tools.RODict({
        "ID": "petBagFullMail",
        "value": 37000021,
    }),
    "petUnlockTips": _tools.RODict({
        "ID": "petUnlockTips",
        "value": 54000955,
    }),
    "petRollProb": _tools.RODict({
        "ID": "petRollProb",
        "value": ((1, 70), (2, 24), (3, 4), (4, 2)),
    }),
    "petRollTicket": _tools.RODict({
        "ID": "petRollTicket",
        "value": 30000235,
    }),
    "petRollPrice": _tools.RODict({
        "ID": "petRollPrice",
        "value": ((1, 1), (10, 11), (100, 110)),
    }),
    "qualitySecuredTriggerNum": _tools.RODict({
        "ID": "qualitySecuredTriggerNum",
        "value": ((1, 0), (2, 0), (3, 30), (4, 60)),
    }),
    "quality3Broadcast": _tools.RODict({
        "ID": "quality3Broadcast",
        "value": 58000006,
    }),
    "quality4Broadcast": _tools.RODict({
        "ID": "quality4Broadcast",
        "value": 58000007,
    }),
    "singleRollText": _tools.RODict({
        "ID": "singleRollText",
        "value": "召唤1次",
    }),
    "batchRollText": _tools.RODict({
        "ID": "batchRollText",
        "value": "召唤10+1次",
    }),
    "batchPlusRollText": _tools.RODict({
        "ID": "batchPlusRollText",
        "value": "召唤100+10次",
    }),
    "petRollSecuredNumText": _tools.RODict({
        "ID": "petRollSecuredNumText",
        "value": "·30次召唤必得史诗品质精灵果\n·60次召唤必得传说品质精灵果\n·获得对应品质精灵果进度重置",
    }),
    "petRollTimesDaily": _tools.RODict({
        "ID": "petRollTimesDaily",
        "value": 9999,
    }),
    "petRollTimesDailyTips": _tools.RODict({
        "ID": "petRollTimesDailyTips",
        "value": "今日剩余召唤次数：{0}",
    }),
    "petRollTimesNotEnoughMsg": _tools.RODict({
        "ID": "petRollTimesNotEnoughMsg",
        "value": 54000950,
    }),
    "firstRollID": _tools.RODict({
        "ID": "firstRollID",
        "value": 15000001,
    }),
    "petFollow": _tools.RODict({
        "ID": "petFollow",
        "value": "跟随",
    }),
    "petCancelFollow": _tools.RODict({
        "ID": "petCancelFollow",
        "value": "取消跟随",
    }),
    "petTeamName": _tools.RODict({
        "ID": "petTeamName",
        "value": ('编队一', '编队二', '编队三', '编队四', '编队五'),
    }),
    "petTeamNameLimit": _tools.RODict({
        "ID": "petTeamNameLimit",
        "value": 54000954,
    }),
    "petTeamNameForbidden": _tools.RODict({
        "ID": "petTeamNameForbidden",
        "value": 54000814,
    }),
    "petTeamNameSave": _tools.RODict({
        "ID": "petTeamNameSave",
        "value": 54000960,
    }),
    "petTeamSwitchMsg": _tools.RODict({
        "ID": "petTeamSwitchMsg",
        "value": 54000961,
    }),
    "petTeamNameEmpty": _tools.RODict({
        "ID": "petTeamNameEmpty",
        "value": 54000962,
    }),
    "petMinLevel": _tools.RODict({
        "ID": "petMinLevel",
        "value": 1,
    }),
    "petMaxLevel": _tools.RODict({
        "ID": "petMaxLevel",
        "value": 5,
    }),
    "petExpOverflowMsg": _tools.RODict({
        "ID": "petExpOverflowMsg",
        "value": 54001800,
    }),
    "petMaxLevelMsg": _tools.RODict({
        "ID": "petMaxLevelMsg",
        "value": 54001801,
    }),
    "petLevelUpFx": _tools.RODict({
        "ID": "petLevelUpFx",
        "value": "Assets/Res/ui/effect/prefab/UIPetPanel_Temp/fx_Temp_shengji.prefab",
    }),
    "petLevelUpFxUI": _tools.RODict({
        "ID": "petLevelUpFxUI",
        "value": (0, 0, 0, 0, 0, 0, 1, 1, 1),
    }),
    "petLevelUpEmpty": _tools.RODict({
        "ID": "petLevelUpEmpty",
        "value": "<color=#dea050>{0}</color>",
    }),
    "petLevelUpPreview": _tools.RODict({
        "ID": "petLevelUpPreview",
        "value": "<color=#dea050>{0}</color><color=#FFFBD7>(+{1})</color>",
    }),
    "petOneClick0": _tools.RODict({
        "ID": "petOneClick0",
        "value": 54000963,
    }),
    "petOneClickLack": _tools.RODict({
        "ID": "petOneClickLack",
        "value": 54000964,
    }),
    "petOneClickOver": _tools.RODict({
        "ID": "petOneClickOver",
        "value": 54000965,
    }),
    "petGearNoSelectMsg": _tools.RODict({
        "ID": "petGearNoSelectMsg",
        "value": 54000966,
    }),
    "petGearUnlockMsg": _tools.RODict({
        "ID": "petGearUnlockMsg",
        "value": 54000967,
    }),
    "petGearWarningMsg": _tools.RODict({
        "ID": "petGearWarningMsg",
        "value": 54000968,
    })
})

qualitySecuredTriggerDic = {3: 30, 4: 60}

