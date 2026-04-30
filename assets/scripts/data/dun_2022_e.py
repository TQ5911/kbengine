datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20220001
    ],
    "num": 1,
    "lv": "28",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1009,
        1006
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
        1013
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 20.0,
    "transition": {}
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      20220001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1020,
        1032,
        1031
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
  "1005": {
    "type": "dunEnd",
    "exitTime": 15.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      20220001
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
  "1011": {
    "type": "popupdialog",
    "entityID": [
      20220001
    ],
    "dialogID": 19021006,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1032": {
    "type": "monsterHp",
    "monsterID": [
      20220001
    ],
    "compare": 5,
    "hpPercent": 75.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1033,
        1102
      ]
    }
  },
  "1031": {
    "type": "monsterHp",
    "monsterID": [
      20220001
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1025,
        1019
      ]
    }
  },
  "1034": {
    "type": "addBuffToMonster",
    "monsterID": [
      20220001
    ],
    "buffID": [
      64004967
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1057
      ]
    }
  },
  "1025": {
    "type": "addBuffToMonster",
    "monsterID": [
      20220001
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
  "1057": {
    "type": "castSkill",
    "entityID": [
      20220001
    ],
    "skillID": 91036012,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1058
      ]
    }
  },
  "1058": {
    "type": "delayLoop",
    "firstDelay": 15.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "loop": [
        1059
      ]
    }
  },
  "1059": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      20220001
    ],
    "buffID": [
      64004967
    ],
    "transition": {}
  },
  "1033": {
    "type": "addBuffToMonster",
    "monsterID": [
      20220001
    ],
    "buffID": [
      64004904
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {
      "finished": [
        1035
      ]
    }
  },
  "1102": {
    "type": "popupdialog",
    "entityID": [
      20220001
    ],
    "dialogID": 19021002,
    "transition": {}
  },
  "1019": {
    "type": "popupdialog",
    "entityID": [
      20220001
    ],
    "dialogID": 19021004,
    "transition": {}
  },
  "1020": {
    "type": "popupdialog",
    "entityID": [
      20220001
    ],
    "dialogID": 19021001,
    "transition": {}
  },
  "1035": {
    "type": "addBuffToMonster",
    "monsterID": [
      20220001
    ],
    "buffID": [
      64004967
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
    "type": "castSkill",
    "entityID": [
      20220001
    ],
    "skillID": 91036012,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1061
      ]
    }
  },
  "1061": {
    "type": "delayLoop",
    "firstDelay": 15.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "loop": [
        1021
      ]
    }
  },
  "1021": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      20220001
    ],
    "buffID": [
      64004967
    ],
    "transition": {}
  }
}