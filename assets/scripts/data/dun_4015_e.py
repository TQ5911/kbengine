datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40150001
    ],
    "num": 0,
    "lv": "13",
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
      40158001
    ],
    "num": 0,
    "transition": {}
  }
}