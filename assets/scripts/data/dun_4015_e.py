datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40150001
    ],
    "num": 0,
    "lv": "10",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1027,
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
      40158001
    ],
    "num": 0,
    "transition": {}
  },
  "1027": {
    "type": "monsterHp",
    "monsterID": [
      40150001
    ],
    "compare": 1,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1028
      ]
    }
  },
  "1028": {
    "type": "popupdialog",
    "entityID": [
      40150001
    ],
    "dialogID": 19900380,
    "transition": {}
  },
  "1029": {
    "type": "monsterHp",
    "monsterID": [
      40150001
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
      40150001
    ],
    "dialogID": 19900381,
    "transition": {}
  }
}