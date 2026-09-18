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
    "transition": {
      "finished": [
        1297
      ]
    }
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
        1318,
        1123,
        1322,
        1145,
        1316,
        1276,
        1321,
        1013,
        1004
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
        1024
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
    "transition": {
      "finished": [
        1288
      ]
    }
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
    "initState": 2,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1036": {
    "type": "createMonster",
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
      40020154
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
    "hp": 2000,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1230,
        1213,
        1247
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
      40024033,
      40024034,
      40024035,
      40024036
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
      40028023,
      40028028,
      40028029,
      40028030
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
    "initState": 2,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1073": {
    "type": "stopAiTick",
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
      40020154
    ],
    "transition": {}
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
  "1122": {
    "type": "taskInProgress",
    "taskID": 86060055,
    "transition": {
      "finished": [
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
  "1138": {
    "type": "taskInProgress",
    "taskID": 86060080,
    "transition": {
      "finished": [
        1282,
        1028
      ]
    }
  },
  "1143": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010016,
    "exitTime": 14.0,
    "transition": {
      "finished": [
        1187,
        1281
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
        1148,
        1067
      ]
    }
  },
  "1148": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1038,
        1036,
        1089,
        1202,
        1201,
        1313,
        1314
      ]
    }
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
  "1168": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028036
    ],
    "num": 1,
    "transition": {}
  },
  "1174": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028039
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
        1282,
        1312,
        1174,
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
  "1187": {
    "type": "transferToTheDesignatedMap",
    "mapId": 1002,
    "posX": 296.3204,
    "posY": 17.83401,
    "posZ": 50.41761,
    "angle": 30,
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
  "1205": {
    "type": "taskFinished",
    "taskID": 86060055,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1168,
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
    "hp": 2000,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
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
    "compare": 5,
    "hpPercent": 80.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
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
        1260,
        1163
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
      40020074
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
    "hp": 2000,
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
        1257
      ]
    }
  },
  "1246": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86060098,
    "transition": {}
  },
  "1247": {
    "type": "monsterHp",
    "monsterID": [
      40020074
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
        1258
      ]
    }
  },
  "1258": {
    "type": "popupdialog",
    "entityID": [
      40020156
    ],
    "dialogID": 19900516,
    "transition": {}
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
        1271
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
        1272,
        1264
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
  "1275": {
    "type": "taskUndertake",
    "taskID": 86030008,
    "transition": {}
  },
  "1276": {
    "type": "monsterHp",
    "monsterID": [
      40020156
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1278
      ]
    }
  },
  "1278": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010016,
    "transition": {
      "finished": [
        1143,
        1280,
        1043,
        1042,
        1044,
        1183,
        1266
      ]
    }
  },
  "1280": {
    "type": "removeMonster",
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
      40020154
    ],
    "transition": {}
  },
  "1281": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86060089,
    "transition": {}
  },
  "1282": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98000057,
    "transition": {
      "finished": [
        1283
      ]
    }
  },
  "1283": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98000057,
    "exitTime": 6.1,
    "transition": {
      "finished": [
        1331,
        1332
      ]
    }
  },
  "1288": {
    "type": "taskFinished",
    "taskID": 86060063,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1306,
        1293
      ]
    }
  },
  "1291": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028042
    ],
    "num": 1,
    "transition": {}
  },
  "1293": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028038
    ],
    "num": 1,
    "transition": {}
  },
  "1294": {
    "type": "removeAirWall",
    "entityID": [
      40028030
    ],
    "transition": {}
  },
  "1296": {
    "type": "removeAirWall",
    "entityID": [
      40028028
    ],
    "transition": {}
  },
  "1297": {
    "type": "taskFinished",
    "taskID": 86060056,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1296,
        1304
      ]
    }
  },
  "1301": {
    "type": "taskFinished",
    "taskID": 86060002,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1302
      ]
    }
  },
  "1302": {
    "type": "removeAirWall",
    "entityID": [
      40028023
    ],
    "transition": {}
  },
  "1304": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028037
    ],
    "num": 1,
    "transition": {}
  },
  "1305": {
    "type": "taskInProgress",
    "taskID": 86060061,
    "transition": {
      "finished": [
        1304
      ]
    }
  },
  "1306": {
    "type": "removeAirWall",
    "entityID": [
      40028029
    ],
    "transition": {}
  },
  "1308": {
    "type": "taskFinished",
    "taskID": 86060128,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1294,
        1324
      ]
    }
  },
  "1310": {
    "type": "taskInProgress",
    "taskID": 86060080,
    "transition": {
      "finished": [
        1174
      ]
    }
  },
  "1312": {
    "type": "createRebornPos",
    "entityID": [
      40028001
    ],
    "num": 1,
    "transition": {}
  },
  "1313": {
    "type": "createAirWall",
    "entityID": [
      40028031
    ],
    "num": 1,
    "transition": {}
  },
  "1314": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028040
    ],
    "num": 1,
    "transition": {}
  },
  "1316": {
    "type": "taskInProgress",
    "taskID": 86060098,
    "transition": {
      "finished": [
        1148
      ]
    }
  },
  "1318": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1301,
        1122,
        1205,
        1305,
        1009,
        1308,
        1325
      ]
    }
  },
  "1321": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1291,
        1060,
        1059,
        1058,
        1061
      ]
    }
  },
  "1322": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1138,
        1178,
        1310,
        1326
      ]
    }
  },
  "1324": {
    "type": "createBreakAwayStuckPos",
    "entityID": [
      40028053
    ],
    "num": 1,
    "transition": {}
  },
  "1325": {
    "type": "taskFinished",
    "taskID": 86060003,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1275
      ]
    }
  },
  "1326": {
    "type": "taskFinished",
    "taskID": 86060083,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1328
      ]
    }
  },
  "1328": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010004,
    "transition": {
      "finished": [
        1329
      ]
    }
  },
  "1329": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010004,
    "exitTime": 8.0,
    "transition": {
      "finished": [
        1330
      ]
    }
  },
  "1330": {
    "type": "createNPC",
    "entityID": [
      40024032
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1331": {
    "type": "monsterChangeInitState",
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
    "initState": 0,
    "transition": {}
  },
  "1332": {
    "type": "taskUndertake",
    "taskID": 86030032,
    "transition": {}
  }
}