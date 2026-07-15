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
      40038002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createMonster",
    "entityID": [
      40030043,
      40030044,
      40030045
    ],
    "num": 0,
    "lv": "13",
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
        1034,
        1046,
        1036
      ]
    }
  },
  "1034": {
    "type": "createMonster",
    "entityID": [
      40030037,
      40030038,
      40030039,
      40030052,
      40030053,
      40030054,
      40030058,
      40030059,
      40030060,
      40030076,
      40030077,
      40030078
    ],
    "num": 0,
    "lv": "13",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1036": {
    "type": "createMonster",
    "entityID": [
      40030056,
      40030057,
      40030061
    ],
    "num": 0,
    "lv": "13",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1037
      ]
    }
  },
  "1037": {
    "type": "addBuffToMonster",
    "monsterID": [
      40030056,
      40030057,
      40030061
    ],
    "buffID": [
      64000140,
      64000141
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1039": {
    "type": "createMonster",
    "entityID": [
      40030065,
      40030066,
      40030075
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
        1040
      ]
    }
  },
  "1040": {
    "type": "addBuffToMonster",
    "monsterID": [
      40030065,
      40030066,
      40030075
    ],
    "buffID": [
      64000140,
      64000141
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1042": {
    "type": "createMonster",
    "entityID": [
      40030071,
      40030072,
      40030073,
      40030074,
      40030085,
      40030086,
      40030087
    ],
    "num": 0,
    "lv": "13",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1043
      ]
    }
  },
  "1043": {
    "type": "taskFinished",
    "taskID": 86060119,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1044
      ]
    }
  },
  "1044": {
    "type": "createMonster",
    "entityID": [
      40030067
    ],
    "num": 0,
    "lv": "13",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1046": {
    "type": "taskFinished",
    "taskID": 86060033,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1050
      ]
    }
  },
  "1048": {
    "type": "createMonster",
    "entityID": [
      40030046,
      40030047,
      40030047,
      40030062,
      40030063,
      40030064,
      40030068,
      40030069,
      40030070,
      40030082,
      40030083,
      40030084,
      40030088,
      40030089,
      40030090
    ],
    "num": 0,
    "lv": "13",
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
  "1049": {
    "type": "taskFinished",
    "taskID": 86060155,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1042
      ]
    }
  },
  "1050": {
    "type": "createMonster",
    "entityID": [
      40030079,
      40030080,
      40030081
    ],
    "num": 0,
    "lv": "13",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1051
      ]
    }
  },
  "1051": {
    "type": "taskFinished",
    "taskID": 86060154,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1048,
        1039
      ]
    }
  }
}