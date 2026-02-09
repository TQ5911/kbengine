import KBEngine
from KBEDebug import *

import random
import itertools

import gameconfig
import gameconst
import gamedecorator
import dataUtils
import dropAward
import gameclass
import LogTrackingMgr

import workShop_config as WSC
import workShop_produce as WSP
import itemData_itemData as ITEMDATA
import antiAddictCategory_antiAddictCategory_def as AAC_AACD

class IWorkshop(object):
    def __init__(self):
        pass
    #------------------------------------------------client api------------------------------------------------------------------
    @gamedecorator.checkGameconfigEnable('workshop')
    @gamedecorator.limitcall(1)
    def reqWorkshopMF(self, exposed, itemID, batchCount, isAutoMF):    
        INFO_MSG("reqWorkshopMF ", exposed, itemID, batchCount, isAutoMF)
        normalDatas = []
        luckyDatas = []
        if not gameconfig.enableWorkshop():
            WARNING_MSG("reqWorkshopSetAutoMF ~ workshop is not open")
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_FUNC_NOT_OPEN, isAutoMF, normalDatas, luckyDatas)
            return
        
        if self.bagData.isFull():
            ERROR_MSG("reqWorkshopMF ~ bag is full", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_SPACE, isAutoMF, normalDatas, luckyDatas)
            return
        
        if self.bagData.isLocked():
            ERROR_MSG("reqWorkshopMF ~ bag is locked", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_LOCK, isAutoMF, normalDatas, luckyDatas)
            return
        
        if not dataUtils.isValidItemId(itemID):
            ERROR_MSG("reqWorkshopMF ~ unknow item id", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_UNKNOW, isAutoMF, normalDatas, luckyDatas)
            return
        
        produceCfgData = WSP.datas.get(itemID)
        if not produceCfgData:
            ERROR_MSG("reqWorkshopMF ~ unknow produce id", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_UNKNOW, isAutoMF, normalDatas, luckyDatas)
            return
        
        batchLimit = WSC.datas['workShop_maxNum'].get("value", 0)
        if batchLimit <= 0:
            ERROR_MSG("reqWorkshopMF ~ workShop_config error", itemID, batchCount, batchLimit)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG, isAutoMF, normalDatas, luckyDatas)
            return
        
        if batchCount > batchLimit:
            ERROR_MSG("reqWorkshopMF ~ workShop_config error", itemID, batchCount, batchLimit)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BATCH_COUNT, isAutoMF, normalDatas, luckyDatas)
            return
        
        ret, normalDatas, luckyDatas = self.doWorkshopManufactoring(itemID, batchCount, isAutoMF)
        if ret != gameconst.WorkshopResult.WORKSHOP_SUCCESS:
            normalDatas = []
            luckyDatas = []
        self.client.onWorkshopMF(ret, isAutoMF, normalDatas, luckyDatas)
    #------------------------------------------------client api------------------------------------------------------------------

    #------------------------------------------------workshop biz----------------------------------------------------------------

    def doWorkshopManufactoring(self, itemID, batchCount, isAutoMF):
        # 消耗的道具
        costItems = {}
        # 消耗的货币
        costCurrency = {}
        # 产出的道具
        normalItems = {}
        # 幸运的道具
        luckyItems = {}
        # 中间产出的需扣除道具
        costExtraItems = {}
        ret = self.calculateWorkshopMaterials(itemID, batchCount, costCurrency, costItems, normalItems, luckyItems, costExtraItems, isAutoMF)
        if ret == gameconst.WorkshopResult.WORKSHOP_SUCCESS:
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACD.datas.BONUS_SRC_WORKSHOP_COST
            addWealthVal = dropAward.AwardVal()
            normalDatas = []
            luckyDatas = []
            # 常规物品
            for outItemKey, outItemCount in normalItems.items():
                mID, mBindType = self.splitWorkshopItemKey(outItemKey)
                addWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
                normalDatas.append({'itemId':mID, 'itemCount':outItemCount, 'bindType':mBindType, 'quality':dataUtils.getItemQuality(mID)})
            # 幸运物品
            for outItemKey, outItemCount in luckyItems.items():
                mID, mBindType = self.splitWorkshopItemKey(outItemKey)
                addWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
                luckyDatas.append({'itemId':mID, 'itemCount':outItemCount, 'bindType':mBindType, 'quality':dataUtils.getItemQuality(mID)})

            if not self.canAddWealthVal(srcType, addWealthVal):
                WARNING_MSG("doWorkshopManufactoring ~ bag space is not enough")
                return gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_SPACE, None, None
            
            # 扣减货币和道具
            deductWealthVal = dropAward.DeductWealthVal()
            for mID, mCount in costCurrency.items():
                deductWealthVal.addWealthByItemId(mID, mCount)
            for mID, mCount in costItems.items():
                deductWealthVal.addWealthByItemId(mID, mCount)

            if not self.canDeductWealth(deductWealthVal):
                WARNING_MSG("doWorkshopManufactoring ~ item is not enough")
                return gameconst.WorkshopResult.WORKSHOP_LIMIT_CURRENCY_IS_NOT_ENOUGH, None, None
            
            costDetail = gameclass.AwardDetail(costItems=costItems)
            gotDetail = gameclass.AwardDetail(normalItems=normalItems, luckyItems = luckyItems)
            # 扣除消耗道具
            self.deductWealth(srcType, deductWealthVal, opUUID, costDetail)
            # 增加获得道具
            self.addWealth(srcType, addWealthVal, opUUID, gotDetail)
            # 扣除额外获得
            deductWealthVal = dropAward.DeductWealthVal()
            for mID, mCount in costExtraItems.items():
                deductWealthVal.addWealthByItemId(mID, mCount)
            self.deductWealth(srcType, deductWealthVal, opUUID, costDetail)

            # 需要计算最终的产出，去掉过程展示
            for itemID, itemNum in costExtraItems.items():
                remain = itemNum
                # 先用绑定的
                key = self.getWorkshopOutItemKey(itemID, gameconst.ItemBindType.BIND)
                num = normalItems.get(key, None)
                if num is not None:
                    if num > itemNum:
                        remain = 0
                        normalItems[key] = num - itemNum
                    else:
                        remain = itemNum - num
                        normalItems.pop(key)
                #  再处理非绑定
                if remain > 0:
                    key = self.getWorkshopOutItemKey(itemID, gameconst.ItemBindType.NORMAL)
                    num = normalItems.get(key, None)
                    if num is not None:
                        if num > itemNum:
                            remain = 0
                            normalItems[key] = num - itemNum
                        else:
                            remain = itemNum - num
                            normalItems.pop(key)
            # 最终道具
            normalWealthVal = dropAward.AwardVal()
            for outItemKey, outItemCount in normalItems.items():
                mID, mBindType = self.splitWorkshopItemKey(outItemKey)
                normalWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
            # 幸运道具
            luckyWealthVal = dropAward.AwardVal()
            for outItemKey, outItemCount in luckyItems.items():
                mID, mBindType = self.splitWorkshopItemKey(outItemKey)
                luckyWealthVal.addWealthByItemId(mID, outItemCount, mBindType)

            # 最终的产出
            finalItems = []
            for outItemKey, outItemCount in normalItems.items():
                mID, mBindType = self.splitWorkshopItemKey(outItemKey)
                addWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
                finalItems.append({'itemId':mID, 'itemCount':outItemCount, 'bindType':mBindType, 'quality':dataUtils.getItemQuality(mID)})

            LogTrackingMgr.LogTrackingMgr.Work_Shop(opUUID, self.gbID, normalDatas, luckyDatas, finalItems)
            return ret, normalWealthVal.toBriefList(), luckyWealthVal.toBriefList()
        return ret, None, None

    def calculateWorkshopMaterials(self, itemID, batchCount, costCurrency, costItems, normalItems, luckyItems, costExtraItems, isAutoMF):
        INFO_MSG("calculateWorkshopMaterials ", itemID, batchCount, costCurrency, costItems, normalItems, luckyItems, costExtraItems, isAutoMF)
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
        
        ret = self.doWorkshopCalculation(produceCfgData, itemID, batchCount, costCurrency, costItems, normalItems, luckyItems, costExtraItems, isAutoMF)
        
        return ret
    
    def doWorkshopCalculation(self, produceCfgData, itemID, batchCount, costCurrency, costItems, normalItems, luckyItems, costExtraItems, isAutoMF):
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
                ret = self.calculateWorkshopMaterials(mID, mCount, costCurrency, costItems, normalItems, luckyItems, costExtraItems, isAutoMF)
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
            normalItems[outKey] = normalItems.get(outKey, 0) + 1
            ret = self.calculateWorkshopLuckyItem(luckyItems, produceCfgData)
            if ret != gameconst.WorkshopResult.WORKSHOP_SUCCESS:
                break
        return ret

    def calculateWorkshopLuckyItem(self, luckyItems, produceCfgData):
        luckyRule = produceCfgData['lucky']
        # 支持空的配置
        if luckyRule is None:
            return gameconst.WorkshopResult.WORKSHOP_SUCCESS
        
        # 如果已配置，检查配置规则
        if len(luckyRule) != 4:
            ERROR_MSG("calculateWorkshopLuckyItem ~ lucky config error", produceCfgData)
            return gameconst.WorkshopResult.WORKSHOP_SUCCESS
        
        luckyProb = luckyRule[2]
        if random.uniform(0, 1) <= luckyProb:
            itemID = luckyRule[0]
            itemCount = luckyRule[1]
            bindType = gameconst.ItemBindType.NORMAL if random.uniform(0, 1) <= luckyRule[3] else gameconst.ItemBindType.BIND
            outKey = self.getWorkshopOutItemKey(itemID, bindType)
            luckyItems[outKey] = luckyItems.get(outKey, 0) + itemCount
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