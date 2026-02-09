datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40200001,
      40200002,
      40200003,
      40200004,
      40200005
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
      40208002
    ],
    "num": 0,
    "transition": {}
  }
}