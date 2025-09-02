# -*- encoding:utf-8 -*-

import avatarPet


class LingShouInfo(object):
    def createObjFromDict(self, dataDict):
        lingShouInfo = avatarPet.LingShouInfo()
        lingShouInfo.initFromDict(dataDict)
        return lingShouInfo

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is avatarPet.LingShouInfo


lingShouInstance = LingShouInfo()