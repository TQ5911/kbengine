
# coding: utf-8

import userType


class AuthStatisticsVal(userType.UserSoleType):
    '''AUTH_STATISTICS_DATA_INFO'''
    def __init__(self, oldLevel=0, oldCoin=0):
        self.oldLevel = oldLevel
        self.oldCoin = oldCoin

    def toAuthStatisticsSavedDict(self):
        return {
            'oldLevel': self.oldLevel,
            'oldCoin': self.oldCoin
        }


class AuthStatisticsInfo(object):
    def createObjFromDict(self, dataDict):
        obj = AuthStatisticsVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toAuthStatisticsSavedDict()

    def isSameType(self, obj):
        return type(obj) is AuthStatisticsVal


AuthStatisticsInstance = AuthStatisticsInfo()

