
# coding: utf-8

import userType


class ActTimesVal(userType.UserSingleType):
    '''ACT_TIMES_DATA_INFO'''
    def __init__(self, actId=0, times=0):
        self.actId = actId
        self.times = times

    def addTimes(self):
        self.times += 1

    def toActTimesSavedDict(self):
        return {
            'actId': self.actId,
            'times': self.times
        }


class ActTimesInfo(object):
    def createObjFromDict(self, dataDict):
        obj = ActTimesVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toActTimesSavedDict()

    def isSameType(self, obj):
        return type(obj) is ActTimesVal


ActTimesInstance = ActTimesInfo()

