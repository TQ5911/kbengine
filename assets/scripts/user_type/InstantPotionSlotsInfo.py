
# coding: utf-8

import userType
import gameconst
import utils
import itemData_set as ID_SD


class InstantPotionSlotsVal(userType.UserSingleType):
    '''INSTANT_POTION_SLOTS_DATA_INFO'''
    def __init__(self, slots):
        self.slots = slots

    def _needAutoDrinkBase(self):
        for potion in self.slots:
            if potion.isHp():
                continue

            if potion.isMp():
                continue

            if potion.isAuto():
                return True

        return False

    def drinkAll(self, avatar):
        for potion in self.slots:
            if potion.isHp():
                continue

            if potion.isMp():
                continue

            if not potion.isAuto():
                continue

            avatar.useItemWithActionInternal(
                gameconst.BagType.BAG_TYPE_NORMAL,
                potion.itemId,
                avatar.id,
            )

    def updateSlot(self, avatar, potion):
        for _slot, _potion in enumerate(self.slots):
            if _potion.isSame(potion):
                if _potion.slotId != potion.slotId:
                    self.slots.pop(_slot)
                    avatar.client.onRemoveInstantPotionSlots(_potion.slotId)
                break

        for _slot, _potion in enumerate(self.slots):
            if _potion.slotId == potion.slotId:
                self.slots[_slot] = potion
                return True

            if _potion.slotId > potion.slotId:
                if len(self.slots) >= ID_SD.datas['customItemSlotNum']['value']:
                    return False

                self.slots.insert(_slot, potion)
                return True

        if len(self.slots) >= ID_SD.datas['customItemSlotNum']['value']:
            return False

        self.slots.append(potion)
        return True

    def _hasAutoHealHp(self):
        for potion in self.slots:
            if potion.isHp() and utils.bhas(potion.potionState, gameconst.PotionState.AUTO):
                return True

        return False

    def _hasAutoHealMp(self):
        for potion in self.slots:
            if potion.isMp() and utils.bhas(potion.potionState, gameconst.PotionState.AUTO):
                return True

        return False

    def unsetSlot(self, slotId):
        for _slot, _potion in enumerate(self.slots):
            if _potion.slotId == slotId:
                self.slots.pop(_slot)
                return

    def toInstantPotionSlotsSavedDict(self):
        return {
            'slots': self.slots,
        }


class InstantPotionSlotsInfo(object):
    def createObjFromDict(self, dataDict):
        obj = InstantPotionSlotsVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toInstantPotionSlotsSavedDict()

    def isSameType(self, obj):
        return type(obj) is InstantPotionSlotsVal


InstantPotionSlotsInstance = InstantPotionSlotsInfo()

