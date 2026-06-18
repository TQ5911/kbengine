datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1023,
        1015,
        1051
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40378002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createMonster",
    "entityID": [
      40370001,
      40370002,
      40370003,
      40370004,
      40370005,
      40370006,
      40370007,
      40370008,
      40370009,
      40370010,
      40370011,
      40370012
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
        1046
      ]
    }
  },
  "1046": {
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
  "1047": {
    "type": "createMonster",
    "entityID": [
      40370013
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
        1049
      ]
    }
  },
  "1048": {
    "type": "createCollection",
    "entityID": [
      40378003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1052
      ]
    }
  },
  "1049": {
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
        1048
      ]
    }
  },
  "1050": {
    "type": "createNPC",
    "entityID": [
      40374002
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1051": {
    "type": "createNPC",
    "entityID": [
      40374001
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1052": {
    "type": "collBeCollected",
    "entityID": [
      40378003
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1050,
        1054
      ]
    }
  },
  "1054": {
    "type": "removeNPC",
    "entityID": [
      40374001
    ],
    "transition": {}
  }
}