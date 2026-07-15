datas ={
  "1003": {
    "type": "createInnerDemon",
    "entityID": [
      31250002
    ],
    "hpMult": 3.3,
    "transition": {
      "finished": [
        1060,
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
        1065
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 60.0,
    "transition": {}
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      31250002
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1006,
        1068
      ]
    }
  },
  "1005": {
    "type": "dunDelayEnd",
    "exitTime": 1800.0,
    "preExitTime": 1800.0,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      31250002
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1005,
        1056,
        1059,
        1069,
        1070
      ]
    }
  },
  "1051": {
    "type": "delayLoop",
    "firstDelay": 3.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1004,
        1003
      ]
    }
  },
  "1056": {
    "type": "createCollection",
    "entityID": [
      31258001
    ],
    "num": 1,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1058
      ]
    }
  },
  "1057": {
    "type": "dunEnd",
    "exitTime": 60.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1058": {
    "type": "collBeCollected",
    "entityID": [
      31258001
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1057
      ]
    }
  },
  "1059": {
    "type": "notifyInnerDemonData",
    "entityID": [
      31250002
    ],
    "transition": {}
  },
  "1060": {
    "type": "alivePlayer",
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
  "1064": {
    "type": "broadcastMsg",
    "messageID": 54479002,
    "transition": {}
  },
  "1065": {
    "type": "delayLoop",
    "firstDelay": 6.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1051,
        1064
      ]
    }
  },
  "1068": {
    "type": "createMonster",
    "entityID": [
      31250003
    ],
    "num": 0,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1069": {
    "type": "removeMonster",
    "entityID": [
      31250003
    ],
    "transition": {}
  },
  "1070": {
    "type": "stopDelayEvent",
    "eventID": [
      1004
    ],
    "transition": {}
  }
}