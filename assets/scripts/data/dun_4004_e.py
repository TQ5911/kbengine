datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40040001,
      40040002,
      40040003
    ],
    "num": 0,
    "lv": "16",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1018
      ]
    }
  },
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
      40040003
    ],
    "num": 0,
    "transition": {}
  },
  "1016": {
    "type": "monsterHp",
    "monsterID": [
      40040004
    ],
    "compare": 2,
    "hpPercent": 30.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1017
      ]
    }
  },
  "1017": {
    "type": "popupdialog",
    "entityID": [
      40040004
    ],
    "dialogID": 19900314,
    "transition": {}
  },
  "1018": {
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
        1019
      ]
    }
  },
  "1019": {
    "type": "createMonster",
    "entityID": [
      40040004,
      40040005,
      40040006,
      4004007,
      40040008,
      40040009
    ],
    "num": 0,
    "lv": "16",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1020
      ]
    }
  },
  "1020": {
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
        1021
      ]
    }
  },
  "1021": {
    "type": "createNPC",
    "entityID": [
      40044001,
      40044002
    ],
    "num": 0,
    "lv": "16",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1024
      ]
    }
  },
  "1023": {
    "type": "createMonster",
    "entityID": [
      40040019,
      40040001,
      40040002,
      40040003
    ],
    "num": 0,
    "lv": "16",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1016
      ]
    }
  },
  "1024": {
    "type": "taskFinished",
    "taskID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1025,
        1026
      ]
    }
  },
  "1025": {
    "type": "removeNPC",
    "entityID": [
      40044001,
      40044002
    ],
    "transition": {}
  },
  "1026": {
    "type": "createNPC",
    "entityID": [
      40044004,
      40044005
    ],
    "num": 0,
    "lv": "16",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1027
      ]
    }
  },
  "1027": {
    "type": "taskFinished",
    "taskID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1028
      ]
    }
  },
  "1028": {
    "type": "createMonster",
    "entityID": [
      40040010,
      40040011,
      40040012,
      40040013,
      40040014,
      40040015,
      40040016,
      40040017,
      40040018,
      40040019
    ],
    "num": 0,
    "lv": "16",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1029
      ]
    }
  },
  "1029": {
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
        1030
      ]
    }
  },
  "1030": {
    "type": "createMonster",
    "entityID": [
      40040019
    ],
    "num": 0,
    "lv": "16",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1016,
        1032
      ]
    }
  },
  "1031": {
    "type": "createNPC",
    "entityID": [
      40044006
    ],
    "num": 0,
    "lv": "16",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1032": {
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
        1031
      ]
    }
  }
}