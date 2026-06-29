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
      40468002
    ],
    "num": 0,
    "transition": {}
  },
  "1023": {
    "type": "createNPC",
    "entityID": [
      40464002,
      40464003,
      40464004
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
    "taskID": 86010286,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1047,
        1050
      ]
    }
  },
  "1047": {
    "type": "createMonster",
    "entityID": [
      40460002,
      40460003,
      40460004,
      40460005,
      40460006,
      40460007,
      40460008,
      40460009,
      40460010,
      40460011,
      40460012,
      40460013
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
        1048
      ]
    }
  },
  "1048": {
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
        1049
      ]
    }
  },
  "1049": {
    "type": "createMonster",
    "entityID": [
      40460014
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
  },
  "1050": {
    "type": "removeNPC",
    "entityID": [
      40464002,
      40464003,
      40464004
    ],
    "transition": {}
  }
}