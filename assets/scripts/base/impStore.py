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

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import LogTrackingMgr

class ImpStore(object):

    def onStoreDailyUpdate(self, *args):
        self.storeData.updateStoreDataDaily(self)

    def onStoreWeeklyUpdate(self, *args):
        DEBUG_MSG('in onStoreWeeklyUpdate:', args)
        self.storeData.updateStoreDataWeekly(self)
        return

    def onStoreMonthlyUpdate(self, *args):
        DEBUG_MSG('in onStoreMonthlyUpdate:', args)
        self.storeData.updateStoreDataMonthly(self)
        return

    def onLimitedStoreHourlyUpdate(self, *args):
        DEBUG_MSG('in onLimitedStoreHourlyUpdate:', args)
        self.storeData.updateLimitedStoreHourly(self)

    def reqGetStoreList(self, exposed, storeIds):
        DEBUG_MSG('in reqGetStoreList:', storeIds)
        self.storeData.sendStoreList(self, storeIds)
        return
    
    def reqGetStoreLimitedItemList(self, exposed, storeId):
        DEBUG_MSG('in reqGetStoreLimitedItemList:', exposed, storeId)
        self.storeData.sendStoreLimitedItemList(self, storeId)

    @gamedecorator.limitcall(1)
    # itemId: mall_coinPrice.datas.ID 不是物品ID
    def reqBuyItemsInStore(self, exposed, storeId, itemId, itemNum):
        DEBUG_MSG('in reqBuyItemsInStore:', storeId, itemId, itemNum)
        self._buyItemsInStore(storeId, itemId, itemNum)

    @gamedecorator.limitcall(1)
    def reqBuyItemsInStoreWithSelection(self, exposed, storeId, itemId, itemNum, propSlot):
        DEBUG_MSG('in reqBuyItemsInStoreWithSelection:', exposed, storeId, itemId, itemNum, propSlot)
        self._buyItemsInStore(storeId, itemId, itemNum, propSlot)

    def _buyItemsInStore(self, storeId, itemId, itemNum, propSlot=0):
        DEBUG_MSG('in _buyItemsInStore:', storeId, itemId, itemNum, propSlot)
        self.buyStoreItems(storeId, itemId, itemNum, propSlot)
        return

    def makeMallFlowLog(self, opUUID, cellId, itemId, itemNum, costItemId, costItemNum):
        tlogParams = {
            "role_id": self.gbID,
            "role_name": self.getRoleCacheAttr('name', ''),
            'op_nuid': opUUID,
            'cell_id': cellId,
            'item_id': itemId,
            'buy_cnt': itemNum,
            "money_type": costItemId,
            "cost": costItemNum,
        }
        # gamelog.makeWLog("GameShopBuy", tlogParams)

    def buyStoreItems(self, storeId, itemId, itemNum, propSlot):
        DEBUG_MSG('in buyStoreItems:', storeId, itemId, itemNum, propSlot)
        if self.isDestroyed:
            INFO_MSG('buyStoreItems: avatar is offline', storeId, itemId, itemNum)
            return

        if not self.storeData.canBuyStoreItems(self, storeId, itemId, itemNum):
            return

        storeItemData = self.storeData.getStoreItemData(itemId)
        costItem = storeItemData.get('costItem')
        exType = storeItemData.get('exType')
        propItem = storeItemData.get('propItem')
        deductWealthVal = dropAward.DeductWealthVal()
        for val in costItem:
            costItemId, num = val
            deductWealthVal.addWealthByItemId(costItemId, num*itemNum)
        
        if propItem:
            if exType == gameconst.ItemExType.NORMAL:
                for val in propItem:
                    propItemId, num = val
                    deductWealthVal.addWealthByItemId(propItemId, num*itemNum)
            elif exType == gameconst.ItemExType.SELECTION:
                if propSlot >= len(propItem) or propSlot < 0:
                    ERROR_MSG('buyStoreItems: propSlot out of range:', propSlot, len(propItem))
                    return
                propItemId, num = propItem[propSlot]
                deductWealthVal.addWealthByItemId(propItemId, num*itemNum)

        if not self.canDeductWealth(deductWealthVal):
            WARNING_MSG('buyStoreItems: items not enough:', deductWealthVal)
            return

        awardCtx = awardContext.CommonContext(mailId=gameconst.MailConstID.REWARD_MAIL_ID)
        realItemId = storeItemData['itemId']
        #1是非绑定
        bindType = gameconst.ItemBindType.NORMAL if storeItemData['isBound'] == 1 else gameconst.ItemBindType.BIND
        wealthVal = dropAward.AwardVal().addWealthByItemId(realItemId, itemNum, bindType)

        detail = gameclass.AwardDetail(storeId=storeId, goodsId=itemId, goodsNum=itemNum)
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BUY_STORE_ITEMS
        
        storeCfgData = MSLD.datas.get(storeId)
        tp = 0
        if storeCfgData:
            tp = storeCfgData["type"]
            if tp == gameconst.STORE_TYPE.EXCHANGE_STORE1 or tp == gameconst.STORE_TYPE.EXCHANGE_STORE2:
                srcType = AAC_AACDD.datas.BONUS_SRC_EXCHANGE_STORE_ITEMS

        storeDic = self.storeData.getStoreDic(storeId)

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
                ERROR_MSG('buyStoreItems: no item in limited storeDic:', storeId, itemId, storeDic)
                return
            storeDic[itemId].buyNum += itemNum
            buyNum = storeDic[itemId].buyNum

        self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx=awardCtx)
        self.client.onBuyStoreItems(storeId, itemId, itemNum, bindType, buyNum)

        LogTrackingMgr.LogTrackingMgr.Store_Buy(
            self.gbID,
            storeId,
            tp,
            itemId,
            realItemId,
            itemNum,
            storeItemData['limitType'],
            storeItemData['limitNumber'],
            buyNum,
            str(costItem),
            opUUID,
        )
