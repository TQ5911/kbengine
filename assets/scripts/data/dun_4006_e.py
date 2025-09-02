datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40060003,
      40060004,
      40060005,
      40060006,
      40060007
    ],
    "num": 1,
    "lv": "2",
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
        1008
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1014,
        1012,
        1009,
        1030,
        1010,
        1011,
        1023,
        1004,
        1029
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1009": {
    "type": "taskInProgress",
    "taskID": 86060023,
    "transition": {
      "finished": [
        1013
      ]
    }
  },
  "1010": {
    "type": "taskInProgress",
    "taskID": 86060024,
    "transition": {
      "finished": [
        1019
      ]
    }
  },
  "1011": {
    "type": "taskInProgress",
    "taskID": 86060025,
    "transition": {
      "finished": [
        1022
      ]
    }
  },
  "1013": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1015,
        1018
      ]
    }
  },
  "1014": {
    "type": "taskFinished",
    "taskID": 86060022,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1016
      ]
    }
  },
  "1015": {
    "type": "createMonster",
    "entityID": [
      40060008
    ],
    "num": 6,
    "lv": "2",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1017": {
    "type": "createMonster",
    "entityID": [
      40060010,
      40060011,
      40060012
    ],
    "num": 2,
    "lv": "2",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1018": {
    "type": "taskFinished",
    "taskID": 86060041,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1019
      ]
    }
  },
  "1019": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1017,
        1024
      ]
    }
  },
  "1020": {
    "type": "createMonster",
    "entityID": [
      40060009
    ],
    "num": 1,
    "lv": "3",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1022": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1020,
        1026
      ]
    }
  },
  "1021": {
    "type": "createMonster",
    "entityID": [
      40060009
    ],
    "num": 1,
    "lv": "3",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1023": {
    "type": "taskInProgress",
    "taskID": 86060026,
    "transition": {
      "finished": [
        1027
      ]
    }
  },
  "1024": {
    "type": "taskFinished",
    "taskID": 86060024,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1022
      ]
    }
  },
  "1026": {
    "type": "taskFinished",
    "taskID": 86060025,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1027
      ]
    }
  },
  "1027": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1021
      ]
    }
  },
  "1029": {
    "type": "createAirWall",
    "entityID": [
      40068002,
      40068003,
      40068004,
      40068005,
      40068006,
      40068007,
      40068008,
      40068009,
      40068010
    ],
    "num": 1,
    "transition": {}
  },
  "1016": {
    "type": "taskFinished",
    "taskID": 86060040,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1013
      ]
    }
  },
  "1012": {
    "type": "taskInProgress",
    "taskID": 86060040,
    "transition": {
      "finished": [
        1016
      ]
    }
  },
  "1030": {
    "type": "taskInProgress",
    "taskID": 86060041,
    "transition": {
      "finished": [
        1018
      ]
    }
  }
}