datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40160008,
      40160009,
      40160010,
      40160011,
      40160012,
      40160013
    ],
    "num": 0,
    "lv": "11",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1029
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
      40168002
    ],
    "num": 0,
    "transition": {}
  },
  "1029": {
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
      40160005,
      40160006,
      40160007,
      40160002,
      40160003,
      40160004,
      40160014,
      40160015,
      40160016
    ],
    "num": 0,
    "lv": "11",
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
    "type": "createMonster",
    "entityID": [
      40160001
    ],
    "num": 0,
    "lv": "11",
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
        1036,
        1037
      ]
    }
  },
  "1036": {
    "type": "createCollection",
    "entityID": [
      40168006
    ],
    "num": 1,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1045,
        1044
      ]
    }
  },
  "1037": {
    "type": "popupdialog",
    "entityID": [
      40160001
    ],
    "dialogID": 19900397,
    "transition": {}
  },
  "1044": {
    "type": "changeAllPlayerCameraLookPos",
    "entityID": [
      40168006
    ],
    "transition": {}
  },
  "1045": {
    "type": "collBeCollected",
    "entityID": [
      40168006
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1046
      ]
    }
  },
  "1046": {
    "type": "createNPC",
    "entityID": [
      40164001
    ],
    "num": 1,
    "lv": "11",
    "ifSetBoss": 0,
    "transition": {}
  }
}