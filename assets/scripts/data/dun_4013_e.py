datas ={
  "1003": {
    "type": "createNPC",
    "entityID": [
      40134001,
      40134002,
      40134003
    ],
    "num": 0,
    "lv": "5",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1003,
        1020,
        1031,
        1037
      ]
    }
  },
  "1020": {
    "type": "createRebornPos",
    "entityID": [
      40138002
    ],
    "num": 0,
    "transition": {}
  },
  "1031": {
    "type": "taskFinished",
    "taskID": 86010142,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1032,
        1034
      ]
    }
  },
  "1032": {
    "type": "removeNPC",
    "entityID": [
      40134001,
      40134002,
      40134003
    ],
    "transition": {}
  },
  "1034": {
    "type": "createMonster",
    "entityID": [
      40130001,
      40130002,
      40130003,
      40130008,
      40130009,
      40130010,
      40130011,
      40130012,
      40130013,
      40130014,
      40130015,
      40130016
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
  "1036": {
    "type": "createMonster",
    "entityID": [
      40130007
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
        1038,
        1040,
        1042
      ]
    }
  },
  "1037": {
    "type": "taskFinished",
    "taskID": 86010144,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1036
      ]
    }
  },
  "1038": {
    "type": "monsterHp",
    "monsterID": [
      40130007
    ],
    "compare": 1,
    "hpPercent": 80.0,
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
      40130007
    ],
    "dialogID": 19900465,
    "transition": {}
  },
  "1040": {
    "type": "monsterHp",
    "monsterID": [
      40130007
    ],
    "compare": 1,
    "hpPercent": 40.0,
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
      40130007
    ],
    "dialogID": 19900466,
    "transition": {}
  },
  "1042": {
    "type": "monsterHp",
    "monsterID": [
      40130007
    ],
    "compare": 1,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1043
      ]
    }
  },
  "1043": {
    "type": "popupdialog",
    "entityID": [
      40130007
    ],
    "dialogID": 19900467,
    "transition": {}
  }
}