# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearEnhance/gearconst
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "enhancedAdvancementLevel": _tools.RODict({
        "ID": "enhancedAdvancementLevel",
        "value": 5,
    }),
    "enhancedGrowthValue": _tools.RODict({
        "ID": "enhancedGrowthValue",
        "value": 100,
    }),
    "intervalWeight": _tools.RODict({
        "ID": "intervalWeight",
        "value": 34000004,
    }),
    "enhanceFailed": _tools.RODict({
        "ID": "enhanceFailed",
        "value": 54000057,
    }),
    "enhanceSuccess": _tools.RODict({
        "ID": "enhanceSuccess",
        "value": 54000058,
    }),
    "enhanceLuckySuccess": _tools.RODict({
        "ID": "enhanceLuckySuccess",
        "value": 54000059,
    }),
    "enhanceGreatFailed": _tools.RODict({
        "ID": "enhanceGreatFailed",
        "value": 54000060,
    }),
    "advancedTips": _tools.RODict({
        "ID": "advancedTips",
        "value": "进阶成功率{0}%",
    }),
    "advancedSuccessTitle": _tools.RODict({
        "ID": "advancedSuccessTitle",
        "value": "进阶成功",
    }),
    "glyphUnlockEnhLv": _tools.RODict({
        "ID": "glyphUnlockEnhLv",
        "value": (2, 5, 8),
    }),
    "gearWeaponGlyphNumWeight": _tools.RODict({
        "ID": "gearWeaponGlyphNumWeight",
        "value": (80, 20),
    }),
    "gearBlessMaxValue": _tools.RODict({
        "ID": "gearBlessMaxValue",
        "value": 7,
    }),
    "totalBlessMaxValue": _tools.RODict({
        "ID": "totalBlessMaxValue",
        "value": 9,
    }),
    "gearBlessSuccess": _tools.RODict({
        "ID": "gearBlessSuccess",
        "value": 54000064,
    }),
    "gearBlessFailed": _tools.RODict({
        "ID": "gearBlessFailed",
        "value": 54000065,
    }),
    "gearBlessGreatFailed": _tools.RODict({
        "ID": "gearBlessGreatFailed",
        "value": 54000066,
    }),
    "glyphSlotUnlockTips": _tools.RODict({
        "ID": "glyphSlotUnlockTips",
        "value": "强化{0}级解锁",
    }),
    "gearBlessBacktrack": _tools.RODict({
        "ID": "gearBlessBacktrack",
        "value": 54000078,
    }),
    "gearBlessCntBacktrack": _tools.RODict({
        "ID": "gearBlessCntBacktrack",
        "value": 54000079,
    }),
    "affixWashNumTask": _tools.RODict({
        "ID": "affixWashNumTask",
        "value": 86020003,
    }),
    "affixWashNumLimit": _tools.RODict({
        "ID": "affixWashNumLimit",
        "value": 9999,
    }),
    "msgId_addAffixWashNum": _tools.RODict({
        "ID": "msgId_addAffixWashNum",
        "value": 54000081,
    }),
    "msgId_affixWashNumLimit": _tools.RODict({
        "ID": "msgId_affixWashNumLimit",
        "value": 54000082,
    }),
    "rarityAffixWashConfirmMinLevel": _tools.RODict({
        "ID": "rarityAffixWashConfirmMinLevel",
        "value": 2,
    }),
    "msgId_rarityAffixWashConfirm": _tools.RODict({
        "ID": "msgId_rarityAffixWashConfirm",
        "value": 54000085,
    }),
    "spiritValueText": _tools.RODict({
        "ID": "spiritValueText",
        "value": "以上材料可转化为<color=#b35b00>{0}点</color>灵气",
    }),
    "addGearSpiritSuccess": _tools.RODict({
        "ID": "addGearSpiritSuccess",
        "value": 54000083,
    }),
    "affixWashNumNotEnough": _tools.RODict({
        "ID": "affixWashNumNotEnough",
        "value": "完成任务：{0}获得附灵次数",
    }),
    "affixWashNumTaskConfirm": _tools.RODict({
        "ID": "affixWashNumTaskConfirm",
        "value": 54000084,
    }),
    "gearButtonAction_enhance": _tools.RODict({
        "ID": "gearButtonAction_enhance",
        "value": "Openinterface,UIEquipTrainingPanel,1",
    }),
    "gearButtonAction_rune": _tools.RODict({
        "ID": "gearButtonAction_rune",
        "value": "Openinterface,UIEquipTrainingPanel,4",
    }),
    "gearButtonAction_bless": _tools.RODict({
        "ID": "gearButtonAction_bless",
        "value": "Openinterface,UIEquipTrainingPanel,5",
    }),
    "gearButtonAction_identify": _tools.RODict({
        "ID": "gearButtonAction_identify",
        "value": "Openinterface,UIEquipTrainingPanel,2",
    }),
    "gearButtonAction_class": _tools.RODict({
        "ID": "gearButtonAction_class",
        "value": "Openinterface,UIEquipTrainingPanel,3",
    }),
    "gearButtonAction_unbounding": _tools.RODict({
        "ID": "gearButtonAction_unbounding",
        "value": "findNearestEntityByTempleteIds,18000019,18000067,18000119",
    }),
    "gearButtonLimitID_train": _tools.RODict({
        "ID": "gearButtonLimitID_train",
        "value": "UIEquipTrainingPanel",
    }),
    "gearButtonLimitID_enhance": _tools.RODict({
        "ID": "gearButtonLimitID_enhance",
        "value": "UIEquipIntensifyPage",
    }),
    "gearButtonLimitID_rune": _tools.RODict({
        "ID": "gearButtonLimitID_rune",
        "value": "UIEquipRunePage",
    }),
    "gearButtonLimitID_bless": _tools.RODict({
        "ID": "gearButtonLimitID_bless",
        "value": "UIEquipBlessPage",
    }),
    "gearButtonLimitID_identify": _tools.RODict({
        "ID": "gearButtonLimitID_identify",
        "value": "UIEquipEnchantingPage",
    }),
    "gearButtonLimitID_class": _tools.RODict({
        "ID": "gearButtonLimitID_class",
        "value": "UIEquipClassPage",
    }),
    "gearButtonLimitID_make": _tools.RODict({
        "ID": "gearButtonLimitID_make",
        "value": "UIEquipMakePanel",
    }),
    "gearButtonLimitID_unbundle": _tools.RODict({
        "ID": "gearButtonLimitID_unbundle",
        "value": "UIEquipUnbundlePanel",
    }),
    "gearStrengthenMax": _tools.RODict({
        "ID": "gearStrengthenMax",
        "value": (0, 8, 8, 10, 10, 10),
    }),
    "gearblessingBack": _tools.RODict({
        "ID": "gearblessingBack",
        "value": 54000243,
    }),
    "auction_slotLocked": _tools.RODict({
        "ID": "auction_slotLocked",
        "value": 54000244,
    }),
    "auction_slotLocked2": _tools.RODict({
        "ID": "auction_slotLocked2",
        "value": 54000245,
    }),
    "gearBacktrack_ValueLack": _tools.RODict({
        "ID": "gearBacktrack_ValueLack",
        "value": 54000246,
    }),
    "strengthenDes1": _tools.RODict({
        "ID": "strengthenDes1",
        "value": "强化失败时，强化等级保持不变",
    }),
    "strengthenDes2": _tools.RODict({
        "ID": "strengthenDes2",
        "value": "强化失败时，强化等级概率<color=#dea050>下降</color>",
    }),
    "strengthenDes3": _tools.RODict({
        "ID": "strengthenDes3",
        "value": "强化失败时，装备概率破损，直接<color=#c60c0c>销毁</color>",
    }),
    "gearFuLing_AccessFailed": _tools.RODict({
        "ID": "gearFuLing_AccessFailed",
        "value": 54000247,
    }),
    "gearEnhance_noChoiceEquipmenr": _tools.RODict({
        "ID": "gearEnhance_noChoiceEquipmenr",
        "value": 54000248,
    }),
    "gearStrengthenLevel": _tools.RODict({
        "ID": "gearStrengthenLevel",
        "value": "强化+{0}",
    }),
    "gearFuLlingCost": _tools.RODict({
        "ID": "gearFuLlingCost",
        "value": "需消耗灵气值：{0}",
    }),
    "gearBlessLevel": _tools.RODict({
        "ID": "gearBlessLevel",
        "value": "幸运值{0}",
    }),
    "equipFuLingReikiInsufficient": _tools.RODict({
        "ID": "equipFuLingReikiInsufficient",
        "value": 54000304,
    }),
    "equipExchangeNoEquipment": _tools.RODict({
        "ID": "equipExchangeNoEquipment",
        "value": 54000305,
    }),
    "gearFuLlingTaskEffects": _tools.RODict({
        "ID": "gearFuLlingTaskEffects",
        "value": 31960000,
    }),
    "gearFuLing_ExtraGain": _tools.RODict({
        "ID": "gearFuLing_ExtraGain",
        "value": 5,
    }),
    "gearFuLing_noFuLingDesc": _tools.RODict({
        "ID": "gearFuLing_noFuLingDesc",
        "value": "通过“装备附灵”可获得额外属性",
    }),
    "gearFuLing_noGlyphDesc": _tools.RODict({
        "ID": "gearFuLing_noGlyphDesc",
        "value": "通过“武器铭文”可获得技能特性",
    }),
    "gearFuLing_ItemTip": _tools.RODict({
        "ID": "gearFuLing_ItemTip",
        "value": "存储灵气：",
    }),
    "gearFuLing_ItemTipNum": _tools.RODict({
        "ID": "gearFuLing_ItemTipNum",
        "value": "{0}+<color=#038304>{1}（每日）</color>",
    }),
    "glyphExplain": _tools.RODict({
        "ID": "glyphExplain",
        "value": "<color=#fffbd7>{0}：</color>{1}",
    }),
    "gearFuLingRating": _tools.RODict({
        "ID": "gearFuLingRating",
        "value": ('C', 'B', 'A', 'S'),
    }),
    "enhanceGreatFailed2": _tools.RODict({
        "ID": "enhanceGreatFailed2",
        "value": 54000306,
    }),
    "enhanceGreatFailed3": _tools.RODict({
        "ID": "enhanceGreatFailed3",
        "value": 54000309,
    }),
    "gearEnhanceBindLimit": _tools.RODict({
        "ID": "gearEnhanceBindLimit",
        "value": 1,
    }),
    "gearEnhanceBindMsg": _tools.RODict({
        "ID": "gearEnhanceBindMsg",
        "value": 54000307,
    }),
    "blessAffixID": _tools.RODict({
        "ID": "blessAffixID",
        "value": _tools.ROList([(3, 78000030), (4, 78000031)]),
    }),
    "noStrengthenList": _tools.RODict({
        "ID": "noStrengthenList",
        "value": ('adjFinalDmg', 'adjFinalDmgAnti', 'adjIgnoreArmor', 'adjDmgArmor', 'adjMonsterDmg', 'adjMonsterDmgAnti', 'adjPVPDmg', 'adjPVPDmgAnti', 'adjMortal', 'adjAntiMortal', 'adjDrugsQuantity'),
    }),
    "strengthenPercent": _tools.RODict({
        "ID": "strengthenPercent",
        "value": (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6),
    }),
    "gearBlessBoundValue": _tools.RODict({
        "ID": "gearBlessBoundValue",
        "value": ((1, 1), (2, 2), (3, 4), (4, 8)),
    }),
    "equipmentClassLevel": _tools.RODict({
        "ID": "equipmentClassLevel",
        "value": 4,
    }),
    "gearBlessFulingValue": _tools.RODict({
        "ID": "gearBlessFulingValue",
        "value": ((1, 0), (2, 2), (3, 3), (4, 3), (5, 3)),
    }),
    "equipWear_partMsg": _tools.RODict({
        "ID": "equipWear_partMsg",
        "value": 54000322,
    }),
    "gearEnhance_defaultLevel": _tools.RODict({
        "ID": "gearEnhance_defaultLevel",
        "value": 4,
    }),
    "gearEnhance_listFull": _tools.RODict({
        "ID": "gearEnhance_listFull",
        "value": 54003259,
    }),
    "gearEnhance_insufficientFunds": _tools.RODict({
        "ID": "gearEnhance_insufficientFunds",
        "value": 54003260,
    }),
    "gearEnhance_damagedMsg": _tools.RODict({
        "ID": "gearEnhance_damagedMsg",
        "value": 54003261,
    }),
    "equipmentClass_targetLevel": _tools.RODict({
        "ID": "equipmentClass_targetLevel",
        "value": 54003262,
    }),
    "gearEnhance_listNumLimit": _tools.RODict({
        "ID": "gearEnhance_listNumLimit",
        "value": 14,
    }),
    "gearBless_textDesc": _tools.RODict({
        "ID": "gearBless_textDesc",
        "value": "攻击触发最大值概率",
    })
})