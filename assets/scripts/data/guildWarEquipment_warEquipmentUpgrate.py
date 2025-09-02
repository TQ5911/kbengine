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
        "type": 1,
        "level": 6,
        "prop": 51004006,
        "upgradeCost": 6000,
        "upgradeExp": 6000,
        "assistExp": 60,
        "upgradeCoinCost": 900,
        "buildingLvReq": 6
    }),
    7: _tools.RODict({
        "ID": 7,
        "type": 1,
        "level": 7,
        "prop": 51004007,
        "upgradeCost": 7000,
        "upgradeExp": 7000,
        "assistExp": 70,
        "upgradeCoinCost": 1000,
        "buildingLvReq": 7
    }),
    8: _tools.RODict({
        "ID": 8,
        "type": 3,
        "level": 1,
        "prop": 51006001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    9: _tools.RODict({
        "ID": 9,
        "type": 3,
        "level": 2,
        "prop": 51006002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    10: _tools.RODict({
        "ID": 10,
        "type": 3,
        "level": 3,
        "prop": 51006003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    11: _tools.RODict({
        "ID": 11,
        "type": 3,
        "level": 4,
        "prop": 51006004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    12: _tools.RODict({
        "ID": 12,
        "type": 3,
        "level": 5,
        "prop": 51006005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    }),
    13: _tools.RODict({
        "ID": 13,
        "type": 3,
        "level": 6,
        "prop": 51006006,
        "upgradeCost": 6000,
        "upgradeExp": 6000,
        "assistExp": 60,
        "upgradeCoinCost": 900,
        "buildingLvReq": 6
    }),
    14: _tools.RODict({
        "ID": 14,
        "type": 3,
        "level": 7,
        "prop": 51006007,
        "upgradeCost": 7000,
        "upgradeExp": 7000,
        "assistExp": 70,
        "upgradeCoinCost": 1000,
        "buildingLvReq": 7
    }),
    15: _tools.RODict({
        "ID": 15,
        "type": 4,
        "level": 1,
        "prop": 51007001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    16: _tools.RODict({
        "ID": 16,
        "type": 4,
        "level": 2,
        "prop": 51007002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    17: _tools.RODict({
        "ID": 17,
        "type": 4,
        "level": 3,
        "prop": 51007003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    18: _tools.RODict({
        "ID": 18,
        "type": 4,
        "level": 4,
        "prop": 51007004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    19: _tools.RODict({
        "ID": 19,
        "type": 4,
        "level": 5,
        "prop": 51007005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    }),
    20: _tools.RODict({
        "ID": 20,
        "type": 4,
        "level": 6,
        "prop": 51007006,
        "upgradeCost": 6000,
        "upgradeExp": 6000,
        "assistExp": 60,
        "upgradeCoinCost": 900,
        "buildingLvReq": 6
    }),
    21: _tools.RODict({
        "ID": 21,
        "type": 4,
        "level": 7,
        "prop": 51007007,
        "upgradeCost": 7000,
        "upgradeExp": 7000,
        "assistExp": 70,
        "upgradeCoinCost": 1000,
        "buildingLvReq": 7
    }),
    22: _tools.RODict({
        "ID": 22,
        "type": 5,
        "level": 1,
        "prop": 51008001,
        "upgradeCost": 1000,
        "upgradeExp": 1000,
        "assistExp": 10,
        "upgradeCoinCost": 400,
        "buildingLvReq": 1
    }),
    23: _tools.RODict({
        "ID": 23,
        "type": 5,
        "level": 2,
        "prop": 51008002,
        "upgradeCost": 2000,
        "upgradeExp": 2000,
        "assistExp": 20,
        "upgradeCoinCost": 500,
        "buildingLvReq": 2
    }),
    24: _tools.RODict({
        "ID": 24,
        "type": 5,
        "level": 3,
        "prop": 51008003,
        "upgradeCost": 3000,
        "upgradeExp": 3000,
        "assistExp": 30,
        "upgradeCoinCost": 600,
        "buildingLvReq": 3
    }),
    25: _tools.RODict({
        "ID": 25,
        "type": 5,
        "level": 4,
        "prop": 51008004,
        "upgradeCost": 4000,
        "upgradeExp": 4000,
        "assistExp": 40,
        "upgradeCoinCost": 700,
        "buildingLvReq": 4
    }),
    26: _tools.RODict({
        "ID": 26,
        "type": 5,
        "level": 5,
        "prop": 51008005,
        "upgradeCost": 5000,
        "upgradeExp": 5000,
        "assistExp": 50,
        "upgradeCoinCost": 800,
        "buildingLvReq": 5
    }),
    27: _tools.RODict({
        "ID": 27,
        "type": 5,
        "level": 6,
        "prop": 51008006,
        "upgradeCost": 6000,
        "upgradeExp": 6000,
        "assistExp": 60,
        "upgradeCoinCost": 900,
        "buildingLvReq": 6
    }),
    28: _tools.RODict({
        "ID": 28,
        "type": 5,
        "level": 7,
        "prop": 51008007,
        "upgradeCost": 7000,
        "upgradeExp": 7000,
        "assistExp": 70,
        "upgradeCoinCost": 1000,
        "buildingLvReq": 7
    })
})
minKey = 1
maxKey = 28

typeLevelDic = _tools.RODict({
    1 : _tools.RODict({
        1 : 1,
        2 : 2,
        3 : 3,
        4 : 4,
        5 : 5,
        6 : 6,
        7 : 7,
    }),
    3 : _tools.RODict({
        1 : 8,
        2 : 9,
        3 : 10,
        4 : 11,
        5 : 12,
        6 : 13,
        7 : 14,
    }),
    4 : _tools.RODict({
        1 : 15,
        2 : 16,
        3 : 17,
        4 : 18,
        5 : 19,
        6 : 20,
        7 : 21,
    }),
    5 : _tools.RODict({
        1 : 22,
        2 : 23,
        3 : 24,
        4 : 25,
        5 : 26,
        6 : 27,
        7 : 28,
    }),
})
