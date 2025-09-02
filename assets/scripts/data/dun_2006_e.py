datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20060003
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
        1017
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
        1004
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
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1012
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
      20060003
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1010
      ]
    }
  },
  "1010": {
    "type": "popupdialog",
    "entityID": [
      20060003
    ],
    "dialogID": 19900053,
    "transition": {
      "finished": [
        1006
      ]
    }
  },
  "1012": {
    "type": "popupdialog",
    "entityID": [
      20060003
    ],
    "dialogID": 19900054,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1017": {
    "type": "createMonster",
    "entityID": [
      20060004,
      20060005,
      20060006,
      20060007,
      20060008,
      20060009
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
  }
}