datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      23020001
    ],
    "num": 0,
    "lv": "50",
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
    "firstDelay": 3490.0,
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
        1036,
        1039
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 10.0,
    "transition": {}
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      23020001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1020,
        1006
      ]
    }
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 125.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      23020001
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
      23020001
    ],
    "dialogID": 19032002,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1020": {
    "type": "popupdialog",
    "entityID": [
      23020001
    ],
    "dialogID": 19032001,
    "transition": {}
  },
  "1036": {
    "type": "delayLoop",
    "firstDelay": 110.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1004,
        1042,
        1043,
        1003
      ]
    }
  },
  "1039": {
    "type": "createAirWall",
    "entityID": [
      23028005
    ],
    "num": 1,
    "transition": {}
  },
  "1041": {
    "type": "removeAirWall",
    "entityID": [
      23028005
    ],
    "transition": {}
  },
  "1042": {
    "type": "delayLoop",
    "firstDelay": 10.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1041
      ]
    }
  },
  "1043": {
    "type": "notifyStartBattleCD",
    "cdTime": 10,
    "transition": {}
  }
}