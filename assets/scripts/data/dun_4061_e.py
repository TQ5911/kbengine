datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1064,
        1015,
        1076
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40618002
    ],
    "num": 0,
    "transition": {}
  },
  "1064": {
    "type": "createMonster",
    "entityID": [
      40610001,
      40610002,
      40610003,
      40610004,
      40610005,
      40610006,
      40610007,
      40610008,
      40610009,
      40610010,
      40610011,
      40610012
    ],
    "num": 0,
    "lv": "40",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1065
      ]
    }
  },
  "1065": {
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
        1066
      ]
    }
  },
  "1066": {
    "type": "createNPC",
    "entityID": [
      40614001
    ],
    "num": 0,
    "lv": "30",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1071
      ]
    }
  },
  "1071": {
    "type": "taskFinished",
    "taskID": 86010517,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1073
      ]
    }
  },
  "1073": {
    "type": "createCollection",
    "entityID": [
      40618003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1074
      ]
    }
  },
  "1074": {
    "type": "collBeCollected",
    "entityID": [
      40618003
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1075
      ]
    }
  },
  "1075": {
    "type": "createMonster",
    "entityID": [
      40610013,
      40610014,
      40610015,
      40610016,
      40610017,
      40610018,
      40610019,
      40610020,
      40610021
    ],
    "num": 0,
    "lv": "40",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1076": {
    "type": "taskFinished",
    "taskID": 86010519,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1077,
        1078
      ]
    }
  },
  "1077": {
    "type": "createCollection",
    "entityID": [
      40618004
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
  "1078": {
    "type": "createNPC",
    "entityID": [
      40614002,
      40614003
    ],
    "num": 0,
    "lv": "30",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1079": {
    "type": "collBeCollected",
    "entityID": [
      40618004
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1080,
        1081
      ]
    }
  },
  "1080": {
    "type": "removeNPC",
    "entityID": [
      40614002,
      40614003
    ],
    "transition": {}
  },
  "1081": {
    "type": "createMonster",
    "entityID": [
      40610022
    ],
    "num": 0,
    "lv": "40",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1082
      ]
    }
  },
  "1082": {
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
        1083,
        1086
      ]
    }
  },
  "1083": {
    "type": "createCollection",
    "entityID": [
      40618005
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1086": {
    "type": "createNPC",
    "entityID": [
      40614004,
      40614005
    ],
    "num": 0,
    "lv": "30",
    "ifSetBoss": 0,
    "transition": {}
  }
}