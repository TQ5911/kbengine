# -*- coding: utf-8 -*-
import KBEngine
import gameconst
from KBEDebug import *
import userType
import dataUtils
import utils
import json

import mounts_mounts as MOUNTS
import gearBase_gearBase as GBGBD

def getDefaultAppearanceEquipPartId():
    return 0, 0

class FaceDataVal(userType.UserSingleType):
    def __init__(self, suitId=0, hairIdFaceId=0, hairColorIdSkinColorId=0):
        self.suitId = suitId
        self.hairIdFaceId = hairIdFaceId
        self.hairColorIdSkinColorId = hairColorIdSkinColorId

    def clone(self):
        return FaceDataVal(
            suitId=self.suitId,
            hairIdFaceId=self.hairIdFaceId,
            hairColorIdSkinColorId=self.hairColorIdSkinColorId)

    def reset(self):
        self.suitId = 0
        self.hairIdFaceId = 0
        self.hairColorIdSkinColorId = 0

    def toStreamSavedDic(self):
        return {
            'suitId': self.suitId,
            'hairIdFaceId': self.hairIdFaceId,
            'hairColorIdSkinColorId': self.hairColorIdSkinColorId,
        }

    def faceId(self):
        return self.hairIdFaceId & 0xff

    def hairId(self):
        return (self.hairIdFaceId >> 8) & 0xff

    def hairColorId(self):
        return (self.hairColorIdSkinColorId >> 8) & 0xff

    def skinColorId(self):
        return self.hairColorIdSkinColorId & 0xff

    def initFromDict(self, savedDic):
        self.suitId = savedDic['suitId']
        self.hairIdFaceId = savedDic['hairIdFaceId']
        self.hairColorIdSkinColorId = savedDic['hairColorIdSkinColorId']
        return self

    def toJsonString(self):
        return json.dumps(self.toStreamSavedDic())


class OutfitDataVal(userType.UserSingleType):
    def __init__(self, hairId=0, clothesId=0, picFrameId=0, wingId=0, mountId=0):
        self.hairId = hairId
        self.clothesId = clothesId
        self.picFrameId = picFrameId
        self.wingId = wingId
        self.mountId = mountId

    def clone(self):
        return OutfitDataVal(
            hairId=self.hairId,
            clothesId=self.clothesId,
            picFrameId=self.picFrameId,
            wingId=self.wingId,
            mountId=self.mountId)

    def toStreamSavedDic(self):
        return {
            'clothesId': self.clothesId,
            'hairId': self.hairId,
            'picFrameId': self.picFrameId,
            'wingId': self.wingId,
            'mountId': self.mountId,
        }

    def initFromDict(self, savedDic):
        self.hairId = savedDic['hairId']
        self.picFrameId = savedDic['picFrameId']
        self.clothesId = savedDic['clothesId']
        self.wingId = savedDic['wingId']
        self.mountId = savedDic['mountId']
        return self

    def toJsonString(self):
        return json.dumps(self.toStreamSavedDic())


class AvatarPhotoDataVal(userType.UserSingleType):
    def __init__(self, avatarId=0, avatarFrameId=0):
        self.avatar = avatarId
        self.avatarFrame = avatarFrameId

    def toStreamSavedDic(self):
        return {
            'avatar': self.avatar,
            'avatarFrame': self.avatarFrame,
        }

    def initFromDict(self, savedDic):
        self.avatar = savedDic['avatar']
        self.avatarFrame = savedDic['avatarFrame']
        return self

    def toJsonString(self):
        return json.dumps(self.toStreamSavedDic())

    def setDefaultData(self, avatarId, avatarFrameId):
        self.avatar = avatarId
        self.avatarFrame = avatarFrameId


class Appearance(userType.UserSingleType):
    def __init__(self, weapon=0, breast=0, outfitData=None, faceData=None):
        self.weapon = weapon
        self.breast = breast
        self.outfitData = outfitData or OutfitDataVal()
        self.faceData = faceData or FaceDataVal()
        return

    def clone(self):
        return Appearance(
            weapon=self.weapon,
            breast=self.breast,
            outfitData=self.outfitData.clone(),
            faceData=self.faceData.clone())

    def toStreamSavedDic(self):
        return {
            'weapon': self.weapon,
            'breast': self.breast,
            'outfitData': self.outfitData,
            'faceData': self.faceData,
        }

    def toJsonString(self):
        return "{\"outfitData\":" + self.outfitData.toJsonString() + "," \
            + "\"faceData\":" + self.faceData.toJsonString() + "," \
            + "\"weapon\":" + str(self.weapon) + "," \
            + "\"breast\":" + str(self.breast) + "}"

    def _lateReload(self):
        super(Appearance, self)._lateReload()
        self.outfitData.reloadScript()
        self.faceData.reloadScript()

    def initFromDict(self, savedDic):
        self.weapon = savedDic['weapon']
        self.breast = savedDic['breast']
        self.outfitData = savedDic['outfitData']
        self.faceData = savedDic['faceData']
        return self

    def updateFromAvatarAppearanceDBData(self, data, startIdx):
        LOG_DBG('updateFromAvatarAppearanceDBData:', data, startIdx)
        self.weapon = int(data[startIdx])
        self.breast = int(data[startIdx+1])
        suitId = int(data[startIdx+2])
        hairIdFaceId = int(data[startIdx+3])
        hairColorIdSkinColorId = int(data[startIdx+4])
        hairId = int(data[startIdx+5])
        clothesId = int(data[startIdx+6])
        picFrameId = int(data[startIdx+7])
        wingId = int(data[startIdx+8])
        mountId = int(data[startIdx+9])
        self.faceData = FaceDataVal(suitId=suitId, hairIdFaceId=hairIdFaceId, hairColorIdSkinColorId=hairColorIdSkinColorId)
        self.outfitData = OutfitDataVal(hairId=hairId, clothesId=clothesId, picFrameId=picFrameId, wingId=wingId, mountId=mountId)
        return

    def setEquip(self, owner, part, val, grade):
        LOG_INFO("setEquip ", part, val, grade)
        realVal = 0
        if val > 0 and grade > 0:
            appearance = GBGBD.datas.get(val, {}).get('appearance', None)
            if appearance and len(appearance) >= grade:
                realVal = appearance[grade - 1]
        if part == gameconst.BodyEquipSlot.EQUIP_WEAPON_SLOT:
            if 0 == realVal:
                realVal, _ = getDefaultAppearanceEquipPartId()
            self.weapon = realVal
            owner.allClients.onAppearanceUpdated(part, realVal)
            owner.base.updateAccountCharacterAppearance({'weapon':realVal})
        elif part == gameconst.BodyEquipSlot.EQUIP_CLOTHES_SLOT:
            if 0 == realVal:
                _, realVal = getDefaultAppearanceEquipPartId()
            self.breast = realVal
            owner.allClients.onAppearanceUpdated(part, realVal)
            owner.base.updateAccountCharacterAppearance({'breast':realVal})

    def syncAppearanceToAccount(self, owner):
        owner.base.updateAccountCharacterAppearance({
            'breast': self.breast,
            'weapon': self.weapon,
        })

    def setOutfitId(self, owner, outfitType, outfitId):
        if self.checkOutfitIdSetup(outfitType, outfitId):
            LOG_WARN("setOutfitId ", outfitId, outfitType)
            return
        if outfitType == gameconst.OutfitEnum.wing:
            self.outfitData.wingId = outfitId
        elif outfitType == gameconst.OutfitEnum.hair:
            self.outfitData.hairId = outfitId
        elif outfitType == gameconst.OutfitEnum.clothes:
            self.outfitData.clothesId = outfitId
        elif outfitType == gameconst.OutfitEnum.picFrame:
            self.outfitData.picFrameId = outfitId
        elif outfitType == gameconst.OutfitEnum.mount:
            self.outfitData.mountId = outfitId
        else:
            LOG_ERR("setOutfitId wrong type", outfitId)
            return
        owner.allClients.onAppearanceOutfitUpdated(outfitType, outfitId)

    def getOutFitId(self, school, sex, outfitType, outfitId):
        LOG_DBG("getOutFitId", school, sex, outfitType, outfitId)
        return school * 100000 + sex * 10000 + outfitType * 1000 + outfitId

    def removeOutfitById(self, owner, outfitType, outfitId):
        if not self.checkOutfitIdSetup(outfitType, outfitId):
            return
        if outfitType == gameconst.OutfitEnum.wing:
            self.outfitData.wingId = 0
            _outfitName = 'wingId'
        elif outfitType == gameconst.OutfitEnum.hair:
            self.outfitData.hairId = 0
            _outfitName = 'hairId'
        elif outfitType == gameconst.OutfitEnum.clothes:
            self.outfitData.clothesId = 0
            _outfitName = 'clothesId'
        elif outfitType == gameconst.OutfitEnum.picFrame:
            self.outfitData.picFrameId = 0
            _outfitName = 'picFrameId'
            owner.updatePicFrameId(self.outfitData.picFrameId)
        elif outfitType == gameconst.OutfitEnum.mount:
            self.outfitData.mountId = 0
            _outfitName = 'mountId'
        else:
            LOG_ERR("setOutfitId wrong type", outfitId, outfitType)
            return
        owner.allClients.onAppearanceOutfitUpdated(outfitType, 0)
        owner.base.updateAccountCharacterOutfit(_outfitName, 0)

    def checkOutfitIdSetup(self, outfitType, outfitId):
        if outfitType == gameconst.OutfitEnum.wing:
            if self.outfitData.wingId == outfitId:
                return True
        elif outfitType == gameconst.OutfitEnum.hair:
            if self.outfitData.hairId == outfitId:
                return True
        elif outfitType == gameconst.OutfitEnum.clothes:
            if self.outfitData.clothesId == outfitId:
                return True
        elif outfitType == gameconst.OutfitEnum.picFrame:
            if self.outfitData.picFrameId == outfitId:
                return True
        elif outfitType == gameconst.OutfitEnum.mount:
            if self.outfitData.mountId == outfitId:
                return True

        return False

    def removeAccountOutfitId(self, outfitType, outfitId):
        LOG_DBG("removeAccountOutfitId ", outfitType, outfitId)
        if outfitType == gameconst.OutfitEnum.wing:
            self.outfitData.wingId = 0
        elif outfitType == gameconst.OutfitEnum.hair:
            self.outfitData.hairId = 0
        elif outfitType == gameconst.OutfitEnum.clothes:
            self.outfitData.clothesId = 0
        elif outfitType == gameconst.OutfitEnum.picFrame:
            self.outfitData.picFrameId = 0
        elif outfitType == gameconst.OutfitEnum.mount:
            self.outfitData.mountId = 0
        else:
            LOG_ERR("removeAccountOutfitId wrong type", outfitId, outfitType)

    def resetOutfitData(self, outfitType, outfitId, expireTime):
        if not self.checkOutfitIdSetup(outfitType, outfitId):
            return
        if expireTime and utils.curTS() >= expireTime:
            self.removeAccountOutfitId(outfitType, outfitId)
        return True


class AvatarOutfit(userType.UserSingleType):
    def __init__(self, outfitType=0, outfitId=0, expireTime=0, isNew=True):
        self.outfitType = outfitType
        self.outfitId = outfitId
        self.expireTime = expireTime
        self.isNew = isNew

    def _lateReload(self):
        super(AvatarOutfit, self)._lateReload()

    # db -> obj
    def initFromDict(self, savedDataDict):
        self.outfitId = savedDataDict['outfitId']
        self.expireTime = savedDataDict['expireTime']
        self.outfitType = savedDataDict['outfitType']
        self.isNew = savedDataDict['isNew']

    # obj -> db
    def toStreamSavedDic(self):
        return {
            'outfitId': self.outfitId,
            'expireTime': self.expireTime,
            'outfitType': self.outfitType,
            'isNew': self.isNew,
        }

    def setExpireTime(self, expireTime):
        if not self.expireTime:
            LOG_WARN("outfit is forever", self.outfitId)
            return
        if expireTime and self.expireTime > expireTime:
            LOG_WARN("outfit is longer", self.outfitId, self.expireTime, expireTime)
            return
        self.expireTime = expireTime

    def toClientData(self):
        clientData = self.toStreamSavedDic()
        return clientData


class AvatarOutfitInfo(userType.UserSingleType):
    def __init__(self):
        self.outfitDic = {}

    def getOutfitKey(self, outfitType, outfitId):
        return str(outfitType) + str(outfitId)

    def _lateReload(self):
        super(AvatarOutfitInfo, self)._lateReload()
        for _v in self.outfitDic.values():
            _v.reloadScript()

    # db -> obj
    def initFromDict(self, savedDataDict):
        for _dataDict in savedDataDict['outfitList']:
            outfit = AvatarOutfit()
            outfit.initFromDict(_dataDict)
            self.outfitDic[self.getOutfitKey(_dataDict['outfitType'], _dataDict['outfitId'])] = outfit

    # obj -> db
    def toStreamSavedDic(self):
        _outfitList = []
        for outfit in self.outfitDic.values():
            _outfitList.append(outfit.toStreamSavedDic())
        return {'outfitList': _outfitList, }

    def toClientData(self, outfits=None):
        _outfitList = []
        if not outfits:
            for outfit in self.outfitDic.values():
                if not dataUtils.checkOpenOutfit(outfit.outfitType, outfit.outfitId):
                    continue
                _outfitList.append(outfit.toClientData())
        else:
            for _outfitType, outfitId in outfits:
                outfitKey = self.getOutfitKey(_outfitType, outfitId)
                if not dataUtils.checkOpenOutfit(_outfitType, outfitId):
                    continue
                _outfitList.append(self.outfitDic[outfitKey].toClientData())
        return _outfitList

    def addOutfit(self, owner, outfitType, outfitId, expireTime, isNew=True):
        LOG_INFO("addOutfit ", outfitType, outfitId, expireTime)
        outfit = self.getOutfitInfo(outfitType, outfitId)
        if not outfit:
            outfit = AvatarOutfit(outfitType, outfitId, expireTime, isNew)
            outfitKey = self.getOutfitKey(outfitType, outfitId)
            self.outfitDic[outfitKey] = outfit
            if outfitType == gameconst.OutfitEnum.mount:
                prop = MOUNTS.datas[outfitId]['prop']
                if prop:
                    owner.cell.updatePropByMount(outfitId, True)
                    owner.updateMountScore()
        else:
            outfit.setExpireTime(expireTime)

    def removeOutfit(self, owner, outfitType, outfitId):
        LOG_INFO("removeOutfit ", outfitType, outfitId)
        _outfit = self.getOutfitInfo(outfitType, outfitId)
        if not _outfit:
            return

        outfitKey = self.getOutfitKey(outfitType, outfitId)
        self.outfitDic.pop(outfitKey, None)

        if outfitType == gameconst.OutfitEnum.mount:
            prop = MOUNTS.datas[outfitId]['prop']
            if prop:
                owner.cell.updatePropByMount(outfitId, False)
            score = MOUNTS.datas[outfitId]['score']
            if score:
                owner.updateMountScore()

    def getOutfitInfo(self, outfitType, outfitId):
        outfitKey = self.getOutfitKey(outfitType, outfitId)
        return self.outfitDic.get(outfitKey, None)

    def setClickOutfit(self, outfitType, outfitId):
        outfitKey = self.getOutfitKey(outfitType, outfitId)
        if not self.outfitDic.get(outfitKey, None):
            LOG_ERR("setClickOutfit ", outfitType, outfitId)
            return
        self.outfitDic[outfitKey].isNew = False
        return True
