datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40250001,
      40250002,
      40250003,
      40250004,
      40250005
    ],
    "num": 0,
    "lv": "20",
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
        1020,
        1031
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40258002
    ],
    "num": 0,
    "transition": {}
  },
  "1031": {
    "type": "taskFinished",
    "taskID": 86010180,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1032
      ]
    }
  },
  "1032": {
    "type": "createMonster",
    "entityID": [
      40250006,
      40250007,
      40250008,
      40250009,
      40250010
    ],
    "num": 0,
    "lv": "20",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  }
}