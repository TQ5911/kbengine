# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guildWarEquipment/warEquipmentUpgrate
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "ID": 1,
        "type": 1,
        "level": 1,
        "prop": 51004001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    2: _tools.RODict({
        "ID": 2,
        "type": 1,
        "level": 2,
        "prop": 51004002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    3: _tools.RODict({
        "ID": 3,
        "type": 1,
        "level": 3,
        "prop": 51004003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    4: _tools.RODict({
        "ID": 4,
        "type": 1,
        "level": 4,
        "prop": 51004004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    5: _tools.RODict({
        "ID": 5,
        "type": 1,
        "level": 5,
        "prop": 51004005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    }),
    6: _tools.RODict({
        "ID": 6,
        "type": 3,
        "level": 1,
        "prop": 51006001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    7: _tools.RODict({
        "ID": 7,
        "type": 3,
        "level": 2,
        "prop": 51006002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    8: _tools.RODict({
        "ID": 8,
        "type": 3,
        "level": 3,
        "prop": 51006003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    9: _tools.RODict({
        "ID": 9,
        "type": 3,
        "level": 4,
        "prop": 51006004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    10: _tools.RODict({
        "ID": 10,
        "type": 3,
        "level": 5,
        "prop": 51006005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    }),
    11: _tools.RODict({
        "ID": 11,
        "type": 4,
        "level": 1,
        "prop": 51007001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    12: _tools.RODict({
        "ID": 12,
        "type": 4,
        "level": 2,
        "prop": 51007002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    13: _tools.RODict({
        "ID": 13,
        "type": 4,
        "level": 3,
        "prop": 51007003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    14: _tools.RODict({
        "ID": 14,
        "type": 4,
        "level": 4,
        "prop": 51007004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    15: _tools.RODict({
        "ID": 15,
        "type": 4,
        "level": 5,
        "prop": 51007005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    }),
    16: _tools.RODict({
        "ID": 16,
        "type": 5,
        "level": 1,
        "prop": 51008001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    17: _tools.RODict({
        "ID": 17,
        "type": 5,
        "level": 2,
        "prop": 51008002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    18: _tools.RODict({
        "ID": 18,
        "type": 5,
        "level": 3,
        "prop": 51008003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    19: _tools.RODict({
        "ID": 19,
        "type": 5,
        "level": 4,
        "prop": 51008004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    20: _tools.RODict({
        "ID": 20,
        "type": 5,
        "level": 5,
        "prop": 51008005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    }),
    21: _tools.RODict({
        "ID": 21,
        "type": 6,
        "level": 1,
        "prop": 51004001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    22: _tools.RODict({
        "ID": 22,
        "type": 6,
        "level": 2,
        "prop": 51004002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    23: _tools.RODict({
        "ID": 23,
        "type": 6,
        "level": 3,
        "prop": 51004003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    24: _tools.RODict({
        "ID": 24,
        "type": 6,
        "level": 4,
        "prop": 51004004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    25: _tools.RODict({
        "ID": 25,
        "type": 6,
        "level": 5,
        "prop": 51004005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    }),
    26: _tools.RODict({
        "ID": 26,
        "type": 7,
        "level": 1,
        "prop": 51004001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    27: _tools.RODict({
        "ID": 27,
        "type": 7,
        "level": 2,
        "prop": 51004002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    28: _tools.RODict({
        "ID": 28,
        "type": 7,
        "level": 3,
        "prop": 51004003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    29: _tools.RODict({
        "ID": 29,
        "type": 7,
        "level": 4,
        "prop": 51004004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    30: _tools.RODict({
        "ID": 30,
        "type": 7,
        "level": 5,
        "prop": 51004005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    })
})
minKey = 1
maxKey = 30

typeLevelDic = _tools.RODict({
    1 : _tools.RODict({
        1 : 1,
        2 : 2,
        3 : 3,
        4 : 4,
        5 : 5,
    }),
    3 : _tools.RODict({
        1 : 6,
        2 : 7,
        3 : 8,
        4 : 9,
        5 : 10,
    }),
    4 : _tools.RODict({
        1 : 11,
        2 : 12,
        3 : 13,
        4 : 14,
        5 : 15,
    }),
    5 : _tools.RODict({
        1 : 16,
        2 : 17,
        3 : 18,
        4 : 19,
        5 : 20,
    }),
    6 : _tools.RODict({
        1 : 21,
        2 : 22,
        3 : 23,
        4 : 24,
        5 : 25,
    }),
    7 : _tools.RODict({
        1 : 26,
        2 : 27,
        3 : 28,
        4 : 29,
        5 : 30,
    }),
})
