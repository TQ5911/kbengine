datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1046,
        1015
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40388002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
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
        1047
      ]
    }
  },
  "1046": {
    "type": "createMonster",
    "entityID": [
      40380004,
      40380005,
      40380006,
      40380007,
      40380008,
      40380009,
      40380010,
      40380011,
      40380012,
      40380013,
      40380014,
      40380015
    ],
    "num": 0,
    "lv": "0",
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
  "1047": {
    "type": "createMonster",
    "entityID": [
      40380016
    ],
    "num": 0,
    "lv": "0",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1048
      ]
    }
  },
  "1048": {
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
        1049,
        1050
      ]
    }
  },
  "1049": {
    "type": "createCollection",
    "entityID": [
      40388003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1051
      ]
    }
  },
  "1050": {
    "type": "createNPC",
    "entityID": [
      40384001
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1051": {
    "type": "collBeCollected",
    "entityID": [
      40388003
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1052,
        1053
      ]
    }
  },
  "1052": {
    "type": "removeNPC",
    "entityID": [
      40384001
    ],
    "transition": {}
  },
  "1053": {
    "type": "createNPC",
    "entityID": [
      40384002
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  }
}