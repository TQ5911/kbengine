# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: const/const
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "createConst_CharLimit": _tools.RODict({
        "ID": "createConst_CharLimit",
        "value": 5,
    }),
    "createConst_BornGamePlayID": _tools.RODict({
        "ID": "createConst_BornGamePlayID",
        "value": 1002,
    }),
    "createConst_BornPos": _tools.RODict({
        "ID": "createConst_BornPos",
        "value": _tools.ROList([((374, 15, 96), 90)]),
    }),
    "defaultGamePlayID": _tools.RODict({
        "ID": "defaultGamePlayID",
        "value": 1001,
    }),
    "maxDmgAvoidance": _tools.RODict({
        "ID": "maxDmgAvoidance",
        "value": 0.85,
    }),
    "minFatalRate": _tools.RODict({
        "ID": "minFatalRate",
        "value": 0.0,
    }),
    "maxFatalRate": _tools.RODict({
        "ID": "maxFatalRate",
        "value": 1.0,
    }),
    "minFatalDmgRatio": _tools.RODict({
        "ID": "minFatalDmgRatio",
        "value": 1.1,
    }),
    "maxFatalDmgRatio": _tools.RODict({
        "ID": "maxFatalDmgRatio",
        "value": 2.0,
    }),
    "monsterMinFatalDmgRatio": _tools.RODict({
        "ID": "monsterMinFatalDmgRatio",
        "value": 1.2,
    }),
    "monsterMaxFatalDmgRatio": _tools.RODict({
        "ID": "monsterMaxFatalDmgRatio",
        "value": 1.25,
    }),
    "minHitRate": _tools.RODict({
        "ID": "minHitRate",
        "value": 0.5,
    }),
    "maxHitRate": _tools.RODict({
        "ID": "maxHitRate",
        "value": 1.0,
    }),
    "dmgAvoidanceLevelRatio": _tools.RODict({
        "ID": "dmgAvoidanceLevelRatio",
        "value": 13.84,
    }),
    "dmgAvoidanceConst": _tools.RODict({
        "ID": "dmgAvoidanceConst",
        "value": 31.16,
    }),
    "dodgeRateLevelRatio": _tools.RODict({
        "ID": "dodgeRateLevelRatio",
        "value": 13.84,
    }),
    "dodgeRateConst": _tools.RODict({
        "ID": "dodgeRateConst",
        "value": 31.16,
    }),
    "hitRateLevelRatio": _tools.RODict({
        "ID": "hitRateLevelRatio",
        "value": 13.84,
    }),
    "hitRateConst": _tools.RODict({
        "ID": "hitRateConst",
        "value": 31.16,
    }),
    "OTRatio": _tools.RODict({
        "ID": "OTRatio",
        "value": 1.2,
    }),
    "hpRecoveryInterval": _tools.RODict({
        "ID": "hpRecoveryInterval",
        "value": 1,
    }),
    "atkBlessToplimit": _tools.RODict({
        "ID": "atkBlessToplimit",
        "value": 9,
    }),
    "armorBlessToplimit": _tools.RODict({
        "ID": "armorBlessToplimit",
        "value": 9,
    }),
    "autoFightTick": _tools.RODict({
        "ID": "autoFightTick",
        "value": 0.5,
    }),
    "autoFightRange": _tools.RODict({
        "ID": "autoFightRange",
        "value": 30,
    }),
    "autoFightFollowRange": _tools.RODict({
        "ID": "autoFightFollowRange",
        "value": 30,
    }),
    "autoFightEnterTime": _tools.RODict({
        "ID": "autoFightEnterTime",
        "value": 0.1,
    }),
    "autoFightFailRetryNum": _tools.RODict({
        "ID": "autoFightFailRetryNum",
        "value": 10,
    }),
    "autoFightFailMsg": _tools.RODict({
        "ID": "autoFightFailMsg",
        "value": 54001519,
    }),
    "treatmentSkillLimit": _tools.RODict({
        "ID": "treatmentSkillLimit",
        "value": 0.8,
    }),
    "autoFightReturnRange": _tools.RODict({
        "ID": "autoFightReturnRange",
        "value": (20, 50),
    }),
    "dropTime": _tools.RODict({
        "ID": "dropTime",
        "value": 4.0,
    }),
    "dropDelay": _tools.RODict({
        "ID": "dropDelay",
        "value": 2.0,
    }),
    "dropShareRange": _tools.RODict({
        "ID": "dropShareRange",
        "value": 50.0,
    }),
    "dropFxTime": _tools.RODict({
        "ID": "dropFxTime",
        "value": 0.733,
    }),
    "dropRewardAndBagFull_mailID": _tools.RODict({
        "ID": "dropRewardAndBagFull_mailID",
        "value": 37000001,
    }),
    "moveSkill_cameraMoveTime": _tools.RODict({
        "ID": "moveSkill_cameraMoveTime",
        "value": 0.5,
    }),
    "raidMemberLimit": _tools.RODict({
        "ID": "raidMemberLimit",
        "value": 40,
    }),
    "raidTeamLimit": _tools.RODict({
        "ID": "raidTeamLimit",
        "value": 8,
    }),
    "raidApplyLimit": _tools.RODict({
        "ID": "raidApplyLimit",
        "value": 50,
    }),
    "raidUnlcokLevel": _tools.RODict({
        "ID": "raidUnlcokLevel",
        "value": 40,
    }),
    "raidInvDeniedMsg": _tools.RODict({
        "ID": "raidInvDeniedMsg",
        "value": 54000111,
    }),
    "showNearestMonsterDistance": _tools.RODict({
        "ID": "showNearestMonsterDistance",
        "value": 24.0,
    }),
    "nearestMonsterJiantouFx": _tools.RODict({
        "ID": "nearestMonsterJiantouFx",
        "value": 31900005,
    }),
    "fightToIdleChangeTime": _tools.RODict({
        "ID": "fightToIdleChangeTime",
        "value": 5.0,
    }),
    "changeDirAngelThreshold": _tools.RODict({
        "ID": "changeDirAngelThreshold",
        "value": 120,
    }),
    "targetIsOutOfRange": _tools.RODict({
        "ID": "targetIsOutOfRange",
        "value": 54000134,
    }),
    "targetIsOutOfRange_butCasted": _tools.RODict({
        "ID": "targetIsOutOfRange_butCasted",
        "value": 54002242,
    }),
    "hitAniInterval": _tools.RODict({
        "ID": "hitAniInterval",
        "value": 0.0,
    }),
    "leisureTime": _tools.RODict({
        "ID": "leisureTime",
        "value": (10, 25),
    }),
    "leaveFightStateTime": _tools.RODict({
        "ID": "leaveFightStateTime",
        "value": 8.0,
    }),
    "leaveLockTargerTime": _tools.RODict({
        "ID": "leaveLockTargerTime",
        "value": 3.5,
    }),
    "monsterGoHomeBuffList": _tools.RODict({
        "ID": "monsterGoHomeBuffList",
        "value": _tools.ROList([64000203, 64000072]),
    }),
    "deadDisappearTime_base": _tools.RODict({
        "ID": "deadDisappearTime_base",
        "value": 1.0,
    }),
    "deadDisappearTime_max": _tools.RODict({
        "ID": "deadDisappearTime_max",
        "value": 3.0,
    }),
    "hpAlert": _tools.RODict({
        "ID": "hpAlert",
        "value": 0.2,
    }),
    "skillPreReleaseTime": _tools.RODict({
        "ID": "skillPreReleaseTime",
        "value": 0.5,
    }),
    "maxPropertiesType": _tools.RODict({
        "ID": "maxPropertiesType",
        "value": 11,
    }),
    "pickBeforeAct": _tools.RODict({
        "ID": "pickBeforeAct",
        "value": "idle01",
    }),
    "pickingAct": _tools.RODict({
        "ID": "pickingAct",
        "value": "beCatched01",
    }),
    "pickAfterAct": _tools.RODict({
        "ID": "pickAfterAct",
        "value": "idle02",
    }),
    "pickingOpening": _tools.RODict({
        "ID": "pickingOpening",
        "value": "opening",
    }),
    "xuanzhongNPCMat": _tools.RODict({
        "ID": "xuanzhongNPCMat",
        "value": "Assets/Res/art/effectRes/Textures/other/Materials/Fresnel_shanbai.mat",
    }),
    "raidApplyDuration": _tools.RODict({
        "ID": "raidApplyDuration",
        "value": 10,
    }),
    "raidPressTime": _tools.RODict({
        "ID": "raidPressTime",
        "value": 0.1,
    }),
    "selectRange": _tools.RODict({
        "ID": "selectRange",
        "value": 40,
    }),
    "selectRangeInRaid": _tools.RODict({
        "ID": "selectRangeInRaid",
        "value": 80,
    }),
    "clickDistanceSqr": _tools.RODict({
        "ID": "clickDistanceSqr",
        "value": 600,
    }),
    "renameItem": _tools.RODict({
        "ID": "renameItem",
        "value": 30000237,
    }),
    "startPosIllegalMsg": _tools.RODict({
        "ID": "startPosIllegalMsg",
        "value": 54001551,
    }),
    "teleportStart": _tools.RODict({
        "ID": "teleportStart",
        "value": 31900019,
    }),
    "teleportStartLoopTime": _tools.RODict({
        "ID": "teleportStartLoopTime",
        "value": 1.8,
    }),
    "navigationWaypointMin": _tools.RODict({
        "ID": "navigationWaypointMin",
        "value": 40,
    }),
    "navigationWaypointHeightMin": _tools.RODict({
        "ID": "navigationWaypointHeightMin",
        "value": 5,
    }),
    "navigationIllegalMsg": _tools.RODict({
        "ID": "navigationIllegalMsg",
        "value": 54001227,
    }),
    "eternalItemIDList": _tools.RODict({
        "ID": "eternalItemIDList",
        "value": set([30050087,30001044,30001045,30001301,30001302]),
    }),
    "teleportStoneInvalidMsg": _tools.RODict({
        "ID": "teleportStoneInvalidMsg",
        "value": 54001273,
    }),
    "teleportCastTime": _tools.RODict({
        "ID": "teleportCastTime",
        "value": 3,
    }),
    "antiAddictAgeReminder": _tools.RODict({
        "ID": "antiAddictAgeReminder",
        "value": 54002000,
    }),
    "antiAddictPermittedTime": _tools.RODict({
        "ID": "antiAddictPermittedTime",
        "value": 54002001,
    }),
    "antiAddictForbiddenTime": _tools.RODict({
        "ID": "antiAddictForbiddenTime",
        "value": 54002002,
    }),
    "antiAddictForceLogout": _tools.RODict({
        "ID": "antiAddictForceLogout",
        "value": 54002003,
    }),
    "antiAddictAgeUnder16": _tools.RODict({
        "ID": "antiAddictAgeUnder16",
        "value": 54002004,
    }),
    "maxLevel": _tools.RODict({
        "ID": "maxLevel",
        "value": 90,
    }),
    "bankSortCooldown": _tools.RODict({
        "ID": "bankSortCooldown",
        "value": 10,
    }),
    "outOfStuckTimeLimit": _tools.RODict({
        "ID": "outOfStuckTimeLimit",
        "value": 60,
    }),
    "outOfStuckCDMsg": _tools.RODict({
        "ID": "outOfStuckCDMsg",
        "value": 54000031,
    }),
    "clientNpcAOI": _tools.RODict({
        "ID": "clientNpcAOI",
        "value": 50,
    }),
    "goalListQuantityt": _tools.RODict({
        "ID": "goalListQuantityt",
        "value": 8,
    }),
    "refreshGoalListcd": _tools.RODict({
        "ID": "refreshGoalListcd",
        "value": 3.0,
    }),
    "autoChooseTarget_FxID": _tools.RODict({
        "ID": "autoChooseTarget_FxID",
        "value": 31600007,
    }),
    "noOtherMedicinee_msgID": _tools.RODict({
        "ID": "noOtherMedicinee_msgID",
        "value": 54000196,
    }),
    "deathTimesToCancelAutoReturn": _tools.RODict({
        "ID": "deathTimesToCancelAutoReturn",
        "value": 3,
    }),
    "autoFightSettingsDefaultStatus": _tools.RODict({
        "ID": "autoFightSettingsDefaultStatus",
        "value": (1, 1, 0, 0, 1, 0),
    }),
    "autoFightSettingsReliveTime": _tools.RODict({
        "ID": "autoFightSettingsReliveTime",
        "value": 1,
    }),
    "autoHealHpAndMpPct": _tools.RODict({
        "ID": "autoHealHpAndMpPct",
        "value": (0.8, 0.8),
    }),
    "lackOfItem_msgID": _tools.RODict({
        "ID": "lackOfItem_msgID",
        "value": 54000191,
    }),
    "conflict_common_msgID": _tools.RODict({
        "ID": "conflict_common_msgID",
        "value": 54000052,
    }),
    "mpNotEnough_msgID": _tools.RODict({
        "ID": "mpNotEnough_msgID",
        "value": 54000028,
    }),
    "getRewardAndBagFull_mailID": _tools.RODict({
        "ID": "getRewardAndBagFull_mailID",
        "value": 37000002,
    }),
    "getRewardAndBagLock_mailID": _tools.RODict({
        "ID": "getRewardAndBagLock_mailID",
        "value": 37000020,
    }),
    "renameEmptyTip": _tools.RODict({
        "ID": "renameEmptyTip",
        "value": 54001017,
    }),
    "renameConfirmTip": _tools.RODict({
        "ID": "renameConfirmTip",
        "value": 54000807,
    }),
    "forbiddenContent": _tools.RODict({
        "ID": "forbiddenContent",
        "value": 54000814,
    }),
    "cameraLock_SwitchSpeed": _tools.RODict({
        "ID": "cameraLock_SwitchSpeed",
        "value": 0.5,
    }),
    "BattleCameraRotY": _tools.RODict({
        "ID": "BattleCameraRotY",
        "value": 26.0,
    }),
    "25DCameraYRotation": _tools.RODict({
        "ID": "25DCameraYRotation",
        "value": 13.5,
    }),
    "25DCameraDefault": _tools.RODict({
        "ID": "25DCameraDefault",
        "value": 33010015,
    }),
    "25DCameraRideDefault": _tools.RODict({
        "ID": "25DCameraRideDefault",
        "value": 33010016,
    }),
    "stepSoundDistance": _tools.RODict({
        "ID": "stepSoundDistance",
        "value": 24,
    }),
    "defaultArea": _tools.RODict({
        "ID": "defaultArea",
        "value": 0,
    }),
    "resetPositionSuccessMsg": _tools.RODict({
        "ID": "resetPositionSuccessMsg",
        "value": 54001778,
    }),
    "musicVolume": _tools.RODict({
        "ID": "musicVolume",
        "value": 0.5,
    }),
    "soundEffectVolume": _tools.RODict({
        "ID": "soundEffectVolume",
        "value": 0.5,
    }),
    "entitiesRefreshOnTime": _tools.RODict({
        "ID": "entitiesRefreshOnTime",
        "value": _tools.ROList([10001064, 20001117, 20001118, 11000001]),
    }),
    "formatOfLevels": _tools.RODict({
        "ID": "formatOfLevels",
        "value": "{0}级",
    }),
    "PowerChangedMsgID": _tools.RODict({
        "ID": "PowerChangedMsgID",
        "value": 54000152,
    }),
    "PropertyChangedMsgID": _tools.RODict({
        "ID": "PropertyChangedMsgID",
        "value": 54000154,
    }),
    "worldMapBgRes": _tools.RODict({
        "ID": "worldMapBgRes",
        "value": "Assets/Res/ui/texturenp/worldmap/worldmap_taotal_bg_img.png",
    }),
    "highFallingMsgID": _tools.RODict({
        "ID": "highFallingMsgID",
        "value": 58000023,
    }),
    "playerDamageOffset": _tools.RODict({
        "ID": "playerDamageOffset",
        "value": ((80, -120), (110, -120), (130, 20), (-130, -100), (-115, -20), (-115, 0), (-170, -100), (-170, -40), (0, -80), (0, -80), (80, -120), (110, -120)),
    }),
    "othersDamageOffset": _tools.RODict({
        "ID": "othersDamageOffset",
        "value": ((70, 30), (80, 50), (130, 20), (130, -100), (-115, -20), (-115, 0), (170, -100), (170, -40), (0, -80), (0, -80), (90, 30), (90, 70)),
    }),
    "playerDamageHudscale": _tools.RODict({
        "ID": "playerDamageHudscale",
        "value": ((0, 5.625, 9, 30, 10000), (2, 1, 1, 0.5, 0.5)),
    }),
    "othersDamageHudscale": _tools.RODict({
        "ID": "othersDamageHudscale",
        "value": ((0, 5.625, 9, 30, 10000), (2, 1, 1, 0.5, 0.5)),
    }),
    "beDrownLimit": _tools.RODict({
        "ID": "beDrownLimit",
        "value": 1.5,
    }),
    "itemUnboundProb": _tools.RODict({
        "ID": "itemUnboundProb",
        "value": 0.0,
    }),
    "ultimatePowerMax": _tools.RODict({
        "ID": "ultimatePowerMax",
        "value": 100,
    }),
    "uiVisibleLvLimitMsg": _tools.RODict({
        "ID": "uiVisibleLvLimitMsg",
        "value": 54000159,
    }),
    "uiVisibleTaskLimitMsg": _tools.RODict({
        "ID": "uiVisibleTaskLimitMsg",
        "value": 54000160,
    }),
    "uiVisiblePropmt": _tools.RODict({
        "ID": "uiVisiblePropmt",
        "value": 54001959,
    }),
    "leaveTheScene": _tools.RODict({
        "ID": "leaveTheScene",
        "value": 54001966,
    }),
    "taskGuideFx": _tools.RODict({
        "ID": "taskGuideFx",
        "value": "Assets/Res/art/effect/Prefabs/common/Common_xunluzhiyin.prefab",
    }),
    "taskGuideFxStep": _tools.RODict({
        "ID": "taskGuideFxStep",
        "value": 5,
    }),
    "taskGuideFxInterval": _tools.RODict({
        "ID": "taskGuideFxInterval",
        "value": 3.5,
    }),
    "taskGuideFxAfterIntrTime": _tools.RODict({
        "ID": "taskGuideFxAfterIntrTime",
        "value": 30,
    }),
    "taskGuideFxDestroyTime": _tools.RODict({
        "ID": "taskGuideFxDestroyTime",
        "value": 5.0,
    }),
    "taskGuideFxSpeed": _tools.RODict({
        "ID": "taskGuideFxSpeed",
        "value": 2.5,
    }),
    "taskGuideUICenterOffset": _tools.RODict({
        "ID": "taskGuideUICenterOffset",
        "value": (0, 56),
    }),
    "taskGuideUIEllipseSemiAxes": _tools.RODict({
        "ID": "taskGuideUIEllipseSemiAxes",
        "value": (607, 350),
    }),
    "taskGuideUIFxHighMount": _tools.RODict({
        "ID": "taskGuideUIFxHighMount",
        "value": 0.5,
    }),
    "resolution_set": _tools.RODict({
        "ID": "resolution_set",
        "value": 54001968,
    }),
    "translucentRangeCamera": _tools.RODict({
        "ID": "translucentRangeCamera",
        "value": (1, 1.5),
    }),
    "taskGuideFxNum": _tools.RODict({
        "ID": "taskGuideFxNum",
        "value": 20,
    }),
    "taskGuideFxAfterIntrInterval": _tools.RODict({
        "ID": "taskGuideFxAfterIntrInterval",
        "value": 4.0,
    }),
    "backBattleRecoveryPer": _tools.RODict({
        "ID": "backBattleRecoveryPer",
        "value": 10.0,
    }),
    "summonBcakRange": _tools.RODict({
        "ID": "summonBcakRange",
        "value": 30,
    }),
    "selectTargetTooFarMsg": _tools.RODict({
        "ID": "selectTargetTooFarMsg",
        "value": 54000624,
    }),
    "reliveTime": _tools.RODict({
        "ID": "reliveTime",
        "value": 2,
    }),
    "killMonsterLowerExpBonus": _tools.RODict({
        "ID": "killMonsterLowerExpBonus",
        "value": 0.04,
    }),
    "killMonsterHighExpBonus": _tools.RODict({
        "ID": "killMonsterHighExpBonus",
        "value": 0.04,
    }),
    "killMonsterTeamExpBonus": _tools.RODict({
        "ID": "killMonsterTeamExpBonus",
        "value": (1, 1.1, 1.2, 1.35, 1.5),
    }),
    "claimTaskTips": _tools.RODict({
        "ID": "claimTaskTips",
        "value": 54990062,
    }),
    "monsterSkillRange": _tools.RODict({
        "ID": "monsterSkillRange",
        "value": 2.5,
    }),
    "monsterSkillRangeTriggerCD": _tools.RODict({
        "ID": "monsterSkillRangeTriggerCD",
        "value": 3,
    }),
    "monsterSkillRangeCoefficient": _tools.RODict({
        "ID": "monsterSkillRangeCoefficient",
        "value": 0.2,
    }),
    "taskFuLingMsg": _tools.RODict({
        "ID": "taskFuLingMsg",
        "value": 54003100,
    }),
    "changeSceneFxId": _tools.RODict({
        "ID": "changeSceneFxId",
        "value": 31710002,
    }),
    "SelectRolePositon": _tools.RODict({
        "ID": "SelectRolePositon",
        "value": ((2.03, -2.4, -27.96), (2.03, -2.4, -27.96), (-1.674, 180, 0), (-1.674, 180, 0)),
    }),
    "BossProfileRange": _tools.RODict({
        "ID": "BossProfileRange",
        "value": 6400.0,
    }),
    "killRecordTimeLimit": _tools.RODict({
        "ID": "killRecordTimeLimit",
        "value": 60,
    }),
    "summonUnlockedLv": _tools.RODict({
        "ID": "summonUnlockedLv",
        "value": ((11002005, 1), (11002006, 5), (11002007, 12)),
    }),
    "transportcost": _tools.RODict({
        "ID": "transportcost",
        "value": 1000,
    }),
    "transportcostMsg": _tools.RODict({
        "ID": "transportcostMsg",
        "value": 54990064,
    }),
    "taskExceedReturn": _tools.RODict({
        "ID": "taskExceedReturn",
        "value": 50,
    }),
    "SummonChangeTips": _tools.RODict({
        "ID": "SummonChangeTips",
        "value": 54003104,
    }),
    "damageHeightLimit": _tools.RODict({
        "ID": "damageHeightLimit",
        "value": 12.0,
    }),
    "isMonsterTauntImmunityTime": _tools.RODict({
        "ID": "isMonsterTauntImmunityTime",
        "value": 10,
    }),
    "isBossTauntImmunityTime": _tools.RODict({
        "ID": "isBossTauntImmunityTime",
        "value": 30,
    }),
    "popupNotificationAutoClose": _tools.RODict({
        "ID": "popupNotificationAutoClose",
        "value": "<color=#e4dabd>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口",
    }),
    "rewardPopupQualityLowList": _tools.RODict({
        "ID": "rewardPopupQualityLowList",
        "value": (30000002, 30000003),
    }),
    "rewardPopupQualityHigh": _tools.RODict({
        "ID": "rewardPopupQualityHigh",
        "value": 2,
    }),
    "selectedDuration": _tools.RODict({
        "ID": "selectedDuration",
        "value": 10,
    }),
    "selectedListReselect": _tools.RODict({
        "ID": "selectedListReselect",
        "value": 3,
    }),
    "selectedTargetMonster": _tools.RODict({
        "ID": "selectedTargetMonster",
        "value": "Assets/Res/ui/texture/maincity/target_monster_icon.png",
    }),
    "selectedTargetNeutrality": _tools.RODict({
        "ID": "selectedTargetNeutrality",
        "value": "Assets/Res/ui/texture/common/Selection_neutrality_Icon.png",
    }),
    "nearbyListLimit": _tools.RODict({
        "ID": "nearbyListLimit",
        "value": 15,
    }),
    "teleportTime": _tools.RODict({
        "ID": "teleportTime",
        "value": 3,
    }),
    "selectedCheckLine": _tools.RODict({
        "ID": "selectedCheckLine",
        "value": "Assets/Res/art/effect/Prefabs/common/PlayerCheckLine.prefab",
    }),
    "teamMarkLimit": _tools.RODict({
        "ID": "teamMarkLimit",
        "value": 25,
    }),
    "customizedMail": _tools.RODict({
        "ID": "customizedMail",
        "value": 37001001,
    }),
    "flashWindowEndMsg": _tools.RODict({
        "ID": "flashWindowEndMsg",
        "value": 54001991,
    }),
    "flashWindowEvent": _tools.RODict({
        "ID": "flashWindowEvent",
        "value": "限时活动",
    }),
    "flashWindowMall": _tools.RODict({
        "ID": "flashWindowMall",
        "value": "商城上新",
    }),
    "bloodBase": _tools.RODict({
        "ID": "bloodBase",
        "value": 10000,
    }),
    "bloodLowLimit": _tools.RODict({
        "ID": "bloodLowLimit",
        "value": 5000,
    }),
    "bloodTransientTime": _tools.RODict({
        "ID": "bloodTransientTime",
        "value": 5000,
    }),
    "bloodInvincible": _tools.RODict({
        "ID": "bloodInvincible",
        "value": 64000070,
    }),
    "bloodCycle": _tools.RODict({
        "ID": "bloodCycle",
        "value": (216, 220, 221, 222),
    }),
    "chestOpened": _tools.RODict({
        "ID": "chestOpened",
        "value": 0.3,
    }),
    "followRadius": _tools.RODict({
        "ID": "followRadius",
        "value": 3,
    }),
    "basicStaTitle1": _tools.RODict({
        "ID": "basicStaTitle1",
        "value": "基础属性",
    }),
    "basicStaTitle2": _tools.RODict({
        "ID": "basicStaTitle2",
        "value": "进阶属性",
    }),
    "basicStaTitle3": _tools.RODict({
        "ID": "basicStaTitle3",
        "value": "控制属性",
    }),
    "basicStaTitle4": _tools.RODict({
        "ID": "basicStaTitle4",
        "value": "附加属性",
    }),
    "basicStaIcon1": _tools.RODict({
        "ID": "basicStaIcon1",
        "value": "Assets/Res/ui/texture/attribute/attribute_titleicon01_icon.png",
    }),
    "basicStaIcon2": _tools.RODict({
        "ID": "basicStaIcon2",
        "value": "Assets/Res/ui/texture/attribute/attribute_titleicon02_icon.png",
    }),
    "basicStaIcon3": _tools.RODict({
        "ID": "basicStaIcon3",
        "value": "Assets/Res/ui/texture/attribute/attribute_titleicon03_icon.png",
    }),
    "basicStaIcon4": _tools.RODict({
        "ID": "basicStaIcon4",
        "value": "Assets/Res/ui/texture/attribute/attribute_titleicon04_icon.png",
    }),
    "homepageMe": _tools.RODict({
        "ID": "homepageMe",
        "value": "我的信息",
    }),
    "homepageOthers": _tools.RODict({
        "ID": "homepageOthers",
        "value": "他人信息",
    }),
    "homepageNoGuild": _tools.RODict({
        "ID": "homepageNoGuild",
        "value": "暂无帮会",
    }),
    "homepageOthersNoGuild": _tools.RODict({
        "ID": "homepageOthersNoGuild",
        "value": 54000379,
    }),
    "copyNameSuccess": _tools.RODict({
        "ID": "copyNameSuccess",
        "value": 54000380,
    }),
    "homepageRank": _tools.RODict({
        "ID": "homepageRank",
        "value": "第{0}名",
    }),
    "messageDelayAfterDeath": _tools.RODict({
        "ID": "messageDelayAfterDeath",
        "value": 600,
    }),
    "pathFindingTargetScope": _tools.RODict({
        "ID": "pathFindingTargetScope",
        "value": 5,
    }),
    "pathFindingTargetSceneChange": _tools.RODict({
        "ID": "pathFindingTargetSceneChange",
        "value": 54000716,
    }),
    "pathFindingFinish": _tools.RODict({
        "ID": "pathFindingFinish",
        "value": 54000717,
    }),
    "pathFindingInterrupt": _tools.RODict({
        "ID": "pathFindingInterrupt",
        "value": 54000718,
    }),
    "monsterResetCount": _tools.RODict({
        "ID": "monsterResetCount",
        "value": 8,
    }),
    "monsterResetTimer": _tools.RODict({
        "ID": "monsterResetTimer",
        "value": 15,
    }),
    "systemSwitch": _tools.RODict({
        "ID": "systemSwitch",
        "value": 54481003,
    }),
    "OnDeadLaterTime": _tools.RODict({
        "ID": "OnDeadLaterTime",
        "value": 2,
    }),
    "autoGatherVerticalMaxDistance": _tools.RODict({
        "ID": "autoGatherVerticalMaxDistance",
        "value": 3,
    }),
    "dpsStaText1": _tools.RODict({
        "ID": "dpsStaText1",
        "value": "伤害统计",
    }),
    "dpsStaText2": _tools.RODict({
        "ID": "dpsStaText2",
        "value": "治疗统计",
    }),
    "dpsStaText3": _tools.RODict({
        "ID": "dpsStaText3",
        "value": "承伤统计",
    }),
    "dpsStaText4": _tools.RODict({
        "ID": "dpsStaText4",
        "value": "重置数据",
    }),
    "dpsRankText1": _tools.RODict({
        "ID": "dpsRankText1",
        "value": "伤害排行",
    }),
    "dpsRankText2": _tools.RODict({
        "ID": "dpsRankText2",
        "value": "治疗排行",
    }),
    "dpsRankText3": _tools.RODict({
        "ID": "dpsRankText3",
        "value": "承伤排行",
    }),
    "dpsResetCheck": _tools.RODict({
        "ID": "dpsResetCheck",
        "value": 54000386,
    }),
    "dpsResetFeedback": _tools.RODict({
        "ID": "dpsResetFeedback",
        "value": 54000387,
    }),
    "dpsUpdateCD": _tools.RODict({
        "ID": "dpsUpdateCD",
        "value": 3,
    }),
    "dpsMyRank": _tools.RODict({
        "ID": "dpsMyRank",
        "value": "第{0}名 {1}",
    }),
    "dialogbuttonleave": _tools.RODict({
        "ID": "dialogbuttonleave",
        "value": 15.0,
    }),
    "function_notAvailable": _tools.RODict({
        "ID": "function_notAvailable",
        "value": 54003127,
    }),
    "offlineRetentionTime": _tools.RODict({
        "ID": "offlineRetentionTime",
        "value": 5,
    }),
    "maxAccumulateTime": _tools.RODict({
        "ID": "maxAccumulateTime",
        "value": 3360,
    }),
    "offlineTriggerMin": _tools.RODict({
        "ID": "offlineTriggerMin",
        "value": 9,
    }),
    "offlineMail": _tools.RODict({
        "ID": "offlineMail",
        "value": 37000016,
    }),
    "monsterCombatPathingMaxAngle": _tools.RODict({
        "ID": "monsterCombatPathingMaxAngle",
        "value": 34010039,
    }),
    "monsterCombatPathingMaxTurnAngle": _tools.RODict({
        "ID": "monsterCombatPathingMaxTurnAngle",
        "value": 6,
    }),
    "monsterPathingWeight": _tools.RODict({
        "ID": "monsterPathingWeight",
        "value": 1,
    }),
    "monsterCombatingWeight": _tools.RODict({
        "ID": "monsterCombatingWeight",
        "value": 2,
    }),
    "monsterCombatPathingTime": _tools.RODict({
        "ID": "monsterCombatPathingTime",
        "value": 3,
    }),
    "chat_banned": _tools.RODict({
        "ID": "chat_banned",
        "value": 54001558,
    }),
    "uiVisibleDayLimit": _tools.RODict({
        "ID": "uiVisibleDayLimit",
        "value": 54481004,
    }),
    "bossRefreshSystem": _tools.RODict({
        "ID": "bossRefreshSystem",
        "value": 2,
    }),
    "mapHelpInfo": _tools.RODict({
        "ID": "mapHelpInfo",
        "value": 50,
    }),
    "constBornPosName": _tools.RODict({
        "ID": "constBornPosName",
        "value": "出生点",
    }),
    "constRebornPosName": _tools.RODict({
        "ID": "constRebornPosName",
        "value": "复活点",
    }),
    "loginVideoFilePath": _tools.RODict({
        "ID": "loginVideoFilePath",
        "value": "login_video.mp4",
    }),
    "loginVideoFilePath_Mobile": _tools.RODict({
        "ID": "loginVideoFilePath_Mobile",
        "value": "login_video_mobile.mp4",
    }),
    "shareSuccessMsg": _tools.RODict({
        "ID": "shareSuccessMsg",
        "value": 54920009,
    }),
    "shareFailedMsg": _tools.RODict({
        "ID": "shareFailedMsg",
        "value": 54920012,
    }),
    "saveSuccessMsg": _tools.RODict({
        "ID": "saveSuccessMsg",
        "value": 54920010,
    }),
    "saveFailedMsg": _tools.RODict({
        "ID": "saveFailedMsg",
        "value": 54920011,
    }),
    "photoMinDistance": _tools.RODict({
        "ID": "photoMinDistance",
        "value": 1.5,
    }),
    "wechatFailedJump": _tools.RODict({
        "ID": "wechatFailedJump",
        "value": 54000390,
    }),
    "pathFindAutoRide": _tools.RODict({
        "ID": "pathFindAutoRide",
        "value": 5.0,
    }),
    "pathFindAutoRun": _tools.RODict({
        "ID": "pathFindAutoRun",
        "value": 5.0,
    }),
    "regularTurn": _tools.RODict({
        "ID": "regularTurn",
        "value": 600,
    }),
    "ridingTurn": _tools.RODict({
        "ID": "ridingTurn",
        "value": 420,
    }),
    "teleportationProtectionBuffId": _tools.RODict({
        "ID": "teleportationProtectionBuffId",
        "value": 64000126,
    }),
    "teleportationProtectionTime": _tools.RODict({
        "ID": "teleportationProtectionTime",
        "value": 5,
    }),
    "legalRegulationsTest": _tools.RODict({
        "ID": "legalRegulationsTest",
        "value": "http://192.168.10.16:3007/#/privacy",
    }),
    "legalRegulations": _tools.RODict({
        "ID": "legalRegulations",
        "value": "https://api.yunxingu.com/mobile/index.html/#/privacy",
    }),
    "taskQualityTest": _tools.RODict({
        "ID": "taskQualityTest",
        "value": "简单#困难#危险",
    }),
    "skillFrequentNormal": _tools.RODict({
        "ID": "skillFrequentNormal",
        "value": (2, 2),
    }),
    "mainLockTime": _tools.RODict({
        "ID": "mainLockTime",
        "value": (-1, 5, 15, 30),
    }),
    "mainLockTimeDefaultStatus": _tools.RODict({
        "ID": "mainLockTimeDefaultStatus",
        "value": 2,
    }),
    "mainLockDefaultStatus": _tools.RODict({
        "ID": "mainLockDefaultStatus",
        "value": 1,
    }),
    "mainLockTimeTxt": _tools.RODict({
        "ID": "mainLockTimeTxt",
        "value": "{0}分钟",
    }),
    "taskReset": _tools.RODict({
        "ID": "taskReset",
        "value": 54002167,
    }),
    "iDoYouWantToResetTheTask": _tools.RODict({
        "ID": "iDoYouWantToResetTheTask",
        "value": 54002168,
    }),
    "functionNotAvailable": _tools.RODict({
        "ID": "functionNotAvailable",
        "value": 54481006,
    }),
    "conflictSkill": _tools.RODict({
        "ID": "conflictSkill",
        "value": 54000003,
    }),
    "fallFastEndTime": _tools.RODict({
        "ID": "fallFastEndTime",
        "value": 0.6,
    }),
    "fallEndTime": _tools.RODict({
        "ID": "fallEndTime",
        "value": 0.0,
    }),
    "EpCannotFly": _tools.RODict({
        "ID": "EpCannotFly",
        "value": 54481011,
    }),
    "areaCannotFly": _tools.RODict({
        "ID": "areaCannotFly",
        "value": 54481008,
    }),
    "rewardDeposit": _tools.RODict({
        "ID": "rewardDeposit",
        "value": 100,
    }),
    "InitialAmount": _tools.RODict({
        "ID": "InitialAmount",
        "value": 100,
    }),
    "InitialTopAmount": _tools.RODict({
        "ID": "InitialTopAmount",
        "value": 999999,
    }),
    "rewardLimit": _tools.RODict({
        "ID": "rewardLimit",
        "value": 5,
    }),
    "listCD": _tools.RODict({
        "ID": "listCD",
        "value": 3,
    }),
    "killTime": _tools.RODict({
        "ID": "killTime",
        "value": 1,
    }),
    "specifyKillTime": _tools.RODict({
        "ID": "specifyKillTime",
        "value": 1,
    }),
    "killerRefreshTime": _tools.RODict({
        "ID": "killerRefreshTime",
        "value": 7,
    }),
    "BountyTaxRate": _tools.RODict({
        "ID": "BountyTaxRate",
        "value": 10,
    }),
    "Bounty_KillingSuccess": _tools.RODict({
        "ID": "Bounty_KillingSuccess",
        "value": 37002001,
    }),
    "Bounty_OrderSuccess": _tools.RODict({
        "ID": "Bounty_OrderSuccess",
        "value": 37002002,
    }),
    "Bounty_OrderFailed": _tools.RODict({
        "ID": "Bounty_OrderFailed",
        "value": 37002003,
    }),
    "Bounty_KillingFailed": _tools.RODict({
        "ID": "Bounty_KillingFailed",
        "value": 37002004,
    }),
    "Bounty_OrderAccept": _tools.RODict({
        "ID": "Bounty_OrderAccept",
        "value": 37002005,
    }),
    "Bounty_KillingAccept": _tools.RODict({
        "ID": "Bounty_KillingAccept",
        "value": 37002006,
    }),
    "Bounty_OrderDue": _tools.RODict({
        "ID": "Bounty_OrderDue",
        "value": 37002007,
    }),
    "Bounty_DepositRefund": _tools.RODict({
        "ID": "Bounty_DepositRefund",
        "value": 37002008,
    }),
    "Bounty_DepositReturn": _tools.RODict({
        "ID": "Bounty_DepositReturn",
        "value": 37002009,
    }),
    "Bounty_AllMoneyGet": _tools.RODict({
        "ID": "Bounty_AllMoneyGet",
        "value": 37002011,
    }),
    "Bounty_MoneyGet": _tools.RODict({
        "ID": "Bounty_MoneyGet",
        "value": 37002012,
    }),
    "Bounty_RefuseOrder": _tools.RODict({
        "ID": "Bounty_RefuseOrder",
        "value": 37002013,
    }),
    "Bounty_CantOrderSelf": _tools.RODict({
        "ID": "Bounty_CantOrderSelf",
        "value": 54002225,
    }),
    "Bounty_CantBeSelfKiller": _tools.RODict({
        "ID": "Bounty_CantBeSelfKiller",
        "value": 54002226,
    }),
    "Bounty_CantDoOrderSelf": _tools.RODict({
        "ID": "Bounty_CantDoOrderSelf",
        "value": 54002227,
    }),
    "Bounty_CantOrderSelfOrder": _tools.RODict({
        "ID": "Bounty_CantOrderSelfOrder",
        "value": 54002228,
    }),
    "Bounty_NoMoney": _tools.RODict({
        "ID": "Bounty_NoMoney",
        "value": 54002229,
    }),
    "Bounty_KillerBuff": _tools.RODict({
        "ID": "Bounty_KillerBuff",
        "value": 64008001,
    }),
    "Bounty_LoserDebuff": _tools.RODict({
        "ID": "Bounty_LoserDebuff",
        "value": 64008002,
    }),
    "Bounty_DesignatedKiller": _tools.RODict({
        "ID": "Bounty_DesignatedKiller",
        "value": 54002205,
    }),
    "Bounty_KillerAgree": _tools.RODict({
        "ID": "Bounty_KillerAgree",
        "value": 54002206,
    }),
    "Bounty_KillerAccept": _tools.RODict({
        "ID": "Bounty_KillerAccept",
        "value": 54002200,
    }),
    "Bounty_Countdown": _tools.RODict({
        "ID": "Bounty_Countdown",
        "value": 60,
    }),
    "Bounty_OutOrder": _tools.RODict({
        "ID": "Bounty_OutOrder",
        "value": 60,
    }),
    "autoPathStop": _tools.RODict({
        "ID": "autoPathStop",
        "value": 54001520,
    }),
    "autoGatherStop": _tools.RODict({
        "ID": "autoGatherStop",
        "value": 54001521,
    }),
    "autoFightStop": _tools.RODict({
        "ID": "autoFightStop",
        "value": 54001522,
    }),
    "autoQuestStop": _tools.RODict({
        "ID": "autoQuestStop",
        "value": 54001523,
    }),
    "showMousePopup": _tools.RODict({
        "ID": "showMousePopup",
        "value": (1, 8, 14, 19, 33, 34, 53),
    }),
    "triggerAutoCounter": _tools.RODict({
        "ID": "triggerAutoCounter",
        "value": (3116, 3121, 3216, 3221, 3316, 3321, 3421, 3521),
    }),
    "flyEpMax": _tools.RODict({
        "ID": "flyEpMax",
        "value": 4,
    }),
    "flyEpCostRate": _tools.RODict({
        "ID": "flyEpCostRate",
        "value": 1,
    }),
    "flyEpRate": _tools.RODict({
        "ID": "flyEpRate",
        "value": 8.0,
    }),
    "ControlflyCheating": _tools.RODict({
        "ID": "ControlflyCheating",
        "value": -5,
    }),
    "speedCheckTimeUnit": _tools.RODict({
        "ID": "speedCheckTimeUnit",
        "value": 1,
    }),
    "speedCheckSpeedillegallyOverRate": _tools.RODict({
        "ID": "speedCheckSpeedillegallyOverRate",
        "value": 30.0,
    }),
    "speedCheckFrameillegallyOverCount": _tools.RODict({
        "ID": "speedCheckFrameillegallyOverCount",
        "value": 3,
    }),
    "speedCheckWindowSize": _tools.RODict({
        "ID": "speedCheckWindowSize",
        "value": (2, 5),
    }),
    "speedCheckContinuousUnit": _tools.RODict({
        "ID": "speedCheckContinuousUnit",
        "value": 30,
    }),
    "lowHPAutoCounter": _tools.RODict({
        "ID": "lowHPAutoCounter",
        "value": 20,
    }),
    "defaultInitialRatioHP": _tools.RODict({
        "ID": "defaultInitialRatioHP",
        "value": 80,
    }),
    "defaultInitialRatioMP": _tools.RODict({
        "ID": "defaultInitialRatioMP",
        "value": 80,
    }),
    "blazeMaxSpeed": _tools.RODict({
        "ID": "blazeMaxSpeed",
        "value": 35,
    }),
    "navAgentWidth": _tools.RODict({
        "ID": "navAgentWidth",
        "value": 0.5,
    }),
    "ChangeTitleCD": _tools.RODict({
        "ID": "ChangeTitleCD",
        "value": 2,
    }),
    "maxSkillMove": _tools.RODict({
        "ID": "maxSkillMove",
        "value": 10,
    }),
    "MonsterDamageReductionBuff": _tools.RODict({
        "ID": "MonsterDamageReductionBuff",
        "value": 64004098,
    }),
    "characterSurroundArea": _tools.RODict({
        "ID": "characterSurroundArea",
        "value": 5.0,
    }),
    "cameraDirectionArea": _tools.RODict({
        "ID": "cameraDirectionArea",
        "value": 55.0,
    }),
    "dropThrowRange": _tools.RODict({
        "ID": "dropThrowRange",
        "value": (1, 2.5),
    }),
    "dropLocationRange": _tools.RODict({
        "ID": "dropLocationRange",
        "value": (0.8, 2.9),
    }),
    "dropGravityAcc": _tools.RODict({
        "ID": "dropGravityAcc",
        "value": 16.0,
    }),
    "dropBounceCount": _tools.RODict({
        "ID": "dropBounceCount",
        "value": 3,
    }),
    "dropEnergyDecreaseRatio": _tools.RODict({
        "ID": "dropEnergyDecreaseRatio",
        "value": 0.2,
    }),
    "dropInterval": _tools.RODict({
        "ID": "dropInterval",
        "value": (0.03, 0.5),
    }),
    "highFrameNotice": _tools.RODict({
        "ID": "highFrameNotice",
        "value": 54001339,
    }),
    "settlementPopup": _tools.RODict({
        "ID": "settlementPopup",
        "value": 60.0,
    }),
    "earlyAccess": _tools.RODict({
        "ID": "earlyAccess",
        "value": 54000269,
    }),
    "targetSurroundArea": _tools.RODict({
        "ID": "targetSurroundArea",
        "value": 20,
    }),
    "autoRefreshTxt": _tools.RODict({
        "ID": "autoRefreshTxt",
        "value": "自动刷新({0}s)",
    }),
    "autoRefreshTxt2": _tools.RODict({
        "ID": "autoRefreshTxt2",
        "value": "自动刷新",
    }),
    "filterCreepType1": _tools.RODict({
        "ID": "filterCreepType1",
        "value": (1, 8),
    }),
    "filterCreepType2": _tools.RODict({
        "ID": "filterCreepType2",
        "value": (2, 9),
    }),
    "userhelperUrl": _tools.RODict({
        "ID": "userhelperUrl",
        "value": "http://192.168.10.148:3001/#/help",
    }),
    "openUserServiceError": _tools.RODict({
        "ID": "openUserServiceError",
        "value": 54482014,
    }),
    "userServiceIsLogin": _tools.RODict({
        "ID": "userServiceIsLogin",
        "value": 54482021,
    }),
    "bagFullGeneralMessage": _tools.RODict({
        "ID": "bagFullGeneralMessage",
        "value": 54000663,
    })
})