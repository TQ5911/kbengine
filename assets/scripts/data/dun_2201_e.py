datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      22010001
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
      22010001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1020,
        1021,
        1031,
        1006,
        1061
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
    "exitTime": 65.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      22010001
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
      22010001
    ],
    "dialogID": 19021006,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1021": {
    "type": "monsterHp",
    "monsterID": [
      22010001
    ],
    "compare": 5,
    "hpPercent": 75.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1022,
        1102
      ]
    }
  },
  "1023": {
    "type": "castSkill",
    "entityID": [
      22010001
    ],
    "skillID": 91027021,
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
      22010001
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
      22010001
    ],
    "buffID": [
      64004957
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
      22010001
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
      22010001
    ],
    "buffID": [
      64004957
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
  "1028": {
    "type": "delayLoop",
    "firstDelay": 26.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "loop": [
        1029
      ]
    }
  },
  "1029": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      22010001
    ],
    "buffID": [
      64004957
    ],
    "transition": {
      "finished": [
        1062
      ]
    }
  },
  "1057": {
    "type": "castSkill",
    "entityID": [
      22010001
    ],
    "skillID": 91027025,
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
    "firstDelay": 26.0,
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
      22010001
    ],
    "buffID": [
      64004957
    ],
    "transition": {
      "finished": [
        1063
      ]
    }
  },
  "1022": {
    "type": "addBuffToMonster",
    "monsterID": [
      22010001
    ],
    "buffID": [
      64004904
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
  "1102": {
    "type": "popupdialog",
    "entityID": [
      22010001
    ],
    "dialogID": 19021002,
    "transition": {}
  },
  "1019": {
    "type": "popupdialog",
    "entityID": [
      22010001
    ],
    "dialogID": 19021004,
    "transition": {}
  },
  "1020": {
    "type": "popupdialog",
    "entityID": [
      22010001
    ],
    "dialogID": 19021001,
    "transition": {}
  },
  "1061": {
    "type": "addBuffToMonster",
    "monsterID": [
      22010001
    ],
    "buffID": [
      64004087
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": 60.0,
    "transition": {}
  },
  "1062": {
    "type": "addBuffToMonster",
    "monsterID": [
      22010001
    ],
    "buffID": [
      64004088
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": 60.0,
    "transition": {}
  },
  "1063": {
    "type": "addBuffToMonster",
    "monsterID": [
      22010001
    ],
    "buffID": [
      64004088
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": 60.0,
    "transition": {}
  }
}