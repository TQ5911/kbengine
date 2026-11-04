datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1015,
        1075,
        1064,
        1102,
        1104
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40688002
    ],
    "num": 0,
    "transition": {}
  },
  "1064": {
    "type": "createCollection",
    "entityID": [
      40688003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1065
      ]
    }
  },
  "1065": {
    "type": "collBeCollected",
    "entityID": [
      40688003
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1084,
        1077,
        1092
      ]
    }
  },
  "1075": {
    "type": "createNPC",
    "entityID": [
      40684005,
      40684006,
      40684007,
      40684008,
      40684020,
      40684021,
      40684022,
      40684023
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1077": {
    "type": "createNPC",
    "entityID": [
      40684001
    ],
    "num": 0,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1078": {
    "type": "collBeCollected",
    "entityID": [
      40688004
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1085,
        1089,
        1094
      ]
    }
  },
  "1079": {
    "type": "collBeCollected",
    "entityID": [
      40688005
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1086,
        1090,
        1096
      ]
    }
  },
  "1084": {
    "type": "createMonster",
    "entityID": [
      40680002,
      40680003,
      40680004,
      40680005,
      40680006,
      40680007,
      40680008,
      40680009,
      40680010,
      40680011
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
        1099
      ]
    }
  },
  "1085": {
    "type": "createMonster",
    "entityID": [
      40680012,
      40680013
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
        1101
      ]
    }
  },
  "1086": {
    "type": "createMonster",
    "entityID": [
      40680001
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
        1097,
        1098,
        1103,
        1123
      ]
    }
  },
  "1089": {
    "type": "createNPC",
    "entityID": [
      40684002
    ],
    "num": 0,
    "lv": "9",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1090": {
    "type": "createNPC",
    "entityID": [
      40684003
    ],
    "num": 0,
    "lv": "9",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1092": {
    "type": "removeNPC",
    "entityID": [
      40684005,
      40684020
    ],
    "transition": {}
  },
  "1093": {
    "type": "createCollection",
    "entityID": [
      40688004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1078
      ]
    }
  },
  "1094": {
    "type": "removeNPC",
    "entityID": [
      40684006,
      40684021
    ],
    "transition": {}
  },
  "1095": {
    "type": "createCollection",
    "entityID": [
      40688005
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1079
      ]
    }
  },
  "1096": {
    "type": "removeNPC",
    "entityID": [
      40684007,
      40684022
    ],
    "transition": {}
  },
  "1097": {
    "type": "removeNPC",
    "entityID": [
      40684001,
      40684002,
      40684003,
      40684004,
      40684005,
      40684006,
      40684007,
      40684008,
      40684023
    ],
    "transition": {}
  },
  "1098": {
    "type": "removeCollection",
    "entityID": [
      40688003,
      40688004,
      40688005,
      40688006
    ],
    "transition": {}
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
        1093
      ]
    }
  },
  "1101": {
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
        1095
      ]
    }
  },
  "1102": {
    "type": "createNPC",
    "entityID": [
      40684019
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1103": {
    "type": "removeNPC",
    "entityID": [
      40684019
    ],
    "transition": {}
  },
  "1104": {
    "type": "createNPC",
    "entityID": [
      40684009,
      40684010
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1105": {
    "type": "popupdialog",
    "entityID": [
      40684010
    ],
    "dialogID": 19900705,
    "transition": {
      "finished": [
        1106
      ]
    }
  },
  "1106": {
    "type": "delayLoop",
    "firstDelay": 3.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1107
      ]
    }
  },
  "1107": {
    "type": "popupdialog",
    "entityID": [
      40680001
    ],
    "dialogID": 19900706,
    "transition": {
      "finished": [
        1108
      ]
    }
  },
  "1108": {
    "type": "delayLoop",
    "firstDelay": 3.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1109
      ]
    }
  },
  "1109": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010029,
    "transition": {
      "finished": [
        1110,
        1111,
        1116
      ]
    }
  },
  "1110": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010029,
    "exitTime": 19.01667,
    "transition": {
      "finished": [
        1114
      ]
    }
  },
  "1111": {
    "type": "removeMonster",
    "entityID": [
      40680001
    ],
    "transition": {}
  },
  "1114": {
    "type": "createMonster",
    "entityID": [
      40680001
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
        1115,
        1124
      ]
    }
  },
  "1115": {
    "type": "monsterHp",
    "monsterID": [
      40680001
    ],
    "compare": 5,
    "hpPercent": 30.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1117
      ]
    }
  },
  "1116": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86010551,
    "transition": {}
  },
  "1117": {
    "type": "popupdialog",
    "entityID": [
      40680001
    ],
    "dialogID": 19900711,
    "transition": {
      "finished": [
        1118
      ]
    }
  },
  "1118": {
    "type": "delayLoop",
    "firstDelay": 5.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1119
      ]
    }
  },
  "1119": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010026,
    "transition": {
      "finished": [
        1120,
        1126
      ]
    }
  },
  "1120": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010026,
    "exitTime": 2.96,
    "transition": {
      "finished": [
        1121,
        1122
      ]
    }
  },
  "1121": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86010510,
    "transition": {}
  },
  "1122": {
    "type": "removeNPC",
    "entityID": [
      40684009
    ],
    "transition": {}
  },
  "1123": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010015,
    "exitTime": 21.0,
    "transition": {
      "finished": [
        1105
      ]
    }
  },
  "1124": {
    "type": "popupdialog",
    "entityID": [
      40684010
    ],
    "dialogID": 19900707,
    "transition": {}
  },
  "1126": {
    "type": "removeMonster",
    "entityID": [
      40680001
    ],
    "transition": {}
  }
}