# coding: utf-8

import userType

class GuildTaskInfoVal(userType.UserSingleType):
    "GUILD_ONETASK_INFO"
    def __init__(self, taskID = 0, num = 0, completed = False):
        self.taskID = taskID
        self.num = num
        self.complete = 1 if completed else 0

    def toGuildTaskInfoSavedDict(self):
        return {
            'taskID': self.taskID,
            'num': self.num,
            'completed': self.complete,
        }

class GuildTaskInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildTaskInfoVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildTaskInfoSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildTaskInfoVal


GuildTaskInfoInstance = GuildTaskInfo()