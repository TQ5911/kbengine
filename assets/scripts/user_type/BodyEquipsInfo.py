# -*- encoding:utf-8 -*-

import BodyEquips


class BodyEquipInfo(object):
    def createObjFromDict(self, dataDict):
        _bodyEquips = BodyEquips.BodyEquips()
        _bodyEquips.initObjFromSavedDict(dataDict)
        return _bodyEquips

    def isSameType(self, obj):
        return type(obj) is BodyEquips.BodyEquips

    def getDictFromObj(self, obj):
        return obj.toBodyEquipsSavedDict()

bodyEquipsInstance = BodyEquipInfo()
