# -*- encoding:utf-8 -*-

import TaskInfo
import Task


class TaskInfoVal(object):
    def createObjFromDict(self, dataDict):
        taskInfo = TaskInfo.TaskInfo()
        taskInfo.fromSavedDict(dataDict)
        return taskInfo

    def getDictFromObj(self, obj):
        dic = obj.toTaskInfoSavedDict()
        return dic

    def isSameType(self, obj):
        return type(obj) is TaskInfo.TaskInfo


taskInfoInstance = TaskInfoVal()


class TaskClientInfoVal(object):
    def createObjFromDict(self, dataDict):
        taskInfo = TaskInfo.TaskInfo()
        taskInfo.fromSavedDict(dataDict)
        return taskInfo

    def getDictFromObj(self, obj):
        dic = obj.toTaskInfoClientDict()
        return dic

    def isSameType(self, obj):
        return type(obj) is TaskInfo.TaskInfo


taskClientInfoInstance = TaskClientInfoVal()


class TaskVal(object):
    def createObjFromDict(self, dataDict):
        return Task.TaskFactory.createTaskBySavedDict(dataDict)

    def getDictFromObj(self, obj):
        return obj.toTaskSavedDict()

    def isSameType(self, obj):
        return type(obj) is Task.Task


taskValInstance = TaskVal()
