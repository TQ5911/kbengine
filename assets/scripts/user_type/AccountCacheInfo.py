
# coding: utf-8

import userType
import gameconst


class AccountCacheVal(userType.UserSingleType):
    '''ACCOUNT_CACHE_DATA_INFO'''
    def __init__(self, eid=0, actHostType=gameconst.AccountHostType.NONE):
        self.eid = eid
        self.actHostType = actHostType

    def isAccountHost(self):
        return self.actHostType == gameconst.AccountHostType.HOST

    def toAccountCacheSavedDict(self):
        return {
            'eid': self.eid,
            'actHostType': self.actHostType
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

