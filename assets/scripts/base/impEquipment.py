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

import agent_agentConfig as A_ACD
import message_Message_def as MMD
import gearBase_gearBase as GBGBD
import gearBase_gearConst as GBGCD
import itemData_itemData as ITEM_DATA
import gearManufacture_details as GMDD
import agent_agentFunction as A_AFD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import soul_soul as SS_D

from proto.gameServerDrop_pb2 import DropResult_SUCCESS,\
    DropResult_NOT_FOUND,\
    DropResult_NOT_OWNER,\
    DropResult_EXPIRE,\
    DropResult_OTHER_GIVEUP,\
    DropResult_OTHER_REDEEM, \
    DropResult_REDEEM_NOT_SET_PRICE

import LogTrackingMgr

class ImpEquipment(object):
    # 需要绑定值
    NEED_BIND_VALUE_METHOD = (
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
        'bagEquipSoulSocketDeductItemsCB',
    )

    def __init__(self):
        super(ImpEquipment, self).__init__()

    def calculateUpgradeConditions(self, opUUID, box, methodName, args, upgradeType, consumeGridIds, targetLv, itemId, grade):
        totalBindValue = 0
        totalGradeValue = 0
        equipCfgData = GBGBD.datas.get(itemId, None)
        if not equipCfgData:
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
            LOG_ERR('   in calculateUpgradeConditions, missing equip cfg', itemId)
            return False, None, None
        
        allGrades = [grade]
        for consumeGridId in consumeGridIds:
            consumeBagEquipItem = self.bagData.getItemObjByGridId(consumeGridId)
            if not consumeBagEquipItem:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('   in calculateUpgradeConditions, wrong arg 1 !', consumeGridId)
                return False, None, None

            if consumeBagEquipItem.itemId != itemId:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('   in calculateUpgradeConditions, invalid comsume grid item id', consumeGridId, consumeBagEquipItem.itemId, itemId)
                return False, None, None
            
            if upgradeType == gameconst.EquipUpgradeType.SINGLE:
                if consumeBagEquipItem.getGrade() != grade:
                    self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                    LOG_ERR('   in calculateUpgradeConditions, invalid comsume grid item grade', consumeGridId, consumeBagEquipItem.getGrade(), grade)
                    return False, None, None
            
            if consumeBagEquipItem.isLocked():
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('   in calculateUpgradeConditions, invalid comsume grid item lock status', consumeGridId, consumeBagEquipItem.getGrade(), grade, consumeBagEquipItem.isLocked())
                return False, None, None
            
            totalBindValue += consumeBagEquipItem.getOriginalBindValue()
            totalGradeValue += math.pow(2, consumeBagEquipItem.getGrade() - 1)
            allGrades.append(consumeBagEquipItem.getGrade())
        # 跨级升阶检测逻辑
        if upgradeType == gameconst.EquipUpgradeType.MULTIPLE:
            # 检查升阶是否合法
            if not dataUtils.checkEquipUpgradeValid(equipCfgData['type'], equipCfgData['quality'], grade, upgradeType, targetLv):
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('   in calculateUpgradeConditions, invalid item grade', consumeGridId, consumeBagEquipItem.getGrade(), grade)
                return False, None, None
            
            # 计算升级到各阶所需要的资源
            needTotalGrade = 0
            for gradeGap in range(grade, targetLv):
                needTotalGrade += math.pow(2, gradeGap - 1)
            if totalGradeValue != needTotalGrade:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('   in calculateUpgradeConditions, grade value is invalid', totalGradeValue, needTotalGrade)
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
        LOG_INFO('in baseEquipDeductItems:', costItemDic, gridNeedItems, gridIdList, gridCountList, opUUID, srcType, detail, methodName, args, autoBuy)
        bindValue = 0
        unbindValue = 0

        if methodName =='bagEquipUpgradeDeductItemsCB':
            consumeGridIds = args.pop(0)
            upgradeType = args[0]
            targetLv = args[1]
            gridId = args[3]
            if gridId in consumeGridIds:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, same grid id!')
                return

            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if not bagEquipItem:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('   in baseEquipDeductItems, bagEquipUpgradeDeductItemsCB, wrong arg 2 !', gridId)
                return

            ret, bindValue, costItemDic = self.calculateUpgradeConditions(opUUID, box, methodName, args, upgradeType, consumeGridIds, targetLv, bagEquipItem.itemId, bagEquipItem.getGrade())
            if not ret:
                LOG_WARN(methodName, 'no bag equip upgrade')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                return
            
            if not costItemDic:
                LOG_WARN(methodName, 'cost item is empty')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                return

        elif methodName == 'cellEquipUpgrade':
            if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipClassPage, 
                                                A_ACD.datas['restrictedPromptMsg1']['value']):
                return

            consumeGridIds = args.pop(0)
            itemId = args.pop(0)
            grade = args.pop(0)
            upgradeType = args[0]
            targetLv = args[1] 
            ret, bindValue, costItemDic = self.calculateUpgradeConditions(opUUID, box, methodName, args, upgradeType, consumeGridIds, targetLv, itemId, grade)
            if not ret:
                LOG_WARN(methodName, 'no body equip upgrade')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                return
            
            if not costItemDic:
                LOG_WARN(methodName, 'cost item is empty')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                return

        if methodName == 'cellEquipBindValueWashing' or methodName == 'bagEquipBindValueWashingDeductItemsCB':
            needUnbindItemDic = args.pop(0)
            if not needUnbindItemDic:
                LOG_WARN(methodName, 'no needUnbindItemDic')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                return
            gridNeedItems, _, _ = self.calculateConsumePlanGrids(needUnbindItemDic, gameconst.ItemBindType.NORMAL)
            if not gridNeedItems:
                LOG_WARN(methodName, 'no gridNeedItems')
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                return

        if self.bagData.isLocked():
            LOG_WARN('   in baseEquipDeductItems, bagData locked!')
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED, 0, 0)
            return
        
        # 额外的格子消耗
        needGridIdList = gridNeedItems
        # 有特殊自选需求的额外格子消耗
        if gridIdList and gridCountList and gridNeedItems:
            ret, needGridIdList, bindValue, unbindValue = self.calculateConsumePlan(gridNeedItems, gridIdList, gridCountList)
            if not ret:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('in baseEquipDeductItems wrong args:', gridNeedItems, gridIdList, gridCountList)
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
                        self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                        LOG_ERR('   in baseEquipDeductItems, invalid grid id', needGridId)
                        return
                    if needGridItem.isLocked():
                        self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                        LOG_ERR('   in baseEquipDeductItems, grid is locked', opUUID)
                        return
                self.bagData.deductItemsByGrid(self, needGridIdList, opUUID, srcType, detail)
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            LOG_INFO('in baseEquipDeductItems ', methodName, args)
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_STAT_OK, bindValue, unbindValue)
            return
        else:
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
            LOG_ERR('   in baseEquipDeductItems, canDeductWealth fail:', opUUID)

        if not autoBuy:
            #不需要自动购买
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ITEMS_NOT_ENOUGH, 0, 0)
            return

    def equipMethodCallback(self, opUUID, box, methodName, args, opStat, bindValue, unbindValue):
        if methodName in ImpEquipment.NEED_BIND_VALUE_METHOD:
            args=(bindValue,)+tuple(args)
        elif methodName in ImpEquipment.NEED_BIND_AND_UNBIND_VALUE_METHOD:
            args=(bindValue, unbindValue)+tuple(args)
        box and methodName and getattr(box, methodName)(opStat, *args)
    
    def baseEquipDeductItemsWithBindTypes(self, costCurrencies, costItems, itemIds, bindTypes, opUUID, srcType, detail, box, methodName, args):
        LOG_INFO('in baseEquipDeductItemsWithBindTypes:', costCurrencies, costItems, itemIds, bindTypes, opUUID, srcType, detail, box, methodName, args)
        if 'cellEquipGlyphWashing' == methodName:
            if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipRunePage, 
                                                A_ACD.datas['restrictedPromptMsg1']['value']):
                return

        elif 'cellEquipBless' == methodName:
            if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipBlessPage, 
                                                A_ACD.datas['restrictedPromptMsg1']['value']):
                return

        elif 'cellEquipSpiritWashing' == methodName:
            if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipEnchantingPanel, 
                                                A_ACD.datas['restrictedPromptMsg1']['value']):
                return

        if self.bagData.isLocked():
            LOG_WARN('in baseEquipDeductItemsWithBindTypes, bagData locked!')
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED, 0, 0)
            return
        # 检查物品消耗
        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costCurrencies.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)
        for itemId, itemNum in costItems.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)

        if not self.canDeductWealth(deductWealthVal):
            LOG_WARN('in baseEquipDeductItemsWithBindTypes, item is not enough')
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ITEMS_NOT_ENOUGH, 0, 0)
            return
        
        itemBindInfos = {}
        for idx in range(0, len(itemIds)):
            itemId = itemIds[idx]
            bindType = bindTypes[idx]
            # 重复了
            if itemId in itemBindInfos:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('in baseEquipDeductItemsWithBindTypes wrong args, item id is repeated:', itemId, itemIds, bindTypes)
                return
            itemBindInfos[itemId] = bindType

        # 计算消耗的格子
        gridNeedItems, bindInfos, _ = self.calculateConsumePlanGridsWithBindTyps(costItems, itemBindInfos)
        if costItems and not gridNeedItems:
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ITEMS_NOT_ENOUGH, 0, 0)
            LOG_WARN('in baseEquipDeductItemsWithBindTypes no gridNeedItems', costItems, itemBindInfos)
            return
        
        self.bagData.deductItemsByGrid(self, gridNeedItems, opUUID, srcType, detail)

        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costCurrencies.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)

        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
        self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_STAT_OK, bindInfos[0], bindInfos[1])
        LOG_INFO('in baseEquipDeductItemsWithBindTypes ', methodName, args)

    def addAutoDressEquipItem(self, equipList, opUUID, srcType, taskId, awardCtx):
        LOG_INFO('addAutoDressEquipItem')
        #新手引导使用，装备进背包后自动穿到身上
        if self.bagData.isLocked():
            gameengine.panicStack('addAutoDressEquipItem, bag locked, try later:', opUUID)
            self.addTimerCB(1, 'addAutoDressEquipItem', (equipList, opUUID, srcType, taskId, awardCtx), gametimer.TIMER_TAG_AUTO_DRESS_EQUIP)
            return

        if len(equipList) > self.bagData.leftGridCount:
            gameengine.panicStack('addAutoDressEquipItem, no space')
            return

        succGridIdList = []
        for it in equipList:
            opStat, gridId = self.bagData.addItemsToNewGrid(
                self, 
                it, 
                opUUID, 
                srcType, 
                str(taskId), 
                syncToClient=False
            )

            if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
                gameengine.panicStack('addAutoDressEquipItem, add equip failed:', it.itemId, it.uniqueId)
                return
            succGridIdList.append(gridId)

        for gridId in succGridIdList:
            self.dressEquipment(gridId, gameconst.EQUIP_DRESS_TYPE.OP_AUTO_DRESS, False, 0)
        return

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def dressEquipment(self, exposed, gridId, dressType, dstSlotId):
        LOG_INFO('in dressEquipment:', gridId, dressType, dstSlotId, self.baseSpaceNo)
        self.bagData.doDressEquip(self, gridId, dressType, dstSlotId)

    def dressEquipmentCB(self, uniqId, result, bagEquipDic):
        LOG_INFO('in dressEquipmentCB:', uniqId, result)
        self.bagData.doDressEquipCB(self, uniqId, result)
        if result != gameconst.DressEquipOpStat.EQUIP_OP_FAILED:
            if 'attrJson' in bagEquipDic:
                attrJson = bagEquipDic['attrJson']
                attrDict = json.loads(attrJson)
                enhanceLv = attrDict.get('enhanceLv', 0)

    @gamedecorator.crossServer
    def replaceEquipment(self, uniqId, result, oldBodyEquipDic):
        LOG_INFO('in replaceEquipment:', uniqId, result, self.baseSpaceNo, oldBodyEquipDic)
        self.bagData.doDressEquipCB(self, uniqId, result, oldBodyEquipDic)

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def undressEquipment(self, exposed, slotId):
        LOG_INFO("in undressEquipment:", slotId, self.baseSpaceNo)
        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        if not self.bagData.tryLockBag(lockDesc='undressEquipment, slotId:%s'%(slotId)):
            LOG_ERR('in undressEquipment, lock bag fail:', self.bagData.lockDesc, slotId)
            return

        self.cell.cellUndressEquipment(slotId)

    def updateAccountCharacterAppearance(self, updateDic):
        self.accountEntity.updateAppearance(self.gbID, updateDic)
        if self.subAccount:
            self.subAccount.updateAppearance(self.gbID, updateDic)

    def cellUndressEquipmentSucc(self, bodyEquipDic):
        LOG_INFO('in cellUndressEquipmentSucc', bodyEquipDic)
        self.unlockBag()
        self.bagData.doBagUndressEquip(self, bodyEquipDic)
    
    def cellUndressEquipmentFail(self, slotId, reason):
        LOG_INFO("cellUndressEquipmentFail::", slotId, reason)
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL, reason)

    def cellBrokenEquipment(self, srcType, uniqueId, bodyEquipDic):
        LOG_INFO("cellBrokenEquipment::", srcType, uniqueId, bodyEquipDic)
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

    def bagEquipUpgrade(self, upgradeType, gridId, uniqueId, consumeGridIds, targetLv, autoBuy):
        LOG_INFO('in bagEquipUpgrade:', upgradeType, gridId, uniqueId, consumeGridIds, targetLv, autoBuy)
        if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipClassPage, 
                                               A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('in bagEquipUpgrade, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('in bagEquipUpgrade, uniqueId not matched:', bagEquipItem.uniqueId, uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('   in bagEquipUpgrade, equipment can not be growing, equipment:', bagEquipItem)
            return
        
        if len(consumeGridIds) == 0:
            LOG_ERR('   in bagEquipUpgrade, args error, consumed grid is empty')
            return
        
        ret = dataUtils.checkEquipmentUpgradeType(bagEquipItem.equipAttr.equipType)
        if not ret:
            LOG_ERR('   in bagEquipUpgrade, equipment upgrade is invalid, equipment:', bagEquipItem)
            return

        if not dataUtils.checkEquipUpgradeValid(bagEquipItem.equipAttr.equipType, bagEquipItem.equipAttr.quality, bagEquipItem.getGrade(), upgradeType, targetLv):
            LOG_ERR('   in bagEquipUpgrade, equipment upgrade is invalid', bagEquipItem.itemId)
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
        LOG_INFO('in bagEquipUpgradeDeductItemsCB:', opStat, bindValue, upgradeType, targetLv, opUUID, gridId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipUpgradeDeductItemsCB, deduct items error')
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

    def bagEquipGlyphWashing(self, gridId, uniqueId, glyphPos, itemIds, bindTypes):
        LOG_INFO('in bagEquipGlyphWashing:', gridId, uniqueId, glyphPos, itemIds, bindTypes)
        if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipRunePage, 
                                               A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('in bagEquipGlyphWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('in bagEquipGlyphWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('in bagEquipGlyphWashing, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
        if not ret:
            LOG_ERR('in bagEquipGlyphWashing, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkGlyphNum(glyphPos):
            LOG_ERR('in bagEquipGlyphWashing slot is empty')
            return

        costItemDic, costCurrencyDic = bagEquipItem.glyphWashingNeedItems()
        if not costItemDic or not costCurrencyDic:
            LOG_ERR('     in bagEquipGlyphWashing, cost is empty:')
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_WEAPON_GLYPH_WASHING
        
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                    'bagEquipGlyphWashingDeductItemsCB', (opUUID, gridId, glyphPos))
        
        return

    def bagEquipGlyphWashingDeductItemsCB(self, opStat, bindValue, opUUID, gridId, glyphPos):
        LOG_INFO('in bagEquipGlyphWashingDeductItemsCB:', opStat, bindValue, opUUID, gridId, glyphPos)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipGlyphWashingDeductItemsCB, deduct items error')
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
            self.triggerAchievement(gameconst.AchieveType.INSCRIPTION)
        return

    def bagEquipGlyphApply(self, gridId, uniqueId, groupId):
        LOG_INFO('in bagEquipGlyphApply:', gridId, uniqueId, groupId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('in bagEquipGlyphApply, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('in bagEquipGlyphApply, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('in bagEquipGlyphApply, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
        if not ret:
            LOG_ERR('in bagEquipGlyphApply, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkGlyphApplyGroupId(groupId):
            LOG_ERR('in bagEquipGlyphApply groupId is wrong')
            return

        bagEquipItem.doApplyGlyphGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, groupId)
        self.client.onEquipGlyphApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, groupId, bagEquipItem.getEquipScore())
        return

    def bagEquipSpiritApply(self, gridId, uniqueId, groupId):
        LOG_INFO('in bagEquipSpiritApply:', gridId, uniqueId, groupId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('in bagEquipSpiritApply, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('in bagEquipSpiritApply, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('in bagEquipSpiritApply, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentSpiritType(bagEquipItem.equipAttr.equipType)
        if not ret:
            LOG_ERR('in bagEquipSpiritApply, equipment can not glyph, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkSpiritApplyGroupId(groupId):
            LOG_ERR('in bagEquipSpiritApply groupId is wrong')
            return

        bagEquipItem.doApplySpiritGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, groupId)
        self.client.onEquipSpiritApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, groupId, bagEquipItem.getEquipScore())
        return

    def bagEquipBless(self, gridId, uniqueId, itemIds, bindTypes):
        LOG_INFO('in bagEquipBless:', gridId, uniqueId, itemIds, bindTypes)
        if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipBlessPage, 
                                               A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('in bagEquipBless, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('in bagEquipBless, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('   in bagEquipBless, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentBlessType(bagEquipItem.equipAttr.equipType, bagEquipItem.getQuality())
        if not ret:
            LOG_ERR('   in bagEquipBless, equipment can not bless, equipment:', bagEquipItem)
            return False

        costItemDic, costCurrencyDic = bagEquipItem.blessNeedItems()
        if not costItemDic:
            LOG_ERR('     in bagEquipBless, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_BLESSING
        
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                    'bagEquipBlessDeductItemsCB', (opUUID, gridId))
        
        return

    def bagEquipBlessDeductItemsCB(self, opStat, bindValue, opUUID, gridId):
        LOG_INFO('in bagEquipBlessDeductItemsCB:', opStat, bindValue, opUUID, gridId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipBlessDeductItemsCB, deduct items error')
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
        LOG_INFO('in bagEquipBackBless:', gridId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('bagEquipBackBless, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('bagEquipBackBless, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        ret = dataUtils.checkEquipmentBlessType(bagEquipItem.equipAttr.equipType, bagEquipItem.getQuality())
        if not ret:
            LOG_ERR('bagEquipBackBless not bless type')
            return

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('   in bagEquipBackBless, equipment can not be growing, equipment:', bagEquipItem)
            return

        if not bagEquipItem.isCanBackBless():
            LOG_ERR('bagEquipBackBless not can backBless')
            return

        if bagEquipItem.doEquipBackBless():
            blessAffixes = []
            for oneAffix in bagEquipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBackBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, blessAffixes,
                                             bagEquipItem.equipAttr.maxBlessLv, bagEquipItem.equipAttr.blessLvRate,
                                             bagEquipItem.getEquipScore())

    def bagEquipSpiritWashing(self, gridId, uniqueId, spiritPos, itemIds, bindTypes):
        LOG_INFO('in bagEquipSpiritWashing:', gridId, uniqueId, spiritPos, itemIds, bindTypes)
        if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipEnchantingPanel, 
                                            A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('bagEquipSpiritWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('bagEquipSpiritWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('bagEquipSpiritWashing, equipment can not be growing, equipment:', bagEquipItem)
            return

        ret = dataUtils.checkEquipmentSpiritType(bagEquipItem.equipAttr.equipType)
        if not ret:
            LOG_ERR('bagEquipSpiritWashing, equipment can not affix, equipment:', bagEquipItem)
            return False

        if not bagEquipItem.checkSpiritNum(spiritPos):
            LOG_ERR('bagEquipSpiritWashing slot is empty')
            return

        costItemDic, costCurrencyDic = bagEquipItem.spiritWashingNeedItems()
        if not costItemDic or not costCurrencyDic:
            LOG_ERR('     bagEquipSpiritWashing, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_AFFIX_WASHING
            
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                    'bagEquipSpiritWashingDeductItemsCB', (opUUID, gridId, spiritPos))
        
        return

    def bagEquipSpiritWashingDeductItemsCB(self, opStat, bindValue, unbindValue, opUUID, gridId, spiritPos):
        LOG_INFO('in bagEquipSpiritWashingDeductItemsCB:', opStat, bindValue, unbindValue, opUUID, gridId, spiritPos)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipSpiritWashingDeductItemsCB, deduct items error')
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


    def bagEquipSoulSocket(self, gridId, uniqueId, soulGridId, itemIds, bindTypes):
        LOG_INFO('in bagEquipSoulSocket:', gridId, uniqueId, soulGridId, itemIds, bindTypes)
        if not self.checkAuthDisassembleAndMsg(A_AFD.UlEquipSoul, 
                                            A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('bagEquipSoulSocket, gridId is invalid:', gridId)
            return
        # if bagEquipItem.uniqueId != uniqueId:
        #     LOG_ERR('bagEquipSoulSocket, uniqueId not matched:', bagEquipItem.uniqueId, uniqueId)
        #     return

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('bagEquipSoulSocket, equipment can not be growing, equipment:', bagEquipItem)
            return
        
        soulItem = self.bagData.getItemObjByGridId(soulGridId)
        if not soulItem:
            LOG_ERR('bagEquipSoulSocket, soulGridId is invalid:', soulGridId)
            return

        if soulItem.itemSubType != gameconst.ItemSubType.EQUIP_SOUL:
            LOG_ERR('bagEquipSoulSocket, soulGridId is not soul item:', soulGridId)
            return

        soulData = SS_D.datas.get(soulItem.itemId, None)
        if not soulData:
            LOG_ERR('bagEquipSoulSocket, soulItem is not soul item:', soulItem.itemId)
            return

        if soulData['equipmentID'] != bagEquipItem.equipAttr.equipType:
            LOG_ERR('bagEquipSoulSocket, equipType is not match:', soulItem.itemId, bagEquipItem.equipAttr.equipType)
            return

        costItemDic, costCurrencyDic = bagEquipItem.soulSocketNeedItems()
        if not costCurrencyDic:
            LOG_ERR('     bagEquipSoulSocket, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_SOUL
        
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                    'bagEquipSoulSocketDeductItemsCB', (opUUID, gridId, soulItem.rollProps))
        
        return

    def bagEquipSoulSocketDeductItemsCB(self, opStat, bindValue, unbindValue, opUUID, gridId, rollProps):
        LOG_INFO('in bagEquipSoulSocketDeductItemsCB:', opStat, bindValue, unbindValue, opUUID, gridId, rollProps)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipSoulSocketDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if bindValue > 0:
            bagEquipItem.updateBindValue()
        ret = bagEquipItem.doEquipSoulSocket(self, rollProps)
        if ret:

            soulAffixes = []
            for oneAffix in bagEquipItem.equipAttr.soulAffixes:
                soulAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipSoulSocketSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, soulAffixes,
                                                 bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return

    def bagEquipBindWashing(self, gridId, uniqueId, washCount):
        LOG_INFO('in bagEquipBindWashing:', gridId, uniqueId, washCount)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_ERR('in bagEquipBindWashing, gridId is invalid:', gridId)
            return
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('     in bagEquipBindWashing, uniqueId not matched:', bagEquipItem.uniqueId)
            return
        if not bagEquipItem.hasBindValue() or bagEquipItem.getBindValue() < washCount:
            LOG_ERR('     in bagEquipBindWashing, no bind value remain:', bagEquipItem.uniqueId)
            return

        costItemDic, needUnbindItemDic = bagEquipItem.bindValueWashingNeedItems(washCount)
        if not costItemDic or not needUnbindItemDic:
            LOG_ERR('     in bagEquipBindWashing, cost is empty')
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BINDVALUE_WASHING_BAG_EQUIP
        detail = gameclass.AwardDetail(uniqueId=bagEquipItem.uniqueId)
        args = [needUnbindItemDic, opUUID, gridId, washCount]
        self.baseEquipDeductItems(costItemDic, None, None, None, opUUID, srcType, detail, self, 'bagEquipBindValueWashingDeductItemsCB', args,
                                  False, True)

    def bagEquipBindValueWashingDeductItemsCB(self, opStat, opUUID, gridId, washCount):
        LOG_INFO('in bagEquipBindValueWashingDeductItemsCB:', opStat, gridId, washCount)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipBindValueWashingDeductItemsCB, deduct items error')
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
        LOG_INFO('reqMultiEquipDisassemble:', gridIdList, uniqueIdList)
        self.bagData.doBagEquipDisassemble(self, gridIdList, uniqueIdList)

    def bagEquipSell(self, gridId, uniqueId):
        self.bagData.doBagEquipSell(self, gridId, uniqueId)

    def updateBodyEquipDressData(self, dressDataDic):
        self.baseBodyEquipDressDataDic = dressDataDic

    def canEquipAutoDisassemble(self, owner, equipItem):
        cliConfig = self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY, 0)
        # 自动分解开关
        autoSwitch = utils.bhas(cliConfig, gameconst.AUTO_DISA_KEY.AUTOS_WITCH)
        if not autoSwitch:
            return False
        # 可交易开关
        isCanTrade = utils.bhas(cliConfig, gameconst.AUTO_DISA_KEY.TRADE)
        if not isCanTrade and equipItem.bindType != gameconst.ItemBindType.BIND:
            return False
        # 装备品质
        if not utils.bhas(cliConfig, equipItem.quality):
            return False
        # 装备大类
        equipDisKey = gameconst.AUTO_DISA_MAP.datas.get(equipItem.equipAttr.equipType, None)
        if not equipDisKey:
            return False
        if not utils.bhas(cliConfig, equipDisKey):
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
        LOG_INFO('reqMakeEquipment:', itemId, gridIdList, gridCountList, makeType)
        itemData = dataUtils.getEquipItemData(itemId)
        if not itemData:
            LOG_ERR('in reqMakeEquipment, gearBase_gearBase not found:', itemId)
            return

        if len(gridIdList) > self.bagData.capacity or len(gridIdList) != len(gridCountList):
            LOG_ERR('in reqMakeEquipment, wrong args:', itemId)
            return

        school = self.getRoleCacheAttr('school', 0)
        recommendClasses = dataUtils.equipRecommendClass(itemData['type'], itemData['subType'])
        if school not in recommendClasses:
            LOG_ERR('in reqMakeEquipment, in valid school:', itemId, school, recommendClasses)
            return

        cfgData = GMDD.datas.get(itemId, None)
        if not cfgData:
            LOG_ERR('in reqMakeEquipment, gearManufacture_details not found:', itemId)
            return

        isOpen = cfgData.get('isOpen')
        if not isOpen:
            LOG_ERR('in reqMakeEquipment not open:', itemId)
            self.client.onEquipMakeFailed()
            return

        if self.bagData.isFull():
            self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
            return

        if self.bagData.isLocked():
            LOG_WARN('   in reqMakeEquipment, bagData locked!:', itemId)
            return
        
        consumeItem = None
        if makeType == gameconst.EquipmentManufactureType.MANUFACTURE_LEFT:
            consumeItem = cfgData.get('consumeItem')
            if not consumeItem:
                LOG_ERR('in reqMakeEquipment missing consumeItem:', itemId, makeType)
                return
        elif makeType == gameconst.EquipmentManufactureType.MANUFACTURE_RIGHT:
            consumeItem = cfgData.get('consumeItem2')
            if not consumeItem:
                LOG_ERR('in reqMakeEquipment missing consumeItem2:', itemId, makeType)
                return
        else:
            LOG_ERR('in reqMakeEquipment unknow equipment manufacture type:', itemId, makeType)
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
            LOG_ERR('in reqMakeEquipment wrong args:', itemId, makeType, needGridIdList, needCostItems, okCount)
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
            LOG_ERR('in reqMakeEquipment, consume item is empty, equipment manufacture is forbidden:', itemId)
            self.client.onEquipMakeFailed()
            return

        if not self.canDeductWealth(deductVal, sendMsg=True):
            LOG_ERR('in reqMakeEquipment, canDeductWealth fail:', itemId)
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
        LOG_INFO('reqMakeEquipment: done', itemId, gridIdList, makeType, bindValue)
        opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem, ], opUUID, srcType, detail, notify=False)
        if opStat == gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LogTrackingMgr.LogTrackingMgr.Equip_Make(opUUID, self.gbID, equipItem.uniqueId, equipItem.itemId, 1, equipItem.getGrade(), equipItem.getQuality(), equipItem.getBindValue(), makeType, equipItem.getBaseAttrs(), equipItem.getUpgradeAttrs(), equipItem.getEnhanceAttrs(), equipItem.getEquipScore())
            data = equipItem.toClientEquipItemDict()
            LOG_INFO('in reqMakeEquipment, addItemsWithPlan success:', opStat, data)
            self.client.onEquipMakeSucc(data)
        else:
            LOG_ERR('in reqMakeEquipment, addItemsWithPlan fail:', opStat, itemId)
            self.client.onEquipMakeFailed()

        self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.MAKE_EQUIPMENT, actionContext.AchievementCtx())
        
    ################################## gm cmd ###################################
    def gmAddGearbaseEquipItem(self, templateId, bindType=dataUtils.getItemDefaultBindType(), grade = 1):
        LOG_INFO('gmAddGearbaseEquipItem:', templateId)
        equipItem = itemFactory.ItemFactory.createItem(templateId, 1, bindType=bindType, grade = grade)
        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_GM
        detail = gameclass.AwardDetail(templateId=templateId)

        opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem, ], opUUID, src, detail)
        return opStat


    def gmBaseDressEquips(self, bodyDressSlotIds, quality):
        LOG_INFO("gmBaseDressEquips ", bodyDressSlotIds, quality)
        myLevel = gameglobal.roleCache[self.id]['level']
        myClass = gameglobal.roleCache[self.id]['school']
        for gridId, it in self.bagData.gridIdToGridObj.items():
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
                    self.addTimerCB(0.2, 'gmSendDressEquips', (gridId, slotId, it), gametimer.TIMER_TAG_GM_SEND_DRESS_EQUIPS)
                    break

            if len(bodyDressSlotIds) == 0:
                break
        return

    def gmSendDressEquips(self, gridId, slotId, equipItem):
        LOG_INFO("gmSendDressEquips ", gridId, slotId, equipItem)
        self.unlockBag()
        self.bagData.doDressEquip(self, gridId, 0, slotId)

    def gmGlyphWashingEquips(self, itemId, glyphPos, affixId1, affixId2):
        gridIds = self.bagData.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
                LOG_ERR('in gmGlyphWashingEquips, equipment can not be growing, equipment:', bagEquipItem)
                return

            ret = dataUtils.checkEquipmentGlyphType(bagEquipItem.equipAttr.equipType)
            if not ret:
                LOG_ERR('in gmGlyphWashingEquips, equipment can not glyph, equipment:', bagEquipItem)
                return False

            if not bagEquipItem.checkGlyphNum(glyphPos):
                LOG_ERR('in gmGlyphWashingEquips slot is empty')
                return

            ret, _, _ = bagEquipItem.doEquipGlyphWashing(self, glyphPos, affixIds=[affixId1, affixId2])
            if ret:
                glyphData = bagEquipItem.equipAttr.getGlyphData(glyphPos)
                self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, glyphData.toClientData(), bagEquipItem.getEquipScore(), bagEquipItem.getAddBindValueStatus(), bagEquipItem.bindType)
        return
################################## gm cmd end ###################################

    ################################### drop equip start ##############################
    def checkDropEquip(self, equipInfo, baseDropInfo):
        # 掉落列表满了
        if self.equipDropData.dropNum() >= GBGCD.datas['equipRepairListMaxNum']['value']:
            # 如果是自己的，直接破碎
            if baseDropInfo['ownerId'] == self.gbID:
                srcType = AAC_AACDD.datas.BONUS_SRC_EQUIPMENT_DROP
                self.cellBrokenEquipment(srcType, equipInfo['uniqueId'], equipInfo)
            else:
                # 别人的，掉落时间到了，那就不处理了，等自动返还
                if utils.curTS() < baseDropInfo['returnTime']:
                # 不创建创生物，系统代为保管，时间到了自动赎回
                    _blob = cPickle.dumps(equipInfo)
                    gameengine.getGlobalBase('DropStub').custodyEquipItem(self.gbID, equipInfo['uniqueId'], gameconst.DropType.TYPE_RETURN_WAIT, baseDropInfo['price'], _blob, \
                                                                      0, 0, baseDropInfo['returnTime'], baseDropInfo['ownerId'], baseDropInfo['ownerServerId'], 0)
                           
            # 发邮件告知，装备由于掉落列表满了，已消失
            _mailId = GBGCD.datas['equipDisappearMailID']['value']
            _args = [
                str(GBGBD.datas[equipInfo['itemId']]["name"]),
            ]
            mailAssistor.sendMailToPlayers(
                [self.gbID],
                _mailId,
                opUUID=KBEngine.genUUID64(),
                despArgs=_args,
                srcType=AAC_AACDD.datas.BONUS_SRC_EQUIPMENT_DROP_REMOVE
            )
        else:
            self.cell.doDropEquipByItem(baseDropInfo, equipInfo)

    def onDropEquipBase(self, ownerId, returnTime, ownerServerId, uniqueId, price, mapId, pos, equipInfo, collEndTime, killerName, endTime, extraBlob, collectionId, dropTime):
        _blob = cPickle.dumps(equipInfo)
        gameengine.getGlobalBase('DropStub').dropEquipItem(
            ownerServerId,
            ownerId,
            returnTime,
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
            dropTime
        )

        # _reachNum = self.equipDropData.dropNum() - GBGCD.datas['equipRepairListMaxNum']['value']
        # if _reachNum > 0:
        #     _val = self.equipDropData.fetchNeedRemoveDropEquip()
        #     LOG_INFO('Drop onDropEquipBase _reachNum', self.equipDropData.dropNum(), _reachNum, _val)
        #     if _val:
        #         self.removeDropEquip(_val.uniqueId, _reachNum)

    def addNotifyDropFixTimer(self, uniqueId, endTime):
        self.equipDropData.addNotifyDropFixTimer(uniqueId, endTime)

    # 检测捡装备
    def checkPickDropEquip(self, uniqueId):
        if self.pickDropEquipLockTime > utils.curTS():
            return False

        return self.equipDropData.checkCouldTakeDrop(uniqueId)

    # 自己捡起来或者赎回会走到这里
    def onGetBackDropEquip(self, uniqueId, equipInfo, dropType):
        equipInfo = cPickle.loads(equipInfo)
        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)
        
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
        # 对方返还或者自己捡起来，需要倒计时
        if dropType == gameconst.TYPE_DROP.TYPE_TAKE_WAIT_DROP_GET or dropType == gameconst.TYPE_DROP.TYPE_GIVEUP_WAIT_DROP_GET:
            _fixEndTime = utils.curTS() + GBGCD.datas['equipRepairTime']['value']
            equipItem.setDropFixEndTime(_fixEndTime)
            self.addNotifyDropFixTimer(equipItem.uniqueId, _fixEndTime)
            _args = [
                str(equipItem.itemId),
                str(GBGCD.datas['equipRepairTime']['value']),
            ]
            self.onMessagePre(GBGCD.datas['equipRepairing_msgId']['value'], _args)
        # 自己赎回，无需倒计时
        elif dropType == gameconst.TYPE_DROP.TYPE_REDEEM_WAIT_DROP_GET:
            pass
        # 赎回倒计时结束，无需倒计时
        elif dropType == gameconst.TYPE_DROP.TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET:
            pass
        # 超时自动返还，无需倒计时
        elif dropType == gameconst.TYPE_DROP.TYPE_RETURN_GET:
            pass

    def removeDropEquip(self, uniqueId, times):
        if not self.equipDropData.tryLock():
            LOG_WARN('removeDropEquip lock failed:', uniqueId)
            return

        if not self.equipDropData.hasDrop(uniqueId):
            LOG_ERR('removeDropEquip not found drop:', uniqueId)
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
        LOG_INFO('onRemoveDropEquip:', uniqueId, result, times)
        self.equipDropData.unlock()

        if result == DropResult_SUCCESS:
            _dropVal = self.equipDropData.removeDrop(self, uniqueId)
            if _dropVal:
                _item = _dropVal.equipItem()
                self._sendDestroyMail(_item.itemId)

                if utils.curTS() < _dropVal.collEndTime:
                    gameengine.callCellApps('removeEquipDropDestroyCollection', (collectionId, _dropVal.uniqueId))

                self.onMessagePre(
                    GBGCD.datas['equipDestroyedForPick_msgID']['value'],
                    [str(_item.itemId)])
        else:
            LOG_ERR('onRemoveDropEquip fail:', uniqueId, result, times)

        times -= 1

        if times > 0 and self.equipDropData.dropNum() > GBGCD.datas['equipRepairListMaxNum']['value']:
            _val = self.equipDropData.fetchNeedRemoveDropEquip()
            if _val:
                self.removeDropEquip(_val.uniqueId, times)

    def onTakeDropEquipFailed(self, uniqueId, result):
        LOG_INFO('onTakeDropEquipFailed:', uniqueId, result)
        self.pickDropEquipLockTime = 0

    # 捡别人的装备成功的回调
    def onTakeDropEquipSuccess(self, dropGbId, uniqueId, equipInfo, endTime, price, redeemWaitTime):
        LOG_INFO('onTakeDropEquipSuccess:', dropGbId, uniqueId, equipInfo, endTime, price, redeemWaitTime)
        self.pickDropEquipLockTime = 0

        if dropGbId == self.gbID:
            #self.equipDropData.removeDrop(self, uniqueId)
            self.onDropTypeChangeToAvatar(uniqueId, gameconst.DropNotifyType.NOTIFY_TYPE_TAKE_WAIT_DROP_GET)
            return

        equipInfo = cPickle.loads(equipInfo)
        self.equipDropData.addTaker(
            self,
            uniqueId,
            equipInfo,
            endTime,
            gameconst.DropType.TYPE_TAKE,
            price,
            True,
            redeemWaitTime
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

        _posInfo = self.popTempMiscProp(gameconst.EntityPropsEnum.takeDropInfo, None)
        if _posInfo is None:
            LOG_ERR('onGetBackDropEquip not found temp misc prop:', uniqueId)
            return

        _spaceNo, _pos = _posInfo
        LogTrackingMgr.LogTrackingMgr.Drop_Equip(
            self.gbID,
            equipItem.uniqueId,
            equipItem.itemId,
            equipItem.getQuality(),
            equipItem.getGrade(),
            formula.fetchMapId(_spaceNo),
            str(_pos),
            gameconst.EQUIP_OPR_PICK,
        )

    @gamedecorator.checkGameconfigEnable('equip')
    def giveUpDropEquip(self, exposed, uniqueId):
        LOG_INFO('giveUpDropEquip:', uniqueId)
        if not self.equipDropData.hasTakeDrop(uniqueId):
            LOG_ERR('giveUpDropEquip not found take:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').giveUpDropEquip(self.gbID, uniqueId, self)

    @gamedecorator.checkGameconfigEnable('equip')
    def redeemEquipDrop(self, exposed, uniqueId):
        LOG_INFO('redeemEquipDrop:', uniqueId)
        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if not _dropVal:
            LOG_ERR('redeemEquipDrop not found drop:', uniqueId)
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(
            GBGCD.datas['equipRepairCostItemID']['value'],
            _dropVal.price,
        )

        if not self.canDeductWealth(_deductVal, sendMsg=True):
            LOG_WARN('       in doUnlockGrids, items not enough:', _deductVal)
            return

        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_EQUIP_DROP
        _detail = gameclass.AwardDetail()
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        gameengine.getGlobalBase('DropStub').doRedeemEquipDrop(self.gbID, uniqueId, self)

    def onRedeemResult(self, uniqueId, result):
        LOG_INFO('onRedeemResult:', uniqueId, result)
        if result == DropResult_SUCCESS:
            self.equipDropData.removeDrop(self, uniqueId)
            return
        elif result == DropResult_NOT_FOUND:
            LOG_WARN('onRedeemResult not found drop:', uniqueId)
            self.equipDropData.removeTaker(self, uniqueId)
        elif result == DropResult_EXPIRE:
            LOG_WARN('onRedeemResult expire:', uniqueId)
            self.equipDropData.removeTaker(self, uniqueId)
        elif result == DropResult_OTHER_GIVEUP:
            self._fetchOtherGiveUpEquip(uniqueId)
        elif result == DropResult_REDEEM_NOT_SET_PRICE:
            # 这里缺乏一个提示，推给客户端先
            self.client.onRedeemNotSetPrice(uniqueId)
            return
        else:
            LOG_ERR('onRedeemResult unknown:', uniqueId, result)

        # _dropVal = self.equipDropData.getDropVal(uniqueId)
        # if not _dropVal:
        #     LOG_ERR('onRedeemResult not found drop:', uniqueId)
        #     return

        # _awardVal = dropAward.AwardVal()
        # _awardVal.addWealthByItemId(
        #     GBGCD.datas['equipRepairCostItemID']['value'],
        #     _dropVal.price,
        # )
        # _opUUID = KBEngine.genUUID64()
        # _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_EQUIP_DROP
        # _detail = gameclass.AwardDetail()

        # self.addWealth(
        #     _src,
        #     _awardVal,
        #     _opUUID,
        #     _detail,
        #     awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
        # )

    # 别人赎回后，你领取奖励
    def _getTakeReward(self, uniqueId):
        gameengine.getGlobalBase('DropStub').doGetTakeReward(self.gbID, uniqueId, self)

    def onGetDropTakeReward(self, uniqueId, price):
        LOG_INFO('onGetDropTakeReward:', uniqueId, price)
        _takerVal = self.equipDropData.removeTaker(self, uniqueId, isNotify=False)
        if not _takerVal:
            LOG_ERR('onGetDropTakeReward not found taker:', uniqueId)
            return

        self.equipDropData.addTakerWait(uniqueId, _takerVal.equip, _takerVal.endTime, _takerVal.price, _takerVal.redeemWaitTime, _takerVal.hasPrice)
        self.client.onEquipDropStateChange(uniqueId, gameconst.DropType.TYPE_REDEEM)

    @gamedecorator.checkGameconfigEnable('equip')
    def getTakerWaitReward(self, exposed, uniqueId):
        LOG_INFO('getTakerWaitReward:', uniqueId)
        _takerVal = self.equipDropData.removeTakerWait(self, uniqueId)
        if not _takerVal:
            LOG_ERR('getTakerWaitReward not found takerWait:', uniqueId)
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
        LOG_INFO('_fetchOtherGiveUpEquip:', uniqueId)
        gameengine.getGlobalBase('DropStub').doFetchOtherGiveUpEquip(self.gbID, uniqueId, self)

    def onDropTypeChangeToAvatar(self, uniqueIds, notifyTypes):
        LOG_INFO('onDropTypeChangeToAvatar:', uniqueIds, notifyTypes)
        for idx in range(0, len(uniqueIds)):
            uniqueId = uniqueIds[idx]
            notifyType = notifyTypes[idx]
            if notifyType == gameconst.DropNotifyType.NOTIFY_REMOVE_ALL:
                self.equipDropData.removeDrop(self, uniqueId)
                self.equipDropData.removeTaker(self, uniqueId)
                return
            elif notifyType == gameconst.DropNotifyType.NOTIFY_REMOVE_DROP:
                self.equipDropData.removeDrop(self, uniqueId)
                return
            elif notifyType == gameconst.DropNotifyType.NOTIFY_REMOVE_TAKE:
                self.equipDropData.removeTaker(self, uniqueId)
                return
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_DROP \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_TAKE_WAIT_DROP_GET \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_REDEEM_WAIT_DROP_GET \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_GIVEUP_WAIT_DROP_GET \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_RETURN_WAIT \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_RETURN_GET \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_TAKE:
                self.equipDropData.onDropTypeChange(uniqueId, notifyType)
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_REWARD:
                self.equipDropData.onTakeTypeChange(uniqueId, notifyType)

            self.client.onEquipDropStateChange(uniqueId, notifyType)

    # 别人放弃了你捡起来的装备会走到这里
    def onFetchOtherGiveUpEquip(self, uniqueId, equipInfo, result, giveUpTime):
        LOG_INFO('onFetchOtherGiveUpEquip:', uniqueId, equipInfo, result, giveUpTime)
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

            LOG_ERR('onFetchOtherGiveUpEquip not found:', uniqueId, result)
            self.equipDropData.removeDrop(self, uniqueId)

    def _initGetAllDropEquipStatus(self):
        gameengine.getGlobalBase('DropStub').doGetDropInfo(self.gbID, self)

    def onGetDropInfo(self, dropInfo, takerInfo):
        LOG_INFO('onGetDropInfo:', dropInfo, takerInfo)
        for _uniqueId, _equipInfo, _endTime, _dropType, _extraInfo, _collExpireTime, _price, _dropTime in dropInfo:
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
                _dropTime
            )

        for _uniqueId, _equipInfo, _endTime, _dropType, _price, redeemWaitTime, hasPrice in takerInfo:
            self.equipDropData.addTaker(
                self,
                _uniqueId,
                _equipInfo,
                _endTime,
                _dropType,
                _price,
                False,
                redeemWaitTime, 
                hasPrice
            )

        self.equipDropInitStatus = 1
        self.triggerTempEvent(gameconst.EntityPropsEnum.equipDropInitEvent)

    def _sendDropEquipInfo(self):
        if not self.equipDropInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.equipDropInitEvent, '_sendDropEquipInfo', ())
            return

        # self.equipDropData.clearEndTimeVals()
        self.client.onInitEquipDropData(self.equipDropData)

    def _initEquipDrop(self):
        self.equipDropInitStatus = 0
        self.createTempEvent(gameconst.EntityPropsEnum.equipDropInitEvent)
        self.pyAddTimer(10, 10, gametimer.DEAL_DROP_EQUIP_EXPIRE)

    @property
    def equipDropInitStatus(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.equipDropInitStatus, 1)

    @equipDropInitStatus.setter
    def equipDropInitStatus(self, val):
        if val:
            self.popTempMiscProp(gameconst.EntityPropsEnum.equipDropInitStatus)
        else:
            self.setTempMiscProp(gameconst.EntityPropsEnum.equipDropInitStatus, 0)

    def takeEquipBase(self, uniqueId, spaceNo, position):
        if not self.checkPickDropEquip(uniqueId):
            LOG_ERR('takeEquipBase not could take drop:', uniqueId)
            return
        curTs = utils.curTS() 
        redeemWaitTime = GBGCD.datas['equipRedeemWaitTime']['value']
        gameengine.getGlobalBase('DropStub').takeDropEquip(self.gbID, self.serverId, uniqueId, self, redeemWaitTime)
        self.pickDropEquipLockTime = curTs + 60
        self.setTempMiscProp(gameconst.EntityPropsEnum.takeDropInfo, (spaceNo, position))

    def onGiveUpDropEquip(self, uniqueId, result, dropGbId):
        LOG_INFO('onGiveUpDropEquip:', uniqueId, result, dropGbId)
        if result == DropResult_SUCCESS:
            _takerVal = self.equipDropData.removeTaker(self, uniqueId)
            if _takerVal:
                redisUtils.RedisUtils.getSingleUserInfo(dropGbId, functools.partial(self._onGiveUpGetUserInfo, _takerVal))

    def _onGiveUpGetUserInfo(self, _takerVal, fcVal):
        _item = itemFactory.ItemFactory.createItemWithSavedDict(_takerVal.equip)
        _args = [
            str(_item.itemId),
            fcVal.name
        ]
        _msgId = GBGCD.datas['returnEnergyCrystalSuccess_msgID']['value']

        self.onMessagePre(_msgId, _args)

    def onOtherRemoveDropEquip(self, uniqueId):
        LOG_INFO('onOtherRemoveDropEquip:', uniqueId)
        self.equipDropData.removeTaker(self, uniqueId)

    def _dealDropEquipExpire(self):
        self.equipDropData.doDealDropEquipExpire(self)

        _endTime = utils.curTS()
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
        #self._sendPickDestroyMail(itemId)

    def onDropEquipExpire(self, uniqueId, result):
        LOG_INFO('onDropEquipExpire:', uniqueId, result)
        if result != DropResult_SUCCESS:
            return

        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if _dropVal:
            self._dropExpire(uniqueId, _dropVal.equipItem().itemId)
            return

    @gamedecorator.checkGameconfigEnable('equip')
    def setTakeEquipRedeemPrice(self, exposed, uniqueId, price):
        LOG_INFO('setTakeEquipRedeemPrice:', uniqueId, price)
        if price < 0:
            LOG_ERR('setTakeEquipRedeemPrice not valid price:', uniqueId, price)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        _dropVal = self.equipDropData.getTakerVal(uniqueId)
        if not _dropVal:
            LOG_ERR('setTakeEquipRedeemPrice not found take:', uniqueId)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        curTs = utils.curTS()
        if curTs > _dropVal.redeemWaitTime:
            LOG_ERR('setTakeEquipRedeemPrice over redeemTime:', uniqueId)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        if price < _dropVal.price:
            LOG_ERR('setTakeEquipRedeemPrice invalid price:', uniqueId, price, _dropVal.price)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        gameengine.getGlobalBase('DropStub').setTakeEquipRedeemPrice(self.gbID, uniqueId, self, price)
    
    def onSetTakeEquipRedeemPriceBase(self, uniqueId, price, result):
        LOG_INFO('onSetTakeEquipRedeemPriceBase:', uniqueId, price, result)
        if result != DropResult_SUCCESS:
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return

        _dropVal = self.equipDropData.getTakerVal(uniqueId)
        if not _dropVal:
            LOG_ERR('onSetTakeEquipRedeemPriceBase not found take:', uniqueId)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        _dropVal.price = price
        self.client.onSetTakeEquipRedeemPrice(uniqueId, price)

    @gamedecorator.offlineCallback
    def onReturnEquipNotify(self, gbId, equipData):
        LOG_INFO('in onReturnEquipNotify:', gbId, equipData)
        equipInfo = cPickle.loads(equipInfo)
        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)
        equipItem.setDropFixEndTime(0)

        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByObjList([equipItem])
        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_DROP_RETURN_BACK_EQUIP
        _detail = gameclass.AwardDetail()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID),
        )

    @gamedecorator.offlineCallback
    def onRemoveEquipNotify(self, gbId, uniqueId):
        LOG_INFO('in onRemoveEquipNotify:', gbId, uniqueId)
        # 先查背包里数据
        gridId, gridObj = self.getGridItemByUniqueId(uniqueId)
        if gridObj:
            bagType = self.bagData.bagType
            detail = gameclass.AwardDetail(bagType=bagType, gridId=gridId, itemId=gridObj.itemId)
            uuid = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_DROP_REMOVE_EQUIP
            self.bagData.cleanGridByGridId(self, gridId, gridObj.itemId, uuid, srcType, detail)
        else:
            # 从玩家身上移除
            self.cell.onRemoveEquipNotifyCell(uniqueId)

    @gamedecorator.checkGameconfigEnable('equip')
    def getBackEquip(self, exposed, uniqueId, dropType):
        LOG_INFO('in getBackEquip:', uniqueId, dropType)
        gameengine.getGlobalBase('DropStub').doGetBackEquip(self.gbID, self, uniqueId, dropType)

    @gamedecorator.checkGameconfigEnable('equip')
    def payDropPrice(self, exposed, uniqueId, price):
        LOG_INFO('payDropPrice:', uniqueId, price)
        if price < 0:
            LOG_ERR('payDropPrice not valid price:', uniqueId, price)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if not _dropVal:
            LOG_ERR('payDropPrice not found drop:', uniqueId)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        curTs = utils.curTS()
        if curTs > _dropVal.redeemWaitTime:
            LOG_ERR('payDropPrice over redeem time:', uniqueId)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        if price < _dropVal.price:
            LOG_ERR('payDropPrice invalid price:', uniqueId, price, _dropVal.price)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        gameengine.getGlobalBase('DropStub').setDropEquipPayPrice(self.gbID, uniqueId, self, price)
    
    def onSetDropEquipPayPriceBase(self, uniqueId, price, result):
        LOG_INFO('onSetDropEquipPayPriceBase:', uniqueId, price, result)
        if result != DropResult_SUCCESS:
            self.client.onPayDropPrice(uniqueId, -1)
            return

        _dropVal = self.equipDropData.getDropVal(uniqueId)
        if not _dropVal:
            LOG_ERR('onSetDropEquipPayPriceBase not found take:', uniqueId)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        self.client.onPayDropPrice(uniqueId, price)

    def onNotifyCustodyEquip(self, uniqueId, equipInfo, dropType, equip, retunTime):
        LOG_INFO('onNotifyCustodyEquip:', uniqueId, equipInfo, dropType, equip, retunTime)
        self.equipDropData.addNewDrop(
            self,
            uniqueId,
            0,
            0,
            (0,0,0),
            equipInfo,
            0,
            '',
            retunTime,
            dropType,
            True,
            0
        )
    ################################### drop equip end ##############################

    def checkEquipmentCore(self, itemID):
        itemData = ITEM_DATA.datas.get(itemID)
        return itemData and itemData['type'] == 0 and itemData['subType'] == gameconst.ItemSubType.EQUIP_CORE

    def calculateConsumePlan(self, needCostItems, gridIdList, gridCountList, needEquipCore=False):
        if len(gridIdList) != len(gridCountList):
            LOG_ERR('in calculateConsumePlan wrong args 1:', gridIdList, gridCountList)
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
                LOG_ERR('in calculateConsumePlan wrong args 2:', bagEquipItem, gridCount)
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

    def calculateConsumePlanGrids(self, itemsDic, bindType):
        results = {}
        bindInfos = [0, 0]
        consumedItemBindInfos = {}
        for itemId, itemNum in itemsDic.items():
            ret, bindInfo = self.getGridDatasWithConds(itemId, bindType, itemNum, False)
            # 出现不满足
            if not ret:
                return None, None, None
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
    
    def calculateConsumePlanGridsWithBindTyps(self, itemsDic, itemBindInfos):
        results = {}
        bindInfos = [0, 0]
        consumedItemBindInfos = {}

        for itemId, itemNum in itemsDic.items():
            bindType = itemBindInfos.get(itemId, None)
            if bindType is None:
                LOG_ERR('in calculateConsumePlanGridsWithBindTyps wrong args 2, missing item bind type:', itemId, itemNum, itemBindInfos)
                return None, None, None
            
            ret, bindInfo = self.getGridDatasWithConds(itemId, bindType, itemNum, False)
            # 出现不满足
            if not ret:
                return None, None, None
            
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
            LOG_ERR('checkBagEquipEnhanceConditions, gridId is invalid:', gridId)
            return False, None, None, None, False
        
        if bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('checkBagEquipEnhanceConditions, uniqueId not matched:', bagEquipItem.uniqueId)
            return False, None, None, None, False

        if dataUtils.checkEquipGrowingForbidden(self.gbID, bagEquipItem):
            LOG_ERR('checkBagEquipEnhanceConditions, equipment can not be growing, equipment:', bagEquipItem)
            return False, None, None, None, False

        ret = dataUtils.checkEquipmentEnhancementType(bagEquipItem.equipAttr.equipType)
        if not ret:
            LOG_ERR('checkBagEquipEnhanceConditions, equipment enhancement is invalid, equipment:', bagEquipItem)
            return False, None, None, None, False

        if not bagEquipItem.checkEnhancementValid(bagEquipItem.equipAttr.getEnhanceLv() + 1):
            LOG_ERR('checkBagEquipEnhanceConditions, equipment enhancement is invalid', bagEquipItem.itemId)
            return False, None, None, None, True

        costItemDic, costCurrencyDic = bagEquipItem.enhanceNeedItems()
        if not costItemDic or not costCurrencyDic:
            LOG_ERR('checkBagEquipEnhanceConditions, cost is empty:', bagEquipItem.equipAttr.getEnhanceLv() + 1)
            return False, None, None, None, False
        return True, bagEquipItem, costCurrencyDic, costItemDic, False
    
    def baseMultiEquipEnhance(self, equipUniqueIds, bagEquipDatas, validBodyItems, itemIds, bindTypes, isMulti):
        LOG_INFO('baseMultiEquipEnhance:', equipUniqueIds, bagEquipDatas, validBodyItems, itemIds, bindTypes, isMulti)
        if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipIntensifyPage, 
                                               A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        if not self.bagData.tryLockBag(lockDesc='baseMultiEquipEnhance'):
            self.cell.unlockBodyEquips()
            self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.BAG_EQUIP_LOCKED, [], [], isMulti)
            LOG_WARN('baseMultiEquipEnhance, bag data is locked')
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
                self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ARG_ERR, [], [], isMulti)
                LOG_WARN('baseMultiEquipEnhance, wrong args 1:', gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, uniqueId)
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

        itemBindInfos = {}
        for idx in range(0, len(itemIds)):
            itemId = itemIds[idx]
            bindType = bindTypes[idx]
            # 重复了
            if itemId in itemBindInfos:
                LOG_ERR('baseMultiEquipEnhance wrong args 2, item id is repeated:', itemId, itemIds, bindTypes)
                return None, None, None
            itemBindInfos[itemId] = bindType

        # 检查物品消耗
        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costCurrency.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)
        for itemId, itemNum in costItem.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)

        if not self.canDeductWealth(deductWealthVal):
            self.cell.unlockBodyEquips()
            self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ITEM_NOT_ENOUGH, [], [], isMulti)
            LOG_WARN('baseMultiEquipEnhance, item is not enough')
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
                self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ARG_ERR, [], [], isMulti)
                LOG_WARN('baseMultiEquipEnhance, arg is wrong', equipUniqueId)
                return
            isAddBindStatus = itemData[1]
            costCurrencyDic = itemData[2]
            costItemDic = itemData[3]
            # 计算消耗的格子
            gridNeedItems, bindInfos, consumedItemBindInfo = self.calculateConsumePlanGridsWithBindTyps(costItemDic, itemBindInfos)
            if not gridNeedItems:
                LOG_WARN('baseMultiEquipEnhance, not enough', costItem, isAddBindStatus)
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
                LOG_WARN('baseMultiEquipEnhance, no bag equip item', uniqueId, bindInfos)
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
        self.cell.cellMultiEquipEnhance(opUUID, bodyEquipInfos, bodyEquipBindInfos, enhanceResults, consumedItemInfos, isMulti)
