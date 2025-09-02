datas ={
  "1003": {
    "type": "createMonster",
    "entityID": [
      20080003
    ],
    "num": 1,
    "lv": "60",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1007
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
        1012
      ]
    }
  },
  "1005": {
    "type": "dunEnd",
    "exitTime": 5.0,
    "isDungeonDone": 1,
    "transition": {}
  },
  "1008": {
    "type": "dunFailed",
    "exitTime": 5.0,
    "transition": {}
  },
  "1007": {
    "type": "monsterInBattle",
    "monsterID": [
      20080003
    ],
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1009
      ]
    }
  },
  "1009": {
    "type": "popupdialog",
    "entityID": [
      20080003
    ],
    "dialogID": 19900179,
    "transition": {
      "finished": [
        1011
      ]
    }
  },
  "1010": {
    "type": "popupdialog",
    "entityID": [
      20080003
    ],
    "dialogID": 19900180,
    "transition": {
      "finished": [
        1005
      ]
    }
  },
  "1011": {
    "type": "monsterRestNum",
    "monsterID": [
      20080003
    ],
    "compare": 1,
    "restNum": 0,
    "usePrototypeID": 0,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1010
      ]
    }
  },
  "1012": {
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
  }
}