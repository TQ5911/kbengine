datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      21030103,
      21030104,
      21030105,
      21030106,
      21030107,
      21030108,
      21030109,
      21030110,
      21030111,
      21030112,
      21030113,
      21030114,
      21030115,
      21030116,
      21030117,
      21030118,
      21030119,
      21030120,
      21030121,
      21030122,
      21030123,
      21030124,
      21030125,
      21030126,
      21030127,
      21030128,
      21030129,
      21030130,
      21030131,
      21030132
    ],
    "num": 0,
    "lv": "50",
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
    "firstDelay": 1800.0,
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
        1003,
        1004,
        1013,
        1086,
        1141,
        1150
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 30.0,
    "transition": {}
  },
  "1009": {
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
        2002
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
  "2002": {
    "type": "createMonster",
    "entityID": [
      21030133
    ],
    "num": 0,
    "lv": "50",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1088
      ]
    }
  },
  "1086": {
    "type": "createAirWall",
    "entityID": [
      21038006,
      21038007
    ],
    "num": 1,
    "transition": {}
  },
  "1088": {
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
        1089,
        1090
      ]
    }
  },
  "1089": {
    "type": "removeAirWall",
    "entityID": [
      21038006
    ],
    "transition": {}
  },
  "1090": {
    "type": "createMonster",
    "entityID": [
      21030134,
      21030135,
      21030136,
      21030137,
      21030138,
      21030139,
      21030140,
      21030141,
      21030142,
      21030143,
      21030144,
      21030145,
      21030146,
      21030147,
      21030148,
      21030149,
      21030150,
      21030151,
      21030152,
      21030153,
      21030154,
      21030155,
      21030156,
      21030157,
      21030158,
      21030159,
      21030160,
      21030161,
      21030162,
      21030163
    ],
    "num": 0,
    "lv": "50",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1095
      ]
    }
  },
  "1095": {
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
        1122
      ]
    }
  },
  "1911": {
    "type": "createMonster",
    "entityID": [
      21030164,
      21030165,
      21030166,
      21030167,
      21030168,
      21030169,
      21030170,
      21030171,
      21030172,
      21030173,
      21030174,
      21030175,
      21030176,
      21030177,
      21030178,
      21030179,
      21030180,
      21030181,
      21030182,
      21030183,
      21030184,
      21030185,
      21030186,
      21030187,
      21030188,
      21030189,
      21030190,
      21030191,
      21030192,
      21030193
    ],
    "num": 0,
    "lv": "50",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1916
      ]
    }
  },
  "1916": {
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
        1133
      ]
    }
  },
  "1133": {
    "type": "createMonster",
    "entityID": [
      21030002
    ],
    "num": 1,
    "lv": "52",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1011,
        1006
      ]
    }
  },
  "1830": {
    "type": "removeAirWall",
    "entityID": [
      21038007
    ],
    "transition": {}
  },
  "1114": {
    "type": "monsterRestNum",
    "monsterID": [
      21030001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1830,
        1912
      ]
    }
  },
  "1122": {
    "type": "createMonster",
    "entityID": [
      21030001
    ],
    "num": 0,
    "lv": "51",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1181,
        1114,
        1151
      ]
    }
  },
  "1185": {
    "type": "monsterRestNum",
    "monsterID": [
      21030001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1186
      ]
    }
  },
  "1181": {
    "type": "monsterInBattle",
    "monsterID": [
      21030001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1183,
        1132
      ]
    }
  },
  "1186": {
    "type": "popupdialog",
    "entityID": [
      21030001
    ],
    "dialogID": 19104009,
    "transition": {}
  },
  "1183": {
    "type": "monsterHp",
    "monsterID": [
      21030001
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1134,
        1184
      ]
    }
  },
  "1184": {
    "type": "addBuffToMonster",
    "monsterID": [
      21030001
    ],
    "buffID": [
      64004905
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1185
      ]
    }
  },
  "1011": {
    "type": "monsterInBattle",
    "monsterID": [
      21030002
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1021,
        1135,
        1031,
        1051,
        1155
      ]
    }
  },
  "1132": {
    "type": "popupdialog",
    "entityID": [
      21030001
    ],
    "dialogID": 19104007,
    "transition": {}
  },
  "1134": {
    "type": "popupdialog",
    "entityID": [
      21030001
    ],
    "dialogID": 19104008,
    "transition": {}
  },
  "1135": {
    "type": "popupdialog",
    "entityID": [
      21030001
    ],
    "dialogID": 19016003,
    "transition": {}
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 30.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      21030002
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1012
      ]
    }
  },
  "1012": {
    "type": "popupdialog",
    "entityID": [
      21030002
    ],
    "dialogID": 19015005,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1021": {
    "type": "monsterHp",
    "monsterID": [
      21030002
    ],
    "compare": 5,
    "hpPercent": 75.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1026,
        1999
      ]
    }
  },
  "1023": {
    "type": "castSkill",
    "entityID": [
      21030002
    ],
    "skillID": 91015007,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1028
      ]
    }
  },
  "1031": {
    "type": "monsterHp",
    "monsterID": [
      21030002
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1998,
        1025
      ]
    }
  },
  "1033": {
    "type": "createMonster",
    "entityID": [
      21030099,
      21030100,
      21030101,
      21030102
    ],
    "num": 1,
    "lv": "50",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1035,
        1041
      ]
    }
  },
  "1034": {
    "type": "addBuffToMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004010
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1033,
        1146
      ]
    }
  },
  "1041": {
    "type": "killMonsterNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "killNum": 4,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1042
      ]
    }
  },
  "1042": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004010
    ],
    "transition": {
      "finished": [
        1043
      ]
    }
  },
  "1035": {
    "type": "delayLoop",
    "firstDelay": 0.0,
    "loopDelay": 5.0,
    "loopNum": 4,
    "transition": {
      "loop": [
        1036
      ]
    }
  },
  "1036": {
    "type": "castSkill",
    "entityID": [
      21030002
    ],
    "skillID": 91015010,
    "lv": "1",
    "forceToUse": 1,
    "transition": {}
  },
  "1043": {
    "type": "stopDelayEvent",
    "eventID": [
      1035
    ],
    "transition": {
      "finished": [
        1044
      ]
    }
  },
  "1044": {
    "type": "stopDelayEvent",
    "eventID": [
      1036
    ],
    "transition": {}
  },
  "1051": {
    "type": "monsterHp",
    "monsterID": [
      21030002
    ],
    "compare": 5,
    "hpPercent": 25.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1027,
        1140
      ]
    }
  },
  "1053": {
    "type": "castSkill",
    "entityID": [
      21030002
    ],
    "skillID": 91015011,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1056
      ]
    }
  },
  "1054": {
    "type": "removeCreation",
    "monsterID": [
      21030002
    ],
    "range": 100.0,
    "creationID": [
      66000005
    ],
    "transition": {
      "finished": [
        1053
      ]
    }
  },
  "1025": {
    "type": "addBuffToMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004905
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1034
      ]
    }
  },
  "1026": {
    "type": "addBuffToMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004010
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1023
      ]
    }
  },
  "1027": {
    "type": "addBuffToMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004010
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1054
      ]
    }
  },
  "1028": {
    "type": "delayLoop",
    "firstDelay": 8.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1029
      ]
    }
  },
  "1029": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004010
    ],
    "transition": {}
  },
  "1056": {
    "type": "delayLoop",
    "firstDelay": 15.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1057
      ]
    }
  },
  "1057": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004010
    ],
    "transition": {}
  },
  "1146": {
    "type": "delayLoop",
    "firstDelay": 20.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1909
      ]
    }
  },
  "1909": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004010
    ],
    "transition": {}
  },
  "1999": {
    "type": "popupdialog",
    "entityID": [
      21030002
    ],
    "dialogID": 19015002,
    "transition": {}
  },
  "1998": {
    "type": "popupdialog",
    "entityID": [
      21030002
    ],
    "dialogID": 19015003,
    "transition": {}
  },
  "1140": {
    "type": "popupdialog",
    "entityID": [
      21030002
    ],
    "dialogID": 19015004,
    "transition": {}
  },
  "1141": {
    "type": "createNPC",
    "entityID": [
      21034001,
      21034002,
      21034003,
      21034004
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1150": {
    "type": "createRebornPos",
    "entityID": [
      21038002
    ],
    "num": 1,
    "transition": {}
  },
  "1151": {
    "type": "removeRebornPos",
    "entityID": [
      21038002
    ],
    "transition": {
      "finished": [
        1152
      ]
    }
  },
  "1152": {
    "type": "createRebornPos",
    "entityID": [
      21038008
    ],
    "num": 1,
    "transition": {}
  },
  "1155": {
    "type": "removeRebornPos",
    "entityID": [
      21038008
    ],
    "transition": {
      "finished": [
        1153
      ]
    }
  },
  "1153": {
    "type": "createRebornPos",
    "entityID": [
      21038009
    ],
    "num": 1,
    "transition": {}
  },
  "1912": {
    "type": "createMonster",
    "entityID": [
      21030194,
      21030195,
      21030196,
      21030197,
      21030198,
      21030199,
      21030200,
      21030201,
      21030202,
      21030203,
      21030204,
      21030205,
      21030206,
      21030207,
      21030208,
      21030209,
      21030210,
      21030211
    ],
    "num": 0,
    "lv": "50",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1154
      ]
    }
  },
  "1154": {
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
        1911
      ]
    }
  }
}