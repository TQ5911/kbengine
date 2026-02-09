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
        1013,
        1025,
        1026,
        1028,
        1043
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
      40030004,
      40030005,
      40030006,
      40030015,
      40030016,
      40030017,
      40030018,
      40030019,
      40030020,
      40030021,
      40030022,
      40030023
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
      40030024,
      40030025,
      40030026,
      40030027,
      40030028,
      40030029,
      40030030,
      40030031,
      40030032,
      40030033,
      40030034,
      40030035
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
    "transition": {
      "finished": [
        1038
      ]
    }
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
    "lv": "6",
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
    "lv": "6",
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
    "lv": "6",
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
    "lv": "6",
    "initState": 0,
    "hp": 220,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1038": {
    "type": "monsterHp",
    "monsterID": [
      40030008
    ],
    "compare": 5,
    "hpPercent": 60.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1039
      ]
    }
  },
  "1039": {
    "type": "popupdialog",
    "entityID": [
      40030008
    ],
    "dialogID": 19900388,
    "transition": {
      "finished": [
        1040
      ]
    }
  },
  "1040": {
    "type": "monsterHp",
    "monsterID": [
      40030008
    ],
    "compare": 5,
    "hpPercent": 20.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1041
      ]
    }
  },
  "1041": {
    "type": "popupdialog",
    "entityID": [
      40030008
    ],
    "dialogID": 19900389,
    "transition": {}
  },
  "1043": {
    "type": "addBuffToMonster",
    "monsterID": [
      40030009,
      40030010,
      40030011,
      40030012
    ],
    "buffID": [
      64004998
    ],
    "lv": "6",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  }
}