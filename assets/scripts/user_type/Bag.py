# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine
import bagData_commonBagCapacity as BagCommCapData
import gameglobal
import utils
import bagData_set as BagDataSet
import gamelog
import dataUtils
import copy

import message_Message_def as MMD

import itemFactory


import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemData as ITEM_DATA
import const_const as CONST
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
import gametlog
import gameclass
import itemActions


class Bag(BaseBag.BaseBag):

    def __init__(self, bagType=0, capacity=BagDataSet.datas['initCommonBagCapacity']['value']):
        super(Bag, self).__init__(capacity)
        self.bagType = bagType
        self.itemsCDDic = {}
        self.groupCDDic = {}
        self.dailyUseLimitDic = {}
        self.item2timer = {}

    def _lateReload(self):
        super(Bag, self)._lateReload()
        return

    def doBagDailyUpdate(self, owner):
        self.dailyUseLimitDic = {}
        updateGridIds = []
        for gridId, itemObj in self.gridId2GridObj.items():
            if itemObj.onItemDailyUpdate():
                updateGridIds.append(gridId)
        updateGridIds and owner.client.onBagItemsDailyUpdate(updateGridIds)
        return

    @classmethod
    def _checkIgnores_(cls):
        return 'itemsCDDic', 'groupCDDic', 'item2timer', 'lockedTime', 'lockDesc'

    def initFromDict(self, savedDataDict):
        super(Bag, self).initFromDict(savedDataDict)

        self.itemsCDDic = {}
        self.groupCDDic = {}
        self.dailyUseLimitDic = {}

        for cdDic in savedDataDict.get('itemCDList', []):
            self.itemsCDDic[cdDic['itemId']] = cdDic['cdTime']

        for cdDic in savedDataDict.get('groupCDList', []):
            self.groupCDDic[cdDic['groupId']] = cdDic['cdTime']

        for useLimitData in savedDataDict.get('useItemsLimitList', []):
            self.dailyUseLimitDic[useLimitData['itemId']] = useLimitData['useNum']

    def toBagSavedDict(self):
        data = super(Bag, self).toBagSavedDict()
        now = utils.getNow()
        itemCDList = [{'itemId': itemId, 'cdTime': cdTime} for itemId, cdTime in self.itemsCDDic.items() if
                      cdTime > now]
        groupCDList = [{'groupId': groupId, 'cdTime': cdTime} for groupId, cdTime in self.groupCDDic.items() if
                       cdTime > now]
        useItemsLimitList = [{'itemId': itemId, 'useNum': useNum} for itemId, useNum in self.dailyUseLimitDic.items()]

        bagData = {
            'itemCDList': itemCDList,
            'groupCDList': groupCDList,
            'useItemsLimitList': useItemsLimitList,
        }
        data.update(bagData)
        return data

    def toBagClientDict(self):
        data = super(Bag, self).toBaseBagClientDict()

        itemCDList = [{'itemId': itemId, 'cdTime': cdTime} for itemId, cdTime in self.itemsCDDic.items()]
        groupCDList = [{'groupId': groupId, 'cdTime': cdTime} for groupId, cdTime in self.groupCDDic.items()]
        useItemsLimitList = [{'itemId': itemId, 'useNum': useNum} for itemId, useNum in self.dailyUseLimitDic.items()]

        bagData = {
            'itemCDList': itemCDList,
            'groupCDList': groupCDList,
            'useItemsLimitList': useItemsLimitList,
        }
        data.update(bagData)
        return data

    def addItemsToNewGrid(self, owner, itemObj, opUUID, src, detail, gridId=None, notify=True, syncToClient=True,
                          srcSubType=0, idipSource=0):
        opStat, gridId = super(Bag, self).addItemsToNewGrid(owner, itemObj, opUUID, src, detail, gridId, notify,
                                                            syncToClient, srcSubType, idipSource)

        if src != AAC_AACDD.datas.BONUS_SRC_BAG_SORT:
            newCount = self.getItemCount(itemObj.itemId, itemObj.bindType)
            # owner.makeItemFlowLog(self.bagType, itemObj, itemObj.itemNum, opUUID, src, newCount, detail)
            itemData = dataUtils.getCommItemData(itemObj.itemId)

        return opStat, gridId

    def addItemsWithPlan(self, owner, itemList, opUUID, src, detail, planDict=None, notify=True, syncToClient=True,
                         srcSubType=0, idipSource=0, directly=True):
        opStat, planDict = super(Bag, self).addItemsWithPlan(owner, itemList, opUUID, src, detail, planDict, notify,
                                                             syncToClient, srcSubType, idipSource)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            return opStat, planDict

        # tmpFish = {}
        tmpItem = {}
        tmpEquipList = []

        for gridId, planItems in planDict['old'].items():
            item = self.getItemObjByGridId(gridId)
            mergeNum = sum([num for _, num in planItems])
            itemData = ITEM_DATA.datas.get(item.itemId, None)
            if not itemData:
                continue

            if item.isEquipmentItem():
                tmpEquipList.append(item)
                continue

            if str(item.itemId) not in tmpItem:
                tmpItem[str(item.itemId)] = 0
            tmpItem[str(item.itemId)] = tmpItem[str(item.itemId)] + mergeNum

            newCount = self.getItemCount(item.itemId, item.bindType)
            owner.makeItemFlowLog(self.bagType, item, mergeNum, opUUID, src, newCount, detail)

        for gridId, planItems in planDict['new'].items():
            item = self.getItemObjByGridId(gridId)
            sumNum = sum([num for _, num in planItems])
            itemData = dataUtils.getCommItemData(item.itemId)
            if not itemData:
                continue

            if item.isEquipmentItem():
                tmpEquipList.append(item)
                continue
            if str(item.itemId) not in tmpItem:
                tmpItem[str(item.itemId)] = 0
            tmpItem[str(item.itemId)] = tmpItem[str(item.itemId)] + sumNum

        extraDesp = dataUtils.getAddItemExtraDesp(src)

        popRewardUUID, itemsDictList, _ = owner.getPopRewardItemsDict(opUUID, detail, notify)

        if notify:
            for itemId, sumNum in tmpItem.items():
                itemsDictList[0][int(itemId)] = itemsDictList[0].get(int(itemId), 0) + sumNum
                '''
                itemData = dataUtils.getCommItemData(itemId)
                itemData['messageTipsID'] and owner.onMessagePre(
                    itemData['messageTipsID'],
                    [str(sumNum), itemId])
                itemData['messageChatID'] and owner.onMessagePre(
                    itemData['messageChatID'],
                    [str(sumNum), itemId, str(0), extraDesp])
                '''

        if notify:
            for item in tmpEquipList:
                itemsDictList[1].append([item.itemId, item.uniqueId])
                '''
                itemData = dataUtils.getCommItemData(item.itemId)
                itemData['messageTipsID'] and owner.onMessagePre(
                    itemData['messageTipsID'],
                    [str(1), str(item.itemId)])
                itemData['messageChatID'] and owner.onMessagePre(
                    itemData['messageChatID'],
                    [str(item.itemId), str(item.uniqueId), extraDesp])
                '''

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
        return opStat, planDict

    # 这里要求外部检查好每个格子有物品且数量足够，否则抛异常
    def deductItemsByGrid(self, owner, grid2ItemNum, opUUID, srcType, detail, sendClient=True):
        itemIdList = []
        deducteItems = []
        for gridId, num in grid2ItemNum.items():
            item = self.getItemObjByGridId(gridId)
            itemIdList.append(item.itemId)
            deducteItems.append((item, num))

        super(Bag, self).deductItemsByGrid(owner, grid2ItemNum, opUUID, srcType, detail, sendClient=sendClient)

        for item, num in deducteItems:
            newCount = self.getItemCount(item.itemId, item.bindType)
            owner.makeItemFlowLog(self.bagType, item, -num, opUUID, srcType, newCount, detail)

        owner.onItemCountChanged(itemIdList)
        return

    def cleanGridByGridId(self, owner, gridId, itemId, opUUID, srcType, detail, sendClient=True, srcSubType=0,
                          idipSource=0):
        oldObj = self.getItemObjByGridId(gridId)
        cleanItem = super(Bag, self).cleanGridByGridId(owner, gridId, itemId, opUUID, srcType, detail, sendClient,
                                                       srcSubType, idipSource)
        if not cleanItem:
            raise Exception('cleanGridByGridId, cleanItem is None, gridId{} itemId {} batTyp:{}'.format(gridId, itemId,
                                                                                                        self.bagType))
        owner.onItemCountChanged([itemId])
        newCount = self.getItemCount(cleanItem.itemId, cleanItem.bindType)
        owner.makeItemFlowLog(self.bagType, cleanItem, -cleanItem.itemNum, opUUID, srcType, newCount, detail)
        if oldObj.uniqueId in self.item2timer:
            tid = self.item2timer.pop(oldObj.uniqueId)
            owner._cancelDatetimeCallback(tid, gametimer.REPLACE_EXPIRED_ITEM)
        return cleanItem

    def deductItemsWithPlan(self, owner, itemsDict, itemsObjs, opUUID, srcType, detail, planDict=None, isCheckLock=True):
        opStat, planDict = super(Bag, self).deductItemsWithPlan(owner, itemsDict, itemsObjs, opUUID, srcType, detail,
                                                                planDict, isCheckLock)

        return opStat, planDict

    def useItemsFailed(self, owner, errCode, itemId=0):
        DEBUG_MSG('useItemsFailed, errCode:', errCode, itemId)
        if errCode == gameconst.BagOPStat.BAG_OP_LEVEL_ERR:
            owner.onMessagePre(MMD.datas.itemLackOfLevel, [])
        elif errCode == gameconst.BagOPStat.BAG_OP_ITEMS_NOT_ENOUGH:
            owner.onMessagePre(MMD.datas.lackOfItem, [str(itemId)])
        elif errCode == gameconst.BagOPStat.BAG_OP_DAILY_LIMIT:
            owner.onMessagePre(MMD.datas.item_dailyUseLimited, [])
        elif errCode == gameconst.BagOPStat.BAG_OP_CD_ERR:
            owner.onMessagePre(MMD.datas.itemInCD, [])
        return

    def _useItemsSucc(self, owner, gridObj, gridId, useNum):
        itemData = dataUtils.getCommItemData(gridObj.itemId)
        if itemData['itemCD'] > 0:
            self._updateItemCD(owner, gridObj.itemId)
        if gridObj.isReUseItem() and gridObj.useTimes > 0:
            owner.client.onUpdateGridItemsJson(gameconst.BagType.BAG_TYPE_NORMAL, gridId, gridObj.uniqueId,
                                               gridObj.attr2Json())
        if 0 != itemData['dailyUseLimit']:
            self.dailyUseLimitDic[gridObj.itemId] = self.dailyUseLimitDic.get(gridObj.itemId, 0) + useNum
            owner.client.onUpdateDailyUseLimit(gridObj.itemId, self.dailyUseLimitDic.get(gridObj.itemId, 0))

        owner.taskCheckCounterTarget(TCCTD.couterTargetDic['TaskCounterTargetUseItem'], (gridObj.itemId, useNum))
        if itemData['type'] == gameconst.ItemType.Normal:
            if itemData['subType'] == gameconst.ItemSubType.HEAL_HP\
                    or itemData['subType'] == gameconst.ItemSubType.HEAL_MP:
                owner.triggerAchievement(gameconst.AchieveType.USE_POTION)

    def useItemSuccSyncToLocalServer(self, owner, uniqueId, itemId, useNum):
        gridId, itemObj = self.getItemByUniqueId(uniqueId)
        if not itemObj:
            return
        newItemNum = itemObj.itemNum - useNum
        if newItemNum <= 0:
            srcType = AAC_AACDD.datas.BONUS_SRC_CROSS_SERVER_USEITEM_SYNC
            detail = gameclass.AwardDetail(uniqueid=uniqueId)
            self.cleanGridByGridId(owner, gridId, itemId, KBEngine.genUUID64(), 0, detail, sendClient=False)
        else:
            itemObj.setItemNum(newItemNum)

    def doUseGridItems(self, owner, gridId, itemId, useNum, useItemCtx, isBaseAct=False):
        DEBUG_MSG('in doUseGridItems:', gridId, itemId)
        gridObj = self.getItemObjByGridId(gridId)
        if not gridObj:
            self.useItemsFailed(owner, gameconst.BagOPStat.BAG_OP_DATA_ERR, itemId)
            return

        useItemCtx.bindType = gridObj.bindType
        itemData = dataUtils.getCommItemData(gridObj.itemId)
        action = itemData['action'] or itemActions.getItemAction(gridObj)
        actionName = action.__name__ if action else ''

        isBaseAction = (isBaseAct or actionName.endswith('_base'))
        if not isBaseAction and not self.tryLockBag(lockDesc='doUseGridItems:%s' % gridId):
            self.useItemsFailed(owner, gameconst.BagOPStat.BAG_OP_BAG_LOCKED, itemId)
            return

        if action:
            # 消耗品
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_FROM_ITEM
            detail = gameclass.AwardDetail(gridId=gridId, itemId=gridObj.itemId, hasNum=gridObj.itemNum, useNum=useNum)
            now = utils.getNow()

            if gridObj.isReUseItem():
                gridObj.useTimes -= useNum

            if itemId not in CONST.datas["eternalItemIDList"]['value'] or (
                    gridObj.isReUseItem() and gridObj.useTimes <= 0):
                # 正常道具使用完就没了；多次使用的道具，使用次数耗尽也就没了
                self.deductItemsByGrid(owner, {gridId: useNum}, opUUID, srcType, detail)
            else:
                # 无消耗道具需要调用通知接口
                owner.client.onUpdateGridItemsNum(self.bagType, [{'gridId': gridId, 'itemNum': gridObj.itemNum}, ])

            dataDic = owner.getTempMiscProp(gameconst.AvatarProps.useBagItemData, None)
            if not dataDic:
                dataDic = {}
                owner.setTempMiscProp(gameconst.AvatarProps.useBagItemData, dataDic)
            dataDic[opUUID] = {'t': now, 'gridId': gridId, 'itemId': gridObj.itemId,
                               'useNum': useNum, 'gridObj': gridObj, 'opUUID': opUUID, 'srcType': srcType}

            # isBaseAct没用起来，新增支持可以按action名字决定在哪里执行
            if isBaseAction:
                # 在base执行的action
                useItemCtx.itemObj = gridObj
                owner.doBaseUseItemAction(action, gridId, itemId, useNum, opUUID, useItemCtx)
                owner.useItemDone(True, opUUID)
            else:
                owner.cell.doAction(gridId, itemId, useNum, opUUID, useItemCtx)
        else:
            self._useItemsSucc(owner, gridObj, gridId, useNum)
            self.unLockBag()

        return True

    def isUseItemsDailyLimit(self, itemId, useNum):
        itemData = dataUtils.getCommItemData(itemId)
        if 0 == itemData['dailyUseLimit']:
            return False
        hasUseNum = self.dailyUseLimitDic.get(itemId, 0)
        return useNum > itemData['dailyUseLimit'] - hasUseNum

    def canUseGridItem(self, owner, gridId, itemId, useNum):
        if self.isUseItemsDailyLimit(itemId, useNum):
            return gameconst.BagOPStat.BAG_OP_DAILY_LIMIT

        gridObj = self.getItemObjByGridId(gridId)
        if not gridObj:
            return gameconst.BagOPStat.BAG_OP_DATA_ERR

        if gridObj.itemId != itemId:
            return gameconst.BagOPStat.BAG_OP_DATA_ERR

        if self.isLocked():
            return gameconst.BagOPStat.BAG_OP_BAG_LOCKED

        # 道具本身被上锁了
        if gridObj.isLocked():
            return gameconst.BagOPStat.BAG_OP_ITEM_LOCKED

        if useNum > gridObj.itemNum:
            return gameconst.BagOPStat.BAG_OP_ITEMS_NOT_ENOUGH

        # check expireTime
        now = utils.getNow()
        if gridObj.isExpired():
            return gameconst.BagOPStat.BAG_OP_ITEM_EXPIRED

        if not gridObj.isEnabled():
            return gameconst.BagOPStat.BAG_OP_ITEM_DISABLED

        if gridObj.isReUseItem() and (useNum != 1 or gridObj.useTimes < useNum):
            WARNING_MSG('canUseGridItem reuse items useTimes failed:', gridObj.itemId, gridObj.useTimes)
            return gameconst.BagOPStat.BAG_OP_REUSE_ITEM_USE_TIMES_FAILED

        # check level
        itemData = dataUtils.getCommItemData(gridObj.itemId)
        myLevel = gameglobal.roleCache.get(owner.id, {}).get('level', 0)
        if myLevel != 0 and myLevel < itemData['levelRequirement']:
            return gameconst.BagOPStat.BAG_OP_LEVEL_ERR

        # check cdtime
        cdtiem = self._getItemCD(gridObj.itemId)
        if now < cdtiem:
            return gameconst.BagOPStat.BAG_OP_CD_ERR

        return gameconst.BagOPStat.BAG_OP_STAT_OK

    def _updateItemCD(self, owner, itemId):
        if self.bagType != gameconst.BagType.BAG_TYPE_NORMAL:
            return
        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            return
        if 0 == itemData['itemCD']:
            return
        cdGroup = itemData['CDGroup']
        newCD = utils.getNow() + itemData['itemCD']
        if 0 == cdGroup:
            self.itemsCDDic[itemId] = newCD
        else:
            self.groupCDDic[cdGroup] = newCD
        owner.client.onUpdateItemCD(itemId, cdGroup, newCD)
        return

    def _getItemCD(self, itemId):
        now = utils.getNow()
        cd = self.itemsCDDic.get(itemId, None)
        if cd is not None:
            if now < cd:
                return cd

        itemData = dataUtils.getCommItemData(itemId)

        cdGroup = itemData['CDGroup']
        groupCD = self.groupCDDic.get(cdGroup, None)
        if groupCD is not None:
            if now < groupCD:
                return groupCD
        return 0

    def onUseItemDone(self, owner, isSucceed, opUUID):
        DEBUG_MSG('onUseItemDone:', isSucceed, opUUID)
        self.unLockBag()
        dataDic = owner.getTempMiscProp(gameconst.AvatarProps.useBagItemData)
        # if not dataDic:
        #     WARNING_MSG('onUseItemDone, no dataDic:', dataDic)
        #     return
        info = dataDic.pop(opUUID)
        gridId = info['gridId']
        itemId = info['itemId']
        bakGridObj = info.get('gridObj', None)

        itemData = dataUtils.getCommItemData(itemId)
        if isSucceed:
            self._useItemsSucc(owner, bakGridObj, gridId, info['useNum'])

        # 返还物品:有action的物品才是消耗型物品
        elif itemId not in CONST.datas["eternalItemIDList"]['value'] and itemData.get('action') or bakGridObj.isReUseItem():
            curGridObj = self.getItemObjByGridId(gridId)
            if curGridObj:
                if curGridObj.itemId != itemId:
                    WARNING_MSG('onUseItemDone, itemId not matched:', curGridObj.uniqueId, opUUID, curGridObj.itemId,
                                itemId)
                    return
                curGridObj.setItemNum(curGridObj.itemNum + info['useNum'])
                owner.client.onUpdateGridItemsNum(self.bagType, [{'gridId': gridId, 'itemNum': curGridObj.itemNum}])
            else:
                bakGridObj.setItemNum(info['useNum'])
                self.addItemsToNewGrid(owner, bakGridObj, info['opUUID'], info['srcType'], 'useItemFailed', gridId)

        addItemIdSet = info.get('addItemIdSet', None)
        if addItemIdSet:
            srcType = info.get('srcType', None)
            detail = gameclass.AwardDetail(addItemIdSet=list(addItemIdSet))
            itemObjList = []
            for itemId in addItemIdSet:
                item = itemFactory.ItemFactory.createItem(itemId, 1,
                                                          dataUtils.getItemDefaultBindType()
                                                          )
                itemObjList.append(item)

            wealthVal = dropAward.AwardVal(itemObjs=itemObjList)
            owner.addWealth(srcType, wealthVal, opUUID, detail,
                            awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID), notify=False)

    @utils.checkBagLocked
    def doUnlockGrids(self, owner, gridNum):
        DEBUG_MSG('in doUnlockGrids', gridNum)
        commonBagCapacity = BagDataSet.datas['commonBagCapacity']['value']
        if self.capacity >= commonBagCapacity:
            WARNING_MSG('   in doUnlockGrids, reach limit:', self.capacity)
            return
        newCapacity = self.capacity + gridNum
        if newCapacity > commonBagCapacity:
            WARNING_MSG('   in doUnlockGrids, reach limit:', newCapacity)
            return
        initGridNum = BagDataSet.datas['initCommonBagCapacity']['value']
        startGrid = self.capacity - initGridNum + 1
        deductWealthVal = dropAward.DeductWealthVal()
        for gridId in range(startGrid, startGrid + gridNum):
            needItemId = BagCommCapData.datas[gridId]['itemNeeded']
            itemNum = BagCommCapData.datas[gridId]['itemNum']
            deductWealthVal.addWealthByItemId(needItemId, itemNum, dataUtils.getItemDefaultBindType())
            DEBUG_MSG('     in doUnlockGrids:', needItemId, itemNum)

        if not owner.canDeductWealth(deductWealthVal, sendMsg=True):
            WARNING_MSG('       in doUnlockGrids, items not enough:', deductWealthVal)
            return
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_UNLOCK_GRIDS
        detail = gameclass.AwardDetail(capacity=self.capacity, newCapacity=newCapacity)
        owner.deductWealth(srcType, deductWealthVal, opUUID, detail)
        self.capacity = newCapacity
        return self.capacity

    def getTaskItems(self, taskId):
        if self.bagType != gameconst.BagType.BAG_TYPE_TASK:
            gameengine.reportCritical('getTaskItems bagType error:', self.bagType)
            return

        return [(gridId, it.itemId) for gridId, it in self.gridId2GridObj.items() if it.taskId == taskId]

    def doDressEquip(self, owner, gridId, dressType, dstSlotId):
        DEBUG_MSG('in doDressEquip, gridId:', gridId, dressType)
        gridObj = self.getItemObjByGridId(gridId)
        if gridObj is None:
            ERROR_MSG('doDressEquip gridObj is None', gridId, dressType, dstSlotId)
            return False

        if not gridObj.isEquipmentItem():
            WARNING_MSG('     in doDressEquip, gridObj is not equipment')
            return False

        if not gridObj.isGood():
            WARNING_MSG('     in doDressEquip, gridObj can not dress')
            return False

        roleInfo = gameglobal.roleCache.get(owner.id, None)
        gearInfo = GBGBD.datas.get(gridObj.itemId)

        reqClassList = gearInfo.get('reqClass', [])
        myClass = roleInfo['school']
        if 0 not in reqClassList and myClass not in reqClassList:
            WARNING_MSG('     in doDressEquip, school not matched:', gearInfo['reqClass'], roleInfo['school'])
            owner.onMessagePre(MMD.datas.equipFail_classNotMatch, [])
            return False

        equipLevel = gearInfo['equipLevel']
        roleLevel = roleInfo['level']
        DEBUG_MSG('     in doDressEquip, level info:', equipLevel, roleLevel)
        if equipLevel > roleInfo['level']:
            WARNING_MSG('     in doDressEquip, level not matched:', equipLevel, roleLevel)
            owner.onMessagePre(GBGCD.datas['equipWearLowRoleLevel']['value'], [])
            return False

        now = utils.getNow()
        if not self.tryLockBag(lockDesc='doDressEquip uniqueId:%s' % gridObj.uniqueId):
            WARNING_MSG('lock bag fail:', self.lockDesc, gridId, gridObj.itemId)
            return False
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_DRESS
        detail = gameclass.AwardDetail(uniqueid=gridObj.uniqueId)
        self.cleanGridByGridId(owner, gridId, gridObj.itemId, opUUID, srcType, detail, sendClient=False)
        tempDataDic = owner.getTempMiscProp(gameconst.AvatarProps.equipDressTempData, None)
        if tempDataDic is None:
            tempDataDic = {}
            owner.setTempMiscProp(gameconst.AvatarProps.equipDressTempData, tempDataDic)
        tempDataDic[opUUID] = {'t':now, 'gridId':gridId, 'opUUID':opUUID, 'gridObj':gridObj, 'dressType':dressType}

        owner.cell.cellDressEquipment(opUUID, gridObj.toItemSavedDict(), dstSlotId)
        return True

    def doDressEquipCB(self, owner, opUUID, result, oldBodyEquipDic=None):
        DEBUG_MSG('in doDressEquipCB:', opUUID, result)
        self.unLockBag()
        tempDataDic = owner.getTempMiscProp(gameconst.AvatarProps.equipDressTempData, {})
        tempData = tempDataDic.pop(opUUID, None)
        if not tempData:
            gameengine.reportCritical('doDressEquipCB, tempData lost:', opUUID, tempDataDic)

        gridId = tempData['gridId']
        gridObj = tempData['gridObj']
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_DRESS
        if result == gameconst.DressEquipOpStat.EQUIP_OP_FAILED:
            detail = gameclass.AwardDetail(uniqueid=gridObj.uniqueId)
            self.addItemsToNewGrid(owner, gridObj, opUUID, srcType, detail, gridId, syncToClient=False)
            return

        owner.client.onUpdateGridItemsNum(self.bagType, [{'gridId': gridId, 'itemNum': 0}])
        if result == gameconst.DressEquipOpStat.EQUIP_OP_ONLY_DRESS:
            pass
        elif result == gameconst.DressEquipOpStat.EQUIP_OP_REPLACED:
            dressType = tempData.get('dressType', gameconst.EQUIP_DRESS_TYPE.OP_NORMAL)
            equipItem = itemFactory.ItemFactory.createItemWithSavedDict(oldBodyEquipDic)
            if dressType == gameconst.EQUIP_DRESS_TYPE.OP_QUICK_DRESS and self.disassembleReplacedEquip(owner, equipItem, opUUID, srcType):
                #快速装备被替换下来的未强化装备要分解掉
                return
            detail = gameclass.AwardDetail(uniqueid=gridObj.uniqueId)
            self.addItemsToNewGrid(owner, equipItem, opUUID, srcType, detail, gridId, syncToClient=True)
        return

    def doBagUndressEquip(self, owner, bodyEquipDic):
        DEBUG_MSG('in doBagUndressEquip')
        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(bodyEquipDic)
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_DRESS
        detail = gameclass.AwardDetail(itemId=equipItem.itemId)
        self.addItemsWithPlan(owner, [equipItem],  opUUID, srcType, detail, notify=False, directly=False)
        return

    @utils.checkBagLocked
    def doBagEquipDisassemble(self, owner, gridIdList, uniqueIdList):
        DEBUG_MSG('in doBagEquipDisassemble:', gridIdList, uniqueIdList)
        # 装备批量分解，背包空间不够，都不能分解成功
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_DISASSEMBLE
        detail = gameclass.AwardDetail(gridList=gridIdList, uniqueList=uniqueIdList)
        totalWealthVal = dropAward.AwardVal()

        succGridIdList = []
        succUniqueIdList = []
        for gridId, uniqueId in zip(gridIdList, uniqueIdList):
            bagEquipItem = self.getItemObjByGridId(gridId)
            if not bagEquipItem:
                WARNING_MSG('     in doBagEquipDisassemble, gridId error:', gridId)
                continue

            if bagEquipItem.uniqueId != uniqueId:
                WARNING_MSG('     in doBagEquipDisassemble, uniqueId not matched:', bagEquipItem.uniqueId)
                continue

            if not bagEquipItem.canBeDisassembled():
                WARNING_MSG('     in doBagEquipDisassemble, cannot be disassembled:', gridId)
                continue
            totalWealthVal += bagEquipItem.returnWealthyByDisassemble(owner)
            succGridIdList.append(gridId)
            succUniqueIdList.append(uniqueId)

        awardCtx = awardContext.CommonContext(0)
        checkResult = owner.canAddWealthVal(srcType, totalWealthVal, awardCtx)
        if not checkResult and checkResult.extra != gameconst.BagOPStat.BAG_OP_NO_SPACE:
            WARNING_MSG('doBagEquipDisassemble, can not add wealthVal')
            return

        clientData =[]
        for gridId, uniqueId in zip(succGridIdList, succUniqueIdList):
            bagEquipItem = self.getItemObjByGridId(gridId)
            bagEquipItem.setItemNum(0)
            self.cleanGridByGridId(owner, gridId, bagEquipItem.itemId, opUUID, srcType, detail, sendClient=False)
            clientData.append({'gridId': gridId, 'itemNum': 0})

            owner.makeEquipmentLostLog(srcType, bagEquipItem.toItemSavedDict())

        if len(clientData) == 0:
            WARNING_MSG('doBagEquipDisassemble, clientData is empty')
            return
        owner.client.onUpdateGridItemsNum(self.bagType, clientData)
        owner.addWealth(srcType, totalWealthVal, opUUID, detail, awardCtx)
        owner.client.onEquipDisassemble(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, succGridIdList, succUniqueIdList)
        return

    def getItemObjByItemID(self, itemID, bindType):
        gridID, gridObj = self.getMinGridByItemId(itemID, bindType)
        return gridID, gridObj
