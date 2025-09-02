# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine

import BaseBag
import gameconst
import utils
import dataUtils
import dropAward

import bagData_set as BagDataSet
import bagData_bankUnlock as BGBUD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gameclass


class WarehouseBag(BaseBag.BaseBag):

    def __init__(self, capacity=0):
        super(WarehouseBag, self).__init__(capacity)
        self.bagType = gameconst.BagType.BAG_TYPE_WAREHOUSE

    def warehouseDailyUpdate(self):
        for itemObj in self.gridId2GridObj.values():
            itemObj.onItemDailyUpdate()
        return

    @utils.checkBagLocked
    def doUnlockWarehouseGrids(self, owner, gridNum):
        DEBUG_MSG('in doUnlockWarehouseGrids', gridNum)
        bankCapacity = BagDataSet.datas['bankCapacity']['value']
        if self.capacity >= bankCapacity:
            WARNING_MSG('   in doUnlockWarehouseGrids, reach limit:', self.capacity)
            return
        newCapacity = self.capacity + gridNum
        initGridNum = BagDataSet.datas['initBankCapacity']['value']
        if newCapacity > bankCapacity:
            WARNING_MSG('   in doUnlockWarehouseGrids, reach limit:', newCapacity)
            return

        startGrid = self.capacity - initGridNum + 1
        deductWealthVal = dropAward.DeductWealthVal()
        for gridId in range(startGrid, startGrid + gridNum):
            needItemId = BGBUD.datas[gridId]['itemNeeded']
            itemNum = BGBUD.datas[gridId]['itemNum']
            deductWealthVal.addWealthByItemId(needItemId, itemNum, dataUtils.getItemDefaultBindType())
            DEBUG_MSG('     in doUnlockWarehouseGrids:', needItemId, itemNum)

        if not owner.canDeductWealth(deductWealthVal, sendMsg=True):
            WARNING_MSG('       in doUnlockWarehouseGrids, items not enough:', deductWealthVal)
            return
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_UNLOCK_GRIDS
        detail = gameclass.AwardDetail(capacity=self.capacity, newCapacity=newCapacity)
        owner.deductWealth(srcType, deductWealthVal, opUUID, detail)
        self.capacity = newCapacity
        return self.capacity