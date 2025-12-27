datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40100001,
      40100002,
      40100003
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
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1021,
        1020
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40108002
    ],
    "num": 0,
    "transition": {}
  },
  "1021": {
    "type": "taskFinished",
    "taskID": 86090120,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1022
      ]
    }
  },
  "1022": {
    "type": "showPopoverMsg",
    "entityID": [
      40100001
    ],
    "messageID": 19900243,
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1024": {
    "type": "dunEnd",
    "exitTime": 8.0,
    "isDungeonDone": 1,
    "transition": {}
  }
}