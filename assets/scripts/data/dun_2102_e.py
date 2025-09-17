datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      21020003,
      21020004,
      21020005,
      21020006,
      21020007,
      21020008,
      21020009,
      21020010
    ],
    "num": 0,
    "lv": "23",
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
        1086,
        1141,
        1151
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
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
        1014,
        1142
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
  "1014": {
    "type": "createMonster",
    "entityID": [
      21020011,
      21020012,
      21020013,
      21020014,
      21020015,
      21020016,
      21020017,
      21020018,
      21020019
    ],
    "num": 0,
    "lv": "20",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        2020
      ]
    }
  },
  "2020": {
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
        1015
      ]
    }
  },
  "1015": {
    "type": "createMonster",
    "entityID": [
      21020020,
      21020021,
      21020022,
      21020023,
      21020024,
      21020025,
      21020026,
      21020027
    ],
    "num": 0,
    "lv": "23",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1102
      ]
    }
  },
  "1102": {
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
        1103
      ]
    }
  },
  "1103": {
    "type": "createMonster",
    "entityID": [
      21020028,
      21020029,
      21020030,
      21020031,
      21020032,
      21020033,
      21020034,
      21020035,
      21020036
    ],
    "num": 0,
    "lv": "24",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1104,
        1088
      ]
    }
  },
  "1104": {
    "type": "monsterInBattle",
    "monsterID": [
      21020036
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1087
      ]
    }
  },
  "1086": {
    "type": "createAirWall",
    "entityID": [
      21028003,
      21028004,
      21028005,
      21028006,
      21028007,
      21028008,
      21028009,
      21028010,
      21028011,
      21028012,
      21028013,
      21028014,
      21028015,
      21028016,
      21028017,
      21028018
    ],
    "num": 1,
    "transition": {}
  },
  "1087": {
    "type": "popupdialog",
    "entityID": [
      21020036
    ],
    "dialogID": 19900183,
    "transition": {}
  },
  "1088": {
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
        1089,
        1090
      ]
    }
  },
  "1089": {
    "type": "removeAirWall",
    "entityID": [
      21028018
    ],
    "transition": {
      "finished": [
        1110
      ]
    }
  },
  "1090": {
    "type": "createMonster",
    "entityID": [
      21020037,
      21020038,
      21020039,
      21020040,
      21020041,
      21020042,
      21020043,
      21020044
    ],
    "num": 0,
    "lv": "24",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1095
      ]
    }
  },
  "1095": {
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
        1196
      ]
    }
  },
  "1196": {
    "type": "createMonster",
    "entityID": [
      21020045,
      21020046,
      21020047,
      21020048,
      21020049,
      21020050,
      21020051,
      21020052,
      21020053
    ],
    "num": 0,
    "lv": "25",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1099
      ]
    }
  },
  "1099": {
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
        1100
      ]
    }
  },
  "1100": {
    "type": "createMonster",
    "entityID": [
      21020054,
      21020055,
      21020056,
      21020057,
      21020058,
      21020059
    ],
    "num": 0,
    "lv": "25",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1105
      ]
    }
  },
  "1105": {
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
        1106
      ]
    }
  },
  "1106": {
    "type": "createMonster",
    "entityID": [
      21020060,
      21020061,
      21020062,
      21020063,
      21020064,
      21020065,
      21020066
    ],
    "num": 0,
    "lv": "25",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1107
      ]
    }
  },
  "1107": {
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
        1108
      ]
    }
  },
  "1108": {
    "type": "createMonster",
    "entityID": [
      21020067,
      21020068,
      21020069,
      21020070,
      21020071,
      21020072,
      21020073
    ],
    "num": 0,
    "lv": "25",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1109
      ]
    }
  },
  "1109": {
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
        1111,
        1120
      ]
    }
  },
  "1110": {
    "type": "createAirWall",
    "entityID": [
      20128019
    ],
    "num": 0,
    "transition": {}
  },
  "1111": {
    "type": "removeAirWall",
    "entityID": [
      20128019
    ],
    "transition": {
      "finished": [
        1112
      ]
    }
  },
  "1112": {
    "type": "createAirWall",
    "entityID": [
      20128020
    ],
    "num": 0,
    "transition": {}
  },
  "1113": {
    "type": "createMonster",
    "entityID": [
      21020074,
      21020075,
      21020076,
      21020077,
      21020078,
      21020079,
      21020080,
      21020081
    ],
    "num": 0,
    "lv": "26",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1114
      ]
    }
  },
  "1114": {
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
        1115
      ]
    }
  },
  "1115": {
    "type": "createMonster",
    "entityID": [
      21020082,
      21020083,
      21020084,
      21020085,
      21020086,
      21020087,
      21020088,
      21020089,
      21020090
    ],
    "num": 0,
    "lv": "26",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1116,
        1118
      ]
    }
  },
  "1116": {
    "type": "monsterInBattle",
    "monsterID": [
      21020090
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1117
      ]
    }
  },
  "1117": {
    "type": "popupdialog",
    "entityID": [
      21020036
    ],
    "dialogID": 19900184,
    "transition": {}
  },
  "1118": {
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
        1119,
        1132
      ]
    }
  },
  "1119": {
    "type": "removeAirWall",
    "entityID": [
      20128021
    ],
    "transition": {}
  },
  "1132": {
    "type": "createMonster",
    "entityID": [
      21020002
    ],
    "num": 1,
    "lv": "26",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1190
      ]
    }
  },
  "1120": {
    "type": "createMonster",
    "entityID": [
      21020001
    ],
    "num": 1,
    "lv": "25",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1180,
        1125
      ]
    }
  },
  "1125": {
    "type": "monsterRestNum",
    "monsterID": [
      21020001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1200,
        1201,
        1113
      ]
    }
  },
  "1200": {
    "type": "removeAirWall",
    "entityID": [
      20128020
    ],
    "transition": {}
  },
  "1201": {
    "type": "createAirWall",
    "entityID": [
      20128021
    ],
    "num": 1,
    "transition": {}
  },
  "1184": {
    "type": "monsterRestNum",
    "monsterID": [
      21020001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1185
      ]
    }
  },
  "1180": {
    "type": "monsterInBattle",
    "monsterID": [
      21020001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1182,
        1186,
        1143,
        1144,
        1145,
        1146
      ]
    }
  },
  "1185": {
    "type": "popupdialog",
    "entityID": [
      21020001
    ],
    "dialogID": 19013003,
    "transition": {}
  },
  "1182": {
    "type": "monsterHp",
    "monsterID": [
      21020001
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1183,
        1187
      ]
    }
  },
  "1183": {
    "type": "addBuffToMonster",
    "monsterID": [
      21020001
    ],
    "buffID": [
      64004905
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1184
      ]
    }
  },
  "1193": {
    "type": "dunEnd",
    "exitTime": 15.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1195": {
    "type": "monsterRestNum",
    "monsterID": [
      21020002
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1192
      ]
    }
  },
  "1190": {
    "type": "monsterInBattle",
    "monsterID": [
      21020002
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1092,
        1188,
        1147,
        1148,
        1149,
        1150
      ]
    }
  },
  "1192": {
    "type": "popupdialog",
    "entityID": [
      21020002
    ],
    "dialogID": 19014004,
    "transition": {
      "finished": [
        1193
      ]
    }
  },
  "1092": {
    "type": "monsterHp",
    "monsterID": [
      21020002
    ],
    "compare": 5,
    "hpPercent": 75.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1199,
        1189
      ]
    }
  },
  "1199": {
    "type": "addBuffToMonster",
    "monsterID": [
      21020002
    ],
    "buffID": [
      64004904
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1198
      ]
    }
  },
  "1198": {
    "type": "monsterHp",
    "monsterID": [
      21020002
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1197,
        1179
      ]
    }
  },
  "1197": {
    "type": "addBuffToMonster",
    "monsterID": [
      21020002
    ],
    "buffID": [
      64004905
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1194
      ]
    }
  },
  "1194": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      21020002
    ],
    "buffID": [
      64004904
    ],
    "transition": {
      "finished": [
        1195
      ]
    }
  },
  "1186": {
    "type": "popupdialog",
    "entityID": [
      21020001
    ],
    "dialogID": 19013001,
    "transition": {}
  },
  "1187": {
    "type": "popupdialog",
    "entityID": [
      21020001
    ],
    "dialogID": 19013002,
    "transition": {}
  },
  "1188": {
    "type": "popupdialog",
    "entityID": [
      21020002
    ],
    "dialogID": 19014001,
    "transition": {}
  },
  "1189": {
    "type": "popupdialog",
    "entityID": [
      21020002
    ],
    "dialogID": 19014002,
    "transition": {}
  },
  "1179": {
    "type": "popupdialog",
    "entityID": [
      21020002
    ],
    "dialogID": 19014003,
    "transition": {}
  },
  "1141": {
    "type": "createNPC",
    "entityID": [
      21024001,
      21024002,
      21024003,
      21024004
    ],
    "num": 1,
    "lv": "25",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1142": {
    "type": "popupdialog",
    "entityID": [
      21024002
    ],
    "dialogID": 19900211,
    "transition": {}
  },
  "1143": {
    "type": "removeNPC",
    "entityID": [
      21024001,
      21024002,
      21024003,
      21024004
    ],
    "transition": {}
  },
  "1144": {
    "type": "createNPC",
    "entityID": [
      21024005,
      21020006,
      21024007,
      21024008,
      21024009
    ],
    "num": 0,
    "lv": "20",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1145": {
    "type": "removeRebornPos",
    "entityID": [
      21028002
    ],
    "transition": {}
  },
  "1146": {
    "type": "createRebornPos",
    "entityID": [
      21028022
    ],
    "num": 1,
    "transition": {}
  },
  "1147": {
    "type": "removeNPC",
    "entityID": [
      21024006,
      21024007,
      21024008,
      21024009
    ],
    "transition": {}
  },
  "1148": {
    "type": "createNPC",
    "entityID": [
      21024011,
      21024012,
      21024013,
      21024014
    ],
    "num": 0,
    "lv": "20",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1149": {
    "type": "removeRebornPos",
    "entityID": [
      21028022
    ],
    "transition": {}
  },
  "1150": {
    "type": "createRebornPos",
    "entityID": [
      21028023
    ],
    "num": 1,
    "transition": {}
  },
  "1151": {
    "type": "createRebornPos",
    "entityID": [
      21028002
    ],
    "num": 1,
    "transition": {}
  }
}