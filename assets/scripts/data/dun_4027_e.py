datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1046,
        1047,
        1050,
        1048
      ]
    }
  },
  "1046": {
    "type": "createRebornPos",
    "entityID": [
      40278002
    ],
    "num": 0,
    "transition": {}
  },
  "1047": {
    "type": "createMonster",
    "entityID": [
      40270001
    ],
    "num": 0,
    "lv": "19",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1048": {
    "type": "taskFinished",
    "taskID": 86030002,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1049
      ]
    }
  },
  "1049": {
    "type": "changeEntityForce",
    "entityID": [
      40270001
    ],
    "force": 2,
    "transition": {}
  },
  "1050": {
    "type": "taskUndertake",
    "taskID": 86030001,
    "transition": {}
  }
}