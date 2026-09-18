# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: secondpwd/secondPwdConfig
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "pwdMinLength": _tools.RODict({
        "ID": "pwdMinLength",
        "value": 6,
    }),
    "pwdMaxLength": _tools.RODict({
        "ID": "pwdMaxLength",
        "value": 6,
    }),
    "passwordInputHint": _tools.RODict({
        "ID": "passwordInputHint",
        "value": 54000391,
    }),
    "passwordReInputHint": _tools.RODict({
        "ID": "passwordReInputHint",
        "value": 54000392,
    }),
    "pwdConsecutiveNum": _tools.RODict({
        "ID": "pwdConsecutiveNum",
        "value": 54000393,
    }),
    "setSecondPwdSuccess": _tools.RODict({
        "ID": "setSecondPwdSuccess",
        "value": 54000394,
    }),
    "goldCost": _tools.RODict({
        "ID": "goldCost",
        "value": 1,
    }),
    "goldCostLimit": _tools.RODict({
        "ID": "goldCostLimit",
        "value": (101, 2000),
    }),
    "boundGoldCost": _tools.RODict({
        "ID": "boundGoldCost",
        "value": 2,
    }),
    "boundGoldCostLimit": _tools.RODict({
        "ID": "boundGoldCostLimit",
        "value": (101, 2000),
    }),
    "Disassembly": _tools.RODict({
        "ID": "Disassembly",
        "value": 6,
    }),
    "itemDisassemblyLimit": _tools.RODict({
        "ID": "itemDisassemblyLimit",
        "value": 3,
    }),
    "sellRoot": _tools.RODict({
        "ID": "sellRoot",
        "value": 3,
    }),
    "rentalOnSale": _tools.RODict({
        "ID": "rentalOnSale",
        "value": 4,
    }),
    "equip_unbundle": _tools.RODict({
        "ID": "equip_unbundle",
        "value": 5,
    }),
    "modifySuccess": _tools.RODict({
        "ID": "modifySuccess",
        "value": 54000395,
    }),
    "continuousWrongMsg": _tools.RODict({
        "ID": "continuousWrongMsg",
        "value": 54000399,
    }),
    "continuousWrong": _tools.RODict({
        "ID": "continuousWrong",
        "value": _tools.ROList([(3, 30, 54000396), (4, 60, 54000397), (5, 1440, 54000398)]),
    }),
    "secondPwdVisible": _tools.RODict({
        "ID": "secondPwdVisible",
        "value": "secondPwd",
    }),
    "pwdFreeVerifyDurationMs": _tools.RODict({
        "ID": "pwdFreeVerifyDurationMs",
        "value": (300, 600, 900),
    }),
    "pwdVerifySuccess": _tools.RODict({
        "ID": "pwdVerifySuccess",
        "value": 54000400,
    }),
    "pwdVerifyTimeout": _tools.RODict({
        "ID": "pwdVerifyTimeout",
        "value": 54000401,
    }),
    "secondPwdSuccess": _tools.RODict({
        "ID": "secondPwdSuccess",
        "value": 54000402,
    }),
    "errPasswordEmpty": _tools.RODict({
        "ID": "errPasswordEmpty",
        "value": 54000403,
    }),
    "errPpasswordMismatch": _tools.RODict({
        "ID": "errPpasswordMismatch",
        "value": 54000404,
    }),
    "errPasswordLocked": _tools.RODict({
        "ID": "errPasswordLocked",
        "value": 54000405,
    }),
    "errPwdLockEndTime": _tools.RODict({
        "ID": "errPwdLockEndTime",
        "value": 54000406,
    }),
    "agent": _tools.RODict({
        "ID": "agent",
        "value": 7,
    }),
    "pwdNotBindPhone": _tools.RODict({
        "ID": "pwdNotBindPhone",
        "value": 54000407,
    })
})