datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      31250002
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
        1051
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
      31250002
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1006
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
      31250002
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1051": {
    "type": "delayLoop",
    "firstDelay": 5.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1004,
        1003
      ]
    }
  }
}