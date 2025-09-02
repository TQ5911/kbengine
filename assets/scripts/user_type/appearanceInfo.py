# -*- coding: utf-8 -*-
import KBEngine
import random
import gameconst
from KBEDebug import *
import appearance
import time

import userType
import sMath
import utils


class AppearanceInfo(object):

    def createObjFromDict(self, dic):
        a = appearance.Appearance()
        a.initFromDict(dic)
        return a

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is appearance.Appearance


instance = AppearanceInfo()


class FaceDataInfo(object):

    def createObjFromDict(self, dic):
        a = appearance.FaceDataVal()
        a.initFromDict(dic)
        return a

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is appearance.FaceDataVal


faceDataIns = FaceDataInfo()


class OutfitDataInfo(object):

    def createObjFromDict(self, dic):
        a = appearance.OutfitDataVal()
        a.initFromDict(dic)
        return a

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is appearance.OutfitDataVal


outfitDataIns = OutfitDataInfo()


class AvatarOutfitInfo(object):
    def createObjFromDict(self, dataDict):
        outfitInfo = appearance.AvatarOutfitInfo()
        outfitInfo.initFromDict(dataDict)
        return outfitInfo

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is appearance.AvatarOutfitInfo


outfitInstance = AvatarOutfitInfo()


class AvatarPhotoInfo(object):
    def createObjFromDict(self, dataDict):
        outfitInfo = appearance.AvatarPhotoDataVal()
        outfitInfo.initFromDict(dataDict)
        return outfitInfo

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is appearance.AvatarPhotoDataVal


avatarPhotoInstance = AvatarPhotoInfo()
