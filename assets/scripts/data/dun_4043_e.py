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
      40438002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createMonster",
    "entityID": [
      40430001
    ],
    "num": 0,
    "lv": "23",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1046,
        1048
      ]
    }
  },
  "1046": {
    "type": "monsterHp",
    "monsterID": [
      40430001
    ],
    "compare": 5,
    "hpPercent": 90.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1047
      ]
    }
  },
  "1047": {
    "type": "popupdialog",
    "entityID": [
      40430001
    ],
    "dialogID": 19900558,
    "transition": {}
  },
  "1048": {
    "type": "monsterHp",
    "monsterID": [
      40430001
    ],
    "compare": 5,
    "hpPercent": 60.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1049
      ]
    }
  },
  "1049": {
    "type": "popupdialog",
    "entityID": [
      40430001
    ],
    "dialogID": 19900561,
    "transition": {}
  },
  "1050": {
    "type": "monsterHp",
    "monsterID": [
      40430001
    ],
    "compare": 5,
    "hpPercent": 20.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1051
      ]
    }
  },
  "1051": {
    "type": "popupdialog",
    "entityID": [
      40430001
    ],
    "dialogID": 19900565,
    "transition": {}
  }
}