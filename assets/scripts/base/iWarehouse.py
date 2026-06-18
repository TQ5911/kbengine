# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import gameconst
import WarehouseBag

import gamelog
import dropAward
import json
import gzip

import gameengine
import gameclass
import dataUtils
import itemFactory
import gamedecorator
import LogTrackingMgr

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import bagData_set as BGDSD
import itemData_set as IDSD

MAX_ROOMS_NUM = 4

class IWarehouse(object):
    def __init__(self):
        super(IWarehouse, self).__init__()

    def postReloadScript(self):
        if hasattr(super(IWarehouse, self), 'postReloadScript'):
            super(IWarehouse, self).postReloadScript()

        self.warehouse.reloadScript()

    def doWarehouseDailyUpdate(self):
        self.warehouse.warehouseDailyUpdate()
        return

    def sendWarehouseData(self):
        dic = self.warehouse.toBagSavedDict()
        jsonStr = json.dumps(dic).encode('ascii')
        zStr = gzip.compress(jsonStr)
        self.streamStringProxy(zStr, '', gameconst.StreamStringID.WAREHOUSE_INFO)
        return

    def warehouseExpansion(self, pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context):
        LOG_INFO("warehouseExpansion ", pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context)
        bankCapacity = BGDSD.datas['bankCapacity']['value']
        if self.warehouse.capacity >= bankCapacity:
            LOG_WARN('   in warehouseExpansion, reach limit 1:', self.warehouse.capacity)
            self.cell.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.FALSE)
            return
        
        oldCapacity = self.warehouse.capacity
        newCapacity = self.warehouse.capacity + gridNum
        if newCapacity > bankCapacity:
            LOG_WARN('   in warehouseExpansion, reach limit 2:', newCapacity)
            newCapacity = bankCapacity
        self.warehouse.capacity = newCapacity
        self.cell.onPendingUseItemFinished(pendingUseId, gameconst.UseItemEnum.TRUE)
        
        LogTrackingMgr.LogTrackingMgr.Capacity_Expansion(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            opUUID,
            self.gbID,
            gameconst.CapacityExpansionType.WAREHOUSE_ITEM,
            oldCapacity,
            gridNum,
            self.warehouse.capacity,
            self.getRoleCacheAttr('level'),
            {itemId:useNum}
        )

        self.client.onUnlockWarehouseGrids(gameconst.BagOPStat.OPERATE_BAG_STAT_OK, newCapacity)

    @gamedecorator.checkGameconfigEnable('warehouse')
    def reqGetWarehouse(self, exposed):
        self.sendWarehouseData()

    @gamedecorator.checkGameconfigEnable('warehouse')
    def reqUnlockWarehouse(self, exposed, gridNum):
        LOG_INFO('in reqUnlockWarehouse', gridNum)
        if gridNum <= 0:
            LOG_ERR('reqUnlockWarehouse error:', gridNum)
            return

        newCapacity = self.warehouse.doUnlockWarehouseGrids(self, gridNum)
        if newCapacity:
            self.client.onUnlockWarehouseGrids(gameconst.BagOPStat.OPERATE_BAG_STAT_OK, newCapacity)
        return

    @gamedecorator.checkGameconfigEnable('warehouse')
    def reqMoveItemToWarehouse(self, exposed, gridId, itemId, itemNum):
        LOG_INFO('in reqMoveItemToWarehouse:', gridId, itemId, itemNum)
        if self.bagData.isLocked():
            LOG_WARN('     in reqMoveItemToWarehouse, bag locked')
            return

        if self.warehouse.isFull():
            self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
            return
        
        bankForbiddenList = BGDSD.datas['bankForbiddenList']['value']
        if bankForbiddenList and itemId in bankForbiddenList:
            LOG_WARN('     in reqMoveItemToWarehouse, item is forbidden')
            self.onMessagePre(BGDSD.datas['putInFail_itemLimited_msg']['value'], [])
            return
        
        itemObj = self.bagData.getItemObjByGridId(gridId)
        if not itemObj or itemObj.itemId != itemId:
            LOG_WARN('reqMoveItemToWarehouse, no this item:', gridId, itemId, itemNum)
            return
         
        if itemObj.itemNum < itemNum or itemNum <= 0:
            LOG_WARN('reqMoveItemToWarehouse, move item is over limit:', gridId, itemId, itemObj.itemNum, itemNum)
            return
        
        if itemObj.isEquipmentItem() and not itemObj.isGood(self.gbID):
            LOG_WARN('reqMoveItemToWarehouse, item is not good:', gridId, itemId, itemObj.itemNum, itemNum)
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BAG_WAREHOUSE
        detail = gameclass.AwardDetailCls(gridId=gridId, itemId=itemId, itemCount=itemNum)
        # 全部移动
        if itemObj.itemNum == itemNum:
            # 检查进入仓库
            planOp, _, _ = self.warehouse.calcAddItemsPlan([itemObj])
            if planOp != gameconst.BagOpPlan.OPERATE_BAG_OK:
                self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
                return

            bagItem = self.bagData.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail)
            if not bagItem:
                LOG_WARN('     in moveItemToWarehouse, bagItem is None:', gridId, itemId)
                return

            opStat, planDic = self.warehouse.addItemsWithPlan(self, [bagItem, ], opUUID, srcType, detail, notify=False)
            if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                gameengine.panicStack('reqMoveItemToWarehouse, op error:', opStat, gridId, itemId)
        else:
            # 移动一部分
            itemObj = itemFactory.ItemFactory.createItem(itemId, itemNum, itemObj.bindType)
             # 检查进入仓库
            planOp, _, _ = self.warehouse.calcAddItemsPlan([itemObj])
            if planOp != gameconst.BagOpPlan.OPERATE_BAG_OK:
                self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
                return
            # 从背包按照指定格子移除
            self.bagData.deductItemsByGridId(self, {gridId: itemNum}, opUUID, srcType, detail)
            # 加入仓库
            opStat, planDic = self.warehouse.addItemsWithPlan(self, [itemObj, ], opUUID, srcType, detail, notify=False)
            if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                gameengine.panicStack('reqMoveItemToWarehouse, op error:', opStat, gridId, itemId, itemNum)
        LogTrackingMgr.LogTrackingMgr.Item_Movement(self.gbID, self.accountEntity.clientDistinctId, opUUID, self.gbID, itemObj.uniqueId, itemId, itemNum, itemObj.bindType, gameconst.ItemMovementType.BagToWarehouse)
        self.client.onWarehouseInItems(opStat, self.warehouse._getClientDataFromPlanDic(planDic))

    @gamedecorator.checkGameconfigEnable('warehouse')
    def reqMoveItemToBag(self, exposed, gridId, itemId, itemNum):
        LOG_INFO('in reqMoveItemToBag:', gridId, itemId, itemNum)
        if self.bagData.isLocked():
            LOG_WARN('in reqMoveItemToBag, bag locked')
            return

        if self.bagData.isFull():
            self.onMessagePre(BGDSD.datas['takeOutFail_bagFull_msg']['value'], [])
            return
        
        itemObj = self.warehouse.getItemObjByGridId(gridId)
        if not itemObj:
            LOG_WARN("in reqMoveItemToBag, wrong arg gridId", gridId)
            return
        
        if itemObj.itemNum < itemNum or itemNum <= 0:
            LOG_WARN('in reqMoveItemToBag, move item is over limit:', gridId, itemId, itemObj.itemNum, itemNum)
            return
        
        if self.checkBagItemLimit(itemObj.itemId, itemObj.itemNum):
            self.onMessagePre(IDSD.datas['potionMaxLimitMsgID']['value'], [str(self.drugsQuantityBase)])
            return
        
        if itemObj.isEquipmentItem() and not itemObj.isGood(self.gbID):
            LOG_WARN('reqMoveItemToBag, item is not good:', gridId, itemId, itemObj.itemNum, itemNum)
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BAG_WAREHOUSE
        detail = gameclass.AwardDetailCls(gridId=gridId, itemId=itemId, itemCount=itemNum)
        # 全移
        if itemObj.itemNum == itemNum:
             # 检查进入背包
            planOp, _, _ = self.bagData.calcAddItemsPlan([itemObj])
            if planOp != gameconst.BagOpPlan.OPERATE_BAG_OK:
                self.onMessagePre(BGDSD.datas['takeOutFail_bagFull_msg']['value'], [])
                return
            
            roomItem = self.warehouse.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail, sendClient=False)
            if not roomItem:
                LOG_WARN('in reqMoveItemToBag, roomItem is None')
                return
            
            opStat, planDic = self.bagData.addItemsWithPlan(self, [roomItem, ], opUUID, srcType, detail, notify=False)
            if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                gameengine.panicStack('in reqMoveItemToBag, op error:', opStat, gridId, itemId, itemNum)
        else:
            # 移动一部分
            itemObj = itemFactory.ItemFactory.createItem(itemId, itemNum, itemObj.bindType)
             # 检查进入背包
            planOp, _, _ = self.bagData.calcAddItemsPlan([itemObj])
            if planOp != gameconst.BagOpPlan.OPERATE_BAG_OK:
                self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
                return
            # 从背包按照指定格子移除
            self.warehouse.deductItemsByGridId(self, {gridId: itemNum}, opUUID, srcType, detail)
            # 加入仓库
            opStat, planDic = self.bagData.addItemsWithPlan(self, [itemObj, ], opUUID, srcType, detail, notify=False)
            if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                gameengine.panicStack('in reqMoveItemToBag, op error:', opStat, gridId, itemId, itemNum)
        LogTrackingMgr.LogTrackingMgr.Item_Movement(self.gbID, self.accountEntity.clientDistinctId, opUUID, self.gbID, itemObj.uniqueId, itemId, itemNum, itemObj.bindType, gameconst.ItemMovementType.WarehouseToBag)
        self.client.onWarehouseOutItems(opStat, gridId, itemNum)

    @gamedecorator.checkGameconfigEnable('warehouse')
    def reqWarehouseSort(self, exposed):
        LOG_INFO('in reqWarehouseSort:')
        if self.warehouse.doBagSort(self):
            dic = self.warehouse.toBagSavedDict()
            jsonStr = json.dumps(dic).encode('ascii')
            zStr = gzip.compress(jsonStr)
            self.streamStringProxy(zStr, '', gameconst.StreamStringID.WAREHOUSE_SORT_INFO)
        return

    @gamedecorator.checkGameconfigEnable('warehouse')
    def reqWarehouseLockItem(self, exposed, gridId, itemId, uniqueId, lockStatus):
        LOG_INFO('in reqWarehouseLockItem::', gridId, itemId, uniqueId, lockStatus)
        if not dataUtils.checkLockAvailableStatus(itemId):
            LOG_ERR('in reqWarehouseLockItem, item locker is not opened', itemId)
            return
        
        if lockStatus not in gameconst.ItemLockStatus.VALID_STATUS:
            LOG_WARN("in reqWarehouseLockItem, wrong arg lockStatus", lockStatus)
            return
        
        itemObj = self.warehouse.getItemObjByGridId(gridId)
        if not itemObj:
            LOG_WARN("in reqWarehouseLockItem, wrong arg gridId", gridId)
            return

        if itemObj.itemId != itemId:
            LOG_WARN("in reqWarehouseLockItem, wrong arg itemid", uniqueId, itemObj.itemId, itemId)
            return
        
        if itemObj.uniqueId != uniqueId:
            LOG_WARN("in reqWarehouseLockItem, wrong arg uniqueId", itemObj.uniqueId, uniqueId, itemObj.itemId, itemId)
            return
        
        itemObj.setLockStatus(lockStatus)
        self.client.onWarehouseLockItemSucc(gridId, itemId, lockStatus)
