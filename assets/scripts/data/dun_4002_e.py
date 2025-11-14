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
        1035,
        1046,
        1031,
        1034,
        1070,
        1095,
        1094,
        1066,
        1065,
        1058,
        1060,
        1059,
        1064,
        1087,
        1088,
        1061,
        1062,
        1063,
        1090,
        1057,
        1096,
        1097,
        1098,
        1093,
        1103,
        1105,
        1041,
        1108,
        1013,
        1004
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
    "taskID": 86060128,
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
    "transition": {}
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
        1073
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
      40024024,
      40024025,
      40024026,
      40024027
    ],
    "num": 1,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1059": {
    "type": "createCollection",
    "entityID": [
      40028003
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
      40028010,
      40028023,
      40028028,
      40028029,
      40028030
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
  "1046": {
    "type": "taskFinished",
    "taskID": 86060087,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1038,
        1037,
        1068
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
        1052,
        1107
      ]
    }
  },
  "1050": {
    "type": "createMonster",
    "entityID": [
      40020085
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
      40028001
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
    "taskID": 86060127,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1036,
        1072,
        1074,
        1075,
        1089
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
  "1067": {
    "type": "createMonster",
    "entityID": [
      40020079,
      40020080,
      40020081,
      40020082,
      40020083,
      40020084
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
  "1068": {
    "type": "createRebornPos",
    "entityID": [
      40028022
    ],
    "num": 1,
    "transition": {}
  },
  "1031": {
    "type": "taskFinished",
    "taskID": 86060051,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1032
      ]
    }
  },
  "1032": {
    "type": "createCollection",
    "entityID": [
      40028011
    ],
    "num": 1,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1034": {
    "type": "taskFinished",
    "taskID": 86060051,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1069
      ]
    }
  },
  "1069": {
    "type": "removeNPC",
    "entityID": [
      40024025
    ],
    "transition": {}
  },
  "1070": {
    "type": "taskFinished",
    "taskID": 86060053,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1071
      ]
    }
  },
  "1071": {
    "type": "removeAirWall",
    "entityID": [
      40028023
    ],
    "transition": {}
  },
  "1072": {
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
        1076
      ]
    }
  },
  "1073": {
    "type": "stopAiTick",
    "entityID": [
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052
    ],
    "transition": {
      "finished": [
        1079
      ]
    }
  },
  "1074": {
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
        1077
      ]
    }
  },
  "1075": {
    "type": "createMonster",
    "entityID": [
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
    "transition": {
      "finished": [
        1078
      ]
    }
  },
  "1076": {
    "type": "stopAiTick",
    "entityID": [
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059
    ],
    "transition": {
      "finished": [
        1081
      ]
    }
  },
  "1077": {
    "type": "stopAiTick",
    "entityID": [
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066
    ],
    "transition": {
      "finished": [
        1083
      ]
    }
  },
  "1078": {
    "type": "stopAiTick",
    "entityID": [
      40020067,
      40020068,
      40020069,
      40020070,
      40020071,
      40020072,
      40020073
    ],
    "transition": {
      "finished": [
        1085
      ]
    }
  },
  "1079": {
    "type": "taskFinished",
    "taskID": 86060121,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1080
      ]
    }
  },
  "1080": {
    "type": "startAiTick",
    "entityID": [
      40020046,
      40020047,
      40020048,
      40020049,
      40020050,
      40020051,
      40020052
    ],
    "transition": {}
  },
  "1081": {
    "type": "taskFinished",
    "taskID": 86060089,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1082
      ]
    }
  },
  "1082": {
    "type": "startAiTick",
    "entityID": [
      40020053,
      40020054,
      40020055,
      40020056,
      40020057,
      40020058,
      40020059
    ],
    "transition": {}
  },
  "1083": {
    "type": "taskFinished",
    "taskID": 86060124,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1084
      ]
    }
  },
  "1084": {
    "type": "startAiTick",
    "entityID": [
      40020060,
      40020061,
      40020062,
      40020063,
      40020064,
      40020065,
      40020066
    ],
    "transition": {}
  },
  "1085": {
    "type": "taskFinished",
    "taskID": 86060118,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1086
      ]
    }
  },
  "1086": {
    "type": "startAiTick",
    "entityID": [
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
  "1087": {
    "type": "taskFinished",
    "taskID": 86060083,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1067
      ]
    }
  },
  "1088": {
    "type": "taskInProgress",
    "taskID": 86060085,
    "transition": {
      "finished": [
        1067
      ]
    }
  },
  "1089": {
    "type": "removeMonster",
    "entityID": [
      40020079,
      40020080,
      40020081,
      40020082,
      40020083,
      40020084
    ],
    "transition": {}
  },
  "1065": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      -1
    ],
    "entityID": [
      40028024
    ],
    "num": 1,
    "transition": {}
  },
  "1066": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      -1
    ],
    "entityID": [
      40028025
    ],
    "num": 1,
    "transition": {}
  },
  "1094": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      -1
    ],
    "entityID": [
      40028026
    ],
    "num": 1,
    "transition": {}
  },
  "1095": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      -1
    ],
    "entityID": [
      40028027
    ],
    "num": 1,
    "transition": {}
  },
  "1057": {
    "type": "taskFinished",
    "taskID": 86060122,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1099
      ]
    }
  },
  "1096": {
    "type": "taskFinished",
    "taskID": 86060116,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1100
      ]
    }
  },
  "1097": {
    "type": "taskFinished",
    "taskID": 86060125,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1101
      ]
    }
  },
  "1098": {
    "type": "taskFinished",
    "taskID": 86060119,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1102
      ]
    }
  },
  "1099": {
    "type": "removeNoHostCreation",
    "entityID": [
      40028026
    ],
    "usePrototypeID": 0,
    "transition": {}
  },
  "1100": {
    "type": "removeNoHostCreation",
    "entityID": [
      40028024
    ],
    "usePrototypeID": 0,
    "transition": {}
  },
  "1101": {
    "type": "removeNoHostCreation",
    "entityID": [
      40028027
    ],
    "usePrototypeID": 0,
    "transition": {}
  },
  "1102": {
    "type": "removeNoHostCreation",
    "entityID": [
      40028025
    ],
    "usePrototypeID": 0,
    "transition": {}
  },
  "1090": {
    "type": "taskFinished",
    "taskID": 86060127,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1091
      ]
    }
  },
  "1091": {
    "type": "createAirWall",
    "entityID": [
      40028031
    ],
    "num": 1,
    "transition": {}
  },
  "1093": {
    "type": "taskFinished",
    "taskID": 86060103,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1092
      ]
    }
  },
  "1092": {
    "type": "removeAirWall",
    "entityID": [
      40028028
    ],
    "transition": {}
  },
  "1103": {
    "type": "taskFinished",
    "taskID": 86060063,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1104
      ]
    }
  },
  "1104": {
    "type": "removeAirWall",
    "entityID": [
      40028029
    ],
    "transition": {}
  },
  "1105": {
    "type": "taskFinished",
    "taskID": 86060067,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1106
      ]
    }
  },
  "1106": {
    "type": "removeAirWall",
    "entityID": [
      40028030
    ],
    "transition": {}
  },
  "1107": {
    "type": "dungeonTaskForceComplete",
    "taskID": 86060098,
    "transition": {}
  },
  "1108": {
    "type": "taskFinished",
    "taskID": 86060098,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1050,
        1109,
        1110,
        1111
      ]
    }
  },
  "1109": {
    "type": "taskUndertake",
    "taskID": 86060129,
    "transition": {}
  },
  "1110": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98000001,
    "transition": {}
  },
  "1111": {
    "type": "taskUndertake",
    "taskID": 86060090,
    "transition": {}
  }
}