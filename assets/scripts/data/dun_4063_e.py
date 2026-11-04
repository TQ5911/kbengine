datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1015,
        1095,
        1113,
        1119,
        1122,
        1124
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40638002
    ],
    "num": 0,
    "transition": {}
  },
  "1095": {
    "type": "createNPC",
    "entityID": [
      40634001
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1096
      ]
    }
  },
  "1096": {
    "type": "taskFinished",
    "taskID": 86010538,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1097
      ]
    }
  },
  "1097": {
    "type": "createMonster",
    "entityID": [
      40630001,
      40630002,
      40630003,
      40630004,
      40630005,
      40630006,
      40630007,
      40630008,
      40630009
    ],
    "num": 0,
    "lv": "48",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1098
      ]
    }
  },
  "1098": {
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
        1099
      ]
    }
  },
  "1099": {
    "type": "createCollection",
    "entityID": [
      40638004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1101
      ]
    }
  },
  "1101": {
    "type": "taskFinished",
    "taskID": 86010540,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1102
      ]
    }
  },
  "1102": {
    "type": "createMonster",
    "entityID": [
      40630010,
      40630011,
      40630012,
      40630013,
      40630014,
      40630015,
      40630016,
      40630017,
      40630018,
      40630019,
      40630020,
      40630021
    ],
    "num": 0,
    "lv": "48",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1103
      ]
    }
  },
  "1103": {
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
        1104
      ]
    }
  },
  "1104": {
    "type": "createCollection",
    "entityID": [
      40638005
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1105
      ]
    }
  },
  "1105": {
    "type": "taskFinished",
    "taskID": 86010542,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1106
      ]
    }
  },
  "1106": {
    "type": "createMonster",
    "entityID": [
      40630022
    ],
    "num": 0,
    "lv": "48",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1107
      ]
    }
  },
  "1107": {
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
        1108
      ]
    }
  },
  "1108": {
    "type": "createCollection",
    "entityID": [
      40638006
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1109
      ]
    }
  },
  "1109": {
    "type": "taskFinished",
    "taskID": 86010544,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1110
      ]
    }
  },
  "1110": {
    "type": "createMonster",
    "entityID": [
      40630023
    ],
    "num": 0,
    "lv": "48",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1111
      ]
    }
  },
  "1111": {
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
        1112
      ]
    }
  },
  "1112": {
    "type": "createCollection",
    "entityID": [
      40638007
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1113": {
    "type": "collBeCollected",
    "entityID": [
      40638004
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1114
      ]
    }
  },
  "1114": {
    "type": "createCollection",
    "entityID": [
      40638008
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1119": {
    "type": "collBeCollected",
    "entityID": [
      40638005
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1120
      ]
    }
  },
  "1120": {
    "type": "createCollection",
    "entityID": [
      40638009
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1122": {
    "type": "collBeCollected",
    "entityID": [
      40638006
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1123
      ]
    }
  },
  "1123": {
    "type": "createCollection",
    "entityID": [
      40638010
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1124": {
    "type": "collBeCollected",
    "entityID": [
      40638007
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1125
      ]
    }
  },
  "1125": {
    "type": "createCollection",
    "entityID": [
      40638011
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  }
}