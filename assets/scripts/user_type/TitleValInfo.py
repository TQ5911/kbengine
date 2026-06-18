
# coding: utf-8
import dataUtils

import userType


class TitleValVal(userType.UserSingleType):
    '''TITLE_VAL_INFO'''
    def __init__(self, titleId=0, expireTime=0):
        self.titleId = titleId
        # expireTime 是纯粹读配表，所以不存储，这里也不读

    def __repr__(self):
        return '{}->{}'.format(self.titleId, self.expireTime)

    @classmethod
    def fromTitleIdAndStartTime(cls, titleId, startTime):
        return cls(titleId, )

    @property
    def expireTime(self):
        return dataUtils.getTitleEndTime(self.titleId)

    def toTitleValSavedDict(self):
        return {
            'titleId': self.titleId,
            'expireTime': self.expireTime,
        }


class TitleValInfo(object):
    def createObjFromDict(self, dataDict):
        obj = TitleValVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toTitleValSavedDict()

    def isSameType(self, obj):
        return type(obj) is TitleValVal


TitleValInstance = TitleValInfo()

