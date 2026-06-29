# -*- encoding:utf-8 -*-

import avatarPet


class LingShouInfo(object):
    def createObjFromDict(self, dataDict):
        _lingShouInfo = avatarPet.LingShouInfo()
        _lingShouInfo.initFromDict(dataDict)
        return _lingShouInfo

    def isSameType(self, obj):
        return type(obj) is avatarPet.LingShouInfo

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()


lingShouInstance = LingShouInfo()
