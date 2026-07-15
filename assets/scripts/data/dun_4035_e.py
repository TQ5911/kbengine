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
      40358002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createMonster",
    "entityID": [
      40350001,
      40350002,
      40350003,
      40350004,
      40350005,
      40350006,
      40350007,
      40350008,
      40350009
    ],
    "num": 0,
    "lv": "8",
    "initState": 2,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1046
      ]
    }
  },
  "1046": {
    "type": "monsterChangeInitState",
    "entityID": [
      40350001,
      40350002,
      40350003,
      40350004,
      40350005,
      40350006,
      40350007,
      40350008,
      40350009
    ],
    "initState": 0,
    "transition": {}
  }
}