datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40160005,
      40160006,
      40160007,
      40160008,
      40160009
    ],
    "num": 0,
    "lv": "11",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1029
      ]
    }
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
      40168002
    ],
    "num": 0,
    "transition": {}
  },
  "1029": {
    "type": "monsterHp",
    "monsterID": [
      40160005
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1031
      ]
    }
  },
  "1031": {
    "type": "popupdialog",
    "entityID": [
      40160005
    ],
    "dialogID": 19900397,
    "transition": {}
  }
}