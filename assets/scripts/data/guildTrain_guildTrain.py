# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: guildTrain/guildTrain
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    95000001: _tools.RODict({
        "ID": 95000001,
        "name": "血气方刚",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjFullHp",
        "valueFormula": 34000018,
    }),
    95000002: _tools.RODict({
        "ID": 95000002,
        "name": "融会贯通",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjExpGrow",
        "valueFormula": 34000020,
    }),
    95000003: _tools.RODict({
        "ID": 95000003,
        "name": "神机妙算",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjFullMp",
        "valueFormula": 34000019,
    }),
    95000004: _tools.RODict({
        "ID": 95000004,
        "name": "财源广进",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjCopper",
        "valueFormula": 34000020,
    }),
    95000005: _tools.RODict({
        "ID": 95000005,
        "name": "妙手回春",
        "unlockYanWuGeLevel": 3,
        "fightProp": "adjMedicineRate",
        "valueFormula": 34000020,
    }),
    95000006: _tools.RODict({
        "ID": 95000006,
        "name": "力拔千钧",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjMaxPhysicalAtk",
        "valueFormula": 34000010,
    }),
    95000007: _tools.RODict({
        "ID": 95000007,
        "name": "气吞山河",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjMaxMagicAtk",
        "valueFormula": 34000010,
    }),
    95000008: _tools.RODict({
        "ID": 95000008,
        "name": "力能扛鼎",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjMinPhysicalAtk",
        "valueFormula": 34000010,
    }),
    95000009: _tools.RODict({
        "ID": 95000009,
        "name": "气贯长虹",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjMinMagicAtk",
        "valueFormula": 34000010,
    }),
    95000010: _tools.RODict({
        "ID": 95000010,
        "name": "猎人天性",
        "unlockYanWuGeLevel": 3,
        "fightProp": "adjMonsterDmg",
        "valueFormula": 34000011,
    }),
    95000011: _tools.RODict({
        "ID": 95000011,
        "name": "猎人天性",
        "unlockYanWuGeLevel": 3,
        "fightProp": "adjMortal",
        "valueFormula": 34000021,
    }),
    95000012: _tools.RODict({
        "ID": 95000012,
        "name": "勇猛无双",
        "unlockYanWuGeLevel": 4,
        "fightProp": "adjFinalDmg",
        "valueFormula": 34000012,
    }),
    95000013: _tools.RODict({
        "ID": 95000013,
        "name": "千军取首",
        "unlockYanWuGeLevel": 4,
        "fightProp": "adjPVPDmg",
        "valueFormula": 34000011,
    }),
    95000014: _tools.RODict({
        "ID": 95000014,
        "name": "猎人天性",
        "unlockYanWuGeLevel": 5,
        "fightProp": "adjIgnoreArmor",
        "valueFormula": 34000012,
    }),
    95000015: _tools.RODict({
        "ID": 95000015,
        "name": "铜墙铁壁",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjMaxPhysicalArmor",
        "valueFormula": 34000017,
    }),
    95000016: _tools.RODict({
        "ID": 95000016,
        "name": "万法不侵",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjMaxMagicArmor",
        "valueFormula": 34000017,
    }),
    95000017: _tools.RODict({
        "ID": 95000017,
        "name": "钢筋铁骨",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjMinPhysicalArmor",
        "valueFormula": 34000017,
    }),
    95000018: _tools.RODict({
        "ID": 95000018,
        "name": "万法归宗",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjMinMagicArmor",
        "valueFormula": 34000017,
    }),
    95000019: _tools.RODict({
        "ID": 95000019,
        "name": "猎人本能",
        "unlockYanWuGeLevel": 3,
        "fightProp": "adjMonsterDmgAnti",
        "valueFormula": 34000011,
    }),
    95000020: _tools.RODict({
        "ID": 95000020,
        "name": "猎人本能",
        "unlockYanWuGeLevel": 3,
        "fightProp": "adjAntiMortal",
        "valueFormula": 34000021,
    }),
    95000021: _tools.RODict({
        "ID": 95000021,
        "name": "固若金汤",
        "unlockYanWuGeLevel": 4,
        "fightProp": "adjFinalDmgAnti",
        "valueFormula": 34000012,
    }),
    95000022: _tools.RODict({
        "ID": 95000022,
        "name": "万夫莫敌",
        "unlockYanWuGeLevel": 4,
        "fightProp": "adjPVPDmgAnti",
        "valueFormula": 34000011,
    }),
    95000023: _tools.RODict({
        "ID": 95000023,
        "name": "万夫莫敌",
        "unlockYanWuGeLevel": 5,
        "fightProp": "adjDmgArmor",
        "valueFormula": 34000012,
    })
})
minKey = 95000001
maxKey = 95000023