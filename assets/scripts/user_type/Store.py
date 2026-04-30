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
import random
import time
import itemData_set as IDSD

class StoreItem(userType.UserSingleType):
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


class StoreData(userType.UserSingleType):

    def __init__(self):
        self.stores = {}
        self.limitedStores = {}
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
        
        for storeId, data in MSLD.datas.items():
            if data['groupId']:
                self.limitedStores.setdefault(storeId, {})

    def toStoreDataSavedDict(self):
        stores = []
        for storeId, storeDic in self.stores.items():
            stores.append({'storeId': storeId, 'itemsList': list(storeDic.values()),
                           })
            
        limitedStores = []
        for storeId, storeDic in self.limitedStores.items():
            limitedStores.append({'storeId': storeId, 'itemsList': list(storeDic.values()),})
        return {'stores': stores, 'limitedStores': limitedStores}

    def fromStoreDataSavedDict(self, dic):
        for storeDic in dic['stores']:
            self.setStoreData(storeDic['storeId'], storeDic['itemsList'])
        for storeDic in dic['limitedStores']:
            storeId = storeDic['storeId']
            for storeItem in storeDic['itemsList']:
                self.limitedStores[storeId][storeItem.itemId] = storeItem

    def setStoreData(self, storeId, savedStoreItemList):
        storeCfgData = MSLD.datas.get(storeId)
        if not storeCfgData:
            return
        storeDataDic = self.getStoreDic(storeId)
        for storeItem in savedStoreItemList:
            # 处理有限量的物品
            storeDataDic[storeItem.itemId] = storeItem
        return
    
    def _checkAndUpdateLimitedStoreHourly(self, owner, storeId):
        nowHour = time.localtime(utils.curTS()).tm_hour
        LOG_DBG('in _checkAndUpdateLimitedStoreHourly, storeId:', storeId, nowHour)
        storeCfgData = MSLD.datas.get(storeId)
        if not storeCfgData:
            LOG_ERR('updateLimitedStoreHourly, no store cfg:', storeId)
            return 0
        nextRefreshTime = self.getNextRefreshTime(storeId)
        if nextRefreshTime == 0:
            return 0
        if storeId not in owner.limitStoreRefreshDict or owner.limitStoreRefreshDict[storeId] < nextRefreshTime:
            LOG_DBG('updateLimitedStoreHourly, refresh store:', storeId, "nextRefreshTime:", nextRefreshTime)
            owner.limitStoreRefreshDict[storeId] = nextRefreshTime
            self.doUpdateStoreLimitedItemList(owner, storeId)
        return nextRefreshTime
    
    def updateLimitedStoreHourly(self, owner):
        LOG_DBG('in updateLimitedStoreHourly')
        for storeId, storeDic in self.limitedStores.items():
            self._checkAndUpdateLimitedStoreHourly(owner, storeId)

    def updateStoreDataDaily(self, owner):
        LOG_DBG('in updateStoreDataDaily')
        for storeId, storeDic in self.stores.items():
            for itemId, storeItem in storeDic.items():
                storeItemData = self.getStoreItemData(itemId)
                if storeItemData['limitType'] == gameconst.StoreLimitType.DAILY:
                    storeItem.buyNum = 0
        self.sendStoreList(owner, list(self.stores.keys()))

    def updateStoreDataWeekly(self, owner):
        LOG_DBG('in updateStoreDataWeekly')
        for storeId, storeDic in self.stores.items():
            for itemId, storeItem in storeDic.items():
                storeItemData = self.getStoreItemData(itemId)
                if storeItemData['limitType'] == gameconst.StoreLimitType.WEEKLY:
                    storeItem.buyNum = 0
        self.sendStoreList(owner, list(self.stores.keys()))

    def updateStoreDataMonthly(self, owner):
        LOG_DBG('in updateStoreDataMonthly')
        for storeId, storeDic in self.stores.items():
            for itemId, storeItem in storeDic.items():
                storeItemData = self.getStoreItemData(itemId)
                if storeItemData['limitType'] == gameconst.StoreLimitType.MONTHLY:
                    storeItem.buyNum = 0
        self.sendStoreList(owner, list(self.stores.keys()))

    def sendStoreList(self, owner, storeIds):
        LOG_DBG('in sendStoreList:', storeIds)
        clientStoreList = []
        for storeId in storeIds:
            storeDic = self.getStoreDic(storeId)
            clientStoreDic = {
                'storeId': storeId,
                'itemsList': list(storeDic.values()),
            }
            clientStoreList.append(clientStoreDic)
        LOG_DBG('     in sendStoreList, client:', clientStoreList)
        owner.client.onGetStoreList(clientStoreList)
        return

    def getNextRefreshTime(self, storeId):
        storeCfgData = MSLD.datas.get(storeId)
        groupRefreshTime = storeCfgData.get('groupRefreshTime', 1) * gameconst.ONE_HOUR_COST_SECONDES
        if groupRefreshTime == 0:
            return 0
        return utils.curTS() + groupRefreshTime - utils.curTS() % groupRefreshTime
    
    def sendStoreLimitedItemList(self, owner, storeId):
        LOG_DBG('in sendStoreLimitedItemList:', storeId)
        # 首日登录是不会触发daily event的，所以需要手动初始化
        nextRefreshTime = self._checkAndUpdateLimitedStoreHourly(owner, storeId)
        if nextRefreshTime == 0:
            return
        storeDic = self.getLimitStoreDic(storeId)
        clientStoreDic = {
            'storeId': storeId,
            'itemsList': list(storeDic.values()),
        }
        LOG_DBG('     in sendStoreLimitedItemList, client:', clientStoreDic, nextRefreshTime)
        owner.client.onGetStoreLimitedItemList(clientStoreDic, nextRefreshTime)
        self.printStoreData(storeId)
    
    def doUpdateStoreLimitedItemList(self, owner, storeId):
        LOG_DBG('doUpdateStoreLimitedItemList:', storeId)
        data = MSLD.datas.get(storeId)
        if not data:
            LOG_ERR('doUpdateStoreLimitedItemList, no store cfg:', storeId)
            return
        if not data['groupId']:
            LOG_ERR('doUpdateStoreLimitedItemList, no groupId:', storeId)
            return
        itemNumList = []
        for weightList in data['numberWeight']:
            nums = [i + 1 for i in range(len(weightList))]
            weightedChoice = random.choices(nums, weights=weightList, k=1)[0]
            LOG_DBG('weighted_choice:', weightedChoice, nums, weightList)
            itemNumList.append(weightedChoice)

        self.printStoreData(storeId)
        limitStoreItemDict = self.getLimitStoreDic(storeId)
        limitStoreItemDict.clear()
        idx = 0
        for groupId in data['groupId']:
            itemNum = itemNumList[idx]
            idx += 1
            weightList = []
            for itemId in MCPD.group2ID.get(groupId):
                weightList.append(MCPD.datas.get(itemId)['weight'])

            idxList = [i for i in range(len(weightList))]
            resIds = []
            for _ in range(itemNum):
                resIdx = random.choices(idxList, weights=weightList, k=1)[0]
                resIds.append(MCPD.group2ID.get(groupId)[resIdx])
                weightList[resIdx] = 0
            LOG_DBG('weighted_choice:', resIds, nums, weightList)
            
            for itemId in resIds:
                limitStoreItemDict[itemId] = StoreItem(itemId, buyNum=0)
        self.printStoreData(storeId)

    def printStoreData(self, storeId):
        for itemId, storeItem in self.limitedStores[storeId].items():
            LOG_DBG('printStoreData:', storeId, itemId, storeItem.toStoreItemSavedDict())

    def getLimitStoreDic(self, storeId):
        return self.limitedStores.get(storeId)

    def getStoreDic(self, storeId):
        return self.stores.get(storeId)

    @staticmethod
    def getStoreItemData(itemId):
        return MCPD.datas.get(itemId)

    def canBuyStoreItems(self, owner, storeId, itemId, itemNum):
        LOG_DBG('in canBuyStoreItems:', storeId, itemId)
        storeData = MSLD.datas.get(storeId)
        if not storeData:
            LOG_ERR('   in canBuyItems, no store cfg:', storeId)
            return False

        isTimeLimit = storeData['isTimeLimit']
        if isTimeLimit:
            if not utils.inTimeTuplesRange(storeData['openTime'], storeData['closeTime'], utils.curTS()):
                LOG_ERR('   in canBuyItems, store not open:', storeId, itemId)
                return

        storeItemData = self.getStoreItemData(itemId)
        if not storeItemData:
            LOG_WARN('   in canBuyItems, no item cfg:', storeId, itemId)
            return False

        if itemId not in storeData['goodsList'] and storeItemData['groupId'] == 0:
            LOG_ERR('   in canBuyItems, store no this item:', storeId, itemId)
            return False

        if storeItemData['guildMallLv'] and storeItemData['guildMallLv'] > owner.wuHuaLevel:
            LOG_WARN('   in canBuyItems, guildMallLv limit:', storeId, itemId, owner.wuHuaLevel)
            return False

        if storeItemData['startTime'] and storeItemData['deleteTime']:
            if not utils.inTimeTuplesRange(storeItemData['startTime'], storeItemData['deleteTime'], utils.curTS()):
                LOG_WARN('   in canBuyItems, not on sale:', storeId, itemId)
                # 尚未到上架时间
                return False

        if storeItemData['limitNumber'] > 0 and storeItemData['groupId'] == 0:
            # 限量购买
            storeDic = self.getStoreDic(storeId)
            if itemId not in storeDic:
                storeDic[itemId] = StoreItem(itemId, buyNum=0)
            if itemNum > storeItemData['limitNumber'] - storeDic[itemId].buyNum:
                LOG_WARN('   in canBuyItems, weekBuyNum limit:',
                            storeItemData['limitNumber'], storeDic[itemId].buyNum)
                owner.onMessagePre(MMCD.datas['mall_itemSoldOut_msg']['value'], [])
                return False
        
        # 商店随机物品
        if storeItemData['groupId'] != 0:
            storeDic = self.getLimitStoreDic(storeId)
            if itemId not in storeDic:
                LOG_ERR('   in canBuyItems, no item in limited storeDic:', storeId, itemId, storeDic)
                return False
            if itemNum > storeItemData['limitNumber'] - storeDic[itemId].buyNum:
                LOG_WARN('in canBuyItems, itemSoldOut:', storeId, itemId, itemNum, storeItemData['limitNumber'], storeDic[itemId].buyNum)
                owner.onMessagePre(MMCD.datas['mall_itemSoldOut_msg']['value'], [])
                return False
            
        if owner.checkBagItemLimit(storeItemData['itemId'], itemNum):
            LOG_DBG('in canBuyItems, bag item limit:', storeItemData['itemId'])
            owner.onMessagePre(IDSD.datas['potionMaxLimitMsgID']['value'], [str(owner.drugsQuantityBase)])
            return False

        return True
