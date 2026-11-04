datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      21050003,
      21050004,
      21050005,
      21050006,
      21050007,
      21050008,
      21050009,
      21050010,
      21050011,
      21050012,
      21050013,
      21050014,
      21050015,
      21050016,
      21050017,
      21050018,
      21050019,
      21050020
    ],
    "num": 0,
    "lv": "60",
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
        1141,
        1157
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
      21050021,
      21050022,
      21050023,
      21050024,
      21050025,
      21050026,
      21050027,
      21050028,
      21050029,
      21050030,
      21050031,
      21050032,
      21050033,
      21050034,
      21050035,
      21050036,
      21050037,
      21050038,
      21050039
    ],
    "num": 0,
    "lv": "60",
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
        1018
      ]
    }
  },
  "1911": {
    "type": "createMonster",
    "entityID": [
      21050053,
      21050054,
      21050055,
      21050056,
      21050057,
      21050058,
      21050059,
      21050060,
      21050061,
      21050062,
      21050063
    ],
    "num": 0,
    "lv": "60",
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
      21050064,
      21050065,
      21050066,
      21050067,
      21050068,
      21050069,
      21050070,
      21050071,
      21050072,
      21050073,
      21050074,
      21050075,
      21050076,
      21050077,
      21050078,
      21050079
    ],
    "num": 0,
    "lv": "60",
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
      21050080,
      21050081,
      21050082,
      21050083,
      21050084,
      21050085,
      21050086,
      21050087,
      21050088,
      21050089,
      21050090,
      21050091
    ],
    "num": 0,
    "lv": "60",
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
        1007
      ]
    }
  },
  "1141": {
    "type": "createNPC",
    "entityID": [
      21054001,
      21054002,
      21054003,
      21054004
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1157": {
    "type": "createRebornPos",
    "entityID": [
      21058002
    ],
    "num": 1,
    "transition": {}
  },
  "1005": {
    "type": "createMonster",
    "entityID": [
      21050001
    ],
    "num": 1,
    "lv": "61",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1010,
        1006
      ]
    }
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      21050001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1011
      ]
    }
  },
  "1010": {
    "type": "monsterInBattle",
    "monsterID": [
      21050001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1026,
        1142,
        1144
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      21050001
    ],
    "dialogID": 19900052,
    "transition": {
      "finished": [
        1911
      ]
    }
  },
  "1026": {
    "type": "monsterHp",
    "monsterID": [
      21050001
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1027
      ]
    }
  },
  "1027": {
    "type": "addBuffToMonster",
    "monsterID": [
      21050001
    ],
    "buffID": [
      64004905
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1007": {
    "type": "createMonster",
    "entityID": [
      21050002
    ],
    "num": 1,
    "lv": "60",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1016,
        1014
      ]
    }
  },
  "1012": {
    "type": "dunEnd",
    "exitTime": 30.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1014": {
    "type": "monsterRestNum",
    "monsterID": [
      21050002
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1017,
        1012
      ]
    }
  },
  "1016": {
    "type": "monsterInBattle",
    "monsterID": [
      21050002
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1032,
        1021,
        1028,
        1146,
        1148
      ]
    }
  },
  "1017": {
    "type": "popupdialog",
    "entityID": [
      21050002
    ],
    "dialogID": 19025004,
    "transition": {}
  },
  "1032": {
    "type": "monsterHp",
    "monsterID": [
      21050002
    ],
    "compare": 5,
    "hpPercent": 75.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1033,
        1022
      ]
    }
  },
  "1033": {
    "type": "addBuffToMonster",
    "monsterID": [
      21050002
    ],
    "buffID": [
      64004904
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1029
      ]
    }
  },
  "1021": {
    "type": "popupdialog",
    "entityID": [
      21050002
    ],
    "dialogID": 19025001,
    "transition": {}
  },
  "1022": {
    "type": "popupdialog",
    "entityID": [
      21050002
    ],
    "dialogID": 19025002,
    "transition": {}
  },
  "1028": {
    "type": "addBuffToMonster",
    "monsterID": [
      21050002
    ],
    "buffID": [
      64004085
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": 30.0,
    "transition": {}
  },
  "1029": {
    "type": "monsterHp",
    "monsterID": [
      21050002
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1023,
        1030
      ]
    }
  },
  "1030": {
    "type": "addBuffToMonster",
    "monsterID": [
      21050002
    ],
    "buffID": [
      64004905
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1031
      ]
    }
  },
  "1023": {
    "type": "popupdialog",
    "entityID": [
      21050002
    ],
    "dialogID": 19025003,
    "transition": {}
  },
  "1031": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      21050002
    ],
    "buffID": [
      64004904
    ],
    "transition": {}
  },
  "1018": {
    "type": "createMonster",
    "entityID": [
      21050040,
      21050041,
      21050042,
      21050043,
      21050044,
      21050045,
      21050046,
      21050047,
      21050048,
      21050049,
      21050050,
      21050051
    ],
    "num": 0,
    "lv": "60",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        2002
      ]
    }
  },
  "2002": {
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
        1005
      ]
    }
  },
  "1142": {
    "type": "removeRebornPos",
    "entityID": [
      21058002
    ],
    "transition": {
      "finished": [
        1143
      ]
    }
  },
  "1143": {
    "type": "createRebornPos",
    "entityID": [
      21058004
    ],
    "num": 1,
    "transition": {}
  },
  "1144": {
    "type": "removeNPC",
    "entityID": [
      21054001,
      21054002,
      21054003,
      21054004
    ],
    "transition": {
      "finished": [
        1145
      ]
    }
  },
  "1145": {
    "type": "createNPC",
    "entityID": [
      21054005,
      21054006,
      21054007,
      21054008
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1146": {
    "type": "removeRebornPos",
    "entityID": [
      21058004
    ],
    "transition": {
      "finished": [
        1147
      ]
    }
  },
  "1147": {
    "type": "createRebornPos",
    "entityID": [
      21058005
    ],
    "num": 1,
    "transition": {}
  },
  "1148": {
    "type": "removeNPC",
    "entityID": [
      21054005,
      21054006,
      21054007,
      21054008
    ],
    "transition": {
      "finished": [
        1149
      ]
    }
  },
  "1149": {
    "type": "createNPC",
    "entityID": [
      21054009,
      21054010,
      21054011,
      21054012
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  }
}