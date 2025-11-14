# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: character/charData
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

import utils
import gameconst
import random
import math
import KBEngine
datas = _tools.RODict({ 
    1001: _tools.RODict({
        "ID": 1001,
        "name": "道士",
        "isOpen": 2,
        "classType": 2,
        "propType": 3,
        "excludePropType": 1,
        "bornAction": None,
        "build": _tools.ROList([90010001, 90010015, 90010040, 90010020, 90010010, 90010005, 90010025, 90010045, 90010050, 90010035, 90010055, 90010030, 90010060]),
        "ult": 90010065,
        "dodgeSkillID": 90010070,
        "selectablility": 1,
        "bePushedDistance": 0.0,
        "bePushedSpeed": 0.0,
        "bePushedExTime": 0.0,
        "baseFullHp": 400,
        "baseFullMp": 80,
        "baseSpeed": 6.0,
        "baseMinPhysicalAtk": 4,
        "baseMaxPhysicalAtk": 12,
        "baseMinMagicAtk": 20,
        "baseMaxMagicAtk": 60,
        "baseMinPhysicalArmor": 8,
        "baseMaxPhysicalArmor": 24,
        "baseMinMagicArmor": 8,
        "baseMaxMagicArmor": 24,
        "baseDrugsQuantity": 2,
        "baseHit": 0,
        "baseDodge": 0,
        "overRange": 4,
    }),
    1002: _tools.RODict({
        "ID": 1002,
        "name": "法师",
        "isOpen": 2,
        "classType": 2,
        "propType": 2,
        "excludePropType": 1,
        "bornAction": None,
        "build": _tools.ROList([90020001, 90020020, 90020010, 90020025, 90020015, 90020035, 90020055, 90020045, 90020040, 90020005, 90020030, 90020050, 90020060]),
        "ult": 90020065,
        "dodgeSkillID": 90020070,
        "selectablility": 1,
        "bePushedDistance": 0.0,
        "bePushedSpeed": 0.0,
        "bePushedExTime": 0.0,
        "baseFullHp": 400,
        "baseFullMp": 80,
        "baseSpeed": 6.0,
        "baseMinPhysicalAtk": 4,
        "baseMaxPhysicalAtk": 12,
        "baseMinMagicAtk": 20,
        "baseMaxMagicAtk": 60,
        "baseMinPhysicalArmor": 8,
        "baseMaxPhysicalArmor": 24,
        "baseMinMagicArmor": 8,
        "baseMaxMagicArmor": 24,
        "baseDrugsQuantity": 2,
        "baseHit": 0,
        "baseDodge": 0,
        "overRange": 4,
    }),
    1003: _tools.RODict({
        "ID": 1003,
        "name": "战士",
        "isOpen": 1,
        "classType": 1,
        "propType": 1,
        "excludePropType": 2,
        "bornAction": None,
        "build": _tools.ROList([90030020, 90030075, 90030015, 90030040, 90030060, 90030065, 90030045, 90030070, 90030030, 90030050, 90030055, 90030005, 90030010]),
        "ult": 90030001,
        "dodgeSkillID": 90030035,
        "selectablility": 1,
        "bePushedDistance": 0.0,
        "bePushedSpeed": 0.0,
        "bePushedExTime": 0.0,
        "baseFullHp": 400,
        "baseFullMp": 80,
        "baseSpeed": 6.0,
        "baseMinPhysicalAtk": 20,
        "baseMaxPhysicalAtk": 60,
        "baseMinMagicAtk": 4,
        "baseMaxMagicAtk": 12,
        "baseMinPhysicalArmor": 8,
        "baseMaxPhysicalArmor": 24,
        "baseMinMagicArmor": 8,
        "baseMaxMagicArmor": 24,
        "baseDrugsQuantity": 2,
        "baseHit": 0,
        "baseDodge": 0,
        "overRange": 4,
    })
})
minKey = 1001
maxKey = 1003

allSchoolList = [1001, 1002, 1003]

