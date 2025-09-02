
# coding: utf-8

import userType


class AutoHealVal(userType.UserSoleType):
    '''AUTO_HEAL_DATA_INFO'''
    def __init__(self, healItem=0, healRatio=0.0):
        self.healItem = healItem
        self.healRatio = healRatio

    def toAutoHealSavedDict(self):
        return {
            'healItem': self.healItem,
            'healRatio': self.healRatio,
        }


class AutoHealInfo(object):
    def createObjFromDict(self, dataDict):
        obj = AutoHealVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toAutoHealSavedDict()

    def isSameType(self, obj):
        return type(obj) is AutoHealVal


AutoHealInstance = AutoHealInfo()

