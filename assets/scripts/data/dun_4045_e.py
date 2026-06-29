datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1023,
        1015
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40458002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createNPC",
    "entityID": [
      40454001
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1046
      ]
    }
  },
  "1046": {
    "type": "taskFinished",
    "taskID": 86010134,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1047
      ]
    }
  },
  "1047": {
    "type": "createMonster",
    "entityID": [
      40450001,
      40450002,
      40450003,
      40450004,
      40450005,
      40450006,
      40450007,
      40450008,
      40450009
    ],
    "num": 0,
    "lv": "25",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1049
      ]
    }
  },
  "1049": {
    "type": "removeNPC",
    "entityID": [
      40454001
    ],
    "transition": {
      "finished": [
        1050
      ]
    }
  },
  "1050": {
    "type": "taskFinished",
    "taskID": 86010282,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1051
      ]
    }
  },
  "1051": {
    "type": "createNPC",
    "entityID": [
      40454002,
      40454003
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  }
}