datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      21010001,
      21010002,
      21010003,
      21010004,
      21010005,
      21010006
    ],
    "num": 0,
    "lv": "33",
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
        1134
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
      21010001,
      21010002,
      21010003,
      21010004,
      21010005,
      21010006
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
      21018003,
      21018004,
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
      21018016
    ],
    "num": 1,
    "transition": {}
  },
  "1099": {
    "type": "createMonster",
    "entityID": [
      21010007,
      21010008,
      21010009,
      21010010,
      21010010,
      21010011,
      21010012,
      21010013
    ],
    "num": 0,
    "lv": "33",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1100
      ]
    }
  },
  "1100": {
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
        1101
      ]
    }
  },
  "1101": {
    "type": "createMonster",
    "entityID": [
      21010014,
      21010015,
      21010016,
      21010017,
      21010018,
      21010019,
      21010020,
      21010021,
      21010022,
      21010023,
      21010024,
      21010025
    ],
    "num": 0,
    "lv": "34",
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
      21010027,
      21010028,
      21010029,
      21010030,
      21010031,
      21010032,
      21010033,
      21010034
    ],
    "num": 0,
    "lv": "34",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1104
      ]
    }
  },
  "1104": {
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
        1105
      ]
    }
  },
  "1105": {
    "type": "createMonster",
    "entityID": [
      21010035,
      21010036,
      21010037,
      21010038,
      21010039
    ],
    "num": 0,
    "lv": "35",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1136
      ]
    }
  },
  "1106": {
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
        1107,
        1109
      ]
    }
  },
  "1107": {
    "type": "removeAirWall",
    "entityID": [
      21018014,
      21018015
    ],
    "transition": {}
  },
  "1109": {
    "type": "createMonster",
    "entityID": [
      21010040,
      21010041,
      21010042,
      21010043,
      21010044,
      21010045,
      21010046,
      21010047,
      21010048
    ],
    "num": 0,
    "lv": "35",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1110
      ]
    }
  },
  "1110": {
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
        1111
      ]
    }
  },
  "1111": {
    "type": "createMonster",
    "entityID": [
      21010049,
      21010050,
      21010051
    ],
    "num": 0,
    "lv": "35",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1138
      ]
    }
  },
  "1112": {
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
        1113
      ]
    }
  },
  "1113": {
    "type": "createMonster",
    "entityID": [
      21010052,
      21010053,
      21010054,
      21010055,
      21010056,
      21010057,
      21010058,
      21010059,
      21010060
    ],
    "num": 0,
    "lv": "35",
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
      21010061,
      21010062,
      21010063,
      21010064,
      21010065,
      21010066,
      21010067,
      21010068,
      21010069
    ],
    "num": 0,
    "lv": "35",
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
        1117
      ]
    }
  },
  "1117": {
    "type": "createMonster",
    "entityID": [
      21010070
    ],
    "num": 0,
    "lv": "35",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1118
      ]
    }
  },
  "1120": {
    "type": "monsterRestNum",
    "monsterID": [
      21010070
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1121,
        1122,
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
  "1122": {
    "type": "createMonster",
    "entityID": [
      21010072,
      21010073,
      21010074,
      21010075,
      21010076,
      21010077,
      21010078
    ],
    "num": 0,
    "lv": "36",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1123
      ]
    }
  },
  "1123": {
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
        1124
      ]
    }
  },
  "1124": {
    "type": "createMonster",
    "entityID": [
      21010079,
      21010080,
      21010081,
      21010082,
      21010083,
      21010084
    ],
    "num": 0,
    "lv": "36",
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
      21010085,
      21010086,
      21010087,
      21010088,
      21010089,
      21010090
    ],
    "num": 0,
    "lv": "36",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1140
      ]
    }
  },
  "1127": {
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
        1128
      ]
    }
  },
  "1128": {
    "type": "createMonster",
    "entityID": [
      21010091
    ],
    "num": 0,
    "lv": "36",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1014
      ]
    }
  },
  "1134": {
    "type": "createNPC",
    "entityID": [
      21014001,
      21014002,
      21014003
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1136": {
    "type": "monsterInBattle",
    "monsterID": [
      21010035
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1137
      ]
    }
  },
  "1137": {
    "type": "popupdialog",
    "entityID": [
      21010070
    ],
    "dialogID": 19900195,
    "transition": {
      "finished": [
        1106
      ]
    }
  },
  "1138": {
    "type": "monsterInBattle",
    "monsterID": [
      21010049
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1139
      ]
    }
  },
  "1139": {
    "type": "popupdialog",
    "entityID": [
      21010049
    ],
    "dialogID": 19900197,
    "transition": {
      "finished": [
        1112
      ]
    }
  },
  "1140": {
    "type": "monsterInBattle",
    "monsterID": [
      21010085
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1141
      ]
    }
  },
  "1141": {
    "type": "popupdialog",
    "entityID": [
      21010085
    ],
    "dialogID": 19900191,
    "transition": {
      "finished": [
        1127
      ]
    }
  },
  "1118": {
    "type": "monsterInBattle",
    "monsterID": [
      21010070
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1119,
        1022
      ]
    }
  },
  "1119": {
    "type": "popupdialog",
    "entityID": [
      21010070
    ],
    "dialogID": 19019001,
    "transition": {
      "finished": [
        1120
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      21010070
    ],
    "dialogID": 19019004,
    "transition": {}
  },
  "1022": {
    "type": "delayLoop",
    "firstDelay": 75.0,
    "loopDelay": 75.0,
    "loopNum": 2,
    "transition": {
      "loop": [
        1142
      ]
    }
  },
  "1025": {
    "type": "castSkill",
    "entityID": [
      21010070
    ],
    "skillID": 91025015,
    "lv": "1",
    "forceToUse": 1,
    "transition": {}
  },
  "1142": {
    "type": "popupdialog",
    "entityID": [
      21010070
    ],
    "dialogID": 19019005,
    "transition": {
      "finished": [
        1025
      ]
    }
  },
  "1007": {
    "type": "dunEnd",
    "exitTime": 5.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      21010091
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
      21010091
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1010,
        1021
      ]
    }
  },
  "1010": {
    "type": "popupdialog",
    "entityID": [
      21010091
    ],
    "dialogID": 19900195,
    "transition": {
      "finished": [
        1006
      ]
    }
  },
  "1015": {
    "type": "popupdialog",
    "entityID": [
      21010091
    ],
    "dialogID": 19900194,
    "transition": {
      "finished": [
        1027
      ]
    }
  },
  "1019": {
    "type": "castSkill",
    "entityID": [
      21010091
    ],
    "skillID": 91026008,
    "lv": "1",
    "forceToUse": 0,
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1024": {
    "type": "createMonster",
    "entityID": [
      21010092
    ],
    "num": 1,
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
        1023
      ]
    }
  },
  "1012": {
    "type": "playerRestNum",
    "compare": 3,
    "num": 1,
    "checkNow": 1,
    "checkOnce": 1,
    "transition": {
      "finished": [
        1026
      ]
    }
  },
  "1023": {
    "type": "monsterHp",
    "monsterID": [
      21010092
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1020
      ]
    }
  },
  "1020": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64004046
    ],
    "transition": {}
  },
  "1021": {
    "type": "delayLoop",
    "firstDelay": 65.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1012,
        1028
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
  "1026": {
    "type": "popupdialog",
    "entityID": [
      21010091
    ],
    "dialogID": 19019002,
    "transition": {
      "finished": [
        1019
      ]
    }
  },
  "1028": {
    "type": "playerRestNum",
    "compare": 1,
    "num": 1,
    "checkNow": 1,
    "checkOnce": 1,
    "transition": {
      "finished": [
        1030
      ]
    }
  },
  "1030": {
    "type": "popupdialog",
    "entityID": [
      21010091
    ],
    "dialogID": 19019005,
    "transition": {
      "finished": [
        1032,
        1037
      ]
    }
  },
  "1032": {
    "type": "createMonster",
    "entityID": [
      21010092
    ],
    "num": 1,
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
        1035
      ]
    }
  },
  "1035": {
    "type": "monsterHp",
    "monsterID": [
      21010092
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1143
      ]
    }
  },
  "1037": {
    "type": "addBuffToMonster",
    "monsterID": [
      21010091
    ],
    "buffID": [
      64004040
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1143": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      21010091
    ],
    "buffID": [
      64004040
    ],
    "transition": {}
  }
}