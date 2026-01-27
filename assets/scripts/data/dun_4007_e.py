datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1031,
        1038,
        1042,
        1013
      ]
    }
  },
  "1013": {
    "type": "monsterHp",
    "monsterID": [
      40070001
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1040
      ]
    }
  },
  "1031": {
    "type": "createMonster",
    "entityID": [
      40070001
    ],
    "num": 1,
    "lv": "23",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1038": {
    "type": "createRebornPos",
    "entityID": [
      40078003
    ],
    "num": 1,
    "transition": {}
  },
  "1040": {
    "type": "popupdialog",
    "entityID": [
      40070001
    ],
    "dialogID": 19900193,
    "transition": {}
  },
  "1042": {
    "type": "createMonster",
    "entityID": [
      40070002,
      40070003
    ],
    "num": 1,
    "lv": "23",
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