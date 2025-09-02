
# coding: utf-8

import userType


class GuildPermissionsVal(userType.UserDictType):
    '''GUILD_PERMISSIONS_DATA_INFO'''
    def __init__(self, permissions):
        for _val in permissions:
            self[_val.job] = _val

    def toGuildPermissionsSavedDict(self):
        return {
            'permissions': list(self.values())
        }


class GuildPermissionsInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildPermissionsVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildPermissionsSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildPermissionsVal


GuildPermissionsInstance = GuildPermissionsInfo()

