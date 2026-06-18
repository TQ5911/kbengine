datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40210002,
      40210003,
      40210004,
      40210005,
      40210006,
      40210007,
      40210008,
      40210009,
      40210010,
      40210011,
      40210012,
      40210013,
      40210014,
      40210015,
      40210016
    ],
    "num": 0,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1031
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1020
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40218002
    ],
    "num": 0,
    "transition": {}
  },
  "1031": {
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
        1032
      ]
    }
  },
  "1032": {
    "type": "createMonster",
    "entityID": [
      40210001
    ],
    "num": 0,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1033
      ]
    }
  },
  "1033": {
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
        1034
      ]
    }
  },
  "1034": {
    "type": "createNPC",
    "entityID": [
      40214001,
      40214002
    ],
    "num": 0,
    "lv": "30",
    "ifSetBoss": 0,
    "transition": {}
  }
}