# -*- encoding:utf-8 -*-

import TaskInfo
import Task


class TaskInfoVal(object):
    def createObjFromDict(self, dataDict):
        _taskInfo = TaskInfo.TaskInfo()
        _taskInfo.fromSavedDict(dataDict)
        return _taskInfo

    def isSameType(self, obj):
        return type(obj) is TaskInfo.TaskInfo

    def getDictFromObj(self, obj):
        _dic = obj.toTaskInfoSavedDict()
        return _dic


taskInfoInstance = TaskInfoVal()


class TaskClientInfoVal(object):
    def createObjFromDict(self, dataDict):
        _taskInfo = TaskInfo.TaskInfo()
        _taskInfo.fromSavedDict(dataDict)
        return _taskInfo

    def isSameType(self, obj):
        return type(obj) is TaskInfo.TaskInfo

    def getDictFromObj(self, obj):
        _dic = obj.toTaskInfoClientDict()
        return _dic


taskClientInfoInstance = TaskClientInfoVal()


class TaskVal(object):
    def createObjFromDict(self, dataDict):
        return Task.TaskFactory.createTaskBySavedDict(dataDict)

    def isSameType(self, obj):
        return type(obj) is Task.Task

    def getDictFromObj(self, obj):
        return obj.toTaskSavedDict()


taskValInstance = TaskVal()
