
# coding: utf-8

import userType
import guildAuthorization_authorizationID as GA_AID
import guildAuthorization_authorization as GA_AD


class PermissionGroupVal(userType.UserSoleType):
    def __init__(self, job=0, permission=0):
        self.job = job
        self.permission = permission

    def initPermissionFromData(self, data):
        self.permission = self.getDefaultPermission()

    def getDefaultPermission(self):
        _permission = 0
        for _idx in (GA_AD.datas[self.job]['authorization'] or []):
            _permission |= 1 << _idx

        return _permission

    def addHidenPermission(self, data):
        for _idx in (data['authorization'] or []):
            if GA_AID.datas[_idx]['hidden']:
                self.permission |= 1 << _idx

    def toPermissionGroupSavedDict(self):
        return {
            'job': self.job,
            'permission': self.permission
        }


class PermissionGroupInfo(object):
    def createObjFromDict(self, dataDict):
        obj = PermissionGroupVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toPermissionGroupSavedDict()

    def isSameType(self, obj):
        return type(obj) is PermissionGroupVal


PermissionGroupInstance = PermissionGroupInfo()

