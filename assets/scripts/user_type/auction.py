# coding: utf-8
from KBEDebug import *
import KBEngine

import json
import math

import gameengine
import gameconst
import utils
import gamelog

import itemFactory
import dataUtils
import userType

import itemData_itemData as ITEMDATA
import auction_auctionConst as AUT_CONST

G_INDEX_SPLIT_KEY = '%%'


class AuctionItem(userType.UserSTDSoleType):
    __attrs__ = ('auctionType',  # 交易行类型
                 'auctionItemUUID',  # 上架物品唯一UUID
                 'addTime',  # 上架物品时间
                 'itemData',  # 物品信息
                 'price',  # 一口价
                 'number',  # 物品数量
                 'bagType',  # 商家时的背包类型
                 'source',  # 拍卖来源
                 'status',  # 物品交易状态
                 'locked',  # 物品是否被锁
                 'extraInfo',  # 其他信息
                 'tCreate',  #  创建时间
                 'isPublicity' # 是否公式
                 )

    # __slots__ = __attrs__

    def initFromDict(self, dataDic):
        for k, v in dataDic.items():
            if k == 'extraInfo':
                try:
                    setattr(self, k, self.json2extra(v))
                except Exception as e:
                    gameengine.reportCritical("AuctionItem::create item with Dict Error - extraInfo", e)
                    setattr(self, k, {})
            elif k == 'itemData':
                try:
                    setattr(self, k, itemFactory.ItemFactory.createItemWithSavedDict(v))
                except Exception as e:
                    gameengine.reportCritical("AuctionItem::create item with Dict Error - itemData", e)
                    setattr(self, k, None)
            else:
                setattr(self, k, v)
        return self

    def toSavedDict(self):
        m_dicData = {}
        for attr in self.__attrs__:
            if attr == 'extraInfo':
                m_dicData[attr] = self.extra2Json()
            elif attr == 'itemData':
                m_dicData[attr] = getattr(self, attr).toItemSavedDict()
            else:
                m_dicData[attr] = getattr(self, attr)
        return m_dicData

    def extra2Json(self):
        return json.dumps(self.extraInfo)

    def json2extra(self, jsonData):
        return json.loads(jsonData)

    def toClientData(self, recommendPrice=-1):
        m_resultData = {
            "auctionType": self.auctionType,
            "auctionItemUUID": self.auctionItemUUID,
            "addTime": self.addTime,
            "itemId": self.itemId,
            "uniqueId": self.uniqueId,
            "price": self.price,
            "number": self.number,
            "status": self.status,
            'createTime': self.tCreate,
            'isPublicity': self.isPublicity,
        }

        m_extra = {}
        m_extra.update({"attrJson": self.itemData.attr2Dict()})
        m_resultData['extra'] = json.dumps(m_extra)
        return m_resultData

    def _lateReload(self):
        self.itemData.reloadScript()

    def __init__(self, auctionType=gameconst.AuctionType.UNKNOWN, auctionItemUUID=0, addTime=0,
                 itemData=None, price=0, number=0, bagType=gameconst.BagType.BAG_TYPE_NORMAL,
                 source=gameconst.AuctionSource.UNKNOWN,
                 status=gameconst.AuctionItemStatus.INIT, locked=False, extraInfo=None,
                 tCreate=utils.getNow(), isPublicity = 0):
        self.auctionType = auctionType
        self.auctionItemUUID = auctionItemUUID
        self.addTime = addTime
        self.itemData = itemData
        self.price = price
        self.number = number
        self.bagType = bagType
        self.source = source
        self.status = status
        self.locked = locked
        extraInfo = {} if extraInfo is None else extraInfo
        self.extraInfo = extraInfo
        # ----------------------------------------
        self.tCreate = tCreate
        self.isPublicity = isPublicity

    def canBeSearched(self):
        # if not self.isNotifyExpired():
        #     return False
        return self.status == gameconst.AuctionItemStatus.SELLING

    @property
    def totalPrice(self):
        return self.price * self.number

    @property
    def itemId(self):
        return self.itemData.itemId

    @property
    def uniqueId(self):
        return self.itemData.uniqueId

    @property
    def quality(self):
        return self.itemData.quality

    @property
    def expireTime(self):
        return self.itemData.expireTime

    @property
    def fromPlayerGBID(self):
        return self.extraInfo.get('fromPlayerGBID', None)

    @fromPlayerGBID.setter
    def fromPlayerGBID(self, newVal):
        self.extraInfo['fromPlayerGBID'] = newVal

    @property
    def playerTlogProps(self):
        return self.extraInfo.get('playerTlogProps', {})

    @playerTlogProps.setter
    def playerTlogProps(self, newVal: dict):
        self.extraInfo.pop('playerTlogProps', None)
        self.extraInfo.setdefault('playerTlogProps', {}).update(newVal)

    def setStatusSelling(self):
        self.status = gameconst.AuctionItemStatus.SELLING

    def setStatusNotify(self):
        self.status = gameconst.AuctionItemStatus.NOTIFY

    def setStatusExpired(self):
        self.status = gameconst.AuctionItemStatus.EXPIRED

    @property
    def notifyExpiredSecond(self):
        return 24 * 3600

    @property
    def notifyExpiredTime(self):
        return (self.notifyExpiredSecond or 0) + self.tCreate

    def isNotifyExpired(self, now=None):
        if self.status != gameconst.AuctionItemStatus.NOTIFY:
            return True
        now = now if now is not None else utils.getNow()
        return now > self.notifyExpiredTime

    @property
    def itemExpiredSecond(self):
        return int(AUT_CONST.datas["auctionAutoUnlist"]['value']) * 3600

    @property
    def itemExpiredTime(self):
        if self.expireTime > 0:
            return min(self.expireTime, (self.itemExpiredSecond or 0) + self.addTime)
        return (self.itemExpiredSecond or 0) + self.addTime

    def isItemExpired(self, now=None):
        if self.status == gameconst.AuctionItemStatus.EXPIRED:
            return True
        now = now if now is not None else utils.getNow()
        return now > self.itemExpiredTime

    def buildIndexKeyFromAttrsName(self, *indexKeys):
        _m_datas = []
        for i in indexKeys:
            _m_value = getattr(self, i)
            if _m_value is None:
                # WARNING_MSG("buildIndexKeyFromAttrsName:: value is None --> ", i, _m_value)
                return None
            _m_datas.append(str(_m_value))
        return G_INDEX_SPLIT_KEY.join(_m_datas)

    def lock(self, timeout=0, now=None):
        now = now if now is not None else utils.getNow()
        if self.isLocked(now):
            return False
        self.locked = timeout + now
        return True

    def unlock(self):
        self.locked = 0

    def isLocked(self, now=None):
        now = now if now is not None else utils.getNow()
        return self.locked > now

    def itemCanMerge(self, withInAuctionItem):
        return self.itemData.canMerge(withInAuctionItem.itemData)

    def iterToSaledItemDataList(self, number=None):
        m_bindType = self.getSaleBindType()

        def _fixData(x):
            x.bindType = m_bindType
            x.clearRoleBindData()
            return x

        return (_fixData(i) for i in self.iterToItemDataList(number=number, forceResetUniqueId=True))

    def iterToItemDataList(self, number=None, forceResetUniqueId=False):
        number = number if number is not None else self.number

        if number == 1:
            # number=1的时候可能是不可堆叠物品, 这个时候更改UniqueID可能导致重新上架逻辑失效
            _data = itemFactory.ItemFactory.forkItemObject(self.itemData, itemNum=number)
            if forceResetUniqueId:
                _data.uniqueId = KBEngine.genUUID64()
            yield _data
            return

        m_maxStackSize = self.itemData.maxStackSize(self.itemId)
        m_singleNum = number % m_maxStackSize
        m_stacks = number // m_maxStackSize
        for i in range(m_stacks):
            _c_data = itemFactory.ItemFactory.forkItemObject(self.itemData, itemNum=m_maxStackSize)
            if _c_data.uniqueId:
                # reset uniqueId
                _c_data.uniqueId = KBEngine.genUUID64()
            yield _c_data
        if m_singleNum > 0:
            _s_data = itemFactory.ItemFactory.forkItemObject(self.itemData, itemNum=m_singleNum)
            if _s_data.uniqueId:
                # reset uniqueId
                _s_data.uniqueId = KBEngine.genUUID64()
            yield _s_data

    def getSaleBindType(self):
        return self.itemData.bindType


class Auction(userType.UserSTDSoleType):

    def initFromDict(self, dataDic):
        self.auctionType = dataDic["auctionType"]
        self.auctionIndexInfo = set(dataDic["auctionIndexInfo"])
        self.auctionItemData = {i.auctionItemUUID: i for i in dataDic['auctionItemData'] if i.itemData}
        # checksum
        if len(dataDic['auctionItemData']) != len(self.auctionItemData):
            WARNING_MSG("Auction::itemdata dict checksum failed")
        self.defaultIndexSortKey = dataDic["defaultIndexSortKey"]
        self.defaultIndexSortReversed = dataDic["defaultIndexSortReversed"]
        self.refreshAuctionIndexData()
        self.refreshAuctionDefaultSortData()
        return self

    def toSavedDict(self):
        m_result = {
            'auctionType': self.auctionType,
            'auctionIndexInfo': list(self.auctionIndexInfo),
            'auctionItemData': list(self.auctionItemData.values()),
            'defaultIndexSortKey': self.defaultIndexSortKey,
            'defaultIndexSortReversed': self.defaultIndexSortReversed,
        }
        return m_result

    def __init__(self, auctionType=gameconst.AuctionType.UNKNOWN,
                 auctionIndexInfo=None, auctionItemData=None,
                 defaultIndexSortKey='', defaultIndexSortReversed=False):
        # 交易行Type, 区分铜贝/金丝玉贝交易行
        self.auctionType = auctionType
        # 交易行索引信息
        auctionIndexInfo = set() if auctionIndexInfo is None else auctionIndexInfo
        self.auctionIndexInfo = auctionIndexInfo  # type: set[indexKey]
        # 交易行数据
        auctionItemData = {} if auctionItemData is None else auctionItemData
        self.auctionItemData = auctionItemData  # type: dict[ductionItemUUID, auctionItem]
        # 默认索引数据key
        self.defaultIndexSortKey = defaultIndexSortKey
        self.defaultIndexSortReversed = defaultIndexSortReversed
        # private: 交易行索引数据
        self._auctionItemIndex = {}  # type: dict[indexKey, dict[key, list[diUUID]]]
        self._auctionItemIndexDirty = {}  # type: dict[indexKey, dict[key, dirtyNum]]
        # private: 默认交易行UUID排序
        self._defaultAuctionSortedData = []
        self.refreshAuctionIndexData()
        self.refreshAuctionDefaultSortData()

    def _lateReload(self):
        for k, v in self.auctionItemData.items():
            v.reloadScript()

    def isEmpty(self):
        return not self.auctionItemData

    @staticmethod
    def joinAuctionIndex(indexKeyList, nosort=False):
        indexKeyList = indexKeyList if nosort else sorted(indexKeyList)
        return G_INDEX_SPLIT_KEY.join((str(i) for i in indexKeyList))

    @staticmethod
    def splitAuctionIndex(indexKey):
        return indexKey.split(G_INDEX_SPLIT_KEY)

    @staticmethod
    def isAuctionIndexKeyValidated(keyList):
        for key in keyList:
            if key not in AuctionItem.__attrs__ and not isinstance(getattr(AuctionItem, key, None), property):
                return False
        return True

    def addAuctionIndex(self, indexKeyList, syncNow=True):
        m_indexKey = self.joinAuctionIndex(indexKeyList)
        if m_indexKey in self.auctionIndexInfo:
            return None, gameconst.AuctionErrno.AUCTION_INDEX_ALREADY_ADDED.initkvbody()()
        if not self.isAuctionIndexKeyValidated(indexKeyList):
            return None, gameconst.AuctionErrno.AUCTION_ITEM_ATTR_NOT_DEFINED.initkvbody()()
        self.auctionIndexInfo.add(m_indexKey)
        if syncNow:
            self.refreshAuctionIndexData()
        return m_indexKey, gameconst.AuctionErrno.AUCTION_OK

    def removeAuctionIndex(self, indexKey, syncNow=True):
        if indexKey not in self.auctionIndexInfo:
            return False, gameconst.AuctionErrno.AUCTION_INDEX_NOT_FOUND.initkvbody()()
        self.auctionIndexInfo.remove(indexKey)
        if syncNow:
            self.refreshAuctionIndexData()
        return True, gameconst.AuctionErrno.AUCTION_OK

    def hasAuctionIndex(self, indexKey):
        return indexKey in self.auctionIndexInfo

    def refreshAuctionDefaultSortData(self):
        self._defaultAuctionSortedData = self.auctionItemData

    def refreshAuctionIndexData(self):
        self._removedUnindexedAuctionIndexData()
        self._addNewAuctionIndexData()

    def _removedUnindexedAuctionIndexData(self):
        _m_needRemoveIndexData = [k for k, v in self._auctionItemIndex.items()
                                  if k not in self.auctionIndexInfo]
        for _j in _m_needRemoveIndexData:
            self._auctionItemIndex.pop(_j)

    def _addNewAuctionIndexData(self):
        _m_indexKeyList = [i for i in self.auctionIndexInfo if i not in self._auctionItemIndex]
        for m_auctionItemData in self.auctionItemData.values():
            for m_indexKey in _m_indexKeyList:
                self._syncAddItemInSpecialAuctionIndex(m_auctionItemData, m_indexKey,
                                                       sortBy='',
                                                       reversed=self.defaultIndexSortReversed)

        sortBy = self.defaultIndexSortKey
        if self.isAuctionIndexKeyValidated((sortBy,)):
            for m_indexKey, _auctionItemIndexDic in self._auctionItemIndex.items():
                for k, _m_auctionItemIndexItemData in _auctionItemIndexDic.items():
                    _m_auctionItemIndexItemData.sort(
                        key=lambda _id: getattr(self.auctionItemData[_id], sortBy),
                        reverse=self.defaultIndexSortReversed)

    def _syncAddItemInAuctionIndex(self, auctionItem: AuctionItem, sortBy='', reversed=False):
        for m_indexKey in self.auctionIndexInfo:
            self._syncAddItemInSpecialAuctionIndex(auctionItem, m_indexKey, sortBy, reversed)

    def _syncAddItemInSpecialAuctionIndex(self, auctionItem, indexKey, sortBy='', reversed=False):
        m_indexKeyList = self.splitAuctionIndex(indexKey)
        m_indexItemKey = auctionItem.buildIndexKeyFromAttrsName(*m_indexKeyList)
        if m_indexItemKey is None:
            # WARNING_MSG("Auction::_syncAddItemInAuctionIndex:: indexKey skipped",
            #             auctionItem.auctionItemUUID, m_indexKeyList)
            return

        self._auctionItemIndex.setdefault(indexKey, {})
        _m_auctionItemIndexDic = self._auctionItemIndex[indexKey]
        _m_auctionItemIndexDic.setdefault(m_indexItemKey, [])
        _m_auctionItemIndexItemData = _m_auctionItemIndexDic[m_indexItemKey]
        _m_auctionItemIndexItemData.insert(0, auctionItem.auctionItemUUID)

        self._auctionItemIndexDirty.setdefault(indexKey, {})
        _m_auctionItemIndexDirtyDic = self._auctionItemIndexDirty[indexKey]
        _m_auctionItemIndexDirtyDic[m_indexItemKey] = _m_auctionItemIndexDirtyDic.get(m_indexItemKey, 0) + 1
        self._sortAuctionItemIndex(indexKey, m_indexItemKey, 100)
        # if sortBy and self.isAuctionIndexKeyValidated((sortBy,)):
        #     _m_auctionItemIndexItemData.sort(
        #         key=lambda _id: getattr(self.auctionItemData[_id], sortBy),
        #         reverse=reversed)

    def putItemInAuction(self, auctionItem: AuctionItem):
        if auctionItem.auctionType != self.auctionType:
            return False, gameconst.AuctionErrno.AUCTION_TYPE_ERR.initkvbody()()
        if auctionItem.auctionItemUUID in self.auctionItemData:
            return False, gameconst.AuctionErrno.AUCTION_ALREADY_IN_AUCTION.initkvbody()()
        self.auctionItemData[auctionItem.auctionItemUUID] = auctionItem
        self._syncAddItemInAuctionIndex(auctionItem, sortBy=self.defaultIndexSortKey,
                                        reversed=self.defaultIndexSortReversed)
        self.refreshAuctionDefaultSortData()
        return True, gameconst.AuctionErrno.AUCTION_OK

    def _syncRemoveItemFromAuctionIndex(self, auctionItem, sortBy='', reversed=False):
        for m_indexKey, _m_auctionItemIndexDic in self._auctionItemIndex.items():
            m_indexKeyList = self.splitAuctionIndex(m_indexKey)
            m_indexItemKey = auctionItem.buildIndexKeyFromAttrsName(*m_indexKeyList)
            if m_indexItemKey is None:
                # WARNING_MSG("Auction::_syncRemoveItemFromAuctionIndex:: indexKey skipped",
                #             auctionItem.auctionItemUUID, m_indexKeyList)
                continue

            _m_auctionItemIndexItemData = _m_auctionItemIndexDic[m_indexItemKey]
            if auctionItem.auctionItemUUID in _m_auctionItemIndexItemData:
                _m_auctionItemIndexItemData.remove(auctionItem.auctionItemUUID)
                self._auctionItemIndexDirty.setdefault(m_indexKey, {})
                _m_auctionItemIndexDirtyDic = self._auctionItemIndexDirty[m_indexKey]
                _m_auctionItemIndexDirtyDic[m_indexItemKey] = _m_auctionItemIndexDirtyDic.get(m_indexItemKey, 0) + 1
                self._sortAuctionItemIndex(m_indexKey, m_indexItemKey, 100)

            # if sortBy and self.isAuctionIndexKeyValidated((sortBy,)):
            #     _m_auctionItemIndexItemData.sort(
            #         key=lambda _id: getattr(self.auctionItemData[_id], sortBy),
            #         reverse=reversed)

    def popItemFromAuction(self, auctionItemUUID):
        if auctionItemUUID not in self.auctionItemData:
            return None, gameconst.AuctionErrno.AUCTION_NOT_IN_AUCTION.initkvbody()()
        m_auctionItem = self.auctionItemData.pop(auctionItemUUID)
        self._syncRemoveItemFromAuctionIndex(m_auctionItem, sortBy=self.defaultIndexSortKey,
                                             reversed=self.defaultIndexSortReversed)
        self.refreshAuctionDefaultSortData()
        return m_auctionItem, gameconst.AuctionErrno.AUCTION_OK

    def getItemFromAuctionByUUID(self, auctionItemUUID, default=None):
        return self.auctionItemData.get(auctionItemUUID, default)

    def _validateSearchOptions(self, searchOptions):
        m_rmKeys = []
        for k, v in searchOptions.items():
            if v is None:
                WARNING_MSG("_validateSearchOptions:: None value in search kv", k, v)
                m_rmKeys.append(k)
        for _i in m_rmKeys:
            searchOptions.pop(_i)
        return searchOptions

    def iterSearchItemFromAuction(self, searchOptions, filterFn=None):
        _m_errno = gameconst.AuctionErrno
        self._validateSearchOptions(searchOptions)
        m_searchAttrs = list(searchOptions)
        if not self.isAuctionIndexKeyValidated(m_searchAttrs):
            return [], _m_errno.AUCTION_ITEM_ATTR_NOT_DEFINED.initkvbody()()
        _hasMultipleOptVal = any(utils.canIterable(i) for i in searchOptions.values())

        m_indexKey = self.joinAuctionIndex(m_searchAttrs)
        m_searchAttrs = self.splitAuctionIndex(m_indexKey)

        if not _hasMultipleOptVal and self.hasAuctionIndex(m_indexKey):
            m_indexItemKey = self.joinAuctionIndex(
                map(lambda i: searchOptions[i], m_searchAttrs), nosort=True)
            return self._iterGetItemsFromAuctionWithIndex(m_indexKey, m_indexItemKey, filterFn), _m_errno.AUCTION_OK

        else:
            return self._iterGetItemsFromAuctionNoIndex(searchOptions, filterFn), _m_errno.AUCTION_OK

    def _iterGetItemsFromAuctionWithIndex(self, indexKey, indexItemKey, filterFn):
        DEBUG_MSG("_iterGetItemsFromAuctionWithIndex::", indexKey, indexItemKey)
        self._sortAuctionItemIndex(indexKey, indexItemKey)

        if not filterFn:
            filterFn = self._getAuctionItemsCommonFilter

        itemIndexList = self._auctionItemIndex.get(indexKey, {}).get(indexItemKey, [])
        if len(itemIndexList) > 0:
            itemIndexList = itemIndexList[0:min(len(itemIndexList), 2000)]
        return filter(filterFn, map(lambda o: self.auctionItemData.get(o, None), itemIndexList))

    def _sortAuctionItemIndex(self, indexKey, indexItemKey, dirtyNumLimit=0):
        self._auctionItemIndexDirty.setdefault(indexKey, {})
        auctionItemIndexDirtyDic = self._auctionItemIndexDirty[indexKey]
        dirtyNum = auctionItemIndexDirtyDic.get(indexItemKey, 0)
        if dirtyNum > dirtyNumLimit:
            auctionItemIndexDirtyDic[indexItemKey] = 0
            auctionItemIndexItemData = self._auctionItemIndex.get(indexKey, {}).get(indexItemKey, [])
            sortLen = min(len(auctionItemIndexItemData), 2000)
            if sortLen:
                headData = auctionItemIndexItemData[0:sortLen]
                headData and headData.sort(
                    key=lambda _id: getattr(self.auctionItemData[_id], self.defaultIndexSortKey),
                    reverse=self.defaultIndexSortReversed)
                if len(auctionItemIndexItemData) > 2000:
                    remainData = auctionItemIndexItemData[2000:len(auctionItemIndexItemData)]
                    headData.extend(remainData)
                self._auctionItemIndex.get(indexKey, {})[indexItemKey] = headData

    def _iterGetItemsFromAuctionNoIndex(self, searchOptions, filterFn=None):
        # DEBUG_MSG("_iterGetItemsFromAuctionNoIndex::", searchOptions)
        for m_auctionItemData in self._defaultAuctionSortedData:
            _skipped = False
            for k, v in searchOptions.items():
                m_attrVal = getattr(m_auctionItemData, k)
                if utils.canIterable(v):
                    if m_attrVal in v:
                        continue
                    else:
                        _skipped = True
                        break
                else:
                    if m_attrVal == v:
                        continue
                    else:
                        _skipped = True
                        break

            if filterFn and not filterFn(m_auctionItemData):
                continue

            if not _skipped:
                yield m_auctionItemData

    def _getAuctionItemsNumberCommonFilter(self, auctionItemUUID):
        _cl_auctionItem = self.getItemFromAuctionByUUID(auctionItemUUID)
        return self._getAuctionItemsNumberByAuctionItemCommonFilter(_cl_auctionItem)

    def _getAuctionItemsCommonFilter(self, auctionItem):
        if not auctionItem:
            return False
        return True

    def _getAuctionItemsNumberByAuctionItemCommonFilter(self, auctionItem):
        if not auctionItem:
            return 0
        return auctionItem.number


class AuctionPlayerCache(userType.UserSTDSoleType):

    def _lateReload(self):
        for d in self.followedItemData:
            d.reloadScript()

    def initFromDict(self, dataDic):
        self.auctionType = dataDic['auctionType']
        self.unlockedGrids = dataDic['unlockedGrids']

        return self

    def toSavedDict(self):
        m_data = {
            'auctionType': self.auctionType,
            'unlockedGrids': self.unlockedGrids,
        }

        return m_data

    @classmethod
    def _checkIgnores_(cls):
        return '_itemDataCache', '_lastSyncTime', '_cacheInited', '_locked'

    def __init__(self, auctionType=gameconst.AuctionType.UNKNOWN, unlockedGrids=0):
        # presistent
        self.auctionType = auctionType
        self.unlockedGrids = unlockedGrids
        self.followedItemData = []
        self.followedAuctionItemUUIDData = []
        # cache from AuctionStub
        self._itemDataCache = set()
        # private data
        self._lastSyncTime = 0
        self._cacheInited = False
        self._locked = 0

    @property
    def initGrids(self):
        if self.auctionType == gameconst.AuctionType.COIN_AUCTION:
            return int(AUT_CONST.datas["auctionInitShelfNum"]["value"])
        else:
            return 0

    @property
    def totalGrids(self):
        return self.initGrids + self.unlockedGrids

    @property
    def totalFollowedNumber(self):
        return len(self.followedItemData) + len(self.followedAuctionItemUUIDData)

    def updateSyncTime(self, t):
        self._lastSyncTime = t

    def isSyncTimeOutdate(self, t):
        return self._lastSyncTime > t

    def isLocked(self, now=None):
        return self._locked > (now or utils.getNow())

    def lock(self, timeout=3, now=None):
        now = now or utils.getNow()
        if self.isLocked(now):
            WARNING_MSG("AuctionPlayerCache::lock::already locked", self.auctionType)
        self._locked = now + timeout

    def unlock(self):
        self._locked = 0

    def isCacheInited(self):
        return bool(self._cacheInited)

    def isSaleGridFull(self):
        if not self.isCacheInited():
            return False
        return len(self._itemDataCache) >= self.totalGrids

    def updatePlayerCache(self, itemIdList=None, cacheSyncT=0):
        if self.isSyncTimeOutdate(cacheSyncT):
            WARNING_MSG("updatePlayerCache:: sync time outdate {}(from) < {}(cached)".format(
                cacheSyncT, self._lastSyncTime))
            return False

        self._itemDataCache.clear()
        if itemIdList is not None:
            self._itemDataCache.update(itemIdList)
        self._cacheInited = True

        self.updateSyncTime(cacheSyncT)
        return True

    def getNextUnlockGridNum(self):
        return self.unlockedGrids + 1

    def unlockGrid(self):
        self.unlockedGrids += 1


class AuctionItemRecord(userType.UserSTDSoleType):

    def initFromDict(self, dataDic):
        self.recordUUID = dataDic['recordUUID']
        self.itemId = dataDic['itemId']
        self.totalPrice = dataDic['totalPrice']
        self.number = dataDic['number']
        self.extraJoinedKV = dataDic['extraJoinedKV']
        return self

    def toSavedDict(self):
        return {
            'recordUUID': self.recordUUID,
            'itemId': self.itemId,
            'totalPrice': self.totalPrice,
            'number': self.number,
            'extraJoinedKV': self.extraJoinedKV,
        }

    def __init__(self, recordUUID=0, itemId=0, totalPrice=0, number=0, extraJoinedKV=None):
        self.recordUUID = recordUUID
        self.itemId = itemId
        self.totalPrice = totalPrice
        self.number = number
        self.extraJoinedKV = extraJoinedKV or {}

    @property
    def avgPrice(self):
        return math.ceil(self.totalPrice / self.number) if self.number != 0 else 0

    def addRecord(self, price, number):
        self.totalPrice += price * number
        self.number += number

    def reset(self):
        self.totalPrice = 0
        self.number = 0


class AuctionItemRecommendRecord(userType.UserSTDSoleType):

    def initFromDict(self, dataDic):
        self.recordUUID = dataDic['recordUUID']
        self.itemId = dataDic['itemId']
        self.price = dataDic['price']
        self.extraJoinedKV = dataDic['extraJoinedKV']
        return self

    def toSavedDict(self):
        return {
            'recordUUID': self.recordUUID,
            'itemId': self.itemId,
            'price': self.price,
            'extraJoinedKV': self.extraJoinedKV,
        }

    def __init__(self, recordUUID=0, itemId=0, price=0, extraJoinedKV=None):
        self.recordUUID = recordUUID
        self.itemId = itemId
        self.price = price
        self.extraJoinedKV = extraJoinedKV or {}

