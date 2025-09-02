
# coding: utf-8

import userType
import itemData_itemData as ID_IDD
import gameconst
import utils

class InstantPotionVal(userType.UserSoleType):
    '''INSTANT_POTION_DATA_INFO'''
    def __init__(self, itemId, slotId, potionState):
        self.itemId = itemId
        self.slotId = slotId
        self.potionState = potionState

    def isSame(self, other):
        if self.itemId != other.itemId:
            return False

        if utils.hasBit(self.potionState, gameconst.PotionState.BIND) != utils.hasBit(other.potionState, gameconst.PotionState.BIND):
            return False

        return True

    def isAuto(self):
        return utils.hasBit(self.potionState, gameconst.PotionState.AUTO)

    def isBind(self):
        return utils.hasBit(self.potionState, gameconst.PotionState.BIND)

    def isHp(self):
        itemData = ID_IDD.datas.get(self.itemId)
        if not itemData:
            return False

        if itemData['type'] != gameconst.ItemType.Normal:
            return False

        return itemData['subType'] == 1

    def isMp(self):
        itemData = ID_IDD.datas.get(self.itemId)
        if not itemData:
            return False

        if itemData['type'] != gameconst.ItemType.Normal:
            return False

        return itemData['subType'] == 2

    def toInstantPotionSavedDict(self):
        return {
            'itemId': self.itemId,
            'slotId': self.slotId,
            'potionState': self.potionState,
        }


class InstantPotionInfo(object):
    def createObjFromDict(self, dataDict):
        obj = InstantPotionVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toInstantPotionSavedDict()

    def isSameType(self, obj):
        return type(obj) is InstantPotionVal


InstantPotionInstance = InstantPotionInfo()

