# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: const/UIconst
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "TasktrackMax": _tools.RODict({
        "ID": "TasktrackMax",
        "value": "10",
        "Type": "int"
    }),
    "maxMessageBufferNum": _tools.RODict({
        "ID": "maxMessageBufferNum",
        "value": "50",
        "Type": "int"
    }),
    "maxMessageBufferTime": _tools.RODict({
        "ID": "maxMessageBufferTime",
        "value": "10",
        "Type": "float"
    }),
    "popDialogCloseTime": _tools.RODict({
        "ID": "popDialogCloseTime",
        "value": "5",
        "Type": "float"
    }),
    "cameraHawkEyeDepthMin": _tools.RODict({
        "ID": "cameraHawkEyeDepthMin",
        "value": "0.3",
        "Type": "float"
    }),
    "cameraHawkEyeDepthMax": _tools.RODict({
        "ID": "cameraHawkEyeDepthMax",
        "value": "200",
        "Type": "float"
    }),
    "cameraHawkEyeDepthPov": _tools.RODict({
        "ID": "cameraHawkEyeDepthPov",
        "value": "0.8",
        "Type": "float"
    }),
    "cameraHawkEyeMergeMax": _tools.RODict({
        "ID": "cameraHawkEyeMergeMax",
        "value": "100",
        "Type": "float"
    }),
    "cameraHawkEyeMergePov": _tools.RODict({
        "ID": "cameraHawkEyeMergePov",
        "value": "0.5",
        "Type": "float"
    }),
    "cameraHawkEyeBkgColor": _tools.RODict({
        "ID": "cameraHawkEyeBkgColor",
        "value": "FFFFFF",
        "Type": "string"
    }),
    "cameraHawkEyeShadowAdd": _tools.RODict({
        "ID": "cameraHawkEyeShadowAdd",
        "value": "0.9",
        "Type": "float"
    }),
    "cameraHawkEyeColorRatio": _tools.RODict({
        "ID": "cameraHawkEyeColorRatio",
        "value": "0",
        "Type": "float"
    }),
    "timeStopHawkEyeMergePov": _tools.RODict({
        "ID": "timeStopHawkEyeMergePov",
        "value": "0",
        "Type": "float"
    }),
    "timeStopNPCHawkEyeGrayRatio": _tools.RODict({
        "ID": "timeStopNPCHawkEyeGrayRatio",
        "value": "0.55",
        "Type": "float"
    }),
    "timeStopNPCHawkEyeColorRatio": _tools.RODict({
        "ID": "timeStopNPCHawkEyeColorRatio",
        "value": "0.2",
        "Type": "float"
    }),
    "timeStopNPCHawkEyeColorRGB": _tools.RODict({
        "ID": "timeStopNPCHawkEyeColorRGB",
        "value": "4159C8",
        "Type": "string"
    }),
    "timeStopNPCHawkEyeColorIntensity": _tools.RODict({
        "ID": "timeStopNPCHawkEyeColorIntensity",
        "value": "0.8",
        "Type": "float"
    }),
    "timeStopPlayerHawkEyeGrayRatio": _tools.RODict({
        "ID": "timeStopPlayerHawkEyeGrayRatio",
        "value": "0.55",
        "Type": "float"
    }),
    "timeStopPlayerHawkEyeColorRatio": _tools.RODict({
        "ID": "timeStopPlayerHawkEyeColorRatio",
        "value": "1",
        "Type": "float"
    }),
    "timeStopPlayerHawkEyeColorRGB": _tools.RODict({
        "ID": "timeStopPlayerHawkEyeColorRGB",
        "value": "A6C8F3",
        "Type": "string"
    }),
    "timeStopPlayerHawkEyeColorIntensity": _tools.RODict({
        "ID": "timeStopPlayerHawkEyeColorIntensity",
        "value": "0.8",
        "Type": "float"
    }),
    "usualHawkEyeGrayRatio": _tools.RODict({
        "ID": "usualHawkEyeGrayRatio",
        "value": "0.55",
        "Type": "float"
    }),
    "usualHawkEyeColorRatio": _tools.RODict({
        "ID": "usualHawkEyeColorRatio",
        "value": "0",
        "Type": "float"
    }),
    "usualHawkEyeColorRGB": _tools.RODict({
        "ID": "usualHawkEyeColorRGB",
        "value": "A6C8F3",
        "Type": "string"
    }),
    "usualHawkEyeColorIntensity": _tools.RODict({
        "ID": "usualHawkEyeColorIntensity",
        "value": "0.8",
        "Type": "float"
    }),
    "targetHawkEyeGrayRatio": _tools.RODict({
        "ID": "targetHawkEyeGrayRatio",
        "value": "0.55",
        "Type": "float"
    }),
    "targetHawkEyeColorRatio": _tools.RODict({
        "ID": "targetHawkEyeColorRatio",
        "value": "0",
        "Type": "float"
    }),
    "targetHawkEyeColorRGB": _tools.RODict({
        "ID": "targetHawkEyeColorRGB",
        "value": "FFCA77",
        "Type": "string"
    }),
    "targetHawkEyeColorIntensity": _tools.RODict({
        "ID": "targetHawkEyeColorIntensity",
        "value": "0.9",
        "Type": "float"
    }),
    "enemyHawkEyeGrayRatio": _tools.RODict({
        "ID": "enemyHawkEyeGrayRatio",
        "value": "0.55",
        "Type": "float"
    }),
    "enemyHawkEyeColorRatio": _tools.RODict({
        "ID": "enemyHawkEyeColorRatio",
        "value": "0",
        "Type": "float"
    }),
    "enemyHawkEyeColorRGB": _tools.RODict({
        "ID": "enemyHawkEyeColorRGB",
        "value": "FF868C",
        "Type": "string"
    }),
    "enemyHawkEyeColorIntensity": _tools.RODict({
        "ID": "enemyHawkEyeColorIntensity",
        "value": "1",
        "Type": "int"
    }),
    "hawkEyeBtnSound": _tools.RODict({
        "ID": "hawkEyeBtnSound",
        "value": "85002011",
        "Type": "int"
    }),
    "depthOfField": _tools.RODict({
        "ID": "depthOfField",
        "value": "8",
        "Type": "float"
    }),
    "switchTime": _tools.RODict({
        "ID": "switchTime",
        "value": "0.3",
        "Type": "float"
    }),
    "monsterModelAppear": _tools.RODict({
        "ID": "monsterModelAppear",
        "value": "0.6",
        "Type": "float"
    }),
    "modelZoomTime": _tools.RODict({
        "ID": "modelZoomTime",
        "value": "0.13",
        "Type": "float"
    }),
    "detailShownOnLeft": _tools.RODict({
        "ID": "detailShownOnLeft",
        "value": "6,7,8",
        "Type": "string"
    }),
    "detailShownOnRight": _tools.RODict({
        "ID": "detailShownOnRight",
        "value": "1,2,3,4,5",
        "Type": "string"
    }),
    "swTextNumColor1": _tools.RODict({
        "ID": "swTextNumColor1",
        "value": "98",
        "Type": "int"
    }),
    "bwTextNumColor1": _tools.RODict({
        "ID": "bwTextNumColor1",
        "value": "99",
        "Type": "int"
    }),
    "qwTextNumColor1": _tools.RODict({
        "ID": "qwTextNumColor1",
        "value": "100",
        "Type": "int"
    }),
    "swTextNumColor2": _tools.RODict({
        "ID": "swTextNumColor2",
        "value": "101",
        "Type": "int"
    }),
    "bwTextNumColor2": _tools.RODict({
        "ID": "bwTextNumColor2",
        "value": "102",
        "Type": "int"
    }),
    "qwTextNumColor2": _tools.RODict({
        "ID": "qwTextNumColor2",
        "value": "103",
        "Type": "int"
    }),
    "whiteNameLetter": _tools.RODict({
        "ID": "whiteNameLetter",
        "value": "_·.~★☆♂♀°",
        "Type": "string"
    }),
    "buyBtnTextColor": _tools.RODict({
        "ID": "buyBtnTextColor",
        "value": "144",
        "Type": "int"
    }),
    "uiTipsDialogTextWidth": _tools.RODict({
        "ID": "uiTipsDialogTextWidth",
        "value": "500",
        "Type": "float"
    }),
    "minimapLookCircleRadius": _tools.RODict({
        "ID": "minimapLookCircleRadius",
        "value": "100",
        "Type": "float"
    }),
    "NormalFunctionFirstLine": _tools.RODict({
        "ID": "NormalFunctionFirstLine",
        "value": "6",
        "Type": "int"
    }),
    "UIModalToonBright": _tools.RODict({
        "ID": "UIModalToonBright",
        "value": "0.88",
        "Type": "float"
    }),
    "MainMenuCloseAudio": _tools.RODict({
        "ID": "MainMenuCloseAudio",
        "value": "",
        "Type": "int"
    })
})