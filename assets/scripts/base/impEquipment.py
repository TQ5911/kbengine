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
import gearManufacture_config as GMCDD
import gearBase_gearConst as GBGCD
import gearManufacture_replacement as GER

import _pickle as cPickle
from proto.gameServerDrop_pb2 import DropResult_SUCCESS,\
    DropResult_NOT_FOUND,\
    DropResult_NOT_OWNER,\
    DropResult_EXPIRE,\
    DropResult_OTHER_GIVEUP,\
    DropResult_OTHER_REDEEM

class ImpEquipment(object):
    def __init__(self):
        super(ImpEquipment, self).__init__()

    def baseEquipDeductItems(self, costItemDic, opUUID, srcType, detail, box,  methodName, args, autoBuy, sendMsg):
        DEBUG_MSG('in baseEquipDeductItems:', costItemDic, methodName, args, autoBuy)
        if self.bagData.isLocked():
            WARNING_MSG('   in baseEquipDeductItems, bagData locked!')
            box and methodName and getattr(box, methodName)(gameconst.BagOPStat.BAG_OP_BAG_LOCKED, *args)
            return
        deductWealthVal = dropAward.DeductWealthVal()
        gridId = costItemDic.pop('gridId', 0)
        if gridId:
            item = self.bagData.getItemObjByGridId(gridId)
            if not item:
                ERROR_MSG('baseEquipDeductItems item not found', gridId)
                return
            deductWealthVal.addWealthByObjList([item])

        for itemId, (itemNum, bindType) in costItemDic.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum, bindType)

        #非自动购买情况下，才需要发送物品不足message
        if self.canDeductWealth(deductWealthVal, not autoBuy):
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            box and methodName and getattr(box, methodName)(gameconst.BagOPStat.BAG_OP_STAT_OK, *args)
            return
        else:
            ERROR_MSG('   in baseEquipDeductItems, canDeductWealth fail:', opUUID)

        if not autoBuy:
            #不需要自动购买
            box and methodName and getattr(box, methodName)(gameconst.BagOPStat.BAG_OP_ITEMS_NOT_ENOUGH, *args)
            return
        #
        # buyItemDic = {}
        # deductWealthVal = dropAward.DeductWealthVal()
        # for itemId, (costNum, bindType) in costItemDic.items():
        #     # if itemId in gameconst.ItemId.CANT_BUY_IN_STORE_ITEMS:
        #     #     deductWealthVal.addWealthByItemId(itemId, costNum)
        #     #     continue
        #     if bindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED or bindType == gameconst.ItemBindType.BIND:
        #         # 如果要扣除绑定材料，需要获得非绑定与绑定材料之和
        #         hasNum = self.getItemNum(itemId, gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED)
        #     else:
        #         hasNum = self.getItemNum(itemId, bindType)
        #     if hasNum > 0:
        #         deductWealthVal.addWealthByItemId(itemId, hasNum, bindType)
        #     if costNum > hasNum:
        #         buyItemDic[itemId] = costNum-hasNum
        # DEBUG_MSG('     in baseEquipDeductItems, atuoBuy:', deductWealthVal, buyItemDic)
        # if len(buyItemDic) > 0:
        #     methArgs = (deductWealthVal, opUUID, srcType, detail, box, methodName, args, sendMsg)
        #     self.queryAutoBuyItemsCost(buyItemDic, self, 'queryEquipEncItemsPriceCB', methArgs)
        # else:
        #     box and methodName and getattr(box, methodName)(gameconst.BagOPStat.BAG_OP_STAT_OK, *args)
        # return

    # def queryEquipEncItemsPriceCB(self, result, totalCostDic, priceDic, marketItemDic, deductWealthVal, opUUID, srcType, desc, box,
    #                               methodName, args, sendMsg):
    #     DEBUG_MSG('queryEquipEncItemsPriceCB:', totalCostDic, marketItemDic, deductWealthVal, methodName)
    #     if not result:
    #         WARNING_MSG('   in queryEquipEncItemsPriceCB, result:', result)
    #         box and methodName and getattr(box, methodName)(gameconst.BagOPStat.BAG_OP_DATA_ERR, *args)
    #         return
    #
    #     if self.bagData.isLocked():
    #         WARNING_MSG('   in queryEquipEncItemsPriceCB, bagData locked!')
    #         box and methodName and getattr(box, methodName)(gameconst.BagOPStat.BAG_OP_BAG_LOCKED, *args)
    #         return
    #     for costId, costNum in totalCostDic.items():
    #         deductWealthVal.addWealthByItemId(costId, costNum)
    #     DEBUG_MSG('     queryEquipEncItemsPriceCB, deductWealthVal:', deductWealthVal)
    #     if self.canDeductWealth(deductWealthVal, sendMsg):
    #         self.deductWealth(srcType, deductWealthVal, opUUID, desc)
    #         box and methodName and getattr(box, methodName)(gameconst.BagOPStat.BAG_OP_STAT_OK, *args)
    #         marketItemDic and self.postBuyMarketItems(marketItemDic, priceDic)
    #     else:
    #         if marketItemDic:
    #             #到这里说明集市物品价格发生了变化
    #             gameengine.getGlobalBase('MarketStub').getMarketItemsList(self, self.marketItemsLimitDic)
    #         box and methodName and getattr(box, methodName)(gameconst.BagOPStat.BAG_OP_ITEMS_NOT_ENOUGH, *args)
    #     return

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

        self.client.onRecordFightProps()
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

    def bagEquipEnhance(self, gridId, uniqueId, enhanceLv, autoBuy,equipSetLv):
        DEBUG_MSG('in bagEquipEnhance:', gridId, uniqueId, enhanceLv, autoBuy)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('     in bagEquipEnhance, uniqueId not matched:', bagEquipItem.uniqueId)
            return
        
        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipEnhance, equipment can not be growing, equipment:', bagEquipItem)
            return
        
        ret = dataUtils.checkEquipmentEnhancementType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('   in bagEquipEnhance, equipment enhancement is invalid, equipment:', bagEquipItem)
            return
        
        if not bagEquipItem.checkEnhancementValid(enhanceLv):
            ERROR_MSG('   in bagEquipEnhance, equipment enhancement is invalid', enhanceLv, bagEquipItem.itemId)
            return

        costItemDic = bagEquipItem.enhanceNeedItems(enhanceLv)
        if not costItemDic:
            ERROR_MSG('     in bagEquipEnhance, cost is empty:', enhanceLv)
            return
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_BAG_EQUIP
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId)
        args = (opUUID, gridId, enhanceLv,equipSetLv)
        self.baseEquipDeductItems(costItemDic, opUUID, srcType, detail, self, 'bagEquipEnhanceDeductItemsCB', args,
                                  autoBuy, True)

    def bagEquipEnhanceDeductItemsCB(self, opStat, opUUID, gridId, enhanceLv,equipSetLv):
        DEBUG_MSG('in bagEquipEnhanceDeductItemsCB:', opStat, gridId)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipEnhanceDeductItemsCB, deduct items error')
            self.client.onEquipEnhanceFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        bagEquipItem.doEnhanceEquip(self, opUUID, enhanceLv)
        self.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
        self.client.onEquipEnhanceSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId,
                                       bagEquipItem.getEnhanceLevel(), bagEquipItem.getEnhanceLvVal())
        # isMaxVal and self.checkAchievementTrigger(gameconst.AchieveTargetType.TARGET_ACTION,
        #                                             gameconst.AchieveTargetActionId.EQUIP_ENHANCE_LEVEL_FULL)
        # self.makeEquipmentEnhanceLog(bagEquipItem.itemId, bagEquipItem.uniqueId, enhanceLv, oldEncVal, enhanceVal,
        #                              bagEquipItem.equipAttr.getEnhanceData()[1], success,equipSetLv)

        # NOTE()(ACHIEVE): 装备::强化或补缀次数
        # self.baseCheckAchievement(gameconst.AchieveTargetType.EQUIPMENT_ENHANCED, ())
        # NOTE()(ACHIEVE): 装备::装备首次达到强化等级
        # self.baseCheckAchievement(gameconst.AchieveTargetType.EQUIPMENT_ENHANCED_TOLVL, (enhanceLv, ))
        return

    def bagEquipGlyphWashing(self, gridId, uniqueId, glyphPos):
        DEBUG_MSG('in bagEquipGlyphWashing:', gridId, uniqueId, glyphPos)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bagEquipItem.uniqueId != uniqueId:
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
        
        costItemDic = bagEquipItem.glyphWashingNeedItems()
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_WEAPON_GLYPH_WASHING
        detail = gameclass.AwardDetail(bodyId=gridId, uniqueId=uniqueId)
        args = (opUUID, gridId, glyphPos)
        self.baseEquipDeductItems(costItemDic, opUUID, srcType, detail, self, 'bagEquipGlyphWashingDeductItemsCB', args,
                                  False, True)
        return

    def bagEquipGlyphWashingDeductItemsCB(self, opStat, opUUID, gridId, glyphPos):
        DEBUG_MSG('in bagEquipGlyphWashingDeductItemsCB:', opStat, opUUID, gridId, glyphPos)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipGlyphWashingDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        ret, _, _ = bagEquipItem.doEquipGlyphWashing(self, glyphPos)
        if ret:
            glyphData = bagEquipItem.equipAttr.glyphDatas[glyphPos]
            self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, glyphData.toClientData())
        return

    def bagEquipGlyphApply(self, gridId, uniqueId, groupId):
        DEBUG_MSG('in bagEquipGlyphApply:', gridId, uniqueId, groupId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bagEquipItem.uniqueId != uniqueId:
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
        self.client.onEquipGlyphApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, groupId)
        return
    
    def bagEquipSpiritApply(self, gridId, uniqueId, groupId):
        DEBUG_MSG('in bagEquipSpiritApply:', gridId, uniqueId, groupId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bagEquipItem.uniqueId != uniqueId:
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
        self.client.onEquipSpiritApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, groupId)
        return
    
    def bagEquipBless(self, gridId, uniqueId):
        DEBUG_MSG('in bagEquipBless:', gridId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bagEquipItem.uniqueId != uniqueId:
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipBless, equipment can not be growing, equipment:', bagEquipItem)
            return
        
        ret = dataUtils.checkEquipmentBlessType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('   in bagEquipBless, equipment can not bless, equipment:', bagEquipItem)
            return False
        
        costItemDic = bagEquipItem.blessNeedItems()
        if not costItemDic:
            ERROR_MSG('     in bagEquipBless, cost is empty:')
            return
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_BLESSING
        detail = gameclass.AwardDetail(bodyId=gridId, uniqueId=uniqueId)
        args = (opUUID, gridId, )
        self.baseEquipDeductItems(costItemDic, opUUID, srcType, detail, self, 'bagEquipBlessDeductItemsCB', args,
                                  False, True)
        return

    def bagEquipBlessDeductItemsCB(self, opStat, opUUID, gridId):
        DEBUG_MSG('in bagEquipBlessDeductItemsCB:', opStat, gridId)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipBlessDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bagEquipItem.doEquipBlessing(self):
            blessAffixes = []
            for oneAffix in bagEquipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, blessAffixes,
                                         bagEquipItem.equipAttr.maxBlessLv,
                                         bagEquipItem.equipAttr.blessLvRate)
        return

    def bagEquipBackBless(self, gridId, uniqueId):
        DEBUG_MSG('in bagEquipBackBless:', gridId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bagEquipItem.uniqueId != uniqueId:
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
                                             bagEquipItem.equipAttr.maxBlessLv,
                                             bagEquipItem.equipAttr.blessLvRate)

    def bagEquipSpiritWashing(self, gridId, uniqueId, spiritPos):
        DEBUG_MSG('in bagEquipSpiritWashing:', gridId, uniqueId, spiritPos)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bagEquipItem.uniqueId != uniqueId:
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
        
        costItemDic = bagEquipItem.spiritWashingNeedItems()
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_AFFIX_WASHING
        detail = gameclass.AwardDetail(bodyId=gridId, uniqueId=uniqueId)
        self.baseEquipDeductItems(costItemDic, opUUID, srcType, detail, self, 'bagEquipSpiritWashingDeductItemsCB', (opUUID, gridId, spiritPos),
                                  False, True)
        return

    def bagEquipSpiritWashingDeductItemsCB(self, opStat, opUUID, gridId, spiritPos):
        DEBUG_MSG('in bagEquipSpiritWashingDeductItemsCB:', opStat, gridId, spiritPos)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipSpiritWashingDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        ret, _, _ = bagEquipItem.doEquipSpiritWashing(self, spiritPos)
        if ret:
            spiritData = bagEquipItem.equipAttr.spiritDatas[spiritPos]
            self.client.onEquipSpiritWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritData.toClientData())
            self.achievementInfo.triggerAchieveByType(
                self, 
                gameconst.AchieveType.EQUIPMENT_WITH_SPIRIT, 
                actionContext.AchievementCtx())
        return

    def reqMultiEquipDisassemble(self, exposed, gridIdList, uniqueIdList):
        DEBUG_MSG('reqMultiEquipDisassemble:', gridIdList, uniqueIdList)
        self.bagData.doBagEquipDisassemble(self, gridIdList, uniqueIdList)

    def bagEquipSell(self, gridId, uniqueId):
        self.bagData.doBagEquipSell(self, gridId, uniqueId)

    def updateBodyEquipDressData(self, dressDataDic):
        self.baseBodyEquipDressDataDic = dressDataDic

    def updateMaxEquipSetLv(self, maxEquipSetLv):
        self.baseMaxEquipSetLv = maxEquipSetLv

    def canEquipAutoDisassemble(self, owner, equipItem):
        cliConfig = self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY, 0)
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

    @gamedecorator.limitcall(1)
    def reqMakeEquipment(self, exposed, itemId, gridIdList, makeType):
        DEBUG_MSG('reqMakeEquipment:', itemId, gridIdList, makeType)
        itemData = dataUtils.getEquipItemData(itemId)
        if not itemData:
            ERROR_MSG('in reqMakeEquipment, gearBase_gearBase not found:', itemId)
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
        needGridIdList = {}
        needCostItems = {}
        okCount = 0
        bindValue = 0
        # 先处理配置表的道具消耗数据，防止重复配置错误
        for val in consumeItem:
            costItemId, itemNum = val
            needCostItems[costItemId] = needCostItems.get(costItemId, 0) + itemNum
        # 分析并计算需要消耗的格子上的道具数量
        for gridId in gridIdList:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if not bagEquipItem:
                continue
            # 检查指定格子材料是否足够
            for costItemID, costItemNum in needCostItems.items():
                if costItemNum <= 0:
                    continue
                if costItemID == bagEquipItem.itemId:
                    if costItemNum > bagEquipItem.itemNum:
                        needCostItems[costItemID] = costItemNum - bagEquipItem.itemNum
                        needGridIdList[gridId] = needGridIdList.get(gridId, 0) + bagEquipItem.itemNum
                        if bagEquipItem.bindType == gameconst.ItemBindType.BIND:
                            bindValue += bagEquipItem.itemNum
                    else:
                        needCostItems[costItemID] = 0
                        needGridIdList[gridId] = needGridIdList.get(gridId, 0) + costItemNum
                        if bagEquipItem.bindType == gameconst.ItemBindType.BIND:
                            bindValue += costItemNum
                        okCount += 1

        if okCount != len(needCostItems):
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
        if len(needGridIdList) == 0 and deductVal.isEmpty():
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
        gearManufUnboundProb = GMCDD.datas['gearManufUnboundProb']['value']
        bindType = gameconst.ItemBindType.NORMAL if random.uniform(0, 1) <= gearManufUnboundProb else gameconst.ItemBindType.BIND
        equipItem = itemFactory.ItemFactory.createItem(itemId, 1, bindType=bindType)
        # 设置绑定值
        equipItem.setBindValue(bindValue)

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

    @gamedecorator.limitcall(1)
    def reqEquipReplace(self, exposed, cfgId, gridId, uniqueId, autoBuy):
        DEBUG_MSG('reqEquipReplace:', cfgId, gridId, uniqueId, autoBuy)
        cfgData = GER.datas.get(cfgId)
        if not cfgData:
            ERROR_MSG('in reqEquipReplace, gearManufacture_replacement not found:', cfgId)
            return
        
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in reqEquipReplace, gridId is invalid:', gridId)
            return
        
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in reqEquipReplace, uniqueId not matched:', bagEquipItem.uniqueId, uniqueId)
            return
        
        if not bagEquipItem.isGood():
            ERROR_MSG('in reqEquipReplace, equipment is not good:', bagEquipItem.uniqueId, uniqueId)
            return
        
        if cfgData["gearID"] != bagEquipItem.itemId:
            ERROR_MSG('in reqEquipReplace, gearManufacture_replacement wrong cfg', cfgData["gearID"], bagEquipItem.itemId)
            return
        
        targetItemId = cfgData["acquireID"]
        if not targetItemId:
            ERROR_MSG('in reqEquipReplace, gearManufacture_replacement is missing acquireID:', bagEquipItem.itemId)
            return 
        
        targetItemData = dataUtils.getEquipItemData(targetItemId)
        if not targetItemData:
            ERROR_MSG('in reqEquipReplace, gearBase_gearBase target item not found:', targetItemId)
            return
        
        if targetItemData['quality'] != bagEquipItem.quality:
            ERROR_MSG('in reqEquipReplace, wrong replacement args:', bagEquipItem.itemId, bagEquipItem.quality, targetItemData['quality'])
            return

        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        consumeItem = cfgData.get('costCurrency')
        if consumeItem is None or len(consumeItem) == 0:
            ERROR_MSG('in reqEquipReplace, gearManufacture_replacement wrong config, missing costCurrency:', bagEquipItem.itemId)
            return
        
        deductVal = dropAward.DeductWealthVal()
        for val in consumeItem:
            costItemId, itemNum = val
            deductVal.addWealthByItemId(costItemId, itemNum)

        deductVal.addWealthByObjList([bagEquipItem])
                
        if not self.canDeductWealth(deductVal, sendMsg=True):
            ERROR_MSG('in reqEquipReplace, canDeductWealth fail:', bagEquipItem.itemId)
            return
        oldData = bagEquipItem.equipAttr.toJson()
        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_EQUIP_REPLACEMENT
        detail = gameclass.AwardDetail(itemId=bagEquipItem.itemId)
        self.deductWealth(src, deductVal, opUUID, detail)

        gearManufUnboundProb = GMCDD.datas['gearReplaceUnboundProb']['value']
        bindType = gameconst.ItemBindType.NORMAL if random.uniform(0, 1) <= gearManufUnboundProb else gameconst.ItemBindType.BIND
        equipItem = itemFactory.ItemFactory.createItem(targetItemId, 1, bindType=bindType)
        
        equipItem.equipAttr.updateAttrFromReplacedEquip(oldData)

        opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem,], opUUID, src, detail)
        if opStat == gameconst.BagOPStat.BAG_OP_STAT_OK:
            self.makeEquipmentGetLog(src, equipItem)
            data = equipItem.toClientEquipItemDict()
            DEBUG_MSG('in reqEquipReplace, addItemsWithPlan success:', opStat, targetItemId)
            self.client.onEquipReplaceSucc(gridId, data)
        else:
            self.client.onEquipReplaceFailed(gridId)
            ERROR_MSG('in reqEquipReplace, addItemsWithPlan fail:', opStat, targetItemId)
        
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

    def makeEquipmentEnhanceLog(self, itemId, uniqueId, enhanceLv, oldVal, newVal, enhanceRate, result,equipSetLv):
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
            'gearSetLevel': equipSetLv,
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
    def gmAddGearbaseEquipItem(self, templateId, bindType=dataUtils.getItemDefaultBindType()):
        DEBUG_MSG('gmAddGearbaseEquipItem:', templateId)
        equipItem = itemFactory.ItemFactory.createItem(templateId, 1, bindType=bindType)
        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_GM
        detail = gameclass.AwardDetail(templateId=templateId)

        opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem, ], opUUID, src, detail)
        if opStat == gameconst.BagOPStat.BAG_OP_STAT_OK:
            self.makeEquipmentGetLog(src, equipItem)
        return opStat

    def gmGenAllEquips(self, quality=gameconst.ItemQuality.RED, bindType=dataUtils.getItemDefaultBindType()):
        import gearBase_gearBase as GBGBD
        equipsDic = {}
        mySchool = gameglobal.roleCache.get(self.id, {}).get('school', 0)
        myClass = mySchool
        myLevel = gameglobal.roleCache.get(self.id, {}).get('level', 0)

        for tid, gearData in GBGBD.datas.items():
            if 0 == gearData['randomWeight']:
                continue
            if myLevel < gearData['equipLevel']:
                continue
            reqClassList = gearData['reqClass']
            if 0 not in reqClassList and myClass not in reqClassList:
                continue
            if quality != gearData['quality']:
                continue
            k = gearData['type']*100 +gearData['subType']
            oldGearDic = equipsDic.get(k, None)
            if oldGearDic:
                if gearData['iLevel'] >= oldGearDic['iLevel']:
                    #替换等级更高的装备
                    equipsDic[k] = {'ID':tid, 'iLevel':gearData['iLevel']}
            else:
                equipsDic[k] = {'ID': tid, 'iLevel': gearData['iLevel']}
        for oneGear in equipsDic.values():
            self.gmAddGearbaseEquipItem(oneGear['ID'], bindType=bindType)
        return

    def gmGenAllRandomEquips(self, bindType=dataUtils.getItemDefaultBindType()):
        import gearBase_gearBase as GBGBD
        import random
        equipsDic = {}
        mySchool = gameglobal.roleCache.get(self.id, {}).get('school', 0)
        myClass = mySchool
        myLevel = gameglobal.roleCache.get(self.id, {}).get('level', 0)

        for tid, gearData in GBGBD.datas.items():
            if 0 == gearData['randomWeight']:
                continue
            if myLevel < gearData['equipLevel']:
                continue
            reqClassList = gearData['reqClass']
            if 0 not in reqClassList and myClass not in reqClassList:
                continue
            k = gearData['type']*100 +gearData['subType']
            equipsDic.setdefault(k,{})
            oldGearDic = equipsDic.get(k).get(gearData['quality'],None)
            if oldGearDic:
                if gearData['iLevel'] >= oldGearDic['iLevel']:
                    #替换等级更高的装备
                    equipsDic[k][gearData['quality']] = {'ID':tid, 'iLevel':gearData['iLevel']}
            else:
                equipsDic[k][gearData['quality']] = {'ID': tid, 'iLevel': gearData['iLevel']}

        DEBUG_MSG("###equipsDic",equipsDic)
        for oneGear in equipsDic.values():
            quality = random.choice(list(oneGear.keys()))
            self.gmAddGearbaseEquipItem(oneGear[quality]['ID'], bindType=bindType)
        return

    def gmGetBagEquipScoreInfo(self, gridId):
        equiItem = self.bagData.getItemObjByGridId(gridId)
        if not equiItem:
            return False, '参数错误'

        if not equiItem.isEquipmentItem():
            return False, '该物品不是装备'
        retStr = equiItem.equipAttr.gmShowScoreInfo(self)
        return True, retStr

    def gmBaseDressEquipsByQuality(self, quality, enhanceLv, bodyDressSlotIds):
        myLevel = gameglobal.roleCache[self.id]['level']
        myClass = gameglobal.roleCache[self.id]['school']
        for gridId, it in self.bagData.gridId2GridObj.items():
            if not it.isEquipmentItem():
                continue
            if it.quality != quality or it.equipAttr.getEnhanceLv() != enhanceLv:
                continue
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
                    self._callback(0.2, 'gmSendDressEquips', (gridId, slotId), gametimer.TIMER_TAG_GM_SEND_DRESS_EQUIPS)
                    break
            if len(bodyDressSlotIds) == 0:
                break
        return

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

    def gmResetBagEquip(self, uniqueId):
        _, equipItem = self.bagData.getItemByUniqueId(uniqueId)
        equipItem and equipItem.gmResetEncAttr()

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

    def giveUpDropEquip(self, exposed, uniqueId):
        INFO_MSG('giveUpDropEquip:', uniqueId)
        if not self.equipDropData.hasTakeDrop(uniqueId):
            ERROR_MSG('giveUpDropEquip not found take:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').giveUpDropEquip(self.gbID, uniqueId, self)

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

