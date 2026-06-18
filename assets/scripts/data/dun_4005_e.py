datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40050005,
      40050006,
      40050007,
      40050008,
      40050009,
      40050010,
      40050011,
      40050012,
      40050013,
      40050014,
      40050015,
      40050016
    ],
    "num": 0,
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
        1047
      ]
    }
  },
  "1004": {
    "type": "delayLoop",
    "firstDelay": 1800.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1008
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1004,
        1046
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1046": {
    "type": "createRebornPos",
    "entityID": [
      40058001
    ],
    "num": 0,
    "transition": {}
  },
  "1047": {
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
        1048
      ]
    }
  },
  "1048": {
    "type": "createMonster",
    "entityID": [
      40050003
    ],
    "num": 0,
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
        1049
      ]
    }
  },
  "1049": {
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
        1050
      ]
    }
  },
  "1050": {
    "type": "createNPC",
    "entityID": [
      40054001,
      40054002
    ],
    "num": 0,
    "lv": "30",
    "ifSetBoss": 0,
    "transition": {}
  }
}