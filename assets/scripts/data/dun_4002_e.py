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
        1009,
        1014,
        1138,
        1035,
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
        1167,
        1170,
        1175,
        1176,
        1178,
        1025,
        1205,
        1210,
        1276,
        1208
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
    "taskID": 86060061,
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
    "taskID": 86060003,
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
      40020026,
      40020027,
      40020028,
      40020029,
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
      40020086,
      40020087,
      40020088,
      40020089,
      40020090,
      40020091,
      40020092,
      40020093,
      40020094,
      40020095,
      40020096,
      40020097,
      40020098,
      40020099,
      40020100,
      40020101,
      40020102,
      40020103,
      40020104,
      40020105,
      40020106,
      40020107,
      40020108,
      40020109,
      40020110,
      40020111,
      40020112,
      40020113,
      40020114,
      40020115,
      40020116,
      40020117,
      40020118,
      40020119,
      40020120,
      40020121,
      40020122,
      40020123,
      40020124,
      40020125,
      40020126,
      40020127,
      40020128,
      40020129,
      40020130,
      40020131,
      40020132,
      40020133,
      40020134,
      40020135,
      40020136,
      40020137,
      40020139,
      40020140,
      40020141,
      40020142,
      40020143,
      40020144,
      40020145,
      40020146,
      40020147,
      40020148,
      40020149,
      40020150,
      40020151,
      40020152,
      40020153,
      40020154,
      40020157,
      40020158,
      40020159,
      40020160,
      40020161,
      40020162
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
        1188,
        1230,
        1253
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
        1151
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
      40024029,
      40024030,
      40024031,
      40024032,
      40024033,
      40024034,
      40024035
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
    "transition": {}
  },
  "1012": {
    "type": "taskInProgress",
    "taskID": 86060061,
    "transition": {}
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
  "1033": {
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
    "taskID": 86060146,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1036,
        1089,
        1259
      ]
    }
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
  "1073": {
    "type": "stopAiTick",
    "entityID": [
      40020086,
      40020087,
      40020088,
      40020089,
      40020090,
      40020091,
      40020092,
      40020093,
      40020094,
      40020095,
      40020096,
      40020097,
      40020098,
      40020099,
      40020100,
      40020101,
      40020102,
      40020103,
      40020104,
      40020105,
      40020106,
      40020107,
      40020108,
      40020109,
      40020110,
      40020111,
      40020112,
      40020113,
      40020114,
      40020115,
      40020116,
      40020117,
      40020118,
      40020119,
      40020120,
      40020121,
      40020122,
      40020123,
      40020124,
      40020125,
      40020126,
      40020127,
      40020128,
      40020129,
      40020130,
      40020131,
      40020132,
      40020133,
      40020134,
      40020135,
      40020136,
      40020137,
      40020138,
      40020139,
      40020140,
      40020141,
      40020142,
      40020143,
      40020144,
      40020145,
      40020146,
      40020147,
      40020148,
      40020149,
      40020150,
      40020151,
      40020152,
      40020153,
      40020154,
      40020157,
      40020158,
      40020159,
      40020160,
      40020161,
      40020162
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
  "1143": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010016,
    "exitTime": 12.0,
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
        1203,
        1183,
        1266
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
    "transition": {
      "finished": [
        1275
      ]
    }
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
    "taskID": 86060146,
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
  "1183": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64000071
    ],
    "transition": {}
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
    "hpPercent": 80.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1251
      ]
    }
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
    "transition": {
      "finished": [
        1204
      ]
    }
  },
  "1205": {
    "type": "taskFinished",
    "taskID": 86060055,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1003
      ]
    }
  },
  "1206": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010026,
    "transition": {
      "finished": [
        1232
      ]
    }
  },
  "1207": {
    "type": "startAiTick",
    "entityID": [
      40020086,
      40020087,
      40020088,
      40020089,
      40020090,
      40020091,
      40020092,
      40020093
    ],
    "transition": {}
  },
  "1208": {
    "type": "monsterRestNum",
    "monsterID": [
      40020086,
      40020087,
      40020088,
      40020089,
      40020090,
      40020091,
      40020092,
      40020093
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1209
      ]
    }
  },
  "1209": {
    "type": "startAiTick",
    "entityID": [
      40020094,
      40020095,
      40020096,
      40020097,
      40020098,
      40020099,
      40020100,
      40020101,
      40020102,
      40020103,
      40020104,
      40020105,
      40020106,
      40020107,
      40020108,
      40020109
    ],
    "transition": {}
  },
  "1210": {
    "type": "taskFinished",
    "taskID": 86060085,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1212
      ]
    }
  },
  "1211": {
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
        1213,
        1215,
        1247
      ]
    }
  },
  "1212": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010027,
    "transition": {
      "finished": [
        1235
      ]
    }
  },
  "1213": {
    "type": "monsterHp",
    "monsterID": [
      40020085
    ],
    "compare": 2,
    "hpPercent": 80.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1163,
        1236
      ]
    }
  },
  "1215": {
    "type": "delayLoop",
    "firstDelay": 2.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1273
      ]
    }
  },
  "1217": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010021,
    "transition": {
      "finished": [
        1238,
        1246
      ]
    }
  },
  "1218": {
    "type": "monsterHp",
    "monsterID": [
      40020156
    ],
    "compare": 5,
    "hpPercent": 80.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1219,
        1220
      ]
    }
  },
  "1219": {
    "type": "startAiTick",
    "entityID": [
      40020110,
      40020111,
      40020112,
      40020113,
      40020114,
      40020115,
      40020116,
      40020117,
      40020118,
      40020119,
      40020120,
      40020121,
      40020122,
      40020123,
      40020124,
      40020125,
      40020126,
      40020127,
      40020128,
      40020129,
      40020130,
      40020131,
      40020132,
      40020133
    ],
    "transition": {}
  },
  "1220": {
    "type": "popupdialog",
    "entityID": [
      40020156
    ],
    "dialogID": 19900514,
    "transition": {}
  },
  "1223": {
    "type": "popupdialog",
    "entityID": [
      40020156
    ],
    "dialogID": 19900515,
    "transition": {}
  },
  "1224": {
    "type": "monsterHp",
    "monsterID": [
      40020156
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1225,
        1223
      ]
    }
  },
  "1225": {
    "type": "startAiTick",
    "entityID": [
      40020134,
      40020135,
      40020136,
      40020137,
      40020138,
      40020139,
      40020140,
      40020141,
      40020142,
      40020143,
      40020144,
      40020145,
      40020146,
      40020147,
      40020148,
      40020149,
      40020150,
      40020151,
      40020152,
      40020153,
      40020154
    ],
    "transition": {}
  },
  "1230": {
    "type": "popupdialog",
    "entityID": [
      40024035
    ],
    "dialogID": 19900327,
    "transition": {}
  },
  "1232": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010026,
    "exitTime": 3.0,
    "transition": {
      "finished": [
        1207,
        1240,
        1254
      ]
    }
  },
  "1235": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010027,
    "exitTime": 10.0,
    "transition": {
      "finished": [
        1211
      ]
    }
  },
  "1236": {
    "type": "popupdialog",
    "entityID": [
      40024035
    ],
    "dialogID": 19900328,
    "transition": {}
  },
  "1238": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010021,
    "exitTime": 19.0,
    "transition": {
      "finished": [
        1242,
        1260
      ]
    }
  },
  "1240": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86060098,
    "transition": {}
  },
  "1241": {
    "type": "removeMonster",
    "entityID": [
      40020085
    ],
    "transition": {}
  },
  "1242": {
    "type": "createMonster",
    "entityID": [
      40020156
    ],
    "num": 1,
    "lv": "8",
    "initState": 0,
    "hp": 3500,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1250,
        1218,
        1224,
        1257,
        1263
      ]
    }
  },
  "1246": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86060087,
    "transition": {}
  },
  "1247": {
    "type": "monsterHp",
    "monsterID": [
      40020085
    ],
    "compare": 2,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1217,
        1241
      ]
    }
  },
  "1250": {
    "type": "popupdialog",
    "entityID": [
      40024035
    ],
    "dialogID": 19900329,
    "transition": {}
  },
  "1251": {
    "type": "popupdialog",
    "entityID": [
      40020074
    ],
    "dialogID": 19900511,
    "transition": {}
  },
  "1253": {
    "type": "monsterHp",
    "monsterID": [
      40020074
    ],
    "compare": 2,
    "hpPercent": 60.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1206,
        1033
      ]
    }
  },
  "1254": {
    "type": "popupdialog",
    "entityID": [
      40024035
    ],
    "dialogID": 19900510,
    "transition": {}
  },
  "1257": {
    "type": "monsterHp",
    "monsterID": [
      40020156
    ],
    "compare": 5,
    "hpPercent": 20.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1261,
        1258,
        1274
      ]
    }
  },
  "1258": {
    "type": "popupdialog",
    "entityID": [
      40020156
    ],
    "dialogID": 19900516,
    "transition": {
      "finished": [
        1268
      ]
    }
  },
  "1259": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010015,
    "transition": {
      "finished": [
        1127
      ]
    }
  },
  "1260": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64000139
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1261": {
    "type": "addBuffToMonster",
    "monsterID": [
      40020156
    ],
    "buffID": [
      64000138
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1263": {
    "type": "monsterRestNum",
    "monsterID": [
      40020110,
      40020111,
      40020112,
      40020113,
      40020114,
      40020115,
      40020116,
      40020117,
      40020118,
      40020119,
      40020120,
      40020121,
      40020122,
      40020123,
      40020124,
      40020125,
      40020126,
      40020127,
      40020128,
      40020129,
      40020130,
      40020131,
      40020132,
      40020133,
      40020134,
      40020135,
      40020136,
      40020137,
      40020139,
      40020140,
      40020141,
      40020142,
      40020143,
      40020144,
      40020145,
      40020146,
      40020147,
      40020148,
      40020149,
      40020150,
      40020151,
      40020152,
      40020153,
      40020154,
      40020157,
      40020158,
      40020159,
      40020160,
      40020161,
      40020162
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1265
      ]
    }
  },
  "1264": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      40020156
    ],
    "buffID": [
      64000138
    ],
    "transition": {}
  },
  "1265": {
    "type": "popupdialog",
    "entityID": [
      40020156
    ],
    "dialogID": 19900519,
    "transition": {
      "finished": [
        1271,
        1264
      ]
    }
  },
  "1266": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64000139
    ],
    "transition": {}
  },
  "1267": {
    "type": "popupdialog",
    "entityID": [
      40024035
    ],
    "dialogID": 19900517,
    "transition": {}
  },
  "1268": {
    "type": "delayLoop",
    "firstDelay": 0.0,
    "loopDelay": 3.0,
    "loopNum": 0,
    "transition": {
      "finished": [
        1267
      ]
    }
  },
  "1271": {
    "type": "delayLoop",
    "firstDelay": 0.0,
    "loopDelay": 3.0,
    "loopNum": 0,
    "transition": {
      "finished": [
        1272
      ]
    }
  },
  "1272": {
    "type": "popupdialog",
    "entityID": [
      40024035
    ],
    "dialogID": 19900520,
    "transition": {}
  },
  "1273": {
    "type": "popupdialog",
    "entityID": [
      40020085
    ],
    "dialogID": 19900512,
    "transition": {}
  },
  "1274": {
    "type": "startAiTick",
    "entityID": [
      40020157,
      40020158,
      40020159,
      40020160,
      40020161,
      40020162
    ],
    "transition": {}
  },
  "1275": {
    "type": "taskUndertake",
    "taskID": 86030008,
    "transition": {}
  },
  "1276": {
    "type": "taskFinished",
    "taskID": 86060089,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1143
      ]
    }
  },
  "1204": {
    "type": "createRebornPos",
    "entityID": [
      40028044
    ],
    "num": 1,
    "transition": {}
  }
}