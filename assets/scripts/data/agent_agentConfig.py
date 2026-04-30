# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: agent/agentConfig
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "approvalMsg": _tools.RODict({
        "ID": "approvalMsg",
        "value": 54000272,
    }),
    "reconfirmMsg": _tools.RODict({
        "ID": "reconfirmMsg",
        "value": 54000273,
    }),
    "revokeMsg": _tools.RODict({
        "ID": "revokeMsg",
        "value": 54000274,
    }),
    "authorizationDayLimit": _tools.RODict({
        "ID": "authorizationDayLimit",
        "value": 1,
    }),
    "authorizationDays": _tools.RODict({
        "ID": "authorizationDays",
        "value": 30,
    }),
    "dailyGoldLimit": _tools.RODict({
        "ID": "dailyGoldLimit",
        "value": 99999,
    }),
    "dailyGoldLimitMsg": _tools.RODict({
        "ID": "dailyGoldLimitMsg",
        "value": 54000280,
    }),
    "itemDisassemblyLimit": _tools.RODict({
        "ID": "itemDisassemblyLimit",
        "value": 3,
    }),
    "itemDisassemblyLimitMsg": _tools.RODict({
        "ID": "itemDisassemblyLimitMsg",
        "value": 54000285,
    }),
    "evilMeterLimit": _tools.RODict({
        "ID": "evilMeterLimit",
        "value": -1000,
    }),
    "evilMeterLimitMsg": _tools.RODict({
        "ID": "evilMeterLimitMsg",
        "value": 54000277,
    }),
    "evilMeterLow": _tools.RODict({
        "ID": "evilMeterLow",
        "value": -2000,
    }),
    "evilMeterLowMsg": _tools.RODict({
        "ID": "evilMeterLowMsg",
        "value": 54000278,
    }),
    "restrictedPromptMsg1": _tools.RODict({
        "ID": "restrictedPromptMsg1",
        "value": 54000275,
    }),
    "restrictedPromptMsg2": _tools.RODict({
        "ID": "restrictedPromptMsg2",
        "value": 54000276,
    }),
    "forceLogin": _tools.RODict({
        "ID": "forceLogin",
        "value": 54000279,
    }),
    "loadingTime": _tools.RODict({
        "ID": "loadingTime",
        "value": 30,
    }),
    "loggingIn": _tools.RODict({
        "ID": "loggingIn",
        "value": "<color=#038304>登录中</color>",
    }),
    "customSort": _tools.RODict({
        "ID": "customSort",
        "value": (30000001, 30000002, 30000013, 30000021),
    }),
    "agentVisible": _tools.RODict({
        "ID": "agentVisible",
        "value": "UIRoleAuthorizationPanel",
    }),
    "loginDailiMsg": _tools.RODict({
        "ID": "loginDailiMsg",
        "value": 54000281,
    }),
    "dailyGoldLimitShow": _tools.RODict({
        "ID": "dailyGoldLimitShow",
        "value": "<color=#c60c0c>{0}</color>/{1}",
    }),
    "copySettlement": _tools.RODict({
        "ID": "copySettlement",
        "value": (27, 9, 15, 25),
    }),
    "deleteRestrictions": _tools.RODict({
        "ID": "deleteRestrictions",
        "value": 54000282,
    }),
    "expirationNotice": _tools.RODict({
        "ID": "expirationNotice",
        "value": 54000283,
    }),
    "modifySuccess": _tools.RODict({
        "ID": "modifySuccess",
        "value": 54000284,
    }),
    "offlineDaili": _tools.RODict({
        "ID": "offlineDaili",
        "value": 54000286,
    }),
    "offlineNotice": _tools.RODict({
        "ID": "offlineNotice",
        "value": 54000287,
    }),
    "onlineNotice": _tools.RODict({
        "ID": "onlineNotice",
        "value": 54000288,
    }),
    "agentOffline": _tools.RODict({
        "ID": "agentOffline",
        "value": 54000289,
    }),
    "agentCancel": _tools.RODict({
        "ID": "agentCancel",
        "value": 54000290,
    }),
    "Disassembly": _tools.RODict({
        "ID": "Disassembly",
        "value": 20,
    }),
    "SellRoot": _tools.RODict({
        "ID": "SellRoot",
        "value": 21,
    }),
    "PullRoot": _tools.RODict({
        "ID": "PullRoot",
        "value": 22,
    }),
    "deFriended": _tools.RODict({
        "ID": "deFriended",
        "value": 23,
    }),
    "deMail": _tools.RODict({
        "ID": "deMail",
        "value": 24,
    })
})