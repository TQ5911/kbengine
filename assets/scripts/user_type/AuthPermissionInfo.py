
# coding: utf-8

import userType


class AuthPermissionVal(userType.UserSoleType):
    '''AUTH_PERMISSION_DATA_INFO'''
    def __init__(self, permission=0, dailyMoney=0):
        self.permission = permission
        self.dailyMoney = dailyMoney

    def toAuthPermissionSavedDict(self):
        return {
            'permission': self.permission,
            'dailyMoney': self.dailyMoney
        }


class AuthPermissionInfo(object):
    def createObjFromDict(self, dataDict):
        obj = AuthPermissionVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toAuthPermissionSavedDict()

    def isSameType(self, obj):
        return type(obj) is AuthPermissionVal


AuthPermissionInstance = AuthPermissionInfo()

