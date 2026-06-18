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
      40478002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createMonster",
    "entityID": [
      40470001,
      40470002,
      40470003,
      40470004,
      40470005,
      40470006,
      40470007,
      40470008,
      40470009,
      40470010,
      40470011,
      40470012,
      40470013,
      40470014,
      40470015
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
    "type": "createCollection",
    "entityID": [
      40478003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1048
      ]
    }
  },
  "1048": {
    "type": "taskFinished",
    "taskID": 86010332,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1049,
        1056
      ]
    }
  },
  "1049": {
    "type": "createCollection",
    "entityID": [
      40478004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1050
      ]
    }
  },
  "1050": {
    "type": "taskFinished",
    "taskID": 86010333,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1051,
        1057
      ]
    }
  },
  "1051": {
    "type": "createCollection",
    "entityID": [
      40478005
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1052
      ]
    }
  },
  "1052": {
    "type": "taskFinished",
    "taskID": 86010334,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1053,
        1058
      ]
    }
  },
  "1053": {
    "type": "createCollection",
    "entityID": [
      40478006
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1054
      ]
    }
  },
  "1054": {
    "type": "taskFinished",
    "taskID": 86010335,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1055,
        1059
      ]
    }
  },
  "1055": {
    "type": "createNPC",
    "entityID": [
      40474001,
      40474002
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1056": {
    "type": "removeCollection",
    "entityID": [
      40478003
    ],
    "transition": {}
  },
  "1057": {
    "type": "removeCollection",
    "entityID": [
      40478004
    ],
    "transition": {}
  },
  "1058": {
    "type": "removeCollection",
    "entityID": [
      40478005
    ],
    "transition": {}
  },
  "1059": {
    "type": "removeCollection",
    "entityID": [
      40478006
    ],
    "transition": {}
  }
}