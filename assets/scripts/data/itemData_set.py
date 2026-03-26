# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: itemData/set
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "itemID_money": _tools.RODict({
        "ID": "itemID_money",
        "value": 30000001,
    }),
    "itemID_bind_money": _tools.RODict({
        "ID": "itemID_bind_money",
        "value": 30000021,
    }),
    "itemID_coin": _tools.RODict({
        "ID": "itemID_coin",
        "value": 30000002,
    }),
    "itemID_exp": _tools.RODict({
        "ID": "itemID_exp",
        "value": 30000003,
    }),
    "itemID_curGuildContribution": _tools.RODict({
        "ID": "itemID_curGuildContribution",
        "value": 30000005,
    }),
    "itemID_darkiron": _tools.RODict({
        "ID": "itemID_darkiron",
        "value": 30000013,
    }),
    "itemID_guildMoney": _tools.RODict({
        "ID": "itemID_guildMoney",
        "value": 30000006,
    }),
    "itemID_guildCoin": _tools.RODict({
        "ID": "itemID_guildCoin",
        "value": 30000007,
    }),
    "itemID_guildExp": _tools.RODict({
        "ID": "itemID_guildExp",
        "value": 30000008,
    }),
    "itemID_equipSpirit": _tools.RODict({
        "ID": "itemID_equipSpirit",
        "value": 30000002,
    }),
    "bagCapacityNotEnough_msgID": _tools.RODict({
        "ID": "bagCapacityNotEnough_msgID",
        "value": 54000188,
    }),
    "itemNotEnough_msgID": _tools.RODict({
        "ID": "itemNotEnough_msgID",
        "value": 54000291,
    }),
    "itemLackOfLevel_msgID": _tools.RODict({
        "ID": "itemLackOfLevel_msgID",
        "value": 54000119,
    }),
    "unlock_commonBag_msgID": _tools.RODict({
        "ID": "unlock_commonBag_msgID",
        "value": 54000090,
    }),
    "itemOverdue_msgID": _tools.RODict({
        "ID": "itemOverdue_msgID",
        "value": 54000093,
    }),
    "itemInCD_msgID": _tools.RODict({
        "ID": "itemInCD_msgID",
        "value": 54000094,
    }),
    "recycleItem_msgID": _tools.RODict({
        "ID": "recycleItem_msgID",
        "value": 54000218,
    }),
    "discardItem_msgID": _tools.RODict({
        "ID": "discardItem_msgID",
        "value": 54000219,
    }),
    "getItem_msgID": _tools.RODict({
        "ID": "getItem_msgID",
        "value": 54000156,
    }),
    "itemNotExist_msgID": _tools.RODict({
        "ID": "itemNotExist_msgID",
        "value": 54001574,
    }),
    "resolveConfirm_msgID": _tools.RODict({
        "ID": "resolveConfirm_msgID",
        "value": 54001098,
    }),
    "resolveAllConfirm_msgID": _tools.RODict({
        "ID": "resolveAllConfirm_msgID",
        "value": 54001099,
    }),
    "autoResolveOn_msgID": _tools.RODict({
        "ID": "autoResolveOn_msgID",
        "value": 54001100,
    }),
    "resolveRareConfirm_msgID": _tools.RODict({
        "ID": "resolveRareConfirm_msgID",
        "value": 54001101,
    }),
    "synthesisItemNotEnough": _tools.RODict({
        "ID": "synthesisItemNotEnough",
        "value": 54001527,
    }),
    "synthesisItemIsBound": _tools.RODict({
        "ID": "synthesisItemIsBound",
        "value": 54002165,
    }),
    "amountChangeMax": _tools.RODict({
        "ID": "amountChangeMax",
        "value": 54001038,
    }),
    "amountChangeMin": _tools.RODict({
        "ID": "amountChangeMin",
        "value": 54001039,
    }),
    "useMedicine_HPIsFull_msgID": _tools.RODict({
        "ID": "useMedicine_HPIsFull_msgID",
        "value": 54000096,
    }),
    "useMedicine_MPIsFull_msgID": _tools.RODict({
        "ID": "useMedicine_MPIsFull_msgID",
        "value": 54000097,
    }),
    "levelRequirementText": _tools.RODict({
        "ID": "levelRequirementText",
        "value": "使用等级：{0}",
    }),
    "levelEquipmentText": _tools.RODict({
        "ID": "levelEquipmentText",
        "value": "穿戴等级：{0}",
    }),
    "manualBindCheck_msgID": _tools.RODict({
        "ID": "manualBindCheck_msgID",
        "value": 54000845,
    }),
    "classNotMatch_msgID": _tools.RODict({
        "ID": "classNotMatch_msgID",
        "value": 54000013,
    }),
    "bulkSalesConfirm_msgID": _tools.RODict({
        "ID": "bulkSalesConfirm_msgID",
        "value": 54000018,
    }),
    "recycleBtnText": _tools.RODict({
        "ID": "recycleBtnText",
        "value": "出售",
    }),
    "discardBtnText": _tools.RODict({
        "ID": "discardBtnText",
        "value": "丢弃",
    }),
    "returnScrollCastingTime": _tools.RODict({
        "ID": "returnScrollCastingTime",
        "value": 5,
    }),
    "returnScrollCastingAnimation": _tools.RODict({
        "ID": "returnScrollCastingAnimation",
        "value": "fall",
    }),
    "returnScrollCastingIcon": _tools.RODict({
        "ID": "returnScrollCastingIcon",
        "value": "Assets/Res/ui/texture/common/com_map_transport_unlock_icon.png",
    }),
    "returnScrollCastingTips": _tools.RODict({
        "ID": "returnScrollCastingTips",
        "value": "传送中",
    }),
    "unboundItemUsedConfirmMsg": _tools.RODict({
        "ID": "unboundItemUsedConfirmMsg",
        "value": 54000131,
    }),
    "enhancedGearUsedConfirmMsg": _tools.RODict({
        "ID": "enhancedGearUsedConfirmMsg",
        "value": 54000132,
    }),
    "customItemSlotNum": _tools.RODict({
        "ID": "customItemSlotNum",
        "value": 9,
    }),
    "approachWarningColorID": _tools.RODict({
        "ID": "approachWarningColorID",
        "value": 6,
    }),
    "approachGreyColorID": _tools.RODict({
        "ID": "approachGreyColorID",
        "value": 200,
    }),
    "itemTipsBagCountText": _tools.RODict({
        "ID": "itemTipsBagCountText",
        "value": "背包数量：",
    }),
    "itemTipsWarehouseCountText": _tools.RODict({
        "ID": "itemTipsWarehouseCountText",
        "value": "仓库数量：",
    }),
    "itemExpirationDate": _tools.RODict({
        "ID": "itemExpirationDate",
        "value": "有效期剩余：{0}",
    }),
    "lockOnMsg": _tools.RODict({
        "ID": "lockOnMsg",
        "value": 54200001,
    }),
    "lockOnText": _tools.RODict({
        "ID": "lockOnText",
        "value": "已锁定",
    }),
    "lockOffMsg": _tools.RODict({
        "ID": "lockOffMsg",
        "value": 54200002,
    }),
    "lockOffText": _tools.RODict({
        "ID": "lockOffText",
        "value": "未锁定",
    }),
    "lockFailMsg": _tools.RODict({
        "ID": "lockFailMsg",
        "value": 54200003,
    }),
    "sellCheckMsg": _tools.RODict({
        "ID": "sellCheckMsg",
        "value": 54200004,
    }),
    "packExpandCheckMsg": _tools.RODict({
        "ID": "packExpandCheckMsg",
        "value": 54200005,
    }),
    "storageExpandCheckMsg": _tools.RODict({
        "ID": "storageExpandCheckMsg",
        "value": 54200006,
    }),
    "recommendScoreText": _tools.RODict({
        "ID": "recommendScoreText",
        "value": "推荐战力{0}",
    }),
    "recommendLvText": _tools.RODict({
        "ID": "recommendLvText",
        "value": "推荐等级{0}",
    }),
    "packShowText": _tools.RODict({
        "ID": "packShowText",
        "value": "可能获得",
    }),
    "findNearestDrugstore": _tools.RODict({
        "ID": "findNearestDrugstore",
        "value": 12,
    }),
    "potionBagStorageLimit": _tools.RODict({
        "ID": "potionBagStorageLimit",
        "value": 10,
    }),
    "potionMaxLimitMsgID": _tools.RODict({
        "ID": "potionMaxLimitMsgID",
        "value": 54003125,
    }),
    "potionMaxLimitMailID": _tools.RODict({
        "ID": "potionMaxLimitMailID",
        "value": 37000014,
    }),
    "usageAndSourceText": _tools.RODict({
        "ID": "usageAndSourceText",
        "value": "来源用途",
    }),
    "itemDetailsText": _tools.RODict({
        "ID": "itemDetailsText",
        "value": "物品详情",
    }),
    "sourceWaysText": _tools.RODict({
        "ID": "sourceWaysText",
        "value": "获取途径",
    }),
    "usageWaysText": _tools.RODict({
        "ID": "usageWaysText",
        "value": "使用途径",
    }),
    "sellingAmountText": _tools.RODict({
        "ID": "sellingAmountText",
        "value": "回收数量：",
    })
})