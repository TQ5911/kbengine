# coding: utf-8
import userType


class MeridianPointVal(userType.UserSingleType):
    """MERIDIAN_POINT_VAL"""
    def __init__(self, pointIdx=0):
        self.pointIdx = pointIdx
        self.level = 0

    @property
    def maxLevel(self):
        return 5

    def initFromDict(self, dataDic):
        self.pointIdx = dataDic['pointIdx']
        self.level = dataDic['level']
        return self
    
    def toStreamSaveDict(self):
        return {
            'pointIdx': self.pointIdx,
            'level': self.level,
        }
    
    def toClientDict(self):
        return {
            'pointIdx': self.pointIdx,
            'level': self.level,
        }
        
    def getCurLevel(self):
        return self.level
    
    def hasFullLevel(self):
        if self.level >= self.maxLevel:
            return True
        return False
    
    def doLevelUp(self):
        self.level += 1
        return self.level

class MeridianSlotVal(userType.UserSingleType):
    """MERIDIAN_SLOT_VAL"""
    def __init__(self, slotIdx=0):
        self.slotIdx = slotIdx
        self.hasEnhance = False
        self.pointDict = {}
        
        for i in range(self.maxPoints):
            self.pointDict[i+1] = MeridianPointVal(i+1)

    @property
    def maxPoints(self):
        return 8

    def initFromDict(self, dataDic):
        self.pointDict = {}
        self.slotIdx = dataDic.get('slotIdx', 0)
        self.hasEnhance = dataDic.get('hasEnhance', False)
        
        for i in range(self.maxPoints):
            self.pointDict[i+1] = MeridianPointVal(i+1)
            
        points = dataDic.get('points', [])
        for pVal in points:
            idx = pVal['pointIdx']
            self.pointDict[idx].initFromDict(pVal)
            
        return self
    
    def toStreamSaveDict(self):
        return {
            'slotIdx': self.slotIdx,
            'hasEnhance': self.hasEnhance,
            'points': [v.toStreamSaveDict() for v in self.pointDict.values()],
        }
    
    def toClientDict(self):
        return {
            'slotIdx': self.slotIdx,
            'hasEnhance': self.hasEnhance,
            'points': [v.toClientDict() for v in self.pointDict.values()],
        }
    
    def getPointLevel(self, pointIdx):
        if pointIdx in self.pointDict:
            return self.pointDict[pointIdx].getCurLevel()
        return None
    
    def canLevelUpPoint(self, pointIdx):
        if pointIdx in self.pointDict:
            _MPVal = self.pointDict[pointIdx]
            if not _MPVal.hasFullLevel():
                return True
        return False

    def doLevelUpPoint(self, pointIdx):
        if self.canLevelUpPoint(pointIdx):
            return self.pointDict[pointIdx].doLevelUp()
        return 0    
    
    def canEnhance(self):
        if self.hasEnhance:
            return False
        for pVal in self.pointDict.values():
            if not pVal.hasFullLevel():
                return False
        return True
    
    def doEnhance(self):
        if self.canEnhance():
            self.hasEnhance = True
            return True
        return False

class MeridianVal(userType.UserSingleType):
    """MERIDIAN_VAL"""
    def __init__(self):
        self.curSlot = 1
        self.slotDict = {}

        # initialize first slot
        self.slotDict[self.curSlot] = MeridianSlotVal(slotIdx=self.curSlot)

    @property
    def maxSlots(self):
        return 20

    def hasFinishAll(self):
        if self.curSlot > self.maxSlots:
            return True
        return False

    def getCurrentSlot(self):
        return self.curSlot

    def initFromDict(self, dataDic):
        self.slotDict = {}
        self.curSlot = dataDic.get('curSlot', 1)
        slots = dataDic.get('slots', [])
        for sVal in slots:
            idx = sVal.get('slotIdx', 0)
            _MSVal = MeridianSlotVal().initFromDict(sVal)
            self.slotDict[idx] = _MSVal
        
        if self.curSlot < 1:
            self.curSlot = 1
        if self.curSlot not in self.slotDict.keys():
            self.slotDict[self.curSlot] = MeridianSlotVal(slotIdx=self.curSlot)
        return self
    
    def toStreamSaveDict(self):
        return {
            'curSlot': self.curSlot,
            'slots': [v.toStreamSaveDict() for v in self.slotDict.values()],
        }
    
    def toClientDict(self):
        return {
            'curSlot': self.curSlot,
            'maxSlots': self.maxSlots,
            # 'slots': [v.toClientDict() for v in self.slotDict.values()],
            'slots': [self.slotDict[self.curSlot].toClientDict()],
        }
        
    def getCurrSlotPointLevel(self, slotIdx, pointIdx):
        if slotIdx in self.slotDict:
            _MSVal = self.slotDict[slotIdx]
            return _MSVal.getPointLevel(pointIdx)
        return None
    
    def canLevelUpSlotPoint(self, slotIdx, pointIdx):
        if self.hasFinishAll():
            return False
        if slotIdx != self.curSlot:
            return False
        _MSVal = self.slotDict.get(slotIdx, None)
        if _MSVal and _MSVal.canLevelUpPoint(pointIdx):
            return True
        return False
    
    def levelUpPoint(self, slotIdx, pointIdx):
        if not self.canLevelUpSlotPoint(slotIdx, pointIdx):
            return False, 0
        level = self.slotDict[slotIdx].doLevelUpPoint(pointIdx)
        if level > 0:
            return True, level
        return False, 0
    
    def canEnhanceCurSlot(self, slotIdx):
        if not self.hasFinishAll() and slotIdx == self.curSlot and slotIdx in self.slotDict:
            _MSVal = self.slotDict[slotIdx]
            if _MSVal and _MSVal.canEnhance():
                return True
        return False
    
    def doEnhanceCurSlot(self, slotIdx):
        if self.canEnhanceCurSlot(slotIdx):
            self.slotDict[slotIdx].doEnhance()
            self.curSlot += 1
            self.slotDict[self.curSlot] = MeridianSlotVal(slotIdx=self.curSlot)
            return True, self.curSlot
        return False, self.curSlot
    

class MeridianInfoVal(object):
    """MERIDIAN_INFO"""
    def createObjFromDict(self, dataDict):
        meridian = MeridianVal()
        meridian.initFromDict(dataDict)
        return meridian
    
    def getDictFromObj(self, obj):
        return obj.toStreamSaveDict()
    
    def isSameType(self, obj):
        return type(obj) is MeridianVal

MeridianInstance = MeridianInfoVal()
