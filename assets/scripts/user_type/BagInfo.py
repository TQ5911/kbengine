# -*- encoding:utf-8 -*-
from KBEDebug import *

import Bag


class BagInfo(object):
    def createObjFromDict(self, dataDict):
        DEBUG_MSG("bag createObjFromDict")
        bag = Bag.Bag()
        bag.initFromDict(dataDict)
        return bag

    def getDictFromObj(self, obj):
        return obj.toBagSavedDict()

    def isSameType(self, obj):
        return type(obj) is Bag.Bag


bagInstance = BagInfo()
