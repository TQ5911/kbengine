
# coding: utf-8

import userType


class SkillTimerLogVal(userType.UserSingleType):
    '''SKILL_TIMER_LOG_DATA_INFO'''
    def __init__(self, objId=0, timerId=0, opr=0, key=0, skillId=0, ts=0):
        self.objId = objId
        self.timerId = timerId
        self.opr = opr
        self.key = key
        self.skillId = skillId
        self.ts = ts

    def __repr__(self):
        return f'<SkillTimerLogVal objId={self.objId} timerId={self.timerId} opr={self.opr} key={self.key}>'

    def toSkillTimerLogSavedDict(self):
        return {
            'objId': self.objId,
            'timerId': self.timerId,
            'opr': self.opr,
            'key': self.key,
            'skillId': self.skillId,
            'ts': self.ts,
        }


class SkillTimerLogInfo(object):
    def createObjFromDict(self, dataDict):
        obj = SkillTimerLogVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toSkillTimerLogSavedDict()

    def isSameType(self, obj):
        return type(obj) is SkillTimerLogVal


SkillTimerLogInstance = SkillTimerLogInfo()

