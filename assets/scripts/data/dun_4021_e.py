datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40210001,
      40210002,
      40210003,
      40210004,
      40210005
    ],
    "num": 0,
    "lv": "30",
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
        1020
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40218002
    ],
    "num": 0,
    "transition": {}
  }
}