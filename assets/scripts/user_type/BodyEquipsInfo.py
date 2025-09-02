# -*- encoding:utf-8 -*-

import BodyEquips


class BodyEquipInfo(object):
    def createObjFromDict(self, dataDict):
        bodyEquips = BodyEquips.BodyEquips()
        bodyEquips.initObjFromSavedDict(dataDict)
        return bodyEquips

    def getDictFromObj(self, obj):
        return obj.toBodyEquipsSavedDict()

    def isSameType(self, obj):
        return type(obj) is BodyEquips.BodyEquips

bodyEquipsInstance = BodyEquipInfo()