datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1023,
        1015
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40368002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createMonster",
    "entityID": [
      40410001,
      40410002,
      40410003,
      40410004,
      40410005,
      40410006,
      40410007,
      40410008,
      40410009,
      40410010,
      40410011,
      40410012
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
      40410013
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
        1049
      ]
    }
  },
  "1049": {
    "type": "createNPC",
    "entityID": [
      40414001
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  }
}