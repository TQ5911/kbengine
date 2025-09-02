# -*- encoding:utf-8 -*-
import WarehouseBag

class WarehouseBagInfo(object):
    def createObjFromDict(self, dataDict):
        bag = WarehouseBag.WarehouseBag()
        bag.initFromDict(dataDict)
        return bag

    def getDictFromObj(self, obj):
        return obj.toBagSavedDict()

    def isSameType(self, obj):
        return type(obj) is WarehouseBag.WarehouseBag

instance = WarehouseBagInfo()

