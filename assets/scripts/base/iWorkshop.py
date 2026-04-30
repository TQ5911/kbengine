import KBEngine
from KBEDebug import *

import random

import gameconfig
import gameconst
import gamedecorator
import dataUtils
import dropAward
import gameclass
import LogTrackingMgr

import workShop_config as WSC
import workShop_produce as WSP
import antiAddictCategory_antiAddictCategory_def as AAC_AACD

class IWorkshop(object):
    def __init__(self):
        pass
    #------------------------------------------------client api------------------------------------------------------------------
    @gamedecorator.checkGameconfigEnable('workshop')
    @gamedecorator.limitcall(1)
    def reqWorkshopMF(self, exposed, itemID, batchCount, gridIds, gridNums):    
        LOG_IFO("reqWorkshopMF ", exposed, itemID, batchCount, gridIds, gridNums)
        normalDatas = []
        luckyDatas = []
        if not gameconfig.enableWorkshop():
            LOG_WARN("reqWorkshopSetAutoMF ~ workshop is not open")
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_FUNC_NOT_OPEN, normalDatas, luckyDatas)
            return
        
        if self.bagData.isFull():
            LOG_ERR("reqWorkshopMF ~ bag is full", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_SPACE, normalDatas, luckyDatas)
            return
        
        if self.bagData.isLocked():
            LOG_ERR("reqWorkshopMF ~ bag is locked", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_LOCK, normalDatas, luckyDatas)
            return
        
        if not dataUtils.isValidItemId(itemID):
            LOG_ERR("reqWorkshopMF ~ unknow item id", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_UNKNOW, normalDatas, luckyDatas)
            return
        
        produceCfgData = WSP.datas.get(itemID)
        if not produceCfgData:
            LOG_ERR("reqWorkshopMF ~ unknow produce id", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_UNKNOW, normalDatas, luckyDatas)
            return
    
        if len(gridIds) != len(gridNums):
            LOG_ERR("reqWorkshopMF ~ grid ids are not equal with grid nums", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_UNKNOW, normalDatas, luckyDatas)
            return
        
        batchLimit = WSC.datas['workShop_maxNum'].get("value", 0)
        if batchLimit <= 0:
            LOG_ERR("reqWorkshopMF ~ workShop_config error 1", itemID, batchCount, batchLimit)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG, normalDatas, luckyDatas)
            return
        
        if batchCount > batchLimit:
            LOG_ERR("reqWorkshopMF ~ workShop_config error 2", itemID, batchCount, batchLimit)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_LIMIT_BATCH_COUNT, normalDatas, luckyDatas)
            return
        
        datas = self.calculateComsumeItems(gridIds, gridNums)
        if not datas:
            LOG_ERR("reqWorkshopMF ~ item is not enough", itemID, batchCount)
            self.client.onWorkshopMF(gameconst.WorkshopResult.WORKSHOP_UNKNOW, normalDatas, luckyDatas)
            return
        
        ret, normalDatas, luckyDatas = self.doWorkshopManufactoring(itemID, batchCount, datas, gridIds, gridNums)
        if ret != gameconst.WorkshopResult.WORKSHOP_SUCCESS:
            normalDatas = []
            luckyDatas = []
        self.client.onWorkshopMF(ret, normalDatas, luckyDatas)
    #------------------------------------------------client api------------------------------------------------------------------

    #------------------------------------------------workshop biz----------------------------------------------------------------

    def calculateComsumeItems(self, gridIds, gridNums):
        # 1.先做一轮同个格子上消耗合并，防止客户端分开上传相同格子，避开了服务端的逻辑检查
        gridInfos = {}
        totalCount = len(gridIds)
        for idx in range(0, totalCount):
            gridId = gridIds[idx]
            gridNum = gridNums[idx]
            gridInfos[gridId] = gridInfos.get(gridId, 0) + gridNum
        # 2.拆分绑定和非绑定，便于后面计算生成的绑定概率
        datas = {}
        for gridId, gridNum in gridInfos.items():
            item = self.bagData.getItemObjByGridId(gridId)
            # 检查数量和锁定状态
            if item.itemNum < gridNum or item.isLocked():
                LOG_ERR("calculateComsumeItems ~ item is not enough ", item.itemId, item.itemNum, gridNum, item.isLocked())
                return None
            itemId = item.itemId
            data = datas.get(itemId, None)
            if not data:
                data = [0, 0]
                datas[itemId] = data
            if item.bindType == gameconst.ItemBindType.BIND:
                data[0] += gridNum
            elif item.bindType == gameconst.ItemBindType.NORMAL:
                data[1] += gridNum
        return datas   

    def calculateUseComsumeItems(self, datas, itemId, useCount):
        normalCount, bindCount = 0, 0
        data = datas.get(itemId, None)
        if not data:
            return False, False, 0, 0, useCount
        # 合并计算绑定和非绑定的消耗
        if data[0] + data[1] < useCount:
            normalCount = data[1]
            bindCount = data[0]
            data[0] = 0
            data[1] = 0
            return True, False, normalCount, bindCount, useCount - normalCount - bindCount
        # 非绑的足够，先用非绑的
        if data[1] >= useCount:
            data[1] -= useCount
            normalCount = useCount
        else:
            # 先消耗非绑的，再消耗绑定的
            normalCount = data[1]
            data[1] = 0
            bindCount = useCount - normalCount
            data[0] -= bindCount
        return True, True, normalCount, bindCount, 0

    def doWorkshopManufactoring(self, itemID, batchCount, datas, gridIds, gridNums):
        # 消耗的货币
        costCurrency = {}
        # 产出的道具
        normalItems = {}
        # 幸运的道具
        luckyItems = {}
        ret, _, _ = self.calculateWorkshopMaterials(itemID, batchCount, costCurrency, normalItems, luckyItems, datas)
        if ret == gameconst.WorkshopResult.WORKSHOP_SUCCESS:
            # 检查消耗是否正常
            for _, data in datas.items():
                if data[0] > 0 or data[1] > 0:
                    LOG_ERR("doWorkshopManufactoring ~ materials are over lmit", itemID, batchCount)
                    return gameconst.WorkshopResult.WORKSHOP_UNKNOW, None, None
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACD.datas.BONUS_SRC_WORKSHOP_COST
            # 增加道具
            addWealthVal = dropAward.AwardVal()
            # 扣减货币和道具
            deductWealthVal = dropAward.DeductWealthVal()
            # 正常产出
            normalWealthVal = dropAward.AwardVal()
            # 幸运产出
            luckyWealthVal = dropAward.AwardVal()
            # 常规物品日志记录用
            normalDatas = []
            # 幸运物品日志记录用
            luckyDatas = []

            # 常规物品
            for outItemKey, outItemCount in normalItems.items():
                mID, mBindType = self.splitWorkshopItemKey(outItemKey)
                # 筛选最终产物
                if mID == itemID:
                    addWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
                    normalWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
                normalDatas.append({'itemId':mID, 'itemCount':outItemCount, 'bindType':mBindType, 'quality':dataUtils.getItemQuality(mID)})
            
            # 幸运物品
            for outItemKey, outItemCount in luckyItems.items():
                mID, mBindType = self.splitWorkshopItemKey(outItemKey)
                addWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
                luckyWealthVal.addWealthByItemId(mID, outItemCount, mBindType)
                luckyDatas.append({'itemId':mID, 'itemCount':outItemCount, 'bindType':mBindType, 'quality':dataUtils.getItemQuality(mID)})

            if not self.canAddWealthVal(srcType, addWealthVal):
                LOG_WARN("doWorkshopManufactoring ~ bag space is not enough")
                return gameconst.WorkshopResult.WORKSHOP_LIMIT_BAG_SPACE, None, None
            
            for mID, mCount in costCurrency.items():
                deductWealthVal.addWealthByItemId(mID, mCount)

            if not self.canDeductWealth(deductWealthVal):
                LOG_WARN("doWorkshopManufactoring ~ item is not enough")
                return gameconst.WorkshopResult.WORKSHOP_LIMIT_CURRENCY_IS_NOT_ENOUGH, None, None
            
            costDetail = gameclass.AwardDetail()
            gotDetail = gameclass.AwardDetail()

            consumedGirdData = {}
            totalCount = len(gridIds)
            for idx in range(0, totalCount):
                gridId = gridIds[idx]
                gridNum = gridNums[idx]
                consumedGirdData[gridId] = consumedGirdData.get(gridId, 0) + gridNum
            
            self.bagData.deductItemsByGrid(self, consumedGirdData, opUUID, srcType, costDetail)
                
            # 扣除消耗道具
            self.deductWealth(srcType, deductWealthVal, opUUID, costDetail)
            # 增加获得道具
            self.addWealth(srcType, addWealthVal, opUUID, gotDetail)

            LogTrackingMgr.LogTrackingMgr.Work_Shop(opUUID, self.gbID, itemID, batchCount, normalDatas, luckyDatas)
            return ret, normalWealthVal.toBriefList(), luckyWealthVal.toBriefList()
        return ret, None, None

    def calculateWorkshopMaterials(self, itemID, batchCount, costCurrency, normalItems, luckyItems, datas):
        LOG_IFO("calculateWorkshopMaterials ", itemID, batchCount, costCurrency, normalItems, luckyItems, datas)
        produceCfgData = WSP.datas.get(itemID)
        if not produceCfgData:
            LOG_WARN("calculateWorkshopMaterials ~ this item has no configuration", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_ITEM_IS_NOT_ENOUGH, 0, 0
        
        if produceCfgData['isOpen'] != gameconst.WorkshopOpenStatus.OPEN:
            LOG_ERR("calculateWorkshopMaterials ~ manufacture is closed", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_MANUFACTURE_NOT_OPEN, 0, 0
        
        materials = produceCfgData['materials']
        if not materials:
            LOG_ERR("calculateWorkshopMaterials ~ materials config error", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG, 0, 0
        
        costs = produceCfgData['cost']
        if not costs:
            LOG_ERR("calculateWorkshopMaterials ~ cost config error", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_ILLEGAL_CONFIG, 0, 0
        
        ret, usedNormalCount, usedBindCount = self.doWorkshopCalculation(produceCfgData, itemID, batchCount, costCurrency, normalItems, luckyItems, datas)
        
        return ret, usedNormalCount, usedBindCount
    
    def doWorkshopCalculation(self, produceCfgData, itemID, batchCount, costCurrency, normalItems, luckyItems, datas):
        costs = produceCfgData['cost']
        materials = produceCfgData['materials']
        for cost in costs:
            mID, mCount = cost
            mCount *= batchCount
            costCurrency[mID] = costCurrency.get(mID, 0) + mCount

        deductWealthVal = dropAward.DeductWealthVal()
        for mID, mCount in costCurrency.items():
            deductWealthVal.addWealthByItemId(mID, mCount)

        if not self.canDeductWealth(deductWealthVal):
            LOG_WARN("calculateWorkshopMaterials ~ currency is not enough", produceCfgData, itemID, batchCount)
            return gameconst.WorkshopResult.WORKSHOP_LIMIT_CURRENCY_IS_NOT_ENOUGH, 0, 0
        
        # 制造这一批需要总的绑定和非绑定材料数量
        allNormalCount, allBindCount = 0, 0
        for _ in range(0, batchCount):
            totalNormalCount = 0
            totalBindCount = 0
            for material in materials:
                mID, mCount = material
                isExisted, ret, normalCount, bindCount, needCount = self.calculateUseComsumeItems(datas, mID, mCount)
                # 存在就计数
                if isExisted:
                    totalNormalCount += normalCount
                    totalBindCount += bindCount
                # 不够需要造needCount
                if not ret:
                    ret, usedNormalCount, usedBindCount = self.calculateWorkshopMaterials(mID, needCount, costCurrency, normalItems, luckyItems, datas)
                    if ret != gameconst.WorkshopResult.WORKSHOP_SUCCESS:
                        LOG_WARN("calculateWorkshopMaterials ~ materials is not enough", produceCfgData, itemID, batchCount)
                        return ret, 0, 0
                    totalNormalCount += usedNormalCount
                    totalBindCount += usedBindCount

            totalCount = totalNormalCount + totalBindCount
            # 这里需要分批次随机额外掉落，以及获得道具绑定类型
            if totalNormalCount == totalCount:
                bindType = gameconst.ItemBindType.NORMAL
            elif totalBindCount == totalCount:
                bindType = gameconst.ItemBindType.BIND
            else:
                bindType = gameconst.ItemBindType.NORMAL if random.uniform(0, 1) <= totalNormalCount/(totalBindCount + totalNormalCount) else gameconst.ItemBindType.BIND
            
            # 对制造出来的绑定和非绑定道具进行计数
            if bindType == gameconst.ItemBindType.NORMAL:
                allNormalCount += 1
            elif bindType == gameconst.ItemBindType.BIND:
                allBindCount += 1
            
            outKey = self.getWorkshopOutItemKey(itemID, bindType)
            normalItems[outKey] = normalItems.get(outKey, 0) + 1
            ret = self.calculateWorkshopLuckyItem(luckyItems, produceCfgData)
            if ret != gameconst.WorkshopResult.WORKSHOP_SUCCESS:
                break
        return ret, allNormalCount, allBindCount

    def calculateWorkshopLuckyItem(self, luckyItems, produceCfgData):
        luckyRule = produceCfgData['lucky']
        # 支持空的配置
        if luckyRule is None:
            return gameconst.WorkshopResult.WORKSHOP_SUCCESS
        
        # 如果已配置，检查配置规则
        if len(luckyRule) != 4:
            LOG_ERR("calculateWorkshopLuckyItem ~ lucky config error", produceCfgData)
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