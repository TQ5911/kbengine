datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1064,
        1015
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40568002
    ],
    "num": 0,
    "transition": {}
  },
  "1064": {
    "type": "createMonster",
    "entityID": [
      40560001,
      40560002,
      40560003,
      40560004,
      40560005,
      40560006,
      40560007,
      40560008,
      40560009
    ],
    "num": 0,
    "lv": "25",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1065
      ]
    }
  },
  "1065": {
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
        1066
      ]
    }
  },
  "1066": {
    "type": "createMonster",
    "entityID": [
      40560010,
      40560011,
      40560012,
      40560013,
      40560014,
      40560015,
      40560016,
      40560017,
      40560018,
      40560019,
      40560020,
      40560021
    ],
    "num": 0,
    "lv": "25",
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