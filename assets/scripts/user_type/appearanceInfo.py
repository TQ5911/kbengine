# -*- coding: utf-8 -*-
import KBEngine
import random
from KBEDebug import *
import appearance


class AppearanceInfo(object):

    def createObjFromDict(self, dic):
        _a = appearance.Appearance()
        _a.initFromDict(dic)
        return _a

    def isSameType(self, obj):
        return type(obj) is appearance.Appearance

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()


instance = AppearanceInfo()


class FaceDataInfo(object):

    def createObjFromDict(self, dic):
        _a = appearance.FaceDataVal()
        _a.initFromDict(dic)
        return _a

    def isSameType(self, obj):
        return type(obj) is appearance.FaceDataVal

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()


faceDataIns = FaceDataInfo()


class OutfitDataInfo(object):

    def createObjFromDict(self, dic):
        _a = appearance.OutfitDataVal()
        _a.initFromDict(dic)
        return _a

    def isSameType(self, obj):
        return type(obj) is appearance.OutfitDataVal

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()


outfitDataIns = OutfitDataInfo()


class AvatarOutfitInfo(object):
    def createObjFromDict(self, dataDict):
        _outfitInfo = appearance.AvatarOutfitInfo()
        _outfitInfo.initFromDict(dataDict)
        return _outfitInfo

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is appearance.AvatarOutfitInfo


outfitInstance = AvatarOutfitInfo()


class AvatarPhotoInfo(object):
    def createObjFromDict(self, dataDict):
        _outfitInfo = appearance.AvatarPhotoDataVal()
        _outfitInfo.initFromDict(dataDict)
        return _outfitInfo

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is appearance.AvatarPhotoDataVal


avatarPhotoInstance = AvatarPhotoInfo()
