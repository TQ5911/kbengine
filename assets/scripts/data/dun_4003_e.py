datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1031,
        1032,
        1033,
        1011,
        1034,
        1035,
        1036,
        1037,
        1013,
        1025,
        1026,
        1028
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1011": {
    "type": "createMonster",
    "entityID": [
      40030004
    ],
    "num": 5,
    "lv": "10",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1013": {
    "type": "taskFinished",
    "taskID": 86060031,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1022
      ]
    }
  },
  "1014": {
    "type": "createMonster",
    "entityID": [
      40030007
    ],
    "num": 5,
    "lv": "10",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1015": {
    "type": "createMonster",
    "entityID": [
      40030008
    ],
    "num": 1,
    "lv": "11",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1019": {
    "type": "taskFinished",
    "taskID": 86060032,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1023
      ]
    }
  },
  "1022": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1014,
        1019
      ]
    }
  },
  "1023": {
    "type": "integrationEvent",
    "transition": {
      "finished": [
        1015
      ]
    }
  },
  "1025": {
    "type": "taskInProgress",
    "taskID": 86060032,
    "transition": {
      "finished": [
        1022
      ]
    }
  },
  "1026": {
    "type": "taskInProgress",
    "taskID": 86060033,
    "transition": {
      "finished": [
        1023
      ]
    }
  },
  "1028": {
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
  "1031": {
    "type": "createMonster",
    "entityID": [
      40030009
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
    "transition": {}
  },
  "1032": {
    "type": "createMonster",
    "entityID": [
      40030010
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
    "transition": {}
  },
  "1033": {
    "type": "createMonster",
    "entityID": [
      40030011
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
    "transition": {}
  },
  "1034": {
    "type": "createMonster",
    "entityID": [
      40030012
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
    "transition": {}
  },
  "1035": {
    "type": "createMonster",
    "entityID": [
      40030005
    ],
    "num": 5,
    "lv": "10",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1036": {
    "type": "createMonster",
    "entityID": [
      40030013
    ],
    "num": 3,
    "lv": "10",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1037": {
    "type": "createMonster",
    "entityID": [
      40030014
    ],
    "num": 2,
    "lv": "10",
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