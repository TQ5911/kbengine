# -*- encoding:utf-8 -*-
from KBEDebug import *

import Bag


class BagInfo(object):
    def createObjFromDict(self, dataDict):
        _bag = Bag.Bag()
        _bag.initFromDict(dataDict)
        return _bag

    def isSameType(self, obj):
        return type(obj) is Bag.Bag

    def getDictFromObj(self, obj):
        return obj.toBagSavedDict()


bagInstance = BagInfo()
