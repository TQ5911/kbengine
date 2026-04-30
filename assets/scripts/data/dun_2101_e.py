datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      21010024,
      21010025,
      21010026,
      21010027,
      21010028,
      21010029,
      21010030,
      21010031,
      21010032,
      21010033,
      21010034,
      21010035,
      21010036,
      21010037,
      21010038
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1009
      ]
    }
  },
  "1004": {
    "type": "delayLoop",
    "firstDelay": 1800.0,
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
        1003,
        1004,
        1013,
        1096,
        1134,
        1144
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 65.0,
    "transition": {}
  },
  "1009": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1099
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
  "1096": {
    "type": "createAirWall",
    "entityID": [
      21018005,
      21018006,
      21018007,
      21018008,
      21018009,
      21018010,
      21018011,
      21018012,
      21018013,
      21018014,
      21018015,
      21018016,
      21018017,
      21018018,
      21018019,
      21018020,
      21018021,
      21018022,
      21018023,
      21018024,
      21018025
    ],
    "num": 1,
    "transition": {}
  },
  "1099": {
    "type": "createMonster",
    "entityID": [
      21010042,
      21010043,
      21010044,
      21010048,
      21010049,
      21010050,
      21010084,
      21010085,
      21010086,
      21010087,
      21010088,
      21010089,
      21010090,
      21010091,
      21010092,
      21010093,
      21010094,
      21010095
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1166
      ]
    }
  },
  "1116": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1146,
        1159
      ]
    }
  },
  "1117": {
    "type": "createMonster",
    "entityID": [
      21010051
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1118,
        1120
      ]
    }
  },
  "1120": {
    "type": "monsterRestNum",
    "monsterID": [
      21010051
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1121,
        1124,
        1011
      ]
    }
  },
  "1121": {
    "type": "removeAirWall",
    "entityID": [
      21018016
    ],
    "transition": {}
  },
  "1124": {
    "type": "createMonster",
    "entityID": [
      21010052,
      21010053,
      21010054,
      21010055
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1125
      ]
    }
  },
  "1125": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1126
      ]
    }
  },
  "1126": {
    "type": "createMonster",
    "entityID": [
      21010100,
      21010101,
      21010102,
      21010103,
      21010104,
      21010105,
      21010106,
      21010107,
      21010108,
      21010109,
      21010110,
      21010111,
      21010112,
      21010113,
      21010114,
      21010115,
      21010116,
      21010117
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1168
      ]
    }
  },
  "1128": {
    "type": "createMonster",
    "entityID": [
      21010082
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1014,
        1006
      ]
    }
  },
  "1134": {
    "type": "createNPC",
    "entityID": [
      21014003,
      21014004,
      21014005,
      21014006
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1118": {
    "type": "monsterInBattle",
    "monsterID": [
      21010051
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1119,
        1147,
        1148,
        1171
      ]
    }
  },
  "1119": {
    "type": "popupdialog",
    "entityID": [
      21010051
    ],
    "dialogID": 19019001,
    "transition": {}
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      21010051
    ],
    "dialogID": 19900198,
    "transition": {}
  },
  "1007": {
    "type": "dunEnd",
    "exitTime": 65.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      21010082
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1015
      ]
    }
  },
  "1014": {
    "type": "monsterInBattle",
    "monsterID": [
      21010082
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1010,
        1191,
        1999,
        1172
      ]
    }
  },
  "1010": {
    "type": "popupdialog",
    "entityID": [
      21010082
    ],
    "dialogID": 19900195,
    "transition": {}
  },
  "1015": {
    "type": "popupdialog",
    "entityID": [
      21010082
    ],
    "dialogID": 19900196,
    "transition": {
      "finished": [
        1027
      ]
    }
  },
  "1027": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64004046
    ],
    "transition": {
      "finished": [
        1007
      ]
    }
  },
  "1144": {
    "type": "createRebornPos",
    "entityID": [
      21018002
    ],
    "num": 1,
    "transition": {}
  },
  "1146": {
    "type": "popupdialog",
    "entityID": [
      21010048
    ],
    "dialogID": 19900197,
    "transition": {
      "finished": [
        1117
      ]
    }
  },
  "1147": {
    "type": "removeRebornPos",
    "entityID": [
      21018002
    ],
    "transition": {
      "finished": [
        1149
      ]
    }
  },
  "1148": {
    "type": "removeNPC",
    "entityID": [
      21014003,
      21014004,
      21014005,
      21014006
    ],
    "transition": {
      "finished": [
        1150
      ]
    }
  },
  "1149": {
    "type": "createRebornPos",
    "entityID": [
      21018003
    ],
    "num": 1,
    "transition": {}
  },
  "1150": {
    "type": "createNPC",
    "entityID": [
      21014007,
      21014008,
      21014009,
      21014010,
      21014011
    ],
    "num": 1,
    "lv": "35",
    "ifSetBoss": 1,
    "transition": {}
  },
  "1151": {
    "type": "monsterInBattle",
    "monsterID": [
      21010118
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1152
      ]
    }
  },
  "1152": {
    "type": "popupdialog",
    "entityID": [
      21010118
    ],
    "dialogID": 19900187,
    "transition": {}
  },
  "1153": {
    "type": "createMonster",
    "entityID": [
      21010118,
      21010119,
      21010120,
      21010121,
      21010122,
      21010123,
      21010124,
      21010125,
      21010126
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1154,
        1151
      ]
    }
  },
  "1154": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1155
      ]
    }
  },
  "1155": {
    "type": "createMonster",
    "entityID": [
      21010127,
      21010128,
      21010129,
      21010130,
      21010131,
      21010132,
      21010133,
      21010134,
      21010135,
      21010136,
      21010137,
      21010138,
      21010139,
      21010140,
      21010141,
      21010142,
      21010143,
      21010144,
      21010145,
      21010146,
      21010147,
      21010148,
      21010149,
      21010150,
      21010151,
      21010152,
      21010153
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1169
      ]
    }
  },
  "1191": {
    "type": "removeRebornPos",
    "entityID": [
      21018003
    ],
    "transition": {
      "finished": [
        1998
      ]
    }
  },
  "1998": {
    "type": "createRebornPos",
    "entityID": [
      21018004
    ],
    "num": 1,
    "transition": {}
  },
  "1999": {
    "type": "removeNPC",
    "entityID": [
      21014008,
      21014009,
      21014010,
      21014011
    ],
    "transition": {
      "finished": [
        1158
      ]
    }
  },
  "1158": {
    "type": "createNPC",
    "entityID": [
      21014013,
      21014014,
      21014015,
      21014016,
      21014012
    ],
    "num": 1,
    "lv": "35",
    "ifSetBoss": 1,
    "transition": {}
  },
  "1159": {
    "type": "removeAirWall",
    "entityID": [
      21018025
    ],
    "transition": {
      "finished": [
        1160
      ]
    }
  },
  "1160": {
    "type": "createAirWall",
    "entityID": [
      21018026
    ],
    "num": 1,
    "transition": {}
  },
  "1163": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1128,
        1164
      ]
    }
  },
  "1164": {
    "type": "removeAirWall",
    "entityID": [
      21018026
    ],
    "transition": {}
  },
  "1166": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1167
      ]
    }
  },
  "1167": {
    "type": "createMonster",
    "entityID": [
      21010096,
      21010097,
      21010098,
      21010099
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1116
      ]
    }
  },
  "1168": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1153
      ]
    }
  },
  "1169": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1170
      ]
    }
  },
  "1170": {
    "type": "createMonster",
    "entityID": [
      21010154,
      21010155,
      21010156,
      21010157,
      21010158
    ],
    "num": 0,
    "lv": "17",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1163
      ]
    }
  },
  "1171": {
    "type": "addBuffToMonster",
    "monsterID": [
      21010051
    ],
    "buffID": [
      64004085
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": 30.0,
    "transition": {}
  },
  "1172": {
    "type": "addBuffToMonster",
    "monsterID": [
      21010082
    ],
    "buffID": [
      64004085
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": 30.0,
    "transition": {}
  }
}