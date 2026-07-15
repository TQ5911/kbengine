# -*- coding: utf-8 -*-

import KBEngine

from KBEDebug import *
import gameconst
import gamedecorator
import dropAward
import awardContext
import gameclass
import Store
import mall_storeList as MSLD
import mall_mallConst as MMC
import utils

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import LogTrackingMgr
import gametimer

class ImpStore(object):

    def onStoreDailyUpdate(self, *args):
        fiveTs = utils.getCurDayTS(utils.curTS() - gameconst.GENERAL_CYCLE_TIME, gameconst.GENERAL_CYCLE_TIME)
        dt = utils.curTS() - fiveTs
        LOG_INFO('onStoreDailyUpdate', 'dt', dt)
        #交易行均价每日5点刷新，商店动态定价依赖均价，所以延迟到5.03刷新商品
        if dt < 3 * 60:
            self.addTimerCB(3 * 60 - dt, 'doStoreDailyUpdate', (), gametimer.TIMER_TAG_STORE_DAILY_UPDATE)
        else:
            self.doStoreDailyUpdate()

    def doStoreDailyUpdate(self, *args):
        LOG_INFO('doStoreDailyUpdate')
        self.storeData.updateStoreDataDaily(self)

    def onStoreWeeklyUpdate(self, *args):
        LOG_INFO('in onStoreWeeklyUpdate:', args)
        self.storeData.updateStoreDataWeekly(self)
        return

    def onStoreMonthlyUpdate(self, *args):
        LOG_INFO('in onStoreMonthlyUpdate:', args)
        self.storeData.updateStoreDataMonthly(self)
        return

    def onLimitedStoreHourlyUpdate(self, *args):
        LOG_INFO('in onLimitedStoreHourlyUpdate:', args)
        self.storeData.updateLimitedStoreHourly(self)

    def reqGetStoreList(self, exposed, storeIds):
        LOG_INFO('in reqGetStoreList:', storeIds)
        self.storeData.sendStoreList(self, storeIds)
        return
    
    def reqGetStoreLimitedItemList(self, exposed, storeId):
        LOG_INFO('in reqGetStoreLimitedItemList:', exposed, storeId)
        self.storeData.sendStoreLimitedItemList(self, storeId)

    @gamedecorator.limitcall(1)
    # itemId: mall_coinPrice.datas.ID 不是物品ID
    def reqBuyItemsInStore(self, exposed, storeId, itemId, itemNum):
        LOG_INFO('in reqBuyItemsInStore:', storeId, itemId, itemNum)
        self._buyItemsInStore(storeId, itemId, itemNum)

    @gamedecorator.limitcall(1)
    def reqBuyItemsInStoreWithSelection(self, exposed, storeId, itemId, itemNum, propSlot):
        LOG_INFO('in reqBuyItemsInStoreWithSelection:', exposed, storeId, itemId, itemNum, propSlot)
        self._buyItemsInStore(storeId, itemId, itemNum, propSlot)

    def _buyItemsInStore(self, storeId, itemId, itemNum, propSlot=0):
        LOG_INFO('in _buyItemsInStore:', storeId, itemId, itemNum, propSlot)
        self.buyStoreItems(storeId, itemId, itemNum, propSlot)
        return

    def buyStoreItems(self, storeId, itemId, itemNum, propSlot):
        LOG_INFO('in buyStoreItems:', storeId, itemId, itemNum, propSlot)
        if self.isDestroyed:
            LOG_INFO('buyStoreItems: avatar is offline', storeId, itemId, itemNum)
            return

        if not self.storeData.canBuyStoreItems(self, storeId, itemId, itemNum):
            return

        storeItemData = self.storeData.getStoreItemData(itemId)
        costItem = storeItemData.get('costItem')
        exType = storeItemData.get('exType')
        propItem = storeItemData.get('propItem')
        itemType = storeItemData.get('type')

        #月卡用户额外次数
        if not self.isPremiumIdMonthCardExpired(MMC.datas['dynGoodsMonthCardTypeId']['value']):
            if itemType == gameconst.StoreItemType.DYNAMIC_PRICE:
                newCostItem = storeItemData.get('monthCardCostItem')
                LOG_INFO('buyStoreItems isBigMonthCard', costItem, '->', newCostItem)
                costItem = newCostItem
        
        #限量物品才可能有动态价格
        storeDic = self.storeData.getStoreDic(storeId)
        if storeItemData['limitNumber'] > 0 and storeItemData['groupId'] == 0:
            if itemId not in storeDic:
                storeDic[itemId] = Store.StoreItem(itemId, buyNum=0)
            price = storeDic[itemId].price
            if price > 0:
                if len(costItem) != 1:
                    LOG_ERR('buyStoreItems: costItem length != 1:', costItem)
                    return
                costItem = list(costItem)
                costItem[0] = list(costItem[0])
                costItem[0][1] = price

        deductWealthVal = dropAward.DeductWealthVal()
        if costItem:
            for val in costItem:
                costItemId, num = val
                deductWealthVal.addWealthByItemId(costItemId, num*itemNum)
        
        if propItem:
            if exType == gameconst.ItemExType.NORMAL:
                for val in propItem:
                    propItemId, num, bindtype = val
                    deductWealthVal.addWealthByItemId(propItemId, num*itemNum, bindtype)
            elif exType == gameconst.ItemExType.SELECTION:
                if propSlot >= len(propItem) or propSlot < 0:
                    LOG_ERR('buyStoreItems: propSlot out of range:', propSlot, len(propItem))
                    return
                propItemId, num, bindtype = propItem[propSlot]
                deductWealthVal.addWealthByItemId(propItemId, num*itemNum, bindtype)

        if not self.canDeductWealth(deductWealthVal):
            LOG_WARN('buyStoreItems: items not enough:', deductWealthVal)
            return

        awardCtx = self.getAvatarAwardCtx(0, None, gameconst.MailConstEnum.REWARD_MAIL_ID)
        realItemId = storeItemData['itemId']
        #1是非绑定
        bindType = gameconst.ItemBindType.NORMAL if storeItemData['isBound'] == 1 else gameconst.ItemBindType.BIND
        wealthVal = dropAward.AwardVal().addWealthByItemId(realItemId, itemNum, bindType)

        detail = gameclass.AwardDetailCls(storeId=storeId, goodsId=itemId, goodsNum=itemNum)
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BUY_STORE_ITEMS
        
        storeCfgData = MSLD.datas.get(storeId)
        tp = 0
        if storeCfgData:
            tp = storeCfgData["type"]
            if tp == gameconst.STORE_TYPE.EXCHANGE_STORE1 or tp == gameconst.STORE_TYPE.EXCHANGE_STORE2:
                srcType = AAC_AACDD.datas.BONUS_SRC_EXCHANGE_STORE_ITEMS

        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
        buyNum = 0
        if storeItemData['limitNumber'] > 0 and storeItemData['groupId'] == 0:
            # 限量购买物品
            if itemId not in storeDic:
                storeDic[itemId] = Store.StoreItem(itemId, buyNum=0)
            storeDic[itemId].buyNum += itemNum
            buyNum = storeDic[itemId].buyNum

        if storeItemData['groupId'] != 0:
            # 商店随机物品
            storeDic = self.storeData.getLimitStoreDic(storeId)
            if itemId not in storeDic:
                LOG_ERR('buyStoreItems: no item in limited storeDic:', storeId, itemId, storeDic)
                return
            storeDic[itemId].buyNum += itemNum
            buyNum = storeDic[itemId].buyNum

        self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx=awardCtx)
        self.client.onBuyStoreItems(storeId, itemId, itemNum, bindType, buyNum)

        LogTrackingMgr.LogTrackingMgr.Store_Buy(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            storeId,
            tp,
            itemId,
            realItemId,
            itemNum,
            storeItemData['limitType'],
            storeItemData['limitNumber'] + self._getBigMonthCardAddNum(storeItemData) + self._getStoreLevelAddNum(storeItemData),
            buyNum,
            str(costItem),
            opUUID,
            self.accountEntity.accountName,
            self.obId,
        )

    def _getBigMonthCardAddNum(self, storeItemData):
        if storeItemData['type'] == gameconst.StoreItemType.DYNAMIC_PRICE and not self.isBigMonthCardExpired():
            level = self.getRoleCacheAttr('level')
            count = 0
            for val in MMC.datas['monthCardExtraTimes']['value']:
                if level >= val[0]:
                    count += val[1]
            return count
        return 0

    # 等级越高，能买的数量越多
    def _getStoreLevelAddNum(self, storeItemData):
        level = self.getRoleCacheAttr('level')
        count = 0
        for val in MMC.datas['dynGoodsExtraTimes']['value']:
            if level >= val[0]:
                count += val[1]
        return count

