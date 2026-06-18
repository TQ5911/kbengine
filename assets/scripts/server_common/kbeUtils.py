# coding: utf-8
import KBEngine
from KBEDebug import *
import gameglobal


STATUS_IDLE = 1
STATUS_PROCESSING = 2

class SpaceGeometryTaskData:
    def __init__(self):
        self.status = STATUS_IDLE
        self.tasks = []
        self.curSpaceID = None

def addSpaceGeometryMapping(spaceID, *args):
    if gameglobal.spaceGeometryTaskData is None:
        gameglobal.spaceGeometryTaskData = SpaceGeometryTaskData()

    if gameglobal.spaceGeometryTaskData.status == STATUS_IDLE:
        gameglobal.spaceGeometryTaskData.status = STATUS_PROCESSING
        KBEngine.addSpaceGeometryMapping(spaceID, *args)
        gameglobal.spaceGeometryTaskData.curSpaceID = spaceID

    elif gameglobal.spaceGeometryTaskData.status == STATUS_PROCESSING:
        gameglobal.spaceGeometryTaskData.tasks.append((spaceID, *args))

def processSpaceGeometryTasks(curSpaceID):
    if gameglobal.spaceGeometryTaskData is None:
        return

    if gameglobal.spaceGeometryTaskData.curSpaceID != curSpaceID:
        return

    if len(gameglobal.spaceGeometryTaskData.tasks) == 0:
        gameglobal.spaceGeometryTaskData.status = STATUS_IDLE
        gameglobal.spaceGeometryTaskData.curSpaceID = None
        return

    taskArgs = gameglobal.spaceGeometryTaskData.tasks.pop(0)
    taskArgs = list(taskArgs)
    if KBEngine.hasRes(taskArgs[2]):
        KBEngine.addSpaceGeometryMapping(*taskArgs)
    else:
        # 这里用个同心村的，保证服务器能起来，然后报个错
        LOG_ERR('addSpaceGeometryMapping res not exists', taskArgs)
        taskArgs[2] = 'spaces/tongXinCun'
        KBEngine.addSpaceGeometryMapping(*taskArgs)

    gameglobal.spaceGeometryTaskData.curSpaceID = taskArgs[0]
