# -*- encoding:utf-8 -*-
from KBEDebug import *
import KBEngine

import random
import json
import gzip
import _pickle as cPickle

import utils
import formula
import gameconst
import mailAssistor
import actionContext
import gameconfig
import itemFactory
import dataUtils
import actionContext
import LogTrackingMgr
import gameclass
import gamedecorator
import gameengine
import message_Message_def as MMD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import conflict_conflict_def as C_C_DD
import gearBase_gearConst as GB_GCD
import formula_generalFormula as F_GFD
import gearBase_typeTab as GB_TTD
import qualityData_qualityData as QD_QDD
import gearEnhance_gearconst as GE_GC
import experience_exp as EXPD

class ImpEquipment(object):
    def __init__(self):
        super(ImpEquipment, self).__init__()

    @gamedecorator.checkGameconfigEnable('equip')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def reqSetEquipSuitHide(self, exposed, needHide):
        LOG_INFO('ImpEquipment::reqSetEquipSuitHide~', needHide)
        self.appearance.onEquipDisplayChanged(self, needHide)

    def sendBodyEquipData(self):
        self.sendStreamBodyEquipData()

    def sendStreamBodyEquipData(self):
        dic = self.bodyEquipData.toBodyEquipsClientDict()
        jsonStr = json.dumps(dic).encode('ascii')
        zStr = gzip.compress(jsonStr)
        self.base.streamStringProxy(zStr, '', gameconst.StreamStringID.BODY_EQUIP_DATA)
        return

    def syncBodyEquipDressData(self):
        self.base.updateBodyEquipDressData(self.bodyEquipData.getBodyEquipScoreDic())

    def applyBodyEquipsOnLogin(self):
        self.bodyEquipData.applyBodyEquipsProps(self, isLogin=True)

    def cellDressEquipment(self, opUUID, gridObjDic, dstSlotId):
        LOG_INFO('in cellDressEquipment:', gridObjDic, dstSlotId)
        if not self.bodyEquipData.tryLockBodyEquips(desp='cellDressEquipment'):
            LOG_WARN('   in cellDressEquipment, locked')
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_FAILED, {})
            return

        if not self.checkConflictState(C_C_DD.datas.changeGear, True):
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_FAILED, {})
            self.unlockBodyEquips()
            return

        _bagEquipItem = itemFactory.ItemFactory.createItemWithSavedDict(gridObjDic)

        slotId, bodyEquipItem = self.bodyEquipData.getDressSlotInfo(_bagEquipItem, dstSlotId)
        if slotId is None:
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_FAILED, {})
            self.unlockBodyEquips()
            return
        
        # 检查等级穿戴限制
        qualityData = QD_QDD.datas.get(_bagEquipItem.getQuality(), None)
        if not qualityData:
            LOG_WARN('   in cellDressEquipment, missing quality data cfg ', _bagEquipItem.getQuality())
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_FAILED, {})
            self.unlockBodyEquips()
            return
        
        equipLimits = qualityData['equipLimit']
        if not equipLimits:
            LOG_WARN('   in cellDressEquipment, missing quality limit data cfg ', _bagEquipItem.getQuality())
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_FAILED, {})
            self.unlockBodyEquips()
            return 

        lastIdx = -1
        for idx, equipLimit in enumerate(equipLimits):
            # 特殊的标识，标识不开放
            if equipLimit == 999:
                break
            if self.level < equipLimit:
                break
            lastIdx = idx + 1
        
        if lastIdx <= -1:
            LOG_WARN('   in cellDressEquipment, missing equip no cfg ', _bagEquipItem.getQuality())
            self.base.onMessagePre(GB_GCD.datas['equipWearLowRoleLevel']['value'], [])
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_FAILED, {})
            self.unlockBodyEquips()
            return
        
        # 检查下替换的情况
        excludeSlotId = -1
        if bodyEquipItem:
            excludeSlotId = slotId
            
        qualityData = self.bodyEquipData.getDressedQualityDatas(excludeSlotId)

        if qualityData.get(_bagEquipItem.getQuality(), 0) >= lastIdx:
            self.base.onMessagePre(GB_GCD.datas['equipWearLowRoleLevel']['value'], [])
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_FAILED, {})
            self.unlockBodyEquips()
            return

        if bodyEquipItem is None:
            # only dress
            self.bodyEquipData.dressEquip(self, slotId, _bagEquipItem)
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_ONLY_DRESS,
                                       _bagEquipItem.toItemSavedDict())
            self.unlockBodyEquips()
            self.client.onDressEquipment(_bagEquipItem.toClientBodyEquipItemDict(slotId))
            return

        self.unlockBodyEquips()
        self.replaceBodyEquip(slotId, opUUID, _bagEquipItem, bodyEquipItem)

    def replaceBodyEquip(self, slotId, opUUID, bagEquipItem, bodyEquipItem, swapEnhance=False):
        LOG_INFO('replaceBodyEquip:', slotId, opUUID, bagEquipItem.itemId, bodyEquipItem.itemId, swapEnhance)
        bodyEquipItem.removeEquipEffectToAvatar(self)
        self.bodyEquipData.dressEquip(self, slotId, bagEquipItem)
        self.client.onDressEquipment(bagEquipItem.toClientBodyEquipItemDict(slotId))
        self.base.replaceEquipment(opUUID, gameconst.DressEquipOpEnum.EQUIP_OP_REPLACED, bodyEquipItem.toItemSavedDict())

    def cellUndressEquipment(self, slotId):
        if self.isBodyEquipsLocked():
            LOG_WARN('     in cellUndressEquipment, locked')
            self.base.cellUndressEquipmentFail(slotId, 'cellUndressEquipment, body equip locked')
            return

        if not self.checkConflictState(C_C_DD.datas.changeGear, True):
            self.base.cellUndressEquipmentFail(slotId, 'cellUndressEquipment, state conflict')
            return

        _bodyEquip = self.bodyEquipData.doBodyUndressEquip(self, slotId)
        if not _bodyEquip:
            self.base.cellUndressEquipmentFail(slotId, 'cellUndressEquipment, data error')
            return

        self.base.cellUndressEquipmentSucc(_bodyEquip.toItemSavedDict())

    def cellLeaseExpireRemoveEquip(self, uniqueId):
        """租赁到期，强制从身上移除装备（不检查状态冲突，但检查装备锁）"""
        if self.isBodyEquipsLocked():
            LOG_WARN('in cellLeaseExpireRemoveEquip, body equips locked')
            self.base.cellLeaseExpireRemoveEquipCB(uniqueId, False)
            return

        slotId, equipItem = self.bodyEquipData.getEquipItemByUniqueId(uniqueId)
        if not equipItem:
            # 身上没有该装备，视为成功（不需要移除）
            self.base.cellLeaseExpireRemoveEquipCB(uniqueId, True)
            return

        bodyEquip = self.bodyEquipData.doBodyUndressEquip(self, slotId)
        if not bodyEquip:
            self.base.cellLeaseExpireRemoveEquipCB(uniqueId, False)
            return

        self.base.cellLeaseExpireRemoveEquipCB(uniqueId, True)

    def checkBodyEquipEnhanceConditions(self, equipPos, uniqueId):
        equipItem = self.bodyEquipData.getEquipItem(equipPos)
        if not equipItem:
            LOG_WARN('checkBodyEquipEnhanceConditions, equipPos error:', equipPos)
            return False, None, None, None, False
        if equipItem.uniqueId != uniqueId:
            LOG_WARN('checkBodyEquipEnhanceConditions, uniqueId not matched:', equipItem.uniqueId, uniqueId)
            return False, None, None, None, False
        if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
            LOG_ERR('checkBodyEquipEnhanceConditions, equipment can not be growing, equipment:', equipItem)
            return False, None, None, None, False

        ret = dataUtils.checkEquipmentEnhancementType(equipItem.equipAttr.equipType)
        if not ret:
            LOG_ERR('checkBodyEquipEnhanceConditions, equipment can not enhance, equipment:', equipItem)
            return  False, None, None, None, False

        if not equipItem.checkEnhancementValid(equipItem.equipAttr.getEnhanceLv() + 1):
            LOG_ERR('checkBodyEquipEnhanceConditions, equipment enhancement is invalid, equipment:', equipItem)
            return  False, None, None, None, True

        costItemDic, currencyDic = equipItem.enhanceNeedItems()
        if not costItemDic or not currencyDic:
            LOG_ERR('checkBodyEquipEnhanceConditions, cost is empty:', equipItem.equipAttr.getEnhanceLv() + 1)
            return  False, None, None, None, False
        return True, equipItem, currencyDic, costItemDic, False

    @gamedecorator.checkGameconfigEnable('equip_class')
    @utils.isMyself
    def reqEquipUpgrade(self, exposed, upgradeType, equipIn, equipPos, uniqueId, consumeGridIds, targetLv, autoBuy):
        LOG_INFO('in reqEquipUpgrade:', upgradeType, equipIn, equipPos, uniqueId, consumeGridIds, targetLv, autoBuy)
        tmpConsumeGridIds = [gridId for gridId in consumeGridIds]
        tmpConsumeGridIds = set(tmpConsumeGridIds)
        if len(tmpConsumeGridIds) == 0 or len(tmpConsumeGridIds) != len(consumeGridIds):
            gameengine.panicStack("reqEquipUpgrade, lack of materials, grid id repeated", consumeGridIds)
            return
        
        if upgradeType not in gameconst.EquipUpgradeType.VALID_UPGRADE_TYPE:
            LOG_WARN('     in reqEquipUpgrade, invalid upgradeType:', upgradeType)
            return
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipUpgrade(upgradeType, equipPos, uniqueId, consumeGridIds, targetLv, autoBuy)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                LOG_WARN('     in reqEquipUpgrade, equipPos error:', equipPos)
                return
            
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('   in reqEquipUpgrade, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return
            
            if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                LOG_ERR('   in reqEquipUpgrade, equipment can not be growing, equipment:', equipItem)
                return
            
            if len(consumeGridIds) == 0:
                LOG_ERR('   in reqEquipUpgrade, args error, consumed grid is empty')
                return
            
            ret = dataUtils.checkEquipmentUpgradeType(equipItem.equipAttr.equipType)
            if not ret:
                LOG_ERR('   in reqEquipUpgrade, equipment can not upgrade, equipment:', equipItem)
                return False
            
            if not dataUtils.checkEquipUpgradeValid(equipItem.equipAttr.equipType, equipItem.equipAttr.quality, equipItem.getGrade(), upgradeType, targetLv):
                LOG_ERR('   in reqEquipUpgrade, equipment upgrade is invalid, equipment:', equipItem)
                return

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipUpgrade'):
                LOG_WARN('   in reqEquipUpgrade, locked')
                return

            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_UPGRADE_BODY_EQUIP
            detail = gameclass.AwardDetailCls(itemId=equipItem.uniqueId)
            gridIds = {}
            for consumeGridId in consumeGridIds:
                gridIds[consumeGridId] = 1
            self.base.baseEquipDeductItems(None, gridIds, None, None, opUUID, src, detail, self,
                                  'cellEquipUpgrade', [consumeGridIds, equipItem.itemId, equipItem.getGrade(), upgradeType, targetLv, opUUID, equipPos], autoBuy, True)
        return

    def cellEquipUpgrade(self, opStat, bindValue, upgradeType, targetLv, opUUID, slotId):
        LOG_INFO('in cellEquipUpgrade:', opStat, bindValue, upgradeType, targetLv, opUUID, slotId)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_WARN('in cellEquipUpgrade, items not enouth')
            self.client.onEquipUpgradeFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId)
            return
        equipItem = self.bodyEquipData.getEquipItem(slotId)

        baseAttrsBefore = equipItem.getBaseAttrs()
        enhanceAttrsBefore = equipItem.getEnhanceAttrs()
        upgradeAttrsBefore = equipItem.getUpgradeAttrs()
        gradeBefore = equipItem.getGrade()
        bindValueBefore = equipItem.getBindValue()
        equipItem.doUpgradeEquip(self, opUUID, upgradeType, targetLv, onBody=True)
        if bindValue > 0:
            equipItem.addBindValue(bindValue)
        bindValueAfter = equipItem.getBindValue()
        self.updateEquipmentScore()
        self.bodyEquipData.updateEquipDressAppearance(self, equipItem.uniqueId)


        equipAttrsBefore = {
                'baseAttrs':baseAttrsBefore,
                'upgradeAttrs':upgradeAttrsBefore,
                'enhanceAttrs':enhanceAttrsBefore,
            }
        
        equipAttrsAfter = {
            'baseAttrs':equipItem.getBaseAttrs(),
            'upgradeAttrs':equipItem.getUpgradeAttrs(),
            'enhanceAttrs':equipItem.getEnhanceAttrs(),
        }

        LogTrackingMgr.LogTrackingMgr.equip_upgrade(self.gbId, self.clientDistinctIdCell, opUUID, self.gbId, equipItem.uniqueId, equipItem.itemId, equipItem.getItemName(), equipItem.itemType, \
                                                    equipItem.getGrade(), equipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, baseAttrsBefore, enhanceAttrsBefore, upgradeAttrsBefore, \
                                                    equipItem.getBaseAttrs(), equipItem.getEnhanceAttrs(), equipItem.getUpgradeAttrs(), gradeBefore, equipItem.getGrade(), bindValueBefore, bindValueAfter, \
                                                    equipItem.getEquipScore(), equipAttrsBefore, equipAttrsAfter)
        self.client.onEquipUpgradeSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, equipItem.getGrade(), equipItem.getEquipScore(), equipItem.getOriginalBindValue(), equipItem.equipAttr.bindValue, equipItem.bindType)

    def unlockBodyEquips(self):
        self.bodyEquipData.doUnlockBodyEquips()

    def isBodyEquipsLocked(self):
        return self.bodyEquipData.isBodyEquipsBeLocked()

    @gamedecorator.checkGameconfigEnable('equip_spirit')
    @utils.isMyself
    def reqEquipSpiritWashing(self, exposed, equipIn, equipPos, spiritPos, uniqueId, itemIds, bindTypes):
        LOG_INFO('in reqEquipSpiritWashing:', equipIn, equipPos, spiritPos, uniqueId, itemIds, bindTypes)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipSpiritWashing(equipPos, uniqueId, spiritPos, itemIds, bindTypes)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                LOG_WARN('    in reqEquipSpiritWashing, equipPos error:', equipPos)
                return
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('   in reqEquipSpiritWashing, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return

            if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                LOG_ERR('   in reqEquipSpiritWashing, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentSpiritType(equipItem.equipAttr.equipType)
            if not ret:
                LOG_ERR('   in reqEquipSpiritWashing, equipment can not affix, equipment:', equipItem)
                return

            # preview 阶段不加锁
            if not equipItem.checkSpiritNum(spiritPos):
                LOG_ERR('    in reqEquipSpiritWashing, slot is empty')
                return

            costItemDic, costCurrencyDic = equipItem.spiritWashingNeedItems()
            if not costItemDic or not costCurrencyDic:
                LOG_ERR(' in reqEquipSpiritWashing, cost is empty:')
                return

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_AFFIX_WASHING
            
            detail = gameclass.AwardDetailCls(uniqueId=equipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
            self.base.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                        'cellEquipSpiritWashingPreview', (opUUID, equipPos, uniqueId, spiritPos))
        return

    def cellEquipSpiritWashingPreview(self, opStat, bindValue, unbinValue, opUUID, slotId, uniqueId, spiritPos):
        LOG_INFO('in cellEquipSpiritWashingPreview:', opStat, bindValue, unbinValue, opUUID, slotId, uniqueId, spiritPos)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_INFO('     in cellEquipSpiritWashingPreview, cost items not enough')
            return
            
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if not equipItem or equipItem.uniqueId != uniqueId:
            LOG_WARN('   in cellEquipSpiritWashingPreview, equip not found or uniqueId not matched:', slotId, uniqueId)
            return

        ret, _, _ = equipItem.doEquipSpiritWashingPreview(self, spiritPos, unbinValue)
        if not ret:
            LOG_ERR('   in cellEquipSpiritWashingPreview, calc preview failed:', slotId, spiritPos)
            return

        previewSpiritData = equipItem.equipAttr.previewSpiritDatas[spiritPos]
        previewScore = equipItem.calcSpiritWashingPreviewScore(spiritPos)
        spiritBindType = gameconst.ItemBindType.BIND if bindValue > 0 else gameconst.ItemBindType.NORMAL
        equipItem.setPreviewSpiritBindType(spiritPos, spiritBindType)
        self.client.onEquipSpiritWashingPreview(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, spiritPos,
                                                previewSpiritData.toClientData(), previewScore,
                                                spiritBindType, equipItem.bindType, opUUID)
        return

    @gamedecorator.checkGameconfigEnable('equip_spirit')
    @utils.isMyself
    def reqEquipSpiritWashingConfirm(self, exposed, equipIn, equipPos, spiritPos, uniqueId):
        LOG_INFO('in reqEquipSpiritWashingConfirm:', equipIn, equipPos, spiritPos, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipSpiritWashingConfirm(equipPos, spiritPos, uniqueId)
            return
        elif equipIn != gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            LOG_WARN('   in reqEquipSpiritWashingConfirm, unknown equipIn:', equipIn)
            return

        equipItem = self.bodyEquipData.getEquipItem(equipPos)
        if not equipItem or equipItem.uniqueId != uniqueId:
            LOG_WARN('   in reqEquipSpiritWashingConfirm, equip not found or uniqueId not matched:', equipPos, uniqueId)
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, spiritPos)
            return

        if spiritPos >= len(equipItem.equipAttr.previewSpiritDatas):
            LOG_WARN('   in reqEquipSpiritWashingConfirm, preview data not found:', equipPos, spiritPos)
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, spiritPos)
            return

        previewSpiritData = equipItem.equipAttr.previewSpiritDatas[spiritPos]
        if not previewSpiritData or len(previewSpiritData.GetSpiritAffixes()) == 0:
            LOG_WARN('   in reqEquipSpiritWashingConfirm, preview data is empty:', equipPos, spiritPos)
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, spiritPos)
            return

        if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipSpiritWashingConfirm'):
            LOG_WARN('   in reqEquipSpiritWashingConfirm, locked')
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, spiritPos)
            return

        spiritDataBefore = equipItem.getSpiritDatas()
        bindValueBefore = equipItem.getBindValue()

        ret = equipItem.doEquipSpiritWashingConfirm(self, spiritPos, onBody=True)
        if not ret:
            LOG_ERR('   in reqEquipSpiritWashingConfirm, apply failed:', equipPos, spiritPos)
            self.unlockBodyEquips()
            self.client.onEquipSpiritWashingConfirmFail(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, spiritPos)
            return

        self.updateEquipmentScore()
        bindValueAfter = equipItem.getBindValue()

        # 记录附灵绑定状态：消耗绑定材料则为绑定，否则为非绑
        spiritBindType = gameconst.ItemBindType.BIND if equipItem.isPreviewSpiritBindType(spiritPos) else gameconst.ItemBindType.NORMAL
        equipItem.removePreviewSpiritBindType(spiritPos)
        equipItem.setSpiritBindType(spiritPos, spiritBindType)

        spiritData = equipItem.equipAttr.spiritDatas[spiritPos]
        self.client.onEquipSpiritWashingSucc(
            gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY,
            equipPos,
            spiritData.toClientData(),
            spiritPos,
            equipItem.getEquipScore(),
            spiritBindType,
            equipItem.bindType
        )
        self.unlockBodyEquips()

        LogTrackingMgr.LogTrackingMgr.equip_spirit(self.gbId, self.clientDistinctIdCell, 0, self.gbId, equipItem.uniqueId, equipItem.itemId, equipItem.getItemName(), equipItem.itemType, \
                                                    equipItem.getGrade(), equipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, spiritDataBefore,\
                                                    equipItem.getSpiritDatas(), 0, 0, spiritBindType, equipItem.getEquipScore(), spiritPos, bindValueBefore, bindValueAfter)
        return

    @gamedecorator.checkGameconfigEnable('equip_soul')
    @utils.isMyself
    def reqEquipSoulSocket(self, exposed, equipIn, equipPos, soulGridId, uniqueId, itemIds, bindTypes):
        LOG_INFO('in reqEquipSoulSocket:', equipIn, equipPos, soulGridId, uniqueId, itemIds, bindTypes)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipSoulSocket(equipPos, uniqueId, soulGridId, itemIds, bindTypes)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                LOG_WARN('    in reqEquipSoulSocket, equipPos error:', equipPos)
                return
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('   in reqEquipSoulSocket, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return

            if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                LOG_ERR('   in reqEquipSoulSocket, equipment can not be growing, equipment:', equipItem)
                return

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipSoulSocket'):
                LOG_WARN('   in reqEquipSoulSocket, locked')
                return

            costItemDic, costCurrencyDic = equipItem.soulSocketNeedItems()
            if not costCurrencyDic:
                LOG_ERR(' in reqEquipSoulSocket, cost is empty:')
                return

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_SOUL
            
            detail = gameclass.AwardDetailCls(uniqueId=equipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
            self.base.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self.base,
                                                        'bodyEquipSoulSocketDeductItemsCB', (opUUID, equipPos, soulGridId))
        return

    def cellEquipSoulSocket(self, opStat, bindValue, unbinValue, opUUID, slotId, rollProps, soulItemId, soulBindType):
        LOG_INFO('in cellEquipSoulSocket:', opStat, bindValue, opUUID, slotId, rollProps, soulItemId)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_INFO('     in cellEquipSoulSocket, cost items not enough')
            return
            
        equipItem = self.bodyEquipData.getEquipItem(slotId)

        # 记录魂魄绑定状态
        equipItem.setSoulBindType(soulBindType)
        
        equipItem.removeEquipEffectToAvatar(self)
        ret = equipItem.doEquipSoulSocket(self, rollProps, soulItemId, True)
        equipItem.applyEquipEffectToAvatar(self)
        self.updateEquipmentScore()
        if ret:
            soulAffixes = []
            for oneAffix in equipItem.equipAttr.soulAffixes:
                soulAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipSoulSocketSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, soulAffixes, 
                                                 equipItem.getEquipScore(), equipItem.equipAttr.soulBindType, equipItem.bindType, soulItemId)
        return

    @gamedecorator.checkGameconfigEnable('equip_weaponGlyph')
    @utils.isMyself
    def reqEquipGlyphApply(self, exposed, equipIn, equipPos, groupId, uniqueId):
        LOG_INFO('in reqEquipGlyphApply:', equipIn, equipPos, groupId, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipGlyphApply(equipPos, uniqueId, groupId)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                LOG_WARN('    in reqEquipGlyphApply, equipPos error:', equipPos)
                return
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('   in reqEquipGlyphApply, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return

            if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                LOG_ERR('   in reqEquipGlyphApply, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentGlyphType(equipItem.equipAttr.equipType)
            if not ret:
                LOG_ERR('   in reqEquipGlyphApply, equipment can not glyph, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipGlyphApply'):
                LOG_WARN('   in reqEquipGlyphApply, locked')
                return

            if not equipItem.checkGlyphApplyGroupId(groupId):
                LOG_ERR('   in reqEquipGlyphApply groupId is wrong')
                return
            self.unlockBodyEquips()
            equipItem.removeEquipEffectToAvatar(self)
            ret = equipItem.doApplyGlyphGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, groupId)
            # 只要存在变动就更新
            if ret:
                self.bodyEquipData.recalculateAllInscriptionEffects(self)
            equipItem.applyEquipEffectToAvatar(self)
            self.updateEquipmentScore()
            self.client.onEquipGlyphApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, groupId, equipItem.getEquipScore())
        return

    @gamedecorator.checkGameconfigEnable('equip_spirit')
    @utils.isMyself
    def reqEquipSpiritApply(self, exposed, equipIn, equipPos, groupId, uniqueId):
        LOG_INFO('in reqEquipSpiritApply:', equipIn, equipPos, groupId, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipSpiritApply(equipPos, uniqueId, groupId)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                LOG_WARN('    in reqEquipSpiritApply, equipPos error:', equipPos)
                return
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('   in reqEquipSpiritApply, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return

            if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                LOG_ERR('   in reqEquipSpiritApply, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentSpiritType(equipItem.equipAttr.equipType)
            if not ret:
                LOG_ERR('   in reqEquipSpiritApply, equipment can not glyph, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipSpiritApply'):
                LOG_WARN('   in reqEquipSpiritApply, locked')
                return

            if not equipItem.checkSpiritApplyGroupId(groupId):
                LOG_ERR('   in reqEquipSpiritApply groupId is wrong')
                return
            self.unlockBodyEquips()
            equipItem.removeEquipEffectToAvatar(self)
            equipItem.doApplySpiritGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, groupId)
            equipItem.applyEquipEffectToAvatar(self)
            self.updateEquipmentScore()
            self.client.onEquipSpiritApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, groupId, equipItem.getEquipScore())
        return

    @gamedecorator.checkGameconfigEnable('equip_weaponGlyph')
    @utils.isMyself
    def reqEquipGlyphWashing(self, exposed, equipIn, equipPos, glyphPos, uniqueId, itemIds, bindTypes):
        LOG_INFO('in reqEquipGlyphWashing:', equipIn, equipPos, glyphPos, uniqueId, itemIds, bindTypes)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipGlyphWashing(equipPos, uniqueId, glyphPos, itemIds, bindTypes)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                LOG_WARN('    in reqEquipGlyphWashing, equipPos error:', equipPos)
                return
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('   in reqEquipGlyphWashing, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return

            if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                LOG_ERR('   in reqEquipGlyphWashing, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentGlyphType(equipItem.equipAttr.equipType)
            if not ret:
                LOG_ERR('   in reqEquipGlyphWashing, equipment can not glyph, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipGlyphWashing'):
                LOG_WARN('   in reqEquipGlyphWashing, locked')
                return

            if not equipItem.checkGlyphNum(glyphPos):
                LOG_ERR('in reqEquipGlyphWashing slot is empty')
                return

            costItemDic, costCurrencyDic = equipItem.glyphWashingNeedItems()
            if not costItemDic or not costCurrencyDic:
                LOG_ERR(' in reqEquipGlyphWashing, cost is empty:')
                return

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_WEAPON_GLYPH_WASHING
            
            detail = gameclass.AwardDetailCls(uniqueId=equipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
            self.base.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                        'cellEquipGlyphWashing', (opUUID, equipPos, uniqueId, glyphPos))
        return

    def cellEquipGlyphWashing(self, opStat, bindValue, opUUID, slotId, uniqueId, glyphPos):
        LOG_INFO('in cellEquipGlyphWashing:', opStat, bindValue, opUUID, slotId, uniqueId, glyphPos)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_INFO('     in cellEquipGlyphWashing, cost items not enough')
            return
        equipItem = self.bodyEquipData.getEquipItem(slotId)

        glyphDataBefore = equipItem.getGlyphDatas()
        bindValueBefore = equipItem.getBindValue()
        equipItem.removeEquipEffectToAvatar(self)
        ret, _, _ = equipItem.doEquipGlyphWashing(self, glyphPos)

        equipItem.applyEquipEffectToAvatar(self)
        self.updateEquipmentScore()
        bindValueAfter = equipItem.getBindValue()
        if ret:
            # 记录铭文绑定状态
            glyphBindType = gameconst.ItemBindType.BIND if bindValue > 0 else gameconst.ItemBindType.NORMAL
            equipItem.setGlyphBindType(glyphPos, glyphBindType)
            glyphData = equipItem.equipAttr.getGlyphData(glyphPos)
            self.bodyEquipData.recalculateAllInscriptionEffects(self)
            
            LogTrackingMgr.LogTrackingMgr.equip_glyph(self.gbId, self.clientDistinctIdCell, opUUID, self.gbId, equipItem.uniqueId, equipItem.itemId, equipItem.getItemName(), equipItem.itemType, \
                                                        equipItem.getGrade(), equipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, glyphDataBefore,\
                                                        equipItem.getGlyphDatas(), 0, 0, bindValue, equipItem.getEquipScore(), glyphPos // 2, glyphPos, bindValueBefore, bindValueAfter)


            self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, glyphPos, glyphData.toClientData(),
                                                equipItem.getEquipScore(), glyphBindType, equipItem.bindType)
            
            self.base.triggerAchievement(gameconst.AchieveType.INSCRIPTION)
        return

    @gamedecorator.checkGameconfigEnable('equip_bless')
    @utils.isMyself
    def reqEquipBless(self, exposed, equipIn, equipPos, uniqueId, itemIds, bindTypes):
        LOG_INFO('in reqEquipBless:', equipIn, equipPos, uniqueId, itemIds, bindTypes)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipBless(equipPos, uniqueId, itemIds, bindTypes)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                LOG_WARN('    in reqEquipBless, equipPos error:', equipPos)
                return
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('   in reqEquipBless, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return

            if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                LOG_ERR('   in reqEquipBless, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentBlessType(equipItem.equipAttr.equipType, equipItem.getQuality())
            if not ret:
                LOG_ERR('   in reqEquipBless, equipment can not bless, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipBless'):
                LOG_WARN('   in reqEquipBless, locked')
                return

            costItemDic, costCurrencyDic = equipItem.blessNeedItems()
            if not costItemDic or not costCurrencyDic:
                LOG_ERR('     in reqEquipBless, cost is empty:')
                return
            
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_BLESSING
            
            detail = gameclass.AwardDetailCls(uniqueId=equipItem.uniqueId, costCurrencyDic=costCurrencyDic, costItemDic=costItemDic)
            self.base.baseEquipDeductItemsWithBindTypes(costCurrencyDic, costItemDic, itemIds, bindTypes, opUUID, srcType, detail, self,
                                                        'cellEquipBless', (opUUID, equipPos, uniqueId))
        return

    def cellEquipBless(self, opStat, bindValue, opUUID, slotId, uniqueId):
        LOG_INFO('in cellEquipBless:', opStat, bindValue, opUUID, slotId, uniqueId)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            LOG_INFO('     in cellEquipBless, cost items not enough')
            return
        equipItem = self.bodyEquipData.getEquipItem(slotId)

        blessDataBefore = equipItem.getBlessDatas()
        blessLvRateBefore = equipItem.getBlessLvRate()
        maxBlessLvBefore = equipItem.getBlessMaxLv()
        bindValueBefore = equipItem.getBindValue()
        if bindValue > 0:
            equipItem.addBindBlessCost(bindValue)
        equipItem.removeEquipEffectToAvatar(self)
        ret = equipItem.doEquipBlessing(self)
        equipItem.applyEquipEffectToAvatar(self)

        self.bodyEquipData.changeAvatarAttrs(self)

        self.updateEquipmentScore()
        bindValueAfter = equipItem.getBindValue()
        if ret:
            LogTrackingMgr.LogTrackingMgr.equip_bless(self.gbId, self.clientDistinctIdCell, opUUID, self.gbId, equipItem.uniqueId, equipItem.itemId, equipItem.getItemName(), equipItem.itemType, \
                                                        equipItem.getGrade(), equipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, blessDataBefore, \
                                                        equipItem.getBlessDatas(), 0, 0, bindValue, blessLvRateBefore, equipItem.getBlessLvRate(), \
                                                        maxBlessLvBefore, equipItem.getBlessMaxLv(), equipItem.getEquipScore(), bindValueBefore, bindValueAfter)

            blessAffixes = []
            for oneAffix in equipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            
            self.client.onEquipBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, blessAffixes,
                                        equipItem.equipAttr.maxBlessLv, equipItem.equipAttr.blessLvRate,
                                        equipItem.getEquipScore(), equipItem.equipAttr.bindBlessCost, equipItem.bindType)
        return

    @gamedecorator.checkGameconfigEnable('equip_bless')
    @utils.isMyself
    def reqEquipBackBless(self, exposed, equipIn, equipPos, uniqueId):
        LOG_INFO('in reqEquipBackBless:', equipIn, equipPos, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipBackBless(equipPos, uniqueId)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                LOG_WARN('    in reqEquipBackBless, equipPos error:', equipPos)
                return
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('   in reqEquipBackBless, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return

            ret = dataUtils.checkEquipmentBlessType(equipItem.equipAttr.equipType, equipItem.getQuality())
            if not ret:
                LOG_ERR('     in reqEquipBackBless, not bless type')
                return

            if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                LOG_ERR('   in reqEquipBackBless, equipment can not be growing, equipment:', equipItem)
                return

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipBless'):
                LOG_WARN('   in reqEquipBackBless, locked')
                return

            if not equipItem.isCanBackBless():
                LOG_ERR('     in reqEquipBackBless, not can backBless')
                return

            self.unlockBodyEquips()
            equipItem.removeEquipEffectToAvatar(self)
            equipItem.doEquipBackBless()
            equipItem.applyEquipEffectToAvatar(self)
            self.updateEquipmentScore()
            blessAffixes = []
            for oneAffix in equipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBackBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, blessAffixes,
                                            equipItem.equipAttr.maxBlessLv, equipItem.equipAttr.blessLvRate,
                                            equipItem.getEquipScore())
        return

    def getBodyEquipExtraSkillLv(self, skillId):
        return self.bodyEquipData.getEquipsAddSkillLv(self, skillId)

    def addPropByGear(self, _, ctx, propList, startIdx=0, endIdx=-1):
        if ctx.actionType == actionContext.ACTION_EQUIP:
            ctx.affixItem.addPropByEquip(self, propList, ctx.affixVals, startIdx=startIdx, endIdx=endIdx)
        elif ctx.actionType == actionContext.ACTION_EQUIP_SET:
            ctx.bodyEquips.addPropBySet(self, propList, ctx.vals, startIdx=startIdx, endIdx=endIdx)

    def onBodyEquipLoseSoulRecovery(self, equipUniqueIdList):
        LOG_INFO('in onBodyEquipLoseSoulRecovery:', equipUniqueIdList)
        gridIdList = []
        equipDataList = []
        for _uniqueId in equipUniqueIdList:
            slotId, _equipItem = self.bodyEquipData.getBodyEquipByUniqueId(_uniqueId)
            if not _equipItem:
                LOG_WARN('       in onBodyEquipLoseSoulRecovery, no lose soul equip:', slotId, _uniqueId)
                continue

            if _equipItem.loseSoulHasFixed():
                LOG_WARN('       in onBodyEquipLoseSoulRecovery, equip already return to normal:', slotId, _equipItem.itemId)
                continue

            _equipItem.fixLoseSoul()
            _equipItem.applyEquipEffectToAvatar(self)
            gridIdList.append(slotId)
            equipDataList.append(_equipItem.toClientEquipItemDict())

        if gridIdList:
            self.updateEquipmentScore()
            self.client.onEquipFixLoseSoulSucc(
                gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, gridIdList, equipDataList)

    def sendItemLinkInfoCell(self, box, uniqueId, itemId):
        if dataUtils.isEquipItemByItemId(itemId):
            for _item in self.bodyEquipData.equips_map.values():
                if _item.itemId == itemId and _item.uniqueId == uniqueId:
                    box.client.onQueryItemLink(uniqueId, _item.toItemSavedDict())
                    return
        box.onMessagePre(MMD.datas.channel_noItem, [])

    ################################## Gm cmd ###################################
    def gmDressEquips(self, quality):
        dressSlotIds = []
        for slotId in range(1, 11):
            it = self.bodyEquipData.getEquipItem(slotId)
            if not it:
                dressSlotIds.append(slotId)
                continue

        if len(dressSlotIds) == 0:
            return False
        self.base.gmBaseDressEquips(dressSlotIds, quality)
        return True

    def gmModifyEquipEnhanceLevel(self, slotId, enhanceLevel):
        LOG_INFO('in modifyEquipEnhanceLevel, slotId:', slotId, enhanceLevel)
        opUUID = KBEngine.genUUID64()
        enhanceResults = []
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if not equipItem.checkEnhancementValid(enhanceLevel + 1, False):
            return False
        
        enhanceVal = equipItem.doEnhanceEquip(self, opUUID, enhanceLevel, onBody=True, isGM=True)
        self.base.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
        enhanceResults.append([gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId,
                               enhanceVal, equipItem.itemId, equipItem.uniqueId, equipItem.getEnhanceLevel(),
                               equipItem.getEquipScore(), equipItem.equipAttr.bindEnhanceCost,
                               equipItem.bindType, equipItem.getMaxEnhanceLevel(),
                               ])
        self.updateEquipmentScore()
        
        equipEnhanceDatas = []
        equipConsumedDatas = []
        for enhanceResult in enhanceResults:
            equipEnhanceDatas.append({
                'eqipIn': enhanceResult[0],
                'eqipPos': enhanceResult[1],
                'enhanceVal': enhanceResult[2],
                'itemId': enhanceResult[3],
                'uniqueId': enhanceResult[4],
                'enhanceLv': enhanceResult[5],
                'score': enhanceResult[6],
                'bindEnhanceCost': enhanceResult[7],
                'bindType': enhanceResult[8],
                'maxEnhanceLv': enhanceResult[9],
            })

        self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.OK, equipEnhanceDatas, equipConsumedDatas, False)
        return True
    

    def gmGlyphWashingEquips(self, equipPos, glyphPos, itemId, affixId1, affixId2):
        if equipPos == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.gmGlyphWashingEquips(itemId, glyphPos, affixId1, affixId2)
            # 异步rpc, 先return true了，后面考虑改造下gm系统，让异步也有回包
            return True
        elif equipPos == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            allEquipItems = self.bodyEquipData.getAllEquipItems()
            for slotId, equipItem in allEquipItems.items():
                if equipItem.itemId != itemId:
                    continue
                if dataUtils.checkEquipGrowingForbidden(self.gbId, equipItem):
                    LOG_ERR('in gmGlyphWashingEquips, equipment can not be growing, equipment:', equipItem)
                    return

                ret = dataUtils.checkEquipmentGlyphType(equipItem.equipAttr.equipType)
                if not ret:
                    LOG_ERR('in gmGlyphWashingEquips, equipment can not glyph, equipment:', equipItem)
                    return False

                if not equipItem.checkGlyphNum(glyphPos):
                    LOG_ERR('in gmGlyphWashingEquips slot is empty')
                    return

                ret, _, _ = equipItem.doEquipGlyphWashing(self, glyphPos, affixIds=[affixId1, affixId2])
                if ret:
                    glyphData = equipItem.equipAttr.getGlyphData(glyphPos)
                    glyphBindType = gameconst.ItemBindType.BIND if glyphPos in equipItem.equipAttr.glyphBindTypes else gameconst.ItemBindType.NORMAL
                    self.bodyEquipData.recalculateAllInscriptionEffects(self)
                    self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, glyphPos, glyphData.toClientData(),
                                                        equipItem.getEquipScore(), glyphBindType, equipItem.bindType)
            return True
        else:
            LOG_ERR('in gmGlyphWashingEquips, error equipPos ', equipPos, itemId, affixId1, affixId2)
        return False
    ################################## gm cmd end ###################################

    ################################### drop equip start ##############################
    def takeEquip(self, uniqueId):
        LOG_INFO('in takeEquip, uniqueId:', uniqueId)
        self.base.takeEquipBase(uniqueId, self.spaceNo, self.position)

    def _dealDeathDrop(self, killerGbId, killerName, dropGearType):
        if dropGearType == 0:
            return
        
        if not gameconfig.visibleConfigEnabled('deathDrop'):
            return

        if dropGearType == 1:
            if not (self._isCritInjured() or (self.moralValue <= GB_GCD.datas['equipDropMoralBound']['value'])):
                return
        else:
            return

        #人在跨服，本服不处理爆装
        if self.isCrossServerInLocalServer:
            return

        _moral = min(GB_GCD.datas['equipDropMoralBound']['value'], self.moralValue)
        _formulaId = GB_GCD.datas['equipDropProbFormulaID']['value']
        _formulaFunc = F_GFD.datas[_formulaId]['serverFormula']

        if self._isCritInjured():
            _moral = min(_moral, GB_GCD.datas['equipDropSeriousInjury']['value'])

        _ratio = _formulaFunc(_moral)
        if random.random() >= _ratio:
            return

        _weights = []
        _slotIds = []
        for _slotId, _item in self.bodyEquipData.equips_map.items():
            _slotIds.append(_slotId)
            _type = _item.equipAttr.equipType
            _weights.append(GB_TTD.datas[_type]['deathDropWeight'])

        if not _weights:
            return

        _idx = utils.randomByWeight(_weights)
        _slotId = _slotIds[_idx]
        LOG_INFO('will drop equip:', _slotId)
        self.dropEquip(_slotId, killerGbId, killerName)

    def dropEquip(self, slotId, killerGbId=0, killerName=''):
        LOG_INFO('in dropEquip, slotId:', slotId)
        bodyEquip = self.bodyEquipData.doBodyUndressEquip(self, slotId)
        if not bodyEquip:
            LOG_ERR('in dropEquip, no equip in slotId:', slotId)
            return
        
        LogTrackingMgr.LogTrackingMgr.drop_equip(
            self.gbId,
            self.clientDistinctIdCell, 
            self.gbId,
            self.name,
            self.accountNameCell,
            bodyEquip.uniqueId,
            bodyEquip.itemId,
            bodyEquip.getQuality(),
            bodyEquip.getGrade(),
            formula.fetchMapId(self.spaceNo),
            str(self.position),
        )

        self.dropEquipByItem(bodyEquip, killerName)

    def dropEquipByItem(self, bodyEquip, killerName):
        # 自动更新返还信息
        isFirst = bodyEquip.updateOwnerInfo(self.gbId, gameconfig.serverId())
        # 检查掉落列表已满
        baseDropInfo = self.getDropBaseInfo(bodyEquip.getOwnerGbId(), bodyEquip.getReturnTime(), bodyEquip.getOwnerServerId(), killerName, bodyEquip.getEquipScore(), bodyEquip.equipAttr.quality, bodyEquip.getGrade(), bodyEquip.uniqueId, isFirst)
        self.base.checkDropEquip(bodyEquip.toItemSavedDict(), baseDropInfo)

    def getDropBaseInfo(self, ownerId, returnTime, ownerServerId, killerName, score, quality, grade, uniqueId, isFirst):
        baseInfo = {}
        _formulaId = GB_GCD.datas['equipRepairCostAmount']['value']
        _formulaFunc = F_GFD.datas[_formulaId]['serverFormula']
        _dropCtx = actionContext.DropEquipCtx(
            score,
            quality,
            grade
        )

        _now = utils.curTS()
        _extraBlob = {
            'n': killerName, # 名字
            'm': self.spaceNo,
            'p': (self.position[0], self.position[1], self.position[2])
        }
        baseInfo['killerName'] = killerName
        baseInfo['extraBlob'] = cPickle.dumps(_extraBlob)
        baseInfo['quality'] = quality
        baseInfo['price'] = int(_formulaFunc(_dropCtx))
        baseInfo['uuid'] = uniqueId
        baseInfo['collectEndTime'] = _now + GB_GCD.datas['equipDropPickLiveTime']['value']
        baseInfo['fixEndTime'] = _now + GB_GCD.datas['equipDamageDestructionTime']['value']
        baseInfo['mapId'] = self.spaceNo
        baseInfo['position'] = self.position
        baseInfo['ownerId'] = ownerId
        baseInfo['returnTime'] = returnTime
        baseInfo['direction'] = self.direction
        baseInfo['spaceMgrId'] = self.spaceMgrId
        baseInfo['spaceId'] = self.spaceID
        baseInfo['dropTime'] = _now
        baseInfo['ownerServerId'] = ownerServerId
        baseInfo['isFirst'] = isFirst
        return baseInfo

    def doDropEquipByItem(self, baseInfo, _equipInfo):
        _collectionId = QD_QDD.datas[baseInfo['quality']]['equipDropPickID']
        _props = {
            'collectionId': _collectionId,
            'spaceNo': baseInfo['mapId'],
            'position': baseInfo['position'],
            'direction': baseInfo['direction'],
            'spaceMgrId': baseInfo['spaceMgrId'],
            'disappearTime': baseInfo['collectEndTime'],
            'dropEquipId': baseInfo['uuid'],
            'dropEquipItemId': _equipInfo['itemId'],
        }

        _ent = KBEngine.createEntity('Collection', baseInfo['spaceId'], baseInfo['position'], baseInfo['direction'], _props)
        self.base.onDropEquipBase(baseInfo['ownerId'], baseInfo['returnTime'], baseInfo['ownerServerId'], baseInfo['uuid'], baseInfo['price'], \
                                  baseInfo['mapId'], baseInfo['position'], _equipInfo, baseInfo['collectEndTime'], \
                                  baseInfo['killerName'], baseInfo['fixEndTime'], baseInfo['extraBlob'], _ent.id, baseInfo['dropTime'], baseInfo['isFirst'])

        _mailId = GB_GCD.datas['equipDamageMailID']['value']
        _args = [
            _equipInfo['itemId'],
            self.gbId,
            int(baseInfo['position'][0]),
            int(baseInfo['position'][2]),
            baseInfo['mapId'],
        ]

        mailAssistor.sendMailToPlayers(
            [self.gbId],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args,
            srcType=AAC_AACDD.datas.BONUS_SRC_EQUIPMENT_DROP
        )

    def onRemoveEquipNotifyCell(self, uniqueId):
        LOG_INFO('in onRemoveEquipNotifyCell:', uniqueId)
        slotId, equipItem = self.bodyEquipData.getEquipItemByUniqueId(uniqueId)
        if not (slotId is None):
            self.bodyEquipData.doBodyUndressEquip(self, slotId)
        else:
            LOG_ERR('in onRemoveEquipNotifyCell, missing equip:', uniqueId)
        
    ################################### drop equip end ##############################

    @gamedecorator.checkGameconfigEnable('equip_unbundle')
    @utils.isMyself
    def reqEquipWash(self, exposed, equipIn, equipPos, uniqueId, washType, count):
        LOG_INFO('in reqEquipWash:', equipIn, equipPos, uniqueId, washType, count)

        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipWash(equipPos, uniqueId, washType, count)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem or equipItem.uniqueId != uniqueId:
                self.client.onEquipWashReply(gameconst.EquipWashResult.EQUIP_NOT_FOUND, '', equipPos, uniqueId, washType, 0)
                return

            resultCode, actualCount, costItemDic = equipItem.checkEquipWashCost(washType, count)
            if resultCode != gameconst.EquipWashResult.OK:
                self.client.onEquipWashReply(resultCode, '', equipPos, uniqueId, washType, 0)
                return

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipWash'):
                self.client.onEquipWashReply(gameconst.EquipWashResult.BAG_LOCKED, '', equipPos, uniqueId, washType, 0)
                return

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_EQUIP_WASH
            detail = gameclass.AwardDetailCls(uniqueId=equipItem.uniqueId, costItemDic=costItemDic)
            self.base.baseEquipWashDeductItems(
                costItemDic,
                opUUID, 
                srcType, 
                detail, 
                self,
                'cellEquipWash', 
                [opUUID, equipPos, uniqueId, washType, actualCount]
            )
        return

    def cellEquipWash(self, opStat, opUUID, slotId, uniqueId, washType, actualCount):
        LOG_INFO('in cellEquipWash:', opStat, slotId, uniqueId, washType, actualCount)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            self.client.onEquipWashReply(gameconst.EquipWashResult.ITEM_NOT_ENOUGH, '', slotId, uniqueId, washType, 0)
            return

        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if not equipItem or equipItem.uniqueId != uniqueId:
            self.client.onEquipWashReply(gameconst.EquipWashResult.EQUIP_NOT_FOUND, '', slotId, uniqueId, washType, 0)
            return

        equipItem.doEquipWash(washType, actualCount)
        self.client.onEquipWashReply(gameconst.EquipWashResult.OK, '', slotId, uniqueId, washType, actualCount)
        return

    def recalculateAllInscriptionEffects(self, isRelogin):
        LOG_INFO('in recalculateAllInscriptionEffects:', isRelogin)
        self.bodyEquipData.recalculateAllInscriptionEffects(self)

    @gamedecorator.checkGameconfigEnable('equip_strengthen')
    @utils.isMyself
    def reqMultiEquipEnhance(self, exposed, equipIn, equipPos, equipUniqueIds, itemIds, bindTypes, isMulti):
        LOG_INFO('reqMultiEquipEnhance:', exposed, equipIn, equipPos, equipUniqueIds, itemIds, bindTypes, isMulti)
        if len(equipIn) == 0 or len(equipIn) > int(GE_GC.datas['gearEnhance_listNumLimit']['value']) \
            or len(equipIn) != len(equipPos) or len(equipIn) != len(equipUniqueIds) or len(itemIds) == 0 \
            or len(itemIds) != len(bindTypes):
            
            self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ARG_ERR, [], [], isMulti)
            LOG_WARN('reqMultiEquipEnhance, wrong args 1:')
            return
        
        if not self.bodyEquipData.tryLockBodyEquips(desp='reqMultiEquipEnhance'):
            self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.BODY_EQUIP_LOCKED, [], [], isMulti)
            LOG_WARN('reqMultiEquipEnhance, body equip data is locked')
            return
        
        # 背包部分强化
        bagEquipDatas = {}
        # 穿戴部分强化
        validBodyItems = {}
        for idx in range(0, len(equipIn)):
            ins = equipIn[idx]
            pos = equipPos[idx]
            ids = equipUniqueIds[idx]
            if ins == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
                bagEquipDatas[pos] = ids
            elif ins == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
                ret, equipItem, currencyDic, costItemDic, isTopLevel = self.checkBodyEquipEnhanceConditions(pos, ids)
                if not ret:
                    if isTopLevel:
                        continue
                    self.unlockBodyEquips()
                    self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ARG_ERR, [], [], isMulti)
                    LOG_WARN('reqMultiEquipEnhance, wrong args 2:', ins, pos, ids)
                    return
                validBodyItems[equipItem.uniqueId] = [pos, False, currencyDic, costItemDic]
            else:
                self.unlockBodyEquips()
                self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ARG_ERR, [], [], isMulti)
                LOG_WARN('reqMultiEquipEnhance, wrong args 3:', ins, pos, ids)
                return
        # 检查下参与强化的装备数据
        if len(bagEquipDatas) == 0 and len(validBodyItems) == 0:
            self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.ARG_ERR, [], [], isMulti)
            LOG_WARN('reqMultiEquipEnhance, wrong args 4:', bagEquipDatas, validBodyItems)
            return  
        self.base.baseMultiEquipEnhance(equipUniqueIds, bagEquipDatas, validBodyItems, itemIds, bindTypes, isMulti)

    def cellMultiEquipEnhance(self, opUUID, bodyEquipInfos, bodyEquipBindInfos, enhanceResults, consumedItemInfos, isMulti):
        LOG_INFO('cellMultiEquipEnhance:', bodyEquipInfos, bodyEquipBindInfos, consumedItemInfos, isMulti)
        self.unlockBodyEquips()
        for bodyEquipInfo in bodyEquipInfos:
            slotId, uniqueId = bodyEquipInfo
            equipItem = self.bodyEquipData.getEquipItem(slotId)
            if not equipItem:
                LOG_WARN('cellMultiEquipEnhance, wrong arg 1:', slotId, uniqueId)
                continue
            if equipItem.uniqueId != uniqueId:
                LOG_WARN('cellMultiEquipEnhance, wrong arg: 2', slotId, equipItem.uniqueId, uniqueId)
                continue

            bindInfo = bodyEquipBindInfos.get(uniqueId, None)
            if not bindInfo:
                LOG_WARN('cellMultiEquipEnhance, wrong arg: 3', slotId, equipItem.uniqueId, uniqueId)
                continue
            bindValue = bindInfo[0]

            baseAttrsBefore = equipItem.getBaseAttrs()
            enhanceAttrsBefore = equipItem.getEnhanceAttrs()
            upgradeAttrsBefore = equipItem.getUpgradeAttrs()
            levelBefore = equipItem.getEnhanceLevel()
            bindValueBefore = equipItem.getBindValue()

            if bindValue > 0:
                # 记录强化消耗的绑定强化石数量（用于装备洗涤）
                equipItem.addBindEnhanceCost(bindValue)

            enhanceLv = equipItem.equipAttr.getEnhanceLv()
            checkEnhanceLv = enhanceLv + 1
            equipItem.checkEnhancementValid(checkEnhanceLv, False)
            enhanceVal = equipItem.doEnhanceEquip(self, opUUID, enhanceLv, onBody=True)
            bindValueAfter = equipItem.getBindValue()
            # 装备破碎了
            if enhanceVal == gameconst.EquipConstVale.ENHANCEMENT_BROKEN_FLAG:
                bodyEquip = self.bodyEquipData.doBodyUndressEquip(self, slotId)
                if bodyEquip:
                    srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_BODY_EQUIP
                    self.base.cellBrokenEquipment(srcType, opUUID, bodyEquip.toItemSavedDict())

            equipAttrsBefore = {
                'baseAttrs':baseAttrsBefore,
                'upgradeAttrs':upgradeAttrsBefore,
                'enhanceAttrs':enhanceAttrsBefore,
            }
            equipAttrsAfter = {
                'baseAttrs':equipItem.getBaseAttrs(),
                'upgradeAttrs':equipItem.getUpgradeAttrs(),
                'enhanceAttrs':equipItem.getEnhanceAttrs(),
            }
            
            LogTrackingMgr.LogTrackingMgr.equip_enhancement(self.gbId, self.clientDistinctIdCell, opUUID, self.gbId, equipItem.uniqueId, equipItem.itemId, equipItem.getItemName(), equipItem.itemType, \
                                                            equipItem.getGrade(), equipItem.getQuality(), gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, baseAttrsBefore, enhanceAttrsBefore, \
                                                            upgradeAttrsBefore, equipItem.getBaseAttrs(), equipItem.getEnhanceAttrs(), equipItem.getUpgradeAttrs(), 0, 0, bindValue, levelBefore, equipItem.getEnhanceLevel(), enhanceVal, equipItem.getEquipScore(), \
                                                            bindValueBefore, bindValueAfter, equipAttrsBefore, equipAttrsAfter)

            self.base.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            enhanceResults.append([gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, enhanceVal,
                                   equipItem.itemId, equipItem.uniqueId, equipItem.getEnhanceLevel(),
                                   equipItem.getEquipScore(), equipItem.equipAttr.bindEnhanceCost,
                                   equipItem.bindType, equipItem.getMaxEnhanceLevel(),
                                   ])
        self.updateEquipmentScore()
        
        
        equipEnhanceDatas = []
        equipConsumedDatas = []

        for enhanceResult in enhanceResults:
            equipEnhanceDatas.append({
                'eqipIn': enhanceResult[0],
                'eqipPos': enhanceResult[1],
                'enhanceVal': enhanceResult[2],
                'itemId': enhanceResult[3],
                'uniqueId': enhanceResult[4],
                'enhanceLv': enhanceResult[5],
                'score': enhanceResult[6],
                'bindEnhanceCost': enhanceResult[7],
                'bindType': enhanceResult[8],
                'maxEnhanceLv': enhanceResult[9],
            })
        
        for itemId, bindInfo in consumedItemInfos.items():
            bindCount = bindInfo[0]
            normalCount = bindInfo[1]
            if bindCount > 0:
                equipConsumedDatas.append({
                    'itemId':itemId,
                    'itemNum':bindCount,
                    'bindType':gameconst.ItemBindType.BIND
                    })
            if normalCount > 0:
                equipConsumedDatas.append({
                    'itemId':itemId,
                    'itemNum':normalCount,
                    'bindType':gameconst.ItemBindType.NORMAL
                    })
        self.client.onMultiEquipEnhance(gameconst.EquipMultiEnhanceResult.OK, equipEnhanceDatas, equipConsumedDatas, isMulti)

    def updateEquipQualityAchievement(self):
        qualityData = {}
        for equipObj in self.bodyEquipData.equips_map.values():
            quality = equipObj.getQuality()
            if quality not in qualityData:
                qualityData[quality] = 0
            qualityData[quality] += 1
        self.base.triggerAchievementWithCtx(gameconst.AchieveType.EQUIP_QUALITY, actionContext.AchievementCtx(qualityData=qualityData))

    def _checkEquipExpire(self):
        self.bodyEquipData.checkEquipExpire(self)

  
