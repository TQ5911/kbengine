# -*- encoding:utf-8 -*-
from KBEDebug import *
import KBEngine
import utils
import gameconst
import random
import mailAssistor
import const_const as CCT
import message_Message_def as MMD
import actionContext
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemFactory
import gameengine
import value_value as VLVLD
import dataUtils
import json
import formula
import gzip
import actionContext
import conflict_conflict_def as CCD
import gameclass
import gamedecorator
import _pickle as cPickle
import gearBase_gearConst as GB_GCD
import formula_generalFormula as F_GFD
import gearBase_typeTab as GB_TTD
import gamePlay_gamePlay as GP_GPD
import qualityData_qualityData as QD_QDD
import affix_affixTypeWeight as AFAFTWD

class ImpEquipment(object):
    def __init__(self):
        super(ImpEquipment, self).__init__()

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def reqSetEquipSuitHide(self, exposed, needHide):
        DEBUG_MSG('ImpEquipment::reqSetEquipSuitHide~', needHide)
        self.appearance.onEquipDisplayChanged(self, needHide)

    def sendBodyEquipData(self):
        self.sendStreamBodyEquipData()

    def sendStreamBodyEquipData(self):
        dic = self.bodyEquipData.toBodyEquipsClientDict()
        jsonStr = json.dumps(dic).encode('ascii')
        zStr = gzip.compress(jsonStr)
        self.base.streamStringProxy(zStr, '', gameconst.StreamStringID.BODY_EQUIP_DATA)
        return

    def applyBodyEquipsOnLogin(self):
        self.bodyEquipData.applyBodyEquipsProps(self, isLogin=True)

    def syncBodyEquipDressData(self):
        self.base.updateBodyEquipDressData(self.bodyEquipData.getBodyEquipScoreDic())

    def cellDressEquipment(self, opUUID, gridObjDic, dstSlotId):
        DEBUG_MSG('in cellDressEquipment:', dstSlotId)
        if not self.bodyEquipData.tryLockBodyEquips(desp='cellDressEquipment'):
            WARNING_MSG('   in cellDressEquipment, locked')
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpStat.EQUIP_OP_FAILED, {})
            return

        if not self.checkConflictState(CCD.datas.changeGear, True):
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpStat.EQUIP_OP_FAILED, {})
            self.unlockBodyEquips()
            return

        bagEquipItem = itemFactory.ItemFactory.createItemWithSavedDict(gridObjDic)
        slotId, bodyEquipItem = self.bodyEquipData.getDressSlotInfo(bagEquipItem, dstSlotId)
        if slotId is None:
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpStat.EQUIP_OP_FAILED, {})
            self.unlockBodyEquips()
            return

        if bodyEquipItem is None:
            # only dress
            self.bodyEquipData.dressEquip(self, slotId, bagEquipItem)
            self.base.dressEquipmentCB(opUUID, gameconst.DressEquipOpStat.EQUIP_OP_ONLY_DRESS,
                                       bagEquipItem.toItemSavedDict())
            self.unlockBodyEquips()
            self.client.onDressEquipment(bagEquipItem.toClientBodyEquipItemDict(slotId))
            return

        self.unlockBodyEquips()
        self.replaceBodyEquip(slotId, opUUID, bagEquipItem, bodyEquipItem)
        return

    def replaceBodyEquip(self, slotId, opUUID, bagEquipItem, bodyEquipItem, swapEnhance=False):
        DEBUG_MSG('replaceBodyEquip:', slotId, opUUID, bagEquipItem.itemId, bodyEquipItem.itemId, swapEnhance)
        bodyEquipItem.removeEquipEffectToAvatar(self)
        self.bodyEquipData.dressEquip(self, slotId, bagEquipItem)
        self.client.onDressEquipment(bagEquipItem.toClientBodyEquipItemDict(slotId))
        self.base.replaceEquipment(opUUID, gameconst.DressEquipOpStat.EQUIP_OP_REPLACED, bodyEquipItem.toItemSavedDict())

    def cellUndressEquipment(self, slotId):
        if self.isBodyEquipsLocked():
            WARNING_MSG('     in cellUndressEquipment, locked')
            self.base.cellUndressEquipmentFail(slotId, 'cellUndressEquipment, body equip locked')
            return

        if not self.checkConflictState(CCD.datas.changeGear, True):
            self.base.cellUndressEquipmentFail(slotId, 'cellUndressEquipment, state conflict')
            return

        bodyEquip = self.bodyEquipData.doBodyUndressEquip(self, slotId)
        if not bodyEquip:
            self.base.cellUndressEquipmentFail(slotId, 'cellUndressEquipment, data error')
            return

        self.base.cellUndressEquipmentSucc(bodyEquip.toItemSavedDict())

    @utils.isMyself
    def reqEquipEnhance(self, exposed, equipIn, equipPos, uniqueId, level, autoBuy):
        DEBUG_MSG('in reqEquipEnhance:', equipIn, equipPos, uniqueId, level, autoBuy)

        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipEnhance(equipPos, uniqueId, level, autoBuy, self.equipSetLv)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if not equipItem:
                WARNING_MSG('     in reqEquipEnhance, equipPos error:', equipPos)
                return
            if equipItem.uniqueId != uniqueId:
                WARNING_MSG('   in reqEquipEnhance, uniqueId not matched:', equipItem.uniqueId, uniqueId)
                return
            if dataUtils.checkEquipGrowingForbidden(equipItem):
                ERROR_MSG('   in reqEquipEnhance, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentEnhancementType(equipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('   in reqEquipEnhance, equipment can not enhance, equipment:', equipItem)
                return False

            if not equipItem.checkEnhancementValid(level):
                ERROR_MSG('   in reqEquipEnhance, equipment enhancement is invalid, equipment:', equipItem)
                return

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipEnhance'):
                WARNING_MSG('   in reqEquipEnhance, locked')
                return
            costItemDic = equipItem.enhanceNeedItems(level)
            if not costItemDic:
                ERROR_MSG('     in reqEquipEnhance, cost is empty:', level)
                return
            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_ENHANCE_BODY_EQUIP
            detail = gameclass.AwardDetail(itemId=equipItem.uniqueId)
            self.base.baseEquipDeductItems(costItemDic, opUUID, src, detail, self,
                                  'cellEquipEnhance', (opUUID, equipPos, level), autoBuy, True)
        return

    def cellEquipEnhance(self, opStat, opUUID, slotId, enhanceLv):
        DEBUG_MSG('in cellEquipEnhance:', opStat, slotId, enhanceLv)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            WARNING_MSG('in cellEquipEnhance, items not enouth')
            self.client.onEquipEnhanceFailed(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId)
            return
        self.enhanceSuccess(opUUID, slotId, enhanceLv)
            # isMaxVal and self.base.baseCheckAchievement(gameconst.AchieveTargetType.TARGET_ACTION,
            #                                             (gameconst.AchieveTargetActionId.EQUIP_ENHANCE_LEVEL_FULL, ))
            # self.base.makeEquipmentEnhanceLog(equipItem.itemId, equipItem.uniqueId, enhanceLv, oldEncVal, enhanceVal,
            #                                   equipItem.equipAttr.getEnhanceData()[1], success,self.equipSetLv)

            # NOTE()(ACHIEVE): 装备::强化或补缀次数
            # self.base.baseCheckAchievement(gameconst.AchieveTargetType.EQUIPMENT_ENHANCED, ())
            # NOTE()(ACHIEVE): 装备::装备首次达到强化等级
            # self.base.baseCheckAchievement(gameconst.AchieveTargetType.EQUIPMENT_ENHANCED_TOLVL, (enhanceLv, ))
    def enhanceSuccess(self, opUUID, slotId, enhanceLv, isGM = False):
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if equipItem and equipItem.checkEnhancementValid(enhanceLv, isGM):
            equipItem.doEnhanceEquip(self, opUUID, enhanceLv, onBody=True, isGM = isGM)
            self.client.onEquipEnhanceSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId,
                                           equipItem.getEnhanceLevel(), equipItem.getEnhanceLvVal())
            self.base.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            self.updateEquipmentScore()
            return True
        return False
    
    def unlockBodyEquips(self):
        self.bodyEquipData.doUnlockBodyEquips()

    def isBodyEquipsLocked(self):
        return self.bodyEquipData.isBodyEquipsBeLocked()

    @utils.isMyself
    def reqEquipSpiritWashing(self, exposed, equipIn, equipPos, uniqueId, spiritPos):
        DEBUG_MSG('in reqEquipSpiritWashing:', equipIn, equipPos, uniqueId, spiritPos)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipSpiritWashing(equipPos, uniqueId, spiritPos)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if equipItem.uniqueId != uniqueId:
                return

            if dataUtils.checkEquipGrowingForbidden(equipItem):
                ERROR_MSG('   in reqEquipSpiritWashing, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentSpiritType(equipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('   in reqEquipSpiritWashing, equipment can not affix, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipSpiritWashing'):
                WARNING_MSG('   in reqEquipSpiritWashing, locked')
                return
            
            if not equipItem.checkSpiritNum(spiritPos):
                ERROR_MSG('    in reqEquipSpiritWashing, slot is empty')
                return
            
            costItemDic = equipItem.spiritWashingNeedItems()
            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_EQUIP_AFFIX_WASHING
            detail = gameclass.AwardDetail(itemId=equipItem.uniqueId)
            self.base.baseEquipDeductItems(costItemDic, opUUID, src, detail, self,
                                  'cellEquipSpiritWashing', (opUUID, equipPos, uniqueId, spiritPos), False, True)
        return

    def cellEquipSpiritWashing(self, opStat, opUUID, slotId, uniqueId, spiritPos):
        DEBUG_MSG('in cellEquipSpiritWashing:', opStat, slotId, uniqueId)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            DEBUG_MSG('     in cellEquipSpiritWashing, cost items not enough')
            return
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if equipItem.uniqueId != uniqueId:
            return
        equipItem.removeEquipEffectToAvatar(self)
        ret, _, _ = equipItem.doEquipSpiritWashing(self, spiritPos)
        if ret:
            spiritData = equipItem.equipAttr.spiritDatas[spiritPos]
            self.client.onEquipSpiritWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, spiritData.toClientData())
        equipItem.applyEquipEffectToAvatar(self)

        self.updateEquipmentScore()
        return

    @utils.isMyself
    def reqEquipGlyphApply(self, exposed, equipIn, equipPos, groupId, uniqueId):
        DEBUG_MSG('in reqEquipGlyphApply:', equipIn, equipPos, groupId, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipGlyphApply(equipPos, uniqueId, groupId)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if equipItem.uniqueId != uniqueId:
                return

            if dataUtils.checkEquipGrowingForbidden(equipItem):
                ERROR_MSG('   in reqEquipGlyphApply, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentGlyphType(equipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('   in reqEquipGlyphApply, equipment can not glyph, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipGlyphApply'):
                WARNING_MSG('   in reqEquipGlyphApply, locked')
                return

            if not equipItem.checkGlyphApplyGroupId(groupId):
                ERROR_MSG('   in reqEquipGlyphApply groupId is wrong')
                return
            self.unlockBodyEquips()
            equipItem.removeEquipEffectToAvatar(self)
            ret = equipItem.doApplyGlyphGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, groupId)
            # 只要存在变动就更新
            if ret:
                self.bodyEquipData.recalculateAllInscriptionEffects(self)
            self.client.onEquipGlyphApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, groupId)
            equipItem.applyEquipEffectToAvatar(self)
            self.updateEquipmentScore()
        return
    
    @utils.isMyself
    def reqEquipSpiritApply(self, exposed, equipIn, equipPos, groupId, uniqueId):
        DEBUG_MSG('in reqEquipSpiritApply:', equipIn, equipPos, groupId, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipGlyphApply(equipPos, uniqueId, groupId)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if equipItem.uniqueId != uniqueId:
                return

            if dataUtils.checkEquipGrowingForbidden(equipItem):
                ERROR_MSG('   in reqEquipSpiritApply, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentSpiritType(equipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('   in reqEquipSpiritApply, equipment can not glyph, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipSpiritApply'):
                WARNING_MSG('   in reqEquipSpiritApply, locked')
                return

            if not equipItem.checkSpiritApplyGroupId(groupId):
                ERROR_MSG('   in reqEquipSpiritApply groupId is wrong')
                return
            self.unlockBodyEquips()
            equipItem.removeEquipEffectToAvatar(self)
            equipItem.doApplySpiritGroupId(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, groupId)
            self.client.onEquipSpiritApplySucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, groupId)
            equipItem.applyEquipEffectToAvatar(self)
            self.updateEquipmentScore()
        return

    @utils.isMyself
    def reqEquipGlyphWashing(self, exposed, equipIn, equipPos, glyphPos, uniqueId):
        DEBUG_MSG('in reqEquipGlyphWashing:', equipIn, equipPos, glyphPos, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipGlyphWashing(equipPos, uniqueId, glyphPos)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if equipItem.uniqueId != uniqueId:
                return

            if dataUtils.checkEquipGrowingForbidden(equipItem):
                ERROR_MSG('   in reqEquipGlyphWashing, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentGlyphType(equipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('   in reqEquipGlyphWashing, equipment can not glyph, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipGlyphWashing'):
                WARNING_MSG('   in reqEquipGlyphWashing, locked')
                return

            if not equipItem.checkGlyphNum(glyphPos):
                ERROR_MSG('in reqEquipGlyphWashing slot is empty')
                return

            costItemDic = equipItem.glyphWashingNeedItems()
            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_WEAPON_GLYPH_WASHING
            detail = gameclass.AwardDetail(itemId=equipItem.uniqueId)
            self.base.baseEquipDeductItems(costItemDic, opUUID, src, detail, self,
                                           'cellEquipGlyphWashing', (opUUID, equipPos, uniqueId, glyphPos), False, True)
        return

    def cellEquipGlyphWashing(self, opStat, opUUID, slotId, uniqueId, glyphPos):
        DEBUG_MSG('in cellEquipGlyphWashing:', opStat, slotId, uniqueId, glyphPos)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            DEBUG_MSG('     in cellEquipGlyphWashing, cost items not enough')
            return
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if equipItem.uniqueId != uniqueId:
            return
        equipItem.removeEquipEffectToAvatar(self)
        ret, _, _ = equipItem.doEquipGlyphWashing(self, glyphPos)
        if ret:
            glyphData = equipItem.equipAttr.glyphDatas[glyphPos]
            self.bodyEquipData.recalculateAllInscriptionEffects(self)
            self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, glyphPos, glyphData.toClientData())
        equipItem.applyEquipEffectToAvatar(self)
        self.updateEquipmentScore()

    @utils.isMyself
    def reqEquipBless(self, exposed, equipIn, equipPos, uniqueId):
        DEBUG_MSG('in reqEquipBless:', equipIn, equipPos, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipBless(equipPos, uniqueId)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if equipItem.uniqueId != uniqueId:
                return

            if dataUtils.checkEquipGrowingForbidden(equipItem):
                ERROR_MSG('   in reqEquipBless, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentBlessType(equipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('   in reqEquipBless, equipment can not bless, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipBless'):
                WARNING_MSG('   in reqEquipBless, locked')
                return

            costItemDic = equipItem.blessNeedItems()
            if not costItemDic:
                ERROR_MSG('     in reqEquipBless, cost is empty:')
                return
            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_EQUIP_BLESSING
            detail = gameclass.AwardDetail(itemId=equipItem.uniqueId)
            self.base.baseEquipDeductItems(costItemDic, opUUID, src, detail, self,
                                           'cellEquipBless', (opUUID, equipPos, uniqueId), False, True)
        return

    def cellEquipBless(self, opStat, opUUID, slotId, uniqueId):
        DEBUG_MSG('in cellEquipBless:', opStat, slotId, uniqueId)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            DEBUG_MSG('     in cellEquipBless, cost items not enough')
            return
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if equipItem.uniqueId != uniqueId:
            return
        equipItem.removeEquipEffectToAvatar(self)
        if equipItem.doEquipBlessing(self):
            blessAffixes = []
            for oneAffix in equipItem.equipAttr.blessAffixes:
                blessAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, blessAffixes,
                                        equipItem.equipAttr.maxBlessLv, equipItem.equipAttr.blessLvRate)

        equipItem.applyEquipEffectToAvatar(self)
        self.updateEquipmentScore()
        return

    @utils.isMyself
    def reqEquipBackBless(self, exposed, equipIn, equipPos, uniqueId):
        DEBUG_MSG('in reqEquipBackBless:', equipIn, equipPos, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipBackBless(equipPos, uniqueId)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if equipItem.uniqueId != uniqueId:
                return

            ret = dataUtils.checkEquipmentBlessType(equipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('     in reqEquipBackBless, not bless type')
                return

            if dataUtils.checkEquipGrowingForbidden(equipItem):
                ERROR_MSG('   in reqEquipBackBless, equipment can not be growing, equipment:', equipItem)
                return

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipBless'):
                WARNING_MSG('   in reqEquipBackBless, locked')
                return

            if not equipItem.isCanBackBless():
                ERROR_MSG('     in reqEquipBackBless, not can backBless')
                return

            self.unlockBodyEquips()
            equipItem.removeEquipEffectToAvatar(self)
            if equipItem.doEquipBackBless():
                blessAffixes = []
                for oneAffix in equipItem.equipAttr.blessAffixes:
                    blessAffixes.append(oneAffix.toAfxClientDic())
                self.client.onEquipBackBlessSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, blessAffixes,
                                                 equipItem.equipAttr.maxBlessLv,
                                                 equipItem.equipAttr.blessLvRate)

            equipItem.applyEquipEffectToAvatar(self)
            self.updateEquipmentScore()

        return

    @utils.isMyself
    def reqEquipSell(self, exposed, equipIn, equipPos, uniqueId):
        DEBUG_MSG('in reqEquipSell:', equipIn, equipPos, uniqueId)
        # if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
        #     self.base.bagEquipSell(equipPos, uniqueId)
        # elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            # equipItem = self.bodyEquipData.doSellBodyEquip(self, equipPos, uniqueId)
            # if equipItem is None:
            #     return
            # self.updateEquipmentScore()
            # self.client.onEquipSell(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, equipPos, uniqueId)
            # self.appearance.setEquip(self, equipPos, 0)
            # opUUID = KBEngine.genUUID64()
            # self.base.setAvatarVariable(VLVLD.AvatarDataVarPropDic['amountWearingGear'], len(self.bodyEquipData.equips_map),
            #                              opUUID, gameconst.VarChangeSrc.VAR_SRC_BODY_EQUIP_SELL, '')
            # self.base.makeEquipmentLostLog(AAC_AACDD.datas.BONUS_SRC_EQUIP_SELL, equipItem)
        return

    def getBodyEquipExtraSkillLv(self, skillId):
        return self.bodyEquipData.getEquipsAddSkillLv(self, skillId)

    def getInscriptionEffects(self, skillID, effectType):
        return self.bodyEquipData.getInscriptionEffects(skillID, effectType)

    def addPropByGear(self, target, context, propList, startIdx=0, endIdx=-1):
        if context.actionType == actionContext.ACTION_EQUIP:
            context.affixItem.addPropByEquip(self, propList, context.affixVals, startIdx=startIdx, endIdx=endIdx)
        elif context.actionType == actionContext.ACTION_EQUIP_SET:
            context.bodyEquips.addPropBySet(self, propList, context.vals, startIdx=startIdx, endIdx=endIdx)
        return

    def addSingleSkLvByGear(self, target, context, skillId, valIdx=0):
        if context.actionType == actionContext.ACTION_EQUIP:
            context.affixItem.addSingleSkLvByEquip(self, skillId, context.affixVals, context.isLogin, valIdx=valIdx)
        return

    def addClassSkLvByGear(self, target, context, schoolList, valIdx=0):
        for school in schoolList:
            if self.school != school:
                continue
            if context.actionType == actionContext.ACTION_EQUIP:
                context.affixItem.addClassSkLvByEquip(self, context.affixVals, school, valIdx, context.isLogin)
        return

    def onBodyEquipLoseSoulRecovery(self, equipUniqueIdList):
        DEBUG_MSG('in onBodyEquipLoseSoulRecovery:', equipUniqueIdList)
        gridIdList = []
        equipDataList = []
        for uniqueId in equipUniqueIdList:
            slotId, equipItem = self.bodyEquipData.getBodyEquipByUniqueId(uniqueId)
            if not equipItem:
                WARNING_MSG('       in onBodyEquipLoseSoulRecovery, no lose soul equip:', slotId, uniqueId)
                continue

            if equipItem.loseSoulHasFixed():
                WARNING_MSG('       in onBodyEquipLoseSoulRecovery, equip already return to normal:', slotId, equipItem.itemId)
                continue

            equipItem.fixLoseSoul()
            equipItem.applyEquipEffectToAvatar(self)
            gridIdList.append(slotId)
            equipDataList.append(equipItem.toClientEquipItemDict())

        if gridIdList:
            self.updateEquipmentScore()
            self.client.onEquipFixLoseSoulSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, gridIdList, equipDataList)

        return

    def sendItemLinkInfoCell(self, box, uniqueId, itemId):
        if dataUtils.isEquipItemByItemId(itemId):
            for slotId, item in self.bodyEquipData.equips_map.items():
                if item.itemId == itemId and item.uniqueId == uniqueId:
                    box.client.onQueryItemLink(uniqueId, item.toItemSavedDict())
                    return
        box.onMessagePre(MMD.datas.channel_noItem, [])

    def getAllEnhanceLv(self):
        return self.bodyEquipData.calcAllEnhanceLvRate()

    ################################## Gm cmd ###################################

    def gmDressEquips(self):
        dressSlotIds = []
        for slotId in range(1, 10):
            it = self.bodyEquipData.getEquipItem(slotId)
            if not it:
                dressSlotIds.append(slotId)
                continue
        
        if len(dressSlotIds) == 0:
            return False
        self.base.gmBaseDressEquips(dressSlotIds)
        return True

    def gmModifyEquipEnhanceLevel(self, slotID, enhanceLevel):
        INFO_MSG('in modifyEquipEnhanceLevel, slotId:', slotID, enhanceLevel)
        return self.enhanceSuccess(0, slotID, enhanceLevel, True)
    ################################## gm cmd end ###################################

    ################################### drop equip start ##############################
    def takeEquip(self, uniqueId):
        INFO_MSG('in takeEquip, uniqueId:', uniqueId)
        self.base.takeEquipBase(uniqueId)

    def _dealDeathDrop(self, killerGbId, killerName):
        if not (self._isCritInjured() or (self.moralValue <= GB_GCD.datas['equipDropMoralBound']['value'])):
            return

        _moral = min(GB_GCD.datas['equipDropMoralBound']['value'], self.moralValue)
        _formulaId = GB_GCD.datas['equipDropProbFormulaID']['value']
        _formulaFunc = F_GFD.datas[_formulaId]['serverFormula']

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
        INFO_MSG('will drop equip:', _slotId)
        self.dropEquip(_slotId, killerGbId, killerName)

    def dropEquip(self, slotId, killerGbId=0, killerName=''):
        INFO_MSG('in dropEquip, slotId:', slotId)
        bodyEquip = self.bodyEquipData.doBodyUndressEquip(self, slotId)
        if not bodyEquip:
            ERROR_MSG('in dropEquip, no equip in slotId:', slotId)
            return

        self.dropEquipByItem(bodyEquip, killerName)

    def dropEquipByItem(self, bodyEquip, killerName):
        _equipInfo = bodyEquip.toItemSavedDict()

        _formulaId = GB_GCD.datas['equipRepairCostAmount']['value']
        _formulaFunc = F_GFD.datas[_formulaId]['serverFormula']
        _dropCtx = actionContext.DropEquipCtx(
            bodyEquip.getEquipScore(),
            bodyEquip.equipAttr.quality,
            bodyEquip.grade()
        )
        _price = int(_formulaFunc(_dropCtx))

        _uuid = KBEngine.genUUID64()

        _now = utils.getNow()
        _collEndTime = _now + GB_GCD.datas['equipDropPickLiveTime']['value']
        _endTime = _now + GB_GCD.datas['equipDamageDestructionTime']['value']

        _extraBlob = {
            'n': killerName, # 名字
            'm': self.spaceNo,
            'p': (self.position[0], self.position[1], self.position[2])
        }
        _extraBlob = cPickle.dumps(_extraBlob)

        _collectionId = QD_QDD.datas[bodyEquip.quality]['equipDropPickID']

        _props = {
            'collectionId': _collectionId,
            'spaceNo': self.spaceNo,
            'position': self.position,
            'direction': self.direction,
            'spaceMgrId': self.spaceMgrId,
            'disappearTime': _collEndTime,
            'dropEquipId': _uuid,
            'dropEquipItemId': bodyEquip.itemId,
        }

        _ent = KBEngine.createEntity('Collection', self.spaceID, self.position, self.direction, _props)
        self.base.onDropEquipBase(_uuid, _price, self.spaceNo, self.position, _equipInfo, _collEndTime, killerName, _endTime, _extraBlob, _ent.id)

        _mailId = GB_GCD.datas['equipDamageMailID']['value']
        _args = [
            bodyEquip.itemId,
            bodyEquip.uniqueId,
            int(self.position[0]),
            int(self.position[2]),
            self.spaceNo,
        ]

        mailAssistor.sendMailToPlayers(
            [self.gbId],
            _mailId,
            opUUID=KBEngine.genUUID64(),
            despArgs=_args
        )

    ################################### drop equip end ##############################

    def getInscriptionEffects(self, skillID, effectType):
        return self.glyphEquipData.getInscriptionEffects(skillID, effectType)

