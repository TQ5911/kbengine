# -*- coding: utf-8 -*-

import KBEngine

from KBEDebug import *
import gameconst
import gamedecorator
import dropAward
import awardContext
import gameclass
import Store

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

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

    def reqGetStoreList(self, storeIds):
        DEBUG_MSG('in reqGetStoreList:', storeIds)
        self.storeData.sendStoreList(self, storeIds)
        return

    @gamedecorator.limitcall(1)
    # itemId: mall_coinPrice.datas.ID 不是物品ID
    def reqBuyItemsInStore(self, storeId, itemId, itemNum):
        DEBUG_MSG('in reqBuyItemsInStore:', storeId, itemId, itemNum)
        self._buyItemsInStore(storeId, itemId, itemNum)

    def _buyItemsInStore(self, storeId, itemId, itemNum):
        DEBUG_MSG('in _buyItemsInStore:', storeId, itemId, itemNum)
        self.buyStoreItems(storeId, itemId, itemNum)
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

    def buyStoreItems(self, storeId, itemId, itemNum):
        DEBUG_MSG('in buyStoreItems:', storeId, itemId, itemNum)
        if self.isDestroyed:
            INFO_MSG('buyStoreItems: avatar is offline', storeId, itemId, itemNum)
            return

        if not self.storeData.canBuyStoreItems(self, storeId, itemId, itemNum):
            return

        storeItemData = self.storeData.getStoreItemData(itemId)
        costItem = storeItemData.get('costItem')
        deductWealthVal = dropAward.DeductWealthVal()
        for val in costItem:
            costItemId, num = val
            deductWealthVal.addWealthByItemId(costItemId, num*itemNum)

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

        storeDic = self.storeData.getStoreDic(storeId)

        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
        buyNum = 0
        if storeItemData['limitNumber'] > 0:
            # 限量购买物品
            if itemId not in storeDic:
                storeDic[itemId] = Store.StoreItem(itemId, buyNum=0)
            storeDic[itemId].buyNum += itemNum
            buyNum = storeDic[itemId].buyNum

        self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx=awardCtx)
        self.client.onBuyStoreItems(storeId, itemId, itemNum, buyNum)
