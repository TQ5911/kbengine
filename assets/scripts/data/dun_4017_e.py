datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40170004,
      40170005,
      40170006
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
      40178002
    ],
    "num": 0,
    "transition": {}
  },
  "1029": {
    "type": "monsterHp",
    "monsterID": [
      40170004
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1030
      ]
    }
  },
  "1030": {
    "type": "popupdialog",
    "entityID": [
      40170004
    ],
    "dialogID": 19900398,
    "transition": {}
  }
}