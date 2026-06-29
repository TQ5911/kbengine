datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      22040001
    ],
    "num": 0,
    "lv": "25",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1012,
        1010
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
    "exitTime": 30.0,
    "transition": {}
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
  "1010": {
    "type": "monsterInBattle",
    "monsterID": [
      22040001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1022,
        1032,
        1031
      ]
    }
  },
  "1007": {
    "type": "dunEnd",
    "exitTime": 30.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1012": {
    "type": "monsterRestNum",
    "monsterID": [
      22040001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1014,
        1007
      ]
    }
  },
  "1014": {
    "type": "popupdialog",
    "entityID": [
      22040001
    ],
    "dialogID": 19022011,
    "transition": {}
  },
  "1032": {
    "type": "monsterHp",
    "monsterID": [
      22040001
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
      22040001
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
      22040001
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
      22040001
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
      22040001
    ],
    "skillID": 91036012,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1058,
        1063
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
      22040001
    ],
    "buffID": [
      64004967
    ],
    "transition": {}
  },
  "1033": {
    "type": "addBuffToMonster",
    "monsterID": [
      22040001
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
      22040001
    ],
    "dialogID": 19022007,
    "transition": {}
  },
  "1019": {
    "type": "popupdialog",
    "entityID": [
      22040001
    ],
    "dialogID": 19022009,
    "transition": {}
  },
  "1022": {
    "type": "popupdialog",
    "entityID": [
      22040001
    ],
    "dialogID": 19022006,
    "transition": {}
  },
  "1035": {
    "type": "addBuffToMonster",
    "monsterID": [
      22040001
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
      22040001
    ],
    "skillID": 91036012,
    "lv": "1",
    "forceToUse": 1,
    "transition": {
      "finished": [
        1061,
        1062
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
        1024
      ]
    }
  },
  "1024": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22040001
    ],
    "buffID": [
      64004967
    ],
    "transition": {}
  },
  "1062": {
    "type": "delayLoop",
    "firstDelay": 5.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "loop": [
        1026
      ]
    }
  },
  "1026": {
    "type": "popupdialog",
    "entityID": [
      22040001
    ],
    "dialogID": 19022008,
    "transition": {}
  },
  "1063": {
    "type": "delayLoop",
    "firstDelay": 5.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "loop": [
        1027
      ]
    }
  },
  "1027": {
    "type": "popupdialog",
    "entityID": [
      22040001
    ],
    "dialogID": 19022010,
    "transition": {}
  }
}