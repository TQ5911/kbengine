datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1031,
        1038,
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
      40070002,
      40070003,
      40070004,
      40070005,
      40070006,
      40070007
    ],
    "num": 1,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1044
      ]
    }
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
  "1044": {
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1045
      ]
    }
  },
  "1045": {
    "type": "createMonster",
    "entityID": [
      40070008,
      40070009,
      40070010,
      40070011,
      40070012,
      40070013,
      40070014,
      40070015,
      40070016
    ],
    "num": 1,
    "lv": "30",
    "initState": 0,
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
    "type": "monsterRestNum",
    "monsterID": [
      -1
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1047
      ]
    }
  },
  "1047": {
    "type": "createMonster",
    "entityID": [
      40070001
    ],
    "num": 1,
    "lv": "30",
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