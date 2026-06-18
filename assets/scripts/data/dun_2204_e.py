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
    "exitTime": 30.0,
    "transition": {}
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      22040001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1020
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
    "exitTime": 30.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
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
        1011,
        1005
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      22040001
    ],
    "dialogID": 19021006,
    "transition": {}
  },
  "1020": {
    "type": "popupdialog",
    "entityID": [
      22040001
    ],
    "dialogID": 19021001,
    "transition": {}
  }
}