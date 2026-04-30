
# coding: utf-8

import userType


class CombatReturnIdleVal(userType.UserSingleType):
    '''COMBAT_RETURN_IDLE_DATA_INFO'''
    def __init__(self, spaceNo=0, pos=None, switch=False, range=0):
        self.spaceNo = spaceNo
        self.pos = pos
        self.switch = switch
        self.range = range

    def toCombatReturnIdleSavedDict(self):
        return {
            "spaceNo": self.spaceNo,
            "pos": self.pos,
            "switch": self.switch,
            "range": self.range
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

