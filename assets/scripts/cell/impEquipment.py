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
        oldBodyEquipDic = bodyEquipItem.toItemSavedDict()
        self.base.replaceEquipment(opUUID, gameconst.DressEquipOpStat.EQUIP_OP_REPLACED,
                                   oldBodyEquipDic)

        if 'attrJson' in oldBodyEquipDic:
            attrJson = oldBodyEquipDic['attrJson']
            attrDict = json.loads(attrJson)
            enhanceLv = attrDict.get('enhanceLv', 0)

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
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if equipItem:
            equipItem.doEnhanceEquip(self, opUUID, enhanceLv, onBody=True)
            self.client.onEquipEnhanceSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId,
                                           equipItem.getEnhanceLevel(), equipItem.getEnhanceLvVal())
            self.base.triggerAchievement(gameconst.AchieveType.ENHANCE_EQUIPMENT)
            self.updateEquipmentScore()

            # isMaxVal and self.base.baseCheckAchievement(gameconst.AchieveTargetType.TARGET_ACTION,
            #                                             (gameconst.AchieveTargetActionId.EQUIP_ENHANCE_LEVEL_FULL, ))
            # self.base.makeEquipmentEnhanceLog(equipItem.itemId, equipItem.uniqueId, enhanceLv, oldEncVal, enhanceVal,
            #                                   equipItem.equipAttr.getEnhanceData()[1], success,self.equipSetLv)

            # NOTE()(ACHIEVE): 装备::强化或补缀次数
            # self.base.baseCheckAchievement(gameconst.AchieveTargetType.EQUIPMENT_ENHANCED, ())
            # NOTE()(ACHIEVE): 装备::装备首次达到强化等级
            # self.base.baseCheckAchievement(gameconst.AchieveTargetType.EQUIPMENT_ENHANCED_TOLVL, (enhanceLv, ))

    def unlockBodyEquips(self):
        self.bodyEquipData.doUnlockBodyEquips()

    def isBodyEquipsLocked(self):
        return self.bodyEquipData.isBodyEquipsBeLocked()

    @utils.isMyself
    def reqEquipAffixWashing(self, exposed, equipIn, equipPos, uniqueId):
        DEBUG_MSG('in reqEquipAffixWashing:', equipIn, equipPos, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipAffixWashing(equipPos, uniqueId)
        elif equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY:
            equipItem = self.bodyEquipData.getEquipItem(equipPos)
            if equipItem.uniqueId != uniqueId:
                return

            if dataUtils.checkEquipGrowingForbidden(equipItem):
                ERROR_MSG('   in reqEquipAffixWashing, equipment can not be growing, equipment:', equipItem)
                return

            ret = dataUtils.checkEquipmentSpiritType(equipItem.equipAttr.equipType)
            if not ret:
                ERROR_MSG('   in reqEquipAffixWashing, equipment can not affix, equipment:', equipItem)
                return False

            if not self.bodyEquipData.tryLockBodyEquips(desp='reqEquipAffixWashing'):
                WARNING_MSG('   in reqEquipAffixWashing, locked')
                return
            costItemDic = equipItem.affixWashingNeedItems()
            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_EQUIP_AFFIX_WASHING
            detail = gameclass.AwardDetail(itemId=equipItem.uniqueId)
            self.base.baseEquipDeductItems(costItemDic, opUUID, src, detail, self,
                                  'cellEquipAffixWashing', (opUUID, equipPos, uniqueId), False, True)
        return

    def cellEquipAffixWashing(self, opStat, opUUID, slotId, uniqueId):
        DEBUG_MSG('in cellEquipAffixWashing:', opStat, slotId, uniqueId)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            DEBUG_MSG('     in cellEquipAffixWashing, cost items not enough')
            return
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if equipItem.uniqueId != uniqueId:
            return
        equipItem.removeEquipEffectToAvatar(self)
        ret, oldRandomAffixes = equipItem.doEquipAffixWashing(self, self.name, self.gbId, True)
        if ret:
            randomAffixes = []
            for oneAffix in equipItem.equipAttr.randomAffixes:
                randomAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipAffixWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, randomAffixes)
            # self.base.baseCheckAchievement(gameconst.AchieveTargetType.EQUIP_AFFIX_WASHING, ())
        equipItem.applyEquipEffectToAvatar(self)

        self.updateEquipmentScore()
        return

    @utils.isMyself
    def reqEquipGlyphWashing(self, exposed, equipIn, equipPos, uniqueId):
        DEBUG_MSG('in reqEquipGlyphWashing:', equipIn, equipPos, uniqueId)
        if equipIn == gameconst.EquipAttrConst.EQUIP_BELONGTO_BAG:
            self.base.bagEquipGlyphWashing(equipPos, uniqueId)
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

            if not equipItem.checkSlotNum():
                ERROR_MSG('in reqEquipGlyphWashing slot is empty')
                return

            costItemDic = equipItem.glyphWashingNeedItems()
            opUUID = KBEngine.genUUID64()
            src = AAC_AACDD.datas.BONUS_SRC_WEAPON_GLYPH_WASHING
            detail = gameclass.AwardDetail(itemId=equipItem.uniqueId)
            self.base.baseEquipDeductItems(costItemDic, opUUID, src, detail, self,
                                           'cellEquipGlyphWashing', (opUUID, equipPos, uniqueId), False, True)
        return

    def cellEquipGlyphWashing(self, opStat, opUUID, slotId, uniqueId):
        DEBUG_MSG('in cellEquipGlyphWashing:', opStat, slotId, uniqueId)
        self.unlockBodyEquips()
        if opStat != gameconst.BagOPStat.BAG_OP_STAT_OK:
            DEBUG_MSG('     in cellEquipGlyphWashing, cost items not enough')
            return
        equipItem = self.bodyEquipData.getEquipItem(slotId)
        if equipItem.uniqueId != uniqueId:
            return
        equipItem.removeEquipEffectToAvatar(self)
        ret, oldGlyphAffixes = equipItem.doEquipGlyphWashing(self)
        if ret:
            glyphAffixes = []
            for oneAffix in equipItem.equipAttr.glyphAffixes:
                glyphAffixes.append(oneAffix.toAfxClientDic())
            self.client.onEquipGlyphWashingSucc(gameconst.EquipAttrConst.EQUIP_BELONGTO_BODY, slotId, glyphAffixes)

        equipItem.applyEquipEffectToAvatar(self)

        self.updateEquipmentScore()
        self.bodyEquipData.recalculateAllInscriptionEffects(self, oldGlyphAffixes, equipItem.equipAttr.glyphAffixes)
        return

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
        return self.bodyEquipData.getEquipsAddSkillLv(skillId)

    def getSkillInciptionEffect(self, skillID, effectType):
        return self.bodyEquipData.getSkillInciptionEffect(skillID, effectType)

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

    def gmEquipEnhanceToMaxLv(self):
        enhanceMaxLvs = 5
        if len(self.bodyEquipData.equips_map) == 0:
            return
        self.bodyEquipData.removeBodyEquipsProps(self)
        clientData = []
        for slotId, equipObj in self.bodyEquipData.equips_map.items():
            equipObj.equipAttr.enhanceLv = enhanceMaxLvs
            equipObj.equipAttr.calcScore()
            clientData.append(equipObj.toClientBodyEquipItemDict(slotId))
        self.bodyEquipData.applyBodyEquipsProps(self)
        self.updateEquipmentScore()
        self.sendBodyEquipData()
        return

    def gmEquipEnhanceToLevel(self, level, full):
        pass
        # import random
        # if len(self.bodyEquipData.equips_map) == 0:
        #     return

        # self.bodyEquipData.removeBodyEquipsProps(self)
        # if level <= 0 or level > max(GEGUD.datas.keys()):
        #     return False
        # clientData = []
        # for slotId, equipObj in self.bodyEquipData.equips_map.items():
        #     equipObj.equipAttr.enhanceLv = 5
        #     equipObj.equipAttr.calcScore()
        #     clientData.append(equipObj.toClientBodyEquipItemDict(slotId))
        # self.bodyEquipData.applyBodyEquipsProps(self)
        # self.updateEquipmentScore()
        # self.sendBodyEquipData()
        # return True

    def gmEquipFullBaseAttr(self):
        # gm指令不考虑对avatar身上的属性影响，重新登陆即可更新
        clientData = []
        if len(self.bodyEquipData.equips_map) == 0:
            return
        self.bodyEquipData.removeBodyEquipsProps(self)
        for slotId, equipObj in self.bodyEquipData.equips_map.items():
            equipObj.equipAttr.calcBaseAttrs()
            clientData.append(equipObj.toClientBodyEquipItemDict(slotId))
            equipObj.equipAttr.calcScore()
        self.bodyEquipData.applyBodyEquipsProps(self)
        self.updateEquipmentScore()
        self.sendBodyEquipData()
        return

    def gmEquipSetAffixNum(self, affixNum):
        clientData = []
        if len(self.bodyEquipData.equips_map) == 0:
            return
        self.bodyEquipData.removeBodyEquipsProps(self)
        for slotId, equipObj in self.bodyEquipData.equips_map.items():
            equipObj.equipAttr.gmSetAffixesNum(affixNum)
            equipObj.onEquipAffixChanged()
            clientData.append(equipObj.toClientBodyEquipItemDict(slotId))
            equipObj.equipAttr.calcScore()
        self.bodyEquipData.applyBodyEquipsProps(self)
        self.updateEquipmentScore()
        self.sendBodyEquipData()
        return

    def gmEquipAddOneAffix(self, affixId):
        clientData = []
        if len(self.bodyEquipData.equips_map) == 0:
            return False
        if affixId not in AFAFTWD.datas:
            DEBUG_MSG('in gmEquipAddOneAffix, equip no this affix:', affixId)
            return False

        self.bodyEquipData.removeBodyEquipsProps(self)
        for slotId, equipObj in self.bodyEquipData.equips_map.items():
            equipObj.equipAttr.gmAddOneAffix(affixId)
            equipObj.onEquipAffixChanged()
            clientData.append(equipObj.toClientBodyEquipItemDict(slotId))
            equipObj.equipAttr.calcScore()
        self.bodyEquipData.applyBodyEquipsProps(self)
        self.updateEquipmentScore()
        self.sendBodyEquipData()
        return True

    def gmEquipReplaceOneAffix(self, affixId):
        clientData = []
        if len(self.bodyEquipData.equips_map) == 0:
            return False
        if affixId not in AFAFTWD.datas:
            DEBUG_MSG('in gmEquipReplaceOneAffix, equip no this affix:', affixId)
            return False

        self.bodyEquipData.removeBodyEquipsProps(self)
        for slotId, equipObj in self.bodyEquipData.equips_map.items():
            equipObj.equipAttr.gmReplaceOneAffix(affixId)
            equipObj.onEquipAffixChanged()
            clientData.append(equipObj.toClientBodyEquipItemDict(slotId))
            equipObj.equipAttr.calcScore()
        self.bodyEquipData.applyBodyEquipsProps(self)
        self.updateEquipmentScore()
        self.sendBodyEquipData()
        return True

    def gmEquipOnlyOneAffix(self, affixId):
        clientData = []
        if len(self.bodyEquipData.equips_map) == 0:
            return False
        if affixId not in AFAFTWD.datas:
            DEBUG_MSG('in gmEquipOnlyOneAffix, equip no this affix:', affixId)
            return False

        self.bodyEquipData.removeBodyEquipsProps(self)
        for slotId, equipObj in self.bodyEquipData.equips_map.items():
            equipObj.equipAttr.gmOnlyOneAffix(affixId)
            equipObj.onEquipAffixChanged()
            clientData.append(equipObj.toClientBodyEquipItemDict(slotId))
            equipObj.equipAttr.calcScore()
        self.bodyEquipData.applyBodyEquipsProps(self)
        self.updateEquipmentScore()
        self.sendBodyEquipData()
        return True

    def gmDressEquipsByQuality(self, quality, enhanceLv):
        dressSlotIds = []
        for slotId in range(1, 10):
            it = self.bodyEquipData.getEquipItem(slotId)
            if not it:
                dressSlotIds.append(slotId)
                continue
            if it.quality != quality or it.equipAttr.getEnhanceLv() != enhanceLv:
                dressSlotIds.append(slotId)
                continue
        self.base.gmBaseDressEquipsByQuality(quality, enhanceLv, dressSlotIds)

    def gmDressEquips(self):
        dressSlotIds = []
        for slotId in range(1, 10):
            it = self.bodyEquipData.getEquipItem(slotId)
            if not it:
                dressSlotIds.append(slotId)
                continue

        self.base.gmBaseDressEquips(dressSlotIds)

    def gmPrintBodyEquipsEnhanceInfo(self):
        DEBUG_MSG('gmPrintBodyEquipsEnhanceInfo')
        import gearEnhance_setEffect as GESED
        for equipObj in self.bodyEquipData.equips_map.values():
            DEBUG_MSG('#################################################')
            gearData = dataUtils.getEquipItemData(equipObj.itemId)
            itemId = equipObj.itemId
            DEBUG_MSG(itemId, gearData['name'], 'enhanceInfo:', equipObj.equipAttr.enhanceLv)
            enhanceLv = equipObj.equipAttr.getEnhanceLv()
            DEBUG_MSG('     强化数据:', equipObj.equipAttr.enhanceLv)
            DEBUG_MSG('     强化等级:', enhanceLv)
            for setLv, oneData in GESED.datas.items():
                if enhanceLv >= oneData['gearGrade']:
                    DEBUG_MSG('     check setLv:', oneData['gearGrade'])
        return

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
        return self.bodyEquipData.getInscriptionEffects(skillID, effectType)
