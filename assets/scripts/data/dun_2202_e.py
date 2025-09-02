datas ={
  "1004": {
    "type": "delayLoop",
    "firstDelay": 1800.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1004,
        1002,
        1013
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
        1024
      ]
    }
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      22020001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1016,
        1201,
        1202,
        1092,
        1022
      ]
    }
  },
  "1002": {
    "type": "createMonster",
    "entityID": [
      22020002
    ],
    "num": 1,
    "lv": "38",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1014
      ]
    }
  },
  "1015": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004938
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1009
      ]
    }
  },
  "1014": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1016": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004938
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1017,
        1101,
        1162,
        1037,
        1121,
        1168,
        1171,
        1139,
        1006
      ]
    }
  },
  "1201": {
    "type": "delayLoop",
    "firstDelay": 60.0,
    "loopDelay": 120.0,
    "loopNum": 15,
    "transition": {
      "loop": [
        1203
      ]
    }
  },
  "1202": {
    "type": "delayLoop",
    "firstDelay": 120.0,
    "loopDelay": 120.0,
    "loopNum": 15,
    "transition": {
      "loop": [
        1204
      ]
    }
  },
  "1203": {
    "type": "castSkill",
    "entityID": [
      22020001
    ],
    "skillID": 91023020,
    "lv": "-1",
    "forceToUse": -1,
    "transition": {
      "finished": [
        1205
      ]
    }
  },
  "1204": {
    "type": "castSkill",
    "entityID": [
      20180002
    ],
    "skillID": 91024014,
    "lv": "-1",
    "forceToUse": -1,
    "transition": {
      "finished": [
        1206
      ]
    }
  },
  "1205": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      22020001
    ],
    "entityID": [
      22028003
    ],
    "num": 1,
    "transition": {}
  },
  "1206": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      20180002
    ],
    "entityID": [
      22028004
    ],
    "num": 1,
    "transition": {}
  },
  "1003": {
    "type": "createMonster",
    "entityID": [
      22020001
    ],
    "num": 1,
    "lv": "38",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1015
      ]
    }
  },
  "1092": {
    "type": "popupdialog",
    "entityID": [
      22020001
    ],
    "dialogID": 19018001,
    "transition": {}
  },
  "1022": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 15.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      22020001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1012
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      22020001
    ],
    "dialogID": 19018013,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1017": {
    "type": "monsterHp",
    "monsterID": [
      22020001
    ],
    "compare": 5,
    "hpPercent": 80.1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1018,
        1019
      ]
    }
  },
  "1021": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1012": {
    "type": "monsterRestNum",
    "monsterID": [
      22020002
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1155
      ]
    }
  },
  "1018": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004943
    ],
    "transition": {}
  },
  "1019": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "transition": {
      "finished": [
        1020
      ]
    }
  },
  "1020": {
    "type": "castSkill",
    "entityID": [
      22020002
    ],
    "skillID": 91024013,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1021,
        1057,
        1080
      ]
    }
  },
  "1057": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004938
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1060
      ]
    }
  },
  "1060": {
    "type": "monsterHp",
    "monsterID": [
      22020002
    ],
    "compare": 5,
    "hpPercent": 80.1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1061,
        1027
      ]
    }
  },
  "1061": {
    "type": "castSkill",
    "entityID": [
      22020001
    ],
    "skillID": 91023019,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1025,
        1081
      ]
    }
  },
  "1025": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1026
      ]
    }
  },
  "1026": {
    "type": "castSkill",
    "entityID": [
      22020001
    ],
    "skillID": 91023017,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1028,
        1031
      ]
    }
  },
  "1027": {
    "type": "castSkill",
    "entityID": [
      22020002
    ],
    "skillID": 91024011,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1034,
        1035
      ]
    }
  },
  "1028": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004944
    ],
    "transition": {
      "finished": [
        1030
      ]
    }
  },
  "1029": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004927
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1030": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004925
    ],
    "transition": {
      "finished": [
        1029
      ]
    }
  },
  "1033": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004927
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1034": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004925
    ],
    "transition": {
      "finished": [
        1033
      ]
    }
  },
  "1031": {
    "type": "delayLoop",
    "firstDelay": 11.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1032,
        1082
      ]
    }
  },
  "1032": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1035": {
    "type": "delayLoop",
    "firstDelay": 11.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1036
      ]
    }
  },
  "1036": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1101": {
    "type": "monsterHp",
    "monsterID": [
      22020001
    ],
    "compare": 5,
    "hpPercent": 60.1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1161,
        1102
      ]
    }
  },
  "1102": {
    "type": "monsterHp",
    "monsterID": [
      22020002
    ],
    "compare": 5,
    "hpPercent": 60.1,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1151
      ]
    }
  },
  "1103": {
    "type": "castSkill",
    "entityID": [
      22020001
    ],
    "skillID": 91023019,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1104,
        1106,
        1083
      ]
    }
  },
  "1105": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004929
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1107
      ]
    }
  },
  "1106": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004927
    ],
    "transition": {
      "finished": [
        1105
      ]
    }
  },
  "1108": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004929
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1119
      ]
    }
  },
  "1109": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004927
    ],
    "transition": {
      "finished": [
        1108
      ]
    }
  },
  "1107": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004939
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1119": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004943
    ],
    "transition": {}
  },
  "1037": {
    "type": "monsterHp",
    "monsterID": [
      22020001
    ],
    "compare": 5,
    "hpPercent": 40.1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1039,
        1040
      ]
    }
  },
  "1038": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1039": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004943
    ],
    "transition": {}
  },
  "1040": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "transition": {
      "finished": [
        1041
      ]
    }
  },
  "1041": {
    "type": "castSkill",
    "entityID": [
      22020002
    ],
    "skillID": 91024013,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1038,
        1042,
        1084
      ]
    }
  },
  "1042": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004939
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1043
      ]
    }
  },
  "1043": {
    "type": "monsterHp",
    "monsterID": [
      22020002
    ],
    "compare": 5,
    "hpPercent": 40.1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1044,
        1047
      ]
    }
  },
  "1044": {
    "type": "castSkill",
    "entityID": [
      22020001
    ],
    "skillID": 91023019,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1045,
        1085
      ]
    }
  },
  "1045": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1046
      ]
    }
  },
  "1046": {
    "type": "castSkill",
    "entityID": [
      22020001
    ],
    "skillID": 91023017,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1048,
        1053
      ]
    }
  },
  "1047": {
    "type": "castSkill",
    "entityID": [
      22020002
    ],
    "skillID": 91024011,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1052,
        1055
      ]
    }
  },
  "1048": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004945
    ],
    "transition": {
      "finished": [
        1050
      ]
    }
  },
  "1049": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004931
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1050": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004929
    ],
    "transition": {
      "finished": [
        1049
      ]
    }
  },
  "1051": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004931
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1052": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004929
    ],
    "transition": {
      "finished": [
        1051
      ]
    }
  },
  "1053": {
    "type": "delayLoop",
    "firstDelay": 11.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1054,
        1086
      ]
    }
  },
  "1054": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1055": {
    "type": "delayLoop",
    "firstDelay": 11.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1056
      ]
    }
  },
  "1056": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1121": {
    "type": "monsterHp",
    "monsterID": [
      22020001
    ],
    "compare": 5,
    "hpPercent": 20.1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1170,
        1122
      ]
    }
  },
  "1122": {
    "type": "monsterHp",
    "monsterID": [
      22020002
    ],
    "compare": 5,
    "hpPercent": 20.1,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1153
      ]
    }
  },
  "1123": {
    "type": "castSkill",
    "entityID": [
      22020001
    ],
    "skillID": 91023019,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1126,
        1087
      ]
    }
  },
  "1125": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004950
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1132
      ]
    }
  },
  "1126": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004931
    ],
    "transition": {
      "finished": [
        1125
      ]
    }
  },
  "1129": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004940
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1127": {
    "type": "castSkill",
    "entityID": [
      22020002
    ],
    "skillID": 91024013,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1131
      ]
    }
  },
  "1130": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004950
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1137
      ]
    }
  },
  "1131": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004931
    ],
    "transition": {
      "finished": [
        1130
      ]
    }
  },
  "1137": {
    "type": "castSkill",
    "entityID": [
      22020002
    ],
    "skillID": 91024008,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1135,
        1136
      ]
    }
  },
  "1132": {
    "type": "castSkill",
    "entityID": [
      22020001
    ],
    "skillID": 91023014,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1129,
        1133
      ]
    }
  },
  "1133": {
    "type": "delayLoop",
    "firstDelay": 11.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1134,
        1088
      ]
    }
  },
  "1134": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1135": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004940
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1136": {
    "type": "delayLoop",
    "firstDelay": 11.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1138
      ]
    }
  },
  "1138": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1139": {
    "type": "monsterHp",
    "monsterID": [
      22020001
    ],
    "compare": 5,
    "hpPercent": 0.01,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1140,
        1173,
        1091
      ]
    }
  },
  "1140": {
    "type": "monsterHp",
    "monsterID": [
      22020002
    ],
    "compare": 5,
    "hpPercent": 0.01,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1154
      ]
    }
  },
  "1141": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004950
    ],
    "transition": {
      "finished": [
        1175
      ]
    }
  },
  "1142": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004950
    ],
    "transition": {
      "finished": [
        1176
      ]
    }
  },
  "1151": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1103,
        1109
      ]
    }
  },
  "1153": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1123,
        1127
      ]
    }
  },
  "1154": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1141,
        1142
      ]
    }
  },
  "1155": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1011,
        1156,
        1157,
        1023
      ]
    }
  },
  "1156": {
    "type": "stopDelayEvent",
    "eventID": [
      1201
    ],
    "transition": {}
  },
  "1157": {
    "type": "stopDelayEvent",
    "eventID": [
      1202
    ],
    "transition": {}
  },
  "1161": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1162": {
    "type": "monsterHp",
    "monsterID": [
      22020002
    ],
    "compare": 5,
    "hpPercent": 60.1,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1163
      ]
    }
  },
  "1163": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1104": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1168": {
    "type": "monsterHp",
    "monsterID": [
      22020002
    ],
    "compare": 5,
    "hpPercent": 20.1,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1169
      ]
    }
  },
  "1169": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1170": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1171": {
    "type": "monsterHp",
    "monsterID": [
      22020002
    ],
    "compare": 5,
    "hpPercent": 0.01,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1174,
        1172,
        1089
      ]
    }
  },
  "1172": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1173": {
    "type": "addBuffToMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1174": {
    "type": "monsterHp",
    "monsterID": [
      20180001
    ],
    "compare": 5,
    "hpPercent": 0.01,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1154
      ]
    }
  },
  "1176": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020002
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1175": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22020001
    ],
    "buffID": [
      64004964
    ],
    "transition": {}
  },
  "1080": {
    "type": "popupdialog",
    "entityID": [
      22020002
    ],
    "dialogID": 19018002,
    "transition": {}
  },
  "1081": {
    "type": "popupdialog",
    "entityID": [
      22020001
    ],
    "dialogID": 19018003,
    "transition": {}
  },
  "1082": {
    "type": "popupdialog",
    "entityID": [
      22020002
    ],
    "dialogID": 19018004,
    "transition": {}
  },
  "1083": {
    "type": "popupdialog",
    "entityID": [
      22020001
    ],
    "dialogID": 19018005,
    "transition": {}
  },
  "1084": {
    "type": "popupdialog",
    "entityID": [
      22020002
    ],
    "dialogID": 19018006,
    "transition": {}
  },
  "1085": {
    "type": "popupdialog",
    "entityID": [
      22020001
    ],
    "dialogID": 19018007,
    "transition": {}
  },
  "1086": {
    "type": "popupdialog",
    "entityID": [
      22020002
    ],
    "dialogID": 19018008,
    "transition": {}
  },
  "1087": {
    "type": "popupdialog",
    "entityID": [
      22020001
    ],
    "dialogID": 19018009,
    "transition": {}
  },
  "1088": {
    "type": "popupdialog",
    "entityID": [
      22020002
    ],
    "dialogID": 19018010,
    "transition": {}
  },
  "1089": {
    "type": "popupdialog",
    "entityID": [
      22020001
    ],
    "dialogID": 19018011,
    "transition": {}
  },
  "1091": {
    "type": "popupdialog",
    "entityID": [
      22020002
    ],
    "dialogID": 19018012,
    "transition": {}
  },
  "1023": {
    "type": "popupdialog",
    "entityID": [
      22020002
    ],
    "dialogID": 19018014,
    "transition": {}
  },
  "1024": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  }
}