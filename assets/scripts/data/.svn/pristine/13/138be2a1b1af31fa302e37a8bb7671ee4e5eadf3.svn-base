datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20050003
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
        1018
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
      20050003
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
      20050003
    ],
    "dialogID": 19900051,
    "transition": {
      "finished": [
        1006
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      20050003
    ],
    "dialogID": 19900052,
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
  "1018": {
    "type": "createAirWall",
    "entityID": [
      20050004,
      20050005,
      20050006,
      20050007,
      20050008,
      20050009,
      20050010,
      20050011
    ],
    "num": 1,
    "transition": {}
  }
}