
# coding: utf-8

import userType


class CombatReturnIdleVal(userType.UserSoleType):
    '''COMBAT_RETURN_IDLE_DATA_INFO'''
    def __init__(self, spaceNo=0, pos=None):
        self.spaceNo = spaceNo
        self.pos = pos

    def toCombatReturnIdleSavedDict(self):
        return {
            "spaceNo": self.spaceNo,
            "pos": self.pos
        }


class CombatReturnIdleInfo(object):
    def createObjFromDict(self, dataDict):
        obj = CombatReturnIdleVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toCombatReturnIdleSavedDict()

    def isSameType(self, obj):
        return type(obj) is CombatReturnIdleVal


CombatReturnIdleInstance = CombatReturnIdleInfo()

