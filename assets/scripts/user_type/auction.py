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


class AuctionItem(userType.UserSTSoleType):
    __attrs__ = (
        'auctionItemUUID',  # 上架物品唯一UUID
        'auctionType',  # 交易行类型
        'addTime',  # 上架物品时间
        'price',  # 一口价
        'itemData',  # 物品信息
        'number',  # 物品数量
        'bagType',  # 商家时的背包类型
        'status',  # 物品交易状态
        'source',  # 拍卖来源
        'locked',  # 物品是否被锁
        'extraInfo',  # 其他信息
        'addPublicityTime', # 公示时间
        'tCreate',  #  创建时间
    )

    def initFromDict(self, dataDic):
        for _k, v in dataDic.items():
            if _k == 'extraInfo':
                try:
                    setattr(self, _k, self.json2extra(v))
                except Exception as e:
                    gameengine.panicStack("AuctionItem::create item with Dict Error - extraInfo", e)
                    setattr(self, _k, {})
            elif _k == 'itemData':
                try:
                    setattr(self, _k, itemFactory.ItemFactory.createItemWithSavedDict(v))
                except Exception as e:
                    gameengine.panicStack("AuctionItem::create item with Dict Error - itemData", e)
                    setattr(self, _k, None)
            else:
                setattr(self, _k, v)
        return self

    def toSavedDict(self):
        mDictData = {}
        for attr in self.__attrs__:
            if attr == 'extraInfo':
                mDictData[attr] = self.extra2Json()
            elif attr == 'itemData':
                mDictData[attr] = getattr(self, attr).toItemSavedDict()
            else:
                mDictData[attr] = getattr(self, attr)
        return mDictData

    def json2extra(self, jsonData):
        return json.loads(jsonData)

    def extra2Json(self):
        return json.dumps(self.extraInfo)

    def toClientData(self, recommendPrice=-1):
        return {
            'auctionItemUUID': self.auctionItemUUID,
            'addTime': self.addTime,
            'price': self.price,
            'number': self.number,
            'status': self.status,
            'itemData': self.itemData.toItemSavedDict(),
            'addPublicityTime': self.addPublicityTime,
        }

    def _lateReload(self):
        self.itemData.reloadScript()

    def __init__(self, auctionType=gameconst.AuctionTypeEnum.UNKNOWN, 
                 auctionItemUUID=0, addTime=0,
                 itemData=None, price=0, number=0, 
                 bagType=gameconst.BagTypeEnum.BAG_TYPE_NORMAL,
                 source=gameconst.AuctionSource.UNKNOWN,
                 status=gameconst.AuctionItemStatus.ENUM_INIT, 
                 locked=False, extraInfo=None,
                 tCreate=utils.curTS(), addPublicityTime = 0):
        self.auctionItemUUID = auctionItemUUID
        self.auctionType = auctionType
        self.addTime = addTime
        self.itemData = itemData
        self.price = price
        self.bagType = bagType
        self.number = number
        self.source = source
        self.locked = locked
        self.status = status
        extraInfo = {} if extraInfo is None else extraInfo
        self.extraInfo = extraInfo
        # ----------------------------------------
        self.tCreate = tCreate
        self.addPublicityTime = addPublicityTime

    def canBeSearched(self):
        # if not self.isNotifyExpired():
        #     return False
        return self.status == gameconst.AuctionItemStatus.ENUM_SELLING

    @property
    def itemId(self):
        return self.itemData.itemId

    @property
    def totalPrice(self):
        return self.price * self.number

    @property
    def uniqueId(self):
        return self.itemData.uniqueId

    @property
    def expireTime(self):
        return self.itemData.expireTime

    @property
    def fromPlayerGBID(self):
        return self.extraInfo.get('fromPlayerGBID', None)

    @property
    def quality(self):
        return self.itemData.quality

    @fromPlayerGBID.setter
    def fromPlayerGBID(self, newVal):
        self.extraInfo['fromPlayerGBID'] = newVal

    def setStatusNotify(self):
        self.status = gameconst.AuctionItemStatus.ENUM_NOTIFY

    @property
    def playerTlogProps(self):
        return self.extraInfo.get('playerTlogProps', {})

    def setStatusSelling(self):
        self.status = gameconst.AuctionItemStatus.ENUM_SELLING

    @playerTlogProps.setter
    def playerTlogProps(self, newVal: dict):
        self.extraInfo.pop('playerTlogProps', None)
        self.extraInfo\
            .setdefault('playerTlogProps', {})\
            .update(newVal)

    def setStatusExpired(self):
        self.status = gameconst.AuctionItemStatus.ENUM_EXPIRED

    @property
    def notifyExpiredTime(self):
        return (self.notifyExpiredSecond or 0) + self.tCreate

    @property
    def notifyExpiredSecond(self):
        return 24 * 3600

    def isNotifyExpired(self, now=None):
        if self.status != gameconst.AuctionItemStatus.ENUM_NOTIFY:
            return True
        now = now if now is not None else utils.curTS()
        return now > self.notifyExpiredTime

    @property
    def itemExpiredSecond(self):
        return int(AUT_CONST.datas["auctionAutoUnlist"]['value']) * 3600

    def isItemExpired(self, now=None):
        if self.status == gameconst.AuctionItemStatus.ENUM_EXPIRED:
            return True
        now = now if now is not None else utils.curTS()
        return now > self.itemExpiredTime

    @property
    def itemExpiredTime(self):
        if self.expireTime > 0:
            return min(self.expireTime, (self.itemExpiredSecond or 0) + self.addTime)
        return (self.itemExpiredSecond or 0) + self.addTime

    def buildIndexKeyFromAttrsName(self, *indexKeys):
        _mDatas = []
        for i in indexKeys:
            _mValue = getattr(self, i)
            if _mValue is None:
                return None
            _mDatas.append(str(_mValue))
        return G_INDEX_SPLIT_KEY.join(_mDatas)

    def lock(self, timeout=0, now=None):
        if now is None:
            now = utils.curTS()

        if self.isLocked(now):
            return False

        self.locked = timeout + now
        return True

    def isLocked(self, now=None):
        now = now if now is not None else utils.curTS()
        return self.locked > now

    def unlock(self):
        self.locked = 0

    def itemCanMerge(self, withInAuctionItem):
        return self.itemData.canMerge(withInAuctionItem.itemData)

    def iterToSaledItemDataList(self, number=None):
        mBindType = self.getSaleBindType()

        def _fixData(x):
            x.bindType = mBindType
            x.clearRoleBindData()
            return x

        return (_fixData(_i) for _i in self.iterToItemDataList(number=number, forceResetUniqueId=True))

    def iterToItemDataList(self, number=None, forceResetUniqueId=False):
        if number is None:
            number = self.number

        if number == 1:
            # number=1的时候可能是不可堆叠物品, 这个时候更改UniqueID可能导致重新上架逻辑失效
            _itemObj = itemFactory.ItemFactory.forkItemObject(self.itemData, itemNum=number)
            if forceResetUniqueId:
                _itemObj.uniqueId = KBEngine.genUUID64()
            yield _itemObj
            return

        mMaxStackSize = self.itemData.maxStackSize(self.itemId)
        mSingleNum = number % mMaxStackSize
        mStacks = number // mMaxStackSize
        for i in range(mStacks):
            _cData = itemFactory.ItemFactory.forkItemObject(self.itemData, itemNum=mMaxStackSize)
            if _cData.uniqueId:
                # reset uniqueId
                _cData.uniqueId = KBEngine.genUUID64()
            yield _cData
        if mSingleNum > 0:
            _sData = itemFactory.ItemFactory.forkItemObject(self.itemData, itemNum=mSingleNum)
            if _sData.uniqueId:
                # reset uniqueId
                _sData.uniqueId = KBEngine.genUUID64()
            yield _sData

    def getSaleBindType(self):
        return self.itemData.bindType


class Auction(userType.UserSTSoleType):

    def initFromDict(self, dataDic):
        self.auctionType = dataDic["auctionType"]
        self.auctionIndexInfo = set(dataDic["auctionIndexInfo"])
        self.auctionItemData = {_i.auctionItemUUID: _i for _i in dataDic['auctionItemData'] if _i.itemData}
        # checksum
        if len(dataDic['auctionItemData']) != len(self.auctionItemData):
            LOG_WARN("Auction::itemdata dict checksum failed")
        self.defaultIndexSortReversed = dataDic["defaultIndexSortReversed"]
        self.defaultIndexSortKey = dataDic["defaultIndexSortKey"]
        self.refreshAuctionIndexData()
        self.refreshAuctionDefaultSortData()
        return self

    def toSavedDict(self):
        m_result = {
            'auctionIndexInfo': list(self.auctionIndexInfo),
            'auctionType': self.auctionType,
            'auctionItemData': list(self.auctionItemData.values()),
            'defaultIndexSortReversed': self.defaultIndexSortReversed,
            'defaultIndexSortKey': self.defaultIndexSortKey,
        }
        return m_result

    def __init__(self, auctionType=gameconst.AuctionTypeEnum.UNKNOWN,
                 auctionIndexInfo=None, auctionItemData=None,
                 defaultIndexSortKey='', defaultIndexSortReversed=False):
        # 交易行索引信息
        auctionIndexInfo = set() if auctionIndexInfo is None else auctionIndexInfo
        # 交易行Type, 区分铜贝/金丝玉贝交易行
        self.auctionType = auctionType
        self.auctionIndexInfo = auctionIndexInfo  # type: set[indexKey]
        # 交易行数据
        auctionItemData = {} if auctionItemData is None else auctionItemData
        self.auctionItemData = auctionItemData  # type: dict[ductionItemUUID, auctionItem]
        self.defaultIndexSortReversed = defaultIndexSortReversed
        # 默认索引数据key
        self.defaultIndexSortKey = defaultIndexSortKey
        # private: 交易行索引数据
        self._auctionItemIndex = {}  # type: dict[indexKey, dict[key, list[diUUID]]]
        self._auctionItemIndexDirty = {}  # type: dict[indexKey, dict[key, dirtyNum]]
        # private: 默认交易行UUID排序
        self._defaultAuctionSortedData = []
        self.refreshAuctionIndexData()
        self.refreshAuctionDefaultSortData()

    def _lateReload(self):
        for _, v in self.auctionItemData.items():
            v.reloadScript()

    def isEmpty(self):
        return not self.auctionItemData

    @staticmethod
    def joinAuctionIndex(indexKeyList, nosort=False):
        if not nosort:
            indexKeyList = sorted(indexKeyList)

        return G_INDEX_SPLIT_KEY.join((str(_i) for _i in indexKeyList))

    @staticmethod
    def isAuctionIndexKeyValidated(keyList):
        for _key in keyList:
            if _key not in AuctionItem.__attrs__ and not isinstance(getattr(AuctionItem, _key, None), property):
                return False
        return True

    @staticmethod
    def splitAuctionIndex(indexKey):
        return indexKey.split(G_INDEX_SPLIT_KEY)

    def addAuctionIndex(self, indexKeyList, syncNow=True):
        mIndexKey = self.joinAuctionIndex(indexKeyList)
        if mIndexKey in self.auctionIndexInfo:
            return None, gameconst.AuctionErrno.ERR_AUCTION_INDEX_ALREADY_ADDED.initkvbody()()
        if not self.isAuctionIndexKeyValidated(indexKeyList):
            return None, gameconst.AuctionErrno.ERR_AUCTION_ITEM_ATTR_NOT_DEFINED.initkvbody()()
        self.auctionIndexInfo.add(mIndexKey)
        if syncNow:
            self.refreshAuctionIndexData()
        return mIndexKey, gameconst.AuctionErrno.ERR_AUCTION_OK

    def removeAuctionIndex(self, indexKey, syncNow=True):
        if indexKey not in self.auctionIndexInfo:
            return False, gameconst.AuctionErrno.ERR_AUCTION_INDEX_NOT_FOUND.initkvbody()()
        self.auctionIndexInfo.remove(indexKey)
        if syncNow:
            self.refreshAuctionIndexData()
        return True, gameconst.AuctionErrno.ERR_AUCTION_OK

    def hasAuctionIndex(self, indexKey):
        return indexKey in self.auctionIndexInfo

    def refreshAuctionDefaultSortData(self):
        self._defaultAuctionSortedData = self.auctionItemData

    def _removedUnindexedAuctionIndexData(self):
        _mNeedRemoveIndexData = [k for k, v in self._auctionItemIndex.items()
                                  if k not in self.auctionIndexInfo]
        for _j in _mNeedRemoveIndexData:
            self._auctionItemIndex.pop(_j)

    def refreshAuctionIndexData(self):
        self._removedUnindexedAuctionIndexData()
        self._addNewAuctionIndexData()

    def _addNewAuctionIndexData(self):
        _mIndexKeyList = [i for i in self.auctionIndexInfo if i not in self._auctionItemIndex]
        for m_auctionItemData in self.auctionItemData.values():
            for mIndexKey in _mIndexKeyList:
                self._syncAddItemInSpecialAuctionIndex(m_auctionItemData, mIndexKey,
                                                       sortBy='',
                                                       reversed=self.defaultIndexSortReversed)

        sortBy = self.defaultIndexSortKey
        if self.isAuctionIndexKeyValidated((sortBy,)):
            for mIndexKey, _auctionItemIndexDic in self._auctionItemIndex.items():
                for k, _m_auctionItemIndexItemData in _auctionItemIndexDic.items():
                    _m_auctionItemIndexItemData.sort(
                        key=lambda _id: getattr(self.auctionItemData[_id], sortBy),
                        reverse=self.defaultIndexSortReversed)

    def _syncAddItemInAuctionIdx(self, auctionItem: AuctionItem, sortBy='', reversed=False):
        for mIndexKey in self.auctionIndexInfo:
            self._syncAddItemInSpecialAuctionIndex(auctionItem, mIndexKey, sortBy, reversed)

    def _syncAddItemInSpecialAuctionIndex(self, auctionItem, indexKey, sortBy='', reversed=False):
        mIndexKeyList = self.splitAuctionIndex(indexKey)
        mIndexItemKey = auctionItem.buildIndexKeyFromAttrsName(*mIndexKeyList)
        if mIndexItemKey is None:
            return

        self._auctionItemIndex.setdefault(indexKey, {})
        _m_auctionItemIndexDic = self._auctionItemIndex[indexKey]
        _m_auctionItemIndexDic.setdefault(mIndexItemKey, [])
        _m_auctionItemIndexItemData = _m_auctionItemIndexDic[mIndexItemKey]
        _m_auctionItemIndexItemData.insert(0, auctionItem.auctionItemUUID)

        self._auctionItemIndexDirty.setdefault(indexKey, {})
        _m_auctionItemIndexDirtyDic = self._auctionItemIndexDirty[indexKey]
        _m_auctionItemIndexDirtyDic[mIndexItemKey] = _m_auctionItemIndexDirtyDic.get(mIndexItemKey, 0) + 1
        self._sortAuctionItemIndex(indexKey, mIndexItemKey, 100)

    def putItemInAuction(self, auctionItem: AuctionItem):
        if auctionItem.auctionType != self.auctionType:
            return False, gameconst.AuctionErrno.ERR_AUCTION_TYPE_ERR.initkvbody()()
        if auctionItem.auctionItemUUID in self.auctionItemData:
            return False, gameconst.AuctionErrno.ERR_AUCTION_ALREADY_IN_AUCTION.initkvbody()()

        self.auctionItemData[auctionItem.auctionItemUUID] = auctionItem

        self._syncAddItemInAuctionIdx(
            auctionItem, 
            sortBy=self.defaultIndexSortKey,
            reversed=self.defaultIndexSortReversed,
        )

        self.refreshAuctionDefaultSortData()
        return True, gameconst.AuctionErrno.ERR_AUCTION_OK

    def _syncRemoveItemFromAuctionIndex(self, auctionItem, sortBy='', reversed=False):
        for mIndexKey, _m_auctionItemIndexDic in self._auctionItemIndex.items():
            mIndexKeyList = self.splitAuctionIndex(mIndexKey)
            mIndexItemKey = auctionItem.buildIndexKeyFromAttrsName(*mIndexKeyList)
            if mIndexItemKey is None:
                # LOG_WARN("Auction::_syncRemoveItemFromAuctionIndex:: indexKey skipped",
                #             auctionItem.auctionItemUUID, mIndexKeyList)
                continue

            _m_auctionItemIndexItemData = _m_auctionItemIndexDic[mIndexItemKey]
            if auctionItem.auctionItemUUID in _m_auctionItemIndexItemData:
                _m_auctionItemIndexItemData.remove(auctionItem.auctionItemUUID)
                self._auctionItemIndexDirty.setdefault(mIndexKey, {})
                _m_auctionItemIndexDirtyDic = self._auctionItemIndexDirty[mIndexKey]
                _m_auctionItemIndexDirtyDic[mIndexItemKey] = _m_auctionItemIndexDirtyDic.get(mIndexItemKey, 0) + 1
                self._sortAuctionItemIndex(mIndexKey, mIndexItemKey, 100)

    def getItemFromAuctionByUUID(self, auctionItemUUID, default=None):
        return self.auctionItemData.get(auctionItemUUID, default)

    def popItemFromAuction(self, auctionItemUUID):
        if auctionItemUUID not in self.auctionItemData:
            return None, gameconst.AuctionErrno.ERR_AUCTION_NOT_IN_AUCTION.initkvbody()()
        mAuctionItem = self.auctionItemData.pop(auctionItemUUID)
        self._syncRemoveItemFromAuctionIndex(mAuctionItem, sortBy=self.defaultIndexSortKey,
                                             reversed=self.defaultIndexSortReversed)
        self.refreshAuctionDefaultSortData()
        return mAuctionItem, gameconst.AuctionErrno.ERR_AUCTION_OK

    def _validateSearchOptions(self, searchOptions):
        mRmKeys = []
        for k, v in searchOptions.items():
            if v is None:
                LOG_WARN("_validateSearchOptions:: None value in search kv", k, v)
                mRmKeys.append(k)
        for _i in mRmKeys:
            searchOptions.pop(_i)
        return searchOptions

    def iterSearchItemFromAuction(self, searchOptions, filterFn=None):
        _mErrno = gameconst.AuctionErrno
        self._validateSearchOptions(searchOptions)
        m_searchAttrs = list(searchOptions)
        if not self.isAuctionIndexKeyValidated(m_searchAttrs):
            return [], _mErrno.ERR_AUCTION_ITEM_ATTR_NOT_DEFINED.initkvbody()()
        _hasMultipleOptVal = any(utils.checkCanIterable(i) for i in searchOptions.values())

        mIndexKey = self.joinAuctionIndex(m_searchAttrs)
        m_searchAttrs = self.splitAuctionIndex(mIndexKey)

        if not _hasMultipleOptVal and self.hasAuctionIndex(mIndexKey):
            mIndexItemKey = self.joinAuctionIndex(
                map(lambda i: searchOptions[i], m_searchAttrs), nosort=True)
            return self._iterGetItemsFromAuctionWithIndex(mIndexKey, mIndexItemKey, filterFn), _mErrno.ERR_AUCTION_OK

        else:
            return self._iterGetItemsFromAuctionNoIndex(searchOptions, filterFn), _mErrno.ERR_AUCTION_OK

    def _iterGetItemsFromAuctionWithIndex(self, indexKey, indexItemKey, filterFn):
        LOG_INFO("_iterGetItemsFromAuctionWithIndex::", indexKey, indexItemKey)
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
        # LOG_DBG("_iterGetItemsFromAuctionNoIndex::", searchOptions)
        for m_auctionItemData in self._defaultAuctionSortedData:
            _skipped = False
            for k, v in searchOptions.items():
                mAttrVal = getattr(m_auctionItemData, k)
                if utils.checkCanIterable(v):
                    if mAttrVal in v:
                        continue
                    else:
                        _skipped = True
                        break
                else:
                    if mAttrVal == v:
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


class AuctionPlayerCache(userType.UserSTSoleType):

    def _lateReload(self):
        for _d in self.followedItemData:
            _d.reloadScript()

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

    def __init__(self, auctionType=gameconst.AuctionTypeEnum.UNKNOWN, unlockedGrids=0):
        # presistent
        self.unlockedGrids = unlockedGrids
        self.auctionType = auctionType
        self.followedItemData = []
        self.followedAuctionItemUUIDData = []
        # cache from AuctionStub
        self._itemDataCache = set()
        # private data
        self._lastSyncTime = 0
        self._locked = 0
        self._cacheInited = False

    @property
    def initGrids(self):
        if self.auctionType == gameconst.AuctionTypeEnum.COIN_AUCTION:
            return int(AUT_CONST.datas["auctionInitShelfNum"]["value"])
        else:
            return 0

    @property
    def totalFollowedNumber(self):
        return len(self.followedItemData) + len(self.followedAuctionItemUUIDData)

    @property
    def totalGrids(self):
        return self.initGrids + self.unlockedGrids

    def isSyncTimeOutdate(self, t):
        return self._lastSyncTime > t

    def updateSyncTime(self, t):
        self._lastSyncTime = t

    def isLocked(self, now=None):
        return self._locked > (now or utils.curTS())

    def lock(self, timeout=3, now=None):
        now = now or utils.curTS()
        if self.isLocked(now):
            LOG_WARN("AuctionPlayerCache::lock::already locked", self.auctionType)
        self._locked = now + timeout

    def isCacheInited(self):
        return bool(self._cacheInited)

    def unlock(self):
        self._locked = 0

    def isSaleGridFull(self):
        if self.isCacheInited():
            return len(self._itemDataCache) >= self.totalGrids
        else:
            return False

    def updatePlayerCache(self, itemIdsList=None, cacheSyncT=0):
        if self.isSyncTimeOutdate(cacheSyncT):
            LOG_WARN("updatePlayerCache:: sync time outdate {}(from) < {}(cached)".format(
                cacheSyncT, self._lastSyncTime))
            return False

        self._itemDataCache.clear()
        if itemIdsList is not None:
            self._itemDataCache.update(itemIdsList)
        self._cacheInited = True

        self.updateSyncTime(cacheSyncT)
        return True

    def unlockGrid(self):
        self.unlockedGrids += 1

    def getNextUnlockGridNum(self):
        return self.unlockedGrids + 1


class AuctionItemRecord(userType.UserSTSoleType):

    def initFromDict(self, dataDic):
        self.itemId = dataDic['itemId']
        self.recordUUID = dataDic['recordUUID']
        self.totalPrice = dataDic['totalPrice']
        self.extraJoinedKV = dataDic['extraJoinedKV']
        self.number = dataDic['number']
        return self

    def toSavedDict(self):
        return {
            'itemId': self.itemId,
            'recordUUID': self.recordUUID,
            'totalPrice': self.totalPrice,
            'extraJoinedKV': self.extraJoinedKV,
            'number': self.number,
        }

    def __init__(self, recordUUID=0, itemId=0, totalPrice=0, number=0, 
                 extraJoinedKV=None, **kwargs):
        self.itemId = itemId
        self.recordUUID = recordUUID
        self.totalPrice = totalPrice
        self.extraJoinedKV = extraJoinedKV or {}
        self.number = number

    @property
    def avgPrice(self):
        return math.ceil(self.totalPrice / self.number) if self.number != 0 else 0

    def reset(self):
        self.totalPrice = 0
        self.number = 0

    def addRecord(self, price, number):
        self.totalPrice += price * number
        self.number += number


class AuctionItemRecommendRecord(userType.UserSTSoleType):

    def initFromDict(self, dataDic):
        self.itemId = dataDic['itemId']
        self.recordUUID = dataDic['recordUUID']
        self.extraJoinedKV = dataDic['extraJoinedKV']
        self.price = dataDic['price']
        return self

    def toSavedDict(self):
        return {
            'itemId': self.itemId,
            'recordUUID': self.recordUUID,
            'extraJoinedKV': self.extraJoinedKV,
            'price': self.price,
        }

    def __init__(self, recordUUID=0, itemId=0, price=0, extraJoinedKV=None):
        self.itemId = itemId
        self.recordUUID = recordUUID
        self.price = price
        self.extraJoinedKV = extraJoinedKV or {}

