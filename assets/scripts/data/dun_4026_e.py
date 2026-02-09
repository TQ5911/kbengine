datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40260001,
      40260002,
      40260003
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
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1020,
        1031,
        1039,
        1042,
        1044
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40218002
    ],
    "num": 0,
    "transition": {}
  },
  "1031": {
    "type": "taskFinished",
    "taskID": 86010188,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1032
      ]
    }
  },
  "1032": {
    "type": "createMonster",
    "entityID": [
      40260004,
      40260006
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
        1033,
        1035
      ]
    }
  },
  "1033": {
    "type": "monsterHp",
    "monsterID": [
      40260006
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1036
      ]
    }
  },
  "1035": {
    "type": "monsterHp",
    "monsterID": [
      40260007
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1038
      ]
    }
  },
  "1036": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      0
    ],
    "entityID": [
      40268003
    ],
    "num": 0,
    "transition": {}
  },
  "1038": {
    "type": "createCreationInFixedPosition",
    "monsterID": [
      0
    ],
    "entityID": [
      40268004
    ],
    "num": 0,
    "transition": {}
  },
  "1039": {
    "type": "taskFinished",
    "taskID": 86010189,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1040,
        1041
      ]
    }
  },
  "1040": {
    "type": "createMonster",
    "entityID": [
      40260007,
      40260008,
      40260009,
      40260010,
      40260011
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
  "1041": {
    "type": "createMonster",
    "entityID": [
      40260012,
      40260013,
      40260014,
      40260015
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
  "1042": {
    "type": "taskFinished",
    "taskID": 86010191,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1043
      ]
    }
  },
  "1043": {
    "type": "createMonster",
    "entityID": [
      40260016,
      40260017,
      40260018,
      40260019,
      40260020
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
  "1044": {
    "type": "taskFinished",
    "taskID": 86010192,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1045
      ]
    }
  },
  "1045": {
    "type": "createMonster",
    "entityID": [
      40260021,
      40260022,
      40260023,
      40260024,
      40260025
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