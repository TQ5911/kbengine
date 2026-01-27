datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40110001
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
        1020,
        1025
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40118002
    ],
    "num": 0,
    "transition": {}
  },
  "1021": {
    "type": "taskFinished",
    "taskID": 86090101,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1022
      ]
    }
  },
  "1022": {
    "type": "popupdialog",
    "entityID": [
      40110001
    ],
    "dialogID": 19900230,
    "transition": {}
  },
  "1025": {
    "type": "createNPC",
    "entityID": [
      40114001
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  }
}