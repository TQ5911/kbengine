
# coding: utf-8

import userType


class AccountCacheVal(userType.UserSoleType):
    '''ACCOUNT_CACHE_DATA_INFO'''
    def __init__(self, eid=0, isHost=False):
        self.eid = eid
        self.isHost = isHost

    def toAccountCacheSavedDict(self):
        return {
            'eid': self.eid,
            'isHost': self.isHost
        }


class AccountCacheInfo(object):
    def createObjFromDict(self, dataDict):
        obj = AccountCacheVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toAccountCacheSavedDict()

    def isSameType(self, obj):
        return type(obj) is AccountCacheVal


AccountCacheInstance = AccountCacheInfo()

