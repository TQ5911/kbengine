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
import message_Message_def as M_M_DD
import gearBase_gearBase as GBGBD
import gearBase_gearConst as GBGCD
import itemData_itemData as ITEM_DATA
import gearManufacture_details as GMDD
import agent_agentFunction as A_AFD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import soul_soul as SS_D
import soul_soulRconst as SSRCD
import SoulInfo
import taskClass_taskTarget as TCCTD
import formula_generalFormula as F_GFD
import gearEnhance_gearconst as GE_GC

from proto.gameServerDrop_pb2 import DropResult_SUCCESS,\
    DropResult_NOT_FOUND,\
    DropResult_NOT_OWNER,\
    DropResult_EXPIRE,\
    DropResult_OTHER_GIVEUP,\
    DropResult_OTHER_REDEEM, \
    DropResult_REDEEM_NOT_SET_PRICE, \
    DropResult_SET_PAY_PRICE_NOT_SAME

import LogTrackingMgr

class ImpEquipment(object):
    # 需要绑定值
    NEED_BIND_VALUE_METHOD = (
        'bagEquipUpgradeDeductItemsCB',
        'cellEquipUpgrade',
        'bagEquipBlessDeductItemsCB',
        'cellEquipBless'
    )
    # 需要绑定和非绑定值
    NEED_BIND_AND_UNBIND_VALUE_METHOD = (
        'bagEquipSpiritWashingPreviewCB',
        'cellEquipSpiritWashingPreview',
        'bagEquipSoulSocketDeductItemsCB',
        'bodyEquipSoulSocketDeductItemsCB',
        'bagEquipGlyphWashingPreviewCB',
        'cellEquipGlyphWashingPreview',
        'bagSoulWashDeductCB',
        'bagEquipSoulWashDeductCB',
        'cellEquipSoulWashPreview',
        'bagSoulClashDeductCB',
        'bagEquipSoulClashDeductCB',
        'bodyEquipSoulClashDeductCB',
        'bagSoulDefReplaceDeductCB',
        'bagEquipSoulDefReplaceDeductCB',
        'bodyEquipSoulDefReplaceDeductCB',
    )

    def __init__(self):
        super(ImpEquipment, self).__init__()
        self.createTempEvent(gameconst.EntityPropsEnum.clientInitEvent)

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
            # 检查下特殊装备消耗
            isGood = consumeBagEquipItem.isGood(self.gbID)
            if not isGood:
                self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
                LOG_ERR('   in calculateUpgradeConditions, invalid comsume grid item is not good', consumeGridId, consumeBagEquipItem.getGrade(), grade, isGood)
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
        res = self.canDeductWealth(deductWealthVal, not autoBuy)
        if res:
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
                self.bagData.deductItemsByGridId(self, needGridIdList, opUUID, srcType, detail)
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            LOG_INFO('in baseEquipDeductItems ', methodName, args)
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_STAT_OK, bindValue, unbindValue)
            return
        else:
            self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_ARG_ERR, 0, 0)
            LOG_WARN('   in baseEquipDeductItems, canDeductWealth fail:', opUUID, res())

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

    def baseEquipWashDeductItems(self, costItemDic, opUUID, srcType, detail, box, methodName, args):
        """洗涤专用扣除接口，只扣非绑定物品"""
        LOG_INFO('in baseEquipWashDeductItems:', costItemDic, opUUID, srcType, detail, methodName, args)
        if self.bagData.isLocked():
            LOG_WARN('in baseEquipWashDeductItems, bagData locked!')
            hasattr(box, methodName) and getattr(box, methodName)(gameconst.BagOPStat.OPERATE_BAG_BAG_LOCKED, *args)
            return
        if self.checkPopupSecondaryPassword([(gameconst.SecondaryPasswordCheckType.ITEM_WASH,)]):
            LOG_WARN('in reqSaleItemInLease, need popup sp!')
            hasattr(box, methodName) and getattr(box, methodName)(gameconst.BagOPStat.OPERATE_BAG_FAIL, *args)
            return

        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costItemDic.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum, gameconst.ItemBindType.NORMAL)

        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_WARN('in baseEquipWashDeductItems, item is not enough', res())
            opStat = gameconst.BagOPStat.OPERATE_BAG_ITEMS_NOT_ENOUGH
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                opStat = gameconst.BagOPStat.OPERATE_BAG_FAIL
            hasattr(box, methodName) and getattr(box, methodName)(opStat, *args)
            return

        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
        hasattr(box, methodName) and getattr(box, methodName)(gameconst.BagOPStat.OPERATE_BAG_STAT_OK, *args)
        return
    
    def baseEquipDeductItemsWithBindTypes(self, costCurrencies, costItems, itemIds, bindTypes, opUUID, srcType, detail, box, methodName, args):
        LOG_INFO('in baseEquipDeductItemsWithBindTypes:', costCurrencies, costItems, itemIds, bindTypes, opUUID, srcType, detail, box, methodName, args)
        if 'cellEquipGlyphWashingPreview' == methodName:
            if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipRunePage, 
                                                A_ACD.datas['restrictedPromptMsg1']['value']):
                return

        elif 'cellEquipBless' == methodName:
            if not self.checkAuthDisassembleAndMsg(A_AFD.UIEquipBlessPage, 
                                                A_ACD.datas['restrictedPromptMsg1']['value']):
                return

        elif 'cellEquipSpiritWashingPreview' == methodName:
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

        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_WARN('in baseEquipDeductItemsWithBindTypes, item is not enough', res())
            opStat = gameconst.BagOPStat.OPERATE_BAG_ITEMS_NOT_ENOUGH
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                opStat = gameconst.BagOPStat.OPERATE_BAG_FAIL
            self.equipMethodCallback(opUUID, box, methodName, args, opStat, 0, 0)
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
        
        self.bagData.deductItemsByGridId(self, gridNeedItems, opUUID, srcType, detail)

        deductWealthVal = dropAward.DeductWealthVal()
        for itemId, itemNum in costCurrencies.items():
            deductWealthVal.addWealthByItemId(itemId, itemNum)

        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
        self.equipMethodCallback(opUUID, box, methodName, args, gameconst.BagOPStat.OPERATE_BAG_STAT_OK, bindInfos[0], bindInfos[1])
        LOG_INFO('in baseEquipDeductItemsWithBindTypes ', methodName, args)

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def dressEquipment(self, exposed, gridId, dressType, dstSlotId):
        LOG_INFO('in dressEquipment:', gridId, dressType, dstSlotId, self.baseSpaceNo)
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_dressEquipment', (gridId, dressType, dstSlotId))
        else:
            self._dressEquipment(gridId, dressType, dstSlotId)

    def _dressEquipment(self, gridId, dressType, dstSlotId):
        if self.bagData.doDressEquip(self, gridId, dressType, dstSlotId):
            self.syncMethodCallToCrossServerBase('_dressEquipment', (gridId, dressType, dstSlotId))

    def dressEquipmentCB(self, uniqId, result, bagEquipDic):
        LOG_INFO('in dressEquipmentCB:', uniqId, result)
        self.bagData.doDressEquipCB(self, uniqId, result)
        if result != gameconst.DressEquipOpEnum.EQUIP_OP_FAILED:
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
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_undressEquipment', (slotId,))
        else:
            self._undressEquipment(slotId)

    def _undressEquipment(self, slotId):
        if self.bagData.isFull():
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
            return

        if not self.bagData.tryLockBag(lockDesc='undressEquipment, slotId:%s'%(slotId)):
            LOG_ERR('in undressEquipment, lock bag fail:', self.bagData.lockDesc, slotId)
            return

        self.cell.cellUndressEquipment(slotId)
        self.syncMethodCallToCrossServerBase('_undressEquipment', (slotId,))

    def updateAccountCharacterAppearance(self, updateDic):
        self.accountEntity.updateAppearance(self.gbID, updateDic)
        if self.subAccount:
            self.subAccount.updateAppearance(self.gbID, updateDic)

    def cellUndressEquipmentSucc(self, opUUID, bodyEquipDic):
        LOG_INFO('in cellUndressEquipmentSucc', opUUID)
        self.unlockBag()
        _opStat, _equipItem, _srcType = self.bagData.doBagUndressEquip(self, opUUID, bodyEquipDic)
        if _opStat == gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            return
        # 背包放不下（或被锁住）时不能把玩家身上的装备直接丢掉，
        # 按工程既有惯例改走邮件把装备发回给玩家
        LOG_WARN('in cellUndressEquipmentSucc, add item to bag failed, send by mail:', _opStat, _equipItem.itemId)
        equipUndressReturnMail = int(GE_GC.datas['equipmentReturnMail']['value'])
        _mailWealth = dropAward.MailAttachVal(itemObjs=[_equipItem])
        mailAssistor.sendMailToPlayers([self.gbID], equipUndressReturnMail, extraAttach=_mailWealth, opUUID=opUUID, srcType=_srcType)
    
    def cellUndressEquipmentFail(self, slotId, reason):
        LOG_INFO("cellUndressEquipmentFail::", slotId, reason)
        self.unlockBag(gameconst.BagTypeEnum.BAG_TYPE_NORMAL, reason)

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
        detail = gameclass.AwardDetailCls(uniqueId=bagEquipItem.uniqueId)
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
        bindValueBefore = bagEquipItem.getBindValueByType(gameconst.EquipWashType.UPGRADE)
        bagEquipItem.doUpgradeEquip(self, opUUID, upgradeType, targetLv)
        # 记录升阶消耗的绑定装备件数（用于装备洗涤）
        if bindValue > 0:
            bagEquipItem.addBindValue(bindValue)
        bindValueAfter = bagEquipItem.getBindValueByType(gameconst.EquipWashType.UPGRADE)

        equipAttrsBefore = {
                'baseAttrs':baseAttrsBefore,
                'upgradeAttrs':upgradeAttrsBefore,
                'enhanceAttrs':enhanceAttrsBefore,
            }
        
        equipAttrsAfter = {
            'baseAttrs':bagEquipItem.getBaseAttrs(),
            'upgradeAttrs':bagEquipItem.getUpgradeAttrs(),
            'enhanceAttrs':bagEquipItem.getEnhanceAttrs(),
        }
        

        LogTrackingMgr.LogTrackingMgr.equip_upgrade(self.gbID, self.accountEntity.clientDistinctId, opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, bagEquipItem.getItemName(), bagEquipItem.getEquipType(), \
                                                    bagEquipItem.getGrade(), bagEquipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, baseAttrsBefore, enhanceAttrsBefore, upgradeAttrsBefore, \
                                                    bagEquipItem.getBaseAttrs(), bagEquipItem.getEnhanceAttrs(), bagEquipItem.getUpgradeAttrs(), gradeBefore, bagEquipItem.getGrade(), bindValueBefore, bindValueAfter, \
                                                    bagEquipItem.getEquipScore(), equipAttrsBefore, equipAttrsAfter)

        self.client.onEquipUpgradeSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getGrade(), bagEquipItem.getEquipScore(), bagEquipItem.getOriginalBindValue(), bagEquipItem.equipAttr.bindValue, bagEquipItem.bindType)
        return

    def bagEquipGlyphWashing(self, gridId, uniqueId, glyphPos, itemIds, bindTypes, isAuto):
        LOG_INFO('in bagEquipGlyphWashing:', gridId, uniqueId, glyphPos, itemIds, bindTypes, isAuto)
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
        
        detail = gameclass.AwardDetailCls(uniqueId=bagEquipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                    'bagEquipGlyphWashingPreviewCB', (opUUID, gridId, glyphPos, isAuto))
        
        return

    def bagEquipGlyphWashingPreviewCB(self, opStat, bindValue, unbindValue, opUUID, gridId, glyphPos, isAuto):
        LOG_INFO('in bagEquipGlyphWashingPreviewCB:', opStat, bindValue, unbindValue, opUUID, gridId, glyphPos, isAuto)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipGlyphWashingPreviewCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_WARN('   in bagEquipGlyphWashingPreviewCB, equip not found:', gridId)
            return

        glyphDataBefore = bagEquipItem.getGlyphDatas()

        ret, _, _ = bagEquipItem.doEquipGlyphWashingPreview(self, glyphPos, unbindValue)
        if not ret:
            LOG_ERR('   in bagEquipGlyphWashingPreviewCB, calc preview failed:', gridId, glyphPos)
            return

        previewGlyphData = bagEquipItem.equipAttr.previewGlyphDatas[glyphPos]
        previewScore = bagEquipItem.calcGlyphWashingPreviewScore(glyphPos)
        glyphBindType = gameconst.ItemBindType.BIND if bindValue > 0 else gameconst.ItemBindType.NORMAL
        bagEquipItem.setPreviewGlyphBindType(glyphPos, glyphBindType)
        self.client.onEquipGlyphWashingPreview(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos,
                                                previewGlyphData.toClientData(), previewScore,
                                                glyphBindType, bagEquipItem.bindType, opUUID)

        self.triggerAchievement(gameconst.AchieveType.INSCRIPTION)

        LogTrackingMgr.LogTrackingMgr.equip_glyph(
            self.gbID,
            self.accountEntity.clientDistinctId,
            opUUID,
            'wash',
            self.gbID,
            bagEquipItem.uniqueId,
            bagEquipItem.itemId,
            bagEquipItem.getItemName(),
            bagEquipItem.getEquipType(),
            bagEquipItem.getGrade(),
            bagEquipItem.getQuality(),
            gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
            glyphDataBefore,
            bagEquipItem.getPreviewGlyphDatas(),
            bindValue,
            previewScore,
            bagEquipItem.getGlyphGroupId(),
            glyphPos,
            bagEquipItem.getBindValueByType(gameconst.EquipWashType.GLYPH, glyphPos),
            bagEquipItem.getBindValueByType(gameconst.EquipWashType.GLYPH, glyphPos),
            isAuto,
        )
        return

    def bagEquipGlyphWashingConfirm(self, gridId, glyphPos, uniqueId):
        LOG_INFO('in bagEquipGlyphWashingConfirm:', gridId, glyphPos, uniqueId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem or bagEquipItem.uniqueId != uniqueId:
            LOG_WARN('   in bagEquipGlyphWashingConfirm, equip not found or uniqueId not matched:', gridId, uniqueId)
            self.client.onEquipGlyphWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos)
            return

        if glyphPos >= len(bagEquipItem.equipAttr.previewGlyphDatas):
            LOG_WARN('   in bagEquipGlyphWashingConfirm, preview data not found:', gridId, glyphPos)
            self.client.onEquipGlyphWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos)
            return

        previewGlyphData = bagEquipItem.equipAttr.previewGlyphDatas[glyphPos]
        if not previewGlyphData or len(previewGlyphData.getGlyphAffixes()) == 0:
            LOG_WARN('   in bagEquipGlyphWashingConfirm, preview data is empty:', gridId, glyphPos)
            self.client.onEquipGlyphWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos)
            return

        glyphDataBefore = bagEquipItem.getGlyphDatas()
        glyphBindValueBefore = bagEquipItem.getBindValueByType(gameconst.EquipWashType.GLYPH, glyphPos)

        ret = bagEquipItem.doEquipGlyphWashingConfirm(self, glyphPos, onBody=False)
        if not ret:
            LOG_ERR('   in bagEquipGlyphWashingConfirm, apply failed:', gridId, glyphPos)
            self.client.onEquipGlyphWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos)
            return

        # confirm 后获取实际绑定状态
        glyphBindType = gameconst.ItemBindType.BIND if glyphPos in bagEquipItem.equipAttr.glyphBindTypes else gameconst.ItemBindType.NORMAL
        glyphBindValueAfter = bagEquipItem.getBindValueByType(gameconst.EquipWashType.GLYPH, glyphPos)
        glyphData = bagEquipItem.equipAttr.getGlyphData(glyphPos)
        self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.INSCRIPTION, actionContext.AchievementCtx())

        self.client.onEquipGlyphWashingSucc(
            gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
            gridId, glyphPos,
            glyphData.toClientData(),
            bagEquipItem.getEquipScore(),
            glyphBindType,
            bagEquipItem.bindType
        )

        LogTrackingMgr.LogTrackingMgr.equip_glyph(
            self.gbID,
            self.accountEntity.clientDistinctId,
            0,
            'confirm',
            self.gbID,
            bagEquipItem.uniqueId,
            bagEquipItem.itemId,
            bagEquipItem.getItemName(),
            bagEquipItem.getEquipType(),
            bagEquipItem.getGrade(),
            bagEquipItem.getQuality(),
            gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
            glyphDataBefore,
            bagEquipItem.getGlyphDatas(),
            glyphBindValueBefore,
            bagEquipItem.getEquipScore(),
            bagEquipItem.getGlyphGroupId(),
            glyphPos,
            glyphBindValueBefore,
            glyphBindValueAfter,
            0,
        )
        return

    def bagEquipGlyphWashingDiscard(self, gridId, glyphPos, uniqueId):
        LOG_INFO('in bagEquipGlyphWashingDiscard:', gridId, glyphPos, uniqueId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem or bagEquipItem.uniqueId != uniqueId:
            LOG_WARN('   in bagEquipGlyphWashingDiscard, equip not found or uniqueId not matched:', gridId, uniqueId)
            self.client.onEquipGlyphWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, 0)
            return

        if glyphPos >= len(bagEquipItem.equipAttr.previewGlyphDatas):
            LOG_WARN('   in bagEquipGlyphWashingDiscard, preview data not found:', gridId, glyphPos)
            self.client.onEquipGlyphWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, 0)
            return

        previewGlyphData = bagEquipItem.equipAttr.previewGlyphDatas[glyphPos]
        if not previewGlyphData or len(previewGlyphData.getGlyphAffixes()) == 0:
            LOG_WARN('   in bagEquipGlyphWashingDiscard, preview data is empty:', gridId, glyphPos)
            self.client.onEquipGlyphWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, 0)
            return

        ret = bagEquipItem.doEquipGlyphWashingDiscard(self, glyphPos)
        if not ret:
            LOG_ERR('   in bagEquipGlyphWashingDiscard, discard failed:', gridId, glyphPos)
            self.client.onEquipGlyphWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, 0)
            return

        self.client.onEquipGlyphWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos, 1)
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

    def bagEquipBless(self, gridId, uniqueId, itemIds, bindTypes, isAuto):
        LOG_INFO('in bagEquipBless:', gridId, uniqueId, itemIds, bindTypes, isAuto)
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
        
        detail = gameclass.AwardDetailCls(uniqueId=bagEquipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                    'bagEquipBlessDeductItemsCB', (opUUID, gridId, isAuto))
        
        return

    def bagEquipBlessDeductItemsCB(self, opStat, bindValue, opUUID, gridId, isAuto):
        LOG_INFO('in bagEquipBlessDeductItemsCB:', opStat, bindValue, opUUID, gridId, isAuto)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipBlessDeductItemsCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)

        blessDataBefore = bagEquipItem.getBlessDatas()
        blessLvRateBefore = bagEquipItem.getBlessLvRate()
        maxBlessLvBefore = bagEquipItem.getBlessMaxLv()
        bindValueBefore = bagEquipItem.getBindValueByType(gameconst.EquipWashType.BLESS)

        if bindValue > 0:
            # 记录祝福消耗的绑定祝福石数量（用于装备洗涤）
            bagEquipItem.addBindBlessCost(bindValue)
        if bagEquipItem.doEquipBlessing():

            bindValueAfter = bagEquipItem.getBindValueByType(gameconst.EquipWashType.BLESS)
            LogTrackingMgr.LogTrackingMgr.equip_bless(self.gbID, self.accountEntity.clientDistinctId, opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, bagEquipItem.getItemName(), bagEquipItem.getEquipType(), \
                                                        bagEquipItem.getGrade(), bagEquipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, blessDataBefore, \
                                                        bagEquipItem.getBlessDatas(), bindValue, blessLvRateBefore, \
                                                        bagEquipItem.getBlessLvRate(), maxBlessLvBefore, bagEquipItem.getBlessMaxLv(), bagEquipItem.getEquipScore(), bindValueBefore, bindValueAfter, isAuto)

            blessAffixes = []
            for oneAffix in bagEquipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, blessAffixes, bagEquipItem.equipAttr.maxBlessLv, \
                                         bagEquipItem.equipAttr.blessLvRate, bagEquipItem.getEquipScore(), bagEquipItem.equipAttr.bindBlessCost, \
                                         bagEquipItem.bindType, bagEquipItem.getBlessFailLevels(), bagEquipItem.getBlessFailCounts())
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

        oldBlessLvRate = bagEquipItem.getBlessLvRate()
        oldBlessData = bagEquipItem.getBlessDatas()
        oldMaxBlessLv = bagEquipItem.getBlessMaxLv()
        
        bagEquipItem.doEquipBackBless()

        LogTrackingMgr.LogTrackingMgr.equip_bless_back(self.gbID, self.accountEntity.clientDistinctId, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, bagEquipItem.getItemName(), 
                                                       bagEquipItem.getEquipType(), bagEquipItem.getGrade(), bagEquipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, 
                                                       oldBlessData, bagEquipItem.getBlessDatas(), oldBlessLvRate, bagEquipItem.getBlessLvRate(), oldMaxBlessLv, bagEquipItem.getBlessMaxLv(), 
                                                       bagEquipItem.getEquipScore())

        self.client.onEquipBackBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getBlessDatas(),
                                         bagEquipItem.getBlessMaxLv(), bagEquipItem.getBlessLvRate(), bagEquipItem.getEquipScore())

    def bagEquipSpiritWashing(self, gridId, uniqueId, spiritPos, itemIds, bindTypes, isAuto):
        LOG_INFO('in bagEquipSpiritWashing:', gridId, uniqueId, spiritPos, itemIds, bindTypes, isAuto)
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
            return

        if not bagEquipItem.checkSpiritNum(spiritPos):
            LOG_ERR('bagEquipSpiritWashing slot is empty')
            return

        costItemDic, costCurrencyDic = bagEquipItem.spiritWashingNeedItems()
        if not costItemDic or not costCurrencyDic:
            LOG_ERR('     bagEquipSpiritWashing, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_AFFIX_WASHING
            
        detail = gameclass.AwardDetailCls(uniqueId=bagEquipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                    'bagEquipSpiritWashingPreviewCB', (opUUID, gridId, spiritPos, isAuto))
        
        return

    def bagEquipSpiritWashingPreviewCB(self, opStat, bindValue, unbindValue, opUUID, gridId, spiritPos, isAuto):
        LOG_INFO('in bagEquipSpiritWashingPreviewCB:', opStat, bindValue, unbindValue, opUUID, gridId, spiritPos, isAuto)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipSpiritWashingPreviewCB, deduct items error')
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem:
            LOG_WARN('   in bagEquipSpiritWashingPreviewCB, equip not found:', gridId)
            return

        spiritDataBefore = bagEquipItem.getSpiritDatas()

        ret, _, _ = bagEquipItem.doEquipSpiritWashingPreview(self, spiritPos, unbindValue)
        if not ret:
            LOG_ERR('   in bagEquipSpiritWashingPreviewCB, calc preview failed:', gridId, spiritPos)
            return

        previewSpiritData = bagEquipItem.equipAttr.previewSpiritDatas[spiritPos]
        previewScore = bagEquipItem.calcSpiritWashingPreviewScore(spiritPos)
        spiritBindType = gameconst.ItemBindType.BIND if bindValue > 0 else gameconst.ItemBindType.NORMAL
        bagEquipItem.setPreviewSpiritBindType(spiritPos, spiritBindType)
        self.client.onEquipSpiritWashingPreview(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos,
                                                previewSpiritData.toClientData(), previewScore,
                                                spiritBindType, bagEquipItem.bindType, opUUID)

        self.triggerAchievement(gameconst.AchieveType.EQUIPMENT_WITH_SPIRIT)

        LogTrackingMgr.LogTrackingMgr.equip_spirit(
            self.gbID,
            self.accountEntity.clientDistinctId,
            opUUID,
            'wash',
            bagEquipItem.uniqueId,
            bagEquipItem.itemId,
            bagEquipItem.getItemName(),
            bagEquipItem.getEquipType(),
            bagEquipItem.getGrade(),
            bagEquipItem.getQuality(),
            gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
            spiritDataBefore,
            bagEquipItem.getPreviewSpiritDatas(),
            bagEquipItem.getBindValueByType(gameconst.EquipWashType.SPIRIT, spiritPos),
            gameconst.ItemBindType.BIND if bagEquipItem.isPreviewSpiritBindType(spiritPos) else gameconst.ItemBindType.NORMAL,
            bagEquipItem.getEquipScore(),
            spiritPos,
            isAuto,
        )
        return

    def bagEquipSpiritWashingConfirm(self, gridId, spiritPos, uniqueId):
        LOG_INFO('in bagEquipSpiritWashingConfirm:', gridId, spiritPos, uniqueId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem or bagEquipItem.uniqueId != uniqueId:
            LOG_WARN('   in bagEquipSpiritWashingConfirm, equip not found or uniqueId not matched:', gridId, uniqueId)
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos)
            return

        if spiritPos >= len(bagEquipItem.equipAttr.previewSpiritDatas):
            LOG_WARN('   in bagEquipSpiritWashingConfirm, preview data not found:', gridId, spiritPos)
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos)
            return

        previewSpiritData = bagEquipItem.equipAttr.previewSpiritDatas[spiritPos]
        if not previewSpiritData or len(previewSpiritData.GetSpiritAffixes()) == 0:
            LOG_WARN('   in bagEquipSpiritWashingConfirm, preview data is empty:', gridId, spiritPos)
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos)
            return

        spiritDataBefore = bagEquipItem.getSpiritDatas()
        spiritBindValueBefore = bagEquipItem.getBindValueByType(gameconst.EquipWashType.SPIRIT, spiritPos)

        ret = bagEquipItem.doEquipSpiritWashingConfirm(self, spiritPos, onBody=False)
        if not ret:
            LOG_ERR('   in bagEquipSpiritWashingConfirm, apply failed:', gridId, spiritPos)
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos)
            return

        # confirm 后读取实际绑定状态
        spiritBindType = gameconst.ItemBindType.BIND if bagEquipItem.isSpiritBindType(spiritPos) else gameconst.ItemBindType.NORMAL
        spiritBindValueAfter = bagEquipItem.getBindValueByType(gameconst.EquipWashType.SPIRIT, spiritPos)
        spiritData = bagEquipItem.equipAttr.spiritDatas[spiritPos]
        self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.EQUIPMENT_WITH_SPIRIT, actionContext.AchievementCtx())

        self.client.onEquipSpiritWashingSucc(
            gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
            gridId, spiritData.toClientData(),
            spiritPos,
            bagEquipItem.getEquipScore(),
            spiritBindType,
            bagEquipItem.bindType
        )

        LogTrackingMgr.LogTrackingMgr.equip_spirit(
            self.gbID,
            self.accountEntity.clientDistinctId,
            0,
            'confirm',
            bagEquipItem.uniqueId,
            bagEquipItem.itemId,
            bagEquipItem.getItemName(),
            bagEquipItem.getEquipType(),
            bagEquipItem.getGrade(),
            bagEquipItem.getQuality(),
            gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
            spiritDataBefore,
            bagEquipItem.getSpiritDatas(),
            spiritBindValueBefore,
            spiritBindValueAfter,
            bagEquipItem.getEquipScore(),
            spiritPos,
            0,
        )
        return

    def bagEquipSpiritWashingDiscard(self, gridId, spiritPos, uniqueId):
        LOG_INFO('in bagEquipSpiritWashingDiscard:', gridId, spiritPos, uniqueId)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem or bagEquipItem.uniqueId != uniqueId:
            LOG_WARN('   in bagEquipSpiritWashingDiscard, equip not found or uniqueId not matched:', gridId, uniqueId)
            self.client.onEquipSpiritWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos, 0)
            return

        if spiritPos >= len(bagEquipItem.equipAttr.previewSpiritDatas):
            LOG_WARN('   in bagEquipSpiritWashingDiscard, preview data not found:', gridId, spiritPos)
            self.client.onEquipSpiritWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos, 0)
            return

        previewSpiritData = bagEquipItem.equipAttr.previewSpiritDatas[spiritPos]
        if not previewSpiritData or len(previewSpiritData.GetSpiritAffixes()) == 0:
            LOG_WARN('   in bagEquipSpiritWashingDiscard, preview data is empty:', gridId, spiritPos)
            self.client.onEquipSpiritWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos, 0)
            return

        ret = bagEquipItem.doEquipSpiritWashingDiscard(self, spiritPos)
        if not ret:
            LOG_ERR('   in bagEquipSpiritWashingDiscard, discard failed:', gridId, spiritPos)
            self.client.onEquipSpiritWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos, 0)
            return

        self.client.onEquipSpiritWashingDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritPos, 1)
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

        if soulItem.itemSubType not in gameconst.ItemSubEnum.EQUIP_SOUL_TYPE:
            LOG_ERR('bagEquipSoulSocket, soulGridId is not soul item:', soulGridId)
            return

        soulData = SS_D.datas.get(soulItem.itemId, None)
        if not soulData:
            LOG_ERR('bagEquipSoulSocket, soulItem is not soul item:', soulItem.itemId)
            return

        if soulData['equipmentID'] != bagEquipItem.equipAttr.equipType:
            LOG_ERR('bagEquipSoulSocket, equipType is not match:', soulItem.itemId, bagEquipItem.equipAttr.equipType)
            return

        if utils.soulInlayForbidden(soulItem.quality, bagEquipItem.getQuality()):
            LOG_ERR('bagEquipSoulSocket, inlayRange forbid:', soulItem.itemId, soulItem.quality, bagEquipItem.getQuality())
            return

        costItemDic, costCurrencyDic = bagEquipItem.soulSocketNeedItems()
        if not costCurrencyDic:
            LOG_ERR('     bagEquipSoulSocket, cost is empty:')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_SOUL
        
        detail = gameclass.AwardDetailCls(uniqueId=bagEquipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                    'bagEquipSoulSocketDeductItemsCB', (opUUID, gridId, soulGridId))
        
        return

    def _doDeductSoulItem(self, opUUID, soulGridId):
        soulItem = self.bagData.getItemObjByGridId(soulGridId)
        if not soulItem:
            LOG_ERR('_doDeductSoulItem, soulGridId is invalid:', soulGridId)
            return None, None, None

        soulPayload = soulItem.exportSoulPayload()
        if not SoulInfo.hasAnyProp(soulPayload):
            LOG_ERR('_doDeductSoulItem, soul has no affix:', soulGridId, soulItem.itemId)
            return None, None, None
        soulItemId = soulItem.itemId
        soulBindType = soulItem.bindType

        _srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_SOUL
        bagType = self.bagData.bagType
        detail = gameclass.AwardDetailCls(bagType=bagType, gridId=soulGridId, itemId=soulItem.itemId)
        _cleanItem = self.bagData.cleanGridByGridId(self, soulGridId, soulItem.itemId, opUUID, _srcType, detail)
        if not _cleanItem:
            LOG_ERR('in _doDeductSoulItem, cleanGridByGridId error')
            return None, None, None

        return soulPayload, soulItemId, soulBindType

    @gamedecorator.checkGameconfigEnable('equip_soulWash')
    def reqSoulWash(self, exposed, gridId, uniqueId, itemIds, bindTypes):
        LOG_INFO('in reqSoulWash:', gridId, uniqueId, itemIds, bindTypes)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if not soulItem:
            self.client.onSoulWashPreview(0, gridId, uniqueId, 0, [], [])
            return
        payload = soulItem.exportSoulPayload()
        if not payload['defLevel']:
            LOG_ERR('reqSoulWash, defLevel is 0:', gridId, soulItem.itemId)
            self.client.onSoulWashPreview(0, gridId, uniqueId, 0, [], [])
            return
        if not self.getRoleCacheAttr('school'):
            LOG_ERR('reqSoulWash, school missing:', gridId)
            self.client.onSoulWashPreview(0, gridId, uniqueId, 0, [], [])
            return
        cost = utils.soulWashCost(payload['defLevel'])
        if not cost:
            LOG_ERR('reqSoulWash, cost missing:', payload['defLevel'])
            self.client.onSoulWashPreview(0, gridId, uniqueId, 0, [], [])
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_SOUL_REFINED_COST
        costItems = {}
        if cost['fragmentNum'] > 0:
            costItems[cost['fragmentItemId']] = cost['fragmentNum']
        costCurrency = {cost['ironItemId']: cost['ironNum']}
        detail = gameclass.AwardDetailCls(uniqueId=soulItem.uniqueId, costCurrencyDic=costCurrency, costItemDic=costItems)
        self.baseEquipDeductItemsWithBindTypes(
            costCurrency, costItems, itemIds, bindTypes, opUUID, srcType, detail, self,
            'bagSoulWashDeductCB', (opUUID, gridId, uniqueId))

    def bagEquipSoulWash(self, equipPos, uniqueId, itemIds, bindTypes):
        LOG_INFO('in bagEquipSoulWash:', equipPos, uniqueId, itemIds, bindTypes)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        if not equipItem:
            self.client.onEquipSoulWashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0, [], [], 0)
            return
        payload = equipItem.equipAttr.soulPayload()
        if not self._beginSoulWashDeduct(equipItem.uniqueId, payload['defLevel'], itemIds, bindTypes,
                                         'bagEquipSoulWashDeductCB', (equipPos, uniqueId)):
            self.client.onEquipSoulWashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0, [], [], 0)

    def bodyEquipSoulWash(self, equipPos, uniqueId, defLevel, itemIds, bindTypes):
        LOG_INFO('in bodyEquipSoulWash:', equipPos, uniqueId, defLevel, itemIds, bindTypes)
        if not self._beginSoulWashDeduct(uniqueId, defLevel, itemIds, bindTypes,
                                         'cellEquipSoulWashPreview', (equipPos, uniqueId), box=self.cell):
            self.client.onEquipSoulWashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId, 0, [], [], 0)

    def bagEquipSoulWashDeductCB(self, opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId):
        LOG_INFO('in bagEquipSoulWashDeductCB:', opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK or not equipItem:
            self.client.onEquipSoulWashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0, [], [], 0)
            return
        if not self._saveEquipSoulWashPreview(equipItem, self.getRoleCacheAttr('school'), bindValue):
            self.client.onEquipSoulWashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0, [], [], 0)
            return
        payload = SoulInfo.readEquip(equipItem.equipAttr)
        preview = payload['previewWash']
        self._syncBagSoulItem(equipPos, equipItem)
        self._sendEquipSoulWashPreview(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, equipItem)
        self._trackSoul(
            'Soul_Wash_Normal', opUUID, None, equipItem, SoulInfo.calcBindType(payload), payload,
            afterBase=preview['baseProps'], afterLucky=preview['luckyProp'], affixOpType='wash')

    def bagEquipSoulWashConfirm(self, equipPos, uniqueId):
        LOG_INFO('in bagEquipSoulWashConfirm:', equipPos, uniqueId)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        before = SoulInfo.readEquip(equipItem.equipAttr) if equipItem else None
        if not equipItem or not self._keepEquipSoulWash(equipItem):
            bindType = equipItem.equipAttr.soulBindType if equipItem else 0
            bindFromWash = equipItem.equipAttr.soulBindFromWash if equipItem else 0
            self.client.onEquipSoulWashConfirm(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, bindType, [], [], bindFromWash)
            return
        after = SoulInfo.readEquip(equipItem.equipAttr)
        self._syncBagSoulItem(equipPos, equipItem)
        self._sendEquipSoulWashConfirm(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, equipItem)
        self._trackSoul(
            'Soul_Wash_Normal', KBEngine.genUUID64(), None, equipItem, SoulInfo.calcBindType(after), before,
            afterBase=after['baseProps'], afterLucky=after['luckyProp'], affixOpType='confirm')

    def bagEquipSoulWashDiscard(self, equipPos, uniqueId):
        LOG_INFO('in bagEquipSoulWashDiscard:', equipPos, uniqueId)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        if not equipItem or not self._discardEquipSoulWash(equipItem):
            LOG_WARN('   in bagEquipSoulWashDiscard, preview not found:', equipPos, uniqueId)
            self.client.onEquipSoulWashDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0)
            return
        self._syncBagSoulItem(equipPos, equipItem)
        self.client.onEquipSoulWashDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 1)

    def _beginSoulWashDeduct(self, uniqueId, defLevel, itemIds, bindTypes, methodName, args, box=None):
        if not defLevel:
            LOG_ERR('_beginSoulWashDeduct, defLevel is 0:', uniqueId)
            return False
        if not self.getRoleCacheAttr('school'):
            LOG_ERR('_beginSoulWashDeduct, school missing:', uniqueId)
            return False
        cost = utils.soulWashCost(defLevel)
        if not cost:
            LOG_ERR('_beginSoulWashDeduct, cost missing:', defLevel)
            return False
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_SOUL_REFINED_COST
        costItems = {}
        if cost['fragmentNum'] > 0:
            costItems[cost['fragmentItemId']] = cost['fragmentNum']
        costCurrency = {cost['ironItemId']: cost['ironNum']}
        detail = gameclass.AwardDetailCls(uniqueId=uniqueId, costCurrencyDic=costCurrency, costItemDic=costItems)
        self.baseEquipDeductItemsWithBindTypes(
            costCurrency, costItems, itemIds, bindTypes, opUUID, srcType, detail, box or self,
            methodName, (opUUID,) + tuple(args))
        return True

    def _saveEquipSoulWashPreview(self, equipItem, schoolId, bindValue):
        preview = SoulInfo.previewEquipWash(equipItem.equipAttr, schoolId, not bindValue)
        if not preview:
            LOG_ERR('_saveEquipSoulWashPreview, preview failed:', equipItem.uniqueId)
            return None
        payload = SoulInfo.readEquip(equipItem.equipAttr)
        payload['previewWash']['materialBound'] = 1 if bindValue else 0
        SoulInfo.writeEquip(equipItem.equipAttr, payload)
        equipItem.equipAttr.setDirtyFlag()
        return payload['previewWash']

    def _keepEquipSoulWash(self, equipItem):
        payload = SoulInfo.keepEquipWash(equipItem.equipAttr)
        if not payload:
            return None
        equipItem.refreshSoulBindFromPayload()
        equipItem.equipAttr.calcScore()
        equipItem.equipAttr.setDirtyFlag()
        return payload

    def _discardEquipSoulWash(self, equipItem):
        payload = SoulInfo.discardEquipWash(equipItem.equipAttr)
        if not payload:
            return None
        equipItem.equipAttr.setDirtyFlag()
        return payload

    def _sendEquipSoulWashPreview(self, equipIn, equipPos, equipItem):
        preview = equipItem.equipAttr.soulPayload()['previewWash']
        lucky = [preview['luckyProp']] if preview and preview['luckyProp'] else []
        baseProps = preview['baseProps'] if preview else []
        materialBound = preview.get('materialBound', 0) if preview else 0
        self.client.onEquipSoulWashPreview(
            1, equipIn, equipPos, equipItem.uniqueId, equipItem.equipAttr.soulBindType,
            SoulInfo.propsToClient(baseProps), SoulInfo.propsToClient(lucky), materialBound)

    def _sendEquipSoulWashConfirm(self, equipIn, equipPos, equipItem):
        payload = equipItem.equipAttr.soulPayload()
        lucky = [payload['luckyProp']] if payload['luckyProp'] else []
        self.client.onEquipSoulWashConfirm(
            1, equipIn, equipPos, equipItem.uniqueId, equipItem.equipAttr.soulBindType,
            SoulInfo.propsToClient(payload['baseProps']), SoulInfo.propsToClient(lucky),
            payload['bindFromWash'])

    def _getBagEquipWithSoul(self, gridId, uniqueId):
        equipItem = self.bagData.getItemObjByGridId(gridId)
        if not equipItem or equipItem.uniqueId != uniqueId or not equipItem.isEquipmentItem():
            LOG_ERR('_getBagEquipWithSoul, invalid equip:', gridId, uniqueId)
            return None
        if dataUtils.checkEquipGrowingForbidden(self.gbID, equipItem):
            LOG_ERR('_getBagEquipWithSoul, equipment can not be growing:', equipItem.itemId)
            return None
        if not equipItem.equipAttr.soulItemId:
            LOG_ERR('_getBagEquipWithSoul, no soul:', gridId, uniqueId)
            return None
        return equipItem

    def bagSoulWashDeductCB(self, opStat, bindValue, unbindValue, opUUID, gridId, uniqueId):
        LOG_INFO('in bagSoulWashDeductCB:', opStat, bindValue, unbindValue, opUUID, gridId, uniqueId)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK or not soulItem:
            self.client.onSoulWashPreview(0, gridId, uniqueId, 0, [], [])
            return
        preview = SoulInfo.previewItemWash(soulItem, self.getRoleCacheAttr('school'), not bindValue)
        if not preview:
            LOG_ERR('bagSoulWashDeductCB, preview failed:', gridId, uniqueId)
            self.client.onSoulWashPreview(0, gridId, uniqueId, 0, [], [])
            return
        payload = SoulInfo.readItem(soulItem)
        payload['previewWash']['materialBound'] = 1 if bindValue else 0
        SoulInfo.writeItem(soulItem, payload)
        self._syncBagSoulItem(gridId, soulItem)
        lucky = [preview['luckyProp']] if preview['luckyProp'] else []
        self.client.onSoulWashPreview(
            1, gridId, uniqueId, soulItem.bindType,
            SoulInfo.propsToClient(preview['baseProps']),
            SoulInfo.propsToClient(lucky))
        self._trackSoul(
            'Soul_Wash_Normal', opUUID, soulItem, None, SoulInfo.calcBindType(payload), payload,
            afterBase=preview['baseProps'], afterLucky=preview['luckyProp'], affixOpType='wash')

    @gamedecorator.checkGameconfigEnable('equip_soulWash')
    def reqSoulWashConfirm(self, exposed, gridId, uniqueId):
        LOG_INFO('in reqSoulWashConfirm:', gridId, uniqueId)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if not soulItem:
            self.client.onSoulWashConfirm(0, gridId, uniqueId, 0, [], [])
            return
        before = SoulInfo.readItem(soulItem)
        payload = SoulInfo.keepItemWash(soulItem)
        if not payload:
            self.client.onSoulWashConfirm(0, gridId, uniqueId, soulItem.bindType, [], [])
            return
        self._syncBagSoulItem(gridId, soulItem)
        lucky = [payload['luckyProp']] if payload['luckyProp'] else []
        self.client.onSoulWashConfirm(
            1, gridId, uniqueId, soulItem.bindType,
            SoulInfo.propsToClient(payload['baseProps']),
            SoulInfo.propsToClient(lucky))
        self._trackSoul(
            'Soul_Wash_Normal', KBEngine.genUUID64(), soulItem, None, SoulInfo.calcBindType(payload), before,
            afterBase=payload['baseProps'], afterLucky=payload['luckyProp'], affixOpType='confirm')

    @gamedecorator.checkGameconfigEnable('equip_soulWash')
    def reqSoulWashDiscard(self, exposed, gridId, uniqueId):
        LOG_INFO('in reqSoulWashDiscard:', gridId, uniqueId)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if not soulItem or not SoulInfo.discardItemWash(soulItem):
            LOG_WARN('   in reqSoulWashDiscard, preview not found:', gridId, uniqueId)
            self.client.onSoulWashDiscardResult(gridId, uniqueId, 0)
            return
        self._syncBagSoulItem(gridId, soulItem)
        self.client.onSoulWashDiscardResult(gridId, uniqueId, 1)

    def _getBagSoulItem(self, gridId, uniqueId):
        soulItem = self.bagData.getItemObjByGridId(gridId)
        if not soulItem or soulItem.uniqueId != uniqueId or not soulItem.isSoul():
            LOG_ERR('_getBagSoulItem, invalid soul:', gridId, uniqueId)
            return None
        return soulItem

    def _trackSoul(self, event, opUUID, soulItem, equipItem, bindType, beforePayload, **kwargs):
        distinctId = self.accountEntity.clientDistinctId if self.accountEntity else ''
        SoulInfo.trackSoul(self.gbID, distinctId, event, opUUID, soulItem, equipItem, bindType, beforePayload, **kwargs)

    def _syncBagSoulItem(self, gridId, soulItem):
        self.client.onUpdateGridItemsJson(
            self.bagData.bagType, gridId, soulItem.uniqueId, soulItem.attr2Json())

    @gamedecorator.checkGameconfigEnable('equip_soulWash')
    def reqSoulClash(self, exposed, gridId, uniqueId, costGridId, costUniqueId, itemIds, bindTypes):
        LOG_INFO('in reqSoulClash:', gridId, uniqueId, costGridId, costUniqueId, itemIds, bindTypes)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if not soulItem or gridId == costGridId:
            self.client.onSoulClashPreview(0, gridId, uniqueId, 0, [])
            return
        material, curLevel = self._clashMaterialLevel(costGridId, costUniqueId, uniqueId, soulItem.itemId)
        if not material or not self._beginSoulClashDeduct(
                soulItem.uniqueId, curLevel, itemIds, bindTypes, 'bagSoulClashDeductCB',
                (gridId, uniqueId, costGridId, costUniqueId, curLevel)):
            self.client.onSoulClashPreview(0, gridId, uniqueId, 0, [])

    def bagSoulClashDeductCB(self, opStat, bindValue, unbindValue, opUUID, gridId, uniqueId, costGridId, costUniqueId, curLevel):
        LOG_INFO('in bagSoulClashDeductCB:', opStat, bindValue, unbindValue, opUUID, gridId, uniqueId, costGridId, curLevel)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK or not soulItem:
            self.client.onSoulClashPreview(0, gridId, uniqueId, 0, [])
            return
        material = self._getBagSoulItem(costGridId, costUniqueId)
        materialQuality = material.quality if material else 0
        payload = SoulInfo.setClashPreview(SoulInfo.readItem(soulItem), soulItem.itemId, self.getRoleCacheAttr('school'), curLevel, materialQuality)
        if not payload:
            LOG_ERR('bagSoulClashDeductCB, preview failed:', gridId, uniqueId)
            self.client.onSoulClashPreview(0, gridId, uniqueId, soulItem.bindType, [])
            return
        materialBound = self._consumeClashMaterial(opUUID, bindValue, costGridId, costUniqueId, uniqueId, soulItem.itemId, curLevel)
        if materialBound is None:
            self.client.onSoulClashPreview(0, gridId, uniqueId, soulItem.bindType, [])
            return
        payload['previewClash']['materialBound'] = materialBound
        SoulInfo.writeItem(soulItem, payload)
        self._syncBagSoulItem(gridId, soulItem)
        self.client.onSoulClashPreview(
            1, gridId, uniqueId, soulItem.bindType, SoulInfo.propsToClient(payload['previewClash']['rareProps']))
        self._trackSoul(
            'Soul_Wash_HighRank', opUUID, soulItem, None, SoulInfo.calcBindType(payload), payload,
            afterRare=payload['previewClash']['rareProps'], affixOpType='wash')

    @gamedecorator.checkGameconfigEnable('equip_soulWash')
    def reqSoulClashConfirm(self, exposed, gridId, uniqueId):
        LOG_INFO('in reqSoulClashConfirm:', gridId, uniqueId)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if not soulItem:
            self.client.onSoulClashConfirm(0, gridId, uniqueId, 0, [])
            return
        before = SoulInfo.readItem(soulItem)
        payload = SoulInfo.keepItemClash(soulItem)
        if not payload:
            self.client.onSoulClashConfirm(0, gridId, uniqueId, soulItem.bindType, [])
            return
        self._syncBagSoulItem(gridId, soulItem)
        self.client.onSoulClashConfirm(
            1, gridId, uniqueId, soulItem.bindType, SoulInfo.propsToClient(payload['rareProps']))
        self._trackSoul(
            'Soul_Wash_HighRank', KBEngine.genUUID64(), soulItem, None, SoulInfo.calcBindType(payload), before,
            afterRare=payload['rareProps'], affixOpType='confirm')

    @gamedecorator.checkGameconfigEnable('equip_soulWash')
    def reqSoulClashDiscard(self, exposed, gridId, uniqueId):
        LOG_INFO('in reqSoulClashDiscard:', gridId, uniqueId)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if not soulItem or not SoulInfo.discardItemClash(soulItem):
            LOG_WARN('   in reqSoulClashDiscard, preview not found:', gridId, uniqueId)
            self.client.onSoulClashDiscardResult(gridId, uniqueId, 0)
            return
        self._syncBagSoulItem(gridId, soulItem)
        self.client.onSoulClashDiscardResult(gridId, uniqueId, 1)

    @gamedecorator.checkGameconfigEnable('equip_soulWash')
    def reqSoulDefReplace(self, exposed, gridId, uniqueId, costGridId, costUniqueId, itemIds, bindTypes):
        LOG_INFO('in reqSoulDefReplace:', gridId, uniqueId, costGridId, costUniqueId, itemIds, bindTypes)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if not soulItem or gridId == costGridId:
            self.client.onSoulDefReplace(0, gridId, uniqueId, 0, 0)
            return
        payload = soulItem.exportSoulPayload()
        material, materialDefLevel = self._defReplaceMaterial(
            costGridId, costUniqueId, uniqueId, soulItem.itemId, payload['defLevel'])
        if not material or not self._beginSoulDefReplaceDeduct(
                soulItem.uniqueId, itemIds, bindTypes, 'bagSoulDefReplaceDeductCB',
                (gridId, uniqueId, costGridId, costUniqueId, materialDefLevel)):
            self.client.onSoulDefReplace(0, gridId, uniqueId, soulItem.bindType, payload['defLevel'])

    def bagSoulDefReplaceDeductCB(self, opStat, bindValue, unbindValue, opUUID, gridId, uniqueId, costGridId, costUniqueId, materialDefLevel):
        LOG_INFO('in bagSoulDefReplaceDeductCB:', opStat, bindValue, unbindValue, opUUID, gridId, uniqueId, costGridId, materialDefLevel)
        soulItem = self._getBagSoulItem(gridId, uniqueId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK or not soulItem:
            bindType = soulItem.bindType if soulItem else 0
            defLevel = soulItem.exportSoulPayload()['defLevel'] if soulItem else 0
            self.client.onSoulDefReplace(0, gridId, uniqueId, bindType, defLevel)
            return
        payload = soulItem.exportSoulPayload()
        consumed = self._consumeDefReplaceMaterial(
            opUUID, bindValue, costGridId, costUniqueId, uniqueId, soulItem.itemId,
            payload['defLevel'], materialDefLevel)
        if not consumed:
            self.client.onSoulDefReplace(0, gridId, uniqueId, soulItem.bindType, payload['defLevel'])
            return
        materialBound, newDefLevel = consumed
        newPayload = SoulInfo.replaceItemDefLevel(soulItem, newDefLevel, materialBound)
        if not newPayload:
            LOG_ERR('bagSoulDefReplaceDeductCB, replace failed:', gridId, uniqueId, newDefLevel)
            self.client.onSoulDefReplace(0, gridId, uniqueId, soulItem.bindType, payload['defLevel'])
            return
        self._syncBagSoulItem(gridId, soulItem)
        self.client.onSoulDefReplace(1, gridId, uniqueId, soulItem.bindType, newPayload['defLevel'])
        self._trackSoul(
            'Soul_Level_Change', opUUID, soulItem, None, SoulInfo.calcBindType(newPayload), payload,
            afterLevel=newPayload['defLevel'])

    def bagEquipSoulClash(self, equipPos, uniqueId, costGridId, costUniqueId, itemIds, bindTypes):
        LOG_INFO('in bagEquipSoulClash:', equipPos, uniqueId, costGridId, costUniqueId, itemIds, bindTypes)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        if not equipItem:
            self.client.onEquipSoulClashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0, [], 0)
            return
        material, curLevel = self._clashMaterialLevel(costGridId, costUniqueId, uniqueId, equipItem.equipAttr.soulItemId)
        if not material or not self._beginSoulClashDeduct(
                equipItem.uniqueId, curLevel, itemIds, bindTypes, 'bagEquipSoulClashDeductCB',
                (equipPos, uniqueId, costGridId, costUniqueId, curLevel)):
            self.client.onEquipSoulClashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0, [], 0)

    def bagEquipSoulClashDeductCB(self, opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId, costGridId, costUniqueId, curLevel):
        LOG_INFO('in bagEquipSoulClashDeductCB:', opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId, costGridId, curLevel)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK or not equipItem:
            self.client.onEquipSoulClashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0, [], 0)
            return
        material = self._getBagSoulItem(costGridId, costUniqueId)
        materialQuality = material.quality if material else 0
        payload = SoulInfo.setClashPreview(
            SoulInfo.readEquip(equipItem.equipAttr), equipItem.equipAttr.soulItemId,
            self.getRoleCacheAttr('school'), curLevel, materialQuality)
        if not payload:
            LOG_ERR('bagEquipSoulClashDeductCB, preview failed:', equipPos, uniqueId)
            self.client.onEquipSoulClashPreview(
                0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, equipItem.equipAttr.soulBindType, [], 0)
            return
        materialBound = self._consumeClashMaterial(
            opUUID, bindValue, costGridId, costUniqueId, uniqueId, equipItem.equipAttr.soulItemId, curLevel)
        if materialBound is None:
            self.client.onEquipSoulClashPreview(
                0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, equipItem.equipAttr.soulBindType, [], 0)
            return
        payload['previewClash']['materialBound'] = materialBound
        SoulInfo.writeEquip(equipItem.equipAttr, payload)
        equipItem.equipAttr.setDirtyFlag()
        self._syncBagSoulItem(equipPos, equipItem)
        self._sendEquipSoulClashPreview(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, equipItem)
        self._trackSoul(
            'Soul_Wash_HighRank', opUUID, None, equipItem, SoulInfo.calcBindType(payload), payload,
            afterRare=payload['previewClash']['rareProps'], affixOpType='wash')

    def bagEquipSoulClashConfirm(self, equipPos, uniqueId):
        LOG_INFO('in bagEquipSoulClashConfirm:', equipPos, uniqueId)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        before = SoulInfo.readEquip(equipItem.equipAttr) if equipItem else None
        payload = self._keepEquipSoulClash(equipItem) if equipItem else None
        if not equipItem or not payload:
            bindType = equipItem.equipAttr.soulBindType if equipItem else 0
            bindFromClash = equipItem.equipAttr.soulBindFromClash if equipItem else 0
            self.client.onEquipSoulClashConfirm(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, bindType, [], bindFromClash)
            return
        self._syncBagSoulItem(equipPos, equipItem)
        self._sendEquipSoulClashConfirm(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, equipItem)
        self._trackSoul(
            'Soul_Wash_HighRank', KBEngine.genUUID64(), None, equipItem, SoulInfo.calcBindType(payload), before,
            afterRare=payload['rareProps'], affixOpType='confirm')

    def bagEquipSoulClashDiscard(self, equipPos, uniqueId):
        LOG_INFO('in bagEquipSoulClashDiscard:', equipPos, uniqueId)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        if not equipItem or not self._discardEquipSoulClash(equipItem):
            LOG_WARN('   in bagEquipSoulClashDiscard, preview not found:', equipPos, uniqueId)
            self.client.onEquipSoulClashDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0)
            return
        self._syncBagSoulItem(equipPos, equipItem)
        self.client.onEquipSoulClashDiscardResult(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 1)

    def bodyEquipSoulClash(self, equipPos, uniqueId, soulItemId, costGridId, costUniqueId, itemIds, bindTypes, defLevel):
        LOG_INFO('in bodyEquipSoulClash:', equipPos, uniqueId, soulItemId, costGridId, costUniqueId, itemIds, bindTypes, defLevel)
        material, curLevel = self._clashMaterialLevel(costGridId, costUniqueId, uniqueId, soulItemId)
        if not material or not self._beginSoulClashDeduct(
                uniqueId, curLevel, itemIds, bindTypes, 'bodyEquipSoulClashDeductCB',
                (equipPos, uniqueId, soulItemId, costGridId, costUniqueId, curLevel, defLevel)):
            self.client.onEquipSoulClashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId, 0, [], 0)

    def bodyEquipSoulClashDeductCB(self, opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId, soulItemId, costGridId, costUniqueId, curLevel, defLevel):
        LOG_INFO('in bodyEquipSoulClashDeductCB:', opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId, costGridId, curLevel, defLevel)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            self.client.onEquipSoulClashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId, 0, [], 0)
            return
        payload = SoulInfo.emptyPayload()
        payload['defLevel'] = defLevel
        material = self._getBagSoulItem(costGridId, costUniqueId)
        materialQuality = material.quality if material else 0
        payload = SoulInfo.setClashPreview(payload, soulItemId, self.getRoleCacheAttr('school'), curLevel, materialQuality)
        if not payload:
            LOG_ERR('bodyEquipSoulClashDeductCB, preview failed:', equipPos, uniqueId, curLevel)
            self.client.onEquipSoulClashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId, 0, [], 0)
            return
        materialBound = self._consumeClashMaterial(opUUID, bindValue, costGridId, costUniqueId, uniqueId, soulItemId, curLevel)
        if materialBound is None:
            self.client.onEquipSoulClashPreview(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId, 0, [], 0)
            return
        self.cell.cellEquipSoulClashPreview(materialBound, equipPos, uniqueId, payload['previewClash']['rareProps'])

    def _beginSoulClashDeduct(self, uniqueId, curLevel, itemIds, bindTypes, methodName, args, box=None):
        if not curLevel:
            LOG_ERR('_beginSoulClashDeduct, curLevel is 0:', uniqueId)
            return False
        if not self.getRoleCacheAttr('school'):
            LOG_ERR('_beginSoulClashDeduct, school missing:', uniqueId)
            return False
        cost = utils.soulClashCost(curLevel)
        if not cost:
            LOG_ERR('_beginSoulClashDeduct, cost missing:', curLevel)
            return False
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_SOUL_HEDGE_COST
        costCurrency = {cost['ironItemId']: cost['ironNum']}
        detail = gameclass.AwardDetailCls(uniqueId=uniqueId, costCurrencyDic=costCurrency)
        self.baseEquipDeductItemsWithBindTypes(
            costCurrency, {}, itemIds, bindTypes, opUUID, srcType, detail, box or self,
            methodName, (opUUID,) + tuple(args))
        return True

    def _clashMaterialLevel(self, costGridId, costUniqueId, targetUniqueId, targetItemId):
        material = self._getBagSoulItem(costGridId, costUniqueId)
        if not material or material.uniqueId == targetUniqueId:
            LOG_ERR('_clashMaterialLevel, invalid material:', costGridId, costUniqueId)
            return None, 0
        if material.isLocked():
            LOG_ERR('_clashMaterialLevel, material is locked:', costGridId, material.itemId)
            return None, 0
        targetData = dataUtils.getCommItemData(targetItemId)
        curLevel = utils.soulCurrentLevel(material.itemId, material.exportSoulPayload()['baseProps'])
        targetQuality = targetData['quality'] if targetData else 0
        if not utils.soulClashMaterialAllowed(material.quality, targetQuality, curLevel):
            LOG_ERR('_clashMaterialLevel, inlayLevelRestrict:', material.itemId, targetItemId, material.quality, targetQuality, curLevel)
            return None, 0
        if curLevel <= 0:
            LOG_ERR('_clashMaterialLevel, level is 0:', material.itemId, costGridId)
            return None, 0
        return material, curLevel

    def _consumeClashMaterial(self, opUUID, bindValue, costGridId, costUniqueId, targetUniqueId, targetItemId, curLevel):
        material, levelNow = self._clashMaterialLevel(costGridId, costUniqueId, targetUniqueId, targetItemId)
        if not material or levelNow != curLevel:
            LOG_ERR('_consumeClashMaterial, material changed:', costGridId, curLevel, levelNow)
            return None
        rareBound = SoulInfo.rareBoundFromClashMaterial(material.exportSoulPayload())
        srcType = AAC_AACDD.datas.BONUS_SRC_SOUL_HEDGE_COST
        detail = gameclass.AwardDetailCls(bagType=self.bagData.bagType, gridId=costGridId, itemId=material.itemId)
        cleaned = self.bagData.cleanGridByGridId(self, costGridId, material.itemId, opUUID, srcType, detail)
        if not cleaned:
            LOG_ERR('_consumeClashMaterial, clean failed:', costGridId)
            return None
        return rareBound

    def _keepEquipSoulClash(self, equipItem):
        payload = SoulInfo.keepEquipClash(equipItem.equipAttr)
        if not payload:
            return None
        equipItem.refreshSoulBindFromPayload()
        equipItem.equipAttr.calcScore()
        equipItem.equipAttr.setDirtyFlag()
        return payload

    def _discardEquipSoulClash(self, equipItem):
        payload = SoulInfo.discardEquipClash(equipItem.equipAttr)
        if not payload:
            return None
        equipItem.equipAttr.setDirtyFlag()
        return payload

    def _sendEquipSoulClashPreview(self, equipIn, equipPos, equipItem):
        preview = equipItem.equipAttr.soulPayload()['previewClash']
        rareProps = preview['rareProps'] if preview else []
        materialBound = preview.get('materialBound', 0) if preview else 0
        self.client.onEquipSoulClashPreview(
            1, equipIn, equipPos, equipItem.uniqueId, equipItem.equipAttr.soulBindType,
            SoulInfo.propsToClient(rareProps), materialBound)

    def _sendEquipSoulClashConfirm(self, equipIn, equipPos, equipItem):
        payload = equipItem.equipAttr.soulPayload()
        self.client.onEquipSoulClashConfirm(
            1, equipIn, equipPos, equipItem.uniqueId, equipItem.equipAttr.soulBindType,
            SoulInfo.propsToClient(payload['rareProps']), payload['bindFromClash'])

    def bagEquipSoulDefReplace(self, equipPos, uniqueId, costGridId, costUniqueId, itemIds, bindTypes):
        LOG_INFO('in bagEquipSoulDefReplace:', equipPos, uniqueId, costGridId, costUniqueId, itemIds, bindTypes)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        if not equipItem:
            self.client.onEquipSoulDefReplace(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, 0, 0, 0)
            return
        payload = equipItem.equipAttr.soulPayload()
        material, materialDefLevel = self._defReplaceMaterial(
            costGridId, costUniqueId, uniqueId, equipItem.equipAttr.soulItemId, payload['defLevel'])
        if not material or not self._beginSoulDefReplaceDeduct(
                equipItem.uniqueId, itemIds, bindTypes, 'bagEquipSoulDefReplaceDeductCB',
                (equipPos, uniqueId, costGridId, costUniqueId, materialDefLevel)):
            self.client.onEquipSoulDefReplace(
                0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId,
                equipItem.equipAttr.soulBindType, payload['defLevel'], equipItem.equipAttr.soulBindFromInherit)

    def bagEquipSoulDefReplaceDeductCB(self, opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId, costGridId, costUniqueId, materialDefLevel):
        LOG_INFO('in bagEquipSoulDefReplaceDeductCB:', opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId, costGridId, materialDefLevel)
        equipItem = self._getBagEquipWithSoul(equipPos, uniqueId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK or not equipItem:
            bindType = equipItem.equipAttr.soulBindType if equipItem else 0
            defLevel = equipItem.equipAttr.soulDefLevel if equipItem else 0
            bindFromInherit = equipItem.equipAttr.soulBindFromInherit if equipItem else 0
            self.client.onEquipSoulDefReplace(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId, bindType, defLevel, bindFromInherit)
            return
        payload = equipItem.equipAttr.soulPayload()
        consumed = self._consumeDefReplaceMaterial(
            opUUID, bindValue, costGridId, costUniqueId, uniqueId, equipItem.equipAttr.soulItemId,
            payload['defLevel'], materialDefLevel)
        if not consumed:
            self.client.onEquipSoulDefReplace(
                0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId,
                equipItem.equipAttr.soulBindType, payload['defLevel'], equipItem.equipAttr.soulBindFromInherit)
            return
        materialBound, newDefLevel = consumed
        newPayload = SoulInfo.replaceEquipDefLevel(equipItem.equipAttr, newDefLevel, materialBound)
        if not newPayload:
            LOG_ERR('bagEquipSoulDefReplaceDeductCB, replace failed:', equipPos, uniqueId, newDefLevel)
            self.client.onEquipSoulDefReplace(
                0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId,
                equipItem.equipAttr.soulBindType, payload['defLevel'], equipItem.equipAttr.soulBindFromInherit)
            return
        equipItem.refreshSoulBindFromPayload()
        equipItem.equipAttr.setDirtyFlag()
        self._syncBagSoulItem(equipPos, equipItem)
        self.client.onEquipSoulDefReplace(
            1, gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, equipPos, uniqueId,
            equipItem.equipAttr.soulBindType, newPayload['defLevel'], newPayload['bindFromInherit'])
        self._trackSoul(
            'Soul_Level_Change', opUUID, None, equipItem, SoulInfo.calcBindType(newPayload), payload,
            afterLevel=newPayload['defLevel'])

    def bodyEquipSoulDefReplace(self, equipPos, uniqueId, soulItemId, costGridId, costUniqueId, itemIds, bindTypes, defLevel):
        LOG_INFO('in bodyEquipSoulDefReplace:', equipPos, uniqueId, soulItemId, costGridId, costUniqueId, itemIds, bindTypes, defLevel)
        material, materialDefLevel = self._defReplaceMaterial(
            costGridId, costUniqueId, uniqueId, soulItemId, defLevel)
        if not material or not self._beginSoulDefReplaceDeduct(
                uniqueId, itemIds, bindTypes, 'bodyEquipSoulDefReplaceDeductCB',
                (equipPos, uniqueId, soulItemId, costGridId, costUniqueId, defLevel, materialDefLevel)):
            self.client.onEquipSoulDefReplace(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId, 0, 0, 0)

    def bodyEquipSoulDefReplaceDeductCB(self, opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId, soulItemId, costGridId, costUniqueId, defLevel, materialDefLevel):
        LOG_INFO('in bodyEquipSoulDefReplaceDeductCB:', opStat, bindValue, unbindValue, opUUID, equipPos, uniqueId, costGridId, defLevel, materialDefLevel)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            self.client.onEquipSoulDefReplace(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId, 0, 0, 0)
            return
        consumed = self._consumeDefReplaceMaterial(
            opUUID, bindValue, costGridId, costUniqueId, uniqueId, soulItemId, defLevel, materialDefLevel)
        if not consumed:
            self.client.onEquipSoulDefReplace(0, gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId, 0, 0, 0)
            return
        materialBound, newDefLevel = consumed
        self.cell.cellEquipSoulDefReplace(materialBound, equipPos, uniqueId, newDefLevel)

    def _beginSoulDefReplaceDeduct(self, uniqueId, itemIds, bindTypes, methodName, args, box=None):
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_SOUL_REPLACE_COST
        costCurrency = {SSRCD.datas['replaceType']['value']: SSRCD.datas['replaceConsume']['value']}
        detail = gameclass.AwardDetailCls(uniqueId=uniqueId, costCurrencyDic=costCurrency)
        self.baseEquipDeductItemsWithBindTypes(
            costCurrency, {}, itemIds, bindTypes, opUUID, srcType, detail, box or self,
            methodName, (opUUID,) + tuple(args))
        return True

    def _defReplaceMaterial(self, costGridId, costUniqueId, targetUniqueId, targetItemId, targetDefLevel):
        material = self._getBagSoulItem(costGridId, costUniqueId)
        if not material or material.uniqueId == targetUniqueId:
            LOG_ERR('_defReplaceMaterial, invalid material:', costGridId, costUniqueId)
            return None, 0
        if material.isLocked():
            LOG_ERR('_defReplaceMaterial, material is locked:', costGridId, material.itemId)
            return None, 0
        targetData = dataUtils.getCommItemData(targetItemId)
        materialDefLevel = material.exportSoulPayload()['defLevel']
        if not targetData or targetData['quality'] != material.quality or materialDefLevel < targetDefLevel:
            LOG_ERR('_defReplaceMaterial, not allowed:', material.itemId, targetItemId,
                    material.quality, materialDefLevel, targetDefLevel)
            return None, 0
        return material, materialDefLevel

    def _consumeDefReplaceMaterial(self, opUUID, bindValue, costGridId, costUniqueId, targetUniqueId, targetItemId, targetDefLevel, materialDefLevel):
        material, levelNow = self._defReplaceMaterial(
            costGridId, costUniqueId, targetUniqueId, targetItemId, targetDefLevel)
        if not material or levelNow != materialDefLevel:
            LOG_ERR('_consumeDefReplaceMaterial, material changed:', costGridId, materialDefLevel, levelNow)
            return None
        bindFromInherit = material.exportSoulPayload().get('bindFromInherit')
        srcType = AAC_AACDD.datas.BONUS_SRC_SOUL_REPLACE_COST
        detail = gameclass.AwardDetailCls(bagType=self.bagData.bagType, gridId=costGridId, itemId=material.itemId)
        cleaned = self.bagData.cleanGridByGridId(self, costGridId, material.itemId, opUUID, srcType, detail)
        if not cleaned:
            LOG_ERR('_consumeDefReplaceMaterial, clean failed:', costGridId)
            return None
        materialBound = 1 if bindValue or bindFromInherit else 0
        return materialBound, levelNow

    def bodyEquipSoulSocket(self, equipQuality, equipType, soulGridId, costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, cbArgs):
        LOG_INFO('in bodyEquipSoulSocket:', equipQuality, equipType, soulGridId)
        soulItem = self.bagData.getItemObjByGridId(soulGridId)
        if not soulItem:
            LOG_ERR('bodyEquipSoulSocket, soulGridId is invalid:', soulGridId)
            self.cell.unlockBodyEquips()
            return

        if soulItem.itemSubType not in gameconst.ItemSubEnum.EQUIP_SOUL_TYPE:
            LOG_ERR('bodyEquipSoulSocket, soulGridId is not soul item:', soulGridId)
            self.cell.unlockBodyEquips()
            return

        soulData = SS_D.datas.get(soulItem.itemId, None)
        if not soulData:
            LOG_ERR('bodyEquipSoulSocket, soulItem is not soul item:', soulItem.itemId)
            self.cell.unlockBodyEquips()
            return

        if soulData['equipmentID'] != equipType:
            LOG_ERR('bodyEquipSoulSocket, equipType is not match:', soulItem.itemId, equipType)
            self.cell.unlockBodyEquips()
            return

        if utils.soulInlayForbidden(soulItem.quality, equipQuality):
            LOG_ERR('bodyEquipSoulSocket, inlayRange forbid:', soulItem.itemId, soulItem.quality, equipQuality)
            self.cell.unlockBodyEquips()
            return

        self.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                'bodyEquipSoulSocketDeductItemsCB', cbArgs)

    def bodyEquipSoulSocketDeductItemsCB(self, opStat, bindValue, unbindValue, opUUID, equipSlot, soulGridId):
        LOG_INFO('in bodyEquipSoulSocketDeductItemsCB:', opStat, bindValue, unbindValue, opUUID, equipSlot, soulGridId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipSoulSocketDeductItemsCB, deduct items error')
            return

        rollProps, soulItemId, soulBindType = self._doDeductSoulItem(opUUID, soulGridId)
        if not rollProps:
            return

        self.cell.cellEquipSoulSocket(opStat, bindValue, unbindValue, opUUID, equipSlot, rollProps, soulItemId, soulBindType)

    def bagEquipSoulSocketDeductItemsCB(self, opStat, bindValue, unbindValue, opUUID, gridId, soulGridId):
        LOG_INFO('in bagEquipSoulSocketDeductItemsCB:', opStat, bindValue, unbindValue, opUUID, gridId, soulGridId)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipSoulSocketDeductItemsCB, deduct items error')
            return

        rollProps, soulItemId, soulBindType = self._doDeductSoulItem(opUUID, soulGridId)
        if not rollProps:
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        # 记录魂魄绑定状态
        beforeSoulAffixes = bagEquipItem.getSoulAffixesLogStr()
        bagEquipItem.setSoulBindType(soulBindType)

        ret = bagEquipItem.doEquipSoulSocket(self, rollProps, soulItemId)
        if ret:
            soulAffixes = []
            for oneAffix in bagEquipItem.equipAttr.soulAffixes:
                soulAffixes.append(oneAffix.toAfxClientDic())
            payload = bagEquipItem.equipAttr.soulPayload()
            lucky = [payload['luckyProp']] if payload['luckyProp'] else []
            self.client.onEquipSoulSocketSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, soulAffixes,
                                                 bagEquipItem.getEquipScore(), bagEquipItem.equipAttr.soulBindType, bagEquipItem.bindType, soulItemId,
                                                 payload['defLevel'],
                                                 SoulInfo.propsToClient(payload['rareProps']), SoulInfo.propsToClient(lucky),
                                                 payload['bindFromWash'], payload['bindFromClash'], payload['bindFromInherit'])

        equipAttrs = {
            'baseAttrs':bagEquipItem.getBaseAttrs(),
            'upgradeAttrs':bagEquipItem.getUpgradeAttrs(),
            'enhanceAttrs':bagEquipItem.getEnhanceAttrs(),
        }
        LogTrackingMgr.LogTrackingMgr.equip_soul(self.gbID, self.accountEntity.clientDistinctId, opUUID, bagEquipItem.uniqueId, \
                                                    bagEquipItem.itemId, bagEquipItem.getItemName(), bagEquipItem.getEquipType(), bagEquipItem.getGrade(), \
                                                        bagEquipItem.getQuality(), bagEquipItem.getEquipScore(), equipAttrs, beforeSoulAffixes, soulAffixes, bagEquipItem.soulSocketNeedItems())

    def bagEquipWash(self, gridId, uniqueId, washType, count):
        LOG_INFO('in bagEquipWash:', gridId, uniqueId, washType, count)
        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem or bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('in bagEquipWash, gridId is invalid:', gridId)
            self.client.onEquipWashReply(gameconst.EquipWashResult.EQUIP_NOT_FOUND, '', gridId, uniqueId, washType, 0)
            return

        resultCode, actualCount, costItemDic = bagEquipItem.checkEquipWashCost(washType, count)
        if resultCode != gameconst.EquipWashResult.OK:
            LOG_INFO("in bagEquipWash, result code:", resultCode)
            self.client.onEquipWashReply(resultCode, '', gridId, uniqueId, washType, 0)
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_WASH
        detail = gameclass.AwardDetailCls(uniqueId=bagEquipItem.uniqueId, costItemDic=costItemDic)
        self.baseEquipWashDeductItems(
            costItemDic, 
            opUUID, 
            srcType, 
            detail, 
            self,
            'bagEquipWashDeductItemsCB', 
            [opUUID, gridId, uniqueId, washType, actualCount]
        )
        return

    def bagEquipWashDeductItemsCB(self, opStat, opUUID, gridId, uniqueId, washType, actualCount):
        LOG_INFO('in bagEquipWashDeductItemsCB:', opStat, gridId, uniqueId, washType, actualCount)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('   in bagEquipWashDeductItemsCB, deduct items error', opStat)
            code = gameconst.EquipWashResult.ITEM_NOT_ENOUGH
            if opStat == gameconst.BagOPStat.OPERATE_BAG_FAIL:
                code = gameconst.EquipWashResult.FAIL
            self.client.onEquipWashReply(code, '', gridId, uniqueId, washType, 0)
            return

        bagEquipItem = self.bagData.getItemObjByGridId(gridId)
        if not bagEquipItem or bagEquipItem.uniqueId != uniqueId:
            LOG_ERR('in bagEquipWashDeductItemsCB, equip not found:', gridId, uniqueId)
            self.client.onEquipWashReply(gameconst.EquipWashResult.EQUIP_NOT_FOUND, '', gridId, uniqueId, washType, 0)
            return

        if washType == gameconst.EquipWashType.ENHANCE:
            bindBefore = bagEquipItem.equipAttr.bindEnhanceCost
        elif washType == gameconst.EquipWashType.BLESS:
            bindBefore = bagEquipItem.equipAttr.bindBlessCost
        else:
            bindBefore = bagEquipItem.getBindValue()

        # 执行洗涤
        bagEquipItem.doEquipWash(washType, actualCount)

        if washType == gameconst.EquipWashType.ENHANCE:
            bindAfter = bagEquipItem.equipAttr.bindEnhanceCost
        elif washType == gameconst.EquipWashType.BLESS:
            bindAfter = bagEquipItem.equipAttr.bindBlessCost
        else:
            bindAfter = bagEquipItem.getBindValue()

        equipAttrs = {
            'baseAttrs': bagEquipItem.getBaseAttrs(),
            'upgradeAttrs': bagEquipItem.getUpgradeAttrs(),
            'enhanceAttrs': bagEquipItem.getEnhanceAttrs(),
        }
        LogTrackingMgr.LogTrackingMgr.equip_wash(
            self.gbID,
            self.accountEntity.clientDistinctId,
            opUUID,
            bagEquipItem.uniqueId,
            bagEquipItem.itemId,
            bagEquipItem.getItemName(),
            bagEquipItem.equipAttr.equipType,
            bagEquipItem.getGrade(),
            bagEquipItem.getQuality(),
            bagEquipItem.getEquipScore(),
            equipAttrs,
            washType,
            bindBefore,
            bindAfter
        )

        self.client.onEquipWashReply(gameconst.EquipWashResult.OK, '', gridId, uniqueId, washType, actualCount)
        return

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.limitcall(1)
    @gamedecorator.crossServer
    def reqMultiEquipDisassemble(self, exposed, gridIdList, uniqueIdList):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_reqMultiEquipDisassemble', (gridIdList, uniqueIdList))
        else:
            self._reqMultiEquipDisassemble(gridIdList, uniqueIdList)

    def _reqMultiEquipDisassemble(self, gridIdList, uniqueIdList):
        LOG_INFO('reqMultiEquipDisassemble:', gridIdList, uniqueIdList)
        tmpGridIdList = [gridId for gridId in gridIdList]
        tmpGridIdList = set(tmpGridIdList)
        if len(tmpGridIdList) == 0 or len(tmpGridIdList) != len(gridIdList):
            gameengine.panicStack("reqMultiEquipDisassemble, lack of materials, grid id repeated ", gridIdList)
            return
        
        tmpUniqueIdList = [uniqueId for uniqueId in uniqueIdList]
        tmpUniqueIdList = set(tmpUniqueIdList)
        if len(tmpUniqueIdList) == 0 or len(tmpUniqueIdList) != len(uniqueIdList):
            gameengine.panicStack("reqMultiEquipDisassemble, lack of materials, unique id repeated ", uniqueIdList)
            return
        
        if len(uniqueIdList) != len(gridIdList):
            gameengine.panicStack("reqMultiEquipDisassemble, lack of materials, unique id list is not equal to grid id list ", uniqueIdList, gridIdList)
            return
        
        self.bagData.doBagEquipDisassemble(self, gridIdList, uniqueIdList) or []

    def _doBagEquipDisassemble(self, srcType, _totalWealthVal, opUUID, detail, awardCtx, _succGridIdList, succUniqueIdList):
        self.bagData._doBagEquipDisassemble(self, srcType, _totalWealthVal, opUUID, detail, awardCtx, _succGridIdList, succUniqueIdList)

    def bagEquipSell(self, gridId, uniqueId):
        self.bagData.doBagEquipSell(self, gridId, uniqueId)

    def updateBodyEquipDressData(self, dressDataDic):
        self.baseBodyEquipDressDataDic = dressDataDic

    def canEquipAutoDisassemble(self, owner, equipItem):
        cliConfig = self.cliConfigDic.get(gameconst.CliConfigDef.EQUIP_AUTO_DISA_KEY, 0)
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
        _reqClassList = dataUtils.getEquipItemData(equipItem.itemId)['reqClass']
        myClass = owner.getRoleCacheAttr('school', 0)
        if 0 not in _reqClassList and myClass not in _reqClassList:
            #自己无法装备，不考虑评分，可以分解
            return True
        _slotIds = dataUtils.equipSlot(equipItem.equipAttr.equipType, equipItem.equipAttr.equipSubType)
        for _slotId in _slotIds:
            bodyEquipScore = self.baseBodyEquipDressDataDic.get(_slotId, {}).get('score', 0)
            if equipItem.getEquipScore() > bodyEquipScore:
                return False
        return True

    @gamedecorator.checkGameconfigEnable('equip_make')
    @gamedecorator.limitcall(1)
    def reqMakeEquipment(self, exposed, itemId, gridIdList, gridCountList, makeType):
        LOG_INFO('reqMakeEquipment:', itemId, gridIdList, gridCountList, makeType)
        tmpGridIdList = [gridId for gridId in gridIdList]
        tmpGridIdList = set(tmpGridIdList)
        if len(tmpGridIdList) == 0 or len(tmpGridIdList) != len(gridIdList):
            gameengine.panicStack("reqMakeEquipment, lack of materials ", gridIdList)
            return
        
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
            self.onMessagePre(M_M_DD.datas.bagFullGeneralMessage, [])
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

        res = self.canDeductWealth(deductVal, sendMsg=True)
        if not res:
            self.client.onEquipMakeFailed()
            LOG_WARN('in reqMakeEquipment, canDeductWealth fail:', itemId, res())
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_MANUFACTURE
        detail = gameclass.AwardDetailCls(itemId=itemId)
        # 扣指定格子指定数量的道具
        self.bagData.deductItemsByGridId(self, needGridIdList, opUUID, srcType, detail)
        # 扣货币
        self.deductWealth(srcType, deductVal, opUUID, detail)
        
        # 获得制造好的道具
        bindType = gameconst.ItemBindType.BIND if bindValue > 0 else gameconst.ItemBindType.NORMAL
        equipItem = itemFactory.ItemFactory.createItem(itemId, 1, bindType=bindType)
        # 设置绑定值
        equipItem.setBindValue(bindValue)
        LOG_INFO('reqMakeEquipment: done', itemId, gridIdList, makeType, bindValue)
        dropAward.WealthItem(itemObjs=[equipItem]).popDebtItemObjs(self, srcType, opUUID, detail, self.bagData.bagType)
        if equipItem.itemNum <= 0:
            opStat = gameconst.BagOPStat.OPERATE_BAG_STAT_OK
        else:
            opStat, _ = self.bagData.addItemsWithPlan(self, [equipItem, ], opUUID, srcType, detail, notify=False)
        if opStat == gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            equipAttrs = {
                'baseAttrs':equipItem.getBaseAttrs(),
                'upgradeAttrs':equipItem.getUpgradeAttrs(),
                'enhanceAttrs':equipItem.getEnhanceAttrs(),
            }
            LogTrackingMgr.LogTrackingMgr.equip_make(self.gbID, self.accountEntity.clientDistinctId, opUUID, self.gbID, equipItem.uniqueId, \
                                                    equipItem.itemId, equipItem.getItemName(), equipItem.getEquipType(), 1, equipItem.getGrade(), \
                                                    equipItem.getQuality(), equipItem.getBindValue(), makeType, equipItem.getBaseAttrs(), \
                                                    equipItem.getUpgradeAttrs(), equipItem.getEnhanceAttrs(), equipItem.getEquipScore(), equipAttrs)
            data = equipItem.toClientEquipItemDict()
            LOG_INFO('in reqMakeEquipment, addItemsWithPlan success:', opStat, data)
            self.client.onEquipMakeSucc(data)
        else:
            LOG_ERR('in reqMakeEquipment, addItemsWithPlan fail:', opStat, itemId)
            self.client.onEquipMakeFailed()

        self.achievementInfo.triggerAchieveByType(self, gameconst.AchieveType.MAKE_EQUIPMENT, actionContext.AchievementCtx(quality=equipItem.getQuality()))
        self.taskCheckCounterTarget(TCCTD.couterTargetDic['MakeEquipmentOnce'], (itemId,))
        
    ################################## gm cmd ###################################
    def gmAddGearbaseEquipItem(self, templateId, bindType=dataUtils.getItemDefaultBindType(), grade = 1):
        LOG_INFO('gmAddGearbaseEquipItem:', templateId)
        equipItem = itemFactory.ItemFactory.createItem(templateId, 1, bindType=bindType, grade = grade)
        opUUID = KBEngine.genUUID64()
        src = AAC_AACDD.datas.BONUS_SRC_GM
        detail = gameclass.AwardDetailCls(templateId=templateId)

        dropAward.WealthItem(itemObjs=[equipItem]).popDebtItemObjs(self, src, opUUID, detail, self.bagData.bagType)
        if equipItem.itemNum <= 0:
            return gameconst.BagOPStat.OPERATE_BAG_STAT_OK
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

            _gearData = dataUtils.getEquipItemData(it.itemId)
            reqClassList = _gearData.get('reqClass', [])
            if 0 not in reqClassList and myClass not in reqClassList:
                continue

            equipLevel = _gearData['equipLevel'][it.getGrade()-1]
            if equipLevel > myLevel:
                continue

            slotIds = dataUtils.equipSlot(it.equipAttr.equipType, it.equipAttr.equipSubType)
            for _slotId in slotIds:
                if _slotId in bodyDressSlotIds:
                    bodyDressSlotIds.remove(_slotId)
                    self.addTimerCB(
                        0.2, 
                        'gmSendDressEquips', 
                        (gridId, _slotId, it), 
                        gametimer.TIMER_TAG_GM_SEND_DRESS_EQUIPS)
                    break

            if len(bodyDressSlotIds) == 0:
                break

    def gmSendDressEquips(self, gridId, slotId, equipItem):
        LOG_INFO("gmSendDressEquips ", gridId, slotId, equipItem)
        self.unlockBag()
        self.bagData.doDressEquip(self, gridId, 0, slotId)

    def gmGlyphWashingEquips(self, itemId, glyphPos, affixId1, affixId2):
        LOG_INFO("gmGlyphWashingEquips ", itemId, glyphPos, affixId1, affixId2)
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
                glyphBindType = gameconst.ItemBindType.BIND if glyphPos in bagEquipItem.equipAttr.glyphBindTypes else gameconst.ItemBindType.NORMAL
                self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos,
                                                    glyphData.toClientData(), bagEquipItem.getEquipScore(),
                                                    glyphBindType, bagEquipItem.bindType)
        return

    def gmSetEquipEnhance(self, su, itemId, equipId, enhanceLv, bindEnhanceCost=-1, syncMaxLv=0):
        """
        GM设置装备强化等级/强化绑定值, 按 背包->仓库->身上 顺序定位装备, 仅支持在线玩家
        """
        LOG_INFO('gmSetEquipEnhance', itemId, equipId, enhanceLv, bindEnhanceCost, syncMaxLv)
        if self.isCrossServer:
            LOG_ERR('gmSetEquipEnhance, player is in cross server:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER, '执行失败, 玩家在跨服中, 请回到本服后执行',
                               {"ec": gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER})
            return

        errMsgMap = {
            gameconst.GMCommandErr.GM_RET_EQUIP_GROWING_FORBIDDEN: '执行失败, 装备当前禁止养成操作(如在架拍卖/掉落中)',
            gameconst.GMCommandErr.GM_RET_EQUIP_LV_OUT_OF_RANGE: '执行失败, 强化等级超出配置范围',
        }

        #先找背包
        gridIds = self.bagData.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if bagEquipItem.uniqueId != equipId:
                continue
            ret, errCode = bagEquipItem.gmSetEnhance(self.gbID, self, enhanceLv, bindEnhanceCost, syncMaxLv)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "enhanceLv": enhanceLv})
                return
            if self.client:
                self.client.onUpdateGridItemsJson(self.bagData.bagType, gridId, equipId, bagEquipItem.attr2Json())
                #onUpdateGridItemsJson只带attrJson, 客户端不刷新bindType与GearInfo解析值, 补发强化回包同步
                equipEnhanceDatas = [{
                    'eqipIn': gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
                    'eqipPos': gridId,
                    'enhanceVal': bagEquipItem.getEnhanceLevel(),
                    'itemId': bagEquipItem.itemId,
                    'uniqueId': bagEquipItem.uniqueId,
                    'enhanceLv': bagEquipItem.getEnhanceLevel(),
                    'score': bagEquipItem.getEquipScore(),
                    'bindEnhanceCost': bagEquipItem.equipAttr.bindEnhanceCost,
                    'bindType': bagEquipItem.bindType,
                    'maxEnhanceLv': bagEquipItem.getMaxEnhanceLevel(),
                }]
                self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.OK, equipEnhanceDatas, [], False)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
                                             "pos": gridId, "enhanceLv": bagEquipItem.getEnhanceLevel(), "bindEnhanceCost": bagEquipItem.equipAttr.bindEnhanceCost})
            return

        #背包没有找仓库
        gridIds = self.warehouse.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            warehouseEquipItem = self.warehouse.getItemObjByGridId(gridId)
            if warehouseEquipItem.uniqueId != equipId:
                continue
            ret, errCode = warehouseEquipItem.gmSetEnhance(self.gbID, self, enhanceLv, bindEnhanceCost, syncMaxLv)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "enhanceLv": enhanceLv})
                return
            if self.client:
                self.sendWarehouseData()
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": "warehouse",
                                             "pos": gridId, "enhanceLv": warehouseEquipItem.getEnhanceLevel(), "bindEnhanceCost": warehouseEquipItem.equipAttr.bindEnhanceCost})
            return

        #仓库没有找身上
        if not self.cell:
            LOG_ERR('gmSetEquipEnhance, cell not exist:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND})
            return
        self.cell.cellGmSetEquipEnhance(su, itemId, equipId, enhanceLv, bindEnhanceCost, syncMaxLv)

    def gmSetEquipGrade(self, su, itemId, equipId, grade, bindValue=-1):
        """
        GM设置装备升阶等级/升阶绑定值, 按 背包->仓库->身上 顺序定位装备, 仅支持在线玩家
        """
        LOG_INFO('gmSetEquipGrade', itemId, equipId, grade, bindValue)
        if self.isCrossServer:
            LOG_ERR('gmSetEquipGrade, player is in cross server:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER, '执行失败, 玩家在跨服中, 请回到本服后执行',
                               {"ec": gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER})
            return

        errMsgMap = {
            gameconst.GMCommandErr.GM_RET_EQUIP_GROWING_FORBIDDEN: '执行失败, 装备当前禁止养成操作(如在架拍卖/掉落中)',
            gameconst.GMCommandErr.GM_RET_EQUIP_LV_OUT_OF_RANGE: '执行失败, 升阶等级超出配置范围',
        }

        #先找背包
        gridIds = self.bagData.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if bagEquipItem.uniqueId != equipId:
                continue
            ret, errCode = bagEquipItem.gmSetGrade(self.gbID, self, grade, bindValue)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "grade": grade})
                return
            if self.client:
                self.client.onUpdateGridItemsJson(self.bagData.bagType, gridId, equipId, bagEquipItem.attr2Json())
                #onUpdateGridItemsJson只带attrJson, 客户端不刷新bindType与GearInfo解析值, 补发升阶回包同步
                self.client.onEquipUpgradeSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, bagEquipItem.getGrade(),
                                               bagEquipItem.getEquipScore(), bagEquipItem.getOriginalBindValue(),
                                               bagEquipItem.equipAttr.bindValue, bagEquipItem.bindType)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
                                             "pos": gridId, "grade": bagEquipItem.getGrade(), "bindValue": bagEquipItem.equipAttr.bindValue})
            return

        #背包没有找仓库
        gridIds = self.warehouse.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            warehouseEquipItem = self.warehouse.getItemObjByGridId(gridId)
            if warehouseEquipItem.uniqueId != equipId:
                continue
            ret, errCode = warehouseEquipItem.gmSetGrade(self.gbID, self, grade, bindValue)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "grade": grade})
                return
            if self.client:
                self.sendWarehouseData()
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": "warehouse",
                                             "pos": gridId, "grade": warehouseEquipItem.getGrade(), "bindValue": warehouseEquipItem.equipAttr.bindValue})
            return

        #仓库没有找身上
        if not self.cell:
            LOG_ERR('gmSetEquipGrade, cell not exist:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND})
            return
        self.cell.cellGmSetEquipGrade(su, itemId, equipId, grade, bindValue)

    def gmSetEquipSpirit(self, su, itemId, equipId, spiritPos, affixIds, bindType=-1):
        """
        GM设置装备附灵词缀/附灵绑定状态, 按 背包->仓库->身上 顺序定位装备, 仅支持在线玩家
        """
        LOG_INFO('gmSetEquipSpirit', itemId, equipId, spiritPos, affixIds, bindType)
        if self.isCrossServer:
            LOG_ERR('gmSetEquipSpirit, player is in cross server:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER, '执行失败, 玩家在跨服中, 请回到本服后执行',
                               {"ec": gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER})
            return

        errMsgMap = {
            gameconst.GMCommandErr.GM_RET_EQUIP_GROWING_FORBIDDEN: '执行失败, 装备当前禁止养成操作(如在架拍卖/掉落中)',
            gameconst.GMCommandErr.GM_RET_ARGS_ERR: '执行失败, 参数错误(词缀格式/词缀ID不合法/附灵槽位未开启)',
        }

        #先找背包
        gridIds = self.bagData.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if bagEquipItem.uniqueId != equipId:
                continue
            ret, errCode = bagEquipItem.gmSetSpirit(self.gbID, self, spiritPos, affixIds, bindType)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "spiritPos": spiritPos})
                return
            if self.client:
                self.client.onUpdateGridItemsJson(self.bagData.bagType, gridId, equipId, bagEquipItem.attr2Json())
                #onUpdateGridItemsJson只带attrJson, 客户端不刷新bindType与GearInfo解析值, 补发附灵回包同步
                spiritBindType = gameconst.ItemBindType.BIND if bagEquipItem.isSpiritBindType(spiritPos) else gameconst.ItemBindType.NORMAL
                spiritData = bagEquipItem.equipAttr.spiritDatas[spiritPos]
                self.client.onEquipSpiritWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, spiritData.toClientData(),
                                                     spiritPos, bagEquipItem.getEquipScore(), spiritBindType, bagEquipItem.bindType)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
                                             "pos": gridId, "spiritPos": spiritPos, "affixIds": affixIds})
            return

        #背包没有找仓库
        gridIds = self.warehouse.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            warehouseEquipItem = self.warehouse.getItemObjByGridId(gridId)
            if warehouseEquipItem.uniqueId != equipId:
                continue
            ret, errCode = warehouseEquipItem.gmSetSpirit(self.gbID, self, spiritPos, affixIds, bindType)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "spiritPos": spiritPos})
                return
            if self.client:
                self.sendWarehouseData()
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": "warehouse",
                                             "pos": gridId, "spiritPos": spiritPos, "affixIds": affixIds})
            return

        #仓库没有找身上
        if not self.cell:
            LOG_ERR('gmSetEquipSpirit, cell not exist:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND})
            return
        self.cell.cellGmSetEquipSpirit(su, itemId, equipId, spiritPos, affixIds, bindType)

    def gmSetEquipGlyph(self, su, itemId, equipId, glyphPos, affixIds, bindType=-1):
        """
        GM设置装备铭文词缀/铭文绑定状态, 按 背包->仓库->身上 顺序定位装备, 仅支持在线玩家
        """
        LOG_INFO('gmSetEquipGlyph', itemId, equipId, glyphPos, affixIds, bindType)
        if self.isCrossServer:
            LOG_ERR('gmSetEquipGlyph, player is in cross server:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER, '执行失败, 玩家在跨服中, 请回到本服后执行',
                               {"ec": gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER})
            return

        errMsgMap = {
            gameconst.GMCommandErr.GM_RET_EQUIP_GROWING_FORBIDDEN: '执行失败, 装备当前禁止养成操作(如在架拍卖/掉落中)',
            gameconst.GMCommandErr.GM_RET_ARGS_ERR: '执行失败, 参数错误(词缀格式/词缀ID不合法/铭文槽位未开启)',
        }

        #先找背包
        gridIds = self.bagData.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if bagEquipItem.uniqueId != equipId:
                continue
            ret, errCode = bagEquipItem.gmSetGlyph(self.gbID, self, glyphPos, affixIds, bindType)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "glyphPos": glyphPos})
                return
            if self.client:
                self.client.onUpdateGridItemsJson(self.bagData.bagType, gridId, equipId, bagEquipItem.attr2Json())
                #onUpdateGridItemsJson只带attrJson, 客户端不刷新bindType与GearInfo解析值, 补发铭文回包同步
                glyphBindType = gameconst.ItemBindType.BIND if glyphPos in bagEquipItem.equipAttr.glyphBindTypes else gameconst.ItemBindType.NORMAL
                glyphData = bagEquipItem.equipAttr.getGlyphData(glyphPos)
                self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, glyphPos,
                                                    glyphData.toClientData(), bagEquipItem.getEquipScore(),
                                                    glyphBindType, bagEquipItem.bindType)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
                                             "pos": gridId, "glyphPos": glyphPos, "affixIds": affixIds})
            return

        #背包没有找仓库
        gridIds = self.warehouse.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            warehouseEquipItem = self.warehouse.getItemObjByGridId(gridId)
            if warehouseEquipItem.uniqueId != equipId:
                continue
            ret, errCode = warehouseEquipItem.gmSetGlyph(self.gbID, self, glyphPos, affixIds, bindType)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "glyphPos": glyphPos})
                return
            if self.client:
                self.sendWarehouseData()
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": "warehouse",
                                             "pos": gridId, "glyphPos": glyphPos, "affixIds": affixIds})
            return

        #仓库没有找身上
        if not self.cell:
            LOG_ERR('gmSetEquipGlyph, cell not exist:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND})
            return
        self.cell.cellGmSetEquipGlyph(su, itemId, equipId, glyphPos, affixIds, bindType)

    def gmSetEquipBless(self, su, itemId, equipId, luckyVal, maxBlessLv=-1, blessLvRate=-1, bindBlessCost=-1):
        """
        GM设置装备祝福幸运值/历史最高/保底回溯进度/祝福绑定值, 按 背包->仓库->身上 顺序定位装备, 仅支持在线玩家
        """
        LOG_INFO('gmSetEquipBless', itemId, equipId, luckyVal, maxBlessLv, blessLvRate, bindBlessCost)
        if self.isCrossServer:
            LOG_ERR('gmSetEquipBless, player is in cross server:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER, '执行失败, 玩家在跨服中, 请回到本服后执行',
                               {"ec": gameconst.GMCommandErr.GM_RET_TARGET_IN_CROSS_SERVER})
            return

        errMsgMap = {
            gameconst.GMCommandErr.GM_RET_EQUIP_GROWING_FORBIDDEN: '执行失败, 装备当前禁止养成操作(如在架拍卖/掉落中)',
            gameconst.GMCommandErr.GM_RET_ARGS_ERR: '执行失败, 该装备不支持祝福',
            gameconst.GMCommandErr.GM_RET_EQUIP_LV_OUT_OF_RANGE: '执行失败, 祝福幸运值超出配置范围',
        }

        #先找背包
        gridIds = self.bagData.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            bagEquipItem = self.bagData.getItemObjByGridId(gridId)
            if bagEquipItem.uniqueId != equipId:
                continue
            ret, errCode = bagEquipItem.gmSetBless(self.gbID, self, luckyVal, maxBlessLv, blessLvRate, bindBlessCost)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "luckyVal": luckyVal})
                return
            if self.client:
                self.client.onUpdateGridItemsJson(self.bagData.bagType, gridId, equipId, bagEquipItem.attr2Json())
                #onUpdateGridItemsJson只带attrJson, 客户端不刷新bindType与GearInfo解析值, 补发祝福回包同步
                blessAffixes = []
                for oneAffix in bagEquipItem.equipAttr.blessAffixes:
                    blessAffixes.append(oneAffix.toAfxClientDic())
                self.client.onEquipBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, blessAffixes,
                                             bagEquipItem.equipAttr.maxBlessLv, bagEquipItem.equipAttr.blessLvRate,
                                             bagEquipItem.getEquipScore(), bagEquipItem.equipAttr.bindBlessCost,
                                             bagEquipItem.bindType, bagEquipItem.getBlessFailLevels(), bagEquipItem.getBlessFailCounts())
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG,
                                             "pos": gridId, "luckyVal": luckyVal, "maxBlessLv": bagEquipItem.equipAttr.maxBlessLv, "blessLvRate": bagEquipItem.equipAttr.blessLvRate})
            return

        #背包没有找仓库
        gridIds = self.warehouse.getGridIdsByItemId(itemId)
        for gridId in gridIds:
            warehouseEquipItem = self.warehouse.getItemObjByGridId(gridId)
            if warehouseEquipItem.uniqueId != equipId:
                continue
            ret, errCode = warehouseEquipItem.gmSetBless(self.gbID, self, luckyVal, maxBlessLv, blessLvRate, bindBlessCost)
            if not ret:
                su.onCommandResult(errCode, errMsgMap.get(errCode, '执行失败'), {"ec": errCode, "luckyVal": luckyVal})
                return
            if self.client:
                self.sendWarehouseData()
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '执行成功', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": self.gbID, "equipIn": "warehouse",
                                             "pos": gridId, "luckyVal": luckyVal, "maxBlessLv": warehouseEquipItem.equipAttr.maxBlessLv, "blessLvRate": warehouseEquipItem.equipAttr.blessLvRate})
            return

        #仓库没有找身上
        if not self.cell:
            LOG_ERR('gmSetEquipBless, cell not exist:', itemId, equipId)
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_EQUIP_NOT_FOUND})
            return
        self.cell.cellGmSetEquipBless(su, itemId, equipId, luckyVal, maxBlessLv, blessLvRate, bindBlessCost)
################################## gm cmd end ###################################

    ################################### drop equip start ##############################
    def checkDropEquip(self, equipInfo, baseDropInfo, isCross):
        # 掉落列表满了
        if self.equipDropInfo.dropNum() >= GBGCD.datas['equipRepairListMaxNum']['value']:
            opUUID=KBEngine.genUUID64()
            # 如果是自己掉的，直接破碎
            if baseDropInfo['isFirst']:
                srcType = gameconst.BodyEquipDressOpType.UNDRESS_DROP_DISAPPEAR
                detail = gameclass.AwardDetailCls(uniqueid=equipInfo['uniqueId'], itemid=equipInfo['itemId'], isCross=self.isCrossServerInLocalServer)
                LogTrackingMgr.LogTrackingMgr.body_equip_flow(
                    self.gbID,
                    self.clientDistinctId,
                    opUUID,
                    gameconfig.serverId(),
                    self.accountName,
                    gameconfig.gameId(),
                    equipInfo['itemId'],
                    0,
                    srcType,
                    equipInfo['uniqueId'],
                    detail
                )
                           
            # 发邮件告知，装备由于掉落列表满了，已消失
            _mailId = GBGCD.datas['equipDisappearMailID']['value']
            _args = [
                str(GBGBD.datas[equipInfo['itemId']]["name"]),
            ]
            mailAssistor.sendMailToPlayers(
                [self.gbID],
                _mailId,
                opUUID=opUUID,
                despArgs=_args,
                srcType=AAC_AACDD.datas.BONUS_SRC_EQUIPMENT_DROP_REMOVE
            )
        else:
            self.cell.doDropEquipByItem(baseDropInfo, equipInfo, isCross)

    def onDropEquipBase(self, ownerId, returnTime, ownerServerId, uniqueId, price, maxPrice, mapId, pos, equipInfo, collEndTime, killerName, endTime, extraBlob, collectionId, dropTime, isFirst, collectionServerId):
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
            maxPrice,
            self.serverId,
            collectionId,
            isFirst,
            collectionServerId
        )
        
        self.equipDropInfo.addNewDrop(
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
            dropTime,
            False,
            returnTime,
            0,
            0
        )

        if self.isCrossServerInLocalServer:
            self.syncMethodCallToCrossServerBase('_syncOnDropEquipBase', (ownerId, returnTime, ownerServerId, uniqueId, price, mapId, pos, equipInfo, collEndTime, killerName, endTime, extraBlob, collectionId, dropTime, isFirst))

    def _syncOnDropEquipBase(self, ownerId, returnTime, ownerServerId, uniqueId, price, mapId, pos, equipInfo, collEndTime, killerName, endTime, extraBlob, collectionId, dropTime, isFirst):
        self.equipDropInfo.addNewDrop(
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
            dropTime,
            False,
            returnTime,
            0,
            0
        )

    def addNotifyDropFixTimer(self, uniqueId, endTime):
        self.equipDropInfo.addNotifyDropFixTimer(uniqueId, endTime)

    # 检测捡装备
    def checkPickDropEquip(self, uniqueId):
        if self.pickDropEquipLockTime > utils.curTS():
            return False

        return self.equipDropInfo.checkCouldTakeDrop(uniqueId)

    # 自己捡起来或者赎回会走到这里
    def onGetBackDropEquip(self, uniqueId, equipInfo, dropType, result, returnTime):
        LOG_INFO('onGetBackDropEquip:', uniqueId, equipInfo, dropType, result, returnTime)
        # 释放背包锁
        self.bagData.unLockBag()
        if result != DropResult_SUCCESS:
            return
        # 主动移除一边身上的，防止关服或者服务挂了，微服务发过来的移除消息没到达游戏服，从而导致同个unique id的装备重复
        self.onNotifyRemoveEquip([uniqueId])

        equipInfo = cPickle.loads(equipInfo)
        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)
        
        # 对方返还或者自己捡起来或者自己赎回，需要倒计时
        if dropType == gameconst.DropType.TYPE_TAKE_WAIT_DROP_GET \
            or dropType == gameconst.DropType.TYPE_GIVEUP_WAIT_DROP_GET \
            or dropType == gameconst.DropType.TYPE_REDEEM_WAIT_DROP_GET:
            self.equipDropInfo.removeDrop(self, uniqueId)
            _fixEndTime = utils.curTS() + GBGCD.datas['equipRepairTime']['value']
            equipItem.setDropFixEndTime(_fixEndTime)
            self.addNotifyDropFixTimer(equipItem.uniqueId, _fixEndTime)
            # 自己的首次掉落
            if returnTime == 0:
                equipItem.resetOwnerInfo()
        # 赎回到期或者自动返还，不需要倒计时
        elif dropType == gameconst.DropType.TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET:
            self.equipDropInfo.removeTaker(self, uniqueId)
        elif dropType == gameconst.DropType.TYPE_RETURN_GET:
            self.equipDropInfo.removeDrop(self, uniqueId)
            equipItem.resetOwnerInfo()

        _awardVal = dropAward.AwardVal()
        _awardVal.addWealthByObjList([equipItem])
        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_TAKE_BACK_DROP_EQUIP
        _detail = gameclass.AwardDetailCls()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID),
        )

        returnType = gameconst.EquipReturnType.ReturnTypeIndex.get(dropType, 0)
        self.logEquipReturn(uniqueId, equipItem.itemId, equipItem.getQuality(), equipItem.getGrade(), 0, returnType)
        # 通知客户端领取结果
        self.client.onGetBackEquipSuccess(uniqueId, dropType)

        if self.isCrossServerInLocalServer:
            self.syncMethodCallToCrossServerBase('_syncOnGetBackDropEquip', (dropType, uniqueId, equipItem.uniqueId, _src, _awardVal, _opUUID, _detail))

    #cross
    def _syncOnGetBackDropEquip(self, dropType, uniqueId, equipItemUniqueId, _src, _awardVal, _opUUID, _detail):
        # 对方返还或者自己捡起来或者自己赎回，需要倒计时
        if dropType == gameconst.DropType.TYPE_TAKE_WAIT_DROP_GET \
            or dropType == gameconst.DropType.TYPE_GIVEUP_WAIT_DROP_GET \
            or dropType == gameconst.DropType.TYPE_REDEEM_WAIT_DROP_GET:
            self.equipDropInfo.removeDrop(self, uniqueId)
            _fixEndTime = utils.curTS() + GBGCD.datas['equipRepairTime']['value']
            self.addNotifyDropFixTimer(equipItemUniqueId, _fixEndTime)
        # 赎回到期或者自动返还，不需要倒计时
        elif dropType == gameconst.DropType.TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET:
            self.equipDropInfo.removeTaker(self, uniqueId)
        elif dropType == gameconst.DropType.TYPE_RETURN_GET:
            self.equipDropInfo.removeDrop(self, uniqueId)

        
        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID),
        )
        
        self.client.onGetBackEquipSuccess(uniqueId, dropType)

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

    def onTakeDropEquipFailed(self, uniqueId, result):
        LOG_INFO('onTakeDropEquipFailed:', uniqueId, result)
        self.pickDropEquipLockTime = 0
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('onTakeDropEquipFailed', (uniqueId, result))

    # 捡别人的装备成功的回调
    def onTakeDropEquipSuccess(self, dropGbId, uniqueId, equipInfo, endTime, maxPrice, price, redeemWaitTime, returnTime):
        _posInfo = self.popTempMiscProp(gameconst.EntityPropsEnum.takeDropInfo, None)
        if _posInfo is None:
            LOG_ERR('onGetBackDropEquip not found temp misc prop:', uniqueId)
            return
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_onTakeDropEquipSuccess', (dropGbId, uniqueId, equipInfo, endTime, maxPrice, price, redeemWaitTime, returnTime, _posInfo))
        self._onTakeDropEquipSuccess(dropGbId, uniqueId, equipInfo, endTime, maxPrice, price, redeemWaitTime, returnTime, _posInfo)

    def _onTakeDropEquipSuccess(self, dropGbId, uniqueId, equipInfo, endTime, maxPrice, price, redeemWaitTime, returnTime, _posInfo):
        LOG_INFO('onTakeDropEquipSuccess:', dropGbId, uniqueId, equipInfo, endTime, maxPrice, price, redeemWaitTime, returnTime, _posInfo)
        self.pickDropEquipLockTime = 0

        equipInfo = cPickle.loads(equipInfo)
        equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipInfo)

        _spaceNo, _pos = _posInfo
        LogTrackingMgr.LogTrackingMgr.pickup_equip(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            self.getRoleCacheAttr('name', ''),
            self.accountName,
            equipItem.uniqueId,
            equipItem.itemId,
            equipItem.getQuality(),
            equipItem.getGrade(),
            formula.fetchMapId(_spaceNo),
            str(_pos),
        )

        # 新手历程 taskType=21: 拾取指定品质装备计数 (任意掉落来源)
        self.beginnerJourney_onTaskEvent(
                gameconst.BjTaskType.BJ_TASK_TYPE_DEATH_DROP_PICKUP,
                delta=1, quality=equipItem.getQuality())
        
        if dropGbId == self.gbID:
            if not gameconfig.isCrossServer():
                self.onDropTypeChangeToAvatar([uniqueId], [gameconst.DropNotifyType.NOTIFY_TYPE_TAKE_WAIT_DROP_GET], [[]])
            self.onMessagePre(
                GBGCD.datas['equipRepairing_msgId']['value'],
                [str(equipInfo.get('itemId', '')), str(GBGCD.datas['equipRepairTime']['value'])]
            )
            return
        
        self.equipDropInfo.addTaker(
            self,
            uniqueId,
            equipInfo,
            endTime,
            gameconst.DropType.TYPE_TAKE,
            price,
            True,
            redeemWaitTime,
            False,
            returnTime,
            0,
            0,
            maxPrice
        )

        self.onMessagePre(
            GBGCD.datas['pickOthersDropEquip_msgID']['value'],
            [str(equipItem.itemId)])

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def giveUpDropEquip(self, exposed, uniqueId):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_giveUpDropEquip', (uniqueId,))
        else:
            self._giveUpDropEquip(uniqueId)

    def _giveUpDropEquip(self, uniqueId):
        LOG_INFO('giveUpDropEquip:', uniqueId)
        if not self.equipDropInfo.hasTakeDrop(uniqueId):
            LOG_ERR('giveUpDropEquip not found take:', uniqueId)
            return

        gameengine.getGlobalBase('DropStub').giveUpDropEquip(self.gbID, uniqueId, self)

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def redeemEquipDrop(self, exposed, uniqueId):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_redeemEquipDrop', (uniqueId,))
        else:
            self._redeemEquipDrop(uniqueId)

    #local
    def _redeemEquipDrop(self, uniqueId):
        LOG_INFO('redeemEquipDrop:', uniqueId)
        _dropVal = self.equipDropInfo.getDropVal(uniqueId)
        if not _dropVal:
            LOG_ERR('redeemEquipDrop not found drop:', uniqueId)
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(
            GBGCD.datas['equipRepairCostItemID']['value'],
            _dropVal.price,
        )

        res = self.canDeductWealth(_deductVal, sendMsg=True)
        if not res:
            LOG_WARN('       in doUnlockGrids, items not enough:', _deductVal, res())
            return

        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_EQUIP_DROP
        _detail = gameclass.AwardDetailCls()
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        gameengine.getGlobalBase('DropStub').doRedeemEquipDrop(self.gbID, uniqueId, self)

        # 扣费发生在本服，跨服镜像同步扣一次，客户端当前连在跨服
        self.syncMethodCallToCrossServerBase('_syncOnRedeemEquipDrop', (_src, _deductVal, _opUUID, _detail))

    #cross
    def _syncOnRedeemEquipDrop(self, _src, _deductVal, _opUUID, _detail):
        LOG_INFO('syncOnRedeemEquipDrop:', _src, _deductVal, _opUUID, _detail)
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

    def onRedeemResult(self, uniqueId, result):
        if self.isCrossServerInLocalServer:
            self.syncMethodCallToCrossServerBase('onRedeemResult', (uniqueId, result))

        LOG_INFO('onRedeemResult:', uniqueId, result)
        if result == DropResult_SUCCESS:
            self.equipDropInfo.onDropTypeChange(uniqueId, gameconst.DropNotifyType.NOTIFY_TYPE_REDEEM_WAIT_DROP_GET)
            self.client.onEquipDropStateChange(uniqueId, gameconst.DropNotifyType.NOTIFY_TYPE_REDEEM_WAIT_DROP_GET)
            #self.equipDropInfo.removeDrop(self, uniqueId)
            return
        elif result == DropResult_NOT_FOUND:
            LOG_WARN('onRedeemResult not found drop:', uniqueId)
            self.equipDropInfo.removeTaker(self, uniqueId)
        elif result == DropResult_EXPIRE:
            LOG_WARN('onRedeemResult expire:', uniqueId)
            self.equipDropInfo.removeTaker(self, uniqueId)
        elif result == DropResult_REDEEM_NOT_SET_PRICE:
            # 这里缺乏一个提示，推给客户端先
            self.client.onRedeemNotSetPrice(uniqueId)
            return
        else:
            LOG_ERR('onRedeemResult unknown:', uniqueId, result)

    def onGetDropTakeReward(self, uniqueId, bindMoney, money, result):
        LOG_INFO('onGetDropTakeReward:', uniqueId, bindMoney, money, result)
        if result != DropResult_SUCCESS:
            return
        takerVal = self.equipDropInfo.getTakerVal(uniqueId)
        # 当前是待领取奖励的情况，就删除
        if takerVal.state == gameconst.DropNotifyType.NOTIFY_TYPE_REWARD:
            self.equipDropInfo.removeTaker(self, uniqueId)

        
        if gameconfig.isCrossServer():
            return

        _awardVal = dropAward.AwardVal(bindMoney=bindMoney, money=money)

        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_REDEEM_FOR_PICKER
        _detail = gameclass.AwardDetailCls()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID),
        )
        self.client.onGetDropTakeRewardSuccess(uniqueId)

        if self.isCrossServerInLocalServer:
            self.syncMethodCallToCrossServerBase('_onGetDropTakeReward', (uniqueId, bindMoney, money, result, _src, _awardVal, _opUUID, _detail))
    
    def _onGetDropTakeReward(self, uniqueId, bindMoney, money, result, _src, _awardVal, _opUUID, _detail):
        LOG_INFO('onGetDropTakeReward:', uniqueId, bindMoney, money, result, _src, _awardVal, _opUUID, _detail)
        self.onGetDropTakeReward(uniqueId, bindMoney, money, result)
        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID),
        )
        self.client.onGetDropTakeRewardSuccess(uniqueId)

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def getTakerWaitReward(self, exposed, uniqueId):
        LOG_INFO('getTakerWaitReward:', uniqueId)
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_getTakerWaitReward', (uniqueId,))
        else:
            self._getTakerWaitReward(uniqueId)

    def _getTakerWaitReward(self, uniqueId):
        gameengine.getGlobalBase('DropStub').doGetTakeReward(self.gbID, uniqueId, self)

    #drop中心服直接返回给跨服时，也应该去本服调用，再同步给跨服
    def onDropTypeChangeToAvatarInCross(self, uniqueIds, notifyTypes, notifyArgs):
        LOG_INFO('onDropTypeChangeToAvatarInCross:', uniqueIds, notifyTypes, notifyArgs)
        self.syncMethodCallToLocalServerBase('onDropTypeChangeToAvatar', (uniqueIds, notifyTypes, notifyArgs))

    def onDropTypeChangeToAvatar(self, uniqueIds, notifyTypes, notifyArgs):
        self.syncMethodCallToCrossServerBase('onDropTypeChangeToAvatar', (uniqueIds, notifyTypes, notifyArgs))
        LOG_INFO('onDropTypeChangeToAvatar:', uniqueIds, notifyTypes, notifyArgs)
        for idx in range(0, len(uniqueIds)):
            uniqueId = uniqueIds[idx]
            notifyType = notifyTypes[idx]
            if notifyType == gameconst.DropNotifyType.NOTIFY_REMOVE_ALL:
                self.equipDropInfo.removeDrop(self, uniqueId)
                self.equipDropInfo.removeTaker(self, uniqueId)
                return
            elif notifyType == gameconst.DropNotifyType.NOTIFY_REMOVE_DROP:
                self.equipDropInfo.removeDrop(self, uniqueId)
                return
            elif notifyType == gameconst.DropNotifyType.NOTIFY_REMOVE_TAKE:
                self.equipDropInfo.removeTaker(self, uniqueId)
                return
            elif notifyType == gameconst.DropNotifyType.NOTIFY_SET_PRICE:
                _dropVal = self.equipDropInfo.getDropVal(uniqueId)
                if _dropVal:
                    notifyArg = notifyArgs[idx]
                    _dropVal.price = notifyArg[0]
                    self.client.onSetTakeEquipRedeemPrice(uniqueId, _dropVal.price)
                return
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_TAKE:
                _dropVal = self.equipDropInfo.getDropVal(uniqueId)
                if _dropVal:
                    notifyArg = notifyArgs[idx]
                    _dropVal.state = gameconst.DropNotifyType.NOTIFY_TYPE_TAKE
                    _dropVal.takerGbId = notifyArg[0]
                    _dropVal.redeemWaitTime = notifyArg[1]
                    self.client.onSetEquipTakeInfo(uniqueId, _dropVal.takerGbId, _dropVal.redeemWaitTime)
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_GIVEUP_WAIT_DROP_GET:
                _dropVal = self.equipDropInfo.getDropVal(uniqueId)
                if _dropVal:
                    _mailId = GBGCD.datas['returnAndStartRepairMailID']['value']
                    _args = [
                        _dropVal.equipItem().itemId,
                        self.gbID
                    ]
                    mailAssistor.sendMailToPlayers(
                        [self.gbID],
                        _mailId,
                        opUUID=KBEngine.genUUID64(),
                        despArgs=_args,
                        srcType=AAC_AACDD.datas.BONUS_SRC_DROP_GIVE_UP_RETURN
                    )
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_RETURN_WAIT:
                _dropVal = self.equipDropInfo.getDropVal(uniqueId)
                if _dropVal:
                    notifyArg = notifyArgs[idx]
                    _dropVal.state = notifyType
                    _dropVal.redeemWaitTime = notifyArg[0]
                    self.client.onSetEquipReturnTime(uniqueId, _dropVal.returnTime)
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_DROP \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_TAKE_WAIT_DROP_GET \
                or notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_REDEEM_WAIT_DROP_GET:
                self.equipDropInfo.onDropTypeChange(uniqueId, notifyType)
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_RETURN_GET:
                # 最后的返还获取，移除捡起来面板的信息，更新掉落状态信息为返还获取
                self.equipDropInfo.onDropTypeChange(uniqueId, notifyType)
                self.equipDropInfo.removeTaker(self, uniqueId)
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET:
                _takeVal = self.equipDropInfo.takerDict.get(uniqueId, None)
                if _takeVal:
                    notifyArg = notifyArgs[idx]
                    _takeVal.state = notifyType
                    _takeVal.returnTime = notifyArg[0]
                    self.client.onSetEquipReturnTime(uniqueId, _takeVal.returnTime)
            elif notifyType == gameconst.DropNotifyType.NOTIFY_TYPE_REWARD:
                _takeVal = self.equipDropInfo.takerDict.get(uniqueId, None)
                if _takeVal:
                    notifyArg = notifyArgs[idx]
                    _takeVal.state = notifyType
                    _takeVal.bindMoney = notifyArg[0]
                    _takeVal.money = notifyArg[1]
                    self.client.onSetEquipPrice(uniqueId, _takeVal.bindMoney, _takeVal.money)

            self.client.onEquipDropStateChange(uniqueId, notifyType)

    def _initGetAllDropEquipStatus(self):
        gameengine.getGlobalBase('DropStub').doGetDropInfo(self.gbID, self)

    def onGetDropInfo(self, dropInfo, takerInfo, returnList, rewardList):
        LOG_INFO('onGetDropInfo:', dropInfo, takerInfo, returnList, rewardList)
        for _uniqueId, _equipInfo, _endTime, _dropType, _extraInfo, _collExpireTime, _price, _dropTime, hasPrice, returnTime, redeemTime, takerGbId in dropInfo:
            self.equipDropInfo.addNewDrop(
                self,
                _uniqueId,
                _price,
                _extraInfo.get('m', 0),
                _extraInfo.get('p', (0, 0, 0)),
                _equipInfo,
                _collExpireTime,
                _extraInfo.get('n', ''),
                _endTime,
                _dropType,
                False,
                _dropTime,
                hasPrice,
                returnTime,
                redeemTime,
                takerGbId
            )

        for _uniqueId, _equipInfo, _endTime, _dropType, _price, redeemWaitTime, hasPrice, returnTime, bindMoney, money, maxPrice in takerInfo:
            self.equipDropInfo.addTaker(
                self,
                _uniqueId,
                _equipInfo,
                _endTime,
                _dropType,
                _price,
                False,
                redeemWaitTime, 
                hasPrice,
                returnTime,
                bindMoney,
                money,
                maxPrice
            )

        self.equipDropInitStatus = 1
        self.triggerTempEvent(gameconst.EntityPropsEnum.equipDropInitEvent)

    def _sendDropEquipInfo(self):
        if not self.equipDropInitStatus:
            self.registerTempEvent(gameconst.EntityPropsEnum.equipDropInitEvent, '_sendDropEquipInfo', ())
            return

        # self.equipDropInfo.clearEndTimeVals()
        self.client.onInitEquipDropInfo(self.equipDropInfo)

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
        gameengine.getGlobalBase('DropStub').takeDropEquip(self.gbID, self.baseFromServerId, uniqueId, self, redeemWaitTime)
        self.pickDropEquipLockTime = curTs + 60
        self.setTempMiscProp(gameconst.EntityPropsEnum.takeDropInfo, (spaceNo, position))

    def onGiveUpDropEquip(self, uniqueId, result, dropGbId):
        LOG_INFO('onGiveUpDropEquip:', uniqueId, result, dropGbId)
        if result == DropResult_SUCCESS:
            _takerVal = self.equipDropInfo.removeTaker(self, uniqueId)
            if _takerVal:
                redisUtils.RedisUtils.getSingleUserInfo(dropGbId, functools.partial(self._onGiveUpGetUserInfo, _takerVal))
            self.syncMethodCallToCrossServerBase('_onGiveUpDropEquip', (uniqueId, result, dropGbId))

    def _onGiveUpDropEquip(self, uniqueId, result, dropGbId):
        LOG_INFO('onGiveUpDropEquip:', uniqueId, result, dropGbId)
        self.equipDropInfo.removeTaker(self, uniqueId)

    def _onGiveUpGetUserInfo(self, _takerVal, fcVal):
        _item = itemFactory.ItemFactory.createItemWithSavedDict(_takerVal.equip)
        _args = [
            str(_item.itemId),
            fcVal.name
        ]
        _msgId = GBGCD.datas['returnEnergyCrystalSuccess_msgID']['value']

        self.onMessagePre(_msgId, _args)
        self.syncMethodCallToCrossServerBase('_onLocalEnergyCrystalSuccess', (_msgId, _args))

    #cross
    def _onLocalEnergyCrystalSuccess(self, _msgId, _args):
        LOG_INFO('onLocalEnergyCrystalSuccess:', _msgId, _args)
        self.onMessagePre(_msgId, _args)

    def _dealDropEquipExpire(self):
        _endTime = utils.curTS()
        # 处理装备修复时间到提示msg
        while True:
            _takerTimerVal = self.equipDropInfo.firstTimerVal()
            if not _takerTimerVal:
                break

            if _takerTimerVal.endTime > _endTime:
                break

            self.equipDropInfo.popFirstTimerVal()
            _, equipItem = self.bagData.getItemByUniqueId(_takerTimerVal.uniqueId)
            if equipItem:
                self.onMessagePre(
                    GBGCD.datas['equipRepaired_msgID']['value'],
                    [str(equipItem.itemId)])

    # 自己掉落的装备过期处理
    def _dropExpire(self, uniqueId, itemId):
        self.equipDropInfo.removeDrop(self, uniqueId)
        # 发邮件告知，装备由于掉落列表满了，已消失
        _mailId = GBGCD.datas['equipDisappearMailID']['value']
        _args = [
            str(GBGBD.datas[itemId]["name"]),
        ]

        mailAssistor.sendMailToPlayers(
            [self.gbID],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args,
            srcType=AAC_AACDD.datas.BONUS_SRC_EQUIPMENT_DROP_EXPIRED_REMOVE
        )

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

    @gamedecorator.offlineCallback
    def onDropEquipExpire(self, uniqueId, itemId):
        LOG_INFO('onDropEquipExpire:', uniqueId, itemId)
        self._dropExpire(uniqueId, itemId)
        
    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def setTakeEquipRedeemPrice(self, exposed, uniqueId, price):
        LOG_INFO('setTakeEquipRedeemPrice:', uniqueId, price)
        if price <= 0:
            LOG_ERR('setTakeEquipRedeemPrice not valid price:', uniqueId, price)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        takerVal = self.equipDropInfo.getTakerVal(uniqueId)
        if not takerVal:
            LOG_ERR('setTakeEquipRedeemPrice not found take:', uniqueId)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        curTs = utils.curTS()
        if curTs > takerVal.redeemWaitTime:
            LOG_ERR('setTakeEquipRedeemPrice over redeemTime:', uniqueId)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        if price > takerVal.maxPrice:
            LOG_ERR('setTakeEquipRedeemPrice invalid price:', uniqueId, price, takerVal.price, takerVal.maxPrice)
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return
        gameengine.getGlobalBase('DropStub').setTakeEquipRedeemPrice(self.gbID, uniqueId, self, price)
    
    def onSetTakeEquipRedeemPriceBase(self, uniqueId, price, result):
        LOG_INFO('onSetTakeEquipRedeemPriceBase:', uniqueId, price, result)
        if result != DropResult_SUCCESS:
            self.client.onSetTakeEquipRedeemPrice(uniqueId, -1)
            return

        _dropVal = self.equipDropInfo.getTakerVal(uniqueId)
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
        _detail = gameclass.AwardDetailCls()

        self.addWealth(
            _src,
            _awardVal,
            _opUUID,
            _detail,
            awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID),
        )

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def getBackEquip(self, exposed, uniqueId, dropType):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_getBackEquip', (uniqueId, dropType))
        else:
            self._getBackEquip(uniqueId, dropType)

    def _getBackEquip(self, uniqueId, dropType):
        LOG_INFO('in getBackEquip:', uniqueId, dropType)
        # 检查是否还有剩余的格子
        if self.bagData.fetchEmptyGrid() is None:
            LOG_ERR("in getBackEquip, no empty grid is left")
            return
        # 给背包上锁
        if not self.bagData.tryLockBag(5, 'func::getBackEquip'):
            LOG_ERR("in getBackEquip, lock bag fail")
            return
        # 发起取回装备操作
        gameengine.getGlobalBase('DropStub').doGetBackEquip(self.gbID, self, uniqueId, dropType)

    @gamedecorator.checkGameconfigEnable('equip')
    @gamedecorator.crossServer
    def payDropPrice(self, exposed, uniqueId, price):
        self._payDropPrice(uniqueId, price)
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_payDropPrice', (uniqueId, price))

    def _payDropPrice(self, uniqueId, price):
        LOG_INFO('payDropPrice:', uniqueId, price)
        if price < 0:
            LOG_ERR('payDropPrice not valid price:', uniqueId, price)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        _dropVal = self.equipDropInfo.getDropVal(uniqueId)
        if not _dropVal:
            LOG_ERR('payDropPrice not found drop:', uniqueId)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        LOG_INFO('payDropPrice: current pay drop price info', _dropVal.price)
        curTs = utils.curTS()
        if curTs > _dropVal.redeemWaitTime:
            LOG_ERR('payDropPrice over redeem time:', uniqueId)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        if _dropVal.returnTime > 0 and curTs > _dropVal.returnTime:
            LOG_ERR('payDropPrice over return time:', uniqueId)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        if _dropVal.price <= 0 or price != _dropVal.price:
            LOG_ERR('payDropPrice invalid price:', uniqueId, price, _dropVal.price)
            self.client.onPayDropPrice(uniqueId, -1)
            return
        # 扣除元宝
        deductWealthVal = dropAward.DeductWealthVal()
        itemId = GBGCD.datas['equipRepairCost']['value']
        deductWealthVal.addWealthByItemId(itemId, _dropVal.price)
        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_WARN('payDropPrice, item is not enough', res())
            self.client.onPayDropPrice(uniqueId, -1)
            return

        #跨服只弹窗，扣钱后面本服同步
        if gameconfig.isCrossServer():
            return
        
        srcType = AAC_AACDD.datas.BONUS_SRC_DROP_PAY_PRICE
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls(uniqueId=uniqueId, itemId=itemId, itemCount=_dropVal.price)

        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        revenueRule = GBGCD.datas['equipRepairRatioForTaxTemp']['value']    
        revenueTax = math.ceil(revenueRule[0] * _dropVal.price)
        if revenueTax >= _dropVal.price:
            revenueTax = _dropVal.price
            revenueMoney = 0
            revenueBindMoney = 0
        else:
            revenueMoney = math.ceil(revenueRule[2] * _dropVal.price)
            if revenueMoney >= _dropVal.price - revenueTax:
                revenueMoney = _dropVal.price - revenueTax
                revenueBindMoney = 0
            else:
                revenueBindMoney = _dropVal.price - revenueTax - revenueMoney

        gameengine.getGlobalBase('DropStub').setDropEquipPayPrice(self.gbID, uniqueId, self, _dropVal.price, revenueBindMoney, revenueMoney)

        self.syncMethodCallToCrossServerBase('_onLocalPayDropPrice', (srcType, deductWealthVal, opUUID, detail))

    def _onLocalPayDropPrice(self, srcType, deductWealthVal, opUUID, detail):
        LOG_INFO('onLocalPayDropPrice:', srcType, deductWealthVal, opUUID, detail)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
    
    def onSetDropEquipPayPriceBase(self, uniqueId, price, result):
        LOG_INFO('onSetDropEquipPayPriceBase:', uniqueId, price, result)
        if result != DropResult_SUCCESS:
            itemId = GBGCD.datas['equipRepairCost']['value']
            src = AAC_AACDD.datas.BONUS_SRC_DROP_PAY_PRICE_RETURN
            detail = gameclass.AwardDetailCls(uniqueId=uniqueId, itemCount=price)
            award = dropAward.AwardVal()
            award.addWealthByItemId(itemId, price)
            opUUID = KBEngine.genUUID64()
            self.addWealth(src, award, opUUID, detail)

            if result == DropResult_SET_PAY_PRICE_NOT_SAME:
                self.onMessagePre(GBGCD.datas['equipReturnChange']['value'], [])
            self.client.onPayDropPrice(uniqueId, -1)
            
            return

        _dropVal = self.equipDropInfo.getDropVal(uniqueId)
        if not _dropVal:
            LOG_ERR('onSetDropEquipPayPriceBase not found take:', uniqueId)
            self.client.onPayDropPrice(uniqueId, -1)
            return

        self.client.onPayDropPrice(uniqueId, price)

    def onNotifyCustodyEquip(self, uniqueId, equipInfo, dropType, returnTime):
        LOG_INFO('onNotifyCustodyEquip:', uniqueId, equipInfo, dropType, returnTime)
        self.equipDropInfo.addNewDrop(
            self,
            uniqueId,
            0,
            0,
            (0,0,0),
            cPickle.loads(equipInfo),
            0,
            '',
            0,
            dropType,
            True,
            0,
            False,
            returnTime,
            0,
            0
        )

    @gamedecorator.offlineCallback
    def onNotifyRemoveEquip(self, uniqueIds):
        LOG_INFO('in onNotifyRemoveEquip:', uniqueIds)
        if not self.clientFinishInit:
            self.registerTempEvent(gameconst.EntityPropsEnum.clientInitEvent, 'onNotifyRemoveEquip', (uniqueIds,))
            return
        
        for uniqueId in uniqueIds:
            # 先查背包里数据
            gridId, gridObj = self.getGridItemByUniqueId(uniqueId)
            if gridObj:
                bagType = self.bagData.bagType
                detail = gameclass.AwardDetailCls(bagType=bagType, gridId=gridId, itemId=gridObj.itemId)
                uuid = KBEngine.genUUID64()
                srcType = AAC_AACDD.datas.BONUS_SRC_DROP_REMOVE_EQUIP
                self.bagData.cleanGridByGridId(self, gridId, gridObj.itemId, uuid, srcType, detail)
            else:
                # 从玩家身上移除
                self.cell.onRemoveEquipNotifyCell(uniqueId)
    ################################### drop equip end ##############################

    def checkEquipmentCore(self, itemID):
        itemData = ITEM_DATA.datas.get(itemID)
        return itemData and itemData['type'] == 0 and\
            itemData['subType'] in gameconst.ItemSubEnum.EQUIP_CORE_TUP


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
        """计算背包中指定绑定类型的材料消耗方案
        
        :param itemsDic: {itemId: needNum} 需要的材料清单
        :param bindType: 指定筛选的绑定类型 (BIND / NORMAL / BINDTYPE_NOT_SPECIFIED)
        :return: (results, bindInfos, consumedItemBindInfos)
            - results: {gridID: deductNum} 从哪些格子扣多少物品
            - bindInfos: [bindCount, normalCount] 绑定/未绑定物品的总消耗数
            - consumedItemBindInfos: {itemId: [bindCount, normalCount]} 按物品种类的绑定/未绑定消耗数
            材料不足时返回 (None, None, None)
        """
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
            if itemNum <= 0:
                continue
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
            validBagItems[bagItem.uniqueId] = [gridId, False, currencyDic, costItemDic, bagItem]

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

        res = self.canDeductWealth(deductWealthVal)
        if not res:
            self.cell.unlockBodyEquips()
            code = gameconst.EquipMultiEnhanceResult.ITEM_NOT_ENOUGH
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                code = gameconst.EquipMultiEnhanceResult.FAIL
            self.client.onMultiEquipEnhance(code, [], [], isMulti)
            LOG_WARN('baseMultiEquipEnhance, item is not enough', res())
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
            costCurrencyDic = itemData[2]
            costItemDic = itemData[3]
            # 计算消耗的格子
            gridNeedItems, bindInfos, consumedItemBindInfo = self.calculateConsumePlanGridsWithBindTyps(costItemDic, itemBindInfos)
            if not gridNeedItems:
                LOG_WARN('baseMultiEquipEnhance, not enough', costItem)
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
                
            detail = gameclass.AwardDetailCls(uniqueId=equipUniqueId, gridNeedItems=gridNeedItems, costItemDic=costItemDic, costCurrencyDic=costCurrencyDic)
            self.bagData.deductItemsByGridId(self, gridNeedItems, opUUID, srcType, detail)

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
            levelBefore = bagEquipItem.getEnhanceLevel()
            bindValueBefore = bagEquipItem.getBindValueByType(gameconst.EquipWashType.ENHANCE)

            bindValue = bindInfos[0]
            if bindValue > 0:
                # 记录强化消耗的绑定强化石数量（用于装备洗涤）
                bagEquipItem.addBindEnhanceCost(bindValue)
            
            enhanceVal = bagEquipItem.doEnhanceEquip(self, opUUID, bagEquipItem.getEnhanceLevel())
            bindValueAfter = bagEquipItem.getBindValueByType(gameconst.EquipWashType.ENHANCE)
            # 装备破碎了
            if enhanceVal == gameconst.EquipConstVale.ENHANCEMENT_BROKEN_FLAG:
                detail = gameclass.AwardDetailCls(uniqueid=uniqueId, itemid=bagEquipItem.itemId)
                self.bagData.cleanGridByGridId(self, gridId, bagEquipItem.itemId, opUUID, srcType, detail)
            equipAttrsBefore = {
                'baseAttrs':baseAttrsBefore,
                'upgradeAttrs':upgradeAttrsBefore,
                'enhanceAttrs':enhanceAttrsBefore,
            }
            equipAttrsAfter = {
                'baseAttrs':bagEquipItem.getBaseAttrs(),
                'upgradeAttrs':bagEquipItem.getUpgradeAttrs(),
                'enhanceAttrs':bagEquipItem.getEnhanceAttrs(),
            }
            LogTrackingMgr.LogTrackingMgr.equip_enhancement(self.gbID, self.accountEntity.clientDistinctId, opUUID, self.gbID, bagEquipItem.uniqueId, bagEquipItem.itemId, bagEquipItem.getItemName(), bagEquipItem.getEquipType(), \
                                                            bagEquipItem.getGrade(), bagEquipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, baseAttrsBefore, enhanceAttrsBefore, \
                                                            bagEquipItem.getBaseAttrs(), bagEquipItem.getEnhanceAttrs(), bindValue, levelBefore, bagEquipItem.getEnhanceLevel(), enhanceVal, bagEquipItem.getEquipScore(), \
                                                            bindValueBefore, bindValueAfter, equipAttrsBefore, equipAttrsAfter, isMulti)
            self.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            enhanceResults.append([gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG, gridId, enhanceVal, bagEquipItem.itemId, bagEquipItem.uniqueId, bagEquipItem.getEnhanceLevel(), bagEquipItem.getEquipScore(), bagEquipItem.equipAttr.bindEnhanceCost, bagEquipItem.bindType, bagEquipItem.getMaxEnhanceLevel()])        
        self.cell.cellMultiEquipEnhance(opUUID, bodyEquipInfos, bodyEquipBindInfos, enhanceResults, consumedItemInfos, isMulti)

    def logEquipReturn(self, uniqueId, itemId, quality, grade, money, returnType):
        LogTrackingMgr.LogTrackingMgr.equip_return(self.gbID, self.accountEntity.clientDistinctId, self.gbID, self.getRoleCacheAttr('name', ''), \
                                                   self.accountName, uniqueId, itemId, quality, grade, money, returnType)
