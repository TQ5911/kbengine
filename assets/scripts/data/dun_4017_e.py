datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40170001,
      40170002,
      40170003
    ],
    "num": 0,
    "lv": "10",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1032,
        1020
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40178002
    ],
    "num": 0,
    "transition": {}
  },
  "1029": {
    "type": "monsterHp",
    "monsterID": [
      40170007
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1030
      ]
    }
  },
  "1030": {
    "type": "popupdialog",
    "entityID": [
      40170007
    ],
    "dialogID": 19900398,
    "transition": {}
  },
  "1032": {
    "type": "createMonster",
    "entityID": [
      40170004,
      40170005,
      40170006,
      40170008,
      40170009,
      40170010
    ],
    "num": 0,
    "lv": "10",
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
      40170007
    ],
    "num": 0,
    "lv": "10",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1029,
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
        1044
      ]
    }
  },
  "1036": {
    "type": "createCollection",
    "entityID": [
      40178003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1039
      ]
    }
  },
  "1039": {
    "type": "collBeCollected",
    "entityID": [
      40178003
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1043
      ]
    }
  },
  "1043": {
    "type": "createNPC",
    "entityID": [
      40174001
    ],
    "num": 0,
    "lv": "11",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1044": {
    "type": "createCollection",
    "entityID": [
      40178006
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1045
      ]
    }
  },
  "1045": {
    "type": "collBeCollected",
    "entityID": [
      40178006
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1036
      ]
    }
  }
}