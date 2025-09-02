# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
import userType
import gameconst
import mall_storeList as MSLD
import mall_coinPrice as MCPD
import mall_mallConst as MMCD
import dataUtils
import utils


class StoreItem(userType.UserSoleType):
    def __init__(self, itemId=0, buyNum=0):
        self.itemId = itemId
        self.buyNum = buyNum

    def toStoreItemSavedDict(self):
        return {
            'itemId': self.itemId,
            'buyNum': self.buyNum,
        }

    def fromStoreItemSavedDict(self, dic):
        self.itemId = dic['itemId']
        self.buyNum = dic['buyNum']

    def initFromDataDic(self, dataDic):
        self.itemId = dataDic['itemId']
        self.buyNum = dataDic['buyNum']


class StoreData(userType.UserSoleType):

    def __init__(self):
        self.stores = {}
        self.resetStores()
        return

    def _lateReload(self):
        super(StoreData, self)._lateReload()
        for storeDic in self.stores.values():
            for storeItem in storeDic.values():
                storeItem.reloadScript()

        return

    def resetStores(self):
        self.stores.clear()
        for storeId in MSLD.datas.keys():
            self.stores.setdefault(storeId, {})
            self.setStoreData(storeId, [])

    def toStoreDataSavedDict(self):
        stores = []
        for storeId, storeDic in self.stores.items():
            stores.append({'storeId': storeId, 'itemsList': list(storeDic.values()),
                           })
        return {'stores': stores}

    def fromStoreDataSavedDict(self, dic):
        for storeDic in dic['stores']:
            self.setStoreData(storeDic['storeId'], storeDic['itemsList'])
        return

    def setStoreData(self, storeId, savedStoreItemList):
        storeCfgData = MSLD.datas.get(storeId)
        if not storeCfgData:
            return
        storeDataDic = self.getStoreDic(storeId)
        for storeItem in savedStoreItemList:
            # 处理有限量的物品
            storeDataDic[storeItem.itemId] = storeItem
        return

    def updateStoreDataDaily(self, owner):
        DEBUG_MSG('in updateStoreDataDaily')
        for storeId, storeDic in self.stores.items():
            for itemId, storeItem in storeDic.items():
                storeItemData = self.getStoreItemData(itemId)
                if storeItemData['limitType'] == gameconst.StoreLimitType.DAILY:
                    storeItem.buyNum = 0
        self.sendStoreList(owner, list(self.stores.keys()))

    def updateStoreDataWeekly(self, owner):
        DEBUG_MSG('in updateStoreDataWeekly')
        for storeId, storeDic in self.stores.items():
            for itemId, storeItem in storeDic.items():
                storeItemData = self.getStoreItemData(itemId)
                if storeItemData['limitType'] == gameconst.StoreLimitType.WEEKLY:
                    storeItem.buyNum = 0
        self.sendStoreList(owner, list(self.stores.keys()))

    def updateStoreDataMonthly(self, owner):
        DEBUG_MSG('in updateStoreDataMonthly')
        for storeId, storeDic in self.stores.items():
            for itemId, storeItem in storeDic.items():
                storeItemData = self.getStoreItemData(itemId)
                if storeItemData['limitType'] == gameconst.StoreLimitType.MONTHLY:
                    storeItem.buyNum = 0
        self.sendStoreList(owner, list(self.stores.keys()))

    def sendStoreList(self, owner, storeIds):
        DEBUG_MSG('in sendStoreList:', storeIds)
        clientStoreList = []
        for storeId in storeIds:
            storeDic = self.getStoreDic(storeId)
            clientStoreDic = {
                'storeId': storeId,
                'itemsList': list(storeDic.values()),
            }
            clientStoreList.append(clientStoreDic)
        DEBUG_MSG('     in sendStoreList, client:', clientStoreList)
        owner.client.onGetStoreList(clientStoreList)
        return

    def getStoreDic(self, storeId):
        return self.stores.get(storeId)

    @staticmethod
    def getStoreItemData(itemId):
        return MCPD.datas.get(itemId)

    def canBuyStoreItems(self, owner, storeId, itemId, itemNum):
        DEBUG_MSG('in canBuyStoreItems:', storeId, itemId)
        storeData = MSLD.datas.get(storeId)
        if not storeData:
            ERROR_MSG('   in canBuyItems, no store cfg:', storeId)
            return False

        isTimeLimit = storeData['isTimeLimit']
        if isTimeLimit:
            if not utils.inTimeTuplesRange(storeData['openTime'], storeData['closeTime'], utils.getNow()):
                ERROR_MSG('   in canBuyItems, store not open:', storeId, itemId)
                return

        if itemId not in storeData['goodsList']:
            ERROR_MSG('   in canBuyItems, store no this item:', storeId, itemId)
            return False

        storeItemData = self.getStoreItemData(itemId)
        if not storeItemData:
            WARNING_MSG('   in canBuyItems, no item cfg:', storeId, itemId)
            return False

        if storeItemData['guildMallLv'] and storeItemData['guildMallLv'] > owner.wuHuaLevel:
            WARNING_MSG('   in canBuyItems, guildMallLv limit:', storeId, itemId, owner.wuHuaLevel)
            return False

        if storeItemData['startTime'] and storeItemData['deleteTime']:
            if not utils.inTimeTuplesRange(storeItemData['startTime'], storeItemData['deleteTime'], utils.getNow()):
                WARNING_MSG('   in canBuyItems, not on sale:', storeId, itemId)
                # 尚未到上架时间
                return False

        if storeItemData['limitNumber'] > 0:
            # 限量购买
            storeDic = self.getStoreDic(storeId)
            if itemId not in storeDic:
                storeDic[itemId] = StoreItem(itemId, buyNum=0)
            if itemNum > storeItemData['limitNumber'] - storeDic[itemId].buyNum:
                WARNING_MSG('   in canBuyItems, weekBuyNum limit:',
                            storeItemData['limitNumber'], storeDic[itemId].buyNum)
                owner.onMessagePre(MMCD.datas['mall_itemSoldOut_msg']['value'], [])
                return False

        return True
