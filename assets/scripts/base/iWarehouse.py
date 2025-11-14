# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import gameconst
import WarehouseBag
import bagData_bankUnlock as BGBND
import bagData_set as BagDataSet
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gamelog
import dropAward
import json
import gzip
import bagData_set as BGDSD
import gameengine
import gameclass
import gametlog
import dataUtils
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
        bankCapacity = BagDataSet.datas['bankCapacity']['value']
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

    def reqMoveItemToWarehouse(self, exposed, gridId, itemId):
        DEBUG_MSG('in reqMoveItemToWarehouse:', gridId, itemId)
        if self.bagData.isLocked():
            WARNING_MSG('     in reqMoveItemToWarehouse, bag locked')
            return

        itemObj = self.bagData.getItemObjByGridId(gridId)
        if not itemObj:
            WARNING_MSG('reqMoveItemToWarehouse, no this item:' ,gridId, itemId)
            return
        planOp, _, _ = self.warehouse.calcAddItemsPlan([itemObj])
        if planOp != gameconst.BagOpPlan.BAG_OP_OK:
            self.onMessagePre(BGDSD.datas['putInFail_bankFull_msg']['value'], [])
            return

        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_BAG_WAREHOUSE
        detail = gameclass.AwardDetail(gridId=gridId, itemId=itemId)
        bagItem = self.bagData.getItemObjByGridId(gridId)
        if not bagItem or bagItem.itemId!=itemId:
            WARNING_MSG('     in moveItemToWarehouse, no bag item:', gridId, itemId, bagItem)
            return

        bagItem = self.bagData.cleanGridByGridId(self, gridId, itemId, opUUID, src, detail)
        if not bagItem:
            WARNING_MSG('     in moveItemToWarehouse, bagItem is None:', gridId, itemId)
            return
        opStat, planDic = self.warehouse.addItemsWithPlan(self, [bagItem, ], opUUID, src, detail, notify=False, syncToClient=False)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            gameengine.reportCritical('reqMoveItemToWarehouse, op error:', opStat, gridId, itemId)
        self.client.onWarehouseInItems(opStat, self.warehouse._getClientDataFromPlanDic(planDic))
        # self.makeWarehouseFlow(bagItem.itemId, bagItem.itemNum, bagItem.uniqueId, bagItem.bindType, 0, '')

    def reqMoveItemToBag(self, exposed, gridId, itemId):
        DEBUG_MSG('in moveItemToBag:', gridId, itemId)
        if self.bagData.isLocked():
            WARNING_MSG('     in moveItemToBag, bag locked')
            return

        if self.bagData.isFull():
            self.onMessagePre(BGDSD.datas['takeOutFail_bagFull_msg']['value'], [])
            return
        
        itemObj = self.warehouse.getItemObjByGridId(gridId)
        if not itemObj:
            WARNING_MSG("in reqWarehouseLockItem, wrong arg gridId", gridId)
            return
        
        if self.checkBagItemLimit(itemObj.itemId, itemObj.itemNum):
            self.onMessagePre(IDSD.datas['potionMaxLimitMsgID']['value'], [str(self.drugsQuantityBase)])
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BAG_WAREHOUSE
        detail = gameclass.AwardDetail(gridId=gridId, itemId=itemId)
        roomItem = self.warehouse.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail, sendClient=False)
        if not roomItem:
            WARNING_MSG('     in moveItemToBag, roomItem is None')
            return
        opStat, planDic = self.bagData.addItemsWithPlan(self, [roomItem, ], opUUID, srcType, detail, notify=False)
        self.client.onWarehouseOutItems(opStat, gridId)
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