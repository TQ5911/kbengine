datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      40230011,
      40230012,
      40230013,
      40230014,
      40230050,
      40230051,
      40230052,
      40230053,
      40230054,
      40230055,
      40230060,
      40230061,
      40230062,
      40230063,
      40230064,
      40230065,
      40230066,
      40230067,
      40230011,
      40230012,
      40230013,
      40230014
    ],
    "num": 0,
    "lv": "30",
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
        1032,
        1036,
        1040,
        1044,
        1061,
        1067,
        1042,
        1074,
        1076,
        1020
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
      40230011,
      40230012,
      40230013,
      40230014,
      40230050,
      40230051,
      40230052,
      40230053,
      40230054,
      40230055,
      40230060,
      40230061,
      40230062,
      40230063,
      40230064,
      40230065,
      40230066,
      40230067,
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
      40230060,
      40230061,
      40230062,
      40230063,
      40230064,
      40230065,
      40230066,
      40230067,
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
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1034
      ]
    }
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
      40230016,
      40230017,
      40230020,
      40230068,
      40230069,
      40230070,
      40230071,
      40230072,
      40230073,
      40230074,
      40230075,
      40230076,
      40230077,
      40230078,
      40230079,
      40230080,
      40230081,
      40230082,
      40230083,
      40230084,
      40230085
    ],
    "num": 0,
    "lv": "30",
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
    "taskID": 86010436,
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
      40230015
    ],
    "num": 0,
    "lv": "30",
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
    "taskID": 86010437,
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
    "lv": "30",
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
        1049,
        1079
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
        1051,
        1071
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
  },
  "1061": {
    "type": "createMonster",
    "entityID": [
      40230005,
      40230006,
      40230007,
      40230026,
      40230027,
      40230028,
      40230029,
      40230030,
      40230031
    ],
    "num": 0,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1062
      ]
    }
  },
  "1062": {
    "type": "taskFinished",
    "taskID": 86010163,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1063
      ]
    }
  },
  "1063": {
    "type": "createMonster",
    "entityID": [
      40230032,
      40230033,
      40230034,
      40230035,
      40230036,
      40230037,
      40230038,
      40230039,
      40230040,
      40230041,
      40230042,
      40230043,
      40230044,
      40230045,
      40230046,
      40230047,
      40230048,
      40230049
    ],
    "num": 0,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1064
      ]
    }
  },
  "1064": {
    "type": "taskFinished",
    "taskID": 86010164,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1066
      ]
    }
  },
  "1066": {
    "type": "startAiTick",
    "entityID": [
      40230050,
      40230051,
      40230052,
      40230053,
      40230054,
      40230055
    ],
    "transition": {}
  },
  "1067": {
    "type": "taskFinished",
    "taskID": 86010439,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1068,
        1070
      ]
    }
  },
  "1068": {
    "type": "startAiTick",
    "entityID": [
      40230090,
      40230091,
      40230092,
      40230093,
      40230094,
      40230095,
      40230096,
      40230097
    ],
    "transition": {}
  },
  "1069": {
    "type": "addBuffToMonster",
    "monsterID": [
      40230022,
      40230023,
      40230024,
      40230025,
      40230086,
      40230087,
      40230088,
      40230089
    ],
    "buffID": [
      64000140
    ],
    "lv": "1",
    "lvlmt": -1,
    "duration": -1.0,
    "transition": {}
  },
  "1070": {
    "type": "createMonster",
    "entityID": [
      40230022,
      40230023,
      40230024,
      40230025,
      40230086,
      40230087,
      40230088,
      40230089
    ],
    "num": 0,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 1,
    "maxAtk": 1,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1069
      ]
    }
  },
  "1071": {
    "type": "startAiTick",
    "entityID": [
      40230098,
      40230099,
      40230100,
      40230101,
      40230102,
      40230103,
      40230104,
      40230105,
      40230106,
      40230107,
      40230108,
      40230109
    ],
    "transition": {}
  },
  "1074": {
    "type": "createMonster",
    "entityID": [
      40230002,
      40230003,
      40230011,
      40230012,
      40230013,
      40230014,
      40230050,
      40230051,
      40230052,
      40230053,
      40230054,
      40230055,
      40230060,
      40230061,
      40230062,
      40230063,
      40230064,
      40230065,
      40230066,
      40230067
    ],
    "num": 0,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1075
      ]
    }
  },
  "1075": {
    "type": "stopAiTick",
    "entityID": [
      40230002,
      40230003,
      40230011,
      40230012,
      40230013,
      40230014,
      40230050,
      40230051,
      40230052,
      40230053,
      40230054,
      40230055,
      40230060,
      40230061,
      40230062,
      40230063,
      40230064,
      40230065,
      40230066,
      40230067
    ],
    "transition": {}
  },
  "1076": {
    "type": "taskFinished",
    "taskID": 86010169,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1077
      ]
    }
  },
  "1077": {
    "type": "createMonster",
    "entityID": [
      40230090,
      40230091,
      40230092,
      40230093,
      40230094,
      40230095,
      40230096,
      40230097
    ],
    "num": 0,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1078
      ]
    }
  },
  "1078": {
    "type": "stopAiTick",
    "entityID": [
      40230090,
      40230091,
      40230092,
      40230093,
      40230094,
      40230095,
      40230096,
      40230097
    ],
    "transition": {}
  },
  "1079": {
    "type": "createMonster",
    "entityID": [
      40230098,
      40230099,
      40230100,
      40230101,
      40230102,
      40230103,
      40230104,
      40230105,
      40230106,
      40230107,
      40230108,
      40230109
    ],
    "num": 0,
    "lv": "30",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1080
      ]
    }
  },
  "1080": {
    "type": "stopAiTick",
    "entityID": [
      40230098,
      40230099,
      40230100,
      40230101,
      40230102,
      40230103,
      40230104,
      40230105,
      40230106,
      40230107,
      40230108,
      40230109
    ],
    "transition": {}
  }
}