datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20150003
    ],
    "num": 1,
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
        1007
      ]
    }
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 5.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      20150003
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
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      20150003
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1006,
        1145,
        1021,
        1031,
        1051
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      20150003
    ],
    "dialogID": 19015005,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1007": {
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
  "1021": {
    "type": "monsterHp",
    "monsterID": [
      20150003
    ],
    "compare": 5,
    "hpPercent": 75.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1026,
        1142
      ]
    }
  },
  "1023": {
    "type": "castSkill",
    "entityID": [
      20150003
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
      20150003
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1143,
        1025
      ]
    }
  },
  "1033": {
    "type": "createMonster",
    "entityID": [
      20150004,
      20150005,
      20150006,
      20150007
    ],
    "num": 1,
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
        1035,
        1041
      ]
    }
  },
  "1034": {
    "type": "addBuffToMonster",
    "monsterID": [
      20150003
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
        1140
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
      20150003
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
      20150003
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
      20150003
    ],
    "compare": 5,
    "hpPercent": 25.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1027,
        1144
      ]
    }
  },
  "1053": {
    "type": "castSkill",
    "entityID": [
      20150003
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
      20150003
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
      20150003
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
      20150003
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
      20150003
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
      20150003
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
      20150003
    ],
    "buffID": [
      64004010
    ],
    "transition": {}
  },
  "1140": {
    "type": "delayLoop",
    "firstDelay": 20.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1141
      ]
    }
  },
  "1141": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      21030002
    ],
    "buffID": [
      64004010
    ],
    "transition": {}
  },
  "1142": {
    "type": "popupdialog",
    "entityID": [
      20150003
    ],
    "dialogID": 19015002,
    "transition": {}
  },
  "1143": {
    "type": "popupdialog",
    "entityID": [
      20150003
    ],
    "dialogID": 19015003,
    "transition": {}
  },
  "1144": {
    "type": "popupdialog",
    "entityID": [
      20150003
    ],
    "dialogID": 19015004,
    "transition": {}
  },
  "1145": {
    "type": "popupdialog",
    "entityID": [
      20150003
    ],
    "dialogID": 19015001,
    "transition": {}
  }
}