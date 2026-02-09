datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40080001
    ],
    "num": 0,
    "lv": "8",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1004": {
    "type": "delayLoop",
    "firstDelay": 1800.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1017,
        1018,
        1004,
        1019
      ]
    }
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 5.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1016": {
    "type": "createMonster",
    "entityID": [
      40080002
    ],
    "num": 0,
    "lv": "8",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1017": {
    "type": "taskFinished",
    "taskID": 86050066,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1016
      ]
    }
  },
  "1018": {
    "type": "taskInProgress",
    "taskID": 86050067,
    "transition": {
      "finished": [
        1016
      ]
    }
  },
  "1019": {
    "type": "createRebornPos",
    "entityID": [
      40088002
    ],
    "num": 0,
    "transition": {}
  }
}