# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import random
import json
import math
import copy
import itertools
import userType
import BaseItem
import gameengine
import dataUtils
import gameconst
import utils
import actionContext
import dropAward
import AffixInfo
import GlyphInfo
import SpiritInfo

import drop_gearQualityWeight as DGQWD
import gearBase_gearBase as GBGBD
import affix_affix as AFAFD
import affix_randomAffixCountWeight as AFRAFCWD
import affix_affixTypeWeight as AFAFTWD
import affix_glyphTypeWeight as GLYPHTWD
import gearEnhance_gearStrengthen as GEGS
import gearEnhance_fakeLuck as GEFLD
import gearEnhance_gearconst as GEGCD
import gearBase_gearConst as GBGCD
import gearBase_typeExplanation as GBTED
import gearEnhance_weaponGlyph as GEWGD
import gearEnhance_gearBless as GEBLD
import gearEnhance_equipmentFuLing as GEEFL
import prop_fightprop as PFPD
import rewardData_rewardData as RDDT
import gearEnhance_equipmentClass as GEES
import gearEnhance_equipmentAttributes as GEEA

class EquipmentItem(BaseItem.BaseItem):
    def __init__(self, itemId, itemNum=1, bindType=dataUtils.getItemDefaultBindType(),  **kwargs):
        super().__init__(itemId, 1, bindType=bindType)
        if itemId == gameconst.ItemId.COMMON_EQUIPMENT_ID:
            gameengine.reportCritical('EquipmentItem.__init__, comm itemId found')
            return
        self.itemType = gameconst.ItemType.Normal
        self.itemSubType = gameconst.ItemSubType.Equipment
        self.equipAttr = EquipAttr()
        self.uniqueId = 0
        gearBaseData = dataUtils.getEquipItemData(self.itemId)
        self.quality = gearBaseData['quality']
        return

    def _lateReload(self):
        super(EquipmentItem, self)._lateReload()
        self.equipAttr.reloadScript()

    def isEquipmentItem(self):
        return True

    def canMerge(self, withIt, **kwargs):
        # 对于装备, 永远不能merge到一起
        return False

    def onItemDailyUpdate(self):
        return

    def initNewItemAttr(self, **kwargs):
        #创建新装备时候的初始化
        self.uniqueId = KBEngine.genUUID64()
        self.initEquipFromGearbaseData()

        grade = kwargs.get('grade', 0)
        if 0 < grade <= GEGCD.datas['equipmentClassLevel']['value']:
            self.equipAttr.grade = grade

        # 绑定的装备才有绑定值
        if self.bindType == gameconst.ItemBindType.BIND:
            datas = GEGCD.datas['gearBlessBoundValue']['value']
            if datas:
                for data in datas:
                    grade, bindValue = data
                    if self.getGrade() == grade:
                        self.setBindValue(bindValue)
                        break

        self.equipAttr.calcBaseAttrs()
        self.equipAttr.calcScore()
        self.onEquipAffixChanged()
        return True

    def initEquipFromGearbaseData(self):
        #以 gearbase 表的数据 创建新装备
        gearBaseData = dataUtils.getEquipItemData(self.itemId)
        self.quality = gearBaseData['quality']
        self.equipAttr.initAttrFromTemplate(self.itemId, gearBaseData)
        return True

    def onSpecificItemChanged(self, savedJson):
        gearBaseData = dataUtils.getEquipItemData(self.itemId)
        self.quality = gearBaseData['quality']
        self.equipAttr = EquipAttr()
        savedDict = self.equipAttr.fromJson(savedJson)
        if savedDict:
            self.auctionTime = savedDict.get("auctionTime", 0)
        return

    def setDropFixEndTime(self, t):
        self.equipAttr.dropFixEndTime = t

    def setAuctionTime(self, t, now=None):
        super().setAuctionTime(t, now=now)
        self.equipAttr.setDirtyFlag()

    def attr2Json(self):
        extra = {}
        if self.auctionTime > 0:
            extra["auctionTime"] = self.auctionTime
        return self.equipAttr.toJson(extraAttrs=extra)

    def attr2Dict(self):
        extra = {}
        if self.auctionTime > 0:
            extra["auctionTime"] = self.auctionTime
        return self.equipAttr.toDict(extraAttrs=extra)

    def toClientBodyEquipItemDict(self, slotId):
        return {
            'itemId' : self.itemId,
            'itemNum' : self.itemNum,
            'createTime' : self.createTime,
            'expireTime' : self.expireTime,
            'slotId': slotId,
            'uniqueId': self.uniqueId,
            'bindType': self.bindType,
            'lockStatus' : self.lockStatus,
            'attrJson': self.attr2Json(),
        }

    def toClientEquipItemDict(self):
        cliDic = {
            'itemId': self.itemId,
            'createTime': self.createTime,
            'expireTime': self.expireTime,
            'uniqueId': self.uniqueId,
            'bindType': self.bindType,
            'auctionTime': self.auctionTime,
            'lockStatus' : self.lockStatus,
        }
        cliDic.update(self.equipAttr.toClientDic())
        return cliDic

    def getItemName(self):
        return dataUtils.getEquipItemData(self.itemId)['name']

    def getQuality(self):
        return self.quality

    def isPreciousEquip(self, washing=False):
        #绝品装备
        if self.quality == gameconst.ItemQuality.RED:
            #红装必定是绝品
            return True
        return False

    def enhanceNeedItems(self):
        itemsDic = {}
        currencyDic = {}
        # 强化一律优先使用绑定材料，如果是非绑定装备，在扣除材料或金钱成功后，再将装备绑定；
        nextKey = self.equipAttr.getEnhanceLevelKey(self.equipAttr.getEnhanceLv() + 1)
        nextCfgData = GEGS.datas.get(nextKey)
        if not nextCfgData:
            ERROR_MSG('in enhanceNeedItems, equipment is enhanced to max level:', nextKey)
            return None, None

        curKey = self.equipAttr.getEnhanceLevelKey(self.equipAttr.getEnhanceLv())
        curCfgData = GEGS.datas.get(curKey)
        if not curCfgData:
            ERROR_MSG('in enhanceNeedItems, missing enhancement cfg data:', curKey)
            return None, None
        # 道具消耗
        enhanceItem = curCfgData.get('costItem')
        for val in enhanceItem:
            costItemId, itemNum = val
            itemsDic[costItemId] = itemsDic.get(costItemId, 0) + itemNum
        # 货币消耗
        enhanceGoldCost = curCfgData.get('costCurrency')
        for val in enhanceGoldCost:
            costItemId, itemNum = val
            currencyDic[costItemId] = currencyDic.get(costItemId, 0) + itemNum

        return itemsDic, currencyDic

    def checkEnhancementValid(self, enhanceLevel, isGM = False):
        # 检查下个强化等级是否有效
        nextKey = self.equipAttr.getEnhanceLevelKey(enhanceLevel)
        if not GEGS.datas.get(nextKey):
            return False
        return True

    def checkUpgradeValid(self):
        # 检查下个升阶是否有效
        nextGrade = self.getGrade() + 1
        if nextGrade > GEGCD.datas['equipmentClassLevel']['value']:
            return False
        nextGradeKey = self.equipAttr.getUpgradeKey(nextGrade)
        if not GEES.datas.get(nextGradeKey):
            return False
        return True

    def upgradeNeedItems(self):
        itemsDic = {}
        nextKey = self.equipAttr.getUpgradeKey(self.getGrade() + 1)
        nextCfgData = GEES.datas.get(nextKey)
        if not nextCfgData:
            ERROR_MSG('in upgradeNeedItems, equipment is upgrade to max:', nextKey)
            return
        curKey = self.equipAttr.getUpgradeKey(self.getGrade())
        curCfgData = GEES.datas.get(curKey)
        if not curCfgData:
            ERROR_MSG('in upgradeNeedItems, missing upgrade cfg data:', curKey)
            return

        enhanceGoldCost = curCfgData.get('costCurrency')
        for val in enhanceGoldCost:
            costItemId, itemNum = val
            itemsDic[costItemId] = itemsDic.get(costItemId, 0) + itemNum
        return itemsDic

    def spiritWashingNeedItems(self):
        cfgData = GEEFL.datas.get(self.quality)
        if not cfgData:
            ERROR_MSG('in spiritWashingNeedItems, cfgData not found', self.quality)
            return None, None

        itemsDic = {}
        currencyDic = {}
        consumedItem = cfgData.get('consumedItem')
        if consumedItem:
            for val in consumedItem:
                costItemId, itemNum = val
                itemsDic[costItemId] = itemsDic.get(costItemId, 0) + itemNum

        consumedCoin = cfgData.get('consumedCoin')
        if consumedCoin:
            for val in consumedCoin:
                costItemId, itemNum = val
                currencyDic[costItemId] = currencyDic.get(costItemId, 0) + itemNum

        return itemsDic, currencyDic

    def glyphWashingNeedItems(self):
        key = self.quality * 10 + self.getGrade()
        cfgData = GEWGD.datas.get(key)
        if not cfgData:
            ERROR_MSG('   in glyphWashingNeedItems, cfgData not found:', key)
            return None, None

        itemsDic = {}
        currencyDic = {}

        glyphCraftItem = cfgData.get('glyphCraftItem')
        for val in glyphCraftItem:
            costItemId, itemNum = val
            itemsDic[costItemId] = itemsDic.get(costItemId, 0) + itemNum

        glyphCraftGoldCost = cfgData.get('glyphCraftGoldCost')
        for val in glyphCraftGoldCost:
            costItemId, itemNum = val
            currencyDic[costItemId] = currencyDic.get(costItemId, 0) + itemNum

        return itemsDic, currencyDic

    def bindValueWashingNeedItems(self, washCount):
        # 计算实际消耗，也不能多扣
        bindValue = self.getBindValue()
        if washCount >= bindValue:
            washCount = bindValue
        gearBaseData = dataUtils.getEquipItemData(self.itemId)
        itemsDic = {}
        consumedCoin = gearBaseData.get('washConsumeMoney')
        if consumedCoin:
            for val in consumedCoin:
                costItemId, itemNum = val
                itemsDic[costItemId] = itemsDic.get(costItemId, 0) + itemNum * washCount
        consumedItem = gearBaseData.get('washConsumeItem')
        if consumedItem:
            for val in consumedItem:
                costItemId, itemNum = val
                itemsDic[costItemId] = itemsDic.get(costItemId, 0) + itemNum * washCount
        return itemsDic

    def getBlessCfgData(self, addVal):
        if len(self.equipAttr.blessAffixes) == 0:
            key = self.equipAttr.equipType * 10 + addVal
        else:
            key = self.equipAttr.equipType * 10 + self.equipAttr.blessAffixes[0].affixVal + addVal
        return GEBLD.datas.get(key)

    def blessNeedItems(self):
        cfgData = self.getBlessCfgData(1)
        if not cfgData:
            ERROR_MSG('   in blessNeedItems, bless is up to max lucky value:')
            return None, None

        cfgData = self.getBlessCfgData(0)
        if not cfgData:
            ERROR_MSG('   in blessNeedItems, cfgData not found:')
            return None, None

        itemsDic = {}
        currencyDic = {}

        gearBlessItem = cfgData.get('gearBlessItem')
        for val in gearBlessItem:
            costItemId, itemNum = val
            itemsDic[costItemId] = itemsDic.get(costItemId, 0) + itemNum

        gearBlessGoldCost = cfgData.get('gearBlessGoldCost')
        for val in gearBlessGoldCost:
            costItemId, itemNum = val
            currencyDic[costItemId] = currencyDic.get(costItemId, 0) + itemNum

        return itemsDic, currencyDic

    def isCanBackBless(self):
        if len(self.equipAttr.blessAffixes) == 0:
            ERROR_MSG('isCanBackBless no blessAffix')
            return False

        curBlessVal = self.equipAttr.blessAffixes[0].affixVal
        key = self.equipAttr.equipType * 10 + self.equipAttr.maxBlessLv
        cfgData = GEBLD.datas.get(key)
        if not cfgData:
            ERROR_MSG('   in isCanBackBless, cfgData not found:', key)
            return False

        backtrack = cfgData.get('backtrack')
        if not backtrack:
            ERROR_MSG('isCanBackBless not config backtrack', key)
            return False

        if self.equipAttr.maxBlessLv <= curBlessVal:
            ERROR_MSG('isCanBackBless maxBlessLv <= curBlessVal', self.equipAttr.maxBlessLv, curBlessVal)
            return False

        if self.equipAttr.blessLvRate < backtrack:
            ERROR_MSG('isCanBackBless blessLvRate < backtrack', self.equipAttr.blessLvRate, backtrack)
            return False

        return True

    def returnWealthyByDisassemble(self, owner):
        gearBaseData = GBGBD.datas[self.itemId]
        if not gearBaseData:
            ERROR_MSG('returnWealthyByDisassemble missing gear base config', self.itemId)
            return

        dissassemblyReward = None
        if self.bindType == gameconst.ItemBindType.BIND:
            dissassemblyReward = gearBaseData['disassemblyReward']
            if dissassemblyReward is None:
                WARNING_MSG('returnWealthyByDisassemble missing dissassemle reward id config', self.itemId)
                return
        elif self.bindType == gameconst.ItemBindType.NORMAL:
            dissassemblyReward = gearBaseData['disassemblyReward2']
            if dissassemblyReward is None:
                WARNING_MSG('returnWealthyByDisassemble missing dissassemle reward2 id config', self.itemId)
                return

        if not dissassemblyReward:
            WARNING_MSG('returnWealthyByDisassemble unknow bind type', self.itemId, self.bindType)
            return

        awardCtx = owner._getAvatarAwardCtx(dissassemblyReward, None)
        awardVal = dropAward.getAwardOne(dissassemblyReward, awardCtx)

        # 额外产出，非必选配置
        dissassemblyExtraItem = gearBaseData['disassemblyExtraItem']
        if dissassemblyExtraItem and type(dissassemblyExtraItem) is tuple and len(dissassemblyExtraItem) > 0:
            # 适配disassemblyExtraItem形式为((a1,b1,c1),(a2,b2,c2))
            grade = self.getGrade()
            if type(dissassemblyExtraItem[0]) is tuple:
                for rewardData in dissassemblyExtraItem:
                    if not rewardData or len(rewardData) != 3:
                        ERROR_MSG('returnWealthyByDisassemble missing reward data config', rewardData)
                        break
                    if grade != rewardData[0]:
                        continue
                    coreItemID = rewardData[1]
                    coreItemCount = rewardData[2]
                    self.calculateDisassemblyReward(coreItemID, coreItemCount, awardVal)
                    break
            else:
                # 适配disassemblyExtraItem形式为(a1,b1,c1)
                if grade == dissassemblyExtraItem[0]:
                    coreItemID = dissassemblyExtraItem[1]
                    coreItemCount = dissassemblyExtraItem[2]
                    self.calculateDisassemblyReward(coreItemID, coreItemCount, awardVal)

        DEBUG_MSG('in returnWealthyByDisassemble, items info:', awardVal)
        return awardVal

    def calculateDisassemblyReward(self, coreItemID, coreItemCount, awardVal):
        if not dataUtils.getCommItemData(coreItemID):
            ERROR_MSG('returnWealthyByDisassemble-->calculateDisassemblyReward: missing item data config', coreItemID)
            return
        # 绑定核心数量
        bindCount = self.getOriginalBindValue()
        # 非绑定核心数量
        normalCount = 0
        if coreItemCount > bindCount:
            normalCount = coreItemCount - bindCount
        if bindCount > 0:
            awardVal.addWealthByItemId(coreItemID, bindCount, gameconst.ItemBindType.BIND)
        if normalCount > 0:
            awardVal.addWealthByItemId(coreItemID, normalCount, gameconst.ItemBindType.NORMAL)

    def canBeDisassembled(self):
        gearBaseData = GBGBD.datas[self.itemId]
        if not gearBaseData:
            ERROR_MSG('canBeDisassembled missing gear base config', self.itemId)
            return False

        dissassemblyReward = None
        if self.bindType == gameconst.ItemBindType.BIND:
            dissassemblyReward = gearBaseData['disassemblyReward']
            if dissassemblyReward is None:
                WARNING_MSG('canBeDisassembled missing dissassemle reward id config', self.itemId)
                return False
        elif self.bindType == gameconst.ItemBindType.NORMAL:
            dissassemblyReward = gearBaseData['disassemblyReward2']
            if dissassemblyReward is None:
                WARNING_MSG('canBeDisassembled missing dissassemle reward2 id config', self.itemId)
                return False

        if not dissassemblyReward:
            WARNING_MSG('canBeDisassembled unknow bind type', self.itemId, self.bindType)
            return False


        awardData = RDDT.datas.get(dissassemblyReward)
        if not awardData:
            ERROR_MSG('canBeDisassembled invalid dissassemle drop id config', self.itemId, dissassemblyReward)
            return False

        return True

    def getEnhanceLevel(self):
        return self.equipAttr.getEnhanceLv()

    def getGrade(self):
        return self.equipAttr.getGrade()

    def _calcEnhanceVal(self, level):
        enhanceKey = self.equipAttr.getEnhanceLevelKey(level)
        enhanceData = GEGS.datas.get(enhanceKey)
        effectData = enhanceData['effect']
        valList = effectData[0]
        weightList = effectData[1]
        idx = utils.randomByWeight(weightList)
        return valList[idx]

    def doEnhanceEquip(self, owner, opUUID, level, onBody=False, isGM = False):
        DEBUG_MSG('in doEnhanceEquip')
        enhanceLevelKey = self.equipAttr.getEnhanceLevelKey(level)
        cfgData = GEGS.datas.get(enhanceLevelKey)
        if not cfgData:
            ERROR_MSG('in doEnhanceEquip, equipment is enhanced to max level:', enhanceLevelKey)
            return
        encVal = level
        if not isGM:
            encVal = self._calcEnhanceVal(level)
        if onBody:
            self.removeEquipEffectToAvatar(owner)

        # 没有破碎就正常强化升级
        if encVal != gameconst.EquipConstVale.ENHANCEMENT_BROKEN_FLAG:
            self.equipAttr.doEnhanceLv(encVal, isGM)
            DEBUG_MSG('     in doEnhanceEquip, success:', level, encVal)
        if onBody:
            self.applyEquipEffectToAvatar(owner)
        return encVal

    def doUpgradeEquip(self, owner, opUUID, onBody=False):
        DEBUG_MSG('in doUpgradeEquip')
        upgradeKey = self.equipAttr.getUpgradeKey(self.getGrade() + 1)
        cfgData = GEES.datas.get(upgradeKey)
        if not cfgData:
            ERROR_MSG('in doUpgradeEquip, equipment is upgraded to max grade:', upgradeKey)
            return

        if onBody:
            self.removeEquipEffectToAvatar(owner)
        self.equipAttr.doUpgrade(1)
        if onBody:
            self.applyEquipEffectToAvatar(owner)
        DEBUG_MSG('     in doUpgradeEquip, success:', self.getGrade())

    def doEquipSpiritWashing(self, owner, spiritPos, unbindValue):
        ret, oldSpiritAffixes, newSpiritAffixes = self.equipAttr.spiritWashing(spiritPos, unbindValue)
        if ret:
            self.onEquipAffixChanged()
        return ret, oldSpiritAffixes, newSpiritAffixes

    def doEquipGlyphWashing(self, owner, glyphPos, affixIds = None):
        ret, oldGlyphAffixes, newGlyphAffixes = self.equipAttr.glyphWashing(glyphPos, affixIds)
        if ret:
            self.onEquipAffixChanged()
        return ret, oldGlyphAffixes, newGlyphAffixes

    def doEquipBlessing(self, owner):
        ret = self.equipAttr.blessing()
        if ret:
            self.onEquipAffixChanged()
        return ret

    def doEquipBackBless(self):
        ret = self.equipAttr.backBless()
        if ret:
            self.onEquipAffixChanged()
        return ret

    def isEquipBaseAttrsMaxVal(self):
        return self.equipAttr.isBaseAttrsMaxVal()

    def applyEquipEffectToAvatar(self, owner, isLogin=False):
        self._applyBaseAttrs(owner)
        self.applyAffixesToAvatar(owner, isLogin=isLogin)

    def removeEquipEffectToAvatar(self, owner):
        self._removeBaseAttrs(owner)
        self.removeAffixesFromAvatar(owner)
        return

    def _applyBaseAttrs(self, owner):
        self._changeBaseAttrByRate(owner, 1, 1)
        return

    def _removeBaseAttrs(self, owner):
        self._changeBaseAttrByRate(owner, 1, -1)
        return

    def _changeBaseAttrByRate(self, owner, rate, factor):
        DEBUG_MSG('in _changeBaseAttrByRate, rate:', rate, factor)
        for attrName, attrValue in itertools.chain.from_iterable([self.equipAttr.baseAttrs.items(), self.equipAttr.upgradeAttrs.items(), self.equipAttr.enhanceAttrs.items()]):
            newVal = attrValue*rate*factor
            owner.addProp(attrName, newVal, gameconst.SourceType.Equip)

    def getBaseAttrInfo(self):
        infoDic = {}
        for attrName, attrValue in self.equipAttr.baseAttrs.items():
            infoDic[attrName] = attrValue
        return infoDic

    def addPropByEquip(self, owner, attrNameList, attrValList, startIdx=0, endIdx=-1):
        DEBUG_MSG('in addPropByEquip:', attrNameList, attrValList)
        AffixInfo.applyAffixPropEffectToAvatar(owner, self, attrNameList, attrValList, gameconst.SourceType.Equip,
                                               afxValStartIdx=startIdx, afxValEndIdx=endIdx)
        return

    def recordAffixAddSingleProp(self, attrName, attrVal):
        DEBUG_MSG('in equipmnetItem recordAffixAddSingleProp:', attrName, attrVal)
        self.equipAttr.baseAttrsByAfxVal.setdefault(attrName, 0)
        self.equipAttr.baseAttrsByAfxVal[attrName] += attrVal
        return

    def isGood(self):
        return self.equipAttr.dropFixEndTime < utils.getNow()

    def hasBindValue(self):
        return self.equipAttr.isAddBindValue or self.equipAttr.bindValue > 0

    def setBindValue(self, value):
        self.equipAttr.bindValue = value
        if self.equipAttr.bindValue > 0:
            self.bindType = gameconst.ItemBindType.BIND
        else:
            self.bindType = gameconst.ItemBindType.NORMAL

    def doDecreaseBindValue(self, opUUID, value):
        if value >= self.getBindValue():
            self.setBindValue(0)
            self.equipAttr.isAddBindValue = False
        elif value >= self.getOriginalBindValue():
            self.setBindValue(0)
        else:
            self.setBindValue(self.equipAttr.bindValue - value)

    def getBindValue(self):
        addValue = int(GEGCD.datas['gearEnhanceBindLimit']['value']) if self.equipAttr.isAddBindValue else 0
        return self.equipAttr.bindValue + addValue

    def getOriginalBindValue(self):
        return self.equipAttr.bindValue

    def addSingleSkLvByEquip(self, owner, skillId, afxValList, isLogin=False, valIdx=0):
        DEBUG_MSG('in addSingleSkLvByEquip:', skillId, afxValList, isLogin)
        if len(afxValList) > 0:
            self.equipAttr.skillAddLvDic.setdefault(skillId, 0)
            self.equipAttr.skillAddLvDic[skillId] += afxValList[valIdx]
            owner.bodyEquipData.addSkillLv(owner, [skillId], [afxValList[valIdx]], isLogin=isLogin)

    def addClassSkLvByEquip(self, owner, aVals, school, valIdx=0, isLogin=False):
        DEBUG_MSG('in addClassSkLvByEquip:', aVals, school, owner.school, valIdx)
        if school != owner.school:
            return
        if len(aVals) == 0 or valIdx >= len(aVals):
            gameengine.reportCritical('     in addClassSkLvByAffix, aVals empty')
            return
        self.equipAttr.skillAddLvDic.setdefault(gameconst.ClassSkillID, 0)
        self.equipAttr.skillAddLvDic[gameconst.ClassSkillID] += aVals[valIdx]
        owner.bodyEquipData.addSkillLv(owner, [gameconst.ClassSkillID], [aVals[valIdx]], isLogin=isLogin)

    def applyAffixesToAvatar(self, owner, isLogin=False):
        self.equipAttr.resetEquipAffixPropsData()

        def doAffixObj(self, affixObj):
            affixData = AFAFD.datas.get(affixObj.afxId)
            if not affixData:
                return False
            event = affixData.get('event', None)
            if event != 'onDress':
                return False
            actionEffect = affixData.get('actionEffect', None)
            if not actionEffect:
                return False
            actionEffect(owner, None, actionContext.EquipActionCtx(self, [affixObj.affixVal], affixObj.lv,
                                                                   affixData['levelGap'], isLogin=isLogin))
            return True

        for affixObj in self.equipAttr.blessAffixes:
            doAffixObj(self, affixObj)

        for idx, spiritData in enumerate(self.equipAttr.spiritDatas):
            if idx != self.equipAttr.spiritGroup:
                continue
            for spiritAffix in spiritData.spiritAffixes:
                doAffixObj(self, spiritAffix)

        for glyphData in self.equipAttr.glyphInfo:
            if glyphData.getGlyphPos() // 2 != self.equipAttr.glyphGroup:
                continue
            for glyphAffix in glyphData.glyphAffixes:
                doAffixObj(self, glyphAffix)
        return

    def removeAffixesFromAvatar(self, owner):
        DEBUG_MSG('in removeAffixesFromAvatar  ', self.equipAttr.baseAttrsByAfxVal)
        AffixInfo.removeAffixEffectFromAvatar(owner, self, self.equipAttr.baseAttrsByAfxVal, gameconst.SourceType.Equip)
        self.equipAttr.resetEquipAffixPropsData()
        return

    def removeAddSkillLv(self, owner):
        skillLvDic = self.getAddSkillLvDic()
        skillIdList = []
        deltaLvList = []
        for skId, addLv in skillLvDic.items():
            skillIdList.append(skId)
            deltaLvList.append(-1*addLv)
        owner.bodyEquipData.addSkillLv(owner, skillIdList, deltaLvList)
        return

    def onEquipAffixChanged(self):
        self.equipAttr.resetAfxInitAttr()

        def doAffixObj(self, affixObj):
            affixData = AFAFD.datas.get(affixObj.afxId)
            if affixData['event'] != 'onInit':
                return False
            actionEffect = affixData.get('actionEffect')
            if not actionEffect:
                return False
            actionEffect(self, None, actionContext.EquipActionCtx(self, [affixObj.affixVal], affixObj.lv, affixData['levelGap']))

            return True

        for affixObj in self.equipAttr.blessAffixes:
            doAffixObj(self, affixObj)

        for idx, spiritData in enumerate(self.equipAttr.spiritDatas):
            if idx != self.equipAttr.spiritGroup:
                continue
            for spiritAffix in spiritData.spiritAffixes:
                doAffixObj(self, spiritAffix)

        for glyphData in self.equipAttr.glyphInfo:
            if glyphData.getGlyphPos() // 2 != self.equipAttr.glyphGroup:
                continue
            for glyphAffix in glyphData.glyphAffixes:
                doAffixObj(self, glyphAffix)
        return

    def getAddSkillLvDic(self):
        return self.equipAttr.skillAddLvDic

    def getEquipScore(self):
        return self.equipAttr.score

    def clearRoleBindData(self, **kwargs):
        super(EquipmentItem, self).clearRoleBindData(**kwargs)
        return

    def getItemLevel(self):
        return GBGBD.datas[self.itemId]["iLevel"]

    def checkGlyphNum(self, glyphPos):
        return glyphPos < self.equipAttr.glyphSlotNum

    def checkGlyphApplyGroupId(self, groupId):
        if self.equipAttr.glyphSlotNum <= 0:
            return False
        return 0 <= groupId <= ((self.equipAttr.glyphSlotNum - 1) // 2)

    def doApplyGlyphGroupId(self, src, groupId):
        ret = self.equipAttr.applyGlyphGroupId(groupId)
        if ret:
            self.onEquipAffixChanged()
        return ret

    def checkSpiritApplyGroupId(self, groupId):
        spiritAffixCount = len(self.equipAttr.spiritDatas)
        if spiritAffixCount > 0:
            return spiritAffixCount // 2 >= groupId
        return False

    def doApplySpiritGroupId(self, src, groupId):
        ret = self.equipAttr.applySpiritGroupId(groupId)
        if ret:
            self.onEquipAffixChanged()
        return ret

    # 获取铭文词缀
    def getGlyphAffixes(self):
        glyphAffixes = []
        for glyphData in self.equipAttr.glyphInfo:
            if glyphData.getGlyphPos() // 2 != self.equipAttr.glyphGroup:
                continue
            for glyphAffix in glyphData.getGlyphAffixes():
                glyphAffixes.append(glyphAffix)
        return glyphAffixes

    def checkSpiritNum(self, spiritGroup):
        return spiritGroup < self.equipAttr.spiritSlotNum

    def getGlyphGroupId(self):
        return self.equipAttr.glyphGroup

    def getSpiritGroupId(self):
        return self.equipAttr.spiritGroup

    def hasGlyphData(self):
        return len(self.equipAttr.glyphInfo) > 0

    def updateBindValue(self):
        if not self.equipAttr.isAddBindValue:
            self.equipAttr.isAddBindValue = True
            self.bindType = gameconst.ItemBindType.BIND

    def getAddBindValueStatus(self):
        return self.equipAttr.isAddBindValue

    def setEquipSchool(self, school):
        self.equipAttr.school = school
        self.equipAttr.calcScore()

    def getEquipType(self):
        return self.equipAttr.equipType
    
    def getEquipQuality(self):
        return self.equipAttr.quality

class EquipAttr(userType.UserSoleType):

    def __init__(self):
        self.equipType = 0
        self.equipSubType = 0
        self.equipLv = 0
        self.quality = 0

        self.grade = 0
        self.templateId = 0
        self.score = 0
        self.baseScore = 0          #不加入强化、附魂的评分
        # 附灵数据
        self.spiritDatas = []
        # 附灵编组
        self.spiritGroup = 0
        # 铭文数据
        self.glyphInfo = []
        # 铭文编组
        self.glyphGroup = 0
        self.blessAffixes = []
        self.washingLuckData = {}    #词条洗练保底数据
        self.enhanceLv = 0
        self.maxBlessLv = 0
        self.blessLvRate = 0
        self.dropFixEndTime = 0 # 掉落修复结束时间
        # 基础属性
        self.baseAttrs = {}
        # 升阶属性
        self.upgradeAttrs = {}
        # 强化属性
        self.enhanceAttrs = {}
        self.resetEquipAffixPropsData()

        self.attrJson = ""
        self.bindValue = 0
        self.isAddBindValue = False
        self.school = 0
        self.setDirtyFlag(False)

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        self.setDirtyFlag()

    @classmethod
    def _checkIgnores_(cls):
        # 当dirty置True以后(EquipAttr的属性发生变化)，旧的 attrJson 过期，toJson()时会根据 EquipAttr 的属性重新生成一份新的；
        # fromJson()会设置 attrJson 为与最新的attrJson(与EquipAttr 对应)
        return 'attrJson'

    def setDirtyFlag(self, flag=True):
        object.__setattr__(self, 'dirty', flag)

    def isDirty(self):
        return self.dirty

    @property
    def glyphSlotNum(self):
        if not dataUtils.checkEquipmentGlyphType(self.equipType):
            return 0
        enhanceLevelKey = self.getEnhanceLevelKey(self.enhanceLv)
        cfgData =  GEGS.datas.get(enhanceLevelKey)
        if not cfgData:
            return 0
        # 铭文槽位数量按照强化等级开启
        return cfgData["slot"]

    @property
    def spiritSlotNum(self):
        if not dataUtils.checkEquipmentSpiritType(self.equipType):
            return 0
        enhanceLevelKey = self.getEnhanceLevelKey(self.enhanceLv)
        cfgData =  GEGS.datas.get(enhanceLevelKey)
        if not cfgData:
            return 0
        # 附灵槽位数量按照强化等级开启
        return cfgData["fuLingGroup"]

    def getEnhanceLevelKey(self, enhanceLevel):
        return self.equipType * 10000 + self.quality * 1000 + self.grade * 100 + enhanceLevel

    def getUpgradeKey(self, grade):
        return self.equipType * 1000 + self.quality * 100 + grade

    def getUpgradePropKey(self, grade):
        return self.templateId* 100 + grade

    def resetEquipAffixPropsData(self):
        # 装备的词缀加成数据清空
        self.baseAttrsByAfxVal = {}
        self.skillAddLvDic = {}

    def _lateReload(self):
        super(EquipAttr, self)._lateReload()

        for v in self.blessAffixes:
            v.reloadScript()

        for v in self.spiritDatas:
            v.reloadScript()

        for v in self.glyphInfo:
            v.reloadScript()

    def toJson(self, extraAttrs=None):
        if not self.attrJson or self.isDirty():
            self.attrJson = json.dumps(self.toDict(extraAttrs=extraAttrs))
            self.setDirtyFlag(False)
        return self.attrJson

    def toClientDic(self):
        blessAffixes = []
        for oneAffix in self.blessAffixes:
            blessAffixes.append(oneAffix.toAfxClientDic())

        spiritDatas = []
        for spiritData in self.spiritDatas:
            spiritDatas.append(spiritData.toClientData())

        glyphDatas = []
        for glyphData in self.glyphInfo:
            glyphDatas.append(glyphData.toClientData())

        return {
            'spiritDatas': spiritDatas,
            'spiritGroup': self.spiritGroup,
            'blessAffixes': blessAffixes,
            'glyphInfo': glyphDatas,
            'glyphGroup': self.glyphGroup,
            'enhanceLv': self.enhanceLv,
            'maxBlessLv': self.maxBlessLv,
            'blessLvRate': self.blessLvRate,
            'dropFixEndTime': self.dropFixEndTime,
            'score': self.score,
            'bindValue': self.bindValue,
            'isAddBindValue': self.isAddBindValue,
            'grade': self.grade
        }

    def toDict(self, extraAttrs=None):
        blessAffixes = []
        for oneAffix in self.blessAffixes:
            blessAffixes.append(oneAffix.toAffixValList())

        spiritDatas = []
        for spiritData in self.spiritDatas:
            spiritDatas.append(spiritData.toDBData())

        glyphDatas = []
        for glyphData in self.glyphInfo:
            glyphDatas.append(glyphData.toDBData())

        jsonDic = {
            'templateId': self.templateId,
            'score': self.score,
            'spiritDatas': spiritDatas,
            'spiritGroup': self.spiritGroup,
            'blessAffixes': blessAffixes,
            'glyphInfo': glyphDatas,
            'glyphGroup': self.glyphGroup,
            'washingLuckData': self.washingLuckData,
            'enhanceLv': self.enhanceLv,
            'maxBlessLv': self.maxBlessLv,
            'blessLvRate': self.blessLvRate,
            'baseAttrsByAfxVal': self.baseAttrsByAfxVal,
            'skillAddLvDic': self.skillAddLvDic,
            'dropFixEndTime': self.dropFixEndTime,
            'bindValue': self.bindValue,
            'isAddBindValue': self.isAddBindValue,
            'grade': self.grade,
            'school': self.school,
        }

        if extraAttrs:
            jsonDic.update(extraAttrs)
        return jsonDic

    def fromJson(self, jsonStr):
        try:
            value = json.loads(jsonStr)
            self.templateId = value.get('templateId', 0)
            gearBaseData = dataUtils.getEquipItemData(self.templateId)
            self.equipType = gearBaseData.get('type', 0)
            self.equipSubType = gearBaseData.get('subType', 0)
            self.equipLv = gearBaseData.get('iLevel', 0)
            self.quality = gearBaseData.get('quality', 0)
            grade = value.get('grade', 0)
            if grade == 0:
                # 装备默认品阶为1
                grade = gearBaseData.get('grade', 1)
            self.grade = grade

            self.spiritDatas = []
            spiritDatas = value.get('spiritDatas', [])
            for spiritData in spiritDatas:
                newSpiritData = SpiritInfo.SpiritInfo()
                newSpiritData.fromDBData(spiritData)
                self.spiritDatas.append(newSpiritData)

            self.spiritGroup = value.get('spiritGroup', 0)

            self.glyphInfo = []
            glyphInfo = value.get('glyphInfo', [])
            for glyphData in glyphInfo:
                newGlyphData = GlyphInfo.GlyphInfo()
                newGlyphData.fromDBData(glyphData)
                self.glyphInfo.append(newGlyphData)

            self.glyphGroup = value.get('glyphGroup', 0)

            self.blessAffixes = []
            blessAffixes = value.get('blessAffixes', [])
            for oneAffixVal in blessAffixes:
                affixObj = AffixInfo.Affix(oneAffixVal[0])
                affixObj.fromAffixValList(oneAffixVal)
                self.blessAffixes.append(affixObj)

            self.washingLuckData = value.get('washingLuckData', {})

            self.enhanceLv = value.get('enhanceLv', 0)
            self.maxBlessLv = value.get('maxBlessLv', 0)
            self.blessLvRate = value.get('blessLvRate', 0)
            self.baseAttrsByAfxVal = value.get('baseAttrsByAfxVal', {})
            self.dropFixEndTime = value.get('dropFixEndTime', 0)

            skillAddLvDic = value.get('skillAddLvDic', {})
            self.skillAddLvDic = {}
            for k, v in skillAddLvDic.items():
                self.skillAddLvDic[int(k)] = v

            self.bindValue = value.get('bindValue', 0)
            self.isAddBindValue = value.get('isAddBindValue', False)
            self.school = value.get('school', 0)
            self.calcBaseAttrs()
            oldScore = value.get('score', 0)
            self.calcScore()
            if oldScore == self.score:
                self.attrJson = jsonStr
                self.setDirtyFlag(False)
            return value
        except Exception as e:
            ERROR_MSG('EEEEEEEEEEEEEEEEror!!! in EquipmentItem:fromJson:', e, jsonStr)
        return {}

    def initAttrFromTemplate(self, templateId, tempData):
        self.equipType = tempData['type']
        self.equipSubType = tempData['subType']
        self.equipLv = tempData['iLevel']
        self.quality = tempData['quality']
        # 默认品阶为1
        self.grade = tempData['grade']
        self.templateId = templateId
        return

    def _genGlyphAffix(self,  totalAffixesNum=0, specificAffixId=0):
        DEBUG_MSG('in _genGlyphAffix:', totalAffixesNum, specificAffixId)
        return self._doRandomAffix(GLYPHTWD.datas, totalAffixesNum, specificAffixId, True)

    def _genSpiritAffix(self,  totalAffixesNum=0, specificAffixId=0):
        DEBUG_MSG('in _genSpiritAffix:', totalAffixesNum, specificAffixId)
        return self._doRandomAffix(AFAFTWD.datas, totalAffixesNum, specificAffixId)

    def _doRandomAffix(self, affixWeights, totalAffixesNum=0, specificAffixId=0, isGlyph = False):
        DEBUG_MSG('in _doRandomAffix:', totalAffixesNum, specificAffixId)
        randomAffixes = []
        if self.quality in gameconst.ItemQuality.NO_RANDOM_FIX_QUALITY:
            ERROR_MSG('in _doRandomAffix: error quality', self.quality, totalAffixesNum, specificAffixId)
            return randomAffixes

        if totalAffixesNum == 0:
            weight_list = AFRAFCWD.affixNumWeightDic.get(self.quality)
            if not weight_list:
                ERROR_MSG('in _doRandomAffix: missing weight list', self.quality, totalAffixesNum, specificAffixId)
                return randomAffixes
            rdIdx = utils.randomByWeight(weight_list)
            rdAfNum = rdIdx
        else:
            rdAfNum = totalAffixesNum

        key = 'gear_' + str(self.equipSubType) + '_' + str(self.quality)
        affixIdList = []
        affixIdWeightList = []
        for affixId, val in affixWeights.items():
            if affixId == specificAffixId:
                continue
            wt = val.get(key, 0)
            if wt:
                affixIdList.append(affixId)
                affixIdWeightList.append(wt)


        for idx in range(rdAfNum):
            if specificAffixId > 0:
                randomAffixId = specificAffixId
                specificAffixId = 0
            else:
                rdIdx = utils.randomByWeight(affixIdWeightList)
                randomAffixId = affixIdList[rdIdx]
                if idx < rdAfNum - 1:
                    affixIdList.pop(rdIdx)
                    affixIdWeightList.pop(rdIdx)
            affix = self.generateAffix(randomAffixId, isGlyph)
            if not affix:
                continue
            randomAffixes.append(affix)

        return randomAffixes

    def generateAffix(self, affixId, isGlyph):
        affixData = AFAFD.datas.get(affixId)
        if not affixData:
            return None
        templateData = dataUtils.getEquipItemData(self.templateId)
        iLevel = templateData['iLevel']
        levelGap = affixData.get('levelGap', gameconst.EquipAttrConst.AFFIX_DEFAULT_LEVEL_GAP)
        affixLv = min(max(math.ceil(iLevel / levelGap), 1), affixData['maxLevel'])
        assessmentWeight = affixData.get('assessmentWeight')
        if affixData['floor'] and affixData['ceiling']:
            DEBUG_MSG('generateAffix 1', affixData['floor'], affixData['ceiling'])
            affixValFloorList = affixData['floor'](affixLv)
            affixValCeilList = affixData['ceiling'](affixLv)
            for floorVal, ceilVal in zip(affixValFloorList, affixValCeilList):
                if isinstance(floorVal, int) and isinstance(ceilVal, int):
                    val = random.randint(floorVal, ceilVal)
                else:
                    val = random.uniform(floorVal, ceilVal)
                    val = round(val, 4)
                break
        elif assessmentWeight:
            DEBUG_MSG('generateAffix 2', assessmentWeight)
            rdIdx = utils.randomByWeight(assessmentWeight)
            assessmentInterval = AFAFD.datas.get(affixId, {}).get('assessmentInterval')
            if not assessmentInterval:
                WARNING_MSG('in _doRandomAffix, no assessmentInterval:', affixId)
                return None
            assessmentInterval = assessmentInterval[rdIdx]
            affixValFloor = assessmentInterval[0]
            affixValCeil = assessmentInterval[1]
            if isinstance(affixValFloor, int) and isinstance(affixValCeil, int):
                val = random.randint(affixValFloor, affixValCeil)
            else:
                val = random.uniform(affixValFloor, affixValCeil)
                val = round(val, 4)
        else:
            WARNING_MSG('in _doRandomAffix, no affixValFloorList:', affixId)
            val = 0
        affix = AffixInfo.genRandomAffix(affixId, iLevel, val, isGlyph)
        return affix

    def isBaseAttrsMaxVal(self):
        return True

    def calcBaseAttrs(self):
        templateData = dataUtils.getEquipItemData(self.templateId)
        propId = templateData.get('propID')
        if propId > 0:
            propCfgDic = PFPD.datas.get(propId, {}).get('propList', {})
            for attrName, val in propCfgDic.items():
                self.baseAttrs[attrName] = val
        # 初始强化和升阶属性
        self.calculateEnhanceAndUpgradeAttrs(self.enhanceLv, self.grade, True)
        return True

    def setGradeAttrs(self, attrName, attrVal):
        self.upgradeAttrs[attrName] = attrVal

    def calcScore(self):
        affixTotalScore = 0
        totalAttrScore = 0

        for attrName, attrVal in itertools.chain.from_iterable([self.baseAttrs.items(), self.upgradeAttrs.items(), self.enhanceAttrs.items()]):
            propBaseScore = dataUtils.filterFightPropScore(self.school, attrName)
            totalAttrScore += int(propBaseScore * attrVal)

        for oneAffix in self.blessAffixes:
            affixTotalScore += oneAffix.getAfxScore(self.school)

        for idx, spiritData in enumerate(self.spiritDatas):
            if idx != self.spiritGroup:
                continue
            for spiritAffix in spiritData.spiritAffixes:
                affixTotalScore += spiritAffix.getAfxScore(self.school)

        for glyphData in self.glyphInfo:
            if glyphData.getGlyphPos() // 2 != self.glyphGroup:
                continue
            for glyphAffix in glyphData.glyphAffixes:
                affixTotalScore += glyphAffix.getAfxScore(self.school)


        baseScore = totalAttrScore + affixTotalScore
        self.baseScore = int(baseScore)
        self.score = baseScore

    def calculateUpgradeScoreAndAttrs(self, grade, needScore = True):
        score = 0
        # 需要更新属性
        self.upgradeAttrs = {}
        dataKey = self.getUpgradePropKey(grade)
        propId = GEEA.attributeDic.get(dataKey)
        if propId > 0:
            propCfgDic = PFPD.datas.get(propId, {}).get('propList', {})
            for attrName, attrValue in propCfgDic.items():
                self.upgradeAttrs[attrName] = attrValue
                if needScore:
                    score += int(round(dataUtils.filterFightPropScore(self.school, attrName) * attrValue))
        return score

    def resetAfxInitAttr(self):
        return

    def getEnhanceLv(self):
        return self.enhanceLv

    def getGrade(self):
        return self.grade

    def doEnhanceLv(self, val, isGM = False):
        lv = self.enhanceLv + val
        if isGM:
            lv = val
        enhanceLv = max(0, lv)
        oldEnhanceLv = self.enhanceLv
        self.enhanceLv = enhanceLv
        self.calculateEnhanceAndUpgradeAttrs(oldEnhanceLv, self.grade)
        self.calcScore()

    # 计算升阶和强化属性
    def calculateEnhanceAndUpgradeAttrs(self, oldEnhanceLv, oldGrade, isInit = False):
        # 检查是否升阶了
        isUpgrade = False
        if self.grade != oldGrade or isInit:
            isUpgrade = True
            self.calculateUpgradeScoreAndAttrs(self.grade, needScore=False)

        # 检查是否升阶了，或者强化了，因为强化属性是在升阶属性的基础上进行加成
        if isUpgrade or self.enhanceLv != oldEnhanceLv or isInit:
            self.enhanceAttrs = {}
            # 强化会回退
            if self.enhanceLv <= 0:
                return
            strengthenPercent = GEGCD.datas['strengthenPercent']['value']
            # 无加成
            if len(strengthenPercent) == 0:
                return
            noStrengthenList = GEGCD.datas['noStrengthenList']['value']
            for attrName, attrValue in self.upgradeAttrs.items():
                if attrName in noStrengthenList:
                    continue
                self.enhanceAttrs[attrName] = math.ceil(strengthenPercent[self.enhanceLv - 1] * attrValue)

    def doUpgrade(self, val, isGM = False):
        lv = self.grade + val
        if isGM:
            lv = val
        grade = max(0, lv)
        oldGrade = self.grade
        self.grade = grade
        self.calculateEnhanceAndUpgradeAttrs(self.enhanceLv, oldGrade)
        self.calcScore()

    def spiritWashing(self, spiritPos, unbindValue):
        DEBUG_MSG('in spiritWashing:', self.washingLuckData, spiritPos, unbindValue)
        if self.spiritSlotNum <= 0:
            ERROR_MSG('in spiritWashing spiritSlotNum is 0')
            return False, None, None

        if spiritPos < 0 or spiritPos >= self.spiritSlotNum:
            ERROR_MSG('in spiritWashing invalid spiritPos', spiritPos)
            return False, None, None

        if 0 == len(self.washingLuckData):
            self._refreshWashingLuckData(reset=True)

        totalAffixesNum = 0
        specificAffixId = 0
        triggerLuck = False
        blessAffixId = int(GEGCD.datas['blessAffixID']['value'])
        for idx, washRecords in self.washingLuckData.items():
            # washRecords :[curNum, dstNum]
            # 固定词条中指定词条数量必须等于配置数量才会触发这条保底
            luckData = GEFLD.datas.get(int(idx))

            washRecords[0] += 1
            if washRecords[0] == washRecords[1]:
                if not luckData:
                    gameengine.reportCritical('affixWashing, idx error:', idx, self.washingLuckData)
                    self._refreshWashingLuckData(reset=True)
                    break

                if luckData['totalAffixNum'] > totalAffixesNum:
                    INFO_MSG('in affixWashing, luck affixNum trigger:', idx, washRecords, luckData)
                    totalAffixesNum = luckData['totalAffixNum']
                    triggerLuck = True

                if luckData['rarityLevel'] > 0:
                    rarityLevel = luckData['rarityLevel']
                    ranAffixIdList = AFAFD.rarityLevelDic.get(rarityLevel, [])
                    key = 'gear_' + str(self.equipSubType) + '_' + str(self.quality)
                    if len(ranAffixIdList) > 0:
                        affixIdList = []
                        affixIdWeightList = []
                        for affixId in ranAffixIdList:
                            # 幸运词条，只有非绑定消耗才能参与随机
                            if blessAffixId and affixId == blessAffixId:
                                if unbindValue <= 0:
                                    continue
                            wt = AFAFTWD.datas.get(affixId)
                            if wt:
                                wt = wt.get(key)
                                if wt:
                                    affixIdList.append(affixId)
                                    affixIdWeightList.append(wt)
                        if len(affixIdList) == 0:
                            ERROR_MSG('affixWashing affix not found by rarityLevel', rarityLevel)
                        else:
                            rdIdx = utils.randomByWeight(affixIdWeightList)
                            specificAffixId = affixIdList[rdIdx]
                    INFO_MSG('in affixWashing, specificAffix trigger:', idx, washRecords, luckData)
                    triggerLuck = True
        if triggerLuck:
            self._refreshWashingLuckData()
        newSpiritAffixes = self._genSpiritAffix(totalAffixesNum, specificAffixId)
        if len(newSpiritAffixes) == 0:
            ERROR_MSG('in spiritWashing empty spirit affixes', totalAffixesNum)
            return False, None, None

        if spiritPos + 1 > len(self.spiritDatas):
            self.spiritDatas.append(SpiritInfo.SpiritInfo())
        spiritData = self.spiritDatas[spiritPos]
        oldSpiritAffixes = spiritData.GetSpiritAffixes()
        spiritData.UpdateSpiritAffixes(newSpiritAffixes)
        self.calcScore()
        self.setDirtyFlag()
        return True, oldSpiritAffixes, newSpiritAffixes

    def _refreshWashingLuckData(self, reset=False):
        DEBUG_MSG('in _refreshWashingLuckData:', self.washingLuckData)
        idxList = GEFLD.qualityIdxDic.get(self.quality)
        if reset:
            self.washingLuckData={}

        lowerRate = GBGCD.datas['fakeLuckCountRangeLowerBound']['value']
        highRate = GBGCD.datas['fakeLuckCountRangeUpperBound']['value']
        for idx in idxList:
            idx = str(idx)
            if idx in self.washingLuckData and self.washingLuckData[idx][0] < self.washingLuckData[idx][1]:
                continue
            luckData = GEFLD.datas[int(idx)]
            dstNum = round(luckData['reforgeCount'] * random.uniform(lowerRate, highRate))
            self.washingLuckData[idx] = [0, dstNum]
        self.setDirtyFlag(True)
        INFO_MSG('after refresh, _refreshWashingLuckData:', self.washingLuckData)
        return

    def glyphWashing(self, glyphPos, affixIds = None):
        DEBUG_MSG('in glyphWashing', glyphPos, affixIds)
        if self.glyphSlotNum <= 0:
            ERROR_MSG('in glyphWashing glyphSlotNum is 0')
            return False, None, None

        if glyphPos < 0 or glyphPos >= self.glyphSlotNum:
            ERROR_MSG('in glyphWashing invalid glyphPos', glyphPos)
            return False, None, None

        if affixIds:
            newGlyphAffixes = []
            for affixId in affixIds:
                affixData = self.generateAffix(affixId, True)
                if affixData:
                    newGlyphAffixes.append(affixData)
        else:
            # 随机铭文个数
            randomVals = GEGCD.datas['gearWeaponGlyphNumWeight']['value']
            idx = utils.randomByWeight(randomVals)
            totalAffixCount = idx + 1
            newGlyphAffixes = self._genGlyphAffix(totalAffixCount)

        if len(newGlyphAffixes) == 0:
            ERROR_MSG('in glyphWashing empty glyph affixes', newGlyphAffixes)
            return False, None, None

        # 更新铭文数据
        oldGlyphAffixes = self.updateGlyphInfo(glyphPos, newGlyphAffixes)
        self.calcScore()
        self.setDirtyFlag()
        return True, oldGlyphAffixes, newGlyphAffixes

    def updateGlyphInfo(self, glyphPos, glyphAffixes):
        isGot = False
        oldGlyphAffixes = None
        for glyphData in self.glyphInfo:
            if glyphPos == glyphData.getGlyphPos():
                isGot = True
                oldGlyphAffixes = glyphData.getGlyphAffixes()
                glyphData.updateGlyphAffixes(glyphAffixes)
                break
        if not isGot:
            glyphData = GlyphInfo.GlyphInfo(glyphPos)
            glyphData.updateGlyphAffixes(glyphAffixes)
            self.glyphInfo.append(glyphData)
        return oldGlyphAffixes

    def getGlyphData(self, glyphPos):
        for glyphData in self.glyphInfo:
            if glyphPos == glyphData.getGlyphPos():
                return glyphData
        return None

    def blessing(self):
        DEBUG_MSG('in blessing')
        templateData = dataUtils.getEquipItemData(self.templateId)
        iLevel = templateData['iLevel']
        affixId = dataUtils.getBlessAffixIdByGearType(self.equipType)
        if len(self.blessAffixes) == 0:
            blessAffix = AffixInfo.genBlessAffix(iLevel, affixId)
            key = self.equipType * 10
        else:
            blessAffix = self.blessAffixes[0]
            key = self.equipType * 10 + blessAffix.affixVal

        result = GEBLD.datas[key]['result']
        gearBlessMaxValue = GEGCD.datas['gearBlessMaxValue']['value']
        blessNum = result[0][utils.randomByWeight(result[1])]
        blessAffix.affixVal = max(0, min(blessAffix.affixVal + blessNum, gearBlessMaxValue))
        key = self.equipType * 10 + max(blessAffix.affixVal, self.maxBlessLv)
        backtrack = GEBLD.datas[key]['backtrack']
        if backtrack:
            if blessAffix.affixVal > self.maxBlessLv:
                self.maxBlessLv = blessAffix.affixVal
                self.blessLvRate = 0
            else:
                if self.blessLvRate < backtrack:
                    self.blessLvRate += 1
        self.blessAffixes = [blessAffix]
        self.calcScore()
        return True

    def backBless(self):
        DEBUG_MSG('in backBless')
        blessAffix = self.blessAffixes[0]
        blessAffix.affixVal = self.maxBlessLv
        self.blessLvRate = 0
        self.calcScore()
        return True

    def applyGlyphGroupId(self, groupId):
        # 检查一下是否有新旧替换
        ret = False
        if groupId != self.glyphGroup:
            self.glyphGroup = groupId
            self.calcScore()
            ret = True
        return ret

    def applySpiritGroupId(self, groupId):
        # 检查一下是否有新旧替换
        ret = False
        if groupId != self.spiritGroup:
            self.spiritGroup = groupId
            self.calcScore()
            ret = True
        return ret

class EquipItemIdGen(object):
    LV_OFFSET_MIN = -14
    LV_OFFSET_MAX = 5

    @classmethod
    def genEquipItemIdByDropData(cls, srcLevel=1, monsterId=0, school=0, quality=0, **kwargs):
        school = school
        equipSchool = cls.calcEquipSchool(school)
        equipType, equipSubType = cls.calcEquipType(equipSchool)
        if not quality:
            quality = cls.calcEquipQuality(monsterId, srcLevel)
        templateId = cls.calcTemplateId(equipSchool, equipType, equipSubType, quality)
        if not templateId:
            ERROR_MSG('   in genEquipItemIdByDropData, no suit equip, rematch:', srcLevel, monsterId, school)
        return templateId

    @classmethod
    def calcEquipSchool(cls, school):
        gearDropRateForOwnClass = GBGCD.datas['gearDropRateForOwnClass']['value']
        if random.uniform(0, 1) <= gearDropRateForOwnClass:
            return school
        else:
            ranSchoolList = copy.deepcopy(gameconst.ALL_SCHOOL_TYPE)
            ranSchoolList.remove(school)
            return random.choice(ranSchoolList)

    @classmethod
    def calcEquipType(cls, equipSchool):
        weight_list = GBTED.dropTypeWeightList.get(0, []) + GBTED.dropTypeWeightList[equipSchool]
        idList = []
        weightList = []
        for val in weight_list:
            if val:
                cfgId, weight = val
                idList.append(cfgId)
                weightList.append(weight)
        cfgId = utils.weightChoice(idList, weightList)[0][0]
        equipType = GBTED.datas[cfgId]['type']
        equipSubType = GBTED.datas[cfgId]['SubType']
        return equipType, equipSubType

    @classmethod
    def calcEquipQuality(cls, monsterId, srcLevel):
        dropQualityDataList = sorted(DGQWD.datas.values(), key=lambda elem:elem['ID'])
        creepMD = dataUtils.getCreepMD(monsterId)
        weight_list = [elem['Probability'](elem['weight'], elem['ID'], creepMD, srcLevel) for elem in dropQualityDataList]
        idx = utils.randomByWeight(weight_list)
        DEBUG_MSG('calcEquipQuality, weight_list:', monsterId, srcLevel, weight_list, idx)
        return dropQualityDataList[idx]['ID']

    @classmethod
    def calcTemplateId(cls, school, equipType, equipSubType, quality):
        DEBUG_MSG('calcTemplateId school:{} type:{} subType:{} quality:{}'.format(school, equipType, equipSubType, quality))
        gearTempIds = dataUtils.getGearIdsByBaseInfo(quality, (equipType, ) if equipType else (), (equipSubType, ) if equipSubType else (), school)

        levelMatchCnt = len(gearTempIds)
        if levelMatchCnt == 1:
            DEBUG_MSG('     in calcTemplateId, one level match equip:', gearTempIds)
            return gearTempIds[0]
        elif levelMatchCnt > 1:
            levelMatchWeight = [GBGBD.datas[tid]['randomWeight'] for tid in gearTempIds]
            randIdx = utils.randomByWeight(levelMatchWeight)
            DEBUG_MSG('     in calcTemplateId, level match equip:', randIdx, gearTempIds)
            return gearTempIds[randIdx]

