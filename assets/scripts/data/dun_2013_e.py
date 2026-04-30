datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20130003
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
      20130003
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
      20130003
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1026,
        1021,
        1028
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      20130003
    ],
    "dialogID": 19013003,
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
      20130003
    ],
    "compare": 5,
    "hpPercent": 50.0,
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
      20130003
    ],
    "buffID": [
      64004905
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1021": {
    "type": "popupdialog",
    "entityID": [
      20130003
    ],
    "dialogID": 19013001,
    "transition": {}
  },
  "1022": {
    "type": "popupdialog",
    "entityID": [
      20130003
    ],
    "dialogID": 19013002,
    "transition": {}
  },
  "1028": {
    "type": "addBuffToMonster",
    "monsterID": [
      20130003
    ],
    "buffID": [
      64004085
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": 30.0,
    "transition": {}
  }
}