# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: gearBase/gearConst
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "gearGeneralItemId": _tools.RODict({
        "ID": "gearGeneralItemId",
        "value": 30000004,
    }),
    "gearDropRateForOwnClass": _tools.RODict({
        "ID": "gearDropRateForOwnClass",
        "value": 0.5,
    }),
    "gearDropUnboundProbForOwnClass": _tools.RODict({
        "ID": "gearDropUnboundProbForOwnClass",
        "value": 0.2,
    }),
    "gearDropUnboundProbForOtherClass": _tools.RODict({
        "ID": "gearDropUnboundProbForOtherClass",
        "value": 1.0,
    }),
    "equipFail_classNotMatch_msg": _tools.RODict({
        "ID": "equipFail_classNotMatch_msg",
        "value": 54000295,
    }),
    "gearDisassembly_checkQuality": _tools.RODict({
        "ID": "gearDisassembly_checkQuality",
        "value": 3,
    }),
    "disassemblyConfirmMsg": _tools.RODict({
        "ID": "disassemblyConfirmMsg",
        "value": 54000296,
    }),
    "batchDisassemblyConfirmMsg": _tools.RODict({
        "ID": "batchDisassemblyConfirmMsg",
        "value": 54000297,
    }),
    "disassembleChatMsg": _tools.RODict({
        "ID": "disassembleChatMsg",
        "value": 58000155,
    }),
    "fixedAffixColor": _tools.RODict({
        "ID": "fixedAffixColor",
        "value": 27,
    }),
    "fakeLuckCountRangeLowerBound": _tools.RODict({
        "ID": "fakeLuckCountRangeLowerBound",
        "value": 0.95,
    }),
    "fakeLuckCountRangeUpperBound": _tools.RODict({
        "ID": "fakeLuckCountRangeUpperBound",
        "value": 1.05,
    }),
    "gearDisassembly_viaMail_msg": _tools.RODict({
        "ID": "gearDisassembly_viaMail_msg",
        "value": 54001244,
    }),
    "gearDisassemblyEnhancedCheck": _tools.RODict({
        "ID": "gearDisassemblyEnhancedCheck",
        "value": 54000036,
    }),
    "notEquippedPartMsg": _tools.RODict({
        "ID": "notEquippedPartMsg",
        "value": 54000133,
    }),
    "equipDropPickID": _tools.RODict({
        "ID": "equipDropPickID",
        "value": 16000028,
    }),
    "equipDropPickLiveTime": _tools.RODict({
        "ID": "equipDropPickLiveTime",
        "value": 1800,
    }),
    "equipDropMoralBound": _tools.RODict({
        "ID": "equipDropMoralBound",
        "value": 10000,
    }),
    "equipDropProbFormulaID": _tools.RODict({
        "ID": "equipDropProbFormulaID",
        "value": 34000013,
    }),
    "equipDropSeriousInjury": _tools.RODict({
        "ID": "equipDropSeriousInjury",
        "value": -501,
    }),
    "equipRepairCostItemID": _tools.RODict({
        "ID": "equipRepairCostItemID",
        "value": 30000001,
    }),
    "equipRepairCostAmount": _tools.RODict({
        "ID": "equipRepairCostAmount",
        "value": 34000014,
    }),
    "equipRepairCost": _tools.RODict({
        "ID": "equipRepairCost",
        "value": 30000001,
    }),
    "equipRepairRatioForTax": _tools.RODict({
        "ID": "equipRepairRatioForTax",
        "value": 0.05,
    }),
    "equipRepairRatioForTaxTemp": _tools.RODict({
        "ID": "equipRepairRatioForTaxTemp",
        "value": (0.05, 0.15, 0.8),
    }),
    "equipRepairRatioForClientTaxTemp": _tools.RODict({
        "ID": "equipRepairRatioForClientTaxTemp",
        "value": (500, 1500, 8000),
    }),
    "equipRepairTime": _tools.RODict({
        "ID": "equipRepairTime",
        "value": 300,
    }),
    "equipDamageDestructionTime": _tools.RODict({
        "ID": "equipDamageDestructionTime",
        "value": 86400,
    }),
    "equipDamageMailID": _tools.RODict({
        "ID": "equipDamageMailID",
        "value": 37000008,
    }),
    "equipNeedRepairMailID": _tools.RODict({
        "ID": "equipNeedRepairMailID",
        "value": 37000009,
    }),
    "equipDestroyedMailID": _tools.RODict({
        "ID": "equipDestroyedMailID",
        "value": 37000010,
    }),
    "returnAndStartRepairMailID": _tools.RODict({
        "ID": "returnAndStartRepairMailID",
        "value": 37000011,
    }),
    "equipDestroyedForPickMailID": _tools.RODict({
        "ID": "equipDestroyedForPickMailID",
        "value": 37000012,
    }),
    "equipNeedPickUpTip": _tools.RODict({
        "ID": "equipNeedPickUpTip",
        "value": "受损状态下属性全部失效\n能量晶核位置：{0}",
    }),
    "equipNeedRepairTip": _tools.RODict({
        "ID": "equipNeedRepairTip",
        "value": "破碎倒计时：{0}",
    }),
    "equipRepairingTip": _tools.RODict({
        "ID": "equipRepairingTip",
        "value": "修复倒计时：{0}",
    }),
    "equipRepairListMaxNum": _tools.RODict({
        "ID": "equipRepairListMaxNum",
        "value": 20,
    }),
    "equipPickUp_msgID": _tools.RODict({
        "ID": "equipPickUp_msgID",
        "value": 54000167,
    }),
    "equipRepairing_msgId": _tools.RODict({
        "ID": "equipRepairing_msgId",
        "value": 54000168,
    }),
    "equipRepairCostConfirm_msgID": _tools.RODict({
        "ID": "equipRepairCostConfirm_msgID",
        "value": 54000169,
    }),
    "equipRepaired_msgID": _tools.RODict({
        "ID": "equipRepaired_msgID",
        "value": 54000170,
    }),
    "equipDestroyed_msgID": _tools.RODict({
        "ID": "equipDestroyed_msgID",
        "value": 54000171,
    }),
    "pickOthersDropEquip_msgID": _tools.RODict({
        "ID": "pickOthersDropEquip_msgID",
        "value": 54000172,
    }),
    "pickListFullNum": _tools.RODict({
        "ID": "pickListFullNum",
        "value": 10,
    }),
    "pickListFull_msgID": _tools.RODict({
        "ID": "pickListFull_msgID",
        "value": 54000173,
    }),
    "returnEnergyCrystalConfirm_msgID": _tools.RODict({
        "ID": "returnEnergyCrystalConfirm_msgID",
        "value": 54000174,
    }),
    "returnEnergyCrystalSuccess_msgID": _tools.RODict({
        "ID": "returnEnergyCrystalSuccess_msgID",
        "value": 54000175,
    }),
    "returnAndStartRepair_msgID": _tools.RODict({
        "ID": "returnAndStartRepair_msgID",
        "value": 54000176,
    }),
    "equipDestroyedForPick_msgID": _tools.RODict({
        "ID": "equipDestroyedForPick_msgID",
        "value": 54000177,
    }),
    "equipDropNoOtherOperation_msgID": _tools.RODict({
        "ID": "equipDropNoOtherOperation_msgID",
        "value": 54000178,
    }),
    "equipWearLowRoleLevel": _tools.RODict({
        "ID": "equipWearLowRoleLevel",
        "value": 54000301,
    }),
    "equipWearLowRoleLevel2": _tools.RODict({
        "ID": "equipWearLowRoleLevel2",
        "value": 54000312,
    }),
    "pickListNumText": _tools.RODict({
        "ID": "pickListNumText",
        "value": "拾取记录  ({0}/{1})",
    }),
    "equipGrowingForbidden": _tools.RODict({
        "ID": "equipGrowingForbidden",
        "value": None,
    }),
    "equipStrengThenText1": _tools.RODict({
        "ID": "equipStrengThenText1",
        "value": "安全",
    }),
    "equipStrengThenText2": _tools.RODict({
        "ID": "equipStrengThenText2",
        "value": "风险",
    }),
    "equipStrengThenText3": _tools.RODict({
        "ID": "equipStrengThenText3",
        "value": "危险",
    }),
    "equipDevelopNoMaterials": _tools.RODict({
        "ID": "equipDevelopNoMaterials",
        "value": 54000302,
    }),
    "equipAnimaGetExceptions": _tools.RODict({
        "ID": "equipAnimaGetExceptions",
        "value": 54000303,
    }),
    "equipSlotText": _tools.RODict({
        "ID": "equipSlotText",
        "value": "穿戴中",
    }),
    "equipSlot1Text": _tools.RODict({
        "ID": "equipSlot1Text",
        "value": "栏位一",
    }),
    "equipSlot2Text": _tools.RODict({
        "ID": "equipSlot2Text",
        "value": "栏位二",
    }),
    "equipUnbindMsg": _tools.RODict({
        "ID": "equipUnbindMsg",
        "value": 54000308,
    }),
    "equipRedeemMailID": _tools.RODict({
        "ID": "equipRedeemMailID",
        "value": 37002014,
    }),
    "equipDisappearMailID": _tools.RODict({
        "ID": "equipDisappearMailID",
        "value": 37002015,
    }),
    "equipReturnMailID": _tools.RODict({
        "ID": "equipReturnMailID",
        "value": 37002016,
    }),
    "equipRedeemWaitTime": _tools.RODict({
        "ID": "equipRedeemWaitTime",
        "value": 1800,
    }),
    "equipReturnText": _tools.RODict({
        "ID": "equipReturnText",
        "value": 54482009,
    }),
    "equipReturnChange": _tools.RODict({
        "ID": "equipReturnChange",
        "value": 54482010,
    }),
    "GearPricingError": _tools.RODict({
        "ID": "GearPricingError",
        "value": 54482016,
    }),
    "equipReturnItem1": _tools.RODict({
        "ID": "equipReturnItem1",
        "value": 37002019,
    }),
    "equipReturnItem2": _tools.RODict({
        "ID": "equipReturnItem2",
        "value": 37002020,
    }),
    "equipReturnItem3": _tools.RODict({
        "ID": "equipReturnItem3",
        "value": 37002021,
    })
})