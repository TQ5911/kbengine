datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40100001
    ],
    "num": 1,
    "lv": "28",
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
        1021,
        1020
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40108002
    ],
    "num": 0,
    "transition": {}
  },
  "1021": {
    "type": "monsterHp",
    "monsterID": [
      40100001
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1022
      ]
    }
  },
  "1022": {
    "type": "popupdialog",
    "entityID": [
      40100001
    ],
    "dialogID": 19900243,
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1024": {
    "type": "dunEnd",
    "exitTime": 8.0,
    "isDungeonDone": 1,
    "transition": {}
  }
}