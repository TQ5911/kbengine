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
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1025,
        1020
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40098002
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
    "lv": "28",
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