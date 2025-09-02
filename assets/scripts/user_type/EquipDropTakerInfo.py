
# coding: utf-8

import userType
import itemFactory

class EquipDropTakerVal(userType.UserSoleType):
    '''EQUIP_DROP_TAKER_DATA_INFO'''
    def __init__(self, uniqueId=0, equip=None, endTime=0, state=0, price=0):
        self.uniqueId = uniqueId
        self.equip = equip
        self.endTime = endTime
        self.state = state
        self.price = price

    def toEquipDropTakerSavedDict(self):
        return {
            'uniqueId': self.uniqueId,
            'equip': self.equip,
            'endTime': self.endTime,
            'state': self.state,
            'price': self.price,
        }

    def equipItem(self):
        return itemFactory.ItemFactory.createItemWithSavedDict(self.equip)


class EquipDropTakerInfo(object):
    def createObjFromDict(self, dataDict):
        obj = EquipDropTakerVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toEquipDropTakerSavedDict()

    def isSameType(self, obj):
        return type(obj) is EquipDropTakerVal


EquipDropTakerInstance = EquipDropTakerInfo()

