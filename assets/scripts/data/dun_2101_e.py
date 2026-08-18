datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      21010084,
      21010085,
      21010086,
      21010087,
      21010088,
      21010089,
      21010090,
      21010091,
      21010092,
      21010093,
      21010094,
      21010095,
      21010096,
      21010097,
      21010098,
      21010099,
      21010100,
      21010101,
      21010102,
      21010103,
      21010104,
      21010105,
      21010106,
      21010107,
      21010108,
      21010109,
      21010110
    ],
    "num": 0,
    "lv": "20",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1009
      ]
    }
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
        1004,
        1013,
        1134,
        1144
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 30.0,
    "transition": {}
  },
  "1009": {
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
        1099
      ]
    }
  },
  "1013": {
    "type": "playerRestNum",
    "compare": 1,
    "num": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1008
      ]
    }
  },
  "1099": {
    "type": "createMonster",
    "entityID": [
      21010111,
      21010112,
      21010113,
      21010114,
      21010115,
      21010116,
      21010117,
      21010118,
      21010119,
      21010120,
      21010121,
      21010122,
      21010123,
      21010124,
      21010125,
      21010126,
      21010127,
      21010128,
      21010129,
      21010130,
      21010131,
      21010132,
      21010133,
      21010134,
      21010135,
      21010136,
      21010137
    ],
    "num": 0,
    "lv": "20",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1116
      ]
    }
  },
  "1116": {
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
        1117
      ]
    }
  },
  "1117": {
    "type": "createMonster",
    "entityID": [
      21010051
    ],
    "num": 0,
    "lv": "21",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1118,
        1120
      ]
    }
  },
  "1120": {
    "type": "monsterRestNum",
    "monsterID": [
      21010051
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1124,
        1011
      ]
    }
  },
  "1124": {
    "type": "createMonster",
    "entityID": [
      21010138,
      21010139,
      21010140,
      21010141,
      21010142,
      21010143,
      21010144,
      21010145,
      21010146,
      21010147,
      21010148,
      21010149,
      21010150,
      21010151,
      21010152,
      21010153,
      21010154,
      21010155,
      21010156,
      21010157,
      21010158
    ],
    "num": 0,
    "lv": "20",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1125
      ]
    }
  },
  "1125": {
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
        1126
      ]
    }
  },
  "1126": {
    "type": "createMonster",
    "entityID": [
      21010159
    ],
    "num": 0,
    "lv": "20",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1168
      ]
    }
  },
  "1128": {
    "type": "createMonster",
    "entityID": [
      21010082
    ],
    "num": 0,
    "lv": "22",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1014,
        1006
      ]
    }
  },
  "1134": {
    "type": "createNPC",
    "entityID": [
      21014003,
      21014004,
      21014005,
      21014006
    ],
    "num": 1,
    "lv": "",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1118": {
    "type": "monsterInBattle",
    "monsterID": [
      21010051
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1119,
        1147,
        1148
      ]
    }
  },
  "1119": {
    "type": "popupdialog",
    "entityID": [
      21010051
    ],
    "dialogID": 19019001,
    "transition": {}
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      21010051
    ],
    "dialogID": 19900198,
    "transition": {}
  },
  "1007": {
    "type": "dunEnd",
    "exitTime": 30.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      21010082
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1015
      ]
    }
  },
  "1014": {
    "type": "monsterInBattle",
    "monsterID": [
      21010082
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1010,
        1191,
        1999
      ]
    }
  },
  "1010": {
    "type": "popupdialog",
    "entityID": [
      21010082
    ],
    "dialogID": 19900195,
    "transition": {}
  },
  "1015": {
    "type": "popupdialog",
    "entityID": [
      21010082
    ],
    "dialogID": 19900196,
    "transition": {
      "finished": [
        1027
      ]
    }
  },
  "1027": {
    "type": "removeBuffFromAllPlayer",
    "buffID": [
      64004046
    ],
    "transition": {
      "finished": [
        1007
      ]
    }
  },
  "1144": {
    "type": "createRebornPos",
    "entityID": [
      21018002
    ],
    "num": 1,
    "transition": {}
  },
  "1147": {
    "type": "removeRebornPos",
    "entityID": [
      21018002
    ],
    "transition": {
      "finished": [
        1149
      ]
    }
  },
  "1148": {
    "type": "removeNPC",
    "entityID": [
      21014003,
      21014004,
      21014005,
      21014006
    ],
    "transition": {
      "finished": [
        1150
      ]
    }
  },
  "1149": {
    "type": "createRebornPos",
    "entityID": [
      21018003
    ],
    "num": 1,
    "transition": {}
  },
  "1150": {
    "type": "createNPC",
    "entityID": [
      21014007,
      21014008,
      21014009,
      21014010,
      21014011
    ],
    "num": 1,
    "lv": "35",
    "ifSetBoss": 1,
    "transition": {}
  },
  "1191": {
    "type": "removeRebornPos",
    "entityID": [
      21018003
    ],
    "transition": {
      "finished": [
        1998
      ]
    }
  },
  "1998": {
    "type": "createRebornPos",
    "entityID": [
      21018004
    ],
    "num": 1,
    "transition": {}
  },
  "1999": {
    "type": "removeNPC",
    "entityID": [
      21014008,
      21014009,
      21014010,
      21014011
    ],
    "transition": {
      "finished": [
        1158
      ]
    }
  },
  "1158": {
    "type": "createNPC",
    "entityID": [
      21014013,
      21014014,
      21014015,
      21014016,
      21014012
    ],
    "num": 1,
    "lv": "35",
    "ifSetBoss": 1,
    "transition": {}
  },
  "1163": {
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
        1128
      ]
    }
  },
  "1168": {
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
        1170
      ]
    }
  },
  "1170": {
    "type": "createMonster",
    "entityID": [
      21010160,
      21010161,
      21010162,
      21010163,
      21010164,
      21010165,
      21010166,
      21010167,
      21010168,
      21010169,
      21010170,
      21010171,
      21010172,
      21010173,
      21010174,
      21010175,
      21010176,
      21010177,
      21010178,
      21010179,
      21010180,
      21010181,
      21010182,
      21010183,
      21010184,
      21010185,
      21010186
    ],
    "num": 0,
    "lv": "20",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1163
      ]
    }
  }
}