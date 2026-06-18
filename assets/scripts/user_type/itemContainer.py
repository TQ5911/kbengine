# -*- encoding:utf-8 -*-

from KBEDebug import *

import utils
import gameconst
import userType
import gameengine
import itemFactory
import dataUtils

import itemData_itemData as ITEMDATA

class ItemContainer(userType.UserSingleType):
    def __init__(self, capacity):
        self.capacity = capacity

        self.gridIdToGridObj = {}
        self.itemIdToGridIds = {}
        self.waitExpireEquipList = {}

    def _lateReload(self):
        super(ItemContainer, self)._lateReload()

        for v in self.gridIdToGridObj.values():
            v.reloadScript()
        for v in self.waitExpireEquipList.values():
            v.reloadScript()
        return

    def initFromDict(self, savedDataDict):
        self.capacity = savedDataDict['capacity']
        self.gridIdToGridObj = {}
        self.itemIdToGridIds = {}
        _itemsList = savedDataDict['itemsList']
        for _itemDict in _itemsList:
            gridId = _itemDict['gridId']
            if _itemDict['itemId'] == 0:
                gameengine.panicStack('in initFromDict, itemid is 0:', _itemDict)
                continue
            try:
                gridObj = itemFactory.ItemFactory.createItemWithSavedDict(_itemDict)
            except Exception as e:
                gameengine.panicStack('load item err:', _itemDict, e)
                continue
            if not gridObj:
                continue
            itemId = gridObj.itemId
            self.gridIdToGridObj[gridId] = gridObj
            if itemId not in self.itemIdToGridIds:
                self.itemIdToGridIds[itemId] = set()
            self.itemIdToGridIds[itemId].add(gridId)

            if gridObj.isEquipmentItem() and gridObj.getOwnerGbId() > 0:
                self.waitExpireEquipList[gridObj.uniqueId] = gridObj

    def getBagData(self):
        _gridIds = self.gridIdToGridObj.keys()
        _itemList = []
        for gridId in _gridIds:
            gridObj = self.gridIdToGridObj[gridId]
            try:
                gridDic = gridObj.toBagItemDict(gridId)
            except Exception as exc:
                LOG_ERR('getBagData err:', gridId, gridObj, getattr(gridObj, 'itemId', 0), exc)
                continue
            _itemList.append(gridDic)
        return _itemList

    def toBagSavedDict(self):
        return {
            'itemsList': self.getBagData(),
            'capacity': self.capacity,
        }

    def toItemContainerClientDict(self):
        return {
            'itemsList': self.getBagData(),
            'capacity': self.capacity,
        }

    def reset(self):
        self.gridIdToGridObj = {}
        self.itemIdToGridIds = {}

    def isFull(self):
        return len(self.gridIdToGridObj) >= self.capacity

    @property
    def leftGridCount(self):
        return self.capacity - len(self.gridIdToGridObj)

    def getItemObjByGridId(self, gridId):
        return self.gridIdToGridObj.get(gridId, None)

    def fetchEmptyGrid(self, excludes=()):
        if self.isFull():
            return None

        for _gridId in range(self.capacity):
            if _gridId in self.gridIdToGridObj or _gridId in excludes:
                continue
            return _gridId
        return None

    def getGridIdsByItemId(self, itemId):
        # 获得指定itemId的所有格子
        return self.itemIdToGridIds.get(itemId, [])

    def getMinGridByItemId(self, itemId, bindType):
        _grids = self.getGridIdsByItemId(itemId)
        for _gridId in _grids:
            gridObj = self.getItemObjByGridId(_gridId)
            if gridObj.bindType == bindType:
                return _gridId, gridObj
        return -1, None
    
    def _recycleGrid(self, gridId, itemId):
        LOG_INFO('_recycleGrid:', gridId, itemId)
        _gridIds = self.itemIdToGridIds.get(itemId)
        if gridId in _gridIds:
            _gridIds.remove(gridId)
        if len(_gridIds) == 0:
            self.itemIdToGridIds.pop(itemId, None)
        gridObj = self.gridIdToGridObj.pop(gridId, None)
        if gridObj:
            # 从背包移除了，清理下待过期的装备列表
            self.waitExpireEquipList.pop(gridObj.uniqueId, None)

    def getItemCount(self, gbId, itemId, bindType):
        _itemCount = 0
        _grids = self.getGridIdsByItemId(itemId)
        for gridId in _grids:
            gridObj = self.getItemObjByGridId(gridId)
            # 过期
            if gridObj.isExpired():
                continue
            # 上锁
            if gridObj.isLocked():
                continue
            # 如果是装备，检查是否损坏了
            if gridObj.isEquipmentItem() and not gridObj.isGood(gbId):
                continue
            if bindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED or bindType == gridObj.bindType:
                _itemCount += gridObj.itemNum
        return _itemCount

    def addItemsToNewGrid(self, owner, itemObj, opUUID, srcType, detail, gridId=None, syncToClient=True):
        if gridId is None:
            gridId = self.fetchEmptyGrid()

        if gridId is None:
            # no free grid
            return gameconst.BagOPStat.OPERATE_BAG_NO_SPACE, None

        if gridId in self.gridIdToGridObj:
            gameengine.panicStack('addItemsToNewGrid: add to non empty grid', gridId)
            return gameconst.BagOPStat.OPERATE_BAG_NO_SPACE, None
        
        # 装备入包需要设置一下职业，战力计算需要
        if dataUtils.isEquipItemByItemId(itemObj.itemId):
            itemObj.setEquipSchool(owner.getAvatarSchool())
            if itemObj.getOwnerGbId() > 0:
                self.waitExpireEquipList[itemObj.uniqueId] = itemObj

        self.gridIdToGridObj[gridId] = itemObj
        self.itemIdToGridIds.setdefault(itemObj.itemId, set()).add(gridId)

        return gameconst.BagOPStat.OPERATE_BAG_STAT_OK, gridId

    def calcAddItemsPlan(self, itemList, planDetails=True):
        # old: wrapped to existing _grids
        # new: insert to empty _grids
        addPlanDict = {'old': {}, 'new': {}}
        leftItemList = []
        for _it in itemList:
            planResult, leftNum = self._calcAddSingleItemPlan(_it, addPlanDict)

            if planResult != gameconst.BagOpPlan.OPERATE_BAG_OK:
                if not planDetails:
                    return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN
                leftItemList.append([_it, leftNum])

        if leftItemList:
            return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN, addPlanDict, leftItemList
        else:
            return gameconst.BagOpPlan.OPERATE_BAG_OK, addPlanDict, leftItemList

    def _calcAddSingleItemPlan(self, item, planDict):
        _totalNum = item.itemNum
        _maxStackSize = item.maxStackSize(item.itemId)
        oldGrids = self.getGridIdsByItemId(item.itemId)
        for gridId in oldGrids:
            _it = self.gridIdToGridObj[gridId]
            _planItems = planDict['old'].get(gridId, [])
            sumNum = sum([num for _, num in _planItems])
            if _it.canMerge(item) and _it.itemNum + sumNum < _maxStackSize:
                addNum = min(_totalNum, _maxStackSize - _it.itemNum - sumNum)
                _totalNum = _totalNum - addNum
                _planItems.append((item, addNum))
                planDict['old'][gridId] = _planItems
                if _totalNum == 0:
                    return gameconst.BagOpPlan.OPERATE_BAG_OK, _totalNum

        for gridId, _planItems in planDict['new'].items():
            sumNum = sum([num for _, num in _planItems])
            _it = _planItems[0][0]
            if _it.canMerge(item) and sumNum < _maxStackSize:
                addNum = min(_totalNum, _maxStackSize - sumNum)
                _totalNum = _totalNum - addNum
                _planItems.append((item, addNum))
                if _totalNum == 0:
                    return gameconst.BagOpPlan.OPERATE_BAG_OK, _totalNum

        for oneNum in range(0, _totalNum, _maxStackSize):
            addNum = min(_maxStackSize, _totalNum - oneNum)
            newGridId = self.fetchEmptyGrid(excludes=list(planDict['new'].keys()))
            if newGridId is None:
                return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN, _totalNum
            planDict['new'][newGridId] = [(item, addNum)]
            _totalNum -= addNum
            if _totalNum == 0:
                return gameconst.BagOpPlan.OPERATE_BAG_OK, _totalNum

        return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN, _totalNum

    def addItemsWithPlan(self, owner, itemList, opUUID, src, detail, planDict=None, notify=True, syncToClient=True):
        LOG_INFO('addItemsWithPlan', self.isLocked(), [(_i.itemId, _i.itemNum) for _i in itemList], opUUID, src)
        if self.isLocked():
            return gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED, {}

        if planDict:
            addPlanCode = gameconst.BagOpPlan.OPERATE_BAG_OK
        else:
            addPlanCode, planDict, leftList = self.calcAddItemsPlan(itemList)

        LOG_INFO('addItemsWithPlan', addPlanCode, planDict)

        if addPlanCode != gameconst.BagOpPlan.OPERATE_BAG_OK:
            return gameconst.BagOPStat.OPERATE_BAG_NO_SPACE, None

        for gridId, _planItems in planDict['old'].items():
            item = self.gridIdToGridObj[gridId]
            mergeNum = sum([num for _, num in _planItems])
            item.setItemNum(item.itemNum + mergeNum)

        for gridId, _planItems in planDict['new'].items():
            sumNum = sum([num for _, num in _planItems])
            _it = _planItems[0][0]
            _it.setItemNum(sumNum)
            # addItemsWithPlan已经通知客户端一次，在addItemsWithPlan里调用addItemsToNewGrid，syncToClient为False
            self.addItemsToNewGrid(owner, _it, opUUID, src, detail, gridId, False)

        return gameconst.BagOPStat.OPERATE_BAG_STAT_OK, planDict

    # 只计算扣除物品的方案，不扣除物品
    def calcDeductItemsPlan(self, itemsDict, itemObjs=None):
        removeDict = {}
        if itemObjs:
            for item in itemObjs:
                gridId, gridObj = self.getItemByUniqueId(item.uniqueId)
                if gridObj is None:
                    LOG_ERR('calcDeductItemsPlan: item not found', item.uniqueId)
                    return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN, None
                maxStackSize = gridObj.maxStackSize(gridObj.itemId)
                if maxStackSize != 1:
                    LOG_ERR('calcDeductItemsPlan: maxStackSize must be 1', gridObj.itemId)
                    return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN, None
                if gridObj.isLocked() :
                    LOG_ERR('calcDeductItemsPlan: item is locked', item.uniqueId, gridObj.itemId)
                    return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN, gridObj.itemId
                if gridId in removeDict:
                    LOG_ERR('calcDeductItemsPlan: grid id is repeated', item.uniqueId, gridObj.itemId)
                    return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN, gridObj.itemId 
                removeDict[gridId] = item.itemNum

        for _itemId, _itemInfo in itemsDict.items():
            for bindType, itemNum in _itemInfo.items():
                if itemNum == 0:
                    continue
                leftNum, ret = self._calcDeductSingleItemPlan(_itemId, bindType, itemNum, removeDict)
                if ret != gameconst.BagOpPlan.OPERATE_BAG_OK and bindType == gameconst.ItemBindType.BIND:
                    leftNum, ret = self._calcDeductSingleItemPlan(_itemId, gameconst.ItemBindType.NORMAL, leftNum, removeDict)
                if ret != gameconst.BagOpPlan.OPERATE_BAG_OK:
                    return gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN, _itemId

        return gameconst.BagOpPlan.OPERATE_BAG_OK, removeDict

    def _calcDeductSingleItemPlan(self, itemId, bindType, totalNum, planDict):
        itemGrids = self.getGridIdsByItemId(itemId)
        for gridId in itemGrids:
            _it = self.gridIdToGridObj[gridId]
            planNum = planDict.get(gridId, 0)

            if _it.bindType != bindType:
                continue

            # 开启了锁，并且已上锁
            if _it.isLocked():
                continue

            if _it.itemId == itemId and not _it.isExpired() and _it.itemNum > planNum:
                # 如果这个格子已经被扣除了planNum了，这次扣除要先减去
                _removeNum = min(totalNum, _it.itemNum - planNum)
                totalNum = totalNum - _removeNum
                planDict[gridId] = planNum + _removeNum
                if totalNum == 0:
                    return 0, gameconst.BagOpPlan.OPERATE_BAG_OK

        return totalNum, gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN

    def getItemByUniqueId(self, uniqueId):
        for _gridId, _item in self.gridIdToGridObj.items():
            if not _item.uniqueId:
                continue

            if _item.uniqueId == uniqueId:
                return _gridId, _item

        return -1, None

    def fetchItemByItemIdAndUniqueId(self, itemId, uniqueId, withGridId=False):
        # FIXME()(AUCTION): 现在非特殊物品没有uniqueId, 以后会有
        # 该方法可以使用`getItemByUniqueId`代替
        _gridId, itemObj = -1, None
        for iGridId, i_it in self.iterGetItemByItemIdAndUniqueId(itemId, uniqueId):
            _gridId, itemObj = iGridId, i_it
            break

        if withGridId:
            return _gridId, itemObj
        else:
            return itemObj


    def iterGetItemByItemIdAndUniqueId(self, itemId, uniqueId):
        for _gridId, _it in self.iterGetItemByItemId(itemId):
            if _it.uniqueId == uniqueId:
                yield _gridId, _it

    def iterGetItemByItemId(self, itemId):
        _gridIds = self.getGridIdsByItemId(itemId)
        for _gridId in _gridIds:
            _it = self.gridIdToGridObj[_gridId]
            yield _gridId, _it

    def cleanGridByGridId(self, owner, gridId, itemId, opUUID, srcType, detail, sendClient=True):
        # 清除grid，并返回清除前的对象
        LOG_INFO('in cleanGridByGridId:', gridId, itemId)
        cleanItem = self.getItemObjByGridId(gridId)
        if not cleanItem or cleanItem.itemId != itemId:
            LOG_WARN('   in cleanGridByGridId, data error:', cleanItem)
            return None
        self._recycleGrid(gridId, itemId)

        return cleanItem

    # 调用前需要判断好每个grid的数量是否足够，这里面不做检查,保证执行成功，不够直接raise
    def deductItemsByGridId(self, owner, grid2ItemNum, opUUID, srcType, detail, sendClient=True):
        for _gridId, deductNum in grid2ItemNum.items():
            item = self.getItemObjByGridId(_gridId)
            if deductNum < 0:
                deductNum = item.itemNum
            if deductNum > item.itemNum:
                raise Exception('deductItemsByGridId error: %s %s %s %s' % (owner.id, _gridId, item.itemNum, grid2ItemNum))
            item.setItemNum(item.itemNum - deductNum)
            if item.itemNum == 0:
                self._recycleGrid(_gridId, item.itemId)
        return

    def deductItemsWithPlan(self, owner, itemsDict, itemsObjs, opUUID, srcType, detail, planDict=None, isCheckLock=True):
        LOG_INFO('in Bag::deductItemsWithPlan:', owner.id, itemsDict, opUUID, srcType)
        if self.isLocked():
            if isCheckLock:
                return gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED, None
            else:
                LOG_WARN("in Bag::deductItemsWithPlan, bag is locked, but isCheckLock is False", owner.id, itemsDict,
                            opUUID, srcType)
        if planDict:
            deductPlan = gameconst.BagOpPlan.OPERATE_BAG_OK
        else:
            deductPlan, planDict = self.calcDeductItemsPlan(itemsDict, itemsObjs)

        if deductPlan == gameconst.BagOpPlan.OPERATE_BAG_NO_PLAN:
            return gameconst.BagOPStat.OPERATE_BAG_ITEMS_NOT_ENOUGH, None

        self.deductItemsByGridId(owner, planDict, opUUID, srcType, detail)

        return gameconst.BagOPStat.OPERATE_BAG_STAT_OK, planDict

    @utils.checkBagLocked
    def doCleanBag(self, owner, opUUID, src, detail):
        _deductDic = {}
        for _gridId, gridObj in self.gridIdToGridObj.items():
            _deductDic[_gridId] = gridObj.itemId

        for _gridId, itemId in _deductDic.items():
            self.cleanGridByGridId(owner, _gridId, itemId, opUUID, src, detail)

        self.gridIdToGridObj = {}
        self.itemIdToGridIds = {}

    def getItemUniqueId(self, itemId):
        for _gridId, item in self.gridIdToGridObj.items():
            if item.itemId == itemId:
                return item.uniqueId
    
    # 这里有限消耗绑定的
    def getGridIDsWithConds(self, itemId, bindType, count, args = None, excludedGridIDs = None, isNormalTypeFirst = False):
        if count <= 0:
            return False, None, None
        if bindType not in gameconst.ItemBindType.VALID_BIND_TYPE:
            return False, None, None
        _gridIDs = self.itemIdToGridIds.get(itemId, None)
        if not _gridIDs:
            return False, None, None
        bindCount = 0
        bindGridIDs = {}
        normalCount = 0
        normalGridIDs = {}
        for _gridID in _gridIDs:
            if excludedGridIDs and _gridID in excludedGridIDs:
                continue
            item = self.gridIdToGridObj.get(_gridID)
            if item.isLocked():
                continue
            if bindType != gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED and bindType != item.bindType:
                continue
            isGot = True
            if args:
                for key, value in args.items():
                    data = item.getattr(key, None)
                    if data is None:
                        isGot = False
                        break
                    if data != value:
                        isGot = False
                        break
            if isGot:
                if bindType == gameconst.ItemBindType.BIND:
                    if item.itemNum >= count:
                        bindGridIDs[_gridID] = bindGridIDs.get(_gridID, 0) + count
                        bindCount += count
                        return True, bindGridIDs, [bindCount, 0]
                    else:
                        count -= item.itemNum
                        bindGridIDs[_gridID] = bindGridIDs.get(_gridID, 0) + item.itemNum
                        bindCount += item.itemNum                        
                        if count == 0:
                            return True, bindGridIDs, [bindCount, 0]

                elif bindType == gameconst.ItemBindType.NORMAL:
                    if item.itemNum >= count:
                        normalGridIDs[_gridID] = normalGridIDs.get(_gridID, 0) + count
                        normalCount += count
                        return True, normalGridIDs, [0, normalCount]
                    else:
                        count -= item.itemNum
                        normalGridIDs[_gridID] = normalGridIDs.get(_gridID, 0) + item.itemNum
                        normalCount += item.itemNum
                        if count == 0:
                            return True, normalGridIDs, [0, normalCount]
    
                elif bindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED:
                    if item.bindType == gameconst.ItemBindType.BIND:
                        bindGridIDs[_gridID] = bindGridIDs.get(_gridID, 0) + item.itemNum
                        bindCount += item.itemNum
                    elif item.bindType == gameconst.ItemBindType.NORMAL:
                        normalGridIDs[_gridID] = normalGridIDs.get(_gridID, 0) + item.itemNum
                        normalCount += item.itemNum
        # 同时满足的, 优先使用绑定的, 再使用未绑定的, 需要计算一遍
        if bindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED:
            results = {}
            bindCount = 0
            normalCount = 0
            if isNormalTypeFirst:
                for _gridID, itemNum in normalGridIDs.items():
                    if itemNum > count:
                        normalCount += count
                        results[_gridID] = results.get(_gridID, 0) + count
                        return True, results, [bindCount, normalCount]
                    else:
                        count -= itemNum
                        normalCount += itemNum
                        results[_gridID] = results.get(_gridID, 0) + itemNum
                        if count == 0:
                            return True, results, [bindCount, normalCount]
                        
                for _gridID, itemNum in bindGridIDs.items():
                    if itemNum > count:
                        bindCount += count
                        results[_gridID] = results.get(_gridID, 0) + count
                        return True, results, [bindCount, normalCount]
                    else:
                        count -= itemNum
                        bindCount += itemNum
                        results[_gridID] = results.get(_gridID, 0) + itemNum
                        if count == 0:
                            return True, results, [bindCount, normalCount]
            else:
                for _gridID, itemNum in bindGridIDs.items():
                    if itemNum > count:
                        bindCount += count
                        results[_gridID] = results.get(_gridID, 0) + count
                        return True, results, [bindCount, normalCount]
                    else:
                        count -= itemNum
                        bindCount += itemNum
                        results[_gridID] = results.get(_gridID, 0) + itemNum
                        if count == 0:
                            return True, results, [bindCount, normalCount]
                        
                for _gridID, itemNum in normalGridIDs.items():
                    if itemNum > count:
                        normalCount += count
                        results[_gridID] = results.get(_gridID, 0) + count
                        return True, results, [bindCount, normalCount]
                    else:
                        count -= itemNum
                        normalCount += itemNum
                        results[_gridID] = results.get(_gridID, 0) + itemNum
                        if count == 0:
                            return True, results, [bindCount, normalCount]

        return False, None, None
    
    def checkEquipExpire(self, owner):
        expiredEquipItemIdToUniqueIds = {}
        curTime = utils.curTS()
        equipUniques = self.waitExpireEquipList.keys()
        for equipUnique in equipUniques:
            equipItem = self.waitExpireEquipList.get(equipUnique)
            if equipItem.getOwnerGbId() != owner.gbID:
                if curTime >= equipItem.getReturnTime():
                    uniqueIds = expiredEquipItemIdToUniqueIds.get(equipItem.itemId, None)
                    if uniqueIds is None:
                        uniqueIds = []
                        expiredEquipItemIdToUniqueIds[equipItem.itemId] = uniqueIds
                    uniqueIds.append(equipItem.uniqueId)

        if len(expiredEquipItemIdToUniqueIds) == 0:
            return
        uniqueIds = []
        for itemId, uniqueIds in expiredEquipItemIdToUniqueIds.items():
            gridIds = self.itemIdToGridIds.get(itemId, None)
            if not gridIds:
                continue
            for gridId in gridIds:
                gridObj = self.gridIdToGridObj.get(gridId, None)
                if not gridObj:
                    continue
                if gridObj.uniqueId in uniqueIds:
                    uniqueIds.append(gridObj.uniqueId)

        if len(uniqueIds) > 0:
            owner.onNotifyRemoveEquip(uniqueIds)