
# coding: utf-8
from KBEDebug import *
import SkillTimerLogInfo
import userType
import gameconst
from collections import deque
import utils


class SkillTimerLogQueueVal(userType.UserSoleType):
    '''SKILL_TIMER_LOG_QUEUE_DATA_INFO'''
    def __init__(self, logQueue=()):
        self.logQueue = deque(logQueue)

    def addSkillTimerLog(self, objId, timerId, opr, key, skillId):
        _val = SkillTimerLogInfo.SkillTimerLogVal(objId, timerId, opr, key, skillId, utils.getNow())
        self.logQueue.append(_val)
        while len(self.logQueue) > gameconst.SKILL_TIMER_LOG_QUEUE_MAX_CNT:
            self.logQueue.popleft()

    def errReportLogQueue(self):
        for log in self.logQueue:
            ERROR_MSG(f"errReportLogQueue: {log}")

    def toSkillTimerLogQueueSavedDict(self):
        return {
            'logQueue': list(self.logQueue)
        }


class SkillTimerLogQueueInfo(object):
    def createObjFromDict(self, dataDict):
        obj = SkillTimerLogQueueVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toSkillTimerLogQueueSavedDict()

    def isSameType(self, obj):
        return type(obj) is SkillTimerLogQueueVal


SkillTimerLogQueueInstance = SkillTimerLogQueueInfo()

