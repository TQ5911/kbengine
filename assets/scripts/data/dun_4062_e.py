datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1015,
        1071,
        1072
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40628002
    ],
    "num": 0,
    "transition": {}
  },
  "1071": {
    "type": "createNPC",
    "entityID": [
      40624001,
      40624003
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1072": {
    "type": "createCollection",
    "entityID": [
      40628008
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
      40628008
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
    "type": "createCollection",
    "entityID": [
      40628004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1075
      ]
    }
  },
  "1075": {
    "type": "collBeCollected",
    "entityID": [
      40628004
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1078,
        1077
      ]
    }
  },
  "1077": {
    "type": "removeNPC",
    "entityID": [
      40624001,
      40624003
    ],
    "transition": {}
  },
  "1078": {
    "type": "createNPC",
    "entityID": [
      40624002,
      40624004
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1080
      ]
    }
  },
  "1080": {
    "type": "taskFinished",
    "taskID": 86010527,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1081
      ]
    }
  },
  "1081": {
    "type": "createMonster",
    "entityID": [
      40620001,
      40620002,
      40620003,
      40620004,
      40620005,
      40620006,
      40620007,
      40620008,
      40620009
    ],
    "num": 0,
    "lv": "40",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1082
      ]
    }
  },
  "1082": {
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
        1083
      ]
    }
  },
  "1083": {
    "type": "createCollection",
    "entityID": [
      40628005
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1084
      ]
    }
  },
  "1084": {
    "type": "collBeCollected",
    "entityID": [
      40628005
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1085
      ]
    }
  },
  "1085": {
    "type": "createMonster",
    "entityID": [
      40620010,
      40620011,
      40620012,
      40620013,
      40620014,
      40620015,
      40620016,
      40620017,
      40620018
    ],
    "num": 0,
    "lv": "40",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1086
      ]
    }
  },
  "1086": {
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
        1087
      ]
    }
  },
  "1087": {
    "type": "createCollection",
    "entityID": [
      40628006
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1088
      ]
    }
  },
  "1088": {
    "type": "collBeCollected",
    "entityID": [
      40628006
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1089
      ]
    }
  },
  "1089": {
    "type": "createCollection",
    "entityID": [
      40628007
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1090
      ]
    }
  },
  "1090": {
    "type": "collBeCollected",
    "entityID": [
      40628007
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1091,
        1092
      ]
    }
  },
  "1091": {
    "type": "createNPC",
    "entityID": [
      40624005,
      40624006
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1092": {
    "type": "taskFinished",
    "taskID": 86010534,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1094,
        1093
      ]
    }
  },
  "1093": {
    "type": "removeNPC",
    "entityID": [
      40624005,
      40624006
    ],
    "transition": {}
  },
  "1094": {
    "type": "createMonster",
    "entityID": [
      40620020
    ],
    "num": 0,
    "lv": "40",
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