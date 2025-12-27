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
import gametlog
import dataUtils
import itemFactory

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
        DEBUG_MSG("warehouseExpansion ", pendingUseId, gridNum, gridId, itemId, useNum, opUUID, context)
        bankCapacity = BGDSD.datas['bankCapacity']['value']
        if self.warehouse.capacity >= bankCapacity:
            WARNING_MSG('   in warehouseExpansion, reach limit 1:', self.warehouse.capacity)
            self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.FALSE)
            return
        newCapacity = self.warehouse.capacity + gridNum
        if newCapacity > bankCapacity:
            WARNING_MSG('   in warehouseExpansion, reach limit 2:', newCapacity)
            newCapacity = bankCapacity
        self.warehouse.capacity = newCapacity
        self.cell.onPendingUseItem(pendingUseId, gameconst.UseItem.TRUE)
        self.client.onUnlockWarehouseGrids(gameconst.BagOPStat.BAG_OP_STAT_OK, newCapacity)

    def reqGetWarehouse(self, exposed):
        self.sendWarehouseData()

    def reqUnlockWarehouse(self, exposed, gridNum):
        DEBUG_MSG('in reqUnlockWarehouse', gridNum)
        if gridNum <= 0:
            ERROR_MSG('reqUnlockWarehouse error:', gridNum)
            return

        newCapacity = self.warehouse.doUnlockWarehouseGrids(self, gridNum)
        if newCapacity:
            self.client.onUnlockWarehouseGrids(gameconst.BagOPStat.BAG_OP_STAT_OK, newCapacity)
        return

    def reqMoveItemToWarehouse(self, exposed, gridId, itemId, itemNum):
        DEBUG_MSG('in reqMoveItemToWarehouse:', gridId, itemId, itemNum)
        if self.bagData.isLocked():
            WARNING_MSG('     in reqMoveItemToWarehouse, bag locked')
            return

        if self.warehouse.isFull():
            self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
            return
        
        bankForbiddenList = BGDSD.datas['bankForbiddenList']['value']
        if bankForbiddenList and itemId in bankForbiddenList:
            WARNING_MSG('     in reqMoveItemToWarehouse, item is forbidden')
            self.onMessagePre(BGDSD.datas['putInFail_itemLimited_msg']['value'], [])
            return
        
        itemObj = self.bagData.getItemObjByGridId(gridId)
        if not itemObj or itemObj.itemId != itemId:
            WARNING_MSG('reqMoveItemToWarehouse, no this item:', gridId, itemId, itemNum)
            return
         
        if itemObj.itemNum < itemNum or itemNum <= 0:
            WARNING_MSG('reqMoveItemToWarehouse, move item is over limit:', gridId, itemId, itemObj.itemNum, itemNum)
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BAG_WAREHOUSE
        detail = gameclass.AwardDetail(gridId=gridId, itemId=itemId, itemCount=itemNum)
        # 全部移动
        if itemObj.itemNum == itemNum:
            # 检查进入仓库
            planOp, _, _ = self.warehouse.calcAddItemsPlan([itemObj])
            if planOp != gameconst.BagOpPlan.BAG_OP_OK:
                self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
                return

            bagItem = self.bagData.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail)
            if not bagItem:
                WARNING_MSG('     in moveItemToWarehouse, bagItem is None:', gridId, itemId)
                return

            opStat, planDic = self.warehouse.addItemsWithPlan(self, [bagItem, ], opUUID, srcType, detail, notify=False)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                gameengine.reportCritical('reqMoveItemToWarehouse, op error:', opStat, gridId, itemId)
        else:
            # 移动一部分
            itemObj = itemFactory.ItemFactory.createItem(itemId, itemNum, itemObj.bindType)
             # 检查进入仓库
            planOp, _, _ = self.warehouse.calcAddItemsPlan([itemObj])
            if planOp != gameconst.BagOpPlan.BAG_OP_OK:
                self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
                return
            # 从背包按照指定格子移除
            self.bagData.deductItemsByGrid(self, {gridId: itemNum}, opUUID, srcType, detail)
            # 加入仓库
            opStat, planDic = self.warehouse.addItemsWithPlan(self, [itemObj, ], opUUID, srcType, detail, notify=False)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                gameengine.reportCritical('reqMoveItemToWarehouse, op error:', opStat, gridId, itemId, itemNum)

        self.client.onWarehouseInItems(opStat, self.warehouse._getClientDataFromPlanDic(planDic))
        # self.makeWarehouseFlow(bagItem.itemId, bagItem.itemNum, bagItem.uniqueId, bagItem.bindType, 0, '')

    def reqMoveItemToBag(self, exposed, gridId, itemId, itemNum):
        DEBUG_MSG('in reqMoveItemToBag:', gridId, itemId, itemNum)
        if self.bagData.isLocked():
            WARNING_MSG('     in reqMoveItemToBag, bag locked')
            return

        if self.bagData.isFull():
            self.onMessagePre(BGDSD.datas['takeOutFail_bagFull_msg']['value'], [])
            return
        
        itemObj = self.warehouse.getItemObjByGridId(gridId)
        if not itemObj:
            WARNING_MSG("in reqMoveItemToBag, wrong arg gridId", gridId)
            return
        
        if itemObj.itemNum < itemNum or itemNum <= 0:
            WARNING_MSG('in reqMoveItemToBag, move item is over limit:', gridId, itemId, itemObj.itemNum, itemNum)
            return
        
        if self.checkBagItemLimit(itemObj.itemId, itemObj.itemNum):
            self.onMessagePre(IDSD.datas['potionMaxLimitMsgID']['value'], [str(self.drugsQuantityBase)])
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BAG_WAREHOUSE
        detail = gameclass.AwardDetail(gridId=gridId, itemId=itemId, itemCount=itemNum)
        # 全移
        if itemObj.itemNum == itemNum:
             # 检查进入背包
            planOp, _, _ = self.bagData.calcAddItemsPlan([itemObj])
            if planOp != gameconst.BagOpPlan.BAG_OP_OK:
                self.onMessagePre(BGDSD.datas['takeOutFail_bagFull_msg']['value'], [])
                return
            
            roomItem = self.warehouse.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail, sendClient=False)
            if not roomItem:
                WARNING_MSG('     in moveItemToBag, roomItem is None')
                return
            
            opStat, planDic = self.bagData.addItemsWithPlan(self, [roomItem, ], opUUID, srcType, detail, notify=False)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                gameengine.reportCritical('reqMoveItemToBag, op error:', opStat, gridId, itemId, itemNum)
        else:
            # 移动一部分
            itemObj = itemFactory.ItemFactory.createItem(itemId, itemNum, itemObj.bindType)
             # 检查进入背包
            planOp, _, _ = self.bagData.calcAddItemsPlan([itemObj])
            if planOp != gameconst.BagOpPlan.BAG_OP_OK:
                self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
                return
            # 从背包按照指定格子移除
            self.warehouse.deductItemsByGrid(self, {gridId: itemNum}, opUUID, srcType, detail)
            # 加入仓库
            opStat, planDic = self.bagData.addItemsWithPlan(self, [itemObj, ], opUUID, srcType, detail, notify=False)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                gameengine.reportCritical('reqMoveItemToBag, op error:', opStat, gridId, itemId, itemNum)
        self.client.onWarehouseOutItems(opStat, gridId, itemNum)
        # self.makeWarehouseFlow(roomItem.itemId, roomItem.itemNum, roomItem.uniqueId, roomItem.bindType, 1, '')

    def reqWarehouseSort(self, exposed):
        DEBUG_MSG('in reqWarehouseSort:')
        if self.warehouse.doBagSort(self):
            dic = self.warehouse.toBagSavedDict()
            jsonStr = json.dumps(dic).encode('ascii')
            zStr = gzip.compress(jsonStr)
            self.streamStringProxy(zStr, '', gameconst.StreamStringID.WAREHOUSE_SORT_INFO)
        return

    def makeWarehouseFlow(self, itemId, itemNum, itemUniqueId, bindType, opType, detail):
        tlogParams = {
            'GameSvrId': None,
            'dtEventTime': None,
            'vGameAppid': None,
            'PlatID': None,
            'iZoneAreaID': None,
            'vOpenID': None,
            'vRoleID': None,
            'vRoleName': None,
            'iLevel': None,
            'iVipLevel': 0,
            'iRoleCE': None,
            'itemId': itemId,
            'itemNum': itemNum,
            'itemUniqueId': itemUniqueId,
            'bindType': bindType,
            'opType': opType,
            'detail': detail,
        }
        tlogParams.update(self.getTLogCommonParams())
        gametlog.build(gameconst.GameLog.LOG_WAREHOUSE_FLOW, **tlogParams).init().commit()

    def reqWarehouseLockItem(self, exposed, gridId, itemId, uniqueId, lockStatus):
        INFO_MSG('in reqWarehouseLockItem::', gridId, itemId, uniqueId, lockStatus)
        if not dataUtils.checkLockAvailableStatus(itemId):
            ERROR_MSG('in reqWarehouseLockItem, item locker is not opened', itemId)
            return
        
        if lockStatus not in gameconst.ItemLockStatus.VALID_STATUS:
            WARNING_MSG("in reqWarehouseLockItem, wrong arg lockStatus", lockStatus)
            return
        
        itemObj = self.warehouse.getItemObjByGridId(gridId)
        if not itemObj:
            WARNING_MSG("in reqWarehouseLockItem, wrong arg gridId", gridId)
            return

        if itemObj.itemId != itemId:
            WARNING_MSG("in reqWarehouseLockItem, wrong arg itemid", uniqueId, itemObj.itemId, itemId)
            return
        
        if itemObj.uniqueId != uniqueId:
            WARNING_MSG("in reqWarehouseLockItem, wrong arg uniqueId", itemObj.uniqueId, uniqueId, itemObj.itemId, itemId)
            return
        
        itemObj.setLockStatus(lockStatus)
        self.client.onWarehouseLockItemSucc(gridId, itemId, lockStatus)