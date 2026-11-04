datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1015,
        1107
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40658002
    ],
    "num": 0,
    "transition": {}
  },
  "1095": {
    "type": "jumpCinemaPlay",
    "cinemaPlayID": 98010030,
    "exitTime": 9.3,
    "transition": {
      "finished": [
        1096
      ]
    }
  },
  "1096": {
    "type": "createMonster",
    "entityID": [
      40650001
    ],
    "num": 0,
    "lv": "48",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1097,
        1098,
        1099,
        1100,
        1105
      ]
    }
  },
  "1097": {
    "type": "monsterHp",
    "monsterID": [
      40650001
    ],
    "compare": 2,
    "hpPercent": 90.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1101
      ]
    }
  },
  "1098": {
    "type": "monsterHp",
    "monsterID": [
      40650001
    ],
    "compare": 2,
    "hpPercent": 70.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1102
      ]
    }
  },
  "1099": {
    "type": "monsterHp",
    "monsterID": [
      40650001
    ],
    "compare": 2,
    "hpPercent": 50.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1103
      ]
    }
  },
  "1100": {
    "type": "monsterHp",
    "monsterID": [
      40650001
    ],
    "compare": 2,
    "hpPercent": 20.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1104
      ]
    }
  },
  "1101": {
    "type": "popupdialog",
    "entityID": [
      40650001
    ],
    "dialogID": 19900761,
    "transition": {}
  },
  "1102": {
    "type": "popupdialog",
    "entityID": [
      40650001
    ],
    "dialogID": 19900762,
    "transition": {}
  },
  "1103": {
    "type": "popupdialog",
    "entityID": [
      40650001
    ],
    "dialogID": 19900763,
    "transition": {}
  },
  "1104": {
    "type": "popupdialog",
    "entityID": [
      40650001
    ],
    "dialogID": 19900764,
    "transition": {}
  },
  "1105": {
    "type": "monsterHp",
    "monsterID": [
      40650001
    ],
    "compare": 5,
    "hpPercent": 0.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1106
      ]
    }
  },
  "1106": {
    "type": "popupdialog",
    "entityID": [
      40650001
    ],
    "dialogID": 19900765,
    "transition": {}
  },
  "1107": {
    "type": "taskFinished",
    "taskID": 86010549,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1111
      ]
    }
  },
  "1111": {
    "type": "castCinemaPlay",
    "cinemaPlayID": 98010030,
    "transition": {
      "finished": [
        1095
      ]
    }
  }
}