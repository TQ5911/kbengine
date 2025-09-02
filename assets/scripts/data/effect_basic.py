# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: effect/basic
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    13010001: _tools.RODict({
        "ID": 13010001,
        "Func": "addFightParam",
        "ParameterType": "Hash{{key=\"Prop\",value=\"FIGHTPROP\"},{key=\"Value\",value=\"Float()\"}}",
        "Example": "[{\"EffectId\": 13010001, \"Prop\": \"MulCD\", \"Value\": -0.5}]"
    }),
    13010003: _tools.RODict({
        "ID": 13010003,
        "Func": "setStatus",
        "ParameterType": "Hash{{key=\"Status\",value=\"STATUSNAME\"}}",
        "Example": "[{\"EffectId\": 13010003, \"Status\": 4}]*状态ID参见右侧"
    }),
    13010004: _tools.RODict({
        "ID": 13010004,
        "Func": "setUnControl",
        "ParameterType": "",
        "Example": "[{\"EffectId\": 13010004}],免控"
    }),
    13010005: _tools.RODict({
        "ID": 13010005,
        "Func": "setSkillUnBroken",
        "ParameterType": "",
        "Example": "[{\"EffectId\": 13010005}],技能不可被打断"
    }),
    13010006: _tools.RODict({
        "ID": 13010006,
        "Func": "addShield",
        "ParameterType": "Hash{{key=\"type\",value=\"Int()\"},{key=\"Value\",value=\"Float()\"}}",
        "Example": "[{\"EffectId\": 13010006, \"type\": 1, \"Value\": 300}],表示传入数值\n[{\"EffectId\": 13010006, \"type\": 2, \"Value\": 0.5}],表示传入百分比"
    }),
    13010007: _tools.RODict({
        "ID": 13010007,
        "Func": "bloodDrain",
        "ParameterType": "Hash{key=\"Value\", value=\"Float()\"}",
        "Example": "[{\"EffectId\": 13010007, \"Value\": 0.1}]全局百分比吸血"
    }),
    13010008: _tools.RODict({
        "ID": 13010008,
        "Func": "addSkillCd",
        "ParameterType": "Hash{{key=\"SkillID\",value=\"Int()\"},{key=\"Value\",value=\"Float()\"},{key=\"IsMul\",value=\"Bool()\"}}",
        "Example": "[{\"EffectId\": 13010008, \"skillId\": [12345678, 23456789], \"Value\": [0.2, 0.5], \"IsMul\":[True]}]\nisMul支持不填写，不填认为加减法，每条配置仅支持一种模式"
    }),
    13010009: _tools.RODict({
        "ID": 13010009,
        "Func": "addMagicFind",
        "ParameterType": "Hash{{key=\"Status\",value=\"Float()\"}}",
        "Example": "[{\"EffectId\": 13010009, \"AddMagicFindVal\": 4}]"
    })
})
minKey = 13010001
maxKey = 13010009