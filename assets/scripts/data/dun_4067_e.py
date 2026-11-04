datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1064,
        1015
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40678002
    ],
    "num": 0,
    "transition": {}
  },
  "1064": {
    "type": "createMonster",
    "entityID": [
      40670001,
      40670002,
      40670003,
      40670004,
      40670005,
      40670006,
      40670007,
      40670008,
      40670009
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
      40670010,
      40670011,
      40670012,
      40670013,
      40670014,
      40670015,
      40670016,
      40670017,
      40670018,
      40670019,
      40670020,
      40670021
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
    "type": "createMonster",
    "entityID": [
      40670022
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
        1071
      ]
    }
  },
  "1071": {
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
        1072
      ]
    }
  },
  "1072": {
    "type": "createCollection",
    "entityID": [
      40678004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1073
      ]
    }
  },
  "1073": {
    "type": "collBeCollected",
    "entityID": [
      40678004
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1074
      ]
    }
  },
  "1074": {
    "type": "createNPC",
    "entityID": [
      40674001,
      40674002
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  }
}