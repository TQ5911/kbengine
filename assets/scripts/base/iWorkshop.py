import KBEngine
from KBEDebug import *

import random

import gameconfig
import gameconst
import gamedecorator
import dataUtils
import dropAward
import gameclass

import workShop_config as WSC
import workShop_produce as WSP
import antiAddictCategory_antiAddictCategory_def as AAC_AACD

class IWorkshop(object):
    def __init__(self):
        pass
    #------------------------------------------------client api------------------------------------------------------------------
    @gamedecorator.limitcall(1)
    def reqWorkshopMF(self, exposed, itemID, batchCount, isAutoMF):    
        DEBUG_MSG("reqWorkshopMF ", exposed, itemID, batchCount, isAutoMF)
        if not gameconfig.enableWorkshop():
            WARNING_MSG("reqWorkshopSetAutoMF ~ workshop is not open")
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_FUNC_NOT_OPEN, itemID, batchCount, isAutoMF)
            return
        
        if self.bagData.isFull():
            ERROR_MSG("reqWorkshopMF ~ bag is full", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_SPACE, itemID, batchCount, isAutoMF)
            return
        
        if self.bagData.isLocked():
            ERROR_MSG("reqWorkshopMF ~ bag is locked", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_LOCK, itemID, batchCount, isAutoMF)
            return
        
        if not dataUtils.isValidItemId(itemID):
            ERROR_MSG("reqWorkshopMF ~ unknow item id", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_UNKNOW, itemID, batchCount, isAutoMF)
            return
        
        produceCfgData = WSP.datas.get(itemID)
        if not produceCfgData:
            ERROR_MSG("reqWorkshopMF ~ unknow produce id", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_UNKNOW, itemID, batchCount, isAutoMF)
            return
        
        batchLimit = WSC.datas['workShop_maxNum'].get("value", 0)
        if batchLimit <= 0:
            ERROR_MSG("reqWorkshopMF ~ workShop_config error", itemID, batchCount, batchLimit)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG, itemID, batchCount, isAutoMF)
            return
        
        if batchCount > batchLimit:
            ERROR_MSG("reqWorkshopMF ~ workShop_config error", itemID, batchCount, batchLimit)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BATCH_COUNT, itemID, batchCount, isAutoMF)
            return
        
        ret = self.doWorkshopManufactoring(itemID, batchCount, isAutoMF)

        self.client.onWorkshopMF(ret, itemID, batchCount, isAutoMF)

    #------------------------------------------------client api------------------------------------------------------------------

    #------------------------------------------------workshop biz----------------------------------------------------------------

    def doWorkshopManufactoring(self, itemID, batchCount, isAutoMF):
        # 消耗的道具
        costItems = {}
        # 消耗的货币
        costCurrency = {}
        # 产出的道具
        outItems = {}
        # 中间产出的需扣除道具
        costExtraItems = {}
        ret = self.calculateWorkshopMaterials(itemID, batchCount, costCurrency, costItems, outItems, costExtraItems, isAutoMF)
        if ret == gameconst.WorkshopResult.WORKSHOP_SUCCESS:
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACD.datas.BONUS_SRC_WORKSHOP_COST
            addWealthVal = dropAward.AwardVal()
            for outItemKey, outItemCount in outItems.items():
                mID, mBindType = self.splitWorkshopItemKey(outItemKey)
                addWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
            if not self.canAddWealthVal(srcType, addWealthVal):
                WARNING_MSG("doWorkshopManufactoring ~ bag space is not enough")
                return gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_SPACE
            
            # 扣减货币和道具
            deductWealthVal = dropAward.DeductWealthVal()
            for mID, mCount in costCurrency.items():
                deductWealthVal.addWealthByItemId(mID, mCount)
            for mID, mCount in costItems.items():
                deductWealthVal.addWealthByItemId(mID, mCount)

            if not self.canDeductWealth(deductWealthVal):
                WARNING_MSG("doWorkshopManufactoring ~ item is not enough")
                return gameconst.WorkshopResult.WORKSHOP_LIMIT_CURRENCY_IS_NOT_ENOUGH
              
            costDetail = gameclass.AwardDetail(costItems=costItems)
            gotDetail = gameclass.AwardDetail(gotItems=outItems)
            # 扣除消耗道具
            self.deductWealth(srcType, deductWealthVal, opUUID, costDetail)
            # 增加获得道具
            self.addWealth(srcType, addWealthVal, opUUID, gotDetail)
            # 扣除额外获得
            deductWealthVal = dropAward.DeductWealthVal()
            for mID, mCount in costExtraItems.items():
                deductWealthVal.addWealthByItemId(mID, mCount)
            self.deductWealth(srcType, deductWealthVal, opUUID, costDetail)
        return ret

    def calculateWorkshopMaterials(self, itemID, batchCount, costCurrency, costItems, outItems, costExtraItems, isAutoMF):
        DEBUG_MSG("calculateWorkshopMaterials ", itemID, batchCount, costCurrency, outItems, costItems, costExtraItems, isAutoMF)
        produceCfgData = WSP.datas.get(itemID)
        if not produceCfgData:
            WARNING_MSG("calculateWorkshopMaterials ~ this item has no configuration", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_ITEM_IS_NOT_ENOUGH
        
        if produceCfgData['isOpen'] != gameconst.WorkshopOpenStatus.OPEN:
            ERROR_MSG("calculateWorkshopMaterials ~ manufacture is closed", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_MANUFACTURE_NOT_OPEN
        
        materials = produceCfgData['materials']
        if not materials:
            ERROR_MSG("calculateWorkshopMaterials ~ materials config error", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG
        
        costs = produceCfgData['cost']
        if not costs:
            ERROR_MSG("calculateWorkshopMaterials ~ cost config error", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG
        
        unboundProb = produceCfgData['unboundProb']
        if unboundProb is None:
            ERROR_MSG("calculateWorkshopMaterials ~ unboundProb config error", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG
        
        ret = self.doWorkshopCalculation(produceCfgData, itemID, batchCount, costCurrency, costItems, outItems, costExtraItems, isAutoMF)
        
        return ret
    
    def doWorkshopCalculation(self, produceCfgData, itemID, batchCount, costCurrency, costItems, outItems, costExtraItems, isAutoMF):
        costs = produceCfgData['cost']
        materials = produceCfgData['materials']
        unboundProb = produceCfgData['unboundProb']
        for cost in costs:
            mID, mCount = cost
            mCount *= batchCount
            costCurrency[mID] = costCurrency.get(mID, 0) + mCount

        deductWealthVal = dropAward.DeductWealthVal()
        for mID, mCount in costCurrency.items():
            deductWealthVal.addWealthByItemId(mID, mCount)

        if not self.canDeductWealth(deductWealthVal):
            WARNING_MSG("calculateWorkshopMaterials ~ currency is not enough", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_CURRENCY_IS_NOT_ENOUGH

        for material in materials:
            mID, mCount = material
            mCount *= batchCount
            remainCount = self.bagData.getItemCount(mID, gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED)
            if mCount > remainCount:
                # 材料不足，检查是否开启自动合成
                if not isAutoMF:
                    WARNING_MSG("calculateWorkshopMaterials ~ item is not enough 1", produceCfgData, itemID, batchCount)
                    return gameconst.WorkshopResult.WORKSHOP_LIMIT_ITEM_IS_NOT_ENOUGH
                if remainCount > 0:
                    costItems[mID] = costItems.get(mID, 0) + remainCount
                mCount -= remainCount
                ret = self.calculateWorkshopMaterials(mID, mCount, costCurrency, costItems, outItems, costExtraItems, isAutoMF)
                if ret != gameconst.WorkshopResult.WORKSHOP_SUCCESS:
                    WARNING_MSG("calculateWorkshopMaterials ~ materials is not enough", produceCfgData, itemID, batchCount)
                    return ret
                costExtraItems[mID] = costExtraItems.get(mID, 0) + mCount
            else:    
                costItems[mID] = costItems.get(mID, 0) + mCount
        
        deductWealthVal = dropAward.DeductWealthVal()
        for mID, mCount in costItems.items():
            deductWealthVal.addWealthByItemId(mID, mCount)
            
        if not self.canDeductWealth(deductWealthVal):
            WARNING_MSG("calculateWorkshopMaterials ~ item is not enough 2", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_CURRENCY_IS_NOT_ENOUGH
        
        # 这里需要分批次随机额外掉落，以及获得道具绑定类型
        for i in range(0, batchCount):
            bindType = gameconst.ItemBindType.NORMAL if random.uniform(0, 1) <= unboundProb else gameconst.ItemBindType.BIND
            outKey = self.getWorkshopOutItemKey(itemID, bindType)
            outItems[outKey] = outItems.get(outKey, 0) + 1
            ret = self.calculateWorkshopLuckyItem(outItems, produceCfgData)
            if ret != gameconst.WorkshopResult.WORKSHOP_SUCCESS:
                break
        return ret

    def calculateWorkshopLuckyItem(self, outItems, produceCfgData):
        luckyRule = produceCfgData['lucky']
        if luckyRule is None or len(luckyRule) != 4:
            ERROR_MSG("calculateWorkshopLuckyItem ~ lucky config error", produceCfgData)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG
        
        luckyProb = luckyRule[2]
        if random.uniform(0, 1) <= luckyProb:
            itemID = luckyRule[0]
            itemCount = luckyRule[1]
            bindType = gameconst.ItemBindType.NORMAL if random.uniform(0, 1) <= luckyRule[3] else gameconst.ItemBindType.BIND
            outKey = self.getWorkshopOutItemKey(itemID, bindType)
            outItems[outKey] = outItems.get(outKey, 0) + itemCount
        return gameconst.WorkshopResult.WORKSHOP_SUCCESS
    
    def getWorkshopOutItemKey(self, itemID, itemBindType):
        chaSign = self.getWorkshopSeparatorSign()
        return "{0}{1}{2}".format(itemID, chaSign, itemBindType)
    
    def splitWorkshopItemKey(self, outItemKey):
        chaSign = self.getWorkshopSeparatorSign()
        itemID, itemBindType = outItemKey.split(chaSign)
        return int(itemID), int(itemBindType)
    
    def getWorkshopSeparatorSign(self):
        return '_'
    
    #------------------------------------------------workshop biz----------------------------------------------------------------