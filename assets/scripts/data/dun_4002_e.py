datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40020008
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1004": {
    "type": "delayLoop",
    "firstDelay": 2400.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1008
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1010,
        1011,
        1009,
        1012,
        1014,
        1138,
        1035,
        1057,
        1096,
        1046,
        1128,
        1108,
        1115,
        1031,
        1059,
        1066,
        1058,
        1060,
        1064,
        1061,
        1088,
        1145,
        1070,
        1090,
        1097,
        1098,
        1093,
        1103,
        1105,
        1118,
        1122,
        1124,
        1125,
        1013,
        1004,
        1041,
        1129,
        1141,
        1167,
        1170,
        1175,
        1176,
        1178,
        1025
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1009": {
    "type": "taskFinished",
    "taskID": 86060056,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1024,
        1150
      ]
    }
  },
  "1013": {
    "type": "playerRestNum",
    "compare": 1,
    "num": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1008
      ]
    }
  },
  "1024": {
    "type": "createMonster",
    "entityID": [
      40020012,
      40020013,
      40020014,
      40020015,
      40020016,
      40020017,
      40020075,
      40020076
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1025": {
    "type": "taskFinished",
    "taskID": 86060063,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1026
      ]
    }
  },
  "1026": {
    "type": "createMonster",
    "entityID": [
      40020019,
      40020020,
      40020021,
      40020022,
      40020023,
      40020024,
      40020077,
      40020078
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1028": {
    "type": "createMonster",
    "entityID": [
      40020030,
      40020031,
      40020032,
      40020033,
      40020034
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1154
      ]
    }
  },
  "1036": {
    "type": "createMonster",
    "entityID": [
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1073
      ]
    }
  },
  "1038": {
    "type": "createMonster",
    "entityID": [
      40020074
    ],
    "num": 1,
    "lv": "5",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1188
      ]
    }
  },
  "1010": {
    "type": "taskFinished",
    "taskID": 86060053,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1151,
        1003
      ]
    }
  },
  "1058": {
    "type": "createNPC",
    "entityID": [
      40024001,
      40024002,
      40024003,
      40024004,
      40024005,
      40024008,
      40024010,
      40024011,
      40024012,
      40024013,
      40024014,
      40024015,
      40024017,
      40024018,
      40024019,
      40024024,
      40024025,
      40024026,
      40024027,
      40024028,
      40024029,
      40024030,
      40024031,
      40024032,
      40024033,
      40024034
    ],
    "num": 1,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1059": {
    "type": "createCollection",
    "entityID": [
      40028003
    ],
    "num": 1,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1060": {
    "type": "createAirWall",
    "entityID": [
      40028008,
      40028009,
      40028010,
      40028023,
      40028028,
      40028029
    ],
    "num": 1,
    "transition": {}
  },
  "1061": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64006022,
      64006028,
      64006023
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1011": {
    "type": "taskInProgress",
    "taskID": 86060055,
    "transition": {
      "finished": [
        1003
      ]
    }
  },
  "1012": {
    "type": "taskInProgress",
    "taskID": 86060061,
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1014": {
    "type": "taskInProgress",
    "taskID": 86060067,
    "transition": {
      "finished": [
        1026
      ]
    }
  },
  "1041": {
    "type": "taskFinished",
    "taskID": 86060101,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1043,
        1042,
        1044,
        1054
      ]
    }
  },
  "1042": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006022
    ],
    "transition": {}
  },
  "1043": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006023
    ],
    "transition": {}
  },
  "1044": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006028
    ],
    "transition": {}
  },
  "1046": {
    "type": "taskFinished",
    "taskID": 86060087,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1037,
        1126
      ]
    }
  },
  "1033": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1107
      ]
    }
  },
  "1052": {
    "type": "removeMonster",
    "entityID": [
      40020074
    ],
    "transition": {}
  },
  "1054": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010018,
    "transition": {
      "finished": [
        1186
      ]
    }
  },
  "1064": {
    "type": "createRebornPos",
    "entityID": [
      40028001
    ],
    "num": 1,
    "transition": {}
  },
  "1018": {
    "type": "monsterHp",
    "monsterID": [
      40020008
    ],
    "compare": 2,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1135
      ]
    }
  },
  "1035": {
    "type": "taskFinished",
    "taskID": 86060127,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1036,
        1072,
        1074,
        1075,
        1089
      ]
    }
  },
  "1037": {
    "type": "removeMonster",
    "entityID": [
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052,
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059,
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066,
      40020067,
      40020068,
      40020069,
      40020070,
      40020071,
      40020072,
      40020073
    ],
    "transition": {}
  },
  "1067": {
    "type": "createMonster",
    "entityID": [
      40020079,
      40020080,
      40020081,
      40020082,
      40020083,
      40020084
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1174
      ]
    }
  },
  "1068": {
    "type": "createRebornPos",
    "entityID": [
      40028022
    ],
    "num": 1,
    "transition": {}
  },
  "1031": {
    "type": "taskFinished",
    "taskID": 86060051,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1032,
        1069
      ]
    }
  },
  "1032": {
    "type": "createCollection",
    "entityID": [
      40028011
    ],
    "num": 1,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1069": {
    "type": "removeNPC",
    "entityID": [
      40024025
    ],
    "transition": {}
  },
  "1070": {
    "type": "taskFinished",
    "taskID": 86060053,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1071
      ]
    }
  },
  "1071": {
    "type": "removeAirWall",
    "entityID": [
      40028023
    ],
    "transition": {}
  },
  "1072": {
    "type": "createMonster",
    "entityID": [
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1076
      ]
    }
  },
  "1073": {
    "type": "stopAiTick",
    "entityID": [
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052
    ],
    "transition": {
      "finished": [
        1079
      ]
    }
  },
  "1074": {
    "type": "createMonster",
    "entityID": [
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1077
      ]
    }
  },
  "1075": {
    "type": "createMonster",
    "entityID": [
      40020067,
      40020068,
      40020069,
      40020070,
      40020071,
      40020072,
      40020073
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1078
      ]
    }
  },
  "1076": {
    "type": "stopAiTick",
    "entityID": [
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059
    ],
    "transition": {
      "finished": [
        1081
      ]
    }
  },
  "1077": {
    "type": "stopAiTick",
    "entityID": [
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066
    ],
    "transition": {
      "finished": [
        1083
      ]
    }
  },
  "1078": {
    "type": "stopAiTick",
    "entityID": [
      40020067,
      40020068,
      40020069,
      40020070,
      40020071,
      40020072,
      40020073
    ],
    "transition": {
      "finished": [
        1085
      ]
    }
  },
  "1079": {
    "type": "taskFinished",
    "taskID": 86060121,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1080
      ]
    }
  },
  "1080": {
    "type": "startAiTick",
    "entityID": [
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052
    ],
    "transition": {}
  },
  "1081": {
    "type": "taskFinished",
    "taskID": 86060089,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1082
      ]
    }
  },
  "1082": {
    "type": "startAiTick",
    "entityID": [
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059
    ],
    "transition": {}
  },
  "1083": {
    "type": "taskFinished",
    "taskID": 86060124,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1084
      ]
    }
  },
  "1084": {
    "type": "startAiTick",
    "entityID": [
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066
    ],
    "transition": {}
  },
  "1085": {
    "type": "taskFinished",
    "taskID": 86060118,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1086
      ]
    }
  },
  "1086": {
    "type": "startAiTick",
    "entityID": [
      40020067,
      40020068,
      40020069,
      40020070,
      40020071,
      40020072,
      40020073
    ],
    "transition": {}
  },
  "1088": {
    "type": "taskInProgress",
    "taskID": 86060086,
    "transition": {
      "finished": [
        1067
      ]
    }
  },
  "1089": {
    "type": "removeMonster",
    "entityID": [
      40020079,
      40020080,
      40020081,
      40020082,
      40020083,
      40020084
    ],
    "transition": {}
  },
  "1066": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      -1
    ],
    "entityID": [
      40028025,
      40028026,
      40028024,
      40028027,
      40028032,
      40028033,
      40028034,
      40028035
    ],
    "num": 1,
    "transition": {}
  },
  "1057": {
    "type": "taskFinished",
    "taskID": 86060122,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1099
      ]
    }
  },
  "1096": {
    "type": "taskFinished",
    "taskID": 86060116,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1100
      ]
    }
  },
  "1097": {
    "type": "taskFinished",
    "taskID": 86060125,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1101
      ]
    }
  },
  "1098": {
    "type": "taskFinished",
    "taskID": 86060119,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1102
      ]
    }
  },
  "1099": {
    "type": "removeNoHostCreation",
    "entityID": [
      40028026,
      40028032
    ],
    "usePrototypeID": 0,
    "transition": {}
  },
  "1100": {
    "type": "removeNoHostCreation",
    "entityID": [
      40028024,
      40028035
    ],
    "usePrototypeID": 0,
    "transition": {}
  },
  "1101": {
    "type": "removeNoHostCreation",
    "entityID": [
      40028027,
      40028034
    ],
    "usePrototypeID": 0,
    "transition": {}
  },
  "1102": {
    "type": "removeNoHostCreation",
    "entityID": [
      40028025,
      40028033
    ],
    "usePrototypeID": 0,
    "transition": {}
  },
  "1090": {
    "type": "taskFinished",
    "taskID": 86060127,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1091
      ]
    }
  },
  "1091": {
    "type": "createAirWall",
    "entityID": [
      40028031
    ],
    "num": 1,
    "transition": {}
  },
  "1093": {
    "type": "taskFinished",
    "taskID": 86060056,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1092
      ]
    }
  },
  "1092": {
    "type": "removeAirWall",
    "entityID": [
      40028028
    ],
    "transition": {}
  },
  "1103": {
    "type": "taskFinished",
    "taskID": 86060063,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1104,
        1139,
        1180
      ]
    }
  },
  "1104": {
    "type": "removeAirWall",
    "entityID": [
      40028029
    ],
    "transition": {}
  },
  "1105": {
    "type": "taskFinished",
    "taskID": 86060067,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1106
      ]
    }
  },
  "1106": {
    "type": "removeAirWall",
    "entityID": [
      40028030
    ],
    "transition": {}
  },
  "1107": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86060098,
    "transition": {
      "finished": [
        1198
      ]
    }
  },
  "1108": {
    "type": "taskFinished",
    "taskID": 86060085,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1195
      ]
    }
  },
  "1109": {
    "type": "taskUndertake",
    "taskID": 86060129,
    "transition": {}
  },
  "1111": {
    "type": "taskUndertake",
    "taskID": 86060090,
    "transition": {}
  },
  "1115": {
    "type": "taskInProgress",
    "taskID": 86060053,
    "transition": {
      "finished": [
        1032,
        1161
      ]
    }
  },
  "1118": {
    "type": "taskInProgress",
    "taskID": 86060071,
    "transition": {
      "finished": [
        1106
      ]
    }
  },
  "1122": {
    "type": "taskInProgress",
    "taskID": 86060055,
    "transition": {
      "finished": [
        1123,
        1168
      ]
    }
  },
  "1123": {
    "type": "changeSpaceVar",
    "varID": 70100001,
    "formula": "34990001",
    "paramVarIDs": [
      70100001
    ],
    "transition": {}
  },
  "1124": {
    "type": "taskInProgress",
    "taskID": 86060061,
    "transition": {
      "finished": [
        1123,
        1169
      ]
    }
  },
  "1125": {
    "type": "taskInProgress",
    "taskID": 86060071,
    "transition": {
      "finished": [
        1123
      ]
    }
  },
  "1126": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010015,
    "exitTime": 21.0,
    "transition": {
      "finished": [
        1038
      ]
    }
  },
  "1127": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010015,
    "exitTime": 21.0,
    "transition": {
      "finished": [
        1038,
        1201,
        1202
      ]
    }
  },
  "1128": {
    "type": "taskInProgress",
    "taskID": 86060098,
    "transition": {
      "finished": [
        1127,
        1174
      ]
    }
  },
  "1129": {
    "type": "taskFinished",
    "taskID": 86060053,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1130
      ]
    }
  },
  "1130": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98000063,
    "exitTime": 20.0,
    "transition": {
      "finished": [
        1123
      ]
    }
  },
  "1135": {
    "type": "triggerGuide",
    "triggerGuideID": 24100301,
    "transition": {}
  },
  "1138": {
    "type": "taskInProgress",
    "taskID": 86060080,
    "transition": {
      "finished": [
        1028,
        1123,
        1064
      ]
    }
  },
  "1139": {
    "type": "createAirWall",
    "entityID": [
      40028030
    ],
    "num": 1,
    "transition": {}
  },
  "1141": {
    "type": "taskFinished",
    "taskID": 86060129,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1143,
        1068,
        1181,
        1183
      ]
    }
  },
  "1143": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010016,
    "exitTime": 30.0,
    "transition": {
      "finished": [
        1144
      ]
    }
  },
  "1144": {
    "type": "transferToTheDesignatedMap",
    "mapId": 4002,
    "posX": 245.5437,
    "posY": 90.26721,
    "posZ": 348.6067,
    "angle": 271,
    "transition": {
      "finished": [
        1159,
        1203
      ]
    }
  },
  "1145": {
    "type": "taskFinished",
    "taskID": 86060102,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1147,
        1067
      ]
    }
  },
  "1147": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010019,
    "exitTime": 13.0,
    "transition": {
      "finished": [
        1148
      ]
    }
  },
  "1148": {
    "type": "transferToTheDesignatedMap",
    "mapId": 4002,
    "posX": 459.0,
    "posY": 81.0,
    "posZ": 347.0,
    "angle": 259,
    "transition": {}
  },
  "1150": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028037
    ],
    "num": 1,
    "transition": {}
  },
  "1151": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028036
    ],
    "num": 1,
    "transition": {}
  },
  "1180": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028038
    ],
    "num": 1,
    "transition": {}
  },
  "1154": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028039
    ],
    "num": 1,
    "transition": {}
  },
  "1159": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028041
    ],
    "num": 1,
    "transition": {}
  },
  "1161": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028042
    ],
    "num": 1,
    "transition": {}
  },
  "1163": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64000071
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1167": {
    "type": "taskInProgress",
    "taskID": 86060001,
    "transition": {
      "finished": [
        1161
      ]
    }
  },
  "1168": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028036
    ],
    "num": 1,
    "transition": {}
  },
  "1169": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028037
    ],
    "num": 1,
    "transition": {}
  },
  "1170": {
    "type": "taskInProgress",
    "taskID": 86060128,
    "transition": {
      "finished": [
        1171,
        1123,
        1064
      ]
    }
  },
  "1171": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028038
    ],
    "num": 1,
    "transition": {}
  },
  "1174": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028040
    ],
    "num": 1,
    "transition": {}
  },
  "1175": {
    "type": "taskInProgress",
    "taskID": 86060127,
    "transition": {
      "finished": [
        1174
      ]
    }
  },
  "1176": {
    "type": "taskInProgress",
    "taskID": 86060114,
    "transition": {
      "finished": [
        1177,
        1068,
        1123
      ]
    }
  },
  "1177": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028041
    ],
    "num": 1,
    "transition": {}
  },
  "1178": {
    "type": "taskFinished",
    "taskID": 86060075,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1028
      ]
    }
  },
  "1181": {
    "type": "removeRebornPos",
    "entityID": [
      40028001
    ],
    "transition": {}
  },
  "1183": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64000071
    ],
    "transition": {}
  },
  "1184": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010021,
    "exitTime": 26.0,
    "transition": {
      "finished": [
        1193
      ]
    }
  },
  "1186": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010018,
    "exitTime": 19.0,
    "transition": {
      "finished": [
        1187
      ]
    }
  },
  "1187": {
    "type": "transferToTheDesignatedMap",
    "mapId": 4001,
    "posX": 167.0,
    "posY": 63.0,
    "posZ": 116.0,
    "angle": 160,
    "transition": {}
  },
  "1188": {
    "type": "monsterHp",
    "monsterID": [
      40020074
    ],
    "compare": 2,
    "hpPercent": 70.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1033
      ]
    }
  },
  "1193": {
    "type": "createMonster",
    "entityID": [
      40020085
    ],
    "num": 1,
    "lv": "7",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1163
      ]
    }
  },
  "1195": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1184,
        1052,
        1111
      ]
    }
  },
  "1198": {
    "type": "monsterHp",
    "monsterID": [
      40020074
    ],
    "compare": 2,
    "hpPercent": 30.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1200
      ]
    }
  },
  "1200": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86060085,
    "transition": {}
  },
  "1201": {
    "type": "createRebornPos",
    "entityID": [
      40028043
    ],
    "num": 1,
    "transition": {}
  },
  "1202": {
    "type": "removeRebornPos",
    "entityID": [
      40028001
    ],
    "transition": {}
  },
  "1203": {
    "type": "removeRebornPos",
    "entityID": [
      40028043
    ],
    "transition": {}
  }
}