# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: taskClass/taskMsg
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "taskClaimAlert_Success": _tools.RODict({
        "ID": "taskClaimAlert_Success",
        "value": 54000194,
        "type": "uint"
    }),
    "taskClaimAlert_OtherFail": _tools.RODict({
        "ID": "taskClaimAlert_OtherFail",
        "value": 54000153,
        "type": "uint"
    }),
    "taskClaimAlert_GuildCheck": _tools.RODict({
        "ID": "taskClaimAlert_GuildCheck",
        "value": 54000746,
        "type": "uint"
    }),
    "taskClaimAlert_ItemCheck": _tools.RODict({
        "ID": "taskClaimAlert_ItemCheck",
        "value": 54000203,
        "type": "uint"
    }),
    "taskClaimAlert_LevelCheck": _tools.RODict({
        "ID": "taskClaimAlert_LevelCheck",
        "value": 54000202,
        "type": "uint"
    }),
    "taskClaimAlert_TimesCheck": _tools.RODict({
        "ID": "taskClaimAlert_TimesCheck",
        "value": 54001042,
        "type": "uint"
    }),
    "taskClaimAlert_GangCheck": _tools.RODict({
        "ID": "taskClaimAlert_GangCheck",
        "value": 54001335,
        "type": "uint"
    }),
    "taskClaimAlert_Team_OtherFail": _tools.RODict({
        "ID": "taskClaimAlert_Team_OtherFail",
        "value": 54001043,
        "type": "uint"
    }),
    "taskClaimAlert_Team_LeaderCheck": _tools.RODict({
        "ID": "taskClaimAlert_Team_LeaderCheck",
        "value": 54000181,
        "type": "uint"
    }),
    "taskClaimAlert_Team_PalNumCheck": _tools.RODict({
        "ID": "taskClaimAlert_Team_PalNumCheck",
        "value": 54000185,
        "type": "uint"
    }),
    "taskClaimAlert_Team_FollowCheck": _tools.RODict({
        "ID": "taskClaimAlert_Team_FollowCheck",
        "value": 54000182,
        "type": "uint"
    }),
    "taskClaimAlert_Team_NearbyCheck": _tools.RODict({
        "ID": "taskClaimAlert_Team_NearbyCheck",
        "value": 54000183,
        "type": "uint"
    }),
    "taskClaimAlert_Team_LevelCheck": _tools.RODict({
        "ID": "taskClaimAlert_Team_LevelCheck",
        "value": 54001191,
        "type": "uint"
    }),
    "taskClaimAlert_Team_ItemCheck": _tools.RODict({
        "ID": "taskClaimAlert_Team_ItemCheck",
        "value": 54000186,
        "type": "uint"
    }),
    "taskClaimAlert_CinemaPlay": _tools.RODict({
        "ID": "taskClaimAlert_CinemaPlay",
        "value": 54000635,
        "type": "uint"
    }),
    "taskClaimAlert_EnterDun": _tools.RODict({
        "ID": "taskClaimAlert_EnterDun",
        "value": 54000205,
        "type": "uint"
    }),
    "taskClaimAlert_GetItem": _tools.RODict({
        "ID": "taskClaimAlert_GetItem",
        "value": 54000204,
        "type": "uint"
    }),
    "taskClickAlert_Fail": _tools.RODict({
        "ID": "taskClickAlert_Fail",
        "value": 54000212,
        "type": "uint"
    }),
    "taskTargetAlert_SearchArea01": _tools.RODict({
        "ID": "taskTargetAlert_SearchArea01",
        "value": 54000395,
        "type": "uint"
    }),
    "taskTargetAlert_SearchArea02": _tools.RODict({
        "ID": "taskTargetAlert_SearchArea02",
        "value": 54000396,
        "type": "uint"
    }),
    "taskTargetAlert_SearchArea03": _tools.RODict({
        "ID": "taskTargetAlert_SearchArea03",
        "value": 54000397,
        "type": "uint"
    }),
    "taskSubmitAlert_Success": _tools.RODict({
        "ID": "taskSubmitAlert_Success",
        "value": 54000195,
        "type": "uint"
    }),
    "taskSubmitAlert_EnterDun": _tools.RODict({
        "ID": "taskSubmitAlert_EnterDun",
        "value": 54000206,
        "type": "uint"
    }),
    "taskSubmitAlert_CinemaPlay": _tools.RODict({
        "ID": "taskSubmitAlert_CinemaPlay",
        "value": 54000636,
        "type": "uint"
    }),
    "taskSubmitAlert_BagCheck": _tools.RODict({
        "ID": "taskSubmitAlert_BagCheck",
        "value": 54001248,
        "type": "uint"
    }),
    "taskSubmitAlert_TaskCheck": _tools.RODict({
        "ID": "taskSubmitAlert_TaskCheck",
        "value": 54001325,
        "type": "uint"
    }),
    "taskSubmitAlert_TimesCheck": _tools.RODict({
        "ID": "taskSubmitAlert_TimesCheck",
        "value": 54001326,
        "type": "uint"
    }),
    "taskSubmitAlert_Team_LeaderCheck": _tools.RODict({
        "ID": "taskSubmitAlert_Team_LeaderCheck",
        "value": 54000184,
        "type": "uint"
    }),
    "taskFailAlert_Success": _tools.RODict({
        "ID": "taskFailAlert_Success",
        "value": 54001327,
        "type": "uint"
    }),
    "taskFailAlert_Death": _tools.RODict({
        "ID": "taskFailAlert_Death",
        "value": 54000209,
        "type": "uint"
    }),
    "taskFailAlert_LeaveDun": _tools.RODict({
        "ID": "taskFailAlert_LeaveDun",
        "value": 54000211,
        "type": "uint"
    }),
    "taskFailAlert_TimeOut": _tools.RODict({
        "ID": "taskFailAlert_TimeOut",
        "value": 54000210,
        "type": "uint"
    }),
    "taskFailAlert_LeaveArea_pre": _tools.RODict({
        "ID": "taskFailAlert_LeaveArea_pre",
        "value": 54000207,
        "type": "uint"
    }),
    "taskFailAlert_LeaveArea": _tools.RODict({
        "ID": "taskFailAlert_LeaveArea",
        "value": 54000208,
        "type": "uint"
    }),
    "taskFailAlert_OutOfActivity": _tools.RODict({
        "ID": "taskFailAlert_OutOfActivity",
        "value": 54001324,
        "type": "uint"
    }),
    "taskAbanAlert_Success": _tools.RODict({
        "ID": "taskAbanAlert_Success",
        "value": 54000231,
        "type": "uint"
    }),
    "taskAbanAlert_Success_pre": _tools.RODict({
        "ID": "taskAbanAlert_Success_pre",
        "value": 54000230,
        "type": "uint"
    }),
    "taskAbanAlert_Fail_NotLeader": _tools.RODict({
        "ID": "taskAbanAlert_Fail_NotLeader",
        "value": 54001547,
        "type": "uint"
    }),
    "taskSubmitItemAlert_NoMoney": _tools.RODict({
        "ID": "taskSubmitItemAlert_NoMoney",
        "value": 54000256,
        "type": "uint"
    }),
    "taskNotInThisScene": _tools.RODict({
        "ID": "taskNotInThisScene",
        "value": 54990219,
        "type": "uint"
    }),
    "taskPercentage": _tools.RODict({
        "ID": "taskPercentage",
        "value": 54001982,
        "type": "uint"
    }),
    "taskComplete": _tools.RODict({
        "ID": "taskComplete",
        "value": 54001983,
        "type": "uint"
    })
})