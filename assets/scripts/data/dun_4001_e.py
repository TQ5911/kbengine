datas ={
  "1002": {
    "type": "createNPC",
    "entityID": [
      40010004,
      40010005
    ],
    "num": 1,
    "lv": "9",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1003": {
    "type": "delayLoop",
    "firstDelay": 1800.0,
    "loopDelay": 0.0,
    "loopNum": 1,
    "transition": {
      "finished": [
        1004
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1002,
        1017,
        1022,
        1015,
        1023,
        1024,
        1027,
        1028,
        1032,
        1003,
        1034,
        1035,
        1036
      ]
    }
  },
  "1006": {
    "type": "createMonster",
    "entityID": [
      40010006,
      40010007,
      40010008,
      40010025
    ],
    "num": 1,
    "lv": "5",
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
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1008": {
    "type": "createMonster",
    "entityID": [
      40010009,
      40010010,
      40010011,
      40010012,
      40010013,
      40010014
    ],
    "num": 1,
    "lv": "5",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1009": {
    "type": "createMonster",
    "entityID": [
      40010021,
      40010022,
      40010023,
      40010024
    ],
    "num": 1,
    "lv": "5",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1011": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1006
      ]
    }
  },
  "1012": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1008
      ]
    }
  },
  "1013": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1009,
        1025,
        1026
      ]
    }
  },
  "1015": {
    "type": "taskFinished",
    "taskID": 86060112,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1013
      ]
    }
  },
  "1017": {
    "type": "taskFinished",
    "taskID": 86060107,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1011
      ]
    }
  },
  "1022": {
    "type": "taskFinished",
    "taskID": 86060110,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1012
      ]
    }
  },
  "1024": {
    "type": "createAirWall",
    "entityID": [
      40018001,
      40018002,
      40018003,
      40018004,
      40018005,
      40018006,
      40018007,
      40018008,
      40018009,
      40018010,
      40018011,
      40018012,
      40018013,
      40018014
    ],
    "num": 1,
    "transition": {}
  },
  "1025": {
    "type": "createMonster",
    "entityID": [
      40010016,
      40010017,
      40010018,
      40010019,
      40010020
    ],
    "num": 1,
    "lv": "5",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1026": {
    "type": "createMonster",
    "entityID": [
      40010015
    ],
    "num": 1,
    "lv": "6",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1027": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64006022
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1028": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64006023
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1023": {
    "type": "taskFinished",
    "taskID": 86060113,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1029
      ]
    }
  },
  "1029": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1030,
        1031,
        1033
      ]
    }
  },
  "1030": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006022
    ],
    "transition": {}
  },
  "1031": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006023
    ],
    "transition": {}
  },
  "1032": {
    "type": "addBuffToAllPlayer",
    "buffID": [
      64006028
    ],
    "lv": "1",
    "messageID": 0,
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1033": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64006028
    ],
    "transition": {}
  },
  "1034": {
    "type": "createNPC",
    "entityID": [
      40014001
    ],
    "num": 1,
    "lv": "9",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1035": {
    "type": "createNPC",
    "entityID": [
      40014002
    ],
    "num": 1,
    "lv": "9",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1036": {
    "type": "createNPC",
    "entityID": [
      40014003,
      40014004
    ],
    "num": 1,
    "lv": "9",
    "ifSetBoss": 0,
    "transition": {}
  }
}