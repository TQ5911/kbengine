datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1064,
        1015,
        1077
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40668002
    ],
    "num": 0,
    "transition": {}
  },
  "1064": {
    "type": "createMonster",
    "entityID": [
      40660001,
      40660002,
      40660003,
      40660004,
      40660005,
      40660006,
      40660007,
      40660008,
      40660009
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
    "type": "createMonster",
    "entityID": [
      40660010,
      40660011,
      40660012,
      40660013,
      40660014,
      40660015,
      40660016,
      40660017,
      40660018,
      40660019,
      40660020,
      40660021
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
        1067
      ]
    }
  },
  "1067": {
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
        1068
      ]
    }
  },
  "1068": {
    "type": "createNPC",
    "entityID": [
      40664001
    ],
    "num": 0,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1072
      ]
    }
  },
  "1072": {
    "type": "taskFinished",
    "taskID": 86010478,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1073,
        1075
      ]
    }
  },
  "1073": {
    "type": "createMonster",
    "entityID": [
      40660022
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
        1074
      ]
    }
  },
  "1074": {
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
        1076
      ]
    }
  },
  "1075": {
    "type": "removeNPC",
    "entityID": [
      40664001
    ],
    "transition": {}
  },
  "1076": {
    "type": "createCollection",
    "entityID": [
      40668004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1077": {
    "type": "taskFinished",
    "taskID": 86010480,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1078,
        1080
      ]
    }
  },
  "1078": {
    "type": "createNPC",
    "entityID": [
      40664002,
      40664003,
      40664004
    ],
    "num": 0,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1080": {
    "type": "removeNPC",
    "entityID": [
      40664001
    ],
    "transition": {}
  }
}