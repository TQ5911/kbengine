datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40040004
    ],
    "num": 0,
    "lv": "12",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1004": {
    "type": "delayLoop",
    "firstDelay": 1800.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1015,
        1004,
        1016
      ]
    }
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 5.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40040003
    ],
    "num": 0,
    "transition": {}
  },
  "1016": {
    "type": "monsterHp",
    "monsterID": [
      40040004
    ],
    "compare": 2,
    "hpPercent": 30.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1017
      ]
    }
  },
  "1017": {
    "type": "popupdialog",
    "entityID": [
      40040004
    ],
    "dialogID": 19900314,
    "transition": {}
  }
}