datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40190002,
      40190003,
      40190004,
      40190005,
      40190006
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
      40198002
    ],
    "num": 0,
    "transition": {}
  }
}