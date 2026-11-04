datas ={
  "1001": {
    "type": "dunStart",
    "transition": {
      "finished": [
        1015,
        1075,
        1102
      ]
    }
  },
  "1015": {
    "type": "createRebornPos",
    "entityID": [
      40698002
    ],
    "num": 0,
    "transition": {}
  },
  "1075": {
    "type": "createNPC",
    "entityID": [
      40694001,
      40694002,
      40694003,
      40694004,
      40694005,
      40694006,
      40694008,
      40694009,
      40694010,
      40694011,
      40694012
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1102": {
    "type": "createCollection",
    "entityID": [
      40698004
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1103
      ]
    }
  },
  "1103": {
    "type": "collBeCollected",
    "entityID": [
      40698004
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1104,
        1105
      ]
    }
  },
  "1104": {
    "type": "removeNPC",
    "entityID": [
      40694001,
      40694002,
      40694003,
      40694005
    ],
    "transition": {}
  },
  "1105": {
    "type": "createCollection",
    "entityID": [
      40698005
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1106
      ]
    }
  },
  "1106": {
    "type": "collBeCollected",
    "entityID": [
      40698005
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1107,
        1108
      ]
    }
  },
  "1107": {
    "type": "removeNPC",
    "entityID": [
      40694004,
      40694006
    ],
    "transition": {}
  },
  "1108": {
    "type": "createCollection",
    "entityID": [
      40698007
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {
      "finished": [
        1109
      ]
    }
  },
  "1109": {
    "type": "collBeCollected",
    "entityID": [
      40698007
    ],
    "usePrototypeID": 0,
    "infLoop": 1,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1110,
        1111
      ]
    }
  },
  "1110": {
    "type": "removeNPC",
    "entityID": [
      40694008,
      40694009,
      40694010,
      40694011,
      40694012
    ],
    "transition": {}
  },
  "1111": {
    "type": "createNPC",
    "entityID": [
      40694007
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {
      "finished": [
        1112
      ]
    }
  },
  "1112": {
    "type": "taskFinished",
    "taskID": 86010486,
    "checkNow": 0,
    "checkOnce": 0,
    "transition": {
      "finished": [
        1113,
        1114,
        1115
      ]
    }
  },
  "1113": {
    "type": "createCollection",
    "entityID": [
      40698006
    ],
    "num": 0,
    "randomCollectionNum": 0,
    "checkHaveInFixed": 0,
    "transition": {}
  },
  "1114": {
    "type": "createNPC",
    "entityID": [
      40694013
    ],
    "num": 0,
    "lv": "1",
    "ifSetBoss": 0,
    "transition": {}
  },
  "1115": {
    "type": "removeNPC",
    "entityID": [
      40694007
    ],
    "transition": {}
  }
}