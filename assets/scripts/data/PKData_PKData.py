# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: PKData/PKData
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "upperLimitOfMoralValues": _tools.RODict({
        "ID": "upperLimitOfMoralValues",
        "value": 0,
    }),
    "lowerLimitOfMoralValues": _tools.RODict({
        "ID": "lowerLimitOfMoralValues",
        "value": -5000,
    }),
    "deductingMoralValues": _tools.RODict({
        "ID": "deductingMoralValues",
        "value": 250,
    }),
    "increasingMoralValues": _tools.RODict({
        "ID": "increasingMoralValues",
        "value": 0,
    }),
    "differenceInMonsterLv": _tools.RODict({
        "ID": "differenceInMonsterLv",
        "value": 10,
    }),
    "defeatRedPlayerCDTime": _tools.RODict({
        "ID": "defeatRedPlayerCDTime",
        "value": 86400,
    }),
    "defeatRedPlayerMoralValues": _tools.RODict({
        "ID": "defeatRedPlayerMoralValues",
        "value": 34000015,
    }),
    "differenceInPlayerLv": _tools.RODict({
        "ID": "differenceInPlayerLv",
        "value": 10,
    }),
    "redNameValue": _tools.RODict({
        "ID": "redNameValue",
        "value": -500,
    }),
    "yellowNameUpperValue": _tools.RODict({
        "ID": "yellowNameUpperValue",
        "value": _tools.ROList([-499, -200]),
    }),
    "fightBackTime": _tools.RODict({
        "ID": "fightBackTime",
        "value": 300,
    }),
    "PK_changeToPeaceMode_msgID": _tools.RODict({
        "ID": "PK_changeToPeaceMode_msgID",
        "value": 54001540,
    }),
    "PK_changeToShaneMode_msgID": _tools.RODict({
        "ID": "PK_changeToShaneMode_msgID",
        "value": 54001541,
    }),
    "PK_changeToAttackMode_msgID": _tools.RODict({
        "ID": "PK_changeToAttackMode_msgID",
        "value": 54001542,
    }),
    "PK_changeToDuelMode_msgID": _tools.RODict({
        "ID": "PK_changeToDuelMode_msgID",
        "value": 54001546,
    }),
    "PK_changeToHostilityMode_msgID": _tools.RODict({
        "ID": "PK_changeToHostilityMode_msgID",
        "value": 54001547,
    }),
    "PK_changeToActivityMode_msgID": _tools.RODict({
        "ID": "PK_changeToActivityMode_msgID",
        "value": 54001548,
    }),
    "modeCd": _tools.RODict({
        "ID": "modeCd",
        "value": 0.3,
    }),
    "modeCdmsg": _tools.RODict({
        "ID": "modeCdmsg",
        "value": 54000163,
    }),
    "grayNameDuration": _tools.RODict({
        "ID": "grayNameDuration",
        "value": 30,
    }),
    "killPlayer": _tools.RODict({
        "ID": "killPlayer",
        "value": 58000002,
    }),
    "beKilledByPlayer": _tools.RODict({
        "ID": "beKilledByPlayer",
        "value": 58000003,
    }),
    "beKilledByOtherUnit": _tools.RODict({
        "ID": "beKilledByOtherUnit",
        "value": 58000004,
    }),
    "PK_cantUseTransItem_msgID": _tools.RODict({
        "ID": "PK_cantUseTransItem_msgID",
        "value": 54000179,
    }),
    "PK_noEffectText": _tools.RODict({
        "ID": "PK_noEffectText",
        "value": "当前未受到性格惩罚",
    }),
    "PK_effectBoolDisplay": _tools.RODict({
        "ID": "PK_effectBoolDisplay",
        "value": ('√', '×'),
    }),
    "PK_effectBooleanValue": _tools.RODict({
        "ID": "PK_effectBooleanValue",
        "value": ('使用传送道具',),
    }),
    "redNameSuffix": _tools.RODict({
        "ID": "redNameSuffix",
        "value": "[{0}]",
    }),
    "RedScreenWarningBlood": _tools.RODict({
        "ID": "RedScreenWarningBlood",
        "value": 25,
    }),
    "RedScreenWarningResPath": _tools.RODict({
        "ID": "RedScreenWarningResPath",
        "value": "Assets/Res/art/effect/Prefabs/ui/fx_ui_com_hongpingbaojing.prefab",
    }),
    "DeathMail": _tools.RODict({
        "ID": "DeathMail",
        "value": 37001021,
    }),
    "DeathMail_fall": _tools.RODict({
        "ID": "DeathMail_fall",
        "value": 37001022,
    }),
    "DeathMail_abnormalDamage": _tools.RODict({
        "ID": "DeathMail_abnormalDamage",
        "value": 37001023,
    }),
    "abnormalDamageMsg": _tools.RODict({
        "ID": "abnormalDamageMsg",
        "value": 58000214,
    }),
    "redPlayerRecover": _tools.RODict({
        "ID": "redPlayerRecover",
        "value": 8.0,
    }),
    "PK_cantExchangeModel": _tools.RODict({
        "ID": "PK_cantExchangeModel",
        "value": 54003600,
    }),
    "refugeExtendMsg": _tools.RODict({
        "ID": "refugeExtendMsg",
        "value": 54003601,
    }),
    "refugeTimeNoEnough": _tools.RODict({
        "ID": "refugeTimeNoEnough",
        "value": 54003602,
    }),
    "refugeOpenConfirm": _tools.RODict({
        "ID": "refugeOpenConfirm",
        "value": 54003603,
    }),
    "refugeExtendPrompt": _tools.RODict({
        "ID": "refugeExtendPrompt",
        "value": 54003604,
    }),
    "refugeTimeLimit": _tools.RODict({
        "ID": "refugeTimeLimit",
        "value": 8,
    }),
    "refugeExtendTime": _tools.RODict({
        "ID": "refugeExtendTime",
        "value": 1,
    }),
    "refugeBuffId": _tools.RODict({
        "ID": "refugeBuffId",
        "value": 64000146,
    }),
    "refugePrice": _tools.RODict({
        "ID": "refugePrice",
        "value": (30000021, 100),
    }),
    "specialStatusMapId": _tools.RODict({
        "ID": "specialStatusMapId",
        "value": (1026, 1036),
    }),
    "refugeTimeMax": _tools.RODict({
        "ID": "refugeTimeMax",
        "value": 99,
    })
})