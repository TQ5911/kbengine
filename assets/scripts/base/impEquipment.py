# -*- coding: utf-8 -*-
import random

import KBEngine
from KBEDebug import *
import gameconst
import gameglobal
import utils
import functools
import json
import actionContext
import redisUtils
import mailAssistor
import message_Message_def as MMD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemFactory
import dataUtils
import awardContext
import dropAward
import gamedecorator
import gametimer
import gameengine
import gametlog
import gameclass
import value_value as VLVLD
import gearManufacture_details as GMDD
import gearBase_gearConst as GBGCD
import gearManufacture_replacement as GER
import itemData_itemData as ITEM_DATA
import AuthClsWraper

import agent_agentFunction as A_AFD
import _pickle as cPickle
from proto.gameServerDrop_pb2 import DropResult_SUCCESS,\
    DropResult_NOT_FOUND,\
    DropResult_NOT_OWNER,\
    DropResult_EXPIRE,\
    DropResult_OTHER_GIVEUP,\
    DropResult_OTHER_REDEEM

class ImpEquipment(object):
    # 需要绑定值
    NEED_BIND_VALUE_METHOD = (
        'bagEquipEnhanceDeductItemsCB',
        'cellEquipEnhance',
        'bagEquipUpgradeDeductItemsCB',
        'cellEquipUpgrade',
        'bagEquipGlyphWashingDeductItemsCB',
        'cellEquipGlyphWashing',
        'bagEquipBlessDeductItemsCB',
        'cellEquipBless'
    )
    # 需要绑定和非绑定值
    NEED_BIND_AND_UNBIND_VALUE_METHOD = (
        'bagEquipSpiritWashingDeductItemsCB',
        'cellEquipSpiritWashing',
    )

    def __init__(self):
        super(ImpEquipment, self).__init__()

    def calculateUpgradeConditions(self, box, methodName, args, consumeGridId, itemId, grade):
        consumeBagEquipItem = self.bagData.getItemObjByGridId(consumeGridId)
        if not consumeBagEquipItem:
            self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
            ERROR_MSG('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, wrong arg 1 !', consumeGridId)
            return False, None

        if consumeBagEquipItem.itemId != itemId:
            self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
            ERROR_MSG('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, invalid comsume grid item id', consumeGridId, consumeBagEquipItem.itemId, itemId)
            return False, None

        if consumeBagEquipItem.getGrade() != grade:
            self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
            ERROR_MSG('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, invalid comsume grid item grade', consumeGridId, consumeBagEquipItem.getGrade(), grade)
            return False, None

        return True, consumeBagEquipItem.getOriginalBindValue()

    def baseEquipDeductItems(self, costItemDic, gridNeedItems, gridIdList, gridCountList, opUUID, srcType, detail, box, methodName, args, autoBuy, sendMsg):
        DEBUG_MSG('in baseEquipDeductItems:', costItemDic, gridNeedItems, gridIdList, gridCountList, opUUID, srcType, detail, methodName, args, autoBuy)
        bindValue = 0
        unbindValue = 0

        if methodName =='bagEquipUpgradeDeductItemsCB':
            consumeGridId = args.pop(0)
            gridId =  args[1]
            if gridId == consumeGridId:
                self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, same grid id!')
                return

            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if not bagEquipItem:
                self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, wrong arg 2 !', gridId)
                return

            ret, bindValue = self.calculateUpgradeConditions(box, methodName, args, consumeGridId, bagEquipItem.itemId, bagEquipItem.getGrade())
            if not ret:
                return

        elif methodName == 'cellEquipUpgrade':
            consumeGridId = args.pop(0)
            itemId = args.pop(0)
            grade = args.pop(0)
            ret, bindValue = self.calculateUpgradeConditions(box, methodName, args, consumeGridId, itemId, grade)
            if not ret:
                return

        if self.bagData.isLocked():
            WARNING_MSG('   in baseEquipDeductItems, bagData locked!')
            self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_BAG_LOCKED, 0, 0)
            return

        args = tuple(args)
        # 额外的格子消耗
        needGridIdList = gridNeedItems
        # 有特殊自选需求的额外格子消耗
        if gridIdList and gridCountList and gridNeedItems:
            ret, needGridIdList, bindValue, unbindValue = self.calculateConsumePlan(gridNeedItems, gridIdList, gridCountList)
            if not ret:
                self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('in baseEquipDeductItems wrong args:', gridNeedItems, gridIdList, gridCountList)
                return

        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costItemDic.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)

        #非自动购买情况下，才需要发送物品不足message
        if self.canDeductWealth(deductWealthVal, not autoBuy):
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            # 额外的格子消耗
            if needGridIdList:
                self.bagData.deductItemsByGrid(self, needGridIdList, opUUID, srcType, detail)
            DEBUG_MSG('in baseEquipDeductItems ', methodName, args)
            self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_STAT_OK, bindValue, unbindValue)
            return
        else:
            ERROR_MSG('   in baseEquipDeductItems, canDeductWealth fail:', opUUID)

        if not autoBuy:
            #不需要自动购买
            self.equipMethodCallback(box, methodName, args, gameconst.BagOPStat.BAG_OP_ITEMS_NOT_ENOUGH, 0, 0)
            return

    def equipMethodCallback(self, box, methodName, args, opStat, bindValue, unbindValue):
        if methodName in ImpEquipment.NEED_BIND_VALUE_METHOD:
            args=(bindValue,)+args
        elif methodName in ImpEquipment.NEED_BIND_AND_UNBIND_VALUE_METHOD:
            args=(bindValue, unbindValue)+args
        box and methodName and getattr(box, methodName)(opStat, *args)

    def addAutoDressEquipItem(self, equipList, opUUID, srcType, taskId, awardCtx):
        DEBUG_MSG('addAutoDressEquipItem')
        #新手引导使用，装备进背包后自动穿到身上
        if self.bagData.isLocked():
            gameengine.reportCritical('addAutoDressEquipItem, bag locked, try later:', opUUID)
            self._callback(1, 'addAutoDressEquipItem', (equipList, opUUID, srcType, taskId, awardCtx), gametimer.TIMER_TAG_AUTO_DRESS_EQUIP)
            return

        if len(equipList) > self.bagData.leftGridCount:
            gameengine.reportCritical('addAutoDressEquipItem, no space')
            return

        succGridIdList = []
        for it in equipList:
            opStat, gridId = self.bagData.addItemsToNewGrid(self, it, opUUID, srcType, str(taskId), notify=True, syncToClient=False)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                gameengine.reportCritical('addAutoDressEquipItem, add equip failed:', it.itemId, it.uniqueId)
                return
            succGridIdList.append(gridId)

        for gridId in succGridIdList:
            self.dressEquipment(gridId, gameconst.EQUIP_DRESS_TYPE.OP_AUTO_DRESS, False, 0)
        return

    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @gamedecorator.crossServer
    def dressEquipment(self, exposed, gridId, dressType, dstSlotId):
        INFO_MSG('in dressEquipment:', gridId, dressType, dstSlotId, self.baseSpaceNo)
        self.bagData.doDressEquip(self, gridId, dressType, dstSlotId)

    def dressEquipmentCB(self, uniqId, result, bagEquipDic):
        DEBUG_MSG('in dressEquipmentCB:', uniqId, result)
        self.bagData.doDressEquipCB(self, uniqId, result)
        if result != gameconst.DressEquipOpStat.EQUIP_OP_FAILED:
            if 'attrJson' in bagEquipDic:
                attrJson = bagEquipDic['attrJson']
                attrDict = json.loads(attrJson)
                enhanceLv = attrDict.get('enhanceLv', 0)

    @gamedecorator.crossServer
    def replaceEquipment(self, uniqId, result, oldBodyEquipDic):
        INFO_MSG('in replaceEquipment:', uniqId, result, self.baseSpaceNo, oldBodyEquipDic)
        self.bagData.doDressEquipCB(self, uniqId, result, oldBodyEquipDic)

    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @gamedecorator.crossServer
    def undressEquipment(self, exposed, slotId):
        INFO_MSG("in undressEquipment:", slotId, self.baseSpaceNo)
        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        if not self.bagData.tryLockBag(lockDesc='undressEquipment, slotId:%s'%(slotId)):
            ERROR_MSG('in undressEquipment, lock bag fail:', self.bagData.lockDesc, slotId)
            return

        self.cell.cellUndressEquipment(slotId)

    def updateAccountCharacterAppearance(self, updateDic):
        self.accountEntity.updateAppearance(self.gbID, updateDic)

    def cellUndressEquipmentSucc(self, bodyEquipDic):
        DEBUG_MSG('in cellUndressEquipmentSucc', bodyEquipDic)
        self.unlockBag()
        self.bagData.doBagUndressEquip(self, bodyEquipDic)

    def cellUndressEquipmentFail(self, slotId, reason):
        DEBUG_MSG("cellUndressEquipmentFail::", slotId, reason)
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL, reason)

    def bagEquipEnhance(self, gridId, uniqueId, gridIdList, gridCountList, autoBuy):
        DEBUG_MSG('in bagEquipEnhance:', gridId, uniqueId, gridIdList, gridCountList, autoBuy)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipEnhance, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipEnhance, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipEnhance, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentEnhancementType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('   in bagEquipEnhance, equipment enhancement is invalid, equipment:', bagEquipItem)
            return

        if not bagEquipItem.checkEnhancementValid(bagEquipItem.equipAttr.getEnhanceLv() + 1):
            ERROR_MSG('   in bagEquipEnhance, equipment enhancement is invalid', bagEquipItem.itemId)
            return

        costItemDic, costCurrencyDic = bagEquipItem.enhanceNeedItems()
        if not costItemDic or not costCurrencyDic:
            ERROR_MSG('     in bagEquipEnhance, cost is empty:', bagEquipItem.equipAttr.getEnhanceLv() + 1)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_BAG_EQUIP
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId)
        args = (opUUID, gridId, uniqueId)
        self.baseEquipDeductItems(costCurrencyDic, costItemDic, gridIdList, gridCountList, opUUID, srcType, detail, self,
                                  'bagEquipEnhanceDeductItemsCB', args, autoBuy, True)

    def bagEquipEnhanceDeductItemsCB(self, opStat, bindValue, opUUID, gridId, uniqueId):
        DEBUG_MSG('in bagEquipEnhanceDeductItemsCB:', opStat, gridId, uniqueId, bindValue)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipEnhanceDeductItemsCB, deduct items error')
            self.client.onEquipEnhanceFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bindValue > 0:
            bagEquipItem.updateBindValue()
        enhanceVal = bagEquipItem.doEnhanceEquip(self, opUUID, bagEquipItem.getEnhanceLevel())
        # 装备破碎了
        if enhanceVal == gameconst.EquipConstVale.ENHANCEMENT_BROKEN_FLAG:
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_BAG_EQUIP
            detail = gameclass.AwardDetail(uniqueid=uniqueId, itemid=bagEquipItem.itemId)
            self.bagData.cleanGridByGridId(self, gridId, bagEquipItem.itemId, opUUID, srcType, detail)
            self.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            self.client.onEquipBroken(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
        else:
            self.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            self.client.onEquipEnhanceSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getEnhanceLevel(), bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipUpgrade(self, gridId, uniqueId, consumeGridId, autoBuy):
        DEBUG_MSG('in bagEquipUpgrade:', gridId, uniqueId, consumeGridId, autoBuy)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipUpgrade, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipUpgrade, uniqueId not matched:', bagEquipItem.uniqueId, uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipUpgrade, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentUpgradeType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('   in bagEquipUpgrade, equipment upgrade is invalid, equipment:', bagEquipItem)
            return

        if not bagEquipItem.checkUpgradeValid():
            ERROR_MSG('   in bagEquipUpgrade, equipment upgrade is invalid', bagEquipItem.itemId)
            return

        costItemDic = bagEquipItem.upgradeNeedItems()
        if not costItemDic:
            ERROR_MSG('     in bagEquipUpgrade, cost is empty:', bagEquipItem.getGrade() + 1)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_UPGRADE_BAG_EQUIP
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId)
        self.baseEquipDeductItems(costItemDic, {consumeGridId:1}, None, None, opUUID, srcType, detail, self,
                                  'bagEquipUpgradeDeductItemsCB', [consumeGridId, opUUID, gridId], autoBuy, True)

    def bagEquipUpgradeDeductItemsCB(self, opStat, bindValue, opUUID, gridId):
        DEBUG_MSG('in bagEquipUpgradeDeductItemsCB:', opStat, bindValue, gridId)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipUpgradeDeductItemsCB, deduct items error')
            self.client.onEquipUpgradeFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        bagEquipItem.doUpgradeEquip(self, opUUID)
        bagEquipItem.setBindValue(bagEquipItem.getOriginalBindValue() + bindValue)
        self.client.onEquipUpgradeSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getGrade(), bagEquipItem.getEquipScore(), bagEquipItem.getOriginalBindValue(), bagEquipItem.bindType)
        return

    def bagEquipGlyphWashing(self, gridId, uniqueId, glyphPos, gridIdList, gridCountList):
        DEBUG_MSG('in bagEquipGlyphWashing:', gridId, uniqueId, glyphPos, gridIdList, gridCountList)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipGlyphWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipGlyphWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('in bagEquipGlyphWashing, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('in bagEquipGlyphWashing, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkGlyphNum(glyphPos):
            ERROR_MSG('in bagEquipGlyphWashing slot is empty')
            return

        costItemDic, costCurrencyDic = bagEquipItem.glyphWashingNeedItems()
        if not costItemDic or not costCurrencyDic:
            ERROR_MSG('     in bagEquipGlyphWashing, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_WEAPON_GLYPH_WASHING
        detail = gameclass.AwardDetail(gridId=gridId, uniqueId=uniqueId)
        args = (opUUID, gridId, glyphPos)
        self.baseEquipDeductItems(costCurrencyDic, costItemDic, gridIdList, gridCountList, opUUID, srcType, detail, self,
                                  'bagEquipGlyphWashingDeductItemsCB', args, False, True)
        return

    def bagEquipGlyphWashingDeductItemsCB(self, opStat, bindValue, opUUID, gridId, glyphPos):
        DEBUG_MSG('in bagEquipGlyphWashingDeductItemsCB:', opStat, bindValue, opUUID, gridId, glyphPos)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipGlyphWashingDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bindValue > 0:
            bagEquipItem.updateBindValue()
        ret, _, _ = bagEquipItem.doEquipGlyphWashing(self, glyphPos)
        if ret:
            glyphData = bagEquipItem.equipAttr.getGlyphData(glyphPos)
            self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, glyphData.toClientData(), bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipGlyphApply(self, gridId, uniqueId, groupId):
        DEBUG_MSG('in bagEquipGlyphApply:', gridId, uniqueId, groupId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipGlyphApply, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipGlyphApply, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('in bagEquipGlyphApply, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('in bagEquipGlyphApply, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkGlyphApplyGroupId(groupId):
            ERROR_MSG('in bagEquipGlyphApply groupId is wrong')
            return

        bagEquipItem.doApplyGlyphGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, groupId)
        self.client.onEquipGlyphApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, groupId, bagEquipItem.getEquipScore())
        return

    def bagEquipSpiritApply(self, gridId, uniqueId, groupId):
        DEBUG_MSG('in bagEquipSpiritApply:', gridId, uniqueId, groupId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipSpiritApply, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipSpiritApply, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('in bagEquipSpiritApply, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentSpiritType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('in bagEquipSpiritApply, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkSpiritApplyGroupId(groupId):
            ERROR_MSG('in bagEquipSpiritApply groupId is wrong')
            return

        bagEquipItem.doApplySpiritGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, groupId)
        self.client.onEquipSpiritApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, groupId, bagEquipItem.getEquipScore())
        return

    def bagEquipBless(self, gridId, uniqueId, gridIdList, gridCountList):
        DEBUG_MSG('in bagEquipBless:', gridId, uniqueId, gridIdList, gridCountList)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipBless, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipBless, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipBless, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentBlessType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('   in bagEquipBless, equipment can not bless, equipment:', bagEquipItem)
            return False

        costItemDic, costCurrencyDic = bagEquipItem.blessNeedItems()
        if not costItemDic:
            ERROR_MSG('     in bagEquipBless, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_BLESSING
        detail = gameclass.AwardDetail(bodyId=gridId, uniqueId=uniqueId)
        args = (opUUID, gridId, )
        self.baseEquipDeductItems(costCurrencyDic, costItemDic, gridIdList, gridCountList, opUUID, srcType, detail, self, 'bagEquipBlessDeductItemsCB', args,
                                  False, True)
        return

    def bagEquipBlessDeductItemsCB(self, opStat, bindValue, opUUID, gridId):
        DEBUG_MSG('in bagEquipBlessDeductItemsCB:', opStat, bindValue, opUUID, gridId)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipBlessDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bindValue > 0:
            bagEquipItem.updateBindValue()
        if bagEquipItem.doEquipBlessing(self):
            blessAffixes = []
            for oneAffix in bagEquipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, blessAffixes,
                                         bagEquipItem.equipAttr.maxBlessLv, bagEquipItem.equipAttr.blessLvRate,
                                         bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipBackBless(self, gridId, uniqueId):
        DEBUG_MSG('in bagEquipBackBless:', gridId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('bagEquipBackBless, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('bagEquipBackBless, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        ret = dataUtils.checkEquipmentBlessType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('bagEquipBackBless not bless type')
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipBackBless, equipment can not be growing, equipment:', bagEquipItem)
            return

        if not bagEquipItem.isCanBackBless():
            ERROR_MSG('bagEquipBackBless not can backBless')
            return

        if bagEquipItem.doEquipBackBless():
            blessAffixes = []
            for oneAffix in bagEquipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBackBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, blessAffixes,
                                             bagEquipItem.equipAttr.maxBlessLv, bagEquipItem.equipAttr.blessLvRate,
                                             bagEquipItem.getEquipScore())

    def bagEquipSpiritWashing(self, gridId, uniqueId, spiritPos, gridIdList, gridCountList):
        DEBUG_MSG('in bagEquipSpiritWashing:', gridId, uniqueId, spiritPos, gridIdList, gridCountList)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('bagEquipSpiritWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('bagEquipSpiritWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('bagEquipSpiritWashing, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentSpiritType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('bagEquipSpiritWashing, equipment can not affix, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkSpiritNum(spiritPos):
            ERROR_MSG('bagEquipSpiritWashing slot is empty')
            return

        costItemDic, costCurrencyDic = bagEquipItem.spiritWashingNeedItems()
        if not costItemDic or not costCurrencyDic:
            ERROR_MSG('     bagEquipSpiritWashing, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_AFFIX_WASHING
        detail = gameclass.AwardDetail(gridId=gridId, uniqueId=uniqueId)
        self.baseEquipDeductItems(costCurrencyDic, costItemDic, gridIdList, gridCountList, opUUID, srcType, detail, self, 'bagEquipSpiritWashingDeductItemsCB', (opUUID, gridId, spiritPos),
                                  False, True)
        return

    def bagEquipSpiritWashingDeductItemsCB(self, opStat, bindValue, unbindValue, opUUID, gridId, spiritPos):
        DEBUG_MSG('in bagEquipSpiritWashingDeductItemsCB:', opStat, bindValue, unbindValue, opUUID, gridId, spiritPos)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipSpiritWashingDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bindValue > 0:
            bagEquipItem.updateBindValue()
        ret, _, _ = bagEquipItem.doEquipSpiritWashing(self, spiritPos, unbindValue)
        if ret:
            spiritData = bagEquipItem.equipAttr.spiritDatas[spiritPos]
            self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.EQUIPMENT_WITH_SPIRIT, actionContext.AchievementCtx())
            self.client.onEquipSpiritWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritData.toClientData(),
                                                 spiritPos, bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipBindWashing(self, gridId, uniqueId, washCount):
        DEBUG_MSG('in bagEquipBindWashing:', gridId, uniqueId, washCount)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipBindWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('     in bagEquipBindWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return
        if not bagEquipItem.hasBindValue() or bagEquipItem.getBindValue() < washCount:
            ERROR_MSG('     in bagEquipBindWashing, no bind value remain:', bagEquipItem.uniqueId)
            return

        costItemDic = bagEquipItem.bindValueWashingNeedItems(washCount)
        if not costItemDic:
            ERROR_MSG('     in bagEquipBindWashing, cost is empty')
            return
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BINDVALUE_WASHING_BAG_EQUIP
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId)
        args = (opUUID, gridId, washCount)
        self.baseEquipDeductItems(costItemDic, None, None, None, opUUID, srcType, detail, self, 'bagEquipBindValueWashingDeductItemsCB', args,
                                  False, True)

    def bagEquipBindValueWashingDeductItemsCB(self, opStat, opUUID, gridId, washCount):
        DEBUG_MSG('in bagEquipBindValueWashingDeductItemsCB:', opStat, gridId, washCount)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipBindValueWashingDeductItemsCB, deduct items error')
            self.client.onEquipBindValueWashingFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        bagEquipItem.doDecreaseBindValue(opUUID, washCount)
        self.client.onEquipBindValueWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getBindValue(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @gamedecorator.limitcall(1)
    def reqMultiEquipDisassemble(self, exposed, gridIdList, uniqueIdList):
        DEBUG_MSG('reqMultiEquipDisassemble:', gridIdList, uniqueIdList)
        self.bagData.doBagEquipDisassemble(self, gridIdList, uniqueIdList)

    def bagEquipSell(self, gridId, uniqueId):
        self.bagData.doBagEquipSell(self, gridId, uniqueId)

    def updateBodyEquipDressData(self, dressDataDic):
        self.baseBodyEquipDressDataDic = dressDataDic

    def canEquipAutoDisassemble(self, owner, equipItem):
        cliConfig = self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY, 0)
        # 自动分解开关
        autoSwitch = utils.hasBit(cliConfig, gameconst.AUTO_DISA_QUALITY_KEY.AUTOS_WITCH)
        if not autoSwitch:
            return False
        isCanTrade = utils.hasBit(cliConfig, gameconst.AUTO_DISA_QUALITY_KEY.TRADE)
        if not isCanTrade and equipItem.bindType != gameconst.ItemBindType.BIND:
            return False

        if not utils.hasBit(cliConfig, equipItem.quality):
            return False

        if equipItem.isPreciousEquip():
            return False
        reqClassList = dataUtils.getEquipItemData(equipItem.itemId)['reqClass']
        myClass = owner.getRoleCacheAttr('school', 0)
        if 0 not in reqClassList and myClass not in reqClassList:
            #自己无法装备，不考虑评分，可以分解
            return True
        slotIds = dataUtils.equipSlot(equipItem.equipAttr.equipType, equipItem.equipAttr.equipSubType)
        for slotId in slotIds:
            bodyEquipScore = self.baseBodyEquipDressDataDic.get(slotId, {}).get('score', 0)
            if equipItem.getEquipScore() > bodyEquipScore:
                return False
        return True

    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    @gamedecorator.limitcall(1)
    def reqMakeEquipment(self, exposed, itemId, gridIdList, gridCountList, makeType):
        DEBUG_MSG('reqMakeEquipment:', itemId, gridIdList, gridCountList, makeType)
        itemData = dataUtils.getEquipItemData(itemId)
        if not itemData:
            ERROR_MSG('in reqMakeEquipment, gearBase_gearBase not found:', itemId)
            return

        if len(gridIdList) > self.bagData.capacity or len(gridIdList) != len(gridCountList):
            ERROR_MSG('in reqMakeEquipment, wrong args:', itemId)
            return

        school = self.getRoleCacheAttr('school', 0)
        recommendClasses = dataUtils.equipRecommendClass(itemData['type'], itemData['subType'])
        if school not in recommendClasses:
            ERROR_MSG('in reqMakeEquipment, in valid school:', itemId, school, recommendClasses)
            return

        cfgData = GMDD.datas.get(itemId, None)
        if not cfgData:
            ERROR_MSG('in reqMakeEquipment, gearManufacture_details not found:', itemId)
            return

        isOpen = cfgData.get('isOpen')
        if not isOpen:
            ERROR_MSG('in reqMakeEquipment not open:', itemId)
            self.client.onEquipMakeFailed()
            return

        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        consumeItem = None
        if makeType == gameconst.EquipmentManufactureType.MANUFACTURE_LEFT:
            consumeItem = cfgData.get('consumeItem')
            if not consumeItem:
                ERROR_MSG('in reqMakeEquipment missing consumeItem:', itemId, makeType)
                return
        elif makeType == gameconst.EquipmentManufactureType.MANUFACTURE_RIGHT:
            consumeItem = cfgData.get('consumeItem2')
            if not consumeItem:
                ERROR_MSG('in reqMakeEquipment missing consumeItem2:', itemId, makeType)
                return
        else:
            ERROR_MSG('in reqMakeEquipment unknow equipment manufacture type:', itemId, makeType)
            return

        # 收集
        needCostItems = {}
        okCount = 0
        # 先处理配置表的道具消耗数据，防止重复配置错误
        for val in consumeItem:
            costItemId, itemNum = val
            needCostItems[costItemId] = needCostItems.get(costItemId, 0) + itemNum

        ret, needGridIdList, bindValue, _ = self.calculateConsumePlan(needCostItems, gridIdList, gridCountList, True)
        if not ret:
            ERROR_MSG('in reqMakeEquipment wrong args:', itemId, makeType, needGridIdList, needCostItems, okCount)
            self.client.onEquipMakeFailed()
            return
        # 开始扣除道具
        deductVal = dropAward.DeductWealthVal()
        # 扣除消耗的货币
        consumeMoney = cfgData.get('consumeMoney')
        if consumeMoney:
            for val in consumeMoney:
                costItemId, itemNum = val
                deductVal.addWealthByItemId(costItemId, itemNum)
        # 如果消耗的资源为空，不允许制造
        if deductVal.isEmpty():
            ERROR_MSG('in reqMakeEquipment, consume item is empty, equipment manufacture is forbidden:', itemId)
            self.client.onEquipMakeFailed()
            return

        if not self.canDeductWealth(deductVal, sendMsg=True):
            ERROR_MSG('in reqMakeEquipment, canDeductWealth fail:', itemId)
            self.client.onEquipMakeFailed()
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_MANUFACTURE
        detail = gameclass.AwardDetail(itemId=itemId)
        # 扣货币
        self.deductWealth(srcType, deductVal, opUUID, detail)
        # 扣指定格子指定数量的道具
        self.bagData.deductItemsByGrid(self, needGridIdList, opUUID, srcType, detail)

        # 获得制造好的道具
        bindType = gameconst.ItemBindType.BIND if bindValue > 0 else gameconst.ItemBindType.NORMAL
        equipItem = itemFactory.ItemFactory.createItem(itemId, 1, bindType=bindType)
        # 设置绑定值
        equipItem.setBindValue(bindValue)
        DEBUG_MSG('reqMakeEquipment: done', itemId, gridIdList, makeType, bindValue)
        opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem, ], opUUID, srcType, detail, notify=False)
        if opStat == gameconst.BagOPStat.BAG_OP_STAT_OK:
            self.makeEquipmentGetLog(srcType, equipItem)
            data = equipItem.toClientEquipItemDict()
            DEBUG_MSG('in reqMakeEquipment, addItemsWithPlan success:', opStat, data)
            self.client.onEquipMakeSucc(data)
        else:
            ERROR_MSG('in reqMakeEquipment, addItemsWithPlan fail:', opStat, itemId)
            self.client.onEquipMakeFailed()

        self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.MAKE_EQUIPMENT, actionContext.AchievementCtx())

    def makeEquipmentGetLog(self, srcType, equipItem):
        tlogParams = {
            'GameSvrId': None,
            'dtEventTime': None,
            'vGameAppid': None,
            'ItemId': equipItem.itemId,
            'ItemUniqueId': equipItem.uniqueId,
            'Reason': srcType,
            'Detail': gameclass.AwardDetail(data=equipItem.toItemSavedDict()),
        }
        # tlogParams.update(self.getTLogCommonParams())
        # gametlog.build(gameconst.GameLog.LOG_GET_EQUIP, **tlogParams).init().commit()

    def makeEquipmentLostLog(self, srcType, equipItemDic):
        tlogParams = {
            'GameSvrId': None,
            'dtEventTime': None,
            'vGameAppid': None,
            'ItemId': equipItemDic['itemId'],
            'ItemUniqueId': equipItemDic['uniqueId'],
            'Reason': srcType,
            'Detail': gameclass.AwardDetail(data=equipItemDic),
        }
        # tlogParams.update(self.getTLogCommonParams())
        # gametlog.build(gameconst.GameLog.LOG_LOST_EQUIP, **tlogParams).init().commit()

    def makeEquipmentEnhanceLog(self, itemId, uniqueId, enhanceLv, oldVal, newVal, enhanceRate, result):
        tlogParams = {
            'GameSvrId': None,
            'dtEventTime': None,
            'vGameAppid': None,
            'ItemId': itemId,
            'ItemUniqueId': uniqueId,
            'EnhanceLv': enhanceLv,
            'OldEnhanceVal': oldVal,
            'NewEnhanceVal': newVal,
            'EnhanceRate': enhanceRate,
            'Result': int(result),
        }

        # tlogParams.update(self.getTLogCommonParams())
        # gametlog.build(gameconst.GameLog.LOG_EQUIP_ENHANCE, **tlogParams).init().commit()

    def makeEquipmentAffixWashingLog(self, itemId, uniqueId, logDataDic):
        tlogParams = {
            'GameSvrId': None,
            'dtEventTime': None,
            'vGameAppid': None,
            'ItemId': itemId,
            'ItemUniqueId': uniqueId,
            "WashingAffixNum" : logDataDic['WashingAffixNum'],
            "IsPrecious" : int(logDataDic['IsPrecious']),
            "WashingAffix" : logDataDic['WashingAffix'],
        }
        # tlogParams.update(self.getTLogCommonParams())
        # gametlog.build(gameconst.GameLog.LOG_EQUIP_DIHUN, **tlogParams).init().commit()

    ################################## gm cmd ###################################
    def gmAddGearbaseEquipItem(self, templateId, bindType=dataUtils.getItemDefaultBindType(), grade = 1):
        DEBUG_MSG('gmAddGearbaseEquipItem:', templateId)
        equipItem = itemFactory.ItemFactory.createItem(templateId, 1, bindType=bindType, grade = grade)
        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_GM
        detail = gameclass.AwardDetail(templateId=templateId)

        opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem, ], opUUID, src, detail)
        if opStat == gameconst.BagOPStat.BAG_OP_STAT_OK:
            self.makeEquipmentGetLog(src, equipItem)
        return opStat


    def gmBaseDressEquips(self, bodyDressSlotIds):
        INFO_MSG("gmBaseDressEquips ", bodyDressSlotIds)
        myLevel = gameglobal.roleCache[self.id]['level']
        myClass = gameglobal.roleCache[self.id]['school']
        for gridId, it in self.bagData.gridId2GridObj.items():
            if not it.isEquipmentItem():
                continue
            gearData = dataUtils.getEquipItemData(it.itemId)
            reqClassList = gearData.get('reqClass', [])
            if 0 not in reqClassList and myClass not in reqClassList:
                continue
            equipLevel = gearData['equipLevel']
            if equipLevel > myLevel:
                continue

            slotIds = dataUtils.equipSlot(it.equipAttr.equipType, it.equipAttr.equipSubType)
            for slotId in slotIds:
                if slotId in bodyDressSlotIds:
                    bodyDressSlotIds.remove(slotId)
                    self._callback(0.2, 'gmSendDressEquips', (gridId, slotId, it), gametimer.TIMER_TAG_GM_SEND_DRESS_EQUIPS)
                    break
            if len(bodyDressSlotIds) == 0:
                break
        return

    def gmSendDressEquips(self, gridId, slotId, equipItem):
        INFO_MSG("gmSendDressEquips ", gridId, slotId, equipItem)
        self.unlockBag()
        self.bagData.doDressEquip(self, gridId, 0, slotId)

    def gmGlyphWashingEquips(self, itemId, glyphPos, affixId1, affixId2):
        gridIds = self.bagData.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
                ERROR_MSG('in gmGlyphWashingEquips, equipment can not be growing, equipment:', bagEquipItem)
                return

            ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('in gmGlyphWashingEquips, equipment can not glyph, equipment:', bagEquipItem)
                return False

            if not bagEquipItem.checkGlyphNum(glyphPos):
                ERROR_MSG('in gmGlyphWashingEquips slot is empty')
                return

            ret, _, _ = bagEquipItem.doEquipGlyphWashing(self, glyphPos, affixIds=[affixId1, affixId2])
            if ret:
                glyphData = bagEquipItem.equipAttr.getGlyphData(glyphPos)
                self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, glyphData.toClientData(), bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return
################################## gm cmd end ###################################

    ################################### drop equip start ##############################
    def onDropEquipBase(self, uniqueId, price, mapId, pos, equipInfo, collEndTime, killerName, endTime, extraBlob, collectionId):
        _blob = cPickle.dumps(equipInfo)
        gameengine.getGlobalBase('DropStub').dropEquipItem(
            self.gbID,
            uniqueId,
            self,
            _blob,
            extraBlob,
            collEndTime,
            endTime,
            price,
            self.serverId,
            collectionId,
        )

        self.equipDropData.addNewDrop(
            self,
            uniqueId,
            price,
            mapId,
            pos,
            equipInfo,
            collEndTime,
            killerName,
            endTime,
            gameconst.DropType.TYPE_DROP,
            True,
        )

        _reachNum = self.equipDropData.dropNum() - GBGCD.datas['equipRepairListMaxNum']['value']
        if _reachNum > 0:
            _val = self.equipDropData.fetchNeedRemoveDropEquip()
            DEBUG_MSG('Drop onDropEquipBase _reachNum', self.equipDropData.dropNum(), _reachNum, _val)
            if _val:
                self.removeDropEquip(_val.uniqueId, _reachNum)

    def addNotifyDropFixTimer(self, uniqueId, endTime):
        self.equipDropData.addNotifyDropFixTimer(uniqueId, endTime)

    # 检测捡装备
    def checkPickDropEquip(self, uniqueId):
        if self.pickDropEquipLockTime > utils.getNow():
            return False

        return self.equipDropData.checkCouldTakeDrop(uniqueId)

    # 自己捡起来或者赎回会走到这里
    def onGetBackDropEquip(self, uniqueId, equipInfo, isSelfTake):
        equipInfo = cPickle.loads(equipInfo)
        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)
        _fixEndTime = utils.getNow() + GBGCD.datas['equipRepairTime']['value']
        equipItem.setDropFixEndTime(_fixEndTime)

        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByObjList([equipItem])
        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_TAKE_BACK_DROP_EQUIP
        _detail = gameclass.AwardDetail()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
        )

        if isSelfTake:
            self.onMessagePre(
                GBGCD.datas['equipPickUp_msgID']['value'],
                [str(equipItem.itemId)])
        else:
            _args = [
                str(equipItem.itemId),
                str(GBGCD.datas['equipRepairTime']['value']),
            ]
            self.onMessagePre(GBGCD.datas['equipRepairing_msgId']['value'], _args)

        self.addNotifyDropFixTimer(equipItem.uniqueId, _fixEndTime)

    def removeDropEquip(self, uniqueId, times):
        if not self.equipDropData.tryLock():
            WARNING_MSG('removeDropEquip lock failed:', uniqueId)
            return

        if not self.equipDropData.hasDrop(uniqueId):
            ERROR_MSG('removeDropEquip not found drop:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').removeDropEquip(self.gbID, uniqueId, times, self)

    def _sendDestroyMail(self, itemId):
        _mailId = GBGCD.datas['equipDestroyedMailID']['value']
        _args = [
            str(itemId),
        ]
        mailAssistor.sendMailToPlayers(
            [self.gbID],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args
        )

    def onRemoveDropEquip(self, uniqueId, result, times, collectionId):
        INFO_MSG('onRemoveDropEquip:', uniqueId, result, times)
        self.equipDropData.unlock()

        if result == DropResult_SUCCESS:
            _dropVal = self.equipDropData.removeDrop(self, uniqueId)
            if _dropVal:
                _item = _dropVal.equipItem()
                self._sendDestroyMail(_item.itemId)

                if utils.getNow() < _dropVal.collEndTime:
                    gameengine.callCellApps('removeEquipDropDestroyCollection', (collectionId, _dropVal.uniqueId))

                self.onMessagePre(
                    GBGCD.datas['equipDestroyedForPick_msgID']['value'],
                    [str(_item.itemId)])
        else:
            ERROR_MSG('onRemoveDropEquip fail:', uniqueId, result, times)

        times -= 1

        if times > 0 and self.equipDropData.dropNum() > GBGCD.datas['equipRepairListMaxNum']['value']:
            _val = self.equipDropData.fetchNeedRemoveDropEquip()
            if _val:
                self.removeDropEquip(_val.uniqueId, times)

    def onTakeDropEquipFailed(self, uniqueId, result):
        INFO_MSG('onTakeDropEquipFailed:', uniqueId, result)
        self.pickDropEquipLockTime = 0

    # 捡别人的装备成功的回调
    def onTakeDropEquipSuccess(self, dropGbId, uniqueId, equipInfo, endTime, price):
        INFO_MSG('onTakeDropEquipSuccess:', dropGbId, uniqueId)
        self.pickDropEquipLockTime = 0

        if dropGbId == self.gbID:
            self.equipDropData.removeDrop(self, uniqueId)
            return

        equipInfo = cPickle.loads(equipInfo)
        self.equipDropData.addTaker(
            self,
            uniqueId,
            equipInfo,
            endTime,
            gameconst.DropType.TYPE_TAKE,
            int(price * GBGCD.datas['equipRepairRatioForPicker']['value']),
            True,
        )

        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)

        _mailId = GBGCD.datas['equipNeedRepairMailID']['value']
        _args = [
            str(equipItem.itemId),
            str(equipItem.uniqueId),
            str(endTime)
        ]
        mailAssistor.sendMailToPlayers(
            [dropGbId],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args
        )

        self.onMessagePre(
            GBGCD.datas['pickOthersDropEquip_msgID']['value'],
            [str(equipItem.itemId)])

    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    def giveUpDropEquip(self, exposed, uniqueId):
        INFO_MSG('giveUpDropEquip:', uniqueId)
        if not self.equipDropData.hasTakeDrop(uniqueId):
            ERROR_MSG('giveUpDropEquip not found take:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').giveUpDropEquip(self.gbID, uniqueId, self)

    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    def redeemEquipDrop(self, exposed, uniqueId):
        INFO_MSG('redeemEquipDrop:', uniqueId)
        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if not _dropVal:
            ERROR_MSG('redeemEquipDrop not found drop:', uniqueId)
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(
            GBGCD.datas['equipRepairCostItemID']['value'],
            _dropVal.price,
        )

        if not self.canDeductWealth(_deductVal, sendMsg=True):
            WARNING_MSG('       in doUnlockGrids, items not enough:', _deductVal)
            return

        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_EQUIP_DROP
        _detail = gameclass.AwardDetail()
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        gameengine.getGlobalBase('DropStub').doRedeemEquipDrop(self.gbID, uniqueId, self)

    def onRedeemResult(self, uniqueId, result):
        INFO_MSG('onRedeemResult:', uniqueId, result)
        if result == DropResult_SUCCESS:
            self.equipDropData.removeDrop(self, uniqueId)
            return
        elif result == DropResult_NOT_FOUND:
            WARNING_MSG('onRedeemResult not found drop:', uniqueId)
            self.equipDropData.removeTaker(self, uniqueId)
        elif result == DropResult_EXPIRE:
            WARNING_MSG('onRedeemResult expire:', uniqueId)
            self.equipDropData.removeTaker(self, uniqueId)
        elif result == DropResult_OTHER_GIVEUP:
            self._fetchOtherGiveUpEquip(uniqueId)
        else:
            ERROR_MSG('onRedeemResult unknown:', uniqueId, result)

        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if not _dropVal:
            ERROR_MSG('onRedeemResult not found drop:', uniqueId)
            return

        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByItemId(
            GBGCD.datas['equipRepairCostItemID']['value'],
            _dropVal.price,
        )
        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_EQUIP_DROP
        _detail = gameclass.AwardDetail()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
        )

    # 别人赎回后，你领取奖励
    def _getTakeReward(self, uniqueId):
        gameengine.getGlobalBase('DropStub').doGetTakeReward(self.gbID, uniqueId, self)

    def onGetDropTakeReward(self, uniqueId, price):
        INFO_MSG('onGetDropTakeReward:', uniqueId, price)
        _takerVal = self.equipDropData.removeTaker(self, uniqueId, isNotify=False)
        if not _takerVal:
            ERROR_MSG('onGetDropTakeReward not found taker:', uniqueId)
            return

        self.equipDropData.addTakerWait(uniqueId, _takerVal.equip, _takerVal.endTime, _takerVal.price)
        self.client.onEquipDropStateChange(uniqueId, gameconst.DropType.TYPE_REDEEM)

    @AuthClsWraper.authWithPermission(A_AFD.UIBusinessPanel)
    def getTakerWaitReward(self, exposed, uniqueId):
        _takerVal = self.equipDropData.removeTakerWait(self, uniqueId)
        if not _takerVal:
            ERROR_MSG('getTakerWaitReward not found takerWait:', uniqueId)
            return

        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByItemId(
            GBGCD.datas['equipRepairCostItemID']['value'],
            _takerVal.price,
        )
        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_FOR_PICKER
        _detail = gameclass.AwardDetail()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
        )

    def _fetchOtherGiveUpEquip(self, uniqueId):
        INFO_MSG('_fetchOtherGiveUpEquip:', uniqueId)
        gameengine.getGlobalBase('DropStub').doFetchOtherGiveUpEquip(self.gbID, uniqueId, self)

    def onDropTypeChangeToAvatar(self, uniqueId, dropType):
        INFO_MSG('onDropTypeChangeToAvatar:', uniqueId, dropType)
        if dropType == gameconst.DropType.TYPE_REDEEM:
            _takerVal = self.equipDropData.getTakerVal(uniqueId)
            if _takerVal:
                self._getTakeReward(uniqueId)

        elif dropType == gameconst.DropType.TYPE_GIVEUP:
            _dropVal = self.equipDropData.getDropVal(uniqueId)
            if _dropVal:
                self._fetchOtherGiveUpEquip(uniqueId)

        elif dropType == gameconst.DropType.TYPE_TAKE:
            self.equipDropData.onDropTypeChange(uniqueId, dropType)

        self.client.onEquipDropStateChange(uniqueId, dropType)

    # 别人放弃了你捡起来的装备会走到这里
    def onFetchOtherGiveUpEquip(self, uniqueId, equipInfo, result, giveUpTime):
        INFO_MSG('onFetchOtherGiveUpEquip:', uniqueId, equipInfo, result, giveUpTime)
        if result == DropResult_SUCCESS:
            self.equipDropData.removeDrop(self, uniqueId)

            equipInfo = cPickle.loads(equipInfo)
            equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)
            _fixEndTime = giveUpTime + GBGCD.datas['equipRepairTime']['value']
            equipItem.setDropFixEndTime(_fixEndTime)

            _awardVal = dropAward.AwardVal()
            _awardVal.addWealthByObjList([equipItem])
            _opUUID = KBEngine.genUUID64()
            _src = AAC_AACDD.datas.BONUS_SRC_FETCH_OTHER_GIVEUP_DROP
            _detail = gameclass.AwardDetail()

            self.addWealth(
                _src,
                _awardVal,
                _opUUID,
                _detail,
                awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
            )

            _msgId = GBGCD.datas['returnAndStartRepair_msgID']['value']
            _args = [
                str(equipItem.itemId),
                str(GBGCD.datas['equipRepairTime']['value'])
            ]

            self.onMessagePre(_msgId, _args)

            _mailId = GBGCD.datas['returnAndStartRepairMailID']['value']
            _args = [
                str(equipItem.itemId),
                str(equipItem.uniqueId),
            ]
            mailAssistor.sendMailToPlayers(
                [self.gbID],
                _mailId,
                opUUID=KBEngine.genUUID64(),
                despArgs=_args
            )

            self.addNotifyDropFixTimer(equipItem.uniqueId, _fixEndTime)
            return

        if result == DropResult_NOT_FOUND or\
                result == DropResult_NOT_OWNER or\
                result == DropResult_EXPIRE:

            ERROR_MSG('onFetchOtherGiveUpEquip not found:', uniqueId, result)
            self.equipDropData.removeDrop(self, uniqueId)

    def _doGetAllDropEquipStatus(self):
        _dropList = self.equipDropData.getDropList()

        for _uniqueId in _dropList:
            self._fetchOtherGiveUpEquip(_uniqueId)
            yield lambda: True

        _takerList = self.equipDropData.getTakeList()
        for _uniqueId in _takerList:
            self._getTakeReward(_uniqueId)
            yield lambda: True

    def _initGetAllDropEquipStatus(self):
        gameengine.getGlobalBase('DropStub').doGetDropInfo(self.gbID, self)

    def onGetDropInfo(self, dropInfo, takerInfo):
        DEBUG_MSG('onGetDropInfo:', dropInfo, takerInfo)
        for _uniqueId, _equipInfo, _endTime, _dropType, _extraInfo, _collExpireTime, _price in dropInfo:
            self.equipDropData.addNewDrop(
                self,
                _uniqueId,
                _price,
                _extraInfo['m'],
                _extraInfo['p'],
                _equipInfo,
                _collExpireTime,
                _extraInfo['n'],
                _endTime,
                _dropType,
                False,
            )

            if _dropType == gameconst.DropType.TYPE_GIVEUP:
                self._fetchOtherGiveUpEquip(_uniqueId)

        for _uniqueId, _equipInfo, _endTime, _dropType, _price in takerInfo:
            self.equipDropData.addTaker(
                self,
                _uniqueId,
                _equipInfo,
                _endTime,
                _dropType,
                int(_price * GBGCD.datas['equipRepairRatioForPicker']['value']),
                False,
            )

            if _dropType == gameconst.DropType.TYPE_REDEEM:
                self._getTakeReward(_uniqueId)

        self.equipDropInitStatus = 1
        self.triggerTempEvent(gameconst.AvatarProps.equipDropInitEvent)

        self._getDropNotifyList()

    def _sendDropEquipInfo(self):
        if not self.equipDropInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.equipDropInitEvent, '_sendDropEquipInfo', ())
            return

        # self.equipDropData.clearEndTimeVals()
        self.client.onInitEquipDropData(self.equipDropData)

    def _initEquipDrop(self):
        self.equipDropInitStatus = 0
        self.createTempEvent(gameconst.AvatarProps.equipDropInitEvent)
        self.pyAddTimer(10, 10, gametimer.DEAL_DROP_EQUIP_EXPIRE)

    @property
    def equipDropInitStatus(self):
        return self.getTempMiscProp(gameconst.AvatarProps.equipDropInitStatus, 1)

    @equipDropInitStatus.setter
    def equipDropInitStatus(self, val):
        if val:
            self.popTempMiscProp(gameconst.AvatarProps.equipDropInitStatus)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.equipDropInitStatus, 0)

    def takeEquipBase(self, uniqueId):
        if not self.checkPickDropEquip(uniqueId):
            ERROR_MSG('takeEquipBase not could take drop:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').takeDropEquip(self.gbID, uniqueId, self)
        self.pickDropEquipLockTime = utils.getNow() + 60

    def onGiveUpDropEquip(self, uniqueId, result, dropGbId):
        INFO_MSG('onGiveUpDropEquip:', uniqueId, result, dropGbId)
        if result == DropResult_SUCCESS:
            _takerVal = self.equipDropData.removeTaker(self, uniqueId)
            if _takerVal:
                redisUtils.RedisUtils.getSingleUserInfo(dropGbId, functools.partial(self._onGiveUpGetUserInfo, _takerVal))

        elif result == DropResult_OTHER_REDEEM:
            self._getTakeReward(uniqueId)

    def _onGiveUpGetUserInfo(self, _takerVal, fcVal):
        _item = itemFactory.ItemFactory.createItemWithSavedDict(_takerVal.equip)
        _args = [
            str(_item.itemId),
            fcVal.name
        ]
        _msgId = GBGCD.datas['returnEnergyCrystalSuccess_msgID']['value']

        self.onMessagePre(_msgId, _args)

    def onOtherRemoveDropEquip(self, uniqueId):
        INFO_MSG('onOtherRemoveDropEquip:', uniqueId)
        self.equipDropData.removeTaker(self, uniqueId)

    def _dealDropEquipExpire(self):
        self.equipDropData.doDealDropEquipExpire(self)

        _endTime = utils.getNow()
        # 处理装备修复时间到提示msg
        while True:
            _takerTimerVal = self.equipDropData.firstTimerVal()
            if not _takerTimerVal:
                break

            if _takerTimerVal.endTime > _endTime:
                break

            self.equipDropData.popFirstTimerVal()
            _, equipItem = self.bagData.getItemByUniqueId(_takerTimerVal.uniqueId)
            if equipItem:
                self.onMessagePre(
                    GBGCD.datas['equipRepaired_msgID']['value'],
                    [str(equipItem.itemId)])

    # 自己掉落的装备过期处理
    def _dropExpire(self, uniqueId, itemId):
        self.equipDropData.removeDrop(self, uniqueId)
        self._sendDestroyMail(itemId)

    def _sendPickDestroyMail(self, itemId):
        _mailId = GBGCD.datas['equipDestroyedForPickMailID']['value']
        _args = [
            str(itemId),
        ]
        mailAssistor.sendMailToPlayers(
            [self.gbID],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args
        )

    # 捡起别人的装备过期处理
    def _takerExpire(self, uniqueId, itemId):
        self.equipDropData.removeTaker(self, uniqueId)
        self._sendPickDestroyMail(itemId)

    def onDropEquipExpire(self, uniqueId, result):
        INFO_MSG('onDropEquipExpire:', uniqueId, result)
        if result != DropResult_SUCCESS:
            return

        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if _dropVal:
            self._dropExpire(uniqueId, _dropVal.equipItem().itemId)
            return

        _takerVal = self.equipDropData.getTakerVal(uniqueId)
        if _takerVal:
            self._takerExpire(uniqueId, _takerVal.equipItem().itemId)
            return

    def onAddDropNotify(self):
        INFO_MSG('onAddDropNotify')
        self._getDropNotifyList()

    def _getDropNotifyList(self):
        gameengine.getGlobalBase('DropStub').getDropNotifyList(self.gbID, self)

    def onGetDropNotifyList(self, notifyList):
        INFO_MSG('onGetDropNotifyList:', notifyList)

        for _data in notifyList:
            _notifyType = _data['notifyType']
            _uniqueId = _data['uniqueId']
            _notifyTime = _data['notifyTime']
            _equipInfo = _data['equipInfo']

            _equipInfo = cPickle.loads(_equipInfo)

            if _notifyType == gameconst.DropNotifyType.NOTIFY_DROP_EXPIRE:
                _item = itemFactory.ItemFactory.createItemWithSavedDict(_equipInfo)
                self._dropExpire(_uniqueId, _item.itemId)
            elif _notifyType == gameconst.DropNotifyType.NOTIFY_TAKE_EXPIRE:
                _item = itemFactory.ItemFactory.createItemWithSavedDict(_equipInfo)
                self._takerExpire(_uniqueId, _item.itemId)

    ################################### drop equip end ##############################

    def checkEquipmentCore(self, itemID):
        itemData = ITEM_DATA.datas.get(itemID)
        return itemData and itemData['type'] == 0 and itemData['subType'] == gameconst.ItemSubType.EQUIP_CORE

    def calculateConsumePlan(self, needCostItems, gridIdList, gridCountList, needEquipCore=False):
        if len(gridIdList) != len(gridCountList):
            ERROR_MSG('in calculateConsumePlan wrong args 1:', gridIdList, gridCountList)
            return False, None, 0, 0
        okCount = 0
        bindValue = 0
        unbindValue = 0
        needGridIdList = {}
        # 分析并计算需要消耗的格子上的道具数量
        for i in range(len(gridIdList)):
            gridId = gridIdList[i]
            gridCount = gridCountList[i]
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if not bagEquipItem or bagEquipItem.itemNum < gridCount:
                ERROR_MSG('in calculateConsumePlan wrong args 2:', bagEquipItem.itemId, gridCount, bagEquipItem.itemNum)
                return False, None, 0, 0
            bagItemNum = bagEquipItem.itemNum
            # 检查指定格子材料是否足够
            for costItemID, costItemNum in needCostItems.items():
                # 已满足
                if costItemNum <= 0:
                    continue
                if costItemID == bagEquipItem.itemId:
                    if costItemNum > bagItemNum:
                        needCostItems[costItemID] = costItemNum - bagItemNum
                        needGridIdList[gridId] = needGridIdList.get(gridId, 0) + bagItemNum
                        if bagEquipItem.bindType == gameconst.ItemBindType.BIND:
                            if needEquipCore:
                                if self.checkEquipmentCore(bagEquipItem.itemId):
                                    bindValue += bagItemNum
                            else:
                                bindValue += bagItemNum
                        else:
                            unbindValue += bagItemNum
                        bagItemNum = 0
                    else:
                        needCostItems[costItemID] = 0
                        needGridIdList[gridId] = needGridIdList.get(gridId, 0) + costItemNum
                        if bagEquipItem.bindType == gameconst.ItemBindType.BIND:
                            if needEquipCore:
                                if self.checkEquipmentCore(bagEquipItem.itemId):
                                    bindValue += costItemNum
                            else:
                                bindValue += costItemNum
                        else:
                            unbindValue += costItemNum
                        bagItemNum -= costItemNum
                        # 以满足的个数
                        okCount += 1
                # 当前提供材料消耗完毕, 结束检查
                if bagItemNum <= 0:
                    break
            # 消耗全部满足了, 结束计算
            if okCount == len(needCostItems):
                return True, needGridIdList, bindValue, unbindValue
        return False, None, 0, 0
