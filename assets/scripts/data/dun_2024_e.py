datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20230001
    ],
    "num": 0,
    "lv": "60",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 1,
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
        1013
      ]
    }
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 20.0,
    "transition": {}
  },
  "1009": {
    "type": "monsterInBattle",
    "monsterID": [
      20230001
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1020,
        1021,
        1031,
        1006
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
  "1005": {
    "type": "dunEnd",
    "exitTime": 15.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1006": {
    "type": "monsterRestNum",
    "monsterID": [
      20230001
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1011
      ]
    }
  },
  "1011": {
    "type": "popupdialog",
    "entityID": [
      20230001
    ],
    "dialogID": 19023008,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1021": {
    "type": "monsterHp",
    "monsterID": [
      20230001
    ],
    "compare": 5,
    "hpPercent": 60.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1022,
        1102
      ]
    }
  },
  "1031": {
    "type": "monsterHp",
    "monsterID": [
      20230001
    ],
    "compare": 5,
    "hpPercent": 30.0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1023,
        1024
      ]
    }
  },
  "1022": {
    "type": "castSkill",
    "entityID": [
      20230001
    ],
    "skillID": 91034025,
    "lv": "1",
    "forceToUse": 0,
    "transition": {}
  },
  "1102": {
    "type": "popupdialog",
    "entityID": [
      20230001
    ],
    "dialogID": 19023003,
    "transition": {}
  },
  "1020": {
    "type": "popupdialog",
    "entityID": [
      20230001
    ],
    "dialogID": 19023001,
    "transition": {}
  },
  "1023": {
    "type": "castSkill",
    "entityID": [
      20230001
    ],
    "skillID": 0,
    "lv": "1",
    "forceToUse": 0,
    "transition": {}
  },
  "1024": {
    "type": "popupdialog",
    "entityID": [
      20230001
    ],
    "dialogID": 19023004,
    "transition": {}
  }
}