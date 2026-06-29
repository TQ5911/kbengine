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
      40448002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createNPC",
    "entityID": [
      40444001,
      40444002,
      40444003,
      40444004,
      40444005
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1046
      ]
    }
  },
  "1046": {
    "type": "taskFinished",
    "taskID": 86010273,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1047,
        1048
      ]
    }
  },
  "1047": {
    "type": "createMonster",
    "entityID": [
      40440001,
      40440002,
      40440003,
      40440004,
      40440005,
      40440006,
      40440007,
      40440008,
      40440009,
      40440010,
      40440011,
      40440012
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
        1049
      ]
    }
  },
  "1048": {
    "type": "removeNPC",
    "entityID": [
      40444001,
      40444002,
      40444003,
      40444004,
      40444005
    ],
    "transition": {}
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
      40444001
    ],
    "num": 0,
    "lv": "0",
    "ifSetBoss": 0,
    "transition": {}
  }
}