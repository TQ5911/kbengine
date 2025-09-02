datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20140003
    ],
    "num": 1,
    "lv": "20",
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
      20140003
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
    "exitTime": 15.0,
    "transition": {}
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      20140003
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1026,
        1021
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      20140003
    ],
    "dialogID": 19014004,
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
  "1026": {
    "type": "monsterHp",
    "monsterID": [
      20140003
    ],
    "compare": 5,
    "hpPercent": 75.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1027,
        1022
      ]
    }
  },
  "1027": {
    "type": "addBuffToMonster",
    "monsterID": [
      20140003
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
  "1029": {
    "type": "monsterHp",
    "monsterID": [
      20140003
    ],
    "compare": 5,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1030,
        1023
      ]
    }
  },
  "1030": {
    "type": "addBuffToMonster",
    "monsterID": [
      20140003
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
  "1031": {
    "type": "removeBuffFromMonster",
    "monsterID": [
      20140003
    ],
    "buffID": [
      64004904
    ],
    "transition": {
      "finished": [
        1006
      ]
    }
  },
  "1021": {
    "type": "popupdialog",
    "entityID": [
      20140003
    ],
    "dialogID": 19014001,
    "transition": {}
  },
  "1022": {
    "type": "popupdialog",
    "entityID": [
      20140003
    ],
    "dialogID": 19014002,
    "transition": {}
  },
  "1023": {
    "type": "popupdialog",
    "entityID": [
      20140003
    ],
    "dialogID": 19014003,
    "transition": {}
  }
}