datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1046,
        1047
      ]
    }
  },
  "1046": {
    "type": "createRebornPos",
    "entityID": [
      40288002
    ],
    "num": 0,
    "transition": {}
  },
  "1047": {
    "type": "createMonster",
    "entityID": [
      40280001,
      40280003,
      40280004,
      40280009,
      40280010,
      40280011
    ],
    "num": 0,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1056
      ]
    }
  },
  "1056": {
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
        1057
      ]
    }
  },
  "1057": {
    "type": "createMonster",
    "entityID": [
      40280005,
      40280006,
      40280007,
      40280012,
      40280013,
      40280014
    ],
    "num": 0,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1058
      ]
    }
  },
  "1058": {
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
        1059
      ]
    }
  },
  "1059": {
    "type": "createMonster",
    "entityID": [
      40280008
    ],
    "num": 0,
    "lv": "1",
    "initState": 0,
    "hp": 0,
    "minAtk": 0,
    "maxAtk": 0,
    "ifSetBoss": 0,
    "aiName": 0,
    "hpPercent": 0.0,
    "transition": {
      "finished": [
        1061
      ]
    }
  },
  "1060": {
    "type": "createCollection",
    "entityID": [
      40028003
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1062
      ]
    }
  },
  "1061": {
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
        1060
      ]
    }
  },
  "1062": {
    "type": "collBeCollected",
    "entityID": [
      40028003
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1063
      ]
    }
  },
  "1063": {
    "type": "createNPC",
    "entityID": [
      40024001
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  }
}