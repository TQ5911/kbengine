# -*- encoding:utf-8 -*-

from KBEDebug import *
import itertools
import utils
import gameconst
import userType
import itemFactory
import gameengine
import dataUtils
import gearEnhance_blessEffect as GEBE

class BodyEquips(userType.UserSoleType):
    EQUIPS_LOCK_TIME = 5
    def __init__(self):
        self.equips_map ={}
        self.lockedTime = 0
        self.lockedDesp = ''
        self.lockData = {}
        self._resetSetInfo()
        self.addSkillLvDic = {}
        self.blessAttrs = {}

    def _lateReload(self):
        super(BodyEquips, self)._lateReload()

        for v in self.equips_map.values():
            v.reloadScript()

        for v in self.lockData.values():
            if 'equipItem' in v and v['equipItem']:
                v['equipItem'].reloadScript()
        return

    @classmethod
    def _checkIgnores_(cls):
        return 'lockedTime', 'lockedDesp'
    
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
                if equipItem:
                    self.loadEquipItem(equipDic['gridId'], equipItem)
                else:
                    WARNING_MSG('equipment template id is missing', equipDic)
            except Exception as e:
                ERROR_MSG('ERRRRRRRRROR!!! in initObjFromSavedDict:', e, equipDic)
                continue
        self.lockData = dataDic.get('lockData', {})
        self.setInfo = dataDic.get('setInfo', {})
        self.addSkillLvDic = dataDic.get('addSkillLvDic', {})
        self.blessAttrs = dataDic.get('blessAttrs', {})
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
                    'lockData':self.lockData,
                    'setInfo':self.setInfo,
                    'addSkillLvDic':self.addSkillLvDic,
                    'blessAttrs':self.blessAttrs,
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

    def loadEquipItem(self, slotId, equipItem):
        self.equips_map[slotId] = equipItem
    
    def hasEquip(self):
        return bool(self.equips_map)

    def applyBodyEquipsProps(self, owner, isLogin=False):
        INFO_MSG("BodyEquips-->applyBodyEquipsProps, begin~ islogin:", isLogin)
        self.addSkillLvDic = {}
        for slotId, equipItem in self.equips_map.items():
            equipItem.applyEquipEffectToAvatar(owner, isLogin=isLogin)
        self.modifyAvatarAttrs(owner, 1)
        INFO_MSG("BodyEquips-->applyBodyEquipsProps, end~ ")

    def tryLockBodyEquips(self, desp=''):
        if self.isBodyEquipsBeLocked():
            WARNING_MSG('   tryLockBodyEquips failed:', self.lockedDesp)
            return False
        INFO_MSG('tryLockBodyEquips:', desp)
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
        INFO_MSG('doUnlockBodyEquips')
        self.lockedTime = 0
        self.lockedDesp= ''

    def _removeSetEffect(self, owner, oldSetLv):
        INFO_MSG('in _removeSetEffect:', self.setInfo)
        if oldSetLv == 0:
            return
        for attrName, val in self.setInfo['propVal'].items():
            owner.addProp(attrName, -1*val, gameconst.SourceType.Equip)
        self.setInfo = {'setLv':0, 'propVal':{}}
        return

    def addPropBySet(self, owner, propList, valList, startIdx=0, endIdx=-1):
        INFO_MSG('in addPropBySet:', propList, valList)
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
        INFO_MSG('     in addPropBySet, after:', self.setInfo)
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
        owner.appearance.setEquip(owner, slotId, bagEquipItem.itemId)
        self.changeAvatarAttrs(owner)
        owner.updateEquipmentScore()

    def doBodyUndressEquip(self, owner, slotId):
        INFO_MSG('in doBodyUndressEquip, slotId:', slotId)
        equipItem = self.removeEquipItem(owner, slotId)
        if not equipItem:
            ERROR_MSG(' in doBodyUndressEquip, data err, no equip:', slotId)
            return

        equipItem.removeEquipEffectToAvatar(owner)
        owner.appearance.setEquip(owner, slotId, 0)
        self.changeAvatarAttrs(owner)
        owner.updateEquipmentScore()
        owner.client.onUndressEquipment(slotId)
        return equipItem
    
    def changeAvatarAttrs(self, owner):
        INFO_MSG('in _changeAvatarAttrs')
        # 先移除
        self.modifyAvatarAttrs(owner, -1)
        # 重新计算
        totalAffixVal = self.calcAllBlessVal()
        newAttrs = self.calculateBlessAttrs(totalAffixVal)
        self.blessAttrs = newAttrs if newAttrs else {}
        # 再加回来
        self.modifyAvatarAttrs(owner, 1)
    
    def modifyAvatarAttrs(self, owner, factor):
        for attrName, attrValue in itertools.chain.from_iterable([self.blessAttrs.items()]):
            attrValue *= factor
            owner.addProp(attrName, attrValue, gameconst.SourceType.Equip)

    def getAllEquipItems(self):
        return self.equips_map
    
    def getEquipItem(self, slotId):
        return self.equips_map.get(slotId, None)

    def removeEquipItem(self, owner, slotId):
        equipItem = self.equips_map.pop(slotId, None)
        if not equipItem:
            return equipItem
        INFO_MSG("BodyEquips-->removeEquipItem, begin~ ", slotId, self.equips_map)
        self.recalculateAllInscriptionEffects(owner)
        INFO_MSG("BodyEquips-->removeEquipItem, end~", slotId, self.equips_map)
        return equipItem
    
    def addEquipItem(self, owner, slotId, equipItem):
        INFO_MSG("BodyEquips-->addEquipItem, begin~")
        self.equips_map[slotId] = equipItem
        self.recalculateAllInscriptionEffects(owner)
        INFO_MSG("BodyEquips-->addEquipItem, end~")

    def recalculateAllInscriptionEffects(self, owner):
        INFO_MSG("recalculateAllInscriptionEffects")
        owner.glyphEquipData.cleanInscriptionEffects(owner)
        for equipItem in self.equips_map.values():
            owner.glyphEquipData.calculateAllInscriptionEffects(owner, equipItem.getGlyphAffixes())
        owner.glyphEquipData.applyInscriptionEffects(owner)

    def getEquipsAddSkillLv(self, owner, skillId):
        inscriptionAddLevel = 0
        ret, args = owner.glyphEquipData.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SKILL_LEVEL_INCREASE_VALUE)
        if ret:
            inscriptionAddLevel = args[0]
        return self.addSkillLvDic.get(skillId, 0) + self.addSkillLvDic.get(gameconst.ClassSkillID, 0) + inscriptionAddLevel

    def addSkillLv(self, owner, skillIdList, addLvList, isLogin=False):
        INFO_MSG('in bodyEquips:addSkillLv:', skillIdList, addLvList, self.addSkillLvDic)
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
    
    def calculateBlessAttrs(self, totalAffixVal):
        blessAttrs = None
        cfg = GEBE.datas.get(totalAffixVal, 0)
        if not cfg:
            return blessAttrs
        
        attrs = cfg['effect']
        if not attrs:
            return blessAttrs
        
        for attr in attrs:
            if blessAttrs is None:
                blessAttrs = {}
            attrName, attrValue = attr
            blessAttrs[attrName] = attrValue
        return blessAttrs
    
    def calcAllBlessVal(self):
        allBlessVal = 0
        for equipItem in self.equips_map.values():
            allBlessVal += equipItem.getBlessVal()
        return allBlessVal    
