# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine
import utils
import gameconst
import message_Message_def as MMD
import gearEnhance_setEffect as GESED
import actionContext
import userType
import itemFactory
import gameengine
import dataUtils
import affix_affix as AFAFD
import inscription_inscription as ININD

class BodyEquips(userType.UserSoleType):
    EQUIPS_LOCK_TIME = 5
    def __init__(self):
        self.equips_map ={}
        self.lockedTime = 0
        self.lockedDesp = ''
        self.lockData = {}
        self._resetSetInfo()
        self.addSkillLvDic = {}
        # 技能ID-->铭文效果列表
        self.inscriptionEffect = {}

    def _lateReload(self):
        super(BodyEquips, self)._lateReload()

        for v in self.equips_map.values():
            v.reloadScript()

        for v in self.lockData.values():
            if 'equipItem' in v and v['equipItem']:
                v['equipItem'].reloadScript()
        return

    def onBodyEquipsDailyUpdate(self, owner):
        updateSlotIds = []
        for slotId, equipItem in self.equips_map.items():
            if equipItem.onItemDailyUpdate():
                updateSlotIds.append(slotId)
        updateSlotIds and owner.client.onBodyEquipDailyUpdate(updateSlotIds)

    def initObjFromSavedDict(self, dataDic):
        for equipDic in dataDic['bodyEquipList']:
            try:
                equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipDic)
                self.loadEquipItem(equipDic['gridId'], equipItem)
            except Exception as e:
                ERROR_MSG('ERRRRRRRRROR!!! in initObjFromSavedDict:', e, equipDic)
                continue
        self.lockedTime = dataDic.get('lockedTime', 0)
        self.lockedDesp = dataDic.get('lockedDesp', '')
        self.lockData = dataDic.get('lockData', {})
        self.setInfo = dataDic.get('setInfo', {})
        self.addSkillLvDic = dataDic.get('addSkillLvDic', {})
        self.inscriptionEffect = dataDic.get('inscriptionEffect', {})
        if not self.setInfo:
            self._resetSetInfo()

    def _resetSetInfo(self):
        self.setInfo = {'setLv': 0, 'propVal': {}, 'equips': []}

    def toBodyEquipsSavedDict(self):
        bodyEquipList = []
        for slotId, equipObj in self.equips_map.items():
            equipDic = equipObj.toItemSavedDict()
            equipDic['gridId'] = slotId
            bodyEquipList.append(equipDic)
        return {
                    'bodyEquipList':bodyEquipList,
                    'lockedTime':self.lockedTime,
                    'lockedDesp':self.lockedDesp,
                    'lockData':self.lockData,
                    'setInfo':self.setInfo,
                    'addSkillLvDic':self.addSkillLvDic,
                    'inscriptionEffect':self.inscriptionEffect,
                }

    def toBodyEquipsClientDict(self):
        bodyEquipList = []
        for slotId, equipObj in self.equips_map.items():
            try:
                equipDic = equipObj.toClientBodyEquipItemDict(slotId)
                bodyEquipList.append(equipDic)
            except Exception as e:
                ERROR_MSG('ERRRRRRRRROR!!! in toBodyEquipsSavedDict:', slotId, e)
                continue
        return bodyEquipList

    def getBodyEquipScoreDic(self):
        slotDressDic = {}
        for slotId, equipObj in self.equips_map.items():
            slotDressDic[slotId] = {
                'itemId':equipObj.itemId,
                'score':equipObj.getEquipScore(),
            }
        return slotDressDic

    def removeBodyEquipsProps(self, owner):
        for slotId, equipItem in self.equips_map.items():
            equipItem.removeEquipEffectToAvatar(owner)
        self.addSkillLvDic = {}
        return

    def loadEquipItem(self, slotId, equipItem):
        DEBUG_MSG("BodyEquips-->loadEquipItem, begin~")
        self.equips_map[slotId] = equipItem
        DEBUG_MSG("BodyEquips-->loadEquipItem, end~")
    
    def hasEquip(self):
        return bool(self.equips_map)

    def applyBodyEquipsProps(self, owner, isLogin=False):
        self.addSkillLvDic = {}
        for slotId, equipItem in self.equips_map.items():
            equipItem.applyEquipEffectToAvatar(owner, isLogin=isLogin)
        self.doRecalculateInscriptionEffects(owner)
        
        return

    def tryLockBodyEquips(self, desp=''):
        if self.isBodyEquipsBeLocked():
            WARNING_MSG('   tryLockBodyEquips failed:', self.lockedDesp)
            return False
        DEBUG_MSG('tryLockBodyEquips:', desp)
        self.lockedTime = utils.getNow() + self.EQUIPS_LOCK_TIME
        self.lockedDesp = desp
        return True

    def getBodyEquipByUniqueId(self, uniqueId):
        for slotId, equipItem in self.equips_map.items():
            if equipItem.uniqueId != uniqueId:
                continue
            return slotId, equipItem
        return None, None

    def isBodyEquipsBeLocked(self):
        return self.lockedTime > utils.getNow()

    def doUnlockBodyEquips(self):
        DEBUG_MSG('doUnlockBodyEquips')
        self.lockedTime = 0
        self.lockedDesp= ''

    def getSetEffectScore(self):
        setLv = self.setInfo.get('setLv', 0)
        return GESED.datas.get(setLv, {}).get('score', 0)

    def calcAllEnhanceLvRate(self):
        DEBUG_MSG("calcAllEnhanceLvRate")
        enhanceAllLvRate = 0
        for _, equipObj in self.equips_map.items():
            enhanceAllLvRate += equipObj.equipAttr.enhanceLvSumValue

        return enhanceAllLvRate

    def _doSetAction(self, owner, newSetlv, onLoing=False):
        DEBUG_MSG('in _addSetEffect:', newSetlv, onLoing)
        if newSetlv == 0:
            return
        action = GESED.datas[newSetlv]['action']
        if not action:
            return
        action(owner, None, actionContext.EquipSetActionCtx(self, newSetlv))
        if onLoing:
            #call client or send msg
            pass
        return

    def _removeSetEffect(self, owner, oldSetLv):
        DEBUG_MSG('in _removeSetEffect:', self.setInfo)
        if oldSetLv == 0:
            return
        for attrName, val in self.setInfo['propVal'].items():
            owner.addProp(attrName, -1*val, gameconst.SourceType.Equip)
        self.setInfo = {'setLv':0, 'propVal':{}}
        return

    def addPropBySet(self, owner, propList, valList, startIdx=0, endIdx=-1):
        DEBUG_MSG('in addPropBySet:', propList, valList)
        valsNum = len(valList)
        if endIdx >= valsNum:
            gameengine.reportCritical('addPropBySet, param error:', startIdx, endIdx, valList)
            return

        for idx, attrName in enumerate(propList):
            self.setInfo['propVal'].setdefault(attrName, 0)
            valueIdx = startIdx+idx
            if endIdx == -1:
                val = valList[valueIdx] if valueIdx < valsNum else valList[endIdx]
            else:
                val = valList[valueIdx] if valueIdx < endIdx else valList[endIdx]

            self.setInfo['propVal'][attrName] += val
            owner.addProp(attrName, val, gameconst.SourceType.Equip)
        DEBUG_MSG('     in addPropBySet, after:', self.setInfo)
        return

    def getDressSlotInfo(self, bagEquipItem, dstSlotId=0):
        equipType, equipSubType = bagEquipItem.equipAttr.equipType, bagEquipItem.equipAttr.equipSubType
        slotIds = dataUtils.equipSlot(equipType, equipSubType)
        if len(slotIds) == 0:
            return None, None

        emptySlotId = None
        for slotId in slotIds:
            if slotId not in self.equips_map:
                emptySlotId = slotId
                break

        if emptySlotId is None:
            #替换
            if dataUtils.isRing(equipType, equipSubType):
                if dstSlotId in slotIds:
                    realSlotId = dstSlotId
                else:
                    realSlotId = self.getRingReplaceSlotId()
            elif dataUtils.isBracelet(equipType, equipSubType):
                if dstSlotId in slotIds:
                    realSlotId = dstSlotId
                else:
                    realSlotId = self.getBraceletReplaceSlotId()
            else:
                realSlotId = slotIds[0]
            oldBodyEquip = self.getEquipItem(realSlotId)
        else:
            #有空位
            realSlotId = emptySlotId
            oldBodyEquip = None
        return realSlotId, oldBodyEquip

    def getRingReplaceSlotId(self):
        leftRing = self.getEquipItem(gameconst.BodyEquipSlot.EQUIP_RING_LEFT_SLOT)
        if not leftRing:
            return gameconst.BodyEquipSlot.EQUIP_RING_LEFT_SLOT

        rightRing = self.getEquipItem(gameconst.BodyEquipSlot.EQUIP_RING_RIGHT_SLOT)
        if not leftRing:
            return gameconst.BodyEquipSlot.EQUIP_RING_RIGHT_SLOT

        if leftRing.getEquipScore() < rightRing.getEquipScore():
            return gameconst.BodyEquipSlot.EQUIP_RING_LEFT_SLOT
        else:
            return gameconst.BodyEquipSlot.EQUIP_RING_RIGHT_SLOT

    def getBraceletReplaceSlotId(self):
        leftBracelet = self.getEquipItem(gameconst.BodyEquipSlot.EQUIP_BRACELET_LEFT_SLOT)
        if not leftBracelet:
            return gameconst.BodyEquipSlot.EQUIP_BRACELET_LEFT_SLOT

        rightBracelet = self.getEquipItem(gameconst.BodyEquipSlot.EQUIP_BRACELET_RIGHT_SLOT)
        if not leftBracelet:
            return gameconst.BodyEquipSlot.EQUIP_BRACELET_RIGHT_SLOT

        if leftBracelet.getEquipScore() < rightBracelet.getEquipScore():
            return gameconst.BodyEquipSlot.EQUIP_BRACELET_LEFT_SLOT
        else:
            return gameconst.BodyEquipSlot.EQUIP_BRACELET_RIGHT_SLOT

    def dressEquip(self, owner, slotId, bagEquipItem):
        # bagEquipItem.setItemBind()
        self.addEquipItem(owner, slotId, bagEquipItem)
        bagEquipItem.applyEquipEffectToAvatar(owner)
        owner.updateEquipmentScore()
        owner.appearance.setEquip(owner, slotId, bagEquipItem.itemId)

    def doBodyUndressEquip(self, owner, slotId):
        DEBUG_MSG('in doBodyUndressEquip, slotId:', slotId)
        equipItem = self.removeEquipItem(owner, slotId)
        if not equipItem:
            ERROR_MSG(' in doBodyUndressEquip, data err, no equip:', slotId)
            return

        equipItem.removeEquipEffectToAvatar(owner)
        owner.appearance.setEquip(owner, slotId, 0)
        owner.updateEquipmentScore()
        owner.client.onUndressEquipment(slotId)
        return equipItem

    def getEquipItem(self, slotId):
        return self.equips_map.get(slotId, None)

    def removeEquipItem(self, owner, slotId):
        equipItem = self.equips_map.pop(slotId, None)
        if not equipItem:
            return equipItem
        DEBUG_MSG("BodyEquips-->removeEquipItem, begin~ ", slotId, self.equips_map)
        self.recalculateAllInscriptionEffects(owner, equipItem.equipAttr.glyphAffixes)
        DEBUG_MSG("BodyEquips-->removeEquipItem, end~", slotId, self.equips_map)
        return equipItem
    
    def addEquipItem(self, owner, slotId, equipItem):
        DEBUG_MSG("BodyEquips-->addEquipItem, begin~")
        self.equips_map[slotId] = equipItem
        self.calculateInscriptionEffects(owner, equipItem)
        DEBUG_MSG("BodyEquips-->addEquipItem, end~")

    def recalculateAllInscriptionEffects(self, owner, oldAffixes = None, newAffixes = None):
        DEBUG_MSG("BodyEquips-->recalculateAllInscriptionEffects, begin~ ", oldAffixes, newAffixes)
        if oldAffixes is not None:
            for removeAffixID in oldAffixes:
                DEBUG_MSG("BodyEquips-->recalculateAllInscriptionEffects 1 ", removeAffixID)
                skillID, effectDatas = self.getAffixInscriptionEffectDatas(removeAffixID)
                if skillID is None or effectDatas is None:
                    continue
                DEBUG_MSG("BodyEquips-->recalculateAllInscriptionEffects, before:", self.inscriptionEffect)
                for effectData in effectDatas:
                    DEBUG_MSG("BodyEquips-->recalculateAllInscriptionEffects 2 ", effectData)
                    effectType, effectValue = effectData
                    # 替换技能直接生效
                    if effectType == gameconst.InscriptionEffectType.REPLACE_SKILL:
                        # 反向替换技能直接生效
                        owner.changeSkill(None, None, effectValue, skillID)
                    elif effectType == gameconst.InscriptionEffectType.SKILL_LEVEL_INCREASE_VALUE:
                        # 移除技能等级值
                        self.addSkillLv(self, owner, [skillID], [-1*effectValue], isLogin=False)
                        
                DEBUG_MSG("BodyEquips-->recalculateAllInscriptionEffects, end:", self.inscriptionEffect)
                    
        # 筛选出技能替换相关的记录
        self.inscriptionEffect = {}
        self.doRecalculateInscriptionEffects(owner)
        DEBUG_MSG("BodyEquips-->recalculateAllInscriptionEffects, end~")

    def doRecalculateInscriptionEffects(self, owner):
        for equipItem in self.equips_map.values():
            self.calculateInscriptionEffects(owner, equipItem)

    def calculateInscriptionEffects(self, owner, equipItem):
        DEBUG_MSG("BodyEquips-->calculateInscriptionDatas ", equipItem)
        insciptionDatas = equipItem.equipAttr.glyphAffixes
        for insciptionData in insciptionDatas:
            skillID, effectDatas = self.getAffixInscriptionEffectDatas(insciptionData.afxId)
            if skillID is None or effectDatas is None:
                continue
            DEBUG_MSG("BodyEquips-->calculateInscriptionDatas, before:", self.inscriptionEffect)
            for effectData in effectDatas:
                effectType, effectValue = effectData
                # 替换技能直接生效
                if effectType == gameconst.InscriptionEffectType.REPLACE_SKILL:
                    # 替换技能直接生效
                    owner.changeSkill(None, None, skillID, effectValue)
                elif effectType == gameconst.InscriptionEffectType.SKILL_LEVEL_INCREASE_VALUE:
                    # 增加技能等级值
                    self.addSkillLv(self, owner, [skillID], [effectValue], isLogin=False)
                effectRecord = self.inscriptionEffect.get(skillID)
                if not effectRecord:
                    effectRecord = {}
                    self.inscriptionEffect[skillID] = effectRecord
                effectRecord[effectType] = effectRecord.get(effectType, 0) + effectValue
                DEBUG_MSG("BodyEquips-->calculateInscriptionDatas, skillID:{}, effectType:{}, effectValu:{}", skillID, effectType, effectValue)
            DEBUG_MSG("BodyEquips-->calculateInscriptionDatas, after:", self.inscriptionEffect)

    def calculateEffectDatas(self, effectType):
        replaceSkills = {}
        for skillID, effectDatas in self.inscriptionEffect.items():
            for effectType, effectValue in effectDatas.items():
                if effectType == gameconst.InscriptionEffectType.REPLACE_SKILL:
                    replaceSkills[skillID] = effectValue
        return replaceSkills
    
    def getAffixInscriptionEffectDatas(self, affixID):
        affixData = AFAFD.datas.get(affixID)
        if not affixData:
            ERROR_MSG('BodyEquips-->getAffixInscriptionEffectDatas, missing affix data ', affixID)
            return None, None
        if affixData['event'] != 'onDress':
            return None, None
        ininData = ININD.datas.get(affixData['inscription'])
        if not ininData:
            WARNING_MSG('BodyEquips-->getAffixInscriptionEffectDatas, missing inscription data ', affixData['inscription'])
            return None, None
        effecDatas = ininData['effect_value']
        if not effecDatas:
            WARNING_MSG('BodyEquips-->getAffixInscriptionEffectDatas, missing effect data ', effecDatas, affixData['inscription'])
            return None, None
        skillID = ininData['skill_id']
        return skillID, effecDatas

    def getEquipsAddSkillLv(self, skillId):
        return self.addSkillLvDic.get(skillId, 0) + self.addSkillLvDic.get(gameconst.ClassSkillID, 0)

    def addSkillLv(self, owner, skillIdList, addLvList, isLogin=False):
        DEBUG_MSG('in bodyEquips:addSkillLv:', skillIdList, addLvList, self.addSkillLvDic)
        newSkillLv = []
        for skillId, addLv in zip(skillIdList, addLvList):
            self.addSkillLvDic[skillId] = self.addSkillLvDic.get(skillId, 0) + addLv
            if self.addSkillLvDic[skillId] < 0:
                gameengine.reportCritical('ERROR!!addSkillLv:', self.addSkillLvDic, skillId, addLv)
                self.addSkillLvDic[skillId] = 0
            newSkillLv.append(self.addSkillLvDic[skillId])
        if not isLogin:
            owner.client.updateSkillsExtraLevel(gameconst.SkillUpdateSrc.Equip, skillIdList, newSkillLv)
        return

    def getSkillInciptionEffect(self, skillID, effectType):
        effectData = self.inscriptionEffect.get(skillID)
        if not effectData:
            return 0
        return effectData.get(effectType, 0)
    
    def getInscriptionEffects(self, skillID, effectType):
        args = []
        return False, args