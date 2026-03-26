datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40230002,
      40230003,
      40230005,
      40230006,
      40230007,
      40230008,
      40230011,
      40230012,
      40230013,
      40230014
    ],
    "num": 0,
    "lv": "34",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1031
      ]
    }
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1020,
        1032,
        1034,
        1036,
        1040,
        1044
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40238002
    ],
    "num": 0,
    "transition": {}
  },
  "1031": {
    "type": "stopAiTick",
    "entityID": [
      40230002,
      40230003,
      40230011,
      40230012,
      40230013,
      40230014
    ],
    "transition": {}
  },
  "1032": {
    "type": "taskFinished",
    "taskID": 86010164,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1033
      ]
    }
  },
  "1033": {
    "type": "startAiTick",
    "entityID": [
      40230002,
      40230003
    ],
    "transition": {}
  },
  "1034": {
    "type": "monsterHp",
    "monsterID": [
      40230009
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1035
      ]
    }
  },
  "1035": {
    "type": "startAiTick",
    "entityID": [
      40230011,
      40230012,
      40230013,
      40230014
    ],
    "transition": {}
  },
  "1036": {
    "type": "taskFinished",
    "taskID": 86010165,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1037
      ]
    }
  },
  "1037": {
    "type": "createMonster",
    "entityID": [
      40230009
    ],
    "num": 0,
    "lv": "34",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1040": {
    "type": "taskFinished",
    "taskID": 86010167,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1041
      ]
    }
  },
  "1041": {
    "type": "createMonster",
    "entityID": [
      40230015,
      40230016,
      40230017,
      40230020,
      40230021
    ],
    "num": 0,
    "lv": "34",
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
    "taskID": 86010168,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {}
  },
  "1043": {
    "type": "createMonster",
    "entityID": [
      40230022,
      40230023,
      40230024,
      40230025
    ],
    "num": 0,
    "lv": "34",
    "initState": 0,
    "hp": 999999,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {}
  },
  "1044": {
    "type": "taskFinished",
    "taskID": 86010169,
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
      40230001
    ],
    "num": 0,
    "lv": "34",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1048,
        1050,
        1052,
        1054,
        1056
      ]
    }
  },
  "1048": {
    "type": "monsterHp",
    "monsterID": [
      40230001
    ],
    "compare": 5,
    "hpPercent": 90.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1049
      ]
    }
  },
  "1049": {
    "type": "popupdialog",
    "entityID": [
      40230001
    ],
    "dialogID": 19900489,
    "transition": {}
  },
  "1050": {
    "type": "monsterHp",
    "monsterID": [
      40230001
    ],
    "compare": 5,
    "hpPercent": 60.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1051
      ]
    }
  },
  "1051": {
    "type": "popupdialog",
    "entityID": [
      40230001
    ],
    "dialogID": 19900491,
    "transition": {}
  },
  "1052": {
    "type": "monsterHp",
    "monsterID": [
      40230001
    ],
    "compare": 5,
    "hpPercent": 40.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1053
      ]
    }
  },
  "1053": {
    "type": "popupdialog",
    "entityID": [
      40230001
    ],
    "dialogID": 19900493,
    "transition": {}
  },
  "1054": {
    "type": "monsterHp",
    "monsterID": [
      40230001
    ],
    "compare": 5,
    "hpPercent": 20.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1055
      ]
    }
  },
  "1055": {
    "type": "popupdialog",
    "entityID": [
      40230001
    ],
    "dialogID": 19900494,
    "transition": {}
  },
  "1056": {
    "type": "monsterHp",
    "monsterID": [
      40230001
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1057
      ]
    }
  },
  "1057": {
    "type": "popupdialog",
    "entityID": [
      40230001
    ],
    "dialogID": 19900495,
    "transition": {}
  },
  "1058": {
    "type": "taskFinished",
    "taskID": 86010170,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1059
      ]
    }
  },
  "1059": {
    "type": "transferToTheDesignatedMap",
    "mapId": 1021,
    "posX": 278.0,
    "posY": 119.0,
    "posZ": 451.0,
    "angle": 25,
    "transition": {}
  }
}