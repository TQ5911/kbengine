datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1031,
        1038
      ]
    }
  },
  "1013": {
    "type": "monsterHp",
    "monsterID": [
      40070001
    ],
    "compare": 1,
    "hpPercent": 30.0,
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
      40070001,
      40070002,
      40070003
    ],
    "num": 1,
    "lv": "1",
    "initState": 0,
    "hp": 220,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1013
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
    "type": "showPopoverMsg",
    "entityID": [
      40070001
    ],
    "messageID": 19900193,
    "transition": {}
  }
}