datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1046,
        1064,
        1065,
        1069
      ]
    }
  },
  "1046": {
    "type": "createRebornPos",
    "entityID": [
      40298002
    ],
    "num": 0,
    "transition": {}
  },
  "1064": {
    "type": "createCollection",
    "entityID": [
      40298003,
      40298004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1065": {
    "type": "taskFinished",
    "taskID": 86010197,
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
      40290001,
      40290002,
      40290003,
      40290004,
      40290005,
      40290006,
      40290007,
      40290008,
      40290009
    ],
    "num": 0,
    "lv": "1",
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
    "type": "createMonster",
    "entityID": [
      40290010
    ],
    "num": 0,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1069": {
    "type": "createNPC",
    "entityID": [
      40294001
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  }
}