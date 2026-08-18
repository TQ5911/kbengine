# -*- encoding:utf-8 -*-
from KBEDebug import *
import KBEngine
import utils

import gameconst
import itemContainer
import gameengine
import dataUtils
import _pickle as cPickle
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemType as IDITD
import Item
import EquipmentItem
import BaseItem


class BaseBag(itemContainer.ItemContainer):
    def __init__(self, capacity=0, **kwargs):
        super(BaseBag, self).__init__(capacity)
        self.lockedTime = 0
        self.bagType = 0
        self.lockDesc = ''
        self.lastSortBag = 0

    @classmethod
    def _checkIgnores_(cls):
        return 'lockedTime', 'lockDesc'
    
    def _lateReload(self):
        try:
            super(BaseBag, self)._lateReload()
        except TypeError as e:
            LOG_ERR('BaseBag', id(BaseBag), id(self.__class__), self.__class__.__name__)
            raise e

    def initFromDict(self, savedDataDict):
        super(BaseBag, self).initFromDict(savedDataDict)
        self.lastSortBag = savedDataDict.get('lastSortBag', 0)
        self.bagType = savedDataDict['bagType']

    def toBagSavedDict(self):
        _containerData = super(BaseBag, self).toBagSavedDict()

        bagData = {
            'bagType': self.bagType,
            'lastSortBag': self.lastSortBag,
        }
        _containerData.update(bagData)

        return _containerData

    def toBaseBagClientDict(self):
        _containerData = super(BaseBag, self).toItemContainerClientDict()

        bagData = {
            'bagType': self.bagType,
            'lastSortBag': self.lastSortBag,
        }
        _containerData.update(bagData)

        return _containerData

    def isLocked(self):
        _now = utils.curTS()
        return _now < self.lockedTime

    def tryLockBag(self, lockSecs=3, lockDesc=''):
        if self.isLocked():
            return False
        self.lockedTime = utils.curTS() + lockSecs
        self.lockDesc = lockDesc
        return True

    def unLockBag(self):
        self.lockedTime = 0
        self.lockDesc = ''

    def _clientDataFromPlanDic(self, planDic):
        normalItemGridList = []
        normalItemList = []
        equipItemGridList = []
        _equipItemList = []

        for _gridId in planDic['old'].keys():
            item = self.getItemObjByGridId(_gridId)
            if item.isEquipmentItem():
                equipItemGridList.append(_gridId)
                _equipItemList.append(item.toClientEquipItemDict())
            else:
                normalItemGridList.append(_gridId)
                normalItemList.append(item.toItemSavedDict())

        for _gridId in planDic['new'].keys():
            item = self.getItemObjByGridId(_gridId)
            if item.isEquipmentItem():
                equipItemGridList.append(_gridId)
                _equipItemList.append(item.toClientEquipItemDict())
            else:
                normalItemGridList.append(_gridId)
                normalItemList.append(item.toItemSavedDict())

        return normalItemGridList, normalItemList, equipItemGridList, _equipItemList

    def _getClientDataFromPlanDic(self, planDic):
        clientData = []
        for _gridId in planDic['old'].keys():
            item = self.getItemObjByGridId(_gridId)
            clientData.append(item.toBagItemDict(_gridId))

        for _gridId in planDic['new'].keys():
            item = self.getItemObjByGridId(_gridId)
            clientData.append(item.toBagItemDict(_gridId))

        return clientData

    def addItemsWithPlan(self, owner, itemList, opUUID, src, detail, planDic=None, notify=True, syncToClient=True):
        opStat, planDic = super(BaseBag, self).addItemsWithPlan(owner, itemList, opUUID, src, detail, planDic, notify,
                                                                 syncToClient)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            return opStat, planDic
        if src == AAC_AACDD.datas.BONUS_SRC_BAG_SORT:
            return opStat, planDic
        if syncToClient:
            normalItemGridList, normalItemList, equipItemGridList, equipItemList = self._clientDataFromPlanDic(planDic)
            owner.client.onAddBagItems(
                self.bagType, 
                src, 
                normalItemGridList, 
                normalItemList, 
                equipItemGridList,
                equipItemList,
                utils.itemListToBriefList(itemList)
            )

        return opStat, planDic

    def addItemsToNewGrid(self, owner, itemObj, opUUID, src, detail, gridId=None, syncToClient=True):
        opStat, gridId = super(BaseBag, self).addItemsToNewGrid(
            owner, 
            itemObj, 
            opUUID, 
            src, 
            detail, 
            gridId, 
            syncToClient=syncToClient
        )

        if opStat == gameconst.BagOPStat.OPERATE_BAG_STAT_OK and syncToClient:
            if itemObj.isEquipmentItem():
                owner.client.onAddBagItems(
                    self.bagType, 
                    src, 
                    [], 
                    [], 
                    [gridId], 
                    [itemObj.toClientEquipItemDict()],
                    utils.itemListToBriefList([itemObj])
                )
            else:
                owner.client.onAddBagItems(
                    self.bagType, 
                    src, 
                    [gridId], 
                    [itemObj.toItemSavedDict()], 
                    [], 
                    [],
                    utils.itemListToBriefList([itemObj])
                )

        return opStat, gridId

    def deductItemsByGridId(self, owner, grid2ItemNum, opUUID, srcType, detail, sendClient=True):
        super(BaseBag, self).deductItemsByGridId(owner, grid2ItemNum, opUUID, srcType, detail, sendClient=sendClient)

        clientData = []
        for _gridId in grid2ItemNum.keys():
            item = self.getItemObjByGridId(_gridId)
            num = item.itemNum if item else 0
            clientData.append({'gridId': _gridId, 'itemNum': num})

        if sendClient:
            owner.client.onUpdateGridItemsNum(self.bagType, clientData)

    def cleanGridByGridId(self, owner, gridId, itemId, opUUID, srcType, detail, sendClient=True):
        _cleanItem = super(BaseBag, self).cleanGridByGridId(owner, gridId, itemId, opUUID, srcType, detail, sendClient)

        if sendClient and _cleanItem:
            owner.client.onUpdateGridItemsNum(self.bagType, [{'gridId': gridId, 'itemNum': 0}])
        return _cleanItem

    def deductItemsWithPlan(self, owner, itemsDict, itemsObjs, opUUID, srcType, detail, planDic=None, isCheckLock=True):
        opStat, planDic = super(BaseBag, self).deductItemsWithPlan(owner, itemsDict, itemsObjs, opUUID, srcType, detail,
                                                                    planDic, isCheckLock)
        return opStat, planDic

    @utils.checkBagLocked
    def doBagSort(self, owner, sortFunc=None):
        now = utils.curTS()
        if now < self.lastSortBag + dataUtils.getConstVal('bankSortCooldown', 5):
            return False
        bak_gridId2GridObj = cPickle.dumps(self.gridIdToGridObj)
        bak_itemId2gridIds = cPickle.dumps(self.itemIdToGridIds)
        try:
            def _sortFunc(gridObj):
                _itemData = dataUtils.getCommItemData(gridObj.itemId)
                _sortKey = IDITD.ItemTypeSortDic.get(gridObj.itemType * 1000 + gridObj.itemSubType, gridObj.itemSubType)
                equipLevel = _itemData.get('levelRequirement', 0)
                return (_sortKey, -1 * gridObj.quality, equipLevel,
                        -gridObj.equipAttr.equipLv if gridObj.isEquipmentItem() else 0, gridObj.itemId, gridObj.bindType, 0)

            _gridObjs = self.gridIdToGridObj.values()
            _gridObjs = sorted(_gridObjs, key=sortFunc or _sortFunc)
            self.reset()
            _opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_BAG_SORT
            opStat, _ = self.addItemsWithPlan(owner, _gridObjs, _opUUID, src, None, notify=False, syncToClient=False)
            if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                # raise Exception
                gameengine.panicStack('!!!!! doBagSort error:', opStat)
                self.gridIdToGridObj = cPickle.loads(bak_gridId2GridObj)
                self.itemIdToGridIds = cPickle.loads(bak_itemId2gridIds)
                return
            self.lastSortBag = utils.curTS()
            return True
        except Exception as e:
            gameengine.panicStack('!!!!! doBagSort Exception:%s' % e)
            self.gridIdToGridObj = cPickle.loads(bak_gridId2GridObj)
            self.itemIdToGridIds = cPickle.loads(bak_itemId2gridIds)
            return True

    def calFnvHash(self):
        #字典无序，需要排序
        checkData = []
        for k in sorted(self.gridIdToGridObj.keys()):
            tmpData = []
            v = self.gridIdToGridObj[k]
            if isinstance(v, Item.Item) or isinstance(v, BaseItem.PureItem):
                tmpData.append((v.itemId, v.itemNum, v.uniqueId))
            elif isinstance(v, EquipmentItem.EquipmentItem):
                tmpData.append((v.itemId, v.itemNum, v.uniqueId, v.getEquipScore()))
            else:
                LOG_ERR('calFnvHash', type(self.gridIdToGridObj[k]))
            checkData.append((k, tmpData))
        # 3. 计算fnv
        fnv = utils.FNV1a64()
        fnv.update_str(str(checkData))
        return fnv.digest_uint64(), checkData

    #这里用pickle打包再解压出来的dict和原先的hash不一致，所以直接传dict
    def getPickleBagData(self):
        return cPickle.dumps(self.gridIdToGridObj), cPickle.dumps(self.itemIdToGridIds)
    
    def forceInitFromBagData(self, gridIdToGridObj, itemIdToGridIds):
        LOG_INFO('forceInitFromBagData', gridIdToGridObj, itemIdToGridIds)
        self.gridIdToGridObj = cPickle.loads(gridIdToGridObj)
        self.itemIdToGridIds = cPickle.loads(itemIdToGridIds)