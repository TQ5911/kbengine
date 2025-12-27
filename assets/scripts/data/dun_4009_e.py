datas ={
  "1003": {
    "type": "taskFinished",
    "taskID": 86090181,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1023
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
        1005
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1004,
        1025,
        1020
      ]
    }
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 5.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40088002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createMonster",
    "entityID": [
      40090002,
      40090001
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
  "1025": {
    "type": "createNPC",
    "entityID": [
      40094001,
      40094002,
      40094003,
      40094004
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  }
}