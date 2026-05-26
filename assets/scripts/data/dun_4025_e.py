datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40250001,
      40250002,
      40250003,
      40250004,
      40250005,
      40250006,
      40250007,
      40250008,
      40250009,
      40250010,
      40250011,
      40250012,
      40250013,
      40250014,
      40250015
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
        1033
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
      40258002
    ],
    "num": 0,
    "transition": {}
  },
  "1032": {
    "type": "createMonster",
    "entityID": [
      40250016
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
        1035
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
        1032
      ]
    }
  },
  "1034": {
    "type": "createMonster",
    "entityID": [
      40250017,
      40250018,
      40250019,
      40250020,
      40250021,
      40250022,
      40250023,
      40250024,
      402500025,
      40250027,
      40250028,
      40250029,
      40250030,
      40250031,
      40250032
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
        1036
      ]
    }
  },
  "1035": {
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
  "1036": {
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
        1037
      ]
    }
  },
  "1037": {
    "type": "createMonster",
    "entityID": [
      40250026
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
        1038
      ]
    }
  },
  "1038": {
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
        1039
      ]
    }
  },
  "1039": {
    "type": "createCollection",
    "entityID": [
      40258003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  }
}