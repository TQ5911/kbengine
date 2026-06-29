# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: taskEditorConfig/taskEditorInfo
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "TaskId": _tools.RODict({
        "value": 0
    }),
    "TaskType": _tools.RODict({
        "value": 0
    }),
    "TaskName": _tools.RODict({
        "value": ''
    }),
    "TaskGroup": _tools.RODict({
        "value": 0
    }),
    "IsAutoTask": _tools.RODict({
        "value": False
    }),
    "IsAutoQuit": _tools.RODict({
        "value": False
    }),
    "FatherTaskId": _tools.RODict({
        "value": 0
    }),
    "ChildTaskIds": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "TaskDesc": _tools.RODict({
        "value": ''
    }),
    "TaskDetailDesc": _tools.RODict({
        "value": ''
    }),
    "ClaimNpcId": _tools.RODict({
        "value": ''
    }),
    "ClaimNpcMapId": _tools.RODict({
        "value": 1
    }),
    "CNUnFinDiallogId": _tools.RODict({
        "value": ''
    }),
    "CNFinDialogId": _tools.RODict({
        "value": ''
    }),
    "FinNpcId": _tools.RODict({
        "value": ''
    }),
    "FinNpcMapId": _tools.RODict({
        "value": 1
    }),
    "FNUnFinDiallogId": _tools.RODict({
        "value": ''
    }),
    "FNFinDialogId": _tools.RODict({
        "value": ''
    }),
    "ChildDoInQueue": _tools.RODict({
        "value": True
    }),
    "ChildDoInRandom": _tools.RODict({
        "value": False
    }),
    "ChildDoInSelection": _tools.RODict({
        "value": False
    }),
    "FatherFailIfChildFail": _tools.RODict({
        "value": True
    }),
    "FaterSuccIfChildSucc": _tools.RODict({
        "value": False
    }),
    "DispHiddenTask": _tools.RODict({
        "value": False
    }),
    "DispInClaimList": _tools.RODict({
        "value": True
    }),
    "DispInOpenList": _tools.RODict({
        "value": True
    }),
    "DispLevel": _tools.RODict({
        "value": 0
    }),
    "DispNotInTaskPanel": _tools.RODict({
        "value": False
    }),
    "DispNotInTaskBar": _tools.RODict({
        "value": False
    }),
    "OpenCondIsTriggerArea": _tools.RODict({
        "value": False
    }),
    "OpenCondTriggerArea": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "OpenCondCheckTaskCount": _tools.RODict({
        "value": False
    }),
    "OpenCondCountCycle": _tools.RODict({
        "value": -1
    }),
    "OpenCondCountLimit": _tools.RODict({
        "value": 0
    }),
    "OpenCondTaskeState": _tools.RODict({
        "value": 0
    }),
    "OpenCondIsFailNoCount": _tools.RODict({
        "value": False
    }),
    "OpenCondIsAbanNoCount": _tools.RODict({
        "value": False
    }),
    "OpenCondCheckSex": _tools.RODict({
        "value": 0
    }),
    "OpenCondCheckRace": _tools.RODict({
        "value": ''
    }),
    "OpenCondCheckProfres": _tools.RODict({
        "value": ''
    }),
    "OpenCondCheckGuildLv": _tools.RODict({
        "value": 0
    }),
    "OpenCondRelateTaskId": _tools.RODict({
        "value": ''
    }),
    "OpenCondRelateActId": _tools.RODict({
        "value": 0
    }),
    "OpenCondRelateTaskState": _tools.RODict({
        "value": 3
    }),
    "OpenCondCheckFavor": _tools.RODict({
        "value": False
    }),
    "OpenCondFavorNpc": _tools.RODict({
        "value": 0
    }),
    "OpenCondFavorLevel": _tools.RODict({
        "value": 0
    }),
    "OpenCondRepeatIfSucess": _tools.RODict({
        "value": False
    }),
    "OpenCondRepeatIfFail": _tools.RODict({
        "value": True
    }),
    "ClaimCondAutoTake": _tools.RODict({
        "value": False
    }),
    "ClaimCondLevelMin": _tools.RODict({
        "value": 0
    }),
    "ClaimCondLevelMax": _tools.RODict({
        "value": 0
    }),
    "ClaimCondNeedCheckTeam": _tools.RODict({
        "value": False
    }),
    "ClaimCondCheckTeam": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "ClaimCondCheckItem": _tools.RODict({
        "value": False
    }),
    "ClaimCondCheckItemInfo": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "ClaimCondCheckGuildSceneId": _tools.RODict({
        "value": False
    }),
    "ClaimCondVarCheckFormID": _tools.RODict({
        "value": 0
    }),
    "ClaimCondVarCheckParam": _tools.RODict({
        "value": ''
    }),
    "ClaimNeedSetClue": _tools.RODict({
        "value": False
    }),
    "ClaimClueID": _tools.RODict({
        "value": 0
    }),
    "ClaimClueState": _tools.RODict({
        "value": 0
    }),
    "ClaimCanRewardITems": _tools.RODict({
        "value": False
    }),
    "ClaimRewardItems": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "ClaimRandomItems": _tools.RODict({
        "value": False
    }),
    "ClaimCanTransIns": _tools.RODict({
        "value": False
    }),
    "ClaimTransInstance": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "ClaimDialog": _tools.RODict({
        "value": 0
    }),
    "ClaimEventName": _tools.RODict({
        "value": ''
    }),
    "ClaimEventParam": _tools.RODict({
        "value": ''
    }),
    "ClaimTriggerStoryID": _tools.RODict({
        "value": 0
    }),
    "FailCondTimeLimit": _tools.RODict({
        "value": 0
    }),
    "FailCondTimingOffline": _tools.RODict({
        "value": False
    }),
    "FailCondIsEnterArea": _tools.RODict({
        "value": False
    }),
    "FailCondEnterArea": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "FailCondIsLeaveArea": _tools.RODict({
        "value": False
    }),
    "FailCondLeaveArea": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "FailCondIfDie": _tools.RODict({
        "value": False
    }),
    "FailCondCanGiveUp": _tools.RODict({
        "value": False
    }),
    "FailCondCanQuitIfFail": _tools.RODict({
        "value": True
    }),
    "FailCondQuitIfFail": _tools.RODict({
        "value": False
    }),
    "FailCondFailIfQtInst": _tools.RODict({
        "value": False
    }),
    "FailCondInstType": _tools.RODict({
        "value": 0
    }),
    "FailCondInstId": _tools.RODict({
        "value": 0
    }),
    "FailCondActId": _tools.RODict({
        "value": 0
    }),
    "FinCondNoLimit": _tools.RODict({
        "value": False
    }),
    "FinCondHasKillMon": _tools.RODict({
        "value": False
    }),
    "FinCondKillMonster": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "FinCondHasGatherItems": _tools.RODict({
        "value": False
    }),
    "FinCondGatherItems": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "FinCondHasFinDia": _tools.RODict({
        "value": False
    }),
    "FinCondFinDialogs": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "FinCondHasInterCollect": _tools.RODict({
        "value": False
    }),
    "FinCondInterCollect": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "FinCondIsTriggerArea": _tools.RODict({
        "value": False
    }),
    "FinCondReachArea": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "FinCondIsTriggerAction": _tools.RODict({
        "value": False
    }),
    "FinCondTriggerAction": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "FinCondFinIntance": _tools.RODict({
        "value": False
    }),
    "FinCondToLevel": _tools.RODict({
        "value": 0
    }),
    "FinCondNeedActiveCard": _tools.RODict({
        "value": False
    }),
    "FinCondMonCardId": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "FinCondNeedCheckValue": _tools.RODict({
        "value": False
    }),
    "FinCondNeedOneValue": _tools.RODict({
        "value": False
    }),
    "FinCondCheckValue": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "FinCondRelateTaskId": _tools.RODict({
        "value": ''
    }),
    "FinCondRelateTaskState": _tools.RODict({
        "value": 3
    }),
    "FinCondNeedMergeTarget": _tools.RODict({
        "value": False
    }),
    "FinCondDefaultText": _tools.RODict({
        "value": ''
    }),
    "FinCondDefaultTempleteId": _tools.RODict({
        "value": 0
    }),
    "DeliMetdNoLimit": _tools.RODict({
        "value": False
    }),
    "DeliMetdFinDialogs": _tools.RODict({
        "value": False
    }),
    "DeliMetdManual": _tools.RODict({
        "value": False
    }),
    "DeliMetDefaultText": _tools.RODict({
        "value": ''
    }),
    "FinRewardID": _tools.RODict({
        "value": 0
    }),
    "FinRewardTaskID": _tools.RODict({
        "value": ''
    }),
    "FinNeedSetClue": _tools.RODict({
        "value": False
    }),
    "FinBlockPopReward": _tools.RODict({
        "value": False
    }),
    "FinClueID": _tools.RODict({
        "value": 0
    }),
    "FinClueState": _tools.RODict({
        "value": 0
    }),
    "FinHasRewardInst": _tools.RODict({
        "value": False
    }),
    "FinRewardInstance": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "FinRewardLeaveInstance": _tools.RODict({
        "value": False
    }),
    "FinRewardLevInsID": _tools.RODict({
        "value": 0
    }),
    "FinRewardLevInsDelay": _tools.RODict({
        "value": 0
    }),
    "FinRewardCountLimit": _tools.RODict({
        "value": 0
    }),
    "FinRewardDialog": _tools.RODict({
        "value": 0
    }),
    "FinRewardEventName": _tools.RODict({
        "value": ''
    }),
    "FinRewardEventParam": _tools.RODict({
        "value": ''
    }),
    "FinRewardTriggerStoryID": _tools.RODict({
        "value": 0
    }),
    "AbanRewardID": _tools.RODict({
        "value": 0
    }),
    "AbanRewardTaskID": _tools.RODict({
        "value": ''
    }),
    "AbanHasRewardInst": _tools.RODict({
        "value": False
    }),
    "AbanRewardInstance": _tools.RODict({
        "value": _tools.RODict({})
    }),
    "AbanRewardDialog": _tools.RODict({
        "value": 0
    }),
    "AbanRewardEventName": _tools.RODict({
        "value": ''
    }),
    "AbanRewardEventParam": _tools.RODict({
        "value": ''
    }),
    "AbanRewardLeaveInstance": _tools.RODict({
        "value": False
    }),
    "AbanRewardLevInsID": _tools.RODict({
        "value": 0
    }),
    "AbanRewardLevInsDelay": _tools.RODict({
        "value": 0
    }),
    "CheckFollowNPC": _tools.RODict({
        "value": False
    }),
    "TaskFollowNPC": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "NoNeedPathFinding": _tools.RODict({
        "value": False
    }),
    "ClickTaskToMapID": _tools.RODict({
        "value": 0
    }),
    "ClickTaskToPosX": _tools.RODict({
        "value": 0
    }),
    "ClickTaskToPosY": _tools.RODict({
        "value": 0
    }),
    "ClickTaskToPosZ": _tools.RODict({
        "value": 0
    }),
    "ClickTaskClientEvent": _tools.RODict({
        "value": ''
    }),
    "ClickTaskEventParam": _tools.RODict({
        "value": ''
    }),
    "FinCondTeamSyncCnt": _tools.RODict({
        "value": False
    }),
    "OpenCondTaskRound": _tools.RODict({
        "value": ''
    }),
    "FinRoundRewardID": _tools.RODict({
        "value": ''
    }),
    "FinRoundEventName": _tools.RODict({
        "value": ''
    }),
    "FinRoundEventParam": _tools.RODict({
        "value": ''
    }),
    "OpenCondVarCheckFormID": _tools.RODict({
        "value": 0
    }),
    "OpenCondVarCheckParam": _tools.RODict({
        "value": ''
    }),
    "FailCondVarCheckFormID": _tools.RODict({
        "value": 0
    }),
    "FailCondVarCheckParam": _tools.RODict({
        "value": ''
    }),
    "FinCondVarCheckFormID": _tools.RODict({
        "value": 0
    }),
    "FinCondVarCheckParam": _tools.RODict({
        "value": ''
    }),
    "FinRewardCanVarMod": _tools.RODict({
        "value": False
    }),
    "FinRewardVarModInfo": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "FinRewardTips": _tools.RODict({
        "value": 0
    }),
    "AbanRewardVarModInfo": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "OpenCondCheckHomeWhaleLv": _tools.RODict({
        "value": 0
    }),
    "AbanRewardCanVarMod": _tools.RODict({
        "value": False
    }),
    "ChildDoInSameTime": _tools.RODict({
        "value": False
    }),
    "ClaimCanVarMod": _tools.RODict({
        "value": False
    }),
    "SoundAban": _tools.RODict({
        "value": False
    }),
    "SoundClaim": _tools.RODict({
        "value": False
    }),
    "SoundFail": _tools.RODict({
        "value": False
    }),
    "SoundFin": _tools.RODict({
        "value": False
    }),
    "SoundSubmmit": _tools.RODict({
        "value": False
    }),
    "FinCondCountID": _tools.RODict({
        "value": 0
    }),
    "FinCondCountTgt": _tools.RODict({
        "value": 0
    }),
    "FinCondCountParam": _tools.RODict({
        "value": ''
    }),
    "ShowSpecialTaskEffect": _tools.RODict({
        "value": False
    }),
    "FinCondKillMonsterMode": _tools.RODict({
        "value": 0
    }),
    "FinCondKillMonsterNum": _tools.RODict({
        "value": 0
    }),
    "ClaimTaskNeedTips": _tools.RODict({
        "value": False
    }),
    "TaskCompletedNeedTips": _tools.RODict({
        "value": False
    }),
    "ChildDoInAccept": _tools.RODict({
        "value": False
    }),
    "GuaranteeTaskId": _tools.RODict({
        "value": 0
    }),
    "GuaranteeCount": _tools.RODict({
        "value": 0
    }),
    "RandomWithWeight": _tools.RODict({
        "value": False
    }),
    "ChildTaskWeights": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "ClamiCameraData": _tools.RODict({
        "value": 0
    }),
    "FinRewardCameraData": _tools.RODict({
        "value": 0
    }),
    "DispInTaskBar": _tools.RODict({
        "value": False
    }),
    "BelongMap": _tools.RODict({
        "value": 0
    }),
    "BelongChapter": _tools.RODict({
        "value": 0
    }),
    "AbanCanRemoveItems": _tools.RODict({
        "value": False
    }),
    "AbanRemoveItems": _tools.RODict({
        "value": _tools.ROList([])
    }),
    "UnlockCustomText": _tools.RODict({
        "value": ''
    })
})