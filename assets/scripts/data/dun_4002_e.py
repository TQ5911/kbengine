datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40020006,
      40020007,
      40020009,
      40020010
    ],
    "num": 1,
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
        1009
      ]
    }
  },
  "1004": {
    "type": "delayLoop",
    "firstDelay": 2400.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1008
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1010,
        1011,
        1012,
        1014,
        1015,
        1016,
        1017,
        1018,
        1019,
        1020,
        1021,
        1058,
        1060,
        1059,
        1061,
        1062,
        1063,
        1004,
        1013
      ]
    }
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 5.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1009": {
    "type": "taskFinished",
    "taskID": 86060061,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1013": {
    "type": "playerRestNum",
    "compare": 1,
    "num": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1008
      ]
    }
  },
  "1024": {
    "type": "createMonster",
    "entityID": [
      40020012,
      40020013,
      40020014,
      40020015,
      40020016,
      40020017
    ],
    "num": 1,
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
        1025
      ]
    }
  },
  "1025": {
    "type": "taskFinished",
    "taskID": 86060003,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1026
      ]
    }
  },
  "1026": {
    "type": "createMonster",
    "entityID": [
      40020019,
      40020020,
      40020021,
      40020022,
      40020023,
      40020024
    ],
    "num": 1,
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
        1027
      ]
    }
  },
  "1027": {
    "type": "taskFinished",
    "taskID": 86060076,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1028
      ]
    }
  },
  "1028": {
    "type": "createMonster",
    "entityID": [
      40020034,
      40020035,
      40020036,
      40020037,
      40020038,
      40020039,
      40020040,
      40020041,
      40020042,
      40020043,
      40020044,
      40020045
    ],
    "num": 1,
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
        1029
      ]
    }
  },
  "1029": {
    "type": "taskFinished",
    "taskID": 86060078,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1030
      ]
    }
  },
  "1030": {
    "type": "createMonster",
    "entityID": [
      40020030,
      40020031,
      40020032,
      40020033
    ],
    "num": 1,
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
        1031
      ]
    }
  },
  "1031": {
    "type": "taskFinished",
    "taskID": 86060089,
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
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052
    ],
    "num": 1,
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
        1033
      ]
    }
  },
  "1033": {
    "type": "taskFinished",
    "taskID": 86060091,
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
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059
    ],
    "num": 1,
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
        1035
      ]
    }
  },
  "1035": {
    "type": "taskFinished",
    "taskID": 86060093,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1036
      ]
    }
  },
  "1036": {
    "type": "createMonster",
    "entityID": [
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066
    ],
    "num": 1,
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
        1037
      ]
    }
  },
  "1037": {
    "type": "taskFinished",
    "taskID": 86060094,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1038
      ]
    }
  },
  "1038": {
    "type": "createMonster",
    "entityID": [
      40020074
    ],
    "num": 1,
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
        1039
      ]
    }
  },
  "1039": {
    "type": "taskFailed",
    "taskID": 86060098,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1040
      ]
    }
  },
  "1040": {
    "type": "createMonster",
    "entityID": [
      40020074
    ],
    "num": 1,
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
        1041
      ]
    }
  },
  "1010": {
    "type": "taskFinished",
    "taskID": 86060055,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1003
      ]
    }
  },
  "1058": {
    "type": "createNPC",
    "entityID": [
      40024001,
      40024002,
      40024003,
      40024004,
      40024005,
      40024006,
      40024007,
      40024008,
      40024009,
      40024010,
      40024011,
      40024012,
      40024013,
      40024014,
      40024015,
      40024016
    ],
    "num": 1,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1059": {
    "type": "createCollection",
    "entityID": [
      40028003,
      40028011,
      40028013,
      40028014,
      40028015,
      40028016,
      40028017,
      40028018,
      40028019
    ],
    "num": 1,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1060": {
    "type": "createAirWall",
    "entityID": [
      40028008,
      40028009,
      40028010
    ],
    "num": 1,
    "transition": {}
  },
  "1061": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64006022
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1062": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64006023
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1063": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64006028
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1011": {
    "type": "taskInProgress",
    "taskID": 86060056,
    "transition": {
      "finished": [
        1003
      ]
    }
  },
  "1012": {
    "type": "taskInProgress",
    "taskID": 86060063,
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1014": {
    "type": "taskInProgress",
    "taskID": 86060067,
    "transition": {
      "finished": [
        1026
      ]
    }
  },
  "1015": {
    "type": "taskInProgress",
    "taskID": 86060078,
    "transition": {
      "finished": [
        1028
      ]
    }
  },
  "1016": {
    "type": "taskInProgress",
    "taskID": 86060080,
    "transition": {
      "finished": [
        1030
      ]
    }
  },
  "1017": {
    "type": "taskInProgress",
    "taskID": 86060090,
    "transition": {
      "finished": [
        1032
      ]
    }
  },
  "1018": {
    "type": "taskInProgress",
    "taskID": 86060092,
    "transition": {
      "finished": [
        1034
      ]
    }
  },
  "1019": {
    "type": "taskInProgress",
    "taskID": 86060094,
    "transition": {
      "finished": [
        1035
      ]
    }
  },
  "1020": {
    "type": "taskInProgress",
    "taskID": 86060098,
    "transition": {
      "finished": [
        1038
      ]
    }
  },
  "1041": {
    "type": "taskFinished",
    "taskID": 86060101,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1043,
        1042,
        1044,
        1005
      ]
    }
  },
  "1021": {
    "type": "taskInProgress",
    "taskID": 86060100,
    "transition": {
      "finished": [
        1040
      ]
    }
  },
  "1042": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006022
    ],
    "transition": {}
  },
  "1043": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006023
    ],
    "transition": {}
  },
  "1044": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006028
    ],
    "transition": {}
  }
}