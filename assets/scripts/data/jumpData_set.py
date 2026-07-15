# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: jumpData/set
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "jumpSpeed": _tools.RODict({
        "ID": "jumpSpeed",
        "value": "10",
        "Type": "float"
    }),
    "jumpGravity": _tools.RODict({
        "ID": "jumpGravity",
        "value": "16",
        "Type": "float"
    }),
    "jumpAirStand": _tools.RODict({
        "ID": "jumpAirStand",
        "value": "0",
        "Type": "float"
    }),
    "doubleJumpSpeed": _tools.RODict({
        "ID": "doubleJumpSpeed",
        "value": "11.3",
        "Type": "float"
    }),
    "doubleJumpGravity": _tools.RODict({
        "ID": "doubleJumpGravity",
        "value": "14.7",
        "Type": "float"
    }),
    "doubleJumpAirStand": _tools.RODict({
        "ID": "doubleJumpAirStand",
        "value": "0",
        "Type": "float"
    }),
    "thirdJumpSpeed": _tools.RODict({
        "ID": "thirdJumpSpeed",
        "value": "10",
        "Type": "float"
    }),
    "thirdJumpGravity": _tools.RODict({
        "ID": "thirdJumpGravity",
        "value": "12.5",
        "Type": "float"
    }),
    "thirdJumpAirStand": _tools.RODict({
        "ID": "thirdJumpAirStand",
        "value": "0",
        "Type": "float"
    }),
    "fallSpeedInit": _tools.RODict({
        "ID": "fallSpeedInit",
        "value": "0",
        "Type": "float"
    }),
    "fallSpeed": _tools.RODict({
        "ID": "fallSpeed",
        "value": "40",
        "Type": "int"
    }),
    "fallSpeedGravity": _tools.RODict({
        "ID": "fallSpeedGravity",
        "value": "28",
        "Type": "float"
    }),
    "speedFallSpeed": _tools.RODict({
        "ID": "speedFallSpeed",
        "value": "60",
        "Type": "int"
    }),
    "horizontalMaxSpeed": _tools.RODict({
        "ID": "horizontalMaxSpeed",
        "value": "6",
        "Type": "int"
    }),
    "horizontalSpeedBlend": _tools.RODict({
        "ID": "horizontalSpeedBlend",
        "value": "2",
        "Type": "float"
    }),
    "horizontalMinSpeed": _tools.RODict({
        "ID": "horizontalMinSpeed",
        "value": "1.8",
        "Type": "float"
    }),
    "doubleJumpFreezeTime": _tools.RODict({
        "ID": "doubleJumpFreezeTime",
        "value": "0.1",
        "Type": "float"
    }),
    "thirdJumpFreezeTime": _tools.RODict({
        "ID": "thirdJumpFreezeTime",
        "value": "1",
        "Type": "float"
    }),
    "flyFreezeTime": _tools.RODict({
        "ID": "flyFreezeTime",
        "value": "0.1",
        "Type": "float"
    }),
    "thirdFlyFreezeTime": _tools.RODict({
        "ID": "thirdFlyFreezeTime",
        "value": "0.1",
        "Type": "float"
    }),
    "flyHorizontalSpeed": _tools.RODict({
        "ID": "flyHorizontalSpeed",
        "value": "17.5",
        "Type": "float"
    }),
    "flyTurnSpeed": _tools.RODict({
        "ID": "flyTurnSpeed",
        "value": "12",
        "Type": "float"
    }),
    "flyLoopTime": _tools.RODict({
        "ID": "flyLoopTime",
        "value": "1.21",
        "Type": "float"
    }),
    "flyEndSpeed": _tools.RODict({
        "ID": "flyEndSpeed",
        "value": "6",
        "Type": "float"
    }),
    "flyEndSpeedBlendTime": _tools.RODict({
        "ID": "flyEndSpeedBlendTime",
        "value": "0.65",
        "Type": "float"
    }),
    "thirdFlyHorizontalSpeed": _tools.RODict({
        "ID": "thirdFlyHorizontalSpeed",
        "value": "18",
        "Type": "float"
    }),
    "thirdFlyTurnSpeed": _tools.RODict({
        "ID": "thirdFlyTurnSpeed",
        "value": "12",
        "Type": "float"
    }),
    "thirdFlyLoopTime": _tools.RODict({
        "ID": "thirdFlyLoopTime",
        "value": "1.44",
        "Type": "float"
    }),
    "thirdFlyEndSpeed": _tools.RODict({
        "ID": "thirdFlyEndSpeed",
        "value": "6",
        "Type": "float"
    }),
    "thirdFlyEndSpeedBlendTime": _tools.RODict({
        "ID": "thirdFlyEndSpeedBlendTime",
        "value": "0.75",
        "Type": "float"
    }),
    "mountHorizontalMaxSpeed": _tools.RODict({
        "ID": "mountHorizontalMaxSpeed",
        "value": "11",
        "Type": "int"
    }),
    "mountHorizontalSpeedBlend": _tools.RODict({
        "ID": "mountHorizontalSpeedBlend",
        "value": "3",
        "Type": "float"
    }),
    "mountHhorizontalMinSpeed": _tools.RODict({
        "ID": "mountHhorizontalMinSpeed",
        "value": "2.7",
        "Type": "float"
    })
})