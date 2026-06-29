# -*- encoding:utf-8 -*-
import WarehouseBag

class WarehouseBagInfo(object):
    def createObjFromDict(self, dataDict):
        _bag = WarehouseBag.WarehouseBag()
        _bag.initFromDict(dataDict)
        return _bag

    def isSameType(self, obj):
        return type(obj) is WarehouseBag.WarehouseBag

    def getDictFromObj(self, obj):
        return obj.toBagSavedDict()

instance = WarehouseBagInfo()

