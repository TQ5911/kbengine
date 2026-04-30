datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20190001
    ],
    "num": 1,
    "lv": "10",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
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
        1013,
        1030
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
      20190001
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
      20190001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1010,
        1022
      ]
    }
  },
  "1010": {
    "type": "popupdialog",
    "entityID": [
      20190001
    ],
    "dialogID": 19019001,
    "transition": {}
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      20190001
    ],
    "dialogID": 19019004,
    "transition": {
      "finished": [
        1005
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
  "1022": {
    "type": "delayLoop",
    "firstDelay": 120.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1031
      ]
    }
  },
  "1025": {
    "type": "castSkill",
    "entityID": [
      20190001
    ],
    "skillID": 91025015,
    "lv": "1",
    "forceToUse": 1,
    "transition": {}
  },
  "1030": {
    "type": "taskUndertake",
    "taskID": 86010001,
    "transition": {}
  },
  "1031": {
    "type": "popupdialog",
    "entityID": [
      20190001
    ],
    "dialogID": 19019005,
    "transition": {
      "finished": [
        1025
      ]
    }
  }
}