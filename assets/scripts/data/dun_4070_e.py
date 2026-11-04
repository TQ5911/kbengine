datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1015,
        1115,
        1116
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40708002
    ],
    "num": 0,
    "transition": {}
  },
  "1115": {
    "type": "createNPC",
    "entityID": [
      40704001
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1116": {
    "type": "createMonster",
    "entityID": [
      40700001,
      40700002,
      40700003,
      40700004,
      40700005,
      40700006,
      40700007,
      40700008,
      40700009
    ],
    "num": 0,
    "lv": "60",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1117
      ]
    }
  },
  "1117": {
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
        1118
      ]
    }
  },
  "1118": {
    "type": "createMonster",
    "entityID": [
      40700013,
      40700014,
      40700015,
      40700016,
      40700017,
      40700018,
      40700019,
      40700020,
      40700021,
      40700022,
      40700023,
      40700024
    ],
    "num": 0,
    "lv": "60",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1119
      ]
    }
  },
  "1119": {
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
        1121
      ]
    }
  },
  "1121": {
    "type": "createMonster",
    "entityID": [
      40700025
    ],
    "num": 0,
    "lv": "60",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1122
      ]
    }
  },
  "1122": {
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
        1123,
        1124
      ]
    }
  },
  "1123": {
    "type": "createNPC",
    "entityID": [
      40704004,
      40704002
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1125
      ]
    }
  },
  "1124": {
    "type": "removeNPC",
    "entityID": [
      40704001
    ],
    "transition": {}
  },
  "1125": {
    "type": "taskFinished",
    "taskID": 86010558,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1126,
        1127
      ]
    }
  },
  "1126": {
    "type": "createNPC",
    "entityID": [
      40704003,
      40704005
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1127": {
    "type": "removeNPC",
    "entityID": [
      40704004,
      40704002
    ],
    "transition": {}
  }
}