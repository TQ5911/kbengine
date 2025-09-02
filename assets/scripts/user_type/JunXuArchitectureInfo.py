
# coding: utf-8

import userType
import JunXuQiXieInfo


class JunXuArchitectureVal(userType.UserSoleType):
    '''JUN_XU_ARCHITECTURE_DATA_INFO'''
    def __init__(self, qixieList=()):
        self.qixieDic = {}
        for qixie in qixieList:
            self.qixieDic[qixie.qixieType] = qixie

    def getQixie(self, qixieType):
        return self.qixieDic.get(qixieType)

    def toJunXuArchitectureSavedDict(self):
        return {
            'qixieList': list(self.qixieDic.values()),
        }
    
    def addQixie(self, qixieType, level, exp):
        self.qixieDic[qixieType] = JunXuQiXieInfo.JunXuQiXieVal(level, exp, qixieType)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, JunXuArchitectureVal):
            return False
        
        for qixie in value.qixieDic.values():
            if self.qixieDic.get(qixie.qixieType) != qixie:
                return False

        return True


class JunXuArchitectureInfo(object):
    def createObjFromDict(self, dataDict):
        obj = JunXuArchitectureVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toJunXuArchitectureSavedDict()

    def isSameType(self, obj):
        return type(obj) is JunXuArchitectureVal


JunXuArchitectureInstance = JunXuArchitectureInfo()

