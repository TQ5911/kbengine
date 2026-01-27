datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40140001,
      40140002,
      40140003,
      40140004,
      40140005,
      40140006,
      40140007,
      40140008,
      40140009,
      40140010
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
        1026,
        1020
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40148002
    ],
    "num": 0,
    "transition": {}
  },
  "1026": {
    "type": "createNPC",
    "entityID": [
      40144001
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  }
}