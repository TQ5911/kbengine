# -*- encoding:utf-8 -*-
from KBEDebug import *
import KBEngine
import utils

import gameconst
import itemContainer
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gameengine
import itemData_itemType as IDITD
import dataUtils
import _pickle as cPickle


class BaseBag(itemContainer.ItemContainer):
    def __init__(self, capacity=0):
        super(BaseBag, self).__init__(capacity)
        self.bagType = 0
        self.lockedTime = 0
        self.lockDesc = ''
        self.lastSortBag = 0

    def _lateReload(self):
        try:
            super(BaseBag, self)._lateReload()
        except TypeError as e:
            DEBUG_MSG('BaseBag', id(BaseBag), id(self.__class__), self.__class__.__name__)
            raise e
        return

    def initFromDict(self, savedDataDict):
        super(BaseBag, self).initFromDict(savedDataDict)
        self.bagType = savedDataDict['bagType']
        self.lastSortBag = savedDataDict.get('lastSortBag', 0)
        self.lockedTime = 0
        self.lockDesc = savedDataDict.get('lockDesc', '')

    def toBagSavedDict(self):
        containerData = super(BaseBag, self).toBagSavedDict()

        bagData = {
            'bagType': self.bagType,
            'lastSortBag': self.lastSortBag,
            'lockedTime': 0,
            'lockDesc': self.lockDesc,
        }
        containerData.update(bagData)

        return containerData

    def toBaseBagClientDict(self):
        containerData = super(BaseBag, self).toItemContainerClientDict()

        bagData = {
            'bagType': self.bagType,
            'lastSortBag': self.lastSortBag,
            'lockedTime': self.lockedTime,
            'lockDesc': self.lockDesc,
        }
        containerData.update(bagData)

        return containerData

    def isLocked(self):
        now = utils.getNow()
        return now < self.lockedTime

    def unLockBag(self):
        self.lockedTime = 0
        self.lockDesc = ''

    def tryLockBag(self, lockSecs=3, lockDesc=''):
        if self.isLocked():
            return False
        self.lockedTime = utils.getNow() + lockSecs
        self.lockDesc = lockDesc
        return True

    def _clientDataFromPlanDic(self, planDic):
        normalItemGridList = []
        normalItemList = []
        equipItemGridList = []
        equipItemList = []

        for gridId in planDic['old'].keys():
            item = self.getItemObjByGridId(gridId)
            if item.isEquipmentItem():
                equipItemGridList.append(gridId)
                equipItemList.append(item.toClientEquipItemDict())
            else:
                normalItemGridList.append(gridId)
                normalItemList.append(item.toItemSavedDict())

        for gridId in planDic['new'].keys():
            item = self.getItemObjByGridId(gridId)
            if item.isEquipmentItem():
                equipItemGridList.append(gridId)
                equipItemList.append(item.toClientEquipItemDict())
            else:
                normalItemGridList.append(gridId)
                normalItemList.append(item.toItemSavedDict())

        return normalItemGridList, normalItemList, equipItemGridList, equipItemList

    def _getClientDataFromPlanDic(self, planDic):
        clientData = []
        for gridId in planDic['old'].keys():
            item = self.getItemObjByGridId(gridId)
            clientData.append(item.toBagItemDict(gridId))

        for gridId in planDic['new'].keys():
            item = self.getItemObjByGridId(gridId)
            clientData.append(item.toBagItemDict(gridId))

        return clientData

    def addItemsWithPlan(self, owner, itemList, opUUID, src, detail, planDict=None, notify=True, syncToClient=True,
                         srcSubType=0, idipSource=0):
        opStat, planDict = super(BaseBag, self).addItemsWithPlan(owner, itemList, opUUID, src, detail, planDict, notify,
                                                                 syncToClient, srcSubType, idipSource)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            return opStat, planDict
        if src == AAC_AACDD.datas.BONUS_SRC_BAG_SORT:
            return opStat, planDict
        if syncToClient:
            normalItemGridList, normalItemList, equipItemGridList, equipItemList = self._clientDataFromPlanDic(planDict)
            owner.client.onAddBagItems(self.bagType, src, normalItemGridList, normalItemList, equipItemGridList,
                                       equipItemList)

        return opStat, planDict

    def addItemsToNewGrid(self, owner, itemObj, opUUID, src, detail, gridId=None, notify=True, syncToClient=True,
                          srcSubType=0, idipSource=0):
        opStat, gridId = super(BaseBag, self).addItemsToNewGrid(owner, itemObj, opUUID, src, detail, gridId,
                                                                notify=notify, syncToClient=syncToClient, srcSubType=0,
                                                                idipSource=0)
        if opStat == gameconst.BagOPStat.BAG_OP_STAT_OK and syncToClient:
            if itemObj.isEquipmentItem():
                owner.client.onAddBagItems(self.bagType, src, [], [], [gridId], [itemObj.toClientEquipItemDict()])
            else:
                owner.client.onAddBagItems(self.bagType, src, [gridId], [itemObj.toItemSavedDict()], [], [])

        return opStat, gridId

    def deductItemsByGrid(self, owner, grid2ItemNum, opUUID, srcType, detail, sendClient=True):
        super(BaseBag, self).deductItemsByGrid(owner, grid2ItemNum, opUUID, srcType, detail, sendClient=sendClient)

        clientData = []
        for gridId in grid2ItemNum.keys():
            item = self.getItemObjByGridId(gridId)
            num = item.itemNum if item else 0
            clientData.append({'gridId': gridId, 'itemNum': num})

        sendClient and owner.client.onUpdateGridItemsNum(self.bagType, clientData)
        return

    def cleanGridByGridId(self, owner, gridId, itemId, opUUID, srcType, detail, sendClient=True, srcSubType=0,
                          idipSource=0):
        cleanItem = super(BaseBag, self).cleanGridByGridId(owner, gridId, itemId, opUUID, srcType, detail, sendClient,
                                                           srcSubType, idipSource=idipSource)

        if sendClient and cleanItem:
            owner.client.onUpdateGridItemsNum(self.bagType, [{'gridId': gridId, 'itemNum': 0}])
        return cleanItem

    def deductItemsWithPlan(self, owner, itemsDict, itemsObjs, opUUID, srcType, detail, planDict=None, isCheckLock=True):
        opStat, planDict = super(BaseBag, self).deductItemsWithPlan(owner, itemsDict, itemsObjs, opUUID, srcType, detail,
                                                                    planDict, isCheckLock)
        return opStat, planDict

    @utils.checkBagLocked
    def doBagSort(self, owner, sortFunc=None):
        now = utils.getNow()
        if now < self.lastSortBag + dataUtils.getConstVal('bankSortCooldown', 5):
            return False
        bak_gridId2GridObj = cPickle.dumps(self.gridId2GridObj)
        bak_itemId2gridIds = cPickle.dumps(self.itemId2gridIds)
        try:
            def _sortFunc(gridObj):
                itemData = dataUtils.getCommItemData(gridObj.itemId)
                sortKey = IDITD.ItemTypeSortDic.get(gridObj.itemType * 1000 + gridObj.itemSubType, gridObj.itemSubType)
                equipLevel = itemData.get('levelRequirement', 0)
                return (sortKey, -1 * gridObj.quality, equipLevel,
                        -gridObj.equipAttr.equipLv if gridObj.isEquipmentItem() else 0, gridObj.itemId, gridObj.bindType, gridObj.auctionTime)

            gridObjs = self.gridId2GridObj.values()
            gridObjs = sorted(gridObjs, key=sortFunc or _sortFunc)
            self.reset()
            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_BAG_SORT
            opStat, _ = self.addItemsWithPlan(owner, gridObjs, opUUID, src, None, notify=False, syncToClient=False)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                # raise Exception
                gameengine.reportCritical('!!!!! doBagSort error:', opStat)
                self.gridId2GridObj = cPickle.loads(bak_gridId2GridObj)
                self.itemId2gridIds = cPickle.loads(bak_itemId2gridIds)
                return
            self.lastSortBag = utils.getNow()
            return True
        except Exception as e:
            gameengine.reportCritical('!!!!! doBagSort Exception:%s' % e)
            self.gridId2GridObj = cPickle.loads(bak_gridId2GridObj)
            self.itemId2gridIds = cPickle.loads(bak_itemId2gridIds)
            return True
