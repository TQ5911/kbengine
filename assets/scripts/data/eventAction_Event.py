# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: eventAction/Event
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "Cnttask": _tools.RODict({
        "ID": "Cnttask",
        "EventID": 10000,
        "sendType": 0,
        "npcId": None
    }),
    "Openinterface": _tools.RODict({
        "ID": "Openinterface",
        "EventID": 10001,
        "sendType": 0,
        "npcId": None
    }),
    "sendMsg": _tools.RODict({
        "ID": "sendMsg",
        "EventID": 10002,
        "sendType": 0,
        "npcId": None
    }),
    "ForceSelectTarget": _tools.RODict({
        "ID": "ForceSelectTarget",
        "EventID": 10003,
        "sendType": 0,
        "npcId": None
    }),
    "SubmitItem": _tools.RODict({
        "ID": "SubmitItem",
        "EventID": 10004,
        "sendType": 0,
        "npcId": None
    }),
    "OpenStore": _tools.RODict({
        "ID": "OpenStore",
        "EventID": 10005,
        "sendType": 0,
        "npcId": None
    }),
    "findNearestEntityByTempleteId": _tools.RODict({
        "ID": "findNearestEntityByTempleteId",
        "EventID": 10006,
        "sendType": 0,
        "npcId": None
    }),
    "equipIdentify": _tools.RODict({
        "ID": "equipIdentify",
        "EventID": 10007,
        "sendType": 0,
        "npcId": None
    }),
    "OpenWarehouse": _tools.RODict({
        "ID": "OpenWarehouse",
        "EventID": 10008,
        "sendType": 0,
        "npcId": None
    }),
    "OpenGuild": _tools.RODict({
        "ID": "OpenGuild",
        "EventID": 10009,
        "sendType": 0,
        "npcId": None
    }),
    "sendGuide": _tools.RODict({
        "ID": "sendGuide",
        "EventID": 10010,
        "sendType": 0,
        "npcId": None
    }),
    "setCameraAtPosition": _tools.RODict({
        "ID": "setCameraAtPosition",
        "EventID": 10011,
        "sendType": 0,
        "npcId": None
    }),
    "findNearestEntityByTempleteIds": _tools.RODict({
        "ID": "findNearestEntityByTempleteIds",
        "EventID": 10012,
        "sendType": 0,
        "npcId": None
    }),
    "OpenPopInfoPanel": _tools.RODict({
        "ID": "OpenPopInfoPanel",
        "EventID": 10013,
        "sendType": 0,
        "npcId": None
    }),
    "OneOffClientNpc": _tools.RODict({
        "ID": "OneOffClientNpc",
        "EventID": 10014,
        "sendType": 0,
        "npcId": None
    }),
    "findNearestEntity": _tools.RODict({
        "ID": "findNearestEntity",
        "EventID": 10015,
        "sendType": 0,
        "npcId": None
    }),
    "cityBattleSignUp": _tools.RODict({
        "ID": "cityBattleSignUp",
        "EventID": 10016,
        "sendType": 0,
        "npcId": None
    }),
    "cityBattleBidding": _tools.RODict({
        "ID": "cityBattleBidding",
        "EventID": 10017,
        "sendType": 0,
        "npcId": None
    }),
    "cityBattleDeclare": _tools.RODict({
        "ID": "cityBattleDeclare",
        "EventID": 10018,
        "sendType": 0,
        "npcId": None
    }),
    "cityBattleEnter": _tools.RODict({
        "ID": "cityBattleEnter",
        "EventID": 10019,
        "sendType": 0,
        "npcId": None
    }),
    "cityBattleData": _tools.RODict({
        "ID": "cityBattleData",
        "EventID": 10020,
        "sendType": 0,
        "npcId": None
    }),
    "showAnimaGetEffect": _tools.RODict({
        "ID": "showAnimaGetEffect",
        "EventID": 10021,
        "sendType": 0,
        "npcId": None
    }),
    "shakeCamera": _tools.RODict({
        "ID": "shakeCamera",
        "EventID": 10023,
        "sendType": 0,
        "npcId": None
    }),
    "shakeCameraEnd": _tools.RODict({
        "ID": "shakeCameraEnd",
        "EventID": 10024,
        "sendType": 0,
        "npcId": None
    }),
    "HealingWounds": _tools.RODict({
        "ID": "HealingWounds",
        "EventID": 10025,
        "sendType": 0,
        "npcId": None
    }),
    "viewPointMovie": _tools.RODict({
        "ID": "viewPointMovie",
        "EventID": 10026,
        "sendType": 0,
        "npcId": None
    }),
    "Gettask": _tools.RODict({
        "ID": "Gettask",
        "EventID": 20000,
        "sendType": 2,
        "npcId": None
    }),
    "Fnstask": _tools.RODict({
        "ID": "Fnstask",
        "EventID": 20001,
        "sendType": 0,
        "npcId": None
    }),
    "Fnstalk": _tools.RODict({
        "ID": "Fnstalk",
        "EventID": 20002,
        "sendType": 0,
        "npcId": None
    }),
    "Failtask": _tools.RODict({
        "ID": "Failtask",
        "EventID": 20004,
        "sendType": 0,
        "npcId": None
    }),
    "setClue": _tools.RODict({
        "ID": "setClue",
        "EventID": 20005,
        "sendType": 0,
        "npcId": None
    }),
    "addEquipWashAnima": _tools.RODict({
        "ID": "addEquipWashAnima",
        "EventID": 20006,
        "sendType": 1,
        "npcId": None
    }),
    "taskRepeat": _tools.RODict({
        "ID": "taskRepeat",
        "EventID": 20018,
        "sendType": 1,
        "npcId": None
    }),
    "removeItem": _tools.RODict({
        "ID": "removeItem",
        "EventID": 20029,
        "sendType": 0,
        "npcId": None
    }),
    "explainGuide": _tools.RODict({
        "ID": "explainGuide",
        "EventID": 20030,
        "sendType": 0,
        "npcId": None
    }),
    "startGuideMove": _tools.RODict({
        "ID": "startGuideMove",
        "EventID": 20031,
        "sendType": 0,
        "npcId": None
    }),
    "startGuide": _tools.RODict({
        "ID": "startGuide",
        "EventID": 20032,
        "sendType": 0,
        "npcId": None
    }),
    "setVariableNoCharProp": _tools.RODict({
        "ID": "setVariableNoCharProp",
        "EventID": 20034,
        "sendType": 0,
        "npcId": None
    }),
    "completeRealName": _tools.RODict({
        "ID": "completeRealName",
        "EventID": 20054,
        "sendType": 0,
        "npcId": None
    }),
    "changeAppearance": _tools.RODict({
        "ID": "changeAppearance",
        "EventID": 20056,
        "sendType": 0,
        "npcId": None
    }),
    "enterSence": _tools.RODict({
        "ID": "enterSence",
        "EventID": 20057,
        "sendType": 0,
        "npcId": 18000515
    }),
    "AddSkillUltimatePoint": _tools.RODict({
        "ID": "AddSkillUltimatePoint",
        "EventID": 20058,
        "sendType": 1,
        "npcId": None
    })
})