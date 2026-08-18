# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine
import bagData_commonBagCapacity as BagCommCapData
import gameglobal
import utils
import bagData_set as BD_SD
import dataUtils

import message_Message_def as MMD

import itemFactory
import LogTrackingMgr

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemData as ITEM_DATA
import agent_agentConfig as A_ACD
import agent_agentFunction as A_AFD
import const_const as C_CD
import gearBase_gearBase as GBGBD
import gearBase_gearConst as GBGCD
import taskClass_taskTarget as TCCTD

import formula
import gameconst
import BaseBag
import dropAward
import awardContext
import gameengine
import gametimer
import gameclass
import itemActions
import actionContext
import gameconfig

class Bag(BaseBag.BaseBag):

    def __init__(self, bagType=0, capacity=BD_SD.datas['initCommonBagCapacity']['value']):
        super(Bag, self).__init__(capacity)
        self.itemsCDDic = {}
        self.bagType = bagType
        self.groupCDDic = {}
        self.dailyUseLimitDic = {}
        self.item2timer = {}

    def _lateReload(self):
        super(Bag, self)._lateReload()

    def doBagDailyUpdate(self, owner):
        self.dailyUseLimitDic = {}
        updateGridIds = []
        for _gridId, itemObj in self.gridIdToGridObj.items():
            if itemObj.onItemDailyUpdate():
                updateGridIds.append(_gridId)
        if updateGridIds:
            owner.client.onBagItemsDailyUpdate(updateGridIds)

    @classmethod
    def _checkIgnores_(cls):
        return 'itemsCDDic', 'groupCDDic', 'item2timer', 'lockedTime', 'lockDesc'

    def initFromDict(self, savedDataDict):
        super(Bag, self).initFromDict(savedDataDict)

        self.groupCDDic = {}
        self.itemsCDDic = {}
        self.dailyUseLimitDic = {}

        for _cdDic in savedDataDict.get('itemCDList', []):
            self.itemsCDDic[_cdDic['itemId']] = _cdDic['cdTime']

        for _cdDic in savedDataDict.get('groupCDList', []):
            self.groupCDDic[_cdDic['groupId']] = _cdDic['cdTime']

        for _useLimitData in savedDataDict.get('useItemsLimitList', []):
            self.dailyUseLimitDic[_useLimitData['itemId']] = _useLimitData['useNum']

    def toBagSavedDict(self):
        _data = super(Bag, self).toBagSavedDict()
        now = utils.curTS()
        _itemCDList = [{'itemId': itemId, 'cdTime': cdTime,} for itemId, cdTime in self.itemsCDDic.items() if
                      cdTime > now]
        groupCDList = [{'groupId': groupId, 'cdTime': cdTime,} for groupId, cdTime in self.groupCDDic.items() if
                       cdTime > now]
        _useItemsLimitList = [{'itemId': itemId, 'useNum': useNum,} for itemId, useNum in self.dailyUseLimitDic.items()]

        bagData = {
            'itemCDList': _itemCDList,
            'groupCDList': groupCDList,
            'useItemsLimitList': _useItemsLimitList,
        }
        _data.update(bagData)
        return _data

    def toBagClientDict(self):
        _data = super(Bag, self).toBaseBagClientDict()

        _itemCDList = [{'itemId': itemId, 'cdTime': cdTime,} for itemId, cdTime in self.itemsCDDic.items()]
        groupCDList = [{'groupId': groupId, 'cdTime': cdTime,} for groupId, cdTime in self.groupCDDic.items()]
        _useItemsLimitList = [{'itemId': itemId, 'useNum': useNum,} for itemId, useNum in self.dailyUseLimitDic.items()]

        bagData = {
            'itemCDList': _itemCDList,
            'groupCDList': groupCDList,
            'useItemsLimitList': _useItemsLimitList,
        }
        _data.update(bagData)
        return _data

    def addItemsToNewGrid(self, owner, itemObj, opUUID, src, detail, gridId=None, syncToClient=True):
        _opStat, gridId = super(Bag, self).addItemsToNewGrid(
            owner, 
            itemObj, 
            opUUID, 
            src, 
            detail, 
            gridId,
            syncToClient
        )

        if src != AAC_AACDD.datas.BONUS_SRC_BAG_SORT:
            newCount = self.getItemCount(owner.gbID, itemObj.itemId, itemObj.bindType, True)
            owner.makeItemFlowLog(
                self.bagType,
                itemObj.bindType,
                itemObj.itemId,
                itemObj.uniqueId,
                itemObj.itemNum,
                opUUID,
                src,
                newCount,
                detail
            )

        return _opStat, gridId

    def addItemsWithPlan(self, owner, itemList, opUUID, src, detail, planDic=None, notify=True, syncToClient=True,
                         directly=True):
        _opStat, planDic = super(Bag, self).addItemsWithPlan(owner, itemList, opUUID, src, detail, planDic, notify,
                                                             syncToClient)
        if _opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            return _opStat, planDic

        tmpItem = {}
        tmpEquipList = []

        for _gridId, _planItems in planDic['old'].items():
            item = self.getItemObjByGridId(_gridId)
            mergeNum = sum([num for _, num in _planItems])
            _itemData = ITEM_DATA.datas.get(item.itemId, None)
            if not _itemData:
                continue

            if item.isEquipmentItem():
                tmpEquipList.append(item)
                continue
            
            datas = tmpItem.setdefault(item.itemId, {})
            datas[item.bindType] = datas.get(item.bindType, 0) + mergeNum

            newCount = self.getItemCount(owner.gbID, item.itemId, item.bindType, True)
            owner.makeItemFlowLog(
                self.bagType,
                item.bindType,
                item.itemId,
                item.uniqueId,
                mergeNum,
                opUUID,
                src,
                newCount,
                detail,
            )

        for _gridId, _planItems in planDic['new'].items():
            item = self.getItemObjByGridId(_gridId)
            sumNum = sum([num for _, num in _planItems])
            _itemData = dataUtils.getCommItemData(item.itemId)
            if not _itemData:
                continue

            if item.isEquipmentItem():
                tmpEquipList.append(item)
                continue

            datas = tmpItem.setdefault(item.itemId, {})
            datas[item.bindType] = datas.get(item.bindType, 0) + sumNum

        popRewardUUID, itemsDictList, _ = owner.getPopRewardItemsDict(opUUID, detail, notify)

        if notify:
            for itemId, bindDatas in tmpItem.items():
                for bindType, itemNum in bindDatas.items():
                    datas = itemsDictList[0].setdefault(itemId, {})
                    datas[bindType] = datas.get(bindType, 0) + itemNum

        if notify:
            for item in tmpEquipList:
                itemsDictList[1].append([item.itemId, item.uniqueId, item.bindType])

        if src != AAC_AACDD.datas.BONUS_SRC_BAG_SORT:
            itemIdSet = set()
            itemUidSet = set()
            for it in itemList:
                itemIdSet.add(it.itemId)
                itemUidSet.add(it.uniqueId)

            owner.onItemCountChanged(itemIdSet)
            owner.onGetNewItems(itemUidSet)

        if notify and directly:
            owner._showPopReward(src, popRewardUUID, detail)
        return _opStat, planDic

    # 这里要求外部检查好每个格子有物品且数量足够，否则抛异常
    def deductItemsByGridId(self, owner, grid2ItemNum, opUUID, srcType, detail, sendClient=True):
        itemIdList = []
        deducteItems = []
        for _gridId, num in grid2ItemNum.items():
            _item = self.getItemObjByGridId(_gridId)
            itemIdList.append(_item.itemId)
            deducteItems.append((_item, num))

        super(Bag, self).deductItemsByGridId(owner, grid2ItemNum, opUUID, srcType, detail, sendClient=sendClient)

        for _item, num in deducteItems:
            newCount = self.getItemCount(owner.gbID, _item.itemId, _item.bindType, True)
            owner.makeItemFlowLog(
                self.bagType, 
                _item.bindType,
                _item.itemId,
                _item.uniqueId,
                -num, 
                opUUID, 
                srcType, 
                newCount, 
                detail,
                _item.getRestoreData(),
            )

        owner.onItemCountChanged(itemIdList)

    def cleanGridByGridId(self, owner, gridId, itemId, opUUID, srcType, detail, sendClient=True):
        oldObj = self.getItemObjByGridId(gridId)
        _cleanItem = super(Bag, self).cleanGridByGridId(owner, gridId, itemId, opUUID, srcType, detail, sendClient)
        if not _cleanItem:
            raise Exception('cleanGridByGridId, cleanItem is None, gridId{} batTyp:{} itemId {}'.format(
                gridId, self.bagType, itemId))

        owner.onItemCountChanged([itemId])
        newCount = self.getItemCount(owner.gbID, _cleanItem.itemId, _cleanItem.bindType, True)
        owner.makeItemFlowLog(
            self.bagType, 
            _cleanItem.bindType,
            _cleanItem.itemId,
            _cleanItem.uniqueId,
            -_cleanItem.itemNum, 
            opUUID, 
            srcType, 
            newCount, 
            detail,
            _cleanItem.getRestoreData(),
        )

        if oldObj.uniqueId in self.item2timer:
            tid = self.item2timer.pop(oldObj.uniqueId)
            owner._cancelDatetimeCallback(tid, gametimer.REPLACE_EXPIRED_ITEM)
        return _cleanItem

    def deductItemsWithPlan(self, owner, itemsDict, itemsObjs, opUUID, srcType, detail, planDic=None, isCheckLock=True):
        _opStat, planDic = super(Bag, self).deductItemsWithPlan(owner, itemsDict, itemsObjs, opUUID, srcType, detail,
                                                                planDic, isCheckLock)

        return _opStat, planDic

    def useItemsFail(self, owner, errCode, itemId=0):
        LOG_INFO('useItemsFail, errCode:', errCode, itemId)
        if errCode == gameconst.BagOPStat.OPERATE_BAG_LEVEL_ERR:
            owner.onMessagePre(MMD.datas.itemLackOfLevel, [])
        elif errCode == gameconst.BagOPStat.OPERATE_BAG_ITEMS_NOT_ENOUGH:
            owner.onMessagePre(MMD.datas.lackOfItem, [str(itemId)])
        elif errCode == gameconst.BagOPStat.OPERATE_BAG_DAILY_LIMIT:
            owner.onMessagePre(MMD.datas.item_dailyUseLimited, [])
        elif errCode == gameconst.BagOPStat.OPERATE_BAG_CD_ERR:
            owner.onMessagePre(MMD.datas.itemInCD, [])

    def _useItemsSucc(self, owner, gridItem, gridId, useNum):
        _itemData = dataUtils.getCommItemData(gridItem.itemId)
        if _itemData['itemCD'] > 0:
            self._updateItemCD(owner, gridItem.itemId)
            owner.syncMethodCallToCrossServerBase('onLocalServerUpdateItemCD', (gridItem.itemId, self.bagType))

        if gridItem.isReUseItem() and gridItem.useTimes > 0:
            owner.client.onUpdateGridItemsJson(
                gameconst.BagTypeEnum.BAG_TYPE_NORMAL, 
                gridId, gridItem.uniqueId, gridItem.attr2Json())

        if 0 != _itemData['dailyUseLimit']:
            self.dailyUseLimitDic[gridItem.itemId] = self.dailyUseLimitDic.get(gridItem.itemId, 0) + useNum
            owner.client.onUpdateDailyUseLimit(gridItem.itemId, self.dailyUseLimitDic.get(gridItem.itemId, 0))

        owner.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetUseItem'], (gridItem.itemId, useNum))
        if _itemData['type'] == gameconst.ItemEnum.Normal:
            if _itemData['subType'] == gameconst.ItemSubEnum.HEAL_HP\
                    or _itemData['subType'] == gameconst.ItemSubEnum.HEAL_MP:
                owner.triggerAchievementWithCtx(
                    gameconst.AchieveType.USE_POTION, 
                    actionContext.AchievementCtx(itemId=int(gridItem.itemId), useNum=useNum))

    def doUseGridItems(self, owner, gridId, itemId, useNum, useItemCtx, isBaseAct=False):
        LOG_DBG('in doUseGridItems:', gridId, itemId)
        gridObj = self.getItemObjByGridId(gridId)
        if not gridObj:
            self.useItemsFail(owner, gameconst.BagOPStat.OPERATE_BAG_DATA_ERR, itemId)
            return

        useItemCtx.bindType = gridObj.bindType
        _itemData = dataUtils.getCommItemData(gridObj.itemId)
        action = _itemData['action'] or itemActions.getItemAction(gridObj)
        actionName = action.__name__ if action else ''

        isBaseAction = (isBaseAct or actionName.endswith('_base'))
        if not isBaseAction and not self.tryLockBag(lockDesc='doUseGridItems:%s' % gridId):
            self.useItemsFail(owner, gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED, itemId)
            return

        if action:
            # 消耗品
            _opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_FROM_ITEM
            detail = gameclass.AwardDetailCls(gridId=gridId, itemId=gridObj.itemId, hasNum=gridObj.itemNum, useNum=useNum)
            now = utils.curTS()

            if gridObj.isReUseItem():
                gridObj.useTimes -= useNum
                owner.syncMethodCallToCrossServerBase('onLocalServerDeductUseTimes', (gridId, gridObj.itemId, useNum))

            if itemId not in C_CD.datas["eternalItemIDList"]['value']\
                    or (gridObj.isReUseItem() and gridObj.useTimes <= 0):
                # 正常道具使用完就没了；多次使用的道具，使用次数耗尽也就没了
                self.deductItemsByGridId(owner, {gridId: useNum}, _opUUID, srcType, detail)
                owner.syncMethodCallToCrossServerBase('onLocalServerDeductUseItem', (self.bagType, {gridId: useNum}, _opUUID, srcType, detail))
            else:
                # 无消耗道具需要调用通知接口
                owner.client.onUpdateGridItemsNum(self.bagType, [{'gridId': gridId, 'itemNum': gridObj.itemNum,}, ])

            dataDic = owner.getTempMiscProp(gameconst.EntityPropsEnum.useBagItemData, None)
            if not dataDic:
                dataDic = {}
                owner.setTempMiscProp(gameconst.EntityPropsEnum.useBagItemData, dataDic)
            dataDic[_opUUID] = {'t': now, 'gridId': gridId, 'itemId': gridObj.itemId,
                               'useNum': useNum, 'gridObj': gridObj, 'opUUID': _opUUID, 'srcType': srcType}

            # isBaseAct没用起来，新增支持可以按action名字决定在哪里执行
            if isBaseAction:
                # 在base执行的action
                useItemCtx.itemObj = gridObj
                owner.doBaseUseItemAction(action, gridId, itemId, useNum, _opUUID, useItemCtx)
                owner.afterUseItemDone(True, _opUUID)
            else:
                owner.cell.doAction(gridId, itemId, useNum, _opUUID, useItemCtx)
        else:
            self._useItemsSucc(owner, gridObj, gridId, useNum)
            self.unLockBag()

        return True

    def isUseItemsDailyLimit(self, itemId, useNum):
        _itemData = dataUtils.getCommItemData(itemId)
        if 0 == _itemData['dailyUseLimit']:
            return False
        _hasUseNum = self.dailyUseLimitDic.get(itemId, 0)
        return useNum > _itemData['dailyUseLimit'] - _hasUseNum

    def canUseGridItem(self, owner, gridId, itemId, useNum):
        if self.isUseItemsDailyLimit(itemId, useNum):
            return gameconst.BagOPStat.OPERATE_BAG_DAILY_LIMIT

        gridObj = self.getItemObjByGridId(gridId)
        if not gridObj:
            return gameconst.BagOPStat.OPERATE_BAG_DATA_ERR

        if gridObj.itemId != itemId:
            return gameconst.BagOPStat.OPERATE_BAG_DATA_ERR

        if self.isLocked():
            return gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED

        # 道具本身被上锁了
        if gridObj.isLocked():
            return gameconst.BagOPStat.OPERATE_BAG_ITEM_LOCKED

        if useNum > gridObj.itemNum:
            return gameconst.BagOPStat.OPERATE_BAG_ITEMS_NOT_ENOUGH

        # check expireTime
        now = utils.curTS()
        if gridObj.isExpired():
            return gameconst.BagOPStat.OPERATE_BAG_ITEM_EXPIRED

        if not gridObj.isEnabled():
            return gameconst.BagOPStat.OPERATE_BAG_ITEM_DISABLED

        if gridObj.isReUseItem() and (useNum != 1 or gridObj.useTimes < useNum):
            LOG_WARN('canUseGridItem reuse items useTimes failed:', gridObj.itemId, gridObj.useTimes)
            return gameconst.BagOPStat.OPERATE_BAG_REUSE_ITEM_USE_TIMES_FAILED

        # check level
        _itemData = dataUtils.getCommItemData(gridObj.itemId)
        _myLevel = gameglobal.roleCache.get(owner.id, {}).get('level', 0)
        if _myLevel != 0 and _myLevel < _itemData['levelRequirement']:
            return gameconst.BagOPStat.OPERATE_BAG_LEVEL_ERR

        # check cdtime
        cdtiem = self._getItemCD(gridObj.itemId)
        if now < cdtiem:
            return gameconst.BagOPStat.OPERATE_BAG_CD_ERR

        return gameconst.BagOPStat.OPERATE_BAG_STAT_OK

    def _updateItemCD(self, owner, itemId):
        if self.bagType != gameconst.BagTypeEnum.BAG_TYPE_NORMAL:
            return
        _itemData = dataUtils.getCommItemData(itemId)
        if not _itemData:
            return
        if 0 == _itemData['itemCD']:
            return
        cdGroup = _itemData['CDGroup']
        _newCD = utils.curTS() + _itemData['itemCD']
        if 0 == cdGroup:
            self.itemsCDDic[itemId] = _newCD
        else:
            self.groupCDDic[cdGroup] = _newCD
        owner.client.onUpdateItemCD(itemId, cdGroup, _newCD)

    def _getItemCD(self, itemId):
        now = utils.curTS()
        cd = self.itemsCDDic.get(itemId, None)
        if cd is not None:
            if now < cd:
                return cd

        _itemData = dataUtils.getCommItemData(itemId)

        cdGroup = _itemData['CDGroup']
        groupCD = self.groupCDDic.get(cdGroup, None)
        if groupCD is not None:
            if now < groupCD:
                return groupCD
        return 0

    def onUseItemDone(self, owner, isSucceed, opUUID, crossServerEnable):
        LOG_INFO('onUseItemDone:', isSucceed, opUUID, crossServerEnable)
        self.unLockBag()
        dataDic = owner.getTempMiscProp(gameconst.EntityPropsEnum.useBagItemData)
        _info = dataDic.pop(opUUID)
        gridId = _info['gridId']
        itemId = _info['itemId']
        bakGridObj = _info.get('gridObj', None)

        _itemData = dataUtils.getCommItemData(itemId)
        if isSucceed:
            self._useItemsSucc(owner, bakGridObj, gridId, _info['useNum'])

        # 返还物品:有action的物品才是消耗型物品
        elif itemId not in C_CD.datas["eternalItemIDList"]['value'] and _itemData.get('action') or bakGridObj.isReUseItem():
            if not crossServerEnable and gameconfig.isCrossServer():
                gameengine.panicStack('onUseItemDone, crossServerEnable is False, but gameconfig.isCrossServer() is True')
            else:
                owner.syncMethodCallToCrossServerBase('onLocalServerUseItemReturn', (self.bagType, _info, opUUID))
            self._doReturnItem(owner, _info, opUUID)

    def _doReturnItem(self, owner, _info, opUUID):
        gridId = _info['gridId']
        itemId = _info['itemId']
        bakGridObj = _info.get('gridObj', None)
        _curGridObj = self.getItemObjByGridId(gridId)
        if _curGridObj:
            if _curGridObj.itemId != itemId:
                LOG_WARN('onUseItemDone, itemId not matched:', _curGridObj.uniqueId, opUUID, _curGridObj.itemId,
                            itemId)
                return
            _curGridObj.setItemNum(_curGridObj.itemNum + _info['useNum'])
            owner.client.onUpdateGridItemsNum(self.bagType, [{'gridId': gridId, 'itemNum': _curGridObj.itemNum}])
        else:
            bakGridObj.setItemNum(_info['useNum'])
            self.addItemsToNewGrid(owner, bakGridObj, _info['opUUID'], _info['srcType'], 'useItemFailed', gridId)

    def _onLocalServerUseItemReturn(self, owner, info, opUUID):
        self._doReturnItem(owner, info, opUUID)

    @utils.checkBagLocked
    def doUnlockGrids(self, owner, gridNum):
        LOG_INFO('in doUnlockGrids', gridNum)
        commonBagCapacity = BD_SD.datas['commonBagCapacity']['value']
        if self.capacity >= commonBagCapacity:
            LOG_WARN('   in doUnlockGrids, reach limit:', self.capacity)
            return
        
        oldCapacity = self.capacity
        newCapacity = self.capacity + gridNum
        if newCapacity > commonBagCapacity:
            LOG_WARN('   in doUnlockGrids, reach limit:', newCapacity)
            return
        
        initGridNum = BD_SD.datas['initCommonBagCapacity']['value']
        startGrid = self.capacity - initGridNum + 1
        needItemId = 0
        itemNum = 0
        totalItemNum = 0
        deductWealthVal = dropAward.DeductWealthVal()
        for gridId in range(startGrid, startGrid + gridNum):
            needItemId = BagCommCapData.datas[gridId]['itemNeeded']
            itemNum = BagCommCapData.datas[gridId]['itemNum']
            totalItemNum += itemNum
            deductWealthVal.addWealthByItemId(needItemId, itemNum, dataUtils.getItemDefaultBindType())
            LOG_INFO('     in doUnlockGrids:', needItemId, itemNum)

        res = owner.canDeductWealth(deductWealthVal, sendMsg=True)
        if not res:
            LOG_WARN('       in doUnlockGrids, items not enough:', deductWealthVal, res())
            return
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_UNLOCK_GRIDS
        detail = gameclass.AwardDetailCls(capacity=self.capacity, newCapacity=newCapacity)
        owner.deductWealth(srcType, deductWealthVal, opUUID, detail)
        self.capacity = newCapacity
        
        LogTrackingMgr.LogTrackingMgr.Capacity_Expansion(
            owner.gbID,
            owner.accountEntity.clientDistinctId,
            opUUID,
            owner.gbID,
            gameconst.CapacityExpansionType.BAG_GOLD,
            oldCapacity,
            gridNum,
            self.capacity,
            owner.getRoleCacheAttr('level'),
            {needItemId:totalItemNum}
        )
        return self.capacity

    def getTaskItems(self, taskId):
        if self.bagType != gameconst.BagTypeEnum.BAG_TYPE_TASK:
            gameengine.panicStack('getTaskItems bagType error:', self.bagType)
            return

        return [(gridId, it.itemId) for gridId, it in self.gridIdToGridObj.items() if it.taskId == taskId]

    def doDressEquip(self, owner, gridId, dressType, dstSlotId):
        LOG_INFO('in doDressEquip, gridId:', gridId, dressType)
        gridObj = self.getItemObjByGridId(gridId)
        if gridObj is None:
            LOG_ERR('doDressEquip gridObj is None', gridId, dressType, dstSlotId)
            return False

        if not gridObj.isEquipmentItem():
            LOG_WARN('     in doDressEquip, gridObj is not equipment')
            return False

        if not gridObj.isGood(owner.gbID, True):
            LOG_WARN('     in doDressEquip, gridObj can not dress')
            return False

        _roleInfo = gameglobal.roleCache.get(owner.id, None)
        _gearInfo = GBGBD.datas.get(gridObj.itemId)

        reqClassList = _gearInfo.get('reqClass', [])
        myClass = _roleInfo['school']
        if 0 not in reqClassList and myClass not in reqClassList:
            LOG_WARN('     in doDressEquip, school not matched:', _gearInfo['reqClass'], _roleInfo['school'])
            owner.onMessagePre(MMD.datas.equipFail_classNotMatch, [])
            return False

        equipLevel = _gearInfo['equipLevel']
        roleLevel = _roleInfo['level']
        LOG_INFO('     in doDressEquip, level info:', equipLevel, roleLevel)
        if equipLevel > _roleInfo['level']:
            LOG_WARN('     in doDressEquip, level not matched:', equipLevel, roleLevel)
            owner.onMessagePre(GBGCD.datas['equipWearLowRoleLevel']['value'], [])
            return False

        now = utils.curTS()
        if not self.tryLockBag(lockDesc='doDressEquip uniqueId:%s' % gridObj.uniqueId):
            LOG_WARN('lock bag fail:', self.lockDesc, gridId, gridObj.itemId)
            return False
        opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_EQUIP_DRESS
        detail = gameclass.AwardDetailCls(uniqueid=gridObj.uniqueId)
        self.cleanGridByGridId(owner, gridId, gridObj.itemId, opUUID, _src, detail, sendClient=False)
        _tempDataDic = owner.getTempMiscProp(gameconst.EntityPropsEnum.equipDressTempData, None)
        if _tempDataDic is None:
            _tempDataDic = {}
            owner.setTempMiscProp(gameconst.EntityPropsEnum.equipDressTempData, _tempDataDic)
        _tempDataDic[opUUID] = {'t':now, 'gridId':gridId, 'opUUID':opUUID, 'gridObj':gridObj, 'dressType':dressType,}

        owner.cell.cellDressEquipment(opUUID, gridObj.toItemSavedDict(), dstSlotId)
        return True

    def doDressEquipCB(self, owner, opUUID, result, oldBodyEquipDic=None):
        LOG_INFO('in doDressEquipCB:', opUUID, result)
        self.unLockBag()
        _tempDataDic = owner.getTempMiscProp(gameconst.EntityPropsEnum.equipDressTempData, {})
        tempData = _tempDataDic.pop(opUUID, None)
        if not tempData:
            gameengine.panicStack('doDressEquipCB, tempData lost:', opUUID, _tempDataDic)

        _gridId = tempData['gridId']
        gridObj = tempData['gridObj']
        _src = AAC_AACDD.datas.BONUS_SRC_EQUIP_DRESS
        if result == gameconst.DressEquipOpEnum.EQUIP_OP_FAILED:
            detail = gameclass.AwardDetailCls(uniqueid=gridObj.uniqueId)
            self.addItemsToNewGrid(owner, gridObj, opUUID, _src, detail, _gridId, syncToClient=False)
            return

        owner.client.onUpdateGridItemsNum(self.bagType, [{'gridId': _gridId, 'itemNum': 0}])
        if result == gameconst.DressEquipOpEnum.EQUIP_OP_REPLACED:
            _dressType = tempData.get('dressType', gameconst.EQUIP_DRESS_TYPE.OP_NORMAL)
            equipItem = itemFactory.ItemFactory.createItemWithSavedDict(oldBodyEquipDic)
            if _dressType == gameconst.EQUIP_DRESS_TYPE.OP_QUICK_DRESS and self.disassembleReplacedEquip(owner, equipItem, opUUID, _src):
                #快速装备被替换下来的未强化装备要分解掉
                return
            detail = gameclass.AwardDetailCls(uniqueid=gridObj.uniqueId)
            self.addItemsToNewGrid(owner, equipItem, opUUID, _src, detail, _gridId, syncToClient=True)

    def doBagUndressEquip(self, owner, bodyEquipDic):
        LOG_INFO('in doBagUndressEquip')
        _equipItem = itemFactory.ItemFactory.createItemWithSavedDict(bodyEquipDic)
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_DRESS
        detail = gameclass.AwardDetailCls(itemId=_equipItem.itemId)
        self.addItemsWithPlan(owner, [_equipItem],  opUUID, srcType, detail, notify=False, directly=False)

    @utils.checkBagLocked
    def doBagEquipDisassemble(self, owner, gridIdList, uniqueIdList):
        LOG_INFO('in doBagEquipDisassemble:', gridIdList, uniqueIdList)
        # 装备批量分解，背包空间不够，都不能分解成功
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_DISASSEMBLE
        detail = gameclass.AwardDetailCls(gridList=gridIdList, uniqueList=uniqueIdList)
        _totalWealthVal = dropAward.AwardVal()

        _succGridIdList = []
        succUniqueIdList = []
        for _gridId, uniqueId in zip(gridIdList, uniqueIdList):
            bagEquipItem = self.getItemObjByGridId(_gridId)
            if not bagEquipItem:
                LOG_WARN('     in doBagEquipDisassemble, gridId error:', _gridId)
                continue

            if bagEquipItem.uniqueId != uniqueId:
                LOG_WARN('     in doBagEquipDisassemble, uniqueId not matched:', bagEquipItem.uniqueId)
                continue

            if not bagEquipItem.canBeDisassembled(owner.gbID):
                LOG_WARN('     in doBagEquipDisassemble, cannot be disassembled:', _gridId)
                continue

            if bagEquipItem.quality >= A_ACD.datas['itemDisassemblyLimit']['value']:
                if not owner.checkAuthDisassembleAndMsg(A_AFD.Disassembly, A_ACD.datas['itemDisassemblyLimitMsg']['value']):
                    return
            if owner.checkPopupSecondaryPassword([(gameconst.SecondaryPasswordCheckType.ITEM_DISASSEMBLE, bagEquipItem.quality)]):
                LOG_WARN('     in doBagEquipDisassemble, need popup sp', _gridId, bagEquipItem.quality)
                return

            _totalWealthVal += bagEquipItem.returnWealthyByDisassemble(owner)
            _succGridIdList.append(_gridId)
            succUniqueIdList.append(uniqueId)

        awardCtx = awardContext.CommonContext(0)
        checkResult = owner.canAddWealthVal(srcType, _totalWealthVal, awardCtx)
        if not checkResult and checkResult.extra != gameconst.BagOPStat.OPERATE_BAG_NO_SPACE:
            LOG_WARN('doBagEquipDisassemble, can not add wealthVal')
            return

        clientData =[]
        consumedItems = []
        for _gridId, uniqueId in zip(_succGridIdList, succUniqueIdList):
            bagEquipItem = self.getItemObjByGridId(_gridId)
            itemNum = bagEquipItem.itemNum
            self.cleanGridByGridId(owner, _gridId, bagEquipItem.itemId, opUUID, srcType, detail, sendClient=False)
            clientData.append({'gridId': _gridId, 'itemNum': 0})
            consumedItems.append({'uniqueId':uniqueId, 'itemId':bagEquipItem.itemId, 'itemNum':itemNum})

        if len(clientData) == 0:
            LOG_WARN('doBagEquipDisassemble, clientData is empty')
            return
        owner.client.onUpdateGridItemsNum(self.bagType, clientData)
        owner.addWealth(srcType, _totalWealthVal, opUUID, detail, awardCtx)

        owner.syncMethodCallToCrossServerBase('_doBagEquipDisassemble', (srcType, _totalWealthVal, opUUID, detail, awardCtx, _succGridIdList, succUniqueIdList))

        LogTrackingMgr.LogTrackingMgr.Item_Disassembly(
            owner.gbID,
            owner.accountEntity.clientDistinctId,
            opUUID,
            owner.gbID,
            gameconst.ItemDisassemblyType.EQUIP,
            consumedItems,
            _totalWealthVal.toBriefList(),
            owner.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY, 0)
        )

    def _doBagEquipDisassemble(self, owner, srcType, _totalWealthVal, opUUID, detail, awardCtx, _succGridIdList, succUniqueIdList):
        clientData =[]
        for _gridId, uniqueId in zip(_succGridIdList, succUniqueIdList):
            bagEquipItem = self.getItemObjByGridId(_gridId)
            itemNum = bagEquipItem.itemNum
            self.cleanGridByGridId(owner, _gridId, bagEquipItem.itemId, opUUID, srcType, detail, sendClient=False)
            clientData.append({'gridId': _gridId, 'itemNum': 0})
        owner.client.onUpdateGridItemsNum(self.bagType, clientData)
        owner.addWealth(srcType, _totalWealthVal, opUUID, detail, awardCtx)

    def getItemObjByItemID(self, itemID, bindType):
        gridID, gridObj = self.getMinGridByItemId(itemID, bindType)
        return gridID, gridObj
