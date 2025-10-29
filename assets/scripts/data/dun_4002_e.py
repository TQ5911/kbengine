datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40020006,
      40020007
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
        1018
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
        1017,
        1012,
        1014,
        1015,
        1016,
        1022,
        1023,
        1045,
        1046,
        1057,
        1058,
        1060,
        1059,
        1064,
        1061,
        1062,
        1063,
        1004,
        1013,
        1041
      ]
    }
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
      40020017,
      40020075,
      40020076
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
      40020024,
      40020077,
      40020078
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
        1035
      ]
    }
  },
  "1036": {
    "type": "createMonster",
    "entityID": [
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052,
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059,
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066,
      40020067,
      40020068,
      40020069,
      40020070,
      40020071,
      40020072,
      40020073
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
    "transition": {}
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
        1047,
        1048,
        1049
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
      40024016,
      40024017,
      40024018,
      40024019,
      40024020,
      40024021,
      40024022,
      40024023
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
      40028012,
      40028013,
      40028014,
      40028015
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
        1055,
        1054
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
  },
  "1022": {
    "type": "collBeCollected",
    "entityID": [
      40028015
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1066
      ]
    }
  },
  "1023": {
    "type": "collBeCollected",
    "entityID": [
      40028012
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1039
      ]
    }
  },
  "1045": {
    "type": "collBeCollected",
    "entityID": [
      40028013
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1065
      ]
    }
  },
  "1046": {
    "type": "taskFinished",
    "taskID": 86060089,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1038,
        1037
      ]
    }
  },
  "1047": {
    "type": "dunAnyPlayerHP",
    "compare": 2,
    "hpPercent": 15.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1033
      ]
    }
  },
  "1048": {
    "type": "monsterHp",
    "monsterID": [
      40020074
    ],
    "compare": 2,
    "hpPercent": 60.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1033
      ]
    }
  },
  "1049": {
    "type": "delayLoop",
    "firstDelay": 60.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1033
      ]
    }
  },
  "1033": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1051,
        1052,
        1050,
        1053
      ]
    }
  },
  "1051": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98000001,
    "transition": {}
  },
  "1050": {
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
    "transition": {}
  },
  "1052": {
    "type": "removeMonster",
    "entityID": [
      40020074
    ],
    "transition": {}
  },
  "1053": {
    "type": "taskUndertake",
    "taskID": 86060090,
    "transition": {}
  },
  "1055": {
    "type": "delayLoop",
    "firstDelay": 5.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1056
      ]
    }
  },
  "1056": {
    "type": "transferToTheDesignatedMap",
    "mapId": 4001,
    "posX": 172.0,
    "posY": 63.0,
    "posZ": 107.0,
    "angle": 297,
    "transition": {}
  },
  "1054": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98000035,
    "transition": {}
  },
  "1064": {
    "type": "createRebornPos",
    "entityID": [
      40028001,
      40028022
    ],
    "num": 1,
    "transition": {}
  },
  "1017": {
    "type": "taskInProgress",
    "taskID": 86060103,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1005": {
    "type": "createMonster",
    "entityID": [
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
  "1018": {
    "type": "taskFinished",
    "taskID": 86060056,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1035": {
    "type": "taskFinished",
    "taskID": 86060088,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1036
      ]
    }
  },
  "1057": {
    "type": "collBeCollected",
    "entityID": [
      40028014
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1040
      ]
    }
  },
  "1037": {
    "type": "removeMonster",
    "entityID": [
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052,
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059,
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066,
      40020067,
      40020068,
      40020069,
      40020070,
      40020071,
      40020072,
      40020073
    ],
    "transition": {}
  },
  "1039": {
    "type": "removeMonster",
    "entityID": [
      40024020
    ],
    "transition": {}
  },
  "1040": {
    "type": "removeMonster",
    "entityID": [
      40024022
    ],
    "transition": {}
  },
  "1065": {
    "type": "removeMonster",
    "entityID": [
      40024021
    ],
    "transition": {}
  },
  "1066": {
    "type": "removeMonster",
    "entityID": [
      40024023
    ],
    "transition": {}
  }
}