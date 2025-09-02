
# coding: utf-8

import userType
import utils
import gameconst
import KBEngine


class DuelAttrVal(userType.UserSoleType):
    '''DUEL_ATTR_DATA_INFO'''
    def __init__(self, duelFlags=0, targetId=0, duelFlagId=0):
        self.duelFlags = duelFlags
        self.targetId = targetId
        self.duelFlagId = duelFlagId

    def reset(self):
        self.duelFlags = 0
        self.targetId = 0
        self.duelFlagId = 0

    def duelFlagEnt(self):
        return KBEngine.entities.get(self.duelFlagId)

    def isDuelEnemy(self, target):
        if not self.inFight():
            return False
        
        if not target.duelAttr.inFight():
            return False
        
        if self.targetId != target.id:
            return False
        
        return True

    def inDuel(self):
        return utils.hasBit(self.duelFlags, gameconst.DuelFlag.IN_DUEL)
    
    def inReady(self):
        return utils.hasBit(self.duelFlags, gameconst.DuelFlag.READY)
    
    def inFight(self):
        return utils.hasBit(self.duelFlags, gameconst.DuelFlag.FIGHT)
    
    def readyDuel(self, targetId):
        self.duelFlags = utils.bitSet(self.duelFlags, gameconst.DuelFlag.IN_DUEL)
        self.duelFlags = utils.bitSet(self.duelFlags, gameconst.DuelFlag.READY)
        self.targetId = targetId

    def startFight(self):
        self.duelFlags = utils.bitSet(self.duelFlags, gameconst.DuelFlag.FIGHT)
        self.duelFlags = utils.bitReset(self.duelFlags, gameconst.DuelFlag.READY)

    def setDuelFlagId(self, duelFlagId):
        self.duelFlagId = duelFlagId

    def toDuelAttrSavedDict(self):
        return {
            'duelFlags': self.duelFlags,
            'targetId': self.targetId,
            'duelFlagId': self.duelFlagId,
        }


class DuelAttrInfo(object):
    def createObjFromDict(self, dataDict):
        obj = DuelAttrVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toDuelAttrSavedDict()

    def isSameType(self, obj):
        return type(obj) is DuelAttrVal


DuelAttrInstance = DuelAttrInfo()

