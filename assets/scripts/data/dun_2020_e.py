datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20200001
    ],
    "num": 1,
    "lv": "20",
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
    "firstDelay": 300.0,
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
  "1005": {
    "type": "dunEnd",
    "exitTime": 5.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      20200001
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
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64004046
    ],
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      20200001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1010,
        1021,
        1006
      ]
    }
  },
  "1010": {
    "type": "popupdialog",
    "entityID": [
      20200001
    ],
    "dialogID": 19020001,
    "transition": {}
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      20200001
    ],
    "dialogID": 19020004,
    "transition": {
      "finished": [
        1025
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
  "1019": {
    "type": "castSkill",
    "entityID": [
      20200001
    ],
    "skillID": 91026008,
    "lv": "1",
    "forceToUse": 0,
    "transition": {
      "finished": [
        1022
      ]
    }
  },
  "1022": {
    "type": "createMonster",
    "entityID": [
      20200003
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
        1023
      ]
    }
  },
  "1012": {
    "type": "playerRestNum",
    "compare": 3,
    "num": 1,
    "checkNow": 1,
    "checkOnce": 1,
    "transition": {
      "finished": [
        1026
      ]
    }
  },
  "1023": {
    "type": "monsterHp",
    "monsterID": [
      20200003
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1020
      ]
    }
  },
  "1020": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64004046
    ],
    "transition": {}
  },
  "1021": {
    "type": "delayLoop",
    "firstDelay": 120.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1012,
        1028
      ]
    }
  },
  "1024": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1025": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64004046
    ],
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1026": {
    "type": "popupdialog",
    "entityID": [
      20200001
    ],
    "dialogID": 54471810,
    "transition": {
      "finished": [
        1019
      ]
    }
  },
  "1028": {
    "type": "playerRestNum",
    "compare": 1,
    "num": 1,
    "checkNow": 1,
    "checkOnce": 1,
    "transition": {
      "finished": [
        1030
      ]
    }
  },
  "1030": {
    "type": "popupdialog",
    "entityID": [
      20200001
    ],
    "dialogID": 54471810,
    "transition": {
      "finished": [
        1032,
        1037
      ]
    }
  },
  "1032": {
    "type": "createMonster",
    "entityID": [
      20200003
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
        1035
      ]
    }
  },
  "1035": {
    "type": "monsterHp",
    "monsterID": [
      20200003
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 1,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1038
      ]
    }
  },
  "1037": {
    "type": "addBuffToMonster",
    "monsterID": [
      20200001
    ],
    "buffID": [
      64004040
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1038": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      20200001
    ],
    "buffID": [
      64004040
    ],
    "transition": {}
  }
}