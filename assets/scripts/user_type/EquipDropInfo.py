
# coding: utf-8

import userType
import itemFactory

class EquipDropVal(userType.UserSingleType):
    '''EQUIP_DROP_DATA_INFO'''
    def __init__(self, uniqueId=0, price=0, state=0, mapId=0, pos=None, equip=None, collEndTime=0, killerName='', endTime=0, dropTime=0, redeemWaitTime=0):
        self.uniqueId = uniqueId
        self.price = price
        self.state = state
        self.mapId = mapId
        self.pos = pos
        self.equip = equip
        self.collEndTime = collEndTime
        self.killerName = killerName
        self.endTime = endTime
        self.dropTime = dropTime
        self.redeemWaitTime = redeemWaitTime

    def toEquipDropSavedDict(self):
        return {
            'uniqueId': self.uniqueId,
            'price': self.price,
            'state': self.state,
            'mapId': self.mapId,
            'pos': self.pos,
            'equip': self.equip,
            'collEndTime': self.collEndTime,
            'killerName': self.killerName,
            'endTime': self.endTime,
            'dropTime': self.dropTime,
            'redeemWaitTime': self.redeemWaitTime,
        }
    
    def equipItem(self):
        return itemFactory.ItemFactory.createItemWithSavedDict(self.equip)
    
    def __lt__(self, other):
        return self.endTime < other.endTime


class EquipDropInfo(object):
    def createObjFromDict(self, dataDict):
        obj = EquipDropVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toEquipDropSavedDict()

    def isSameType(self, obj):
        return type(obj) is EquipDropVal


EquipDropInstance = EquipDropInfo()

