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
        "name": "物理大攻",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjMaxPhysicalAtk",
        "valueFormula": 34000010,
    }),
    95000002: _tools.RODict({
        "ID": 95000002,
        "name": "物理小攻",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjMinPhysicalAtk",
        "valueFormula": 34000010,
    }),
    95000003: _tools.RODict({
        "ID": 95000003,
        "name": "法术大攻",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjMaxMagicAtk",
        "valueFormula": 34000010,
    }),
    95000004: _tools.RODict({
        "ID": 95000004,
        "name": "法术小攻",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjMinMagicAtk",
        "valueFormula": 34000010,
    }),
    95000005: _tools.RODict({
        "ID": 95000005,
        "name": "对怪伤害",
        "unlockYanWuGeLevel": 3,
        "fightProp": "adjMonsterDmg",
        "valueFormula": 34000011,
    }),
    95000006: _tools.RODict({
        "ID": 95000006,
        "name": "对人伤害",
        "unlockYanWuGeLevel": 4,
        "fightProp": "adjPVPDmg",
        "valueFormula": 34000011,
    }),
    95000007: _tools.RODict({
        "ID": 95000007,
        "name": "总伤害提升",
        "unlockYanWuGeLevel": 5,
        "fightProp": "adjFinalDmg",
        "valueFormula": 34000012,
    }),
    95000008: _tools.RODict({
        "ID": 95000008,
        "name": "物理大防",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjMaxPhysicalArmor",
        "valueFormula": 34000010,
    }),
    95000009: _tools.RODict({
        "ID": 95000009,
        "name": "物理小防",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjMinPhysicalArmor",
        "valueFormula": 34000010,
    }),
    95000010: _tools.RODict({
        "ID": 95000010,
        "name": "法术大防",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjMaxMagicArmor",
        "valueFormula": 34000010,
    }),
    95000011: _tools.RODict({
        "ID": 95000011,
        "name": "法术小防",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjMinMagicArmor",
        "valueFormula": 34000010,
    }),
    95000012: _tools.RODict({
        "ID": 95000012,
        "name": "受怪伤害降低",
        "unlockYanWuGeLevel": 3,
        "fightProp": "adjMonsterDmgAnti",
        "valueFormula": 34000011,
    }),
    95000013: _tools.RODict({
        "ID": 95000013,
        "name": "受人伤害降低",
        "unlockYanWuGeLevel": 4,
        "fightProp": "adjPVPDmgAnti",
        "valueFormula": 34000011,
    }),
    95000014: _tools.RODict({
        "ID": 95000014,
        "name": "总伤害降低",
        "unlockYanWuGeLevel": 5,
        "fightProp": "adjFinalDmgAnti",
        "valueFormula": 34000012,
    }),
    95000015: _tools.RODict({
        "ID": 95000015,
        "name": "生命",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjFullHp",
        "valueFormula": 34000018,
    }),
    95000016: _tools.RODict({
        "ID": 95000016,
        "name": "法力",
        "unlockYanWuGeLevel": 1,
        "fightProp": "adjFullMp",
        "valueFormula": 34000019,
    }),
    95000018: _tools.RODict({
        "ID": 95000018,
        "name": "经验获取",
        "unlockYanWuGeLevel": 2,
        "fightProp": "adjExpGrow",
        "valueFormula": 34000020,
    }),
    95000019: _tools.RODict({
        "ID": 95000019,
        "name": "铜币获取",
        "unlockYanWuGeLevel": 3,
        "fightProp": "adjCopper",
        "valueFormula": 34000020,
    }),
    95000020: _tools.RODict({
        "ID": 95000020,
        "name": "吃药收益",
        "unlockYanWuGeLevel": 4,
        "fightProp": "adjMedicineRate",
        "valueFormula": 34000020,
    })
})
minKey = 95000001
maxKey = 95000020