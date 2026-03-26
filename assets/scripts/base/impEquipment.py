# -*- coding: utf-8 -*-
import random

import KBEngine
from KBEDebug import *
import gameconst
import gameglobal
import utils
import formula
import functools
import json
import _pickle as cPickle
import math

import actionContext
import redisUtils
import mailAssistor
import itemFactory
import dataUtils
import awardContext
import dropAward
import gamedecorator
import gametimer
import gameengine
import gameclass
import gameconfig

import message_Message_def as MMD
import gearBase_gearBase as GBGBD
import gearBase_gearConst as GBGCD
import itemData_itemData as ITEM_DATA
import gearManufacture_details as GMDD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

from proto.gameServerDrop_pb2 import DropResult_SUCCESS,\
    DropResult_NOT_FOUND,\
    DropResult_NOT_OWNER,\
    DropResult_EXPIRE,\
    DropResult_OTHER_GIVEUP,\
    DropResult_OTHER_REDEEM

import LogTrackingMgr

class ImpEquipment(object):
    # 需要绑定值
    NEED_BIND_VALUE_METHOD = (
        'bagEquipEnhanceDeductItemsCB',
        'cellEquipEnhance',
        'bagEquipUpgradeDeductItemsCB',
        'cellEquipUpgrade',
        'bagEquipGlyphWashingDeductItemsCB',
        'cellEquipGlyphWashing',
        'bagEquipBlessDeductItemsCB',
        'cellEquipBless'
    )
    # 需要绑定和非绑定值
    NEED_BIND_AND_UNBIND_VALUE_METHOD = (
        'bagEquipSpiritWashingDeductItemsCB',
        'cellEquipSpiritWashing',
    )

    def __init__(self):
        super(ImpEquipment, self).__init__()

    def calculateUpgradeConditions(self, opUUID, box, methodName, args, upgradeType, consumeGridIds, targetLv, itemId, grade):
        totalBindValue = 0
        totalGradeValue = 0
        equipCfgData = GBGBD.datas.get(itemId, None)
        if not equipCfgData:
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
            ERROR_MSG('   in calculateUpgradeConditions, missing equip cfg', itemId)
            return False, None, None
        
        allGrades = [grade]
        for consumeGridId in consumeGridIds:
            consumeBagEquipItem = self.bagData.getItemObjByGridId(consumeGridId)
            if not consumeBagEquipItem:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in calculateUpgradeConditions, wrong arg 1 !', consumeGridId)
                return False, None, None

            if consumeBagEquipItem.itemId != itemId:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in calculateUpgradeConditions, invalid comsume grid item id', consumeGridId, consumeBagEquipItem.itemId, itemId)
                return False, None, None
            
            if upgradeType == gameconst.EquipUpgradeType.SINGLE:
                if consumeBagEquipItem.getGrade() != grade:
                    self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                    ERROR_MSG('   in calculateUpgradeConditions, invalid comsume grid item grade', consumeGridId, consumeBagEquipItem.getGrade(), grade)
                    return False, None, None
            
            if consumeBagEquipItem.isLocked():
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in calculateUpgradeConditions, invalid comsume grid item lock status', consumeGridId, consumeBagEquipItem.getGrade(), grade, consumeBagEquipItem.isLocked())
                return False, None, None
            
            totalBindValue += consumeBagEquipItem.getOriginalBindValue()
            totalGradeValue += math.pow(2, consumeBagEquipItem.getGrade() - 1)
            allGrades.append(consumeBagEquipItem.getGrade())
        # 跨级升阶检测逻辑
        if upgradeType == gameconst.EquipUpgradeType.MULTIPLE:
            # 检查升阶是否合法
            if not dataUtils.checkEquipUpgradeValid(equipCfgData['type'], equipCfgData['quality'], grade, upgradeType, targetLv):
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in calculateUpgradeConditions, invalid item grade', consumeGridId, consumeBagEquipItem.getGrade(), grade)
                return False, None, None
            
            # 计算升级到各阶所需要的资源
            needTotalGrade = 0
            for gradeGap in range(grade, targetLv):
                needTotalGrade += math.pow(2, gradeGap - 1)
            if totalGradeValue != needTotalGrade:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in calculateUpgradeConditions, grade value is invalid', totalGradeValue, needTotalGrade)
                return False, None, None
        # 计算复杂组合情况下的升阶货币消耗    
        equipType = equipCfgData.get('type', 0)
        quality = equipCfgData.get('quality', 0)
        costItems = {}

        changed = True
        while changed:
            changed = False
            n = len(allGrades)
            for i in range(n):
                for j in range(i + 1, n):
                    if allGrades[i] == allGrades[j]:
                        grade = allGrades[i]
                        # 合并它们
                        new_val = allGrades[i] + 1
                        # 删除 j 位置的元素
                        del allGrades[j]
                        # 替换 i 位置的元素
                        allGrades[i] = new_val
                        changed = True
                        dataUtils.calcUpgradeNeedItems(costItems, equipType, quality, grade)
                        break  # 跳出内层循环，重新扫描
                if changed:
                    break

        return True, totalBindValue, costItems

    def baseEquipDeductItems(self, costItemDic, gridNeedItems, gridIdList, gridCountList, opUUID, srcType, detail, box, methodName, args, autoBuy, sendMsg):
        INFO_MSG('in baseEquipDeductItems:', costItemDic, gridNeedItems, gridIdList, gridCountList, opUUID, srcType, detail, methodName, args, autoBuy)
        bindValue = 0
        unbindValue = 0

        if methodName =='bagEquipUpgradeDeductItemsCB':
            consumeGridIds = args.pop(0)
            upgradeType = args[0]
            targetLv = args[1]
            gridId = args[3]
            if gridId in consumeGridIds:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, same grid id!')
                return

            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if not bagEquipItem:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, wrong arg 2 !', gridId)
                return

            ret, bindValue, costItemDic = self.calculateUpgradeConditions(opUUID, box, methodName, args, upgradeType, consumeGridIds, targetLv, bagEquipItem.itemId, bagEquipItem.getGrade())
            if not ret:
                WARNING_MSG(methodName, 'no bag equip upgrade')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                return
            
            if not costItemDic:
                WARNING_MSG(methodName, 'cost item is empty')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                return

        elif methodName == 'cellEquipUpgrade':
            consumeGridIds = args.pop(0)
            itemId = args.pop(0)
            grade = args.pop(0)
            upgradeType = args[0]
            targetLv = args[1] 
            ret, bindValue, costItemDic = self.calculateUpgradeConditions(opUUID, box, methodName, args, upgradeType, consumeGridIds, targetLv, itemId, grade)
            if not ret:
                WARNING_MSG(methodName, 'no body equip upgrade')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                return
            
            if not costItemDic:
                WARNING_MSG(methodName, 'cost item is empty')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                return

        if methodName == 'cellEquipBindValueWashing' or methodName == 'bagEquipBindValueWashingDeductItemsCB':
            needUnbindItemDic = args.pop(0)
            if not needUnbindItemDic:
                WARNING_MSG(methodName, 'no needUnbindItemDic')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                return
            gridNeedItems, _, _ = self.calculateConsumePlanGrids(needUnbindItemDic, gameconst.ItemBindType.NORMAL)
            if not gridNeedItems:
                WARNING_MSG(methodName, 'no gridNeedItems')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                return

        if self.bagData.isLocked():
            WARNING_MSG('   in baseEquipDeductItems, bagData locked!')
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_BAG_LOCKED, 0, 0)
            return
        
        # 额外的格子消耗
        needGridIdList = gridNeedItems
        # 有特殊自选需求的额外格子消耗
        if gridIdList and gridCountList and gridNeedItems:
            ret, needGridIdList, bindValue, unbindValue = self.calculateConsumePlan(gridNeedItems, gridIdList, gridCountList)
            if not ret:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                ERROR_MSG('in baseEquipDeductItems wrong args:', gridNeedItems, gridIdList, gridCountList)
                return

        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costItemDic.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)

        #非自动购买情况下，才需要发送物品不足message
        if self.canDeductWealth(deductWealthVal, not autoBuy):
            # 额外的格子消耗
            if needGridIdList:
                # 二次校验格子是否上锁了
                for needGridId in needGridIdList:
                    needGridItem = self.bagData.getItemObjByGridId(needGridId)
                    if not needGridItem:
                        self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                        ERROR_MSG('   in baseEquipDeductItems, invalid grid id', needGridId)
                        return
                    if needGridItem.isLocked():
                        self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
                        ERROR_MSG('   in baseEquipDeductItems, grid is locked', opUUID)
                        return
                self.bagData.deductItemsByGrid(self, needGridIdList, opUUID, srcType, detail)
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            INFO_MSG('in baseEquipDeductItems ', methodName, args)
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_STAT_OK, bindValue, unbindValue)
            return
        else:
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ARG_ERR, 0, 0)
            ERROR_MSG('   in baseEquipDeductItems, canDeductWealth fail:', opUUID)

        if not autoBuy:
            #不需要自动购买
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.BAG_OP_ITEMS_NOT_ENOUGH, 0, 0)
            return

    def equipMethodCallback(self, opUUID, box, methodName, args, opStat, bindValue, unbindValue):
        if methodName in ImpEquipment.NEED_BIND_VALUE_METHOD:
            args=(bindValue,)+tuple(args)
        elif methodName in ImpEquipment.NEED_BIND_AND_UNBIND_VALUE_METHOD:
            args=(bindValue, unbindValue)+tuple(args)
        box and methodName and getattr(box, methodName)(opStat, *args)

    def addAutoDressEquipItem(self, equipList, opUUID, srcType, taskId, awardCtx):
        INFO_MSG('addAutoDressEquipItem')
        #新手引导使用，装备进背包后自动穿到身上
        if self.bagData.isLocked():
            gameengine.reportCritical('addAutoDressEquipItem, bag locked, try later:', opUUID)
            self._callback(1, 'addAutoDressEquipItem', (equipList, opUUID, srcType, taskId, awardCtx), gametimer.TIMER_TAG_AUTO_DRESS_EQUIP)
            return

        if len(equipList) > self.bagData.leftGridCount:
            gameengine.reportCritical('addAutoDressEquipItem, no space')
            return

        succGridIdList = []
        for it in equipList:
            opStat, gridId = self.bagData.addItemsToNewGrid(self, it, opUUID, srcType, str(taskId), notify=True, syncToClient=False)
            if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
                gameengine.reportCritical('addAutoDressEquipItem, add equip failed:', it.itemId, it.uniqueId)
                return
            succGridIdList.append(gridId)

        for gridId in succGridIdList:
            self.dressEquipment(gridId, gameconst.EQUIP_DRESS_TYPE.OP_AUTO_DRESS, False, 0)
        return

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def dressEquipment(self, exposed, gridId, dressType, dstSlotId):
        INFO_MSG('in dressEquipment:', gridId, dressType, dstSlotId, self.baseSpaceNo)
        self.bagData.doDressEquip(self, gridId, dressType, dstSlotId)

    def dressEquipmentCB(self, uniqId, result, bagEquipDic):
        INFO_MSG('in dressEquipmentCB:', uniqId, result)
        self.bagData.doDressEquipCB(self, uniqId, result)
        if result != gameconst.DressEquipOpStat.EQUIP_OP_FAILED:
            if 'attrJson' in bagEquipDic:
                attrJson = bagEquipDic['attrJson']
                attrDict = json.loads(attrJson)
                enhanceLv = attrDict.get('enhanceLv', 0)

    @gamedecorator.crossServer
    def replaceEquipment(self, uniqId, result, oldBodyEquipDic):
        INFO_MSG('in replaceEquipment:', uniqId, result, self.baseSpaceNo, oldBodyEquipDic)
        self.bagData.doDressEquipCB(self, uniqId, result, oldBodyEquipDic)

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def undressEquipment(self, exposed, slotId):
        INFO_MSG("in undressEquipment:", slotId, self.baseSpaceNo)
        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        if not self.bagData.tryLockBag(lockDesc='undressEquipment, slotId:%s'%(slotId)):
            ERROR_MSG('in undressEquipment, lock bag fail:', self.bagData.lockDesc, slotId)
            return

        self.cell.cellUndressEquipment(slotId)

    def updateAccountCharacterAppearance(self, updateDic):
        self.accountEntity.updateAppearance(self.gbID, updateDic)
        if self.subAccount:
            self.subAccount.updateAppearance(self.gbID, updateDic)

    def cellUndressEquipmentSucc(self, bodyEquipDic):
        INFO_MSG('in cellUndressEquipmentSucc', bodyEquipDic)
        self.unlockBag()
        self.bagData.doBagUndressEquip(self, bodyEquipDic)
    
    def cellUndressEquipmentFail(self, slotId, reason):
        INFO_MSG("cellUndressEquipmentFail::", slotId, reason)
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL, reason)

    def cellBrokenEquipment(self, uniqueId, bodyEquipDic):
        INFO_MSG("cellBrokenEquipment::", uniqueId, bodyEquipDic)
        srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_BODY_EQUIP
        detail = gameclass.AwardDetail(uniqueid=uniqueId, itemid=bodyEquipDic['itemId'])
        LogTrackingMgr.LogTrackingMgr.Get_Item(
            self.accountEntity.accountName,
            self.gbID,
            gameconfig.gameId(),
            bodyEquipDic['itemId'],
            bodyEquipDic['uniqueId'],
            self.bagData.bagType,
            bodyEquipDic['bindType'],
            -1,
            self.getItemNum(bodyEquipDic['itemId']),
            srcType,
            uniqueId,
            str(detail),
        )

    def bagEquipEnhance(self, gridId, uniqueId, gridIdList, gridCountList, autoBuy):
        INFO_MSG('in bagEquipEnhance:', gridId, uniqueId, gridIdList, gridCountList, autoBuy)
        ret, bagEquipItem, costCurrencyDic, costItemDic, _ = self.checkBagEquipEnhanceConditions(gridId, uniqueId)
        if not ret:
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_BAG_EQUIP
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId)
        args = (opUUID, gridId, uniqueId)
        self.baseEquipDeductItems(costCurrencyDic, costItemDic, gridIdList, gridCountList, opUUID, srcType, detail, self,
                                  'bagEquipEnhanceDeductItemsCB', args, autoBuy, True)

    def bagEquipEnhanceDeductItemsCB(self, opStat, bindValue, opUUID, gridId, uniqueId):
        INFO_MSG('in bagEquipEnhanceDeductItemsCB:', opStat, gridId, uniqueId, bindValue)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipEnhanceDeductItemsCB, deduct items error')
            self.client.onEquipEnhanceFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
            return
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        baseAttrsBefore = bagEquipItem.getBaseAttrs()
        enhanceAttrsBefore = bagEquipItem.getEnhanceAttrs()
        upgradeAttrsBefore = bagEquipItem.getUpgradeAttrs()
        addBindValueBefore = bagEquipItem.getAddBindValueStatus()
        levelBefore = bagEquipItem.getEnhanceLevel()
        bindValueBefore = bagEquipItem.getBindValue()
        if bindValue > 0:
            bagEquipItem.updateBindValue()
        
        enhanceVal = bagEquipItem.doEnhanceEquip(self, opUUID, bagEquipItem.getEnhanceLevel())
        bindValueAfter = bagEquipItem.getBindValue()
        # 装备破碎了
        if enhanceVal == gameconst.EquipConstVale.ENHANCEMENT_BROKEN_FLAG:
            srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_BAG_EQUIP
            detail = gameclass.AwardDetail(uniqueid=uniqueId, itemid=bagEquipItem.itemId)
            self.bagData.cleanGridByGridId(self, gridId, bagEquipItem.itemId, opUUID, srcType, detail)
            self.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            LogTrackingMgr.LogTrackingMgr.Equip_Enhancement(opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, baseAttrsBefore, enhanceAttrsBefore, \
                                                            upgradeAttrsBefore, bagEquipItem.getBaseAttrs(), bagEquipItem.getEnhanceAttrs(), bagEquipItem.getUpgradeAttrs(), addBindValueBefore, \
                                                            bagEquipItem.getAddBindValueStatus(), bindValue, levelBefore, bagEquipItem.getEnhanceLevel(), enhanceVal, bagEquipItem.getEquipScore(), bindValueBefore, bindValueAfter)
            self.client.onEquipBroken(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
        else:
            self.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            LogTrackingMgr.LogTrackingMgr.Equip_Enhancement(opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, baseAttrsBefore, enhanceAttrsBefore, \
                                                            upgradeAttrsBefore, bagEquipItem.getBaseAttrs(), bagEquipItem.getEnhanceAttrs(), bagEquipItem.getUpgradeAttrs(), addBindValueBefore, \
                                                            bagEquipItem.getAddBindValueStatus(), bindValue, levelBefore, bagEquipItem.getEnhanceLevel(), enhanceVal, bagEquipItem.getEquipScore(), bindValueBefore, bindValueAfter)
            self.client.onEquipEnhanceSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getEnhanceLevel(), bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType, bagEquipItem.getMaxEnhanceLevel())
        return

    def bagEquipUpgrade(self, upgradeType, gridId, uniqueId, consumeGridIds, targetLv, autoBuy):
        INFO_MSG('in bagEquipUpgrade:', upgradeType, gridId, uniqueId, consumeGridIds, targetLv, autoBuy)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipUpgrade, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipUpgrade, uniqueId not matched:', bagEquipItem.uniqueId, uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipUpgrade, equipment can not be growing, equipment:', bagEquipItem)
            return
        
        if len(consumeGridIds) == 0:
            ERROR_MSG('   in bagEquipUpgrade, args error, consumed grid is empty')
            return
        
        ret = dataUtils.checkEquipmentUpgradeType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('   in bagEquipUpgrade, equipment upgrade is invalid, equipment:', bagEquipItem)
            return

        if not dataUtils.checkEquipUpgradeValid(bagEquipItem.equipAttr.equipType, bagEquipItem.equipAttr.quality, bagEquipItem.getGrade(), upgradeType, targetLv):
            ERROR_MSG('   in bagEquipUpgrade, equipment upgrade is invalid', bagEquipItem.itemId)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_UPGRADE_BAG_EQUIP
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId)
        gridIds = {}
        for consumeGridId in consumeGridIds:
            gridIds[consumeGridId] = 1
        self.baseEquipDeductItems(None, gridIds, None, None, opUUID, srcType, detail, self,
                                  'bagEquipUpgradeDeductItemsCB', [consumeGridIds, upgradeType, targetLv, opUUID, gridId], autoBuy, True)

    def bagEquipUpgradeDeductItemsCB(self, opStat, bindValue, upgradeType, targetLv, opUUID, gridId):
        INFO_MSG('in bagEquipUpgradeDeductItemsCB:', opStat, bindValue, upgradeType, targetLv, opUUID, gridId)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipUpgradeDeductItemsCB, deduct items error')
            self.client.onEquipUpgradeFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)

        baseAttrsBefore = bagEquipItem.getBaseAttrs()
        enhanceAttrsBefore = bagEquipItem.getEnhanceAttrs()
        upgradeAttrsBefore = bagEquipItem.getUpgradeAttrs()
        gradeBefore = bagEquipItem.getGrade()
        bindValueBefore = bagEquipItem.getBindValue()
        bagEquipItem.doUpgradeEquip(self, opUUID, upgradeType, targetLv)
        bagEquipItem.setBindValue(bagEquipItem.getOriginalBindValue() + bindValue)
        bindValueAfter = bagEquipItem.getBindValue()

        LogTrackingMgr.LogTrackingMgr.Equip_Upgrade(opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, baseAttrsBefore, enhanceAttrsBefore, upgradeAttrsBefore, \
                                                    bagEquipItem.getBaseAttrs(), bagEquipItem.getEnhanceAttrs(), bagEquipItem.getUpgradeAttrs(), gradeBefore, bagEquipItem.getGrade(), bindValueBefore, bindValueAfter, \
                                                    bagEquipItem.getEquipScore())

        self.client.onEquipUpgradeSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getGrade(), bagEquipItem.getEquipScore(), bagEquipItem.getOriginalBindValue(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipGlyphWashing(self, gridId, uniqueId, glyphPos, gridIdList, gridCountList):
        INFO_MSG('in bagEquipGlyphWashing:', gridId, uniqueId, glyphPos, gridIdList, gridCountList)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipGlyphWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipGlyphWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('in bagEquipGlyphWashing, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('in bagEquipGlyphWashing, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkGlyphNum(glyphPos):
            ERROR_MSG('in bagEquipGlyphWashing slot is empty')
            return

        costItemDic, costCurrencyDic = bagEquipItem.glyphWashingNeedItems()
        if not costItemDic or not costCurrencyDic:
            ERROR_MSG('     in bagEquipGlyphWashing, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_WEAPON_GLYPH_WASHING
        detail = gameclass.AwardDetail(gridId=gridId, uniqueId=uniqueId)
        args = (opUUID, gridId, glyphPos)
        self.baseEquipDeductItems(costCurrencyDic, costItemDic, gridIdList, gridCountList, opUUID, srcType, detail, self,
                                  'bagEquipGlyphWashingDeductItemsCB', args, False, True)
        return

    def bagEquipGlyphWashingDeductItemsCB(self, opStat, bindValue, opUUID, gridId, glyphPos):
        INFO_MSG('in bagEquipGlyphWashingDeductItemsCB:', opStat, bindValue, opUUID, gridId, glyphPos)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipGlyphWashingDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)

        glyphDataBefore = bagEquipItem.getGlyphDatas()
        addBindValueBefore = bagEquipItem.getAddBindValueStatus()
        bindValueBefore = bagEquipItem.getBindValue()
        if bindValue > 0:
            bagEquipItem.updateBindValue()
        ret, _, _ = bagEquipItem.doEquipGlyphWashing(self, glyphPos)
        bindValueAfter = bagEquipItem.getBindValue()
        if ret:
            glyphData = bagEquipItem.equipAttr.getGlyphData(glyphPos)

            LogTrackingMgr.LogTrackingMgr.Equip_Glyph(opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, glyphDataBefore,\
                                                       bagEquipItem.getGlyphDatas(), addBindValueBefore, bagEquipItem.getAddBindValueStatus(), bindValue, bagEquipItem.getEquipScore(), glyphPos // 2, glyphPos, bindValueBefore, bindValueAfter)
            self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, glyphData.toClientData(), bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipGlyphApply(self, gridId, uniqueId, groupId):
        INFO_MSG('in bagEquipGlyphApply:', gridId, uniqueId, groupId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipGlyphApply, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipGlyphApply, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('in bagEquipGlyphApply, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('in bagEquipGlyphApply, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkGlyphApplyGroupId(groupId):
            ERROR_MSG('in bagEquipGlyphApply groupId is wrong')
            return

        bagEquipItem.doApplyGlyphGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, groupId)
        self.client.onEquipGlyphApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, groupId, bagEquipItem.getEquipScore())
        return

    def bagEquipSpiritApply(self, gridId, uniqueId, groupId):
        INFO_MSG('in bagEquipSpiritApply:', gridId, uniqueId, groupId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipSpiritApply, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipSpiritApply, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('in bagEquipSpiritApply, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentSpiritType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('in bagEquipSpiritApply, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkSpiritApplyGroupId(groupId):
            ERROR_MSG('in bagEquipSpiritApply groupId is wrong')
            return

        bagEquipItem.doApplySpiritGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, groupId)
        self.client.onEquipSpiritApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, groupId, bagEquipItem.getEquipScore())
        return

    def bagEquipBless(self, gridId, uniqueId, gridIdList, gridCountList):
        INFO_MSG('in bagEquipBless:', gridId, uniqueId, gridIdList, gridCountList)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipBless, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('in bagEquipBless, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipBless, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentBlessType(bagEquipItem.equipAttr.equipType, bagEquipItem.getQuality())
        if not ret:
            ERROR_MSG('   in bagEquipBless, equipment can not bless, equipment:', bagEquipItem)
            return False

        costItemDic, costCurrencyDic = bagEquipItem.blessNeedItems()
        if not costItemDic:
            ERROR_MSG('     in bagEquipBless, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_BLESSING
        detail = gameclass.AwardDetail(bodyId=gridId, uniqueId=uniqueId)
        args = (opUUID, gridId, )
        self.baseEquipDeductItems(costCurrencyDic, costItemDic, gridIdList, gridCountList, opUUID, srcType, detail, self, 'bagEquipBlessDeductItemsCB', args,
                                  False, True)
        return

    def bagEquipBlessDeductItemsCB(self, opStat, bindValue, opUUID, gridId):
        INFO_MSG('in bagEquipBlessDeductItemsCB:', opStat, bindValue, opUUID, gridId)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipBlessDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)

        blessDataBefore = bagEquipItem.getBlessDatas()
        blessLvRateBefore = bagEquipItem.getBlessLvRate()
        maxBlessLvBefore = bagEquipItem.getBlessMaxLv()
        addBindValueBefore = bagEquipItem.getAddBindValueStatus()
        bindValueBefore = bagEquipItem.getBindValue()

        if bindValue > 0:
            bagEquipItem.updateBindValue()
        if bagEquipItem.doEquipBlessing(self):

            bindValueAfter = bagEquipItem.getBindValue()
            LogTrackingMgr.LogTrackingMgr.Equip_Bless(opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, blessDataBefore, \
                                                      bagEquipItem.getBlessDatas(), addBindValueBefore, bagEquipItem.getAddBindValueStatus(), bindValue, blessLvRateBefore, \
                                                      bagEquipItem.getBlessLvRate(), maxBlessLvBefore, bagEquipItem.getBlessMaxLv(), bagEquipItem.getEquipScore(), bindValueBefore, bindValueAfter)

            blessAffixes = []
            for oneAffix in bagEquipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, blessAffixes,
                                         bagEquipItem.equipAttr.maxBlessLv, bagEquipItem.equipAttr.blessLvRate,
                                         bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipBackBless(self, gridId, uniqueId):
        INFO_MSG('in bagEquipBackBless:', gridId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('bagEquipBackBless, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('bagEquipBackBless, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        ret = dataUtils.checkEquipmentBlessType(bagEquipItem.equipAttr.equipType, bagEquipItem.getQuality())
        if not ret:
            ERROR_MSG('bagEquipBackBless not bless type')
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('   in bagEquipBackBless, equipment can not be growing, equipment:', bagEquipItem)
            return

        if not bagEquipItem.isCanBackBless():
            ERROR_MSG('bagEquipBackBless not can backBless')
            return

        if bagEquipItem.doEquipBackBless():
            blessAffixes = []
            for oneAffix in bagEquipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBackBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, blessAffixes,
                                             bagEquipItem.equipAttr.maxBlessLv, bagEquipItem.equipAttr.blessLvRate,
                                             bagEquipItem.getEquipScore())

    def bagEquipSpiritWashing(self, gridId, uniqueId, spiritPos, gridIdList, gridCountList):
        INFO_MSG('in bagEquipSpiritWashing:', gridId, uniqueId, spiritPos, gridIdList, gridCountList)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('bagEquipSpiritWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('bagEquipSpiritWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('bagEquipSpiritWashing, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentSpiritType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('bagEquipSpiritWashing, equipment can not affix, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkSpiritNum(spiritPos):
            ERROR_MSG('bagEquipSpiritWashing slot is empty')
            return

        costItemDic, costCurrencyDic = bagEquipItem.spiritWashingNeedItems()
        if not costItemDic or not costCurrencyDic:
            ERROR_MSG('     bagEquipSpiritWashing, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_AFFIX_WASHING
        detail = gameclass.AwardDetail(gridId=gridId, uniqueId=uniqueId)
        self.baseEquipDeductItems(costCurrencyDic, costItemDic, gridIdList, gridCountList, opUUID, srcType, detail, self, 'bagEquipSpiritWashingDeductItemsCB', (opUUID, gridId, spiritPos),
                                  False, True)
        return

    def bagEquipSpiritWashingDeductItemsCB(self, opStat, bindValue, unbindValue, opUUID, gridId, spiritPos):
        INFO_MSG('in bagEquipSpiritWashingDeductItemsCB:', opStat, bindValue, unbindValue, opUUID, gridId, spiritPos)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipSpiritWashingDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        spiritDataBefore = bagEquipItem.getSpiritDatas()
        addBindValueBefore = bagEquipItem.getAddBindValueStatus()
        bindValueBefore = bagEquipItem.getBindValue()
        if bindValue > 0:
            bagEquipItem.updateBindValue()
        ret, _, _ = bagEquipItem.doEquipSpiritWashing(self, spiritPos, unbindValue)
        bindValueAfter = bagEquipItem.getBindValue()
        if ret:
            spiritData = bagEquipItem.equipAttr.spiritDatas[spiritPos]
            self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.EQUIPMENT_WITH_SPIRIT, actionContext.AchievementCtx())
            LogTrackingMgr.LogTrackingMgr.Equip_Spirit(opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, spiritDataBefore,\
                                                       bagEquipItem.getSpiritDatas(), addBindValueBefore, bagEquipItem.getAddBindValueStatus(), bindValue, bagEquipItem.getEquipScore(), \
                                                       spiritPos, bindValueBefore, bindValueAfter)

            self.client.onEquipSpiritWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritData.toClientData(),
                                                 spiritPos, bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipBindWashing(self, gridId, uniqueId, washCount):
        INFO_MSG('in bagEquipBindWashing:', gridId, uniqueId, washCount)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('in bagEquipBindWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('     in bagEquipBindWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return
        if not bagEquipItem.hasBindValue() or bagEquipItem.getBindValue() < washCount:
            ERROR_MSG('     in bagEquipBindWashing, no bind value remain:', bagEquipItem.uniqueId)
            return

        costItemDic, needUnbindItemDic = bagEquipItem.bindValueWashingNeedItems(washCount)
        if not costItemDic or not needUnbindItemDic:
            ERROR_MSG('     in bagEquipBindWashing, cost is empty')
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BINDVALUE_WASHING_BAG_EQUIP
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId)
        args = [needUnbindItemDic, opUUID, gridId, washCount]
        self.baseEquipDeductItems(costItemDic, None, None, None, opUUID, srcType, detail, self, 'bagEquipBindValueWashingDeductItemsCB', args,
                                  False, True)

    def bagEquipBindValueWashingDeductItemsCB(self, opStat, opUUID, gridId, washCount):
        INFO_MSG('in bagEquipBindValueWashingDeductItemsCB:', opStat, gridId, washCount)
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('   in bagEquipBindValueWashingDeductItemsCB, deduct items error')
            self.client.onEquipBindValueWashingFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId)
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)

        addBindValueBefore = bagEquipItem.getAddBindValueStatus()
        bindValueBefore = bagEquipItem.getBindValue()

        bagEquipItem.doDecreaseBindValue(opUUID, washCount)

        LogTrackingMgr.LogTrackingMgr.Equip_BindValue_Washing(opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, bindValueBefore, \
                                                             bagEquipItem.getBindValue(), addBindValueBefore, bagEquipItem.getAddBindValueStatus(), washCount)

        self.client.onEquipBindValueWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getBindValue(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.limitcall(1)
    def reqMultiEquipDisassemble(self, exposed, gridIdList, uniqueIdList):
        INFO_MSG('reqMultiEquipDisassemble:', gridIdList, uniqueIdList)
        self.bagData.doBagEquipDisassemble(self, gridIdList, uniqueIdList)

    def bagEquipSell(self, gridId, uniqueId):
        self.bagData.doBagEquipSell(self, gridId, uniqueId)

    def updateBodyEquipDressData(self, dressDataDic):
        self.baseBodyEquipDressDataDic = dressDataDic

    def canEquipAutoDisassemble(self, owner, equipItem):
        cliConfig = self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY, 0)
        # 自动分解开关
        autoSwitch = utils.hasBit(cliConfig, gameconst.AUTO_DISA_QUALITY_KEY.AUTOS_WITCH)
        if not autoSwitch:
            return False
        isCanTrade = utils.hasBit(cliConfig, gameconst.AUTO_DISA_QUALITY_KEY.TRADE)
        if not isCanTrade and equipItem.bindType != gameconst.ItemBindType.BIND:
            return False

        if not utils.hasBit(cliConfig, equipItem.quality):
            return False

        if equipItem.isPreciousEquip():
            return False
        reqClassList = dataUtils.getEquipItemData(equipItem.itemId)['reqClass']
        myClass = owner.getRoleCacheAttr('school', 0)
        if 0 not in reqClassList and myClass not in reqClassList:
            #自己无法装备，不考虑评分，可以分解
            return True
        slotIds = dataUtils.equipSlot(equipItem.equipAttr.equipType, equipItem.equipAttr.equipSubType)
        for slotId in slotIds:
            bodyEquipScore = self.baseBodyEquipDressDataDic.get(slotId, {}).get('score', 0)
            if equipItem.getEquipScore() > bodyEquipScore:
                return False
        return True

    @gamedecorator.checkGameconfigEnable('equip_make')
    @gamedecorator.limitcall(1)
    def reqMakeEquipment(self, exposed, itemId, gridIdList, gridCountList, makeType):
        INFO_MSG('reqMakeEquipment:', itemId, gridIdList, gridCountList, makeType)
        itemData = dataUtils.getEquipItemData(itemId)
        if not itemData:
            ERROR_MSG('in reqMakeEquipment, gearBase_gearBase not found:', itemId)
            return

        if len(gridIdList) > self.bagData.capacity or len(gridIdList) != len(gridCountList):
            ERROR_MSG('in reqMakeEquipment, wrong args:', itemId)
            return

        school = self.getRoleCacheAttr('school', 0)
        recommendClasses = dataUtils.equipRecommendClass(itemData['type'], itemData['subType'])
        if school not in recommendClasses:
            ERROR_MSG('in reqMakeEquipment, in valid school:', itemId, school, recommendClasses)
            return

        cfgData = GMDD.datas.get(itemId, None)
        if not cfgData:
            ERROR_MSG('in reqMakeEquipment, gearManufacture_details not found:', itemId)
            return

        isOpen = cfgData.get('isOpen')
        if not isOpen:
            ERROR_MSG('in reqMakeEquipment not open:', itemId)
            self.client.onEquipMakeFailed()
            return

        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        if self.bagData.isLocked():
            WARNING_MSG('   in reqMakeEquipment, bagData locked!:', itemId)
            return
        
        consumeItem = None
        if makeType == gameconst.EquipmentManufactureType.MANUFACTURE_LEFT:
            consumeItem = cfgData.get('consumeItem')
            if not consumeItem:
                ERROR_MSG('in reqMakeEquipment missing consumeItem:', itemId, makeType)
                return
        elif makeType == gameconst.EquipmentManufactureType.MANUFACTURE_RIGHT:
            consumeItem = cfgData.get('consumeItem2')
            if not consumeItem:
                ERROR_MSG('in reqMakeEquipment missing consumeItem2:', itemId, makeType)
                return
        else:
            ERROR_MSG('in reqMakeEquipment unknow equipment manufacture type:', itemId, makeType)
            return

        # 收集
        needCostItems = {}
        okCount = 0
        # 先处理配置表的道具消耗数据，防止重复配置错误
        for val in consumeItem:
            costItemId, itemNum = val
            needCostItems[costItemId] = needCostItems.get(costItemId, 0) + itemNum

        ret, needGridIdList, bindValue, _ = self.calculateConsumePlan(needCostItems, gridIdList, gridCountList, True)
        if not ret:
            ERROR_MSG('in reqMakeEquipment wrong args:', itemId, makeType, needGridIdList, needCostItems, okCount)
            self.client.onEquipMakeFailed()
            return
        # 开始扣除道具
        deductVal = dropAward.DeductWealthVal()
        # 扣除消耗的货币
        consumeMoney = cfgData.get('consumeMoney')
        if consumeMoney:
            for val in consumeMoney:
                costItemId, itemNum = val
                deductVal.addWealthByItemId(costItemId, itemNum)
        # 如果消耗的资源为空，不允许制造
        if deductVal.isEmpty():
            ERROR_MSG('in reqMakeEquipment, consume item is empty, equipment manufacture is forbidden:', itemId)
            self.client.onEquipMakeFailed()
            return

        if not self.canDeductWealth(deductVal, sendMsg=True):
            ERROR_MSG('in reqMakeEquipment, canDeductWealth fail:', itemId)
            self.client.onEquipMakeFailed()
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_MANUFACTURE
        detail = gameclass.AwardDetail(itemId=itemId)
        # 扣指定格子指定数量的道具
        self.bagData.deductItemsByGrid(self, needGridIdList, opUUID, srcType, detail)
        # 扣货币
        self.deductWealth(srcType, deductVal, opUUID, detail)
        
        # 获得制造好的道具
        bindType = gameconst.ItemBindType.BIND if bindValue > 0 else gameconst.ItemBindType.NORMAL
        equipItem = itemFactory.ItemFactory.createItem(itemId, 1, bindType=bindType)
        # 设置绑定值
        equipItem.setBindValue(bindValue)
        INFO_MSG('reqMakeEquipment: done', itemId, gridIdList, makeType, bindValue)
        opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem, ], opUUID, srcType, detail, notify=False)
        if opStat == gameconst.BagOPStat.BAG_OP_STAT_OK:
            LogTrackingMgr.LogTrackingMgr.Equip_Make(opUUID, self.gbID, equipItem.uniqueId, equipItem.itemId, 1, equipItem.getGrade(), equipItem.getQuality(), equipItem.getBindValue(), makeType, equipItem.getBaseAttrs(), equipItem.getUpgradeAttrs(), equipItem.getEnhanceAttrs(), equipItem.getEquipScore())
            data = equipItem.toClientEquipItemDict()
            INFO_MSG('in reqMakeEquipment, addItemsWithPlan success:', opStat, data)
            self.client.onEquipMakeSucc(data)
        else:
            ERROR_MSG('in reqMakeEquipment, addItemsWithPlan fail:', opStat, itemId)
            self.client.onEquipMakeFailed()

        self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.MAKE_EQUIPMENT, actionContext.AchievementCtx())
        
    ################################## gm cmd ###################################
    def gmAddGearbaseEquipItem(self, templateId, bindType=dataUtils.getItemDefaultBindType(), grade = 1):
        INFO_MSG('gmAddGearbaseEquipItem:', templateId)
        equipItem = itemFactory.ItemFactory.createItem(templateId, 1, bindType=bindType, grade = grade)
        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_GM
        detail = gameclass.AwardDetail(templateId=templateId)

        opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem, ], opUUID, src, detail)
        return opStat


    def gmBaseDressEquips(self, bodyDressSlotIds, quality):
        INFO_MSG("gmBaseDressEquips ", bodyDressSlotIds, quality)
        myLevel = gameglobal.roleCache[self.id]['level']
        myClass = gameglobal.roleCache[self.id]['school']
        for gridId, it in self.bagData.gridId2GridObj.items():
            if not it.isEquipmentItem():
                continue

            if quality >= 0:
                if it.quality != quality:
                    continue

            gearData = dataUtils.getEquipItemData(it.itemId)
            reqClassList = gearData.get('reqClass', [])
            if 0 not in reqClassList and myClass not in reqClassList:
                continue

            equipLevel = gearData['equipLevel']
            if equipLevel > myLevel:
                continue

            slotIds = dataUtils.equipSlot(it.equipAttr.equipType, it.equipAttr.equipSubType)
            for slotId in slotIds:
                if slotId in bodyDressSlotIds:
                    bodyDressSlotIds.remove(slotId)
                    self._callback(0.2, 'gmSendDressEquips', (gridId, slotId, it), gametimer.TIMER_TAG_GM_SEND_DRESS_EQUIPS)
                    break

            if len(bodyDressSlotIds) == 0:
                break
        return

    def gmSendDressEquips(self, gridId, slotId, equipItem):
        INFO_MSG("gmSendDressEquips ", gridId, slotId, equipItem)
        self.unlockBag()
        self.bagData.doDressEquip(self, gridId, 0, slotId)

    def gmGlyphWashingEquips(self, itemId, glyphPos, affixId1, affixId2):
        gridIds = self.bagData.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
                ERROR_MSG('in gmGlyphWashingEquips, equipment can not be growing, equipment:', bagEquipItem)
                return

            ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('in gmGlyphWashingEquips, equipment can not glyph, equipment:', bagEquipItem)
                return False

            if not bagEquipItem.checkGlyphNum(glyphPos):
                ERROR_MSG('in gmGlyphWashingEquips slot is empty')
                return

            ret, _, _ = bagEquipItem.doEquipGlyphWashing(self, glyphPos, affixIds=[affixId1, affixId2])
            if ret:
                glyphData = bagEquipItem.equipAttr.getGlyphData(glyphPos)
                self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, glyphData.toClientData(), bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return
################################## gm cmd end ###################################

    ################################### drop equip start ##############################
    def onDropEquipBase(self, uniqueId, price, mapId, pos, equipInfo, collEndTime, killerName, endTime, extraBlob, collectionId):
        _blob = cPickle.dumps(equipInfo)
        gameengine.getGlobalBase('DropStub').dropEquipItem(
            self.gbID,
            uniqueId,
            self,
            _blob,
            extraBlob,
            collEndTime,
            endTime,
            price,
            self.serverId,
            collectionId,
        )

        self.equipDropData.addNewDrop(
            self,
            uniqueId,
            price,
            mapId,
            pos,
            equipInfo,
            collEndTime,
            killerName,
            endTime,
            gameconst.DropType.TYPE_DROP,
            True,
        )

        _reachNum = self.equipDropData.dropNum() - GBGCD.datas['equipRepairListMaxNum']['value']
        if _reachNum > 0:
            _val = self.equipDropData.fetchNeedRemoveDropEquip()
            INFO_MSG('Drop onDropEquipBase _reachNum', self.equipDropData.dropNum(), _reachNum, _val)
            if _val:
                self.removeDropEquip(_val.uniqueId, _reachNum)

    def addNotifyDropFixTimer(self, uniqueId, endTime):
        self.equipDropData.addNotifyDropFixTimer(uniqueId, endTime)

    # 检测捡装备
    def checkPickDropEquip(self, uniqueId):
        if self.pickDropEquipLockTime > utils.getNow():
            return False

        return self.equipDropData.checkCouldTakeDrop(uniqueId)

    # 自己捡起来或者赎回会走到这里
    def onGetBackDropEquip(self, uniqueId, equipInfo, isSelfTake):
        equipInfo = cPickle.loads(equipInfo)
        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)
        _fixEndTime = utils.getNow() + GBGCD.datas['equipRepairTime']['value']
        equipItem.setDropFixEndTime(_fixEndTime)

        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByObjList([equipItem])
        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_TAKE_BACK_DROP_EQUIP
        _detail = gameclass.AwardDetail()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
        )

        if isSelfTake:
            self.onMessagePre(
                GBGCD.datas['equipPickUp_msgID']['value'],
                [str(equipItem.itemId)])

            self.cell.logPickDropEquip(
                equipItem.uniqueId,
                equipItem.itemId,
                equipItem.getQuality(),
                equipItem.getGrade(),
            )

        else:
            _args = [
                str(equipItem.itemId),
                str(GBGCD.datas['equipRepairTime']['value']),
            ]
            self.onMessagePre(GBGCD.datas['equipRepairing_msgId']['value'], _args)

        self.addNotifyDropFixTimer(equipItem.uniqueId, _fixEndTime)

    def removeDropEquip(self, uniqueId, times):
        if not self.equipDropData.tryLock():
            WARNING_MSG('removeDropEquip lock failed:', uniqueId)
            return

        if not self.equipDropData.hasDrop(uniqueId):
            ERROR_MSG('removeDropEquip not found drop:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').removeDropEquip(self.gbID, uniqueId, times, self)

    def _sendDestroyMail(self, itemId):
        _mailId = GBGCD.datas['equipDestroyedMailID']['value']
        _args = [
            str(itemId),
        ]
        mailAssistor.sendMailToPlayers(
            [self.gbID],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args,
            srcType=AAC_AACDD.datas.BONUS_SRC_EQUIPMENT_DROP_REMOVE
        )

    def onRemoveDropEquip(self, uniqueId, result, times, collectionId):
        INFO_MSG('onRemoveDropEquip:', uniqueId, result, times)
        self.equipDropData.unlock()

        if result == DropResult_SUCCESS:
            _dropVal = self.equipDropData.removeDrop(self, uniqueId)
            if _dropVal:
                _item = _dropVal.equipItem()
                self._sendDestroyMail(_item.itemId)

                if utils.getNow() < _dropVal.collEndTime:
                    gameengine.callCellApps('removeEquipDropDestroyCollection', (collectionId, _dropVal.uniqueId))

                self.onMessagePre(
                    GBGCD.datas['equipDestroyedForPick_msgID']['value'],
                    [str(_item.itemId)])
        else:
            ERROR_MSG('onRemoveDropEquip fail:', uniqueId, result, times)

        times -= 1

        if times > 0 and self.equipDropData.dropNum() > GBGCD.datas['equipRepairListMaxNum']['value']:
            _val = self.equipDropData.fetchNeedRemoveDropEquip()
            if _val:
                self.removeDropEquip(_val.uniqueId, times)

    def onTakeDropEquipFailed(self, uniqueId, result):
        INFO_MSG('onTakeDropEquipFailed:', uniqueId, result)
        self.pickDropEquipLockTime = 0

    # 捡别人的装备成功的回调
    def onTakeDropEquipSuccess(self, dropGbId, uniqueId, equipInfo, endTime, price):
        INFO_MSG('onTakeDropEquipSuccess:', dropGbId, uniqueId)
        self.pickDropEquipLockTime = 0

        if dropGbId == self.gbID:
            self.equipDropData.removeDrop(self, uniqueId)
            return

        equipInfo = cPickle.loads(equipInfo)
        self.equipDropData.addTaker(
            self,
            uniqueId,
            equipInfo,
            endTime,
            gameconst.DropType.TYPE_TAKE,
            int(price * GBGCD.datas['equipRepairRatioForPicker']['value']),
            True,
        )

        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)

        _mailId = GBGCD.datas['equipNeedRepairMailID']['value']
        _args = [
            str(equipItem.itemId),
            str(equipItem.uniqueId),
            str(endTime)
        ]
        mailAssistor.sendMailToPlayers(
            [dropGbId],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args,
            srcType=AAC_AACDD.datas.BONUS_SRC_EQUIPMENT_TAKE_OK
        )

        self.onMessagePre(
            GBGCD.datas['pickOthersDropEquip_msgID']['value'],
            [str(equipItem.itemId)])

        _posInfo = self.popTempMiscProp(gameconst.AvatarProps.takeDropInfo, None)
        if _posInfo is None:
            ERROR_MSG('onGetBackDropEquip not found temp misc prop:', uniqueId)
            return

        _spaceNo, _pos = _posInfo
        LogTrackingMgr.LogTrackingMgr.Drop_Equip(
            self.gbID,
            equipItem.uniqueId,
            equipItem.itemId,
            equipItem.getQuality(),
            equipItem.getGrade(),
            formula.getMapId(_spaceNo),
            str(_pos),
            gameconst.EQUIP_OPR_PICK,
        )

    @gamedecorator.checkGameconfigEnable('equip')
    def giveUpDropEquip(self, exposed, uniqueId):
        INFO_MSG('giveUpDropEquip:', uniqueId)
        if not self.equipDropData.hasTakeDrop(uniqueId):
            ERROR_MSG('giveUpDropEquip not found take:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').giveUpDropEquip(self.gbID, uniqueId, self)

    @gamedecorator.checkGameconfigEnable('equip')
    def redeemEquipDrop(self, exposed, uniqueId):
        INFO_MSG('redeemEquipDrop:', uniqueId)
        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if not _dropVal:
            ERROR_MSG('redeemEquipDrop not found drop:', uniqueId)
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(
            GBGCD.datas['equipRepairCostItemID']['value'],
            _dropVal.price,
        )

        if not self.canDeductWealth(_deductVal, sendMsg=True):
            WARNING_MSG('       in doUnlockGrids, items not enough:', _deductVal)
            return

        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_EQUIP_DROP
        _detail = gameclass.AwardDetail()
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        gameengine.getGlobalBase('DropStub').doRedeemEquipDrop(self.gbID, uniqueId, self)

    def onRedeemResult(self, uniqueId, result):
        INFO_MSG('onRedeemResult:', uniqueId, result)
        if result == DropResult_SUCCESS:
            self.equipDropData.removeDrop(self, uniqueId)
            return
        elif result == DropResult_NOT_FOUND:
            WARNING_MSG('onRedeemResult not found drop:', uniqueId)
            self.equipDropData.removeTaker(self, uniqueId)
        elif result == DropResult_EXPIRE:
            WARNING_MSG('onRedeemResult expire:', uniqueId)
            self.equipDropData.removeTaker(self, uniqueId)
        elif result == DropResult_OTHER_GIVEUP:
            self._fetchOtherGiveUpEquip(uniqueId)
        else:
            ERROR_MSG('onRedeemResult unknown:', uniqueId, result)

        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if not _dropVal:
            ERROR_MSG('onRedeemResult not found drop:', uniqueId)
            return

        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByItemId(
            GBGCD.datas['equipRepairCostItemID']['value'],
            _dropVal.price,
        )
        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_EQUIP_DROP
        _detail = gameclass.AwardDetail()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
        )

    # 别人赎回后，你领取奖励
    def _getTakeReward(self, uniqueId):
        gameengine.getGlobalBase('DropStub').doGetTakeReward(self.gbID, uniqueId, self)

    def onGetDropTakeReward(self, uniqueId, price):
        INFO_MSG('onGetDropTakeReward:', uniqueId, price)
        _takerVal = self.equipDropData.removeTaker(self, uniqueId, isNotify=False)
        if not _takerVal:
            ERROR_MSG('onGetDropTakeReward not found taker:', uniqueId)
            return

        self.equipDropData.addTakerWait(uniqueId, _takerVal.equip, _takerVal.endTime, _takerVal.price)
        self.client.onEquipDropStateChange(uniqueId, gameconst.DropType.TYPE_REDEEM)

    @gamedecorator.checkGameconfigEnable('equip')
    def getTakerWaitReward(self, exposed, uniqueId):
        _takerVal = self.equipDropData.removeTakerWait(self, uniqueId)
        if not _takerVal:
            ERROR_MSG('getTakerWaitReward not found takerWait:', uniqueId)
            return

        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByItemId(
            GBGCD.datas['equipRepairCostItemID']['value'],
            _takerVal.price,
        )
        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_FOR_PICKER
        _detail = gameclass.AwardDetail()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
        )

    def _fetchOtherGiveUpEquip(self, uniqueId):
        INFO_MSG('_fetchOtherGiveUpEquip:', uniqueId)
        gameengine.getGlobalBase('DropStub').doFetchOtherGiveUpEquip(self.gbID, uniqueId, self)

    def onDropTypeChangeToAvatar(self, uniqueId, dropType):
        INFO_MSG('onDropTypeChangeToAvatar:', uniqueId, dropType)
        if dropType == gameconst.DropType.TYPE_REDEEM:
            _takerVal = self.equipDropData.getTakerVal(uniqueId)
            if _takerVal:
                self._getTakeReward(uniqueId)

        elif dropType == gameconst.DropType.TYPE_GIVEUP:
            _dropVal = self.equipDropData.getDropVal(uniqueId)
            if _dropVal:
                self._fetchOtherGiveUpEquip(uniqueId)

        elif dropType == gameconst.DropType.TYPE_TAKE:
            self.equipDropData.onDropTypeChange(uniqueId, dropType)

        self.client.onEquipDropStateChange(uniqueId, dropType)

    # 别人放弃了你捡起来的装备会走到这里
    def onFetchOtherGiveUpEquip(self, uniqueId, equipInfo, result, giveUpTime):
        INFO_MSG('onFetchOtherGiveUpEquip:', uniqueId, equipInfo, result, giveUpTime)
        if result == DropResult_SUCCESS:
            self.equipDropData.removeDrop(self, uniqueId)

            equipInfo = cPickle.loads(equipInfo)
            equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)
            _fixEndTime = giveUpTime + GBGCD.datas['equipRepairTime']['value']
            equipItem.setDropFixEndTime(_fixEndTime)

            _awardVal = dropAward.AwardVal()
            _awardVal.addWealthByObjList([equipItem])
            _opUUID = KBEngine.genUUID64()
            _src = AAC_AACDD.datas.BONUS_SRC_FETCH_OTHER_GIVEUP_DROP
            _detail = gameclass.AwardDetail()

            self.addWealth(
                _src,
                _awardVal,
                _opUUID,
                _detail,
                awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
            )

            _msgId = GBGCD.datas['returnAndStartRepair_msgID']['value']
            _args = [
                str(equipItem.itemId),
                str(GBGCD.datas['equipRepairTime']['value'])
            ]

            self.onMessagePre(_msgId, _args)

            _mailId = GBGCD.datas['returnAndStartRepairMailID']['value']
            _args = [
                str(equipItem.itemId),
                str(equipItem.uniqueId),
            ]
            mailAssistor.sendMailToPlayers(
                [self.gbID],
                _mailId,
                opUUID=KBEngine.genUUID64(),
                despArgs=_args,
                srcType=_src
            )

            self.addNotifyDropFixTimer(equipItem.uniqueId, _fixEndTime)
            return

        if result == DropResult_NOT_FOUND or\
                result == DropResult_NOT_OWNER or\
                result == DropResult_EXPIRE:

            ERROR_MSG('onFetchOtherGiveUpEquip not found:', uniqueId, result)
            self.equipDropData.removeDrop(self, uniqueId)

    def _doGetAllDropEquipStatus(self):
        _dropList = self.equipDropData.getDropList()

        for _uniqueId in _dropList:
            self._fetchOtherGiveUpEquip(_uniqueId)
            yield lambda: True

        _takerList = self.equipDropData.getTakeList()
        for _uniqueId in _takerList:
            self._getTakeReward(_uniqueId)
            yield lambda: True

    def _initGetAllDropEquipStatus(self):
        gameengine.getGlobalBase('DropStub').doGetDropInfo(self.gbID, self)

    def onGetDropInfo(self, dropInfo, takerInfo):
        INFO_MSG('onGetDropInfo:', dropInfo, takerInfo)
        for _uniqueId, _equipInfo, _endTime, _dropType, _extraInfo, _collExpireTime, _price in dropInfo:
            self.equipDropData.addNewDrop(
                self,
                _uniqueId,
                _price,
                _extraInfo['m'],
                _extraInfo['p'],
                _equipInfo,
                _collExpireTime,
                _extraInfo['n'],
                _endTime,
                _dropType,
                False,
            )

            if _dropType == gameconst.DropType.TYPE_GIVEUP:
                self._fetchOtherGiveUpEquip(_uniqueId)

        for _uniqueId, _equipInfo, _endTime, _dropType, _price in takerInfo:
            self.equipDropData.addTaker(
                self,
                _uniqueId,
                _equipInfo,
                _endTime,
                _dropType,
                int(_price * GBGCD.datas['equipRepairRatioForPicker']['value']),
                False,
            )

            if _dropType == gameconst.DropType.TYPE_REDEEM:
                self._getTakeReward(_uniqueId)

        self.equipDropInitStatus = 1
        self.triggerTempEvent(gameconst.AvatarProps.equipDropInitEvent)

        self._getDropNotifyList()

    def _sendDropEquipInfo(self):
        if not self.equipDropInitStatus:
            self.registerTempEvent(gameconst.AvatarProps.equipDropInitEvent, '_sendDropEquipInfo', ())
            return

        # self.equipDropData.clearEndTimeVals()
        self.client.onInitEquipDropData(self.equipDropData)

    def _initEquipDrop(self):
        self.equipDropInitStatus = 0
        self.createTempEvent(gameconst.AvatarProps.equipDropInitEvent)
        self.pyAddTimer(10, 10, gametimer.DEAL_DROP_EQUIP_EXPIRE)

    @property
    def equipDropInitStatus(self):
        return self.getTempMiscProp(gameconst.AvatarProps.equipDropInitStatus, 1)

    @equipDropInitStatus.setter
    def equipDropInitStatus(self, val):
        if val:
            self.popTempMiscProp(gameconst.AvatarProps.equipDropInitStatus)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.equipDropInitStatus, 0)

    def takeEquipBase(self, uniqueId, spaceNo, position):
        if not self.checkPickDropEquip(uniqueId):
            ERROR_MSG('takeEquipBase not could take drop:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').takeDropEquip(self.gbID, uniqueId, self)
        self.pickDropEquipLockTime = utils.getNow() + 60
        self.setTempMiscProp(gameconst.AvatarProps.takeDropInfo, (spaceNo, position))

    def onGiveUpDropEquip(self, uniqueId, result, dropGbId):
        INFO_MSG('onGiveUpDropEquip:', uniqueId, result, dropGbId)
        if result == DropResult_SUCCESS:
            _takerVal = self.equipDropData.removeTaker(self, uniqueId)
            if _takerVal:
                redisUtils.RedisUtils.getSingleUserInfo(dropGbId, functools.partial(self._onGiveUpGetUserInfo, _takerVal))

        elif result == DropResult_OTHER_REDEEM:
            self._getTakeReward(uniqueId)

    def _onGiveUpGetUserInfo(self, _takerVal, fcVal):
        _item = itemFactory.ItemFactory.createItemWithSavedDict(_takerVal.equip)
        _args = [
            str(_item.itemId),
            fcVal.name
        ]
        _msgId = GBGCD.datas['returnEnergyCrystalSuccess_msgID']['value']

        self.onMessagePre(_msgId, _args)

    def onOtherRemoveDropEquip(self, uniqueId):
        INFO_MSG('onOtherRemoveDropEquip:', uniqueId)
        self.equipDropData.removeTaker(self, uniqueId)

    def _dealDropEquipExpire(self):
        self.equipDropData.doDealDropEquipExpire(self)

        _endTime = utils.getNow()
        # 处理装备修复时间到提示msg
        while True:
            _takerTimerVal = self.equipDropData.firstTimerVal()
            if not _takerTimerVal:
                break

            if _takerTimerVal.endTime > _endTime:
                break

            self.equipDropData.popFirstTimerVal()
            _, equipItem = self.bagData.getItemByUniqueId(_takerTimerVal.uniqueId)
            if equipItem:
                self.onMessagePre(
                    GBGCD.datas['equipRepaired_msgID']['value'],
                    [str(equipItem.itemId)])

    # 自己掉落的装备过期处理
    def _dropExpire(self, uniqueId, itemId):
        self.equipDropData.removeDrop(self, uniqueId)
        self._sendDestroyMail(itemId)

    def _sendPickDestroyMail(self, itemId):
        _mailId = GBGCD.datas['equipDestroyedForPickMailID']['value']
        _args = [
            str(itemId),
        ]
        mailAssistor.sendMailToPlayers(
            [self.gbID],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args,
            srcType=AAC_AACDD.datas.BONUS_SRC_EQUIPMENT_TAKE_EXPIRE
        )

    # 捡起别人的装备过期处理
    def _takerExpire(self, uniqueId, itemId):
        self.equipDropData.removeTaker(self, uniqueId)
        self._sendPickDestroyMail(itemId)

    def onDropEquipExpire(self, uniqueId, result):
        INFO_MSG('onDropEquipExpire:', uniqueId, result)
        if result != DropResult_SUCCESS:
            return

        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if _dropVal:
            self._dropExpire(uniqueId, _dropVal.equipItem().itemId)
            return

        _takerVal = self.equipDropData.getTakerVal(uniqueId)
        if _takerVal:
            self._takerExpire(uniqueId, _takerVal.equipItem().itemId)
            return

    def onAddDropNotify(self):
        INFO_MSG('onAddDropNotify')
        self._getDropNotifyList()

    def _getDropNotifyList(self):
        gameengine.getGlobalBase('DropStub').getDropNotifyList(self.gbID, self)

    def onGetDropNotifyList(self, notifyList):
        INFO_MSG('onGetDropNotifyList:', notifyList)

        for _data in notifyList:
            _notifyType = _data['notifyType']
            _uniqueId = _data['uniqueId']
            _notifyTime = _data['notifyTime']
            _equipInfo = _data['equipInfo']

            _equipInfo = cPickle.loads(_equipInfo)

            if _notifyType == gameconst.DropNotifyType.NOTIFY_DROP_EXPIRE:
                _item = itemFactory.ItemFactory.createItemWithSavedDict(_equipInfo)
                self._dropExpire(_uniqueId, _item.itemId)
            elif _notifyType == gameconst.DropNotifyType.NOTIFY_TAKE_EXPIRE:
                _item = itemFactory.ItemFactory.createItemWithSavedDict(_equipInfo)
                self._takerExpire(_uniqueId, _item.itemId)

    ################################### drop equip end ##############################

    def checkEquipmentCore(self, itemID):
        itemData = ITEM_DATA.datas.get(itemID)
        return itemData and itemData['type'] == 0 and itemData['subType'] == gameconst.ItemSubType.EQUIP_CORE

    def calculateConsumePlan(self, needCostItems, gridIdList, gridCountList, needEquipCore=False):
        if len(gridIdList) != len(gridCountList):
            ERROR_MSG('in calculateConsumePlan wrong args 1:', gridIdList, gridCountList)
            return False, None, 0, 0
        okCount = 0
        bindValue = 0
        unbindValue = 0
        needGridIdList = {}
        # 分析并计算需要消耗的格子上的道具数量
        for i in range(len(gridIdList)):
            gridId = gridIdList[i]
            gridCount = gridCountList[i]
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if not bagEquipItem or bagEquipItem.itemNum < gridCount or bagEquipItem.isLocked():
                ERROR_MSG('in calculateConsumePlan wrong args 2:', bagEquipItem, gridCount)
                return False, None, 0, 0
            bagItemNum = bagEquipItem.itemNum
            # 检查指定格子材料是否足够
            for costItemID, costItemNum in needCostItems.items():
                # 已满足
                if costItemNum <= 0:
                    continue
                if costItemID == bagEquipItem.itemId:
                    if costItemNum > bagItemNum:
                        needCostItems[costItemID] = costItemNum - bagItemNum
                        needGridIdList[gridId] = needGridIdList.get(gridId, 0) + bagItemNum
                        if bagEquipItem.bindType == gameconst.ItemBindType.BIND:
                            if needEquipCore:
                                if self.checkEquipmentCore(bagEquipItem.itemId):
                                    bindValue += bagItemNum
                            else:
                                bindValue += bagItemNum
                        else:
                            unbindValue += bagItemNum
                        bagItemNum = 0
                    else:
                        needCostItems[costItemID] = 0
                        needGridIdList[gridId] = needGridIdList.get(gridId, 0) + costItemNum
                        if bagEquipItem.bindType == gameconst.ItemBindType.BIND:
                            if needEquipCore:
                                if self.checkEquipmentCore(bagEquipItem.itemId):
                                    bindValue += costItemNum
                            else:
                                bindValue += costItemNum
                        else:
                            unbindValue += costItemNum
                        bagItemNum -= costItemNum
                        # 以满足的个数
                        okCount += 1
                # 当前提供材料消耗完毕, 结束检查
                if bagItemNum <= 0:
                    break
            # 消耗全部满足了, 结束计算
            if okCount == len(needCostItems):
                return True, needGridIdList, bindValue, unbindValue
        return False, None, 0, 0

    def calculateConsumePlanGrids(self, itemsDic, bindType, isNormalTypeFirst = False):
        results = {}
        bindInfos = [0, 0]
        consumedItemBindInfos = {}
        for itemId, itemNum in itemsDic.items():
            ret, bindInfo = self.getGridDatasWithConds(itemId, bindType, itemNum, isNormalTypeFirst = isNormalTypeFirst)
            # 出现不满足
            if not ret:
                results = {}
                break
            for k, v in ret.items():
                results[k] = results.get(k, 0) + v
            
            bindInfos[0] += bindInfo[0]
            bindInfos[1] += bindInfo[1]

            bindData = consumedItemBindInfos.get(itemId, None)
            if not bindData:
                bindData = [0, 0]
                consumedItemBindInfos[itemId] = bindData
            bindData[0] += bindInfo[0]
            bindData[1] += bindInfo[1]
        return results, bindInfos, consumedItemBindInfos
    
    def checkBagEquipEnhanceConditions(self, gridId, uniqueId):
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            ERROR_MSG('checkBagEquipEnhanceConditions, gridId is invalid:', gridId)
            return False, None, None, None, False
        
        if bagEquipItem.uniqueId != uniqueId:
            ERROR_MSG('checkBagEquipEnhanceConditions, uniqueId not matched:', bagEquipItem.uniqueId)
            return False, None, None, None, False

        if dataUtils.checkEquipGrowingForbidden(bagEquipItem):
            ERROR_MSG('checkBagEquipEnhanceConditions, equipment can not be growing, equipment:', bagEquipItem)
            return False, None, None, None, False

        ret = dataUtils.checkEquipmentEnhancementType(bagEquipItem.equipAttr.equipType)
        if not ret:
            ERROR_MSG('checkBagEquipEnhanceConditions, equipment enhancement is invalid, equipment:', bagEquipItem)
            return False, None, None, None, False

        if not bagEquipItem.checkEnhancementValid(bagEquipItem.equipAttr.getEnhanceLv() + 1):
            ERROR_MSG('checkBagEquipEnhanceConditions, equipment enhancement is invalid', bagEquipItem.itemId)
            return False, None, None, None, True

        costItemDic, costCurrencyDic = bagEquipItem.enhanceNeedItems()
        if not costItemDic or not costCurrencyDic:
            ERROR_MSG('checkBagEquipEnhanceConditions, cost is empty:', bagEquipItem.equipAttr.getEnhanceLv() + 1)
            return False, None, None, None, False
        return True, bagEquipItem, costCurrencyDic, costItemDic, False
    
    def baseMultiEquipEnhance(self, equipUniqueIds, bagEquipDatas, validBodyItems):
        INFO_MSG('baseMultiEquipEnhance:', equipUniqueIds, bagEquipDatas, validBodyItems)
        if not self.bagData.tryLockBag(lockDesc='baseMultiEquipEnhance'):
            self.cell.unlockBodyEquips()
            self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.BAG_EQUIP_LOCKED, [], [])
            WARNING_MSG('baseMultiEquipEnhance, bag data is locked')
            return
        self.bagData.unLockBag()
        # 有效的背包物品升阶
        validBagItems = {}
        # 批量升阶消耗的物品
        costItem = {}
        # 批量升阶消耗的货币
        costCurrency = {}
        # 背包装备消耗的物品绑定数据
        bagEquipBindInfos = {}
        # 身上装备消耗的物品绑定数据
        bodyEquipBindInfos = {}
        # 身上装备升阶数据
        bodyEquipInfos = []
        # 消耗总的物品信息
        consumedItemInfos = {}
        for gridId, uniqueId in bagEquipDatas.items():
            ret, bagItem, currencyDic, costItemDic, isTopLevel = self.checkBagEquipEnhanceConditions(gridId, uniqueId)
            if not ret:
                if isTopLevel:
                    continue
                self.cell.unlockBodyEquips()
                self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ARG_ERR, [], [])
                WARNING_MSG('baseMultiEquipEnhance, wrong args 1:', gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, uniqueId)
                return
            validBagItems[bagItem.uniqueId] = [gridId, bagItem.getAddBindValueStatus(), currencyDic, costItemDic, bagItem]

            for k, v in currencyDic.items():
                costCurrency[k] = costCurrency.get(k, 0) + v

            for k, v in costItemDic.items():
                costItem[k] = costItem.get(k, 0) + v

        for uniqueId, validBodyItem in validBodyItems.items():
            currencyDic = validBodyItem[2]
            for k, v in currencyDic.items():
                costCurrency[k] = costCurrency.get(k, 0) + v
            
            costItemDic = validBodyItem[3]
            for k, v in costItemDic.items():
                costItem[k] = costItem.get(k, 0) + v

        # 检查物品消耗
        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costCurrency.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)
        for itemId, itemNum in costItem.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)

        if not self.canDeductWealth(deductWealthVal):
            self.cell.unlockBodyEquips()
            self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ITEM_NOT_ENOUGH, [], [])
            WARNING_MSG('baseMultiEquipEnhance, item is not enough')
            return
        
        opUUID = KBEngine.genUUID64()
        for equipUniqueId in equipUniqueIds:
            srcType = AAC_AACDD.datas.BONUS_SRC_AUTO_ENHANCE_BAG_EQUIP
            itemData = validBagItems.get(equipUniqueId, None)
            if not itemData:
                itemData = validBodyItems.get(equipUniqueId, None)
                srcType = AAC_AACDD.datas.BONUS_SRC_AUTO_ENHANCE_BODY_EQUIP
            if not itemData:
                self.cell.unlockBodyEquips()
                self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ARG_ERR, [], [])
                WARNING_MSG('baseMultiEquipEnhance, arg is wrong', equipUniqueId)
                return
            isAddBindStatus = itemData[1]
            costCurrencyDic = itemData[2]
            costItemDic = itemData[3]
            # 计算消耗的格子
            gridNeedItems, bindInfos, consumedItemBindInfo = self.calculateConsumePlanGrids(costItemDic, gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED, isNormalTypeFirst=isAddBindStatus)
            if not gridNeedItems:
                WARNING_MSG('baseMultiEquipEnhance, not enough', costItem, isAddBindStatus)
                break
            # 记录实际消耗
            for itemId, bindData in consumedItemBindInfo.items():
                bindInfo = consumedItemInfos.get(itemId, None)
                if not bindInfo:
                    bindInfo = [0, 0]
                    consumedItemInfos[itemId] = bindInfo
                bindInfo[0] += bindData[0]
                bindInfo[1] += bindData[1]

            for k, v in costCurrencyDic.items():
                bindInfo = consumedItemInfos.get(k, None)
                if not bindInfo:
                    bindInfo = [0, 0]
                    consumedItemInfos[k] = bindInfo
                bindInfo[0] += v

            if srcType == AAC_AACDD.datas.BONUS_SRC_AUTO_ENHANCE_BAG_EQUIP:
                bagEquipBindInfos[equipUniqueId] = bindInfos
            elif srcType == AAC_AACDD.datas.BONUS_SRC_AUTO_ENHANCE_BODY_EQUIP:
                bodyEquipBindInfos[equipUniqueId] = bindInfos
                bodyEquipInfos.append([itemData[0], equipUniqueId])
                
            detail = gameclass.AwardDetail(uniqueId=equipUniqueId, gridNeedItems=gridNeedItems, costItemDic=costItemDic, costCurrencyDic=costCurrencyDic)
            self.bagData.deductItemsByGrid(self, gridNeedItems, opUUID, srcType, detail)

            deductWealthVal = dropAward.DeductWealthVal()
            for itemId, itemNum in costCurrencyDic.items():
                deductWealthVal.addWealthByItemId(itemId, itemNum)

            self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        # 升阶背包装备
        enhanceResults = []
        for uniqueId, bindInfos in bagEquipBindInfos.items():
            datas = validBagItems.get(uniqueId, None)
            if not datas:
                WARNING_MSG('baseMultiEquipEnhance, no bag equip item', uniqueId, bindInfos)
                continue
            gridId = datas[0]
            bagEquipItem = datas[4]
            baseAttrsBefore = bagEquipItem.getBaseAttrs()
            enhanceAttrsBefore = bagEquipItem.getEnhanceAttrs()
            upgradeAttrsBefore = bagEquipItem.getUpgradeAttrs()
            addBindValueBefore = bagEquipItem.getAddBindValueStatus()
            levelBefore = bagEquipItem.getEnhanceLevel()
            bindValueBefore = bagEquipItem.getBindValue()

            bindValue = bindInfos[0]
            if bindValue > 0:
                bagEquipItem.updateBindValue()
            
            enhanceVal = bagEquipItem.doEnhanceEquip(self, opUUID, bagEquipItem.getEnhanceLevel())
            bindValueAfter = bagEquipItem.getBindValue()
            # 装备破碎了
            if enhanceVal == gameconst.EquipConstVale.ENHANCEMENT_BROKEN_FLAG:
                detail = gameclass.AwardDetail(uniqueid=uniqueId, itemid=bagEquipItem.itemId)
                self.bagData.cleanGridByGridId(self, gridId, bagEquipItem.itemId, opUUID, srcType, detail)
                
            LogTrackingMgr.LogTrackingMgr.Equip_Enhancement(opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, baseAttrsBefore, enhanceAttrsBefore, \
                                                            upgradeAttrsBefore, bagEquipItem.getBaseAttrs(), bagEquipItem.getEnhanceAttrs(), bagEquipItem.getUpgradeAttrs(), addBindValueBefore, \
                                                            bagEquipItem.getAddBindValueStatus(), bindValue, levelBefore, bagEquipItem.getEnhanceLevel(), enhanceVal, bagEquipItem.getEquipScore(), bindValueBefore, bindValueAfter)
            self.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            enhanceResults.append([gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, enhanceVal, bagEquipItem.itemId, bagEquipItem.uniqueId, bagEquipItem.getEnhanceLevel(), bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType, bagEquipItem.getMaxEnhanceLevel()])        
        self.cell.cellMultiEquipEnhance(opUUID, bodyEquipInfos, bodyEquipBindInfos, enhanceResults, consumedItemInfos)