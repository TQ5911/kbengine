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

class BodyEquips(userType.UserSingleType):
    EQUIPS_LOCK_TIME = 5
    def __init__(self):
        self.equips_map ={}
        self.lockedTime = 0
        self.lockedDesp = ''
        self.lockData = {}
        self._resetSetInfo()
        self.addSkillLvDic = {}
        self.blessAttrs = {}
        self.waitExpireEquipList = {}

    def _lateReload(self):
        super(BodyEquips, self)._lateReload()

        for _v in self.equips_map.values():
            _v.reloadScript()

        for _v in self.lockData.values():
            if 'equipItem' in _v and _v['equipItem']:
                _v['equipItem'].reloadScript()

        for _v in self.waitExpireEquipList.values():
            _v.reloadScript()

    @classmethod
    def _checkIgnores_(cls):
        return 'lockedTime', 'lockedDesp'
    
    def onBodyEquipsDailyUpdate(self, owner):
        _updateSlotIds = []
        for slotId, equipItem in self.equips_map.items():
            if equipItem.onItemDailyUpdate():
                _updateSlotIds.append(slotId)
        if _updateSlotIds:
            owner.client.onBodyEquipDailyUpdate(_updateSlotIds)

    def initObjFromSavedDict(self, dataDic):
        for equipDic in dataDic['bodyEquipList']:
            try:
                equipItem = itemFactory.ItemFactory.createItemWithSavedDict(equipDic)
                if equipItem:
                    self.loadEquipItem(equipDic['gridId'], equipItem)
                else:
                    LOG_WARN('equipment template id is missing', equipDic)
            except Exception as e:
                LOG_ERR('ERRRRRRRRROR!!! in initObjFromSavedDict:', e, equipDic)
                continue
        self.setInfo = dataDic.get('setInfo', {})
        self.lockData = dataDic.get('lockData', {})
        self.addSkillLvDic = dataDic.get('addSkillLvDic', {})
        self.blessAttrs = dataDic.get('blessAttrs', {})
        if not self.setInfo:
            self._resetSetInfo()

        for equipItem in self.equips_map.values():
            if equipItem.getOwnerGbId() > 0:
                self.waitExpireEquipList[equipItem.uniqueId] = equipItem

    def _resetSetInfo(self):
        self.setInfo = {
            'setLv': 0, 
            'propVal': {}, 
            'equips': [],
        }

    def toBodyEquipsSavedDict(self):
        _bodyEquipList = []
        for slotId, equipObj in self.equips_map.items():
            equipDic = equipObj.toItemSavedDict()
            equipDic['gridId'] = slotId
            _bodyEquipList.append(equipDic)
        return {
            'bodyEquipList':_bodyEquipList,
            'lockData':self.lockData,
            'setInfo':self.setInfo,
            'addSkillLvDic':self.addSkillLvDic,
            'blessAttrs':self.blessAttrs,
        }

    def toBodyEquipsClientDict(self):
        _bodyEquipList = []
        for slotId, equipObj in self.equips_map.items():
            try:
                equipDic = equipObj.toClientBodyEquipItemDict(slotId)
                _bodyEquipList.append(equipDic)
            except Exception as e:
                LOG_ERR('ERRRRRRRRROR!!! in toBodyEquipsSavedDict:', slotId, e)
                continue
        return _bodyEquipList

    def getBodyEquipScoreDic(self):
        _slotDressDic = {}
        for slotId, equipObj in self.equips_map.items():
            _slotDressDic[slotId] = {
                'itemId':equipObj.itemId,
                'score':equipObj.getEquipScore(),
            }
        return _slotDressDic

    def loadEquipItem(self, slotId, equipItem):
        self.equips_map[slotId] = equipItem
    
    def hasEquip(self):
        return bool(self.equips_map)

    def applyBodyEquipsProps(self, owner, isLogin=False):
        LOG_INFO("BodyEquips-->applyBodyEquipsProps, begin~ islogin:", isLogin)
        self.addSkillLvDic = {}
        for slotId, equipItem in self.equips_map.items():
            equipItem.applyEquipEffectToAvatar(owner, isLogin=isLogin)
        self.modifyAvatarAttrs(owner, 1)
        LOG_INFO("BodyEquips-->applyBodyEquipsProps, end~ ")

    def tryLockBodyEquips(self, desp=''):
        if self.isBodyEquipsBeLocked():
            LOG_WARN('   tryLockBodyEquips failed:', self.lockedDesp)
            return False
        LOG_INFO('tryLockBodyEquips:', desp)
        self.lockedTime = utils.curTS() + self.EQUIPS_LOCK_TIME
        self.lockedDesp = desp
        return True

    def getBodyEquipByUniqueId(self, uniqueId):
        for _slotId, equipItem in self.equips_map.items():
            if equipItem.uniqueId != uniqueId:
                continue
            return _slotId, equipItem
        return None, None

    def isBodyEquipsBeLocked(self):
        return self.lockedTime > utils.curTS()

    def doUnlockBodyEquips(self):
        LOG_INFO('doUnlockBodyEquips')
        self.lockedTime = 0
        self.lockedDesp= ''

    def _removeSetEffect(self, owner, oldSetLv):
        LOG_INFO('in _removeSetEffect:', self.setInfo)
        if oldSetLv == 0:
            return
        for _attrName, val in self.setInfo['propVal'].items():
            owner.addProp(_attrName, -1*val, gameconst.SourceType.SrcTpEquip)
        self.setInfo = {'setLv':0, 'propVal':{}}

    def addPropBySet(self, owner, propList, valList, startIdx=0, endIdx=-1):
        LOG_INFO('in addPropBySet:', propList, valList)
        valsNum = len(valList)
        if endIdx >= valsNum:
            gameengine.panicStack('addPropBySet, param error:', startIdx, endIdx, valList)
            return

        for idx, _attrName in enumerate(propList):
            self.setInfo['propVal'].setdefault(_attrName, 0)
            _valueIdx = startIdx+idx
            if endIdx == -1:
                val = valList[_valueIdx] if _valueIdx < valsNum else valList[endIdx]
            else:
                val = valList[_valueIdx] if _valueIdx < endIdx else valList[endIdx]

            self.setInfo['propVal'][_attrName] += val
            owner.addProp(_attrName, val, gameconst.SourceType.SrcTpEquip)
        LOG_INFO('     in addPropBySet, after:', self.setInfo)

    def getDressSlotInfo(self, bagEquipItem, dstSlotId=0):
        _equipType, equipSubType = bagEquipItem.equipAttr.equipType, bagEquipItem.equipAttr.equipSubType
        slotIds = dataUtils.equipSlot(_equipType, equipSubType)
        if len(slotIds) == 0:
            return None, None

        _emptySlotId = None
        for slotId in slotIds:
            if slotId not in self.equips_map:
                _emptySlotId = slotId
                break

        if _emptySlotId is None:
            #替换
            if dataUtils.isRing(_equipType, equipSubType):
                if dstSlotId in slotIds:
                    realSlotId = dstSlotId
                else:
                    realSlotId = self.getRingReplaceSlotId()
            elif dataUtils.isBracelet(_equipType, equipSubType):
                if dstSlotId in slotIds:
                    realSlotId = dstSlotId
                else:
                    realSlotId = self.getBraceletReplaceSlotId()
            else:
                realSlotId = slotIds[0]
            oldBodyEquip = self.getEquipItem(realSlotId)
        else:
            #有空位
            realSlotId = _emptySlotId
            oldBodyEquip = None
        return realSlotId, oldBodyEquip

    def getRingReplaceSlotId(self):
        _leftRing = self.getEquipItem(gameconst.BodyEquipSlot.EQUIP_RING_LEFT_SLOT)
        if not _leftRing:
            return gameconst.BodyEquipSlot.EQUIP_RING_LEFT_SLOT

        rightRing = self.getEquipItem(gameconst.BodyEquipSlot.EQUIP_RING_RIGHT_SLOT)
        if not _leftRing:
            return gameconst.BodyEquipSlot.EQUIP_RING_RIGHT_SLOT

        if _leftRing.getEquipScore() < rightRing.getEquipScore():
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
        owner.appearance.setEquip(owner, slotId, bagEquipItem.itemId, bagEquipItem.getGrade())
        self.changeAvatarAttrs(owner)
        owner.updateEquipmentScore()
        owner.updateEquipQualityAchievement()
        if bagEquipItem.getOwnerGbId() > 0:
            self.waitExpireEquipList[bagEquipItem.uniqueId] = bagEquipItem

    def updateEquipDressAppearance(self, owner, uniqueId):
        slotId, equipItem = self.getEquipItemByUniqueId(uniqueId)
        if equipItem:
            owner.appearance.setEquip(owner, slotId, equipItem.itemId, equipItem.getGrade())

    def doBodyUndressEquip(self, owner, slotId):
        LOG_INFO('in doBodyUndressEquip, slotId:', slotId)
        equipItem = self.removeEquipItem(owner, slotId)
        if not equipItem:
            LOG_ERR(' in doBodyUndressEquip, data err, no equip:', slotId)
            return

        equipItem.removeEquipEffectToAvatar(owner)
        owner.appearance.setEquip(owner, slotId, 0, 0)
        self.changeAvatarAttrs(owner)
        owner.updateEquipmentScore()
        self.waitExpireEquipList.pop(equipItem.uniqueId, None)
        owner.client.onUndressEquipment(slotId)
        return equipItem
    
    def changeAvatarAttrs(self, owner):
        LOG_INFO('in _changeAvatarAttrs')
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
            owner.addProp(attrName, attrValue, gameconst.SourceType.SrcTpEquip)

    def getAllEquipItems(self):
        return self.equips_map
    
    def getEquipItem(self, slotId):
        return self.equips_map.get(slotId, None)

    def getEquipItemByUniqueId(self, uniqueId):
        slotId = None
        equipItem = None
        for k, v in self.equips_map.items():
            if v.uniqueId == uniqueId:
                slotId = k
                equipItem = v
                break
        return slotId, equipItem

    def removeEquipItem(self, owner, slotId):
        equipItem = self.equips_map.pop(slotId, None)
        if not equipItem:
            return equipItem
        LOG_INFO(" BodyEquips-->removeEquipItem, begin~ ", slotId, self.equips_map)
        self.recalculateAllInscriptionEffects(owner)
        LOG_INFO("BodyEquips-->removeEquipItem, end~", slotId, self.equips_map)
        return equipItem
    
    def addEquipItem(self, owner, slotId, equipItem):
        LOG_INFO("BodyEquips-->addEquipItem, begin~")
        self.equips_map[slotId] = equipItem
        self.recalculateAllInscriptionEffects(owner)
        LOG_INFO("BodyEquips-->addEquipItem, end~")

    def getDressedQualityDatas(self, excludeSlotId):
        qualityData = {}
        for slotId, equipObj in self.equips_map.items():
            if slotId == excludeSlotId:
                continue
            quality = equipObj.getQuality()
            qualityData[quality] = qualityData.get(quality, 0) + 1
        return qualityData

    def recalculateAllInscriptionEffects(self, owner):
        LOG_INFO("recalculateAllInscriptionEffects")
        changedInfo = {}
        owner.glyphEquipData.cleanInscriptionEffects(owner)
        for equipItem in self.equips_map.values():
            owner.glyphEquipData.calculateAllInscriptionEffects(owner, changedInfo, equipItem.uniqueId, equipItem.getGlyphGroupId(), equipItem.getGlyphAffixes())
        owner.glyphEquipData.applyInscriptionEffects(owner)
        datas = []
        for uniqueId, changeData in changedInfo.items():
            data = {
                'uniqueId': uniqueId,
                'groupId': changeData[0],
                'status': changeData[1:],
            }
            datas.append(data)
        LOG_INFO("recalculateAllInscriptionEffects : ", datas)
        owner.client.onEquipGlyphStatusChange(datas)

    def getEquipsAddSkillLv(self, owner, skillId):
        inscriptionAddLevel = 0
        ret, args = owner.glyphEquipData.getInscriptionEffects(skillId, gameconst.InscriptionEffectType.SKILL_LEVEL_INCREASE_VALUE)
        if ret:
            inscriptionAddLevel = args[0]
        return self.addSkillLvDic.get(skillId, 0) + self.addSkillLvDic.get(gameconst.ClassSkillID, 0) + inscriptionAddLevel

    def addSkillLv(self, owner, skillIdList, addLvList, isLogin=False):
        LOG_INFO('in bodyEquips:addSkillLv:', skillIdList, addLvList, self.addSkillLvDic)
        _newSkillLv = []
        for skillId, _addLv in zip(skillIdList, addLvList):
            self.addSkillLvDic[skillId] = self.addSkillLvDic.get(skillId, 0) + _addLv
            if self.addSkillLvDic[skillId] < 0:
                gameengine.panicStack('ERROR!!addSkillLv:', self.addSkillLvDic, skillId, _addLv)
                self.addSkillLvDic[skillId] = 0
            _newSkillLv.append(self.addSkillLvDic[skillId])
        if not isLogin:
            owner.client.updateSkillsExtraLevel(gameconst.SkillUpdateSrc.Equip, skillIdList, _newSkillLv)
    
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
    
    def checkEquipExpire(self, owner):
        expiredEquipUniqueIds = []
        curTime = utils.curTS()
        equipUniques = self.waitExpireEquipList.keys()
        for equipUnique in equipUniques:
            equipItem = self.waitExpireEquipList.get(equipUnique)
            if equipItem.getOwnerGbId() != owner.gbId:
                if curTime >= equipItem.getReturnTime():
                    expiredEquipUniqueIds.append(equipUnique)

        if len(expiredEquipUniqueIds) == 0:
            return
        
        uniqueIds = []
        slotIds = self.equips_map.keys()
        for slotId in slotIds:
            equipItem = self.equips_map.get(slotId)
            if equipItem.uniqueId in expiredEquipUniqueIds:
                uniqueIds.append(equipItem.uniqueId)

        if len(uniqueIds) > 0:
            for uniqueId in uniqueIds:
                owner.onRemoveEquipNotifyCell(uniqueId)
