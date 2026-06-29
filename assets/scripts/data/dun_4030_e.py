datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1046,
        1047
      ]
    }
  },
  "1046": {
    "type": "createRebornPos",
    "entityID": [
      40308002
    ],
    "num": 0,
    "transition": {}
  },
  "1047": {
    "type": "createMonster",
    "entityID": [
      40300001,
      40300002,
      40300003,
      40300004,
      40300005,
      40300006
    ],
    "num": 0,
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
        1056
      ]
    }
  },
  "1056": {
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
        1057
      ]
    }
  },
  "1057": {
    "type": "createMonster",
    "entityID": [
      40300007,
      40300008,
      40300009,
      40300010,
      40300011,
      40300012
    ],
    "num": 0,
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
        1058
      ]
    }
  },
  "1058": {
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
        1059,
        1060
      ]
    }
  },
  "1059": {
    "type": "createCollection",
    "entityID": [
      40308003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1060": {
    "type": "createMonster",
    "entityID": [
      40300013,
      40300014,
      40300015,
      40300016,
      40300017,
      40300018
    ],
    "num": 0,
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
        1062
      ]
    }
  },
  "1062": {
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
        1063
      ]
    }
  },
  "1063": {
    "type": "createCollection",
    "entityID": [
      40308004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1064
      ]
    }
  },
  "1064": {
    "type": "collBeCollected",
    "entityID": [
      40308004
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1067
      ]
    }
  },
  "1067": {
    "type": "createMonster",
    "entityID": [
      40300019
    ],
    "num": 0,
    "lv": "20",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  }
}