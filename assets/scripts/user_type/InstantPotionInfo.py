
# coding: utf-8

import userType
import itemData_itemData as ID_IDD
import gameconst
import utils

class InstantPotionVal(userType.UserSingleType):
    '''INSTANT_POTION_DATA_INFO'''
    def __init__(self, itemId, slotId, potionState):
        self.itemId = itemId
        self.slotId = slotId
        self.potionState = potionState

    def isSame(self, other):
        if self.itemId != other.itemId:
            return False

        return True

    def isAuto(self):
        return utils.bhas(self.potionState, gameconst.PotionState.AUTO)

    def isHp(self):
        itemData = ID_IDD.datas.get(self.itemId)
        if not itemData:
            return False

        if itemData['type'] != gameconst.ItemEnum.Normal:
            return False

        return itemData['subType'] == 1

    def isMp(self):
        itemData = ID_IDD.datas.get(self.itemId)
        if not itemData:
            return False

        if itemData['type'] != gameconst.ItemEnum.Normal:
            return False

        return itemData['subType'] == 2

    def isInnerDemonUse(self):
        itemData = ID_IDD.datas.get(self.itemId)
        if not itemData:
            return False

        return itemData['isAutoUseInCustomSlot'] == 1
    
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

