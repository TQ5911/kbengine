datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      21040004,
      21040005,
      21040006,
      21040007,
      21040008,
      21040009,
      21040010,
      21040011,
      21040012,
      21040013,
      21040014,
      21040015,
      21040016,
      21040017,
      21040018,
      21040019,
      21040020,
      21040021,
      21040022,
      21040023,
      21040024,
      21040025,
      21040026,
      21040027
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
        1157
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
        1015
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
  "1015": {
    "type": "createMonster",
    "entityID": [
      21040028,
      21040029,
      21040030,
      21040031,
      21040032,
      21040033,
      21040034,
      21040035,
      21040036,
      21040037,
      21040038,
      21040039,
      21040040,
      21040041,
      21040042,
      21040043,
      21040044,
      21040045,
      21040046,
      21040047,
      21040048,
      21040049,
      21040050,
      21040051
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
      21040003
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
        1808,
        1088
      ]
    }
  },
  "1808": {
    "type": "monsterInBattle",
    "monsterID": [
      21040003
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
      21048004,
      21048005,
      21048006,
      21048007,
      21048008,
      21048009,
      21048012
    ],
    "num": 1,
    "transition": {}
  },
  "1087": {
    "type": "popupdialog",
    "entityID": [
      21040003
    ],
    "dialogID": 19900199,
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
        1090
      ]
    }
  },
  "1090": {
    "type": "createMonster",
    "entityID": [
      21040052,
      21040053,
      21040054,
      21040055,
      21040056,
      21040057,
      21040058
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
      21040059,
      21040061,
      21040062,
      21040063,
      21040064,
      21040065,
      21040066,
      21040067,
      21040068,
      21040069,
      21040070,
      21040071,
      21040072,
      21040073,
      21040074
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
      21040075,
      21040076,
      21040077,
      21040078,
      21040079,
      21040080,
      21040081,
      21040082,
      21040083,
      21040084
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
        1809
      ]
    }
  },
  "1809": {
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
        1812
      ]
    }
  },
  "1812": {
    "type": "createMonster",
    "entityID": [
      21040001
    ],
    "num": 0,
    "lv": "40",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1146,
        1181
      ]
    }
  },
  "1911": {
    "type": "createMonster",
    "entityID": [
      21040085,
      21040086,
      21040087,
      21040088,
      21040089,
      21040090
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
  "1913": {
    "type": "createMonster",
    "entityID": [
      21040091,
      21040092,
      21040093,
      21040094,
      21040095,
      21040096
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
      21040097,
      21040098,
      21040099,
      21040100,
      21040101,
      21040102,
      21040103,
      21040104,
      21040105,
      21040106
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
      21040107,
      21040108,
      21040109,
      21040110,
      21040111,
      21040112,
      21040113,
      21040114,
      21040115,
      21040116,
      21040117,
      21040118,
      21040119,
      21040120,
      21040121
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
      21040002
    ],
    "num": 0,
    "lv": "40",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1120,
        1153
      ]
    }
  },
  "1120": {
    "type": "monsterRestNum",
    "monsterID": [
      21040002
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1169
      ]
    }
  },
  "1141": {
    "type": "createNPC",
    "entityID": [
      21044001,
      21044002,
      21044003,
      21044004
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1146": {
    "type": "monsterInBattle",
    "monsterID": [
      21040001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1147,
        1148,
        1149,
        1156,
        1164
      ]
    }
  },
  "1147": {
    "type": "popupdialog",
    "entityID": [
      21040001
    ],
    "dialogID": 19104001,
    "transition": {}
  },
  "1148": {
    "type": "createRebornPos",
    "entityID": [
      21048010
    ],
    "num": 1,
    "transition": {}
  },
  "1149": {
    "type": "createNPC",
    "entityID": [
      21044005,
      21044006,
      21044007,
      21044008
    ],
    "num": 1,
    "lv": "46",
    "ifSetBoss": 1,
    "transition": {}
  },
  "1181": {
    "type": "monsterRestNum",
    "monsterID": [
      21040001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1911,
        1166
      ]
    }
  },
  "1151": {
    "type": "dunEnd",
    "exitTime": 65.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1153": {
    "type": "monsterInBattle",
    "monsterID": [
      21040002
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1154,
        1150,
        1155,
        1158,
        1168
      ]
    }
  },
  "1154": {
    "type": "popupdialog",
    "entityID": [
      21040002
    ],
    "dialogID": 19104004,
    "transition": {}
  },
  "1150": {
    "type": "createRebornPos",
    "entityID": [
      21048011
    ],
    "num": 1,
    "transition": {}
  },
  "1155": {
    "type": "createNPC",
    "entityID": [
      21044009,
      21040010,
      21040011,
      21040012
    ],
    "num": 1,
    "lv": "46",
    "ifSetBoss": 1,
    "transition": {}
  },
  "1156": {
    "type": "removeRebornPos",
    "entityID": [
      21048003
    ],
    "transition": {}
  },
  "1157": {
    "type": "createRebornPos",
    "entityID": [
      21048003
    ],
    "num": 1,
    "transition": {}
  },
  "1158": {
    "type": "removeRebornPos",
    "entityID": [
      21048010
    ],
    "transition": {}
  },
  "1164": {
    "type": "monsterHp",
    "monsterID": [
      21040001
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1165
      ]
    }
  },
  "1165": {
    "type": "popupdialog",
    "entityID": [
      21040001
    ],
    "dialogID": 19104002,
    "transition": {}
  },
  "1166": {
    "type": "popupdialog",
    "entityID": [
      21040001
    ],
    "dialogID": 19104003,
    "transition": {}
  },
  "1167": {
    "type": "popupdialog",
    "entityID": [
      21040002
    ],
    "dialogID": 19104005,
    "transition": {}
  },
  "1168": {
    "type": "monsterHp",
    "monsterID": [
      21040002
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1167
      ]
    }
  },
  "1169": {
    "type": "popupdialog",
    "entityID": [
      21040002
    ],
    "dialogID": 19104006,
    "transition": {
      "finished": [
        1151
      ]
    }
  }
}