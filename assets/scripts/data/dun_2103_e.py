datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      21030003,
      21030005,
      21030006,
      21030007,
      21030008,
      21030009,
      21030010,
      21030011,
      21030012
    ],
    "num": 0,
    "lv": "43",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1142
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
        1141
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
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
        1014
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
  "1014": {
    "type": "createMonster",
    "entityID": [
      21030013,
      21030014,
      21030015,
      21030016,
      21030017,
      21030018,
      21030019,
      21030020,
      21030021
    ],
    "num": 0,
    "lv": "43",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        2020
      ]
    }
  },
  "2020": {
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
        1015
      ]
    }
  },
  "1015": {
    "type": "createMonster",
    "entityID": [
      21030023,
      21030024,
      21030025,
      21030026,
      21030027,
      21030028
    ],
    "num": 0,
    "lv": "43",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        2001
      ]
    }
  },
  "2001": {
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
  "2002": {
    "type": "createMonster",
    "entityID": [
      21030029,
      21030030,
      21030031,
      21030032
    ],
    "num": 0,
    "lv": "44",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1808,
        1088
      ]
    }
  },
  "1808": {
    "type": "monsterInBattle",
    "monsterID": [
      21030029
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1087
      ]
    }
  },
  "1086": {
    "type": "createAirWall",
    "entityID": [
      21038003,
      21038004,
      21038005,
      21038006,
      21038007
    ],
    "num": 1,
    "transition": {}
  },
  "1087": {
    "type": "popupdialog",
    "entityID": [
      21030029
    ],
    "dialogID": 19900195,
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
      21030033,
      21030034,
      21030035,
      21030036
    ],
    "num": 0,
    "lv": "44",
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
        1196
      ]
    }
  },
  "1196": {
    "type": "createMonster",
    "entityID": [
      21030037,
      21030038,
      21030039,
      21030040,
      21030041,
      21030042,
      21030043,
      21030044,
      21030045
    ],
    "num": 0,
    "lv": "44",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1099
      ]
    }
  },
  "1099": {
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
        1100
      ]
    }
  },
  "1100": {
    "type": "createMonster",
    "entityID": [
      2030046,
      21030047,
      21030048,
      21030049,
      21030050,
      21030051,
      21030052,
      210300531,
      21030054,
      21030055,
      21030056,
      21030057
    ],
    "num": 0,
    "lv": "44",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1809,
        1811
      ]
    }
  },
  "1809": {
    "type": "monsterRestNum",
    "monsterID": [
      21030046
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1812
      ]
    }
  },
  "1811": {
    "type": "monsterRestNum",
    "monsterID": [
      21030047
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1812
      ]
    }
  },
  "1812": {
    "type": "createMonster",
    "entityID": [
      21030058,
      21030059,
      21030060
    ],
    "num": 0,
    "lv": "44",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1121
      ]
    }
  },
  "1911": {
    "type": "createMonster",
    "entityID": [
      21030061,
      21030062,
      21030063
    ],
    "num": 0,
    "lv": "45",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1912
      ]
    }
  },
  "1912": {
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
        1913
      ]
    }
  },
  "1914": {
    "type": "createMonster",
    "entityID": [
      21030090,
      21030091,
      21030092,
      21030093,
      21030094,
      21030095,
      21030096,
      21030097,
      21030098
    ],
    "num": 0,
    "lv": "46",
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
    "lv": "46",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1011
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
        1911
      ]
    }
  },
  "1913": {
    "type": "createMonster",
    "entityID": [
      21030064,
      21030065,
      21030066
    ],
    "num": 0,
    "lv": "45",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1115
      ]
    }
  },
  "1115": {
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
        1915
      ]
    }
  },
  "1915": {
    "type": "createMonster",
    "entityID": [
      21030067,
      21030068,
      21030069
    ],
    "num": 0,
    "lv": "45",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1116
      ]
    }
  },
  "1116": {
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
        1117
      ]
    }
  },
  "1117": {
    "type": "createMonster",
    "entityID": [
      21030070,
      21030071,
      21030072,
      21030073,
      21030074,
      21030075,
      21030076,
      21030077,
      21030078,
      21030079,
      21030080,
      21030081
    ],
    "num": 0,
    "lv": "46",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1118
      ]
    }
  },
  "1118": {
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
        1119
      ]
    }
  },
  "1119": {
    "type": "createMonster",
    "entityID": [
      21030082,
      21030083,
      21030084,
      21030085,
      21030086,
      21030087,
      21030088,
      21030089
    ],
    "num": 0,
    "lv": "46",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1120
      ]
    }
  },
  "1120": {
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
        1914
      ]
    }
  },
  "1121": {
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
  "1122": {
    "type": "createMonster",
    "entityID": [
      21030001
    ],
    "num": 0,
    "lv": "45",
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
        1114
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
    "dialogID": 19016003,
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
        1006
      ]
    }
  },
  "1132": {
    "type": "popupdialog",
    "entityID": [
      21030001
    ],
    "dialogID": 19016001,
    "transition": {}
  },
  "1134": {
    "type": "popupdialog",
    "entityID": [
      21030001
    ],
    "dialogID": 19016002,
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
    "exitTime": 65.0,
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
    "lv": "44",
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
  "1142": {
    "type": "monsterInBattle",
    "monsterID": [
      21030003
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1143
      ]
    }
  },
  "1143": {
    "type": "popupdialog",
    "entityID": [
      21034004
    ],
    "dialogID": 19900212,
    "transition": {
      "finished": [
        1009
      ]
    }
  }
}