# -*- encoding:utf-8 -*-

from KBEDebug import *

import utils
import gameconst
import userType
import gameengine
import itemFactory
import dataUtils

import itemData_itemData as ITEMDATA

class ItemContainer(userType.UserSoleType):
    def __init__(self, capacity):
        self.capacity = capacity

        self.gridId2GridObj = {}
        self.itemId2gridIds = {}

    def _lateReload(self):
        super(ItemContainer, self)._lateReload()

        for v in self.gridId2GridObj.values():
            v.reloadScript()

        return

    def initFromDict(self, savedDataDict):
        self.capacity = savedDataDict['capacity']
        self.gridId2GridObj = {}
        self.itemId2gridIds = {}
        itemsList = savedDataDict['itemsList']
        for itemDict in itemsList:
            gridId = itemDict['gridId']
            if itemDict['itemId'] == 0:
                gameengine.reportCritical('in initFromDict, itemid is 0:', itemDict)
                continue
            try:
                gridObj = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)
            except Exception as e:
                gameengine.reportCritical('load item err:', itemDict, e)
                continue
            if not gridObj:
                continue
            itemId = gridObj.itemId
            self.gridId2GridObj[gridId] = gridObj
            if itemId not in self.itemId2gridIds:
                self.itemId2gridIds[itemId] = set()
            self.itemId2gridIds[itemId].add(gridId)

    def getBagData(self):
        gridIds = self.gridId2GridObj.keys()
        itemList = []
        for gridId in gridIds:
            gridObj = self.gridId2GridObj[gridId]
            try:
                gridDic = gridObj.toBagItemDict(gridId)
            except Exception as e:
                ERROR_MSG('getBagData err:', gridId, gridObj, getattr(gridObj, 'itemId', 0), e)
                continue
            itemList.append(gridDic)
        return itemList

    def toBagSavedDict(self):

        return {
            'capacity': self.capacity,
            'itemsList': self.getBagData(),
        }

    def toItemContainerClientDict(self):

        return {
            'capacity': self.capacity,
            'itemsList': self.getBagData(),
        }

    def reset(self):
        self.gridId2GridObj = {}
        self.itemId2gridIds = {}

    def isFull(self):
        return len(self.gridId2GridObj) >= self.capacity

    @property
    def leftGridCount(self):
        return self.capacity - len(self.gridId2GridObj)

    def getItemIdByGridId(self, gridId):
        gridObj = self.getItemObjByGridId(gridId)
        if gridObj:
            return gridObj.itemId
        else:
            return 0

    def getItemObjByGridId(self, gridId):
        return self.gridId2GridObj.get(gridId, None)

    def getItemDataByGridId(self, gridId):
        gridObj = self.getItemObjByGridId(gridId)
        if not gridObj:
            ERROR_MSG('getItemDataByGridId: gridObj is none {}'.format(gridId))
            return None

        itemData = ITEMDATA.datas.get(gridObj.itemId, None)
        if not itemData:
            ERROR_MSG('getItemDataByGridId: itemData is none {}'.format(gridObj.itemId))
            return None

        return itemData

    def hasItem(self, itemId):
        gridIds = self.itemId2gridIds.get(itemId)
        return bool(gridIds)

    def getEmptyGrid(self, excludes=()):
        if self.isFull():
            return None
        for gridId in range(self.capacity):
            if gridId in self.gridId2GridObj or gridId in excludes:
                continue
            return gridId
        return None

    def countEmptyGrid(self):
        return self.capacity - len(self.gridId2GridObj)

    def getGridIdsByItemId(self, itemId):
        # 获得指定itemId的所有格子
        return self.itemId2gridIds.get(itemId, [])

    def getMinGridByItemId(self, itemId, bindType):
        grids = self.getGridIdsByItemId(itemId)
        for gridId in grids:
            gridObj = self.getItemObjByGridId(gridId)
            if gridObj.bindType == bindType:
                return gridId, gridObj
        return -1, None
    
    def getGridObjsByItemId(self, itemId, bindType = gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED):
        gridObjs = []
        grids = self.getGridIdsByItemId(itemId)
        for gridId in grids:
            gridObj = self.getItemObjByGridId(gridId)
            if gridObj.bindType == bindType or bindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED:
                gridObjs.append(gridObj)
        return gridObjs

    def _recycleGrid(self, gridId, itemId):
        INFO_MSG('_recycleGrid:', gridId, itemId)
        gridIds = self.itemId2gridIds.get(itemId)
        if gridId in gridIds:
            gridIds.remove(gridId)
        if len(gridIds) == 0:
            self.itemId2gridIds.pop(itemId, None)
        self.gridId2GridObj.pop(gridId, None)

    def getItemCount(self, itemId, bindType):
        itemCount = 0
        grids = self.getGridIdsByItemId(itemId)
        for gridId in grids:
            gridObj = self.getItemObjByGridId(gridId)
            # 过期
            if gridObj.isExpired():
                continue
            # 上锁
            if gridObj.isLocked():
                continue
            # 如果是装备，检查是否损坏了
            if gridObj.isEquipmentItem() and not gridObj.isGood():
                continue
            if bindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED or bindType == gridObj.bindType:
                itemCount += gridObj.itemNum
        return itemCount

    def getItemCountWithKargs(self, itemId, bindType, **kwargs):
        itemCount = 0
        # 获取道具Item所在的格子
        grids = self.getGridIdsByItemId(itemId)
        for gridId in grids:
            # 根据格子id获取道具对象
            gridObj = self.getItemObjByGridId(gridId)
            # 判断绑定类型
            if bindType == gridObj.bindType:
                isOk = True
                # 检查属性存在且满足
                for k, v in kwargs.items():
                    if not hasattr(gridObj, k):
                        isOk = False
                        break
                    if getattr(gridObj, k) != v:
                        isOk = False
                        break
                if isOk:
                    # 累加道具个数
                    itemCount += gridObj.itemNum
        return itemCount

    def addItemsToNewGrid(self, owner, itemObj, opUUID, src, detail, gridId=None, notify=True, syncToClient=True,
                          srcSubType=0, idipSource=0):
        if gridId is None:
            gridId = self.getEmptyGrid()
        if gridId is None:
            # no free grid
            return gameconst.BagOPStat.BAG_OP_NO_SPACE, None

        if gridId in self.gridId2GridObj:
            gameengine.reportCritical('addItemsToNewGrid: add to non empty grid', gridId)
            return gameconst.BagOPStat.BAG_OP_NO_SPACE, None
        
        # 装备入包需要设置一下职业，战力计算需要
        if dataUtils.isEquipItemByItemId(itemObj.itemId):
            itemObj.setEquipSchool(owner.getAvatarSchool())

        self.gridId2GridObj[gridId] = itemObj
        self.itemId2gridIds.setdefault(itemObj.itemId, set()).add(gridId)

        return gameconst.BagOPStat.BAG_OP_STAT_OK, gridId

    def canAddItems(self, itemList):
        opPlan, _, _ = self.calcAddItemsPlan(itemList, planDetails=False)
        return opPlan == gameconst.BagOpPlan.BAG_OP_OK

    def calcAddItemsPlan(self, itemList, planDetails=True):
        # old: wrapped to existing grids
        # new: insert to empty grids
        addPlanDict = {'old': {}, 'new': {}}
        leftItemList = []
        for it in itemList:
            planResult, leftNum = self._calcAddSingleItemPlan(it, addPlanDict)

            if planResult != gameconst.BagOpPlan.BAG_OP_OK:
                if not planDetails:
                    return gameconst.BagOpPlan.BAG_OP_NO_PLAN
                leftItemList.append([it, leftNum])

        if leftItemList:
            return gameconst.BagOpPlan.BAG_OP_NO_PLAN, addPlanDict, leftItemList
        else:
            return gameconst.BagOpPlan.BAG_OP_OK, addPlanDict, leftItemList

    def _calcAddSingleItemPlan(self, item, planDict):
        totalNum = item.itemNum
        maxStackSize = item.maxStackSize(item.itemId)
        oldGrids = self.getGridIdsByItemId(item.itemId)
        for gridId in oldGrids:
            it = self.gridId2GridObj[gridId]
            planItems = planDict['old'].get(gridId, [])
            sumNum = sum([num for _, num in planItems])
            if it.canMerge(item) and it.itemNum + sumNum < maxStackSize:
                addNum = min(totalNum, maxStackSize - it.itemNum - sumNum)
                totalNum = totalNum - addNum
                planItems.append((item, addNum))
                planDict['old'][gridId] = planItems
                if totalNum == 0:
                    return gameconst.BagOpPlan.BAG_OP_OK, totalNum

        for gridId, planItems in planDict['new'].items():
            sumNum = sum([num for _, num in planItems])
            it = planItems[0][0]
            if it.canMerge(item) and sumNum < maxStackSize:
                addNum = min(totalNum, maxStackSize - sumNum)
                totalNum = totalNum - addNum
                planItems.append((item, addNum))
                if totalNum == 0:
                    return gameconst.BagOpPlan.BAG_OP_OK, totalNum

        # newGridId = self.getEmptyGrid(excludes=list(planDict['new'].keys()))
        # if newGridId is not None:
        #     planDict['new'][newGridId] = [(item, totalNum)]
        #     return gameconst.BagOpPlan.BAG_OP_OK, 0

        for oneNum in range(0, totalNum, maxStackSize):
            addNum = min(maxStackSize, totalNum - oneNum)
            newGridId = self.getEmptyGrid(excludes=list(planDict['new'].keys()))
            if newGridId is None:
                return gameconst.BagOpPlan.BAG_OP_NO_PLAN, totalNum
            planDict['new'][newGridId] = [(item, addNum)]
            totalNum -= addNum
            if totalNum == 0:
                return gameconst.BagOpPlan.BAG_OP_OK, totalNum

        return gameconst.BagOpPlan.BAG_OP_NO_PLAN, totalNum

    def addItemsWithPlan(self, owner, itemList, opUUID, src, detail, planDict=None, notify=True, syncToClient=True,
                         srcSubType=0, idipSource=0):
        INFO_MSG('addItemsWithPlan', self.isLocked(), [(i.itemId, i.itemNum) for i in itemList], opUUID, src)
        if self.isLocked():
            return gameconst.BagOPStat.BAG_OP_BAG_LOCKED, {}

        if planDict:
            addPlanCode = gameconst.BagOpPlan.BAG_OP_OK
        else:
            addPlanCode, planDict, leftList = self.calcAddItemsPlan(itemList)

        INFO_MSG('addItemsWithPlan', addPlanCode, planDict)

        if addPlanCode != gameconst.BagOpPlan.BAG_OP_OK:
            return gameconst.BagOPStat.BAG_OP_NO_SPACE, None

        for gridId, planItems in planDict['old'].items():
            item = self.gridId2GridObj[gridId]
            mergeNum = sum([num for _, num in planItems])
            item.setItemNum(item.itemNum + mergeNum)

        for gridId, planItems in planDict['new'].items():
            sumNum = sum([num for _, num in planItems])
            it = planItems[0][0]
            it.setItemNum(sumNum)
            # addItemsWithPlan已经通知客户端一次，在addItemsWithPlan里调用addItemsToNewGrid，syncToClient为False
            self.addItemsToNewGrid(owner, it, opUUID, src, detail, gridId, notify, False, srcSubType, idipSource)

        return gameconst.BagOPStat.BAG_OP_STAT_OK, planDict

    # 只计算扣除物品的方案，不扣除物品
    def calcDeductItemsPlan(self, itemsDict, itemObjs=None):
        removeDict = {}
        if itemObjs:
            for item in itemObjs:
                gridId, gridObj = self.getItemByUniqueId(item.uniqueId)
                if gridObj is None:
                    ERROR_MSG('calcDeductItemsPlan: item not found', item.uniqueId)
                    return gameconst.BagOpPlan.BAG_OP_NO_PLAN, None
                maxStackSize = gridObj.maxStackSize(gridObj.itemId)
                if maxStackSize != 1:
                    ERROR_MSG('calcDeductItemsPlan: maxStackSize must be 1', gridObj.itemId)
                    return gameconst.BagOpPlan.BAG_OP_NO_PLAN, None
                if gridObj.isLocked() :
                    ERROR_MSG('calcDeductItemsPlan: item is locked', item.uniqueId, gridObj.itemId)
                    return gameconst.BagOpPlan.BAG_OP_NO_PLAN, gridObj.itemId
                removeDict[gridId] = item.itemNum

        for itemId, itemInfo in itemsDict.items():
            for bindType, itemNum in itemInfo.items():
                if itemNum == 0:
                    continue
                leftNum, ret = self._calcDeductSingleItemPlan(itemId, bindType, itemNum, removeDict)
                if ret != gameconst.BagOpPlan.BAG_OP_OK and bindType == gameconst.ItemBindType.BIND:
                    leftNum, ret = self._calcDeductSingleItemPlan(itemId, gameconst.ItemBindType.NORMAL, leftNum, removeDict)
                if ret != gameconst.BagOpPlan.BAG_OP_OK:
                    return gameconst.BagOpPlan.BAG_OP_NO_PLAN, itemId

        return gameconst.BagOpPlan.BAG_OP_OK, removeDict

    def _calcDeductSingleItemPlan(self, itemId, bindType, totalNum, planDict):
        itemGrids = self.getGridIdsByItemId(itemId)
        for gridId in itemGrids:
            it = self.gridId2GridObj[gridId]
            planNum = planDict.get(gridId, 0)

            if it.bindType != bindType:
                continue

            # 开启了锁，并且已上锁
            if it.isLocked():
                continue

            if it.itemId == itemId and not it.isExpired() and it.itemNum > planNum:
                # 如果这个格子已经被扣除了planNum了，这次扣除要先减去
                removeNum = min(totalNum, it.itemNum - planNum)
                totalNum = totalNum - removeNum
                planDict[gridId] = planNum + removeNum
                if totalNum == 0:
                    return 0, gameconst.BagOpPlan.BAG_OP_OK

        return totalNum, gameconst.BagOpPlan.BAG_OP_NO_PLAN

    def getItemByUniqueId(self, uniqueId):
        for gridId, item in self.gridId2GridObj.items():
            if not item.uniqueId:
                continue

            if item.uniqueId == uniqueId:
                return gridId, item

        return -1, None

    def getItemByItemIdAndUniqueId(self, itemId, uniqueId, withGridId=False):
        # FIXME()(AUCTION): 现在非特殊物品没有uniqueId, 以后会有
        # 该方法可以使用`getItemByUniqueId`代替
        gridId, itemObj = -1, None
        for i_gridId, i_it in self.iterGetItemByItemIdAndUniqueId(itemId, uniqueId):
            gridId, itemObj = i_gridId, i_it
            break

        if withGridId:
            return gridId, itemObj
        else:
            return itemObj


    def iterGetItemByItemIdAndUniqueId(self, itemId, uniqueId):
        for gridId, it in self.iterGetItemByItemId(itemId):
            if it.uniqueId == uniqueId:
                yield gridId, it

    def iterGetItemByItemId(self, itemId):
        gridIds = self.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            it = self.gridId2GridObj[gridId]
            yield gridId, it

    def cleanGridByGridId(self, owner, gridId, itemId, opUUID, srcType, detail, sendClient=True, srcSubType=0,
                          idipSource=0):
        # 清除grid，并返回清除前的对象
        INFO_MSG('in cleanGridByGridId:', gridId, itemId)
        cleanItem = self.getItemObjByGridId(gridId)
        if not cleanItem or cleanItem.itemId != itemId:
            WARNING_MSG('   in cleanGridByGridId, data error:', cleanItem)
            return None
        self._recycleGrid(gridId, itemId)

        return cleanItem

    # 调用前需要判断好每个grid的数量是否足够，这里面不做检查,保证执行成功，不够直接raise
    def deductItemsByGrid(self, owner, grid2ItemNum, opUUID, srcType, detail, sendClient=True):
        for gridId, deductNum in grid2ItemNum.items():
            item = self.getItemObjByGridId(gridId)
            if deductNum < 0:
                deductNum = item.itemNum
            if deductNum > item.itemNum:
                raise Exception('deductItemsByGrid error: %s %s %s %s' % (owner.id, gridId, item.itemNum, grid2ItemNum))
            item.setItemNum(item.itemNum - deductNum)
            if item.itemNum == 0:
                self._recycleGrid(gridId, item.itemId)
        return

    def deductItemsWithPlan(self, owner, itemsDict, itemsObjs, opUUID, srcType, detail, planDict=None, isCheckLock=True):
        INFO_MSG('in Bag::deductItemsWithPlan:', owner.id, itemsDict, opUUID, srcType)
        if self.isLocked():
            if isCheckLock:
                return gameconst.BagOPStat.BAG_OP_BAG_LOCKED, None
            else:
                WARNING_MSG("in Bag::deductItemsWithPlan, bag is locked, but isCheckLock is False", owner.id, itemsDict,
                            opUUID, srcType)
        if planDict:
            deductPlan = gameconst.BagOpPlan.BAG_OP_OK
        else:
            deductPlan, planDict = self.calcDeductItemsPlan(itemsDict, itemsObjs)

        if deductPlan == gameconst.BagOpPlan.BAG_OP_NO_PLAN:
            return gameconst.BagOPStat.BAG_OP_ITEMS_NOT_ENOUGH, None

        self.deductItemsByGrid(owner, planDict, opUUID, srcType, detail)

        return gameconst.BagOPStat.BAG_OP_STAT_OK, planDict

    @utils.checkBagLocked
    def doCleanBag(self, owner, opUUID, src, detail):
        deductDic = {}
        for gridId, gridObj in self.gridId2GridObj.items():
            deductDic[gridId] = gridObj.itemId

        for gridId, itemId in deductDic.items():
            self.cleanGridByGridId(owner, gridId, itemId, opUUID, src, detail)

        self.gridId2GridObj = {}
        self.itemId2gridIds = {}

    def getItemUniqueId(self, itemId):
        for gridId, item in self.gridId2GridObj.items():
            if item.itemId == itemId:
                return item.uniqueId
    
    # 这里有限消耗绑定的
    def getGridIDsWithConds(self, itemId, bindType, count, args = None, excludedGridIDs = None, isNormalTypeFirst = False):
        if count <= 0:
            return False, None, None
        if bindType not in gameconst.ItemBindType.VALID_BIND_TYPE:
            return False, None, None
        gridIDs = self.itemId2gridIds.get(itemId, None)
        if not gridIDs:
            return False, None, None
        bindCount = 0
        bindGridIDs = {}
        normalCount = 0
        normalGridIDs = {}
        for gridID in gridIDs:
            if excludedGridIDs and gridID in excludedGridIDs:
                continue
            item = self.gridId2GridObj.get(gridID)
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
                        bindGridIDs[gridID] = bindGridIDs.get(gridID, 0) + count
                        return True, bindGridIDs, [bindCount, 0]
                    else:
                        count -= item.itemNum
                        bindGridIDs[gridID] = bindGridIDs.get(gridID, 0) + item.itemNum
                        if count == 0:
                            return True, bindGridIDs, [bindCount, 0]

                    bindCount += item.itemNum
                elif bindType == gameconst.ItemBindType.NORMAL:
                    if item.itemNum >= count:
                        normalGridIDs[gridID] = normalGridIDs.get(gridID, 0) + count
                        return True, normalGridIDs, [0, normalCount]
                    else:
                        count -= item.itemNum
                        normalGridIDs[gridID] = normalGridIDs.get(gridID, 0) + item.itemNum
                        if count == 0:
                            return True, normalGridIDs, [0, normalCount]
                        
                    normalCount += item.itemNum
                elif bindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED:
                    if item.bindType == gameconst.ItemBindType.BIND:
                        bindGridIDs[gridID] = bindGridIDs.get(gridID, 0) + item.itemNum
                        bindCount += item.itemNum
                    elif item.bindType == gameconst.ItemBindType.NORMAL:
                        normalGridIDs[gridID] = normalGridIDs.get(gridID, 0) + item.itemNum
                        normalCount += item.itemNum
        # 同时满足的, 优先使用绑定的, 再使用未绑定的, 需要计算一遍
        if bindType == gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED:
            results = {}
            bindCount = 0
            normalCount = 0
            if isNormalTypeFirst:
                for gridID, itemNum in normalGridIDs.items():
                    if itemNum > count:
                        normalCount += count
                        results[gridID] = results.get(gridID, 0) + count
                        return True, results, [bindCount, normalCount]
                    else:
                        count -= itemNum
                        normalCount += itemNum
                        results[gridID] = results.get(gridID, 0) + itemNum
                        if count == 0:
                            return True, results, [bindCount, normalCount]
                        
                for gridID, itemNum in bindGridIDs.items():
                    if itemNum > count:
                        bindCount += count
                        results[gridID] = results.get(gridID, 0) + count
                        return True, results, [bindCount, normalCount]
                    else:
                        count -= itemNum
                        bindCount += itemNum
                        results[gridID] = results.get(gridID, 0) + itemNum
                        if count == 0:
                            return True, results, [bindCount, normalCount]
            else:
                for gridID, itemNum in bindGridIDs.items():
                    if itemNum > count:
                        bindCount += count
                        results[gridID] = results.get(gridID, 0) + count
                        return True, results, [bindCount, normalCount]
                    else:
                        count -= itemNum
                        bindCount += itemNum
                        results[gridID] = results.get(gridID, 0) + itemNum
                        if count == 0:
                            return True, results, [bindCount, normalCount]
                        
                for gridID, itemNum in normalGridIDs.items():
                    if itemNum > count:
                        normalCount += count
                        results[gridID] = results.get(gridID, 0) + count
                        return True, results, [bindCount, normalCount]
                    else:
                        count -= itemNum
                        normalCount += itemNum
                        results[gridID] = results.get(gridID, 0) + itemNum
                        if count == 0:
                            return True, results, [bindCount, normalCount]

        return False, None, None
    