# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *


import dataUtils
import Item
import itemData_itemData as ID_IDD


class LingShouEggItem(Item.Item):
    def __init__(self, itemId, itemNum, bindType, growthRate=0, **keywardargs):
        super(LingShouEggItem, self).__init__(itemId, itemNum, bindType)
        self.petId = ID_IDD.datas[itemId].get('indexID', 0)
        if not self.petId:
            LOG_ERR('petId is invalid:', itemId, itemNum)

    @staticmethod
    def isLingShouEggItem():
        return True

    def onSpecificItemChanged(self, jsonData):
        _itemData = dataUtils.getCommItemData(self.itemId)
        self.quality = _itemData['quality']
        self.petId = ID_IDD.datas[self.itemId].get('indexID', 0)
        self.rollProps = []

    def attr2Dict(self):
        _dict = super().attr2Dict()
        return _dict

    def attr2LingShouData(self):
        lingShouDict = dataUtils.createPetInfo(self.petId)
        return lingShouDict
