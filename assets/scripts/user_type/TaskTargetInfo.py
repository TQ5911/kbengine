# -*- encoding:utf-8 -*-

from KBEDebug import *
import formula
import json
import math
import userType
import gameconst
import gameengine
import dataUtils

import taskClass_taskTarget as TCTTD


MAX_JSON_STR_LENGTH = 1024


class BaseTarget(userType.UserSingleType):
    tgtType = gameconst.TaskTargetType.TARGET_UNKNOWN

    def __init__(self):
        self.tgtId = 0
        self.stepCnt = 0
        self.dstCnt = 0
        return

    def __getstate__(self):
        return self.toTgtSavedDict()

    def __setstate__(self, state):
        self.__init__()
        self.fromSavedDict(state)

    def genExtraStr(self):
        return ''

    @staticmethod
    def loadsExtraJson(extraStr):
        if not extraStr:
            return {}
        try:
            return json.loads(extraStr)
        except Exception as e:
            gameengine.panicStack('in loadsExtraJson:', e, extraStr)
            return {}

    def fromExtraDic(self, extraStr):
        return

    def cliExtra(self):
        return ''

    def setTargetCompleted(self):
        self.stepCnt = self.dstCnt

    def toTgtSavedDict(self):
        extraStr = self.genExtraStr()
        if len(extraStr) >= MAX_JSON_STR_LENGTH:
            gameengine.panicStack('toTgtSavedDict, json str reach max limit:', self.__dict__)
        return {
            'tgtType': self.tgtType,
            'tgtId': self.tgtId,
            'stepCnt': self.stepCnt,
            'dstCnt': self.dstCnt,
            'extraStr': extraStr,
        }

    def toClientDict(self):
        return {
            'tgtType': self.tgtType,
            'tgtId': self.tgtId,
            'stepCnt': self.stepCnt,
            'dstCnt': self.dstCnt,
            'cliExtra': self.cliExtra()
        }

    def fromSavedDict(self, dataDic):
        try:
            self.tgtType = dataDic['tgtType']
            self.tgtId = dataDic['tgtId']
            self.stepCnt = dataDic['stepCnt']
            self.dstCnt = dataDic['dstCnt']
            extraDic = self.loadsExtraJson(dataDic['extraStr'])
            self.fromExtraDic(extraDic)
        except Exception as e:
            gameengine.panicStack('in BaseTarget.fromSavedDict:', e)
        return

    def initFromTgtObj(self, tgt):
        self.tgtType = tgt.tgtType
        self.tgtId = tgt.tgtId
        self.stepCnt = tgt.stepCnt
        self.dstCnt = tgt.dstCnt

    def isTargetCompleted(self):
        return self.stepCnt >= self.dstCnt

    @property
    def dungeonNo(self):
        if hasattr(self, 'mapId'):
            return getattr(self, 'mapId')
        else:
            return 0

    def checkTargetCompleted(self, *args):
        return self.isTargetCompleted()


class TaskTargetMonsters(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_MONSTERS

    def __init__(self):
        super(TaskTargetMonsters, self).__init__()
        self.stepCnt = 0

        self.mapId = 0
        self.targetUIDs = []
        self.killMode = 0
        self.killTotalCountTarget = 0
        self.killedTotalCount = 0
        self.monsterIDsTarget = []

    def initTarget(self, tgtId, dstCnt, mapId, killMode, killTotalCount, monsterIDs):
        self.tgtId = tgtId
        self.dstCnt = dstCnt
        self.mapId = mapId
        self.killMode = killMode
        self.killTotalCountTarget = killTotalCount
        self.monsterIDsTarget = list(monsterIDs)

    def initFromTgtObj(self, tgt):
        super(TaskTargetMonsters, self).initFromTgtObj(tgt)
        self.mapId = tgt.mapId

    def genExtraStr(self):
        datas = {
            'mapId': self.mapId,
            'killMode': self.killMode,
            'killTotalCountTarget': self.killTotalCountTarget,
            'killedTotalCount': self.killedTotalCount,
            'monsterIDsTarget': self.monsterIDsTarget,
        }
        return json.dumps(datas)

    def fromExtraDic(self, extraDic):
        self.mapId = extraDic.get('mapId', 0)
        self.killMode = extraDic.get('killMode', 0)
        self.killTotalCountTarget = extraDic.get('killTotalCountTarget', 0)
        self.killedTotalCount = extraDic.get('killedTotalCount', 0)
        self.monsterIDsTarget = extraDic.get('monsterIDsTarget', [])
        return

    def killOneMonster(self, spaceNo, monsterId, monsterGBId):
        mapId = formula.fetchMapId(spaceNo)
        LOG_INFO('in TargetMonsters::killOneMonster:begin, ', spaceNo, mapId, self.tgtId, self.dstCnt, self.stepCnt, self.killedTotalCount, self.killMode)
        opResult = False
        completed = False
        if mapId != self.mapId:
            return opResult, completed

        if monsterGBId in self.targetUIDs:
            return opResult, completed
        if self.killMode == 0:
            if monsterId != self.tgtId:
                return opResult, completed

            if self.stepCnt < self.dstCnt:
                self.stepCnt += 1
                self.targetUIDs.append(monsterGBId)
                opResult = True
        elif self.killMode == 1:
            if monsterId not in self.monsterIDsTarget:
                return opResult, completed

            if self.killedTotalCount < self.killTotalCountTarget:
                self.killedTotalCount += 1
                if monsterId == self.tgtId:
                    self.stepCnt += 1
                self.targetUIDs.append(monsterGBId)
                opResult = True

        completed = self.isTargetCompleted()
        LOG_INFO('in TargetMonsters::killOneMonster:end, ', spaceNo, mapId, self.tgtId, self.dstCnt, self.stepCnt, self.killedTotalCount, self.killMode, opResult, completed)

        return opResult, completed

    def checkTargetCompleted(self, *args):
        return self.killOneMonster(*args)

    def isTargetCompleted(self):
        completed = False
        if self.killMode == 0:
            completed = self.stepCnt == self.dstCnt
        elif self.killMode == 1:
            completed = self.killedTotalCount == self.killTotalCountTarget
        return completed

class TaskTargetItems(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_ITEMS

    def __init__(self):
        super(TaskTargetItems, self).__init__()
        self.stepCnt = 0

        self.mapId = 0
        self.srcIdList = 0
        self.srcRatio = 0.0
        self.state = 0  # 0:物品尚未扣除, 1:物品已经扣除

    def initTarget(self, tgtId, dstCnt, srcIdList, srcRatio, mapId, itemCurNum):
        self.tgtId = tgtId
        self.dstCnt = dstCnt
        self.stepCnt = min(itemCurNum, dstCnt)
        self.mapId = mapId
        self.srcIdList = [int(srcId) for srcId in srcIdList]
        self.srcRatio = int(100 * srcRatio)
        self.state = 0

    def initFromTgtObj(self, tgt):
        super(TaskTargetItems, self).initFromTgtObj(tgt)
        self.mapId = tgt.mapId
        self.srcIdList = tgt.srcIdList
        self.srcRatio = tgt.srcRatio
        self.state = tgt.state

    def genExtraStr(self):
        return json.dumps(
            {'mapId': self.mapId, 'srcIdList': self.srcIdList, 'srcRatio': self.srcRatio, 'state': self.state})

    def fromExtraDic(self, extraDic):
        self.mapId = extraDic.get('mapId', 0)
        self.srcIdList = extraDic.get('srcIdList', [])
        self.srcRatio = extraDic.get('srcRatio', 0)
        self.state = extraDic.get('state', 0)
        return

    def gottenItems(self, itemId, num):
        LOG_INFO('in TargetItems::gottenItems:', self.tgtId, self.dstCnt, self.stepCnt)
        opResult = False
        completed = False
        if itemId != self.tgtId:
            return opResult, completed

        if self.stepCnt < self.dstCnt:
            self.stepCnt += num
            opResult = True

        if self.stepCnt >= self.dstCnt:
            completed = True
        return opResult, completed

    def deductItemsSucc(self):
        self.state = 1

    def isTargetCompleted(self):
        return 1 == self.state

    def checkTargetCompleted(self, *args):
        if not self.gottenItems(*args):
            return False
        return self.isTargetCompleted()


class TaskTargetTalkToNPC(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_TALK_NPC

    def __init__(self):
        super(TaskTargetTalkToNPC, self).__init__()
        self.stepCnt = 0

        self.npcIdList = []
        self.dialogIdList = []

    def initTarget(self, npcIdList, dialogIdList, mapId):
        self.tgtId = npcIdList[0]
        self.dstCnt = 1
        self.stepCnt = 0
        self.mapId = mapId

        self.npcIdList = npcIdList
        self.dialogIdList = dialogIdList

    def doTgtTalkToNpc(self, npcId, dialogId):
        LOG_INFO('in TargetTalkToNPC::doTgtTalkToNpc:', npcId, dialogId, self.tgtId)
        dialogId = dialogId // 1000
        if npcId not in self.npcIdList or dialogId not in self.dialogIdList:
            return False
        if self.npcIdList.index(npcId) != self.dialogIdList.index(dialogId):
            return False
        self.stepCnt = self.dstCnt
        return True

    def initFromTgtObj(self, tgt):
        super(TaskTargetTalkToNPC, self).initFromTgtObj(tgt)
        self.npcIdList = [npcId for npcId in tgt.npcIdList]
        self.dialogIdList = [dialogId for dialogId in tgt.dialogIdList]
        self.mapId = tgt.mapId

    def genExtraStr(self):
        return json.dumps({
            'npcIdList': self.npcIdList,
            'dialogIdList': self.dialogIdList,
            'mapId': self.mapId,
        })

    def fromExtraDic(self, extraDic):
        self.npcIdList = extraDic.get('npcIdList', [])
        self.dialogIdList = extraDic.get('dialogIdList', [])
        self.mapId = extraDic.get('mapId', 0)
        return

    def checkTargetCompleted(self, *args):
        return self.doTgtTalkToNpc(*args)


class TaskTargetCollect(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_COLLECT

    def __init__(self):
        super(TaskTargetCollect, self).__init__()
        self.stepCnt = 0
        self.mapId = 0
        return

    def initTarget(self, collectId, dstCnt, mapId):
        self.tgtId = collectId
        self.dstCnt = dstCnt
        self.stepCnt = 0
        self.mapId = mapId
        return

    def genExtraStr(self):
        return json.dumps({'mapId': self.mapId})

    def fromExtraDic(self, extraDic):
        self.mapId = extraDic.get('mapId', 0)

    def initFromTgtObj(self, tgt):
        super(TaskTargetCollect, self).initFromTgtObj(tgt)
        self.mapId = tgt.mapId

    def addCollectNum(self, collectId, gameEntityId, spaceNo=0):
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        if self.tgtId != collectId:
            return False
        if dungeonNo and self.mapId and dungeonNo != self.mapId:
            LOG_WARN('   in Task::addCollectNum, mapId mismatch:', dungeonNo, self.mapId)
            return False

        self.stepCnt += 1
        if self.stepCnt >= self.dstCnt:
            self.stepCnt = self.dstCnt
        return True

    def checkTargetCompleted(self, *args):
        return self.isTargetCompleted()


class TaskTargetReachArea(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_REACH_AREA

    def __init__(self):
        super(TaskTargetReachArea, self).__init__()
        self.stepCnt = 0
        self.dstCnt = 0

        self.mapId = 0
        self.posX = 0.0
        self.posZ = 0.0
        self.width = 0.0
        self.length = 0.0
        self.triggerDis = 0.0
        self.cosTheta = 1.0
        self.sinTheta = 0.0

    def initTarget(self, dstAreaData, rdPoint):
        self.dstCnt = 1
        self.mapId = dstAreaData['MapId']
        self.posX = dstAreaData['X']
        self.posZ = dstAreaData['Z']
        self.width = dstAreaData['Width']
        self.length = dstAreaData['Length']
        self.triggerDis = dstAreaData.get('TriggerDis', 0)
        if self.triggerDis > 0 and rdPoint:
            self.posX = rdPoint[0]
            self.posZ = rdPoint[2]

        _angle = dstAreaData.get('Angles', None)
        if _angle is not None:
            _rad = math.radians(_angle)
            self.cosTheta = math.cos(_rad)
            self.sinTheta = math.sin(_rad)

    def initFromTgtObj(self, tgt):
        super(TaskTargetReachArea, self).initFromTgtObj(tgt)
        self.mapId = tgt.mapId
        if 0 == self.mapId:
            gameengine.panicStack('TASK_TARGET_REACH_AREA, initFromTgtObj mapId is 0')
        self.posX = tgt.posX
        self.posZ = tgt.posZ
        self.width = tgt.width
        self.length = tgt.length
        self.triggerDis = tgt.triggerDis
        self.cosTheta = tgt.cosTheta
        self.sinTheta = tgt.sinTheta

    def genExtraStr(self):
        return json.dumps({
            'mapId': self.mapId,
            'posX': self.posX,
            'posZ': self.posZ,
            'width': self.width,
            'length': self.length,
            'triggerDis': self.triggerDis,
            'cosTheta': self.cosTheta,
            'sinTheta': self.sinTheta,
        })

    def fromExtraDic(self, extraDic):
        self.mapId = extraDic.get('mapId', 0)
        self.posX = extraDic.get('posX', 0.0)
        self.posZ = extraDic.get('posZ', 0.0)
        self.width = extraDic.get('width', 0.0)
        self.length = extraDic.get('length', 0.0)
        self.triggerDis = extraDic.get('triggerDis', 0.0)
        self.cosTheta = extraDic.get('cosTheta', 1.0)
        self.sinTheta = extraDic.get('sinTheta', 0.0)

    def reachArea(self, posX, posZ, forceComplete=False):
        if forceComplete:
            self.stepCnt = self.dstCnt
            return self.isTargetCompleted()

        if self.stepCnt != self.dstCnt:
            if self.isInArea(posX, posZ):
                self.stepCnt = self.dstCnt
        return self.isTargetCompleted()

    def isInArea(self, posX, posZ):
        if self.triggerDis > 0:
            widthDelta = abs(self.posX - posX)
            lenthDelta = abs(self.posZ - posZ)
            if math.pow(widthDelta, 2) + math.pow(lenthDelta, 2) <= math.pow(self.triggerDis + 1, 2):
                return True
        else:
            transX = posX - self.posX
            transZ = posZ - self.posZ
            rotX = transX * self.cosTheta - transZ * self.sinTheta
            rotZ = transX * self.sinTheta + transZ * self.cosTheta

            halfWidth = self.width / 2
            halfLength = self.length / 2
            if abs(rotX) <= halfWidth and abs(rotZ) <= halfLength:
                return True

        return False

    def cliExtra(self):
        return str(self.posX) + ",0," + str(self.posZ)

    def checkTargetCompleted(self, *args):
        return self.reachArea(*args)


class TaskTargetAvatarLevel(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_LEVEL

    def __init__(self):
        super(TaskTargetAvatarLevel, self).__init__()
        self.stepCnt = 1
        self.dstCnt = 0

    def initTarget(self, dstLv):
        LOG_DBG('in initTargetAvatarLevel:', dstLv)
        if dstLv <= 0:
            return
        self.dstCnt = dstLv
        self.stepCnt = 1

    def avatarLevelUp(self, newLv):
        LOG_INFO('in TargetAvatarLevel::avatarLevelUp:', self.dstCnt, newLv)
        if newLv >= self.stepCnt:
            self.stepCnt = newLv
        return self.isTargetCompleted()

    def checkTargetCompleted(self, *args):
        return self.avatarLevelUp(*args)


class TaskTargetCount(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_COUNT

    COMPARE_TYPE_EQUAL = 0 # 数量一定要相等
    COMPARE_TYPE_GREATER = 1 # 计数要大于等于完成值
    COMPARE_TYPE_LESS = 2 # 计数要小于等于完成值
    COMPARE_TYPE_GREATER_EQUAL = 3 # 计数要大于完成值
    COMPARE_TYPE_LESS_EQUAL = 4 # 计数要小于完成值

    def __init__(self):
        super(TaskTargetCount, self).__init__()

    def initTarget(self, tgtId, dstCnt, compType):
        LOG_DBG('in initTargetCount:', tgtId, dstCnt, compType)
        self.tgtId = tgtId
        self.stepCnt = 0
        self.dstCnt = dstCnt

        self.compType = compType
        self.lastTime = 0
        return

    def initFromTgtObj(self, tgt):
        super(TaskTargetCount, self).initFromTgtObj(tgt)
        self.compType = tgt.compType
        self.lastTime = tgt.lastTime

    def genExtraStr(self):
        return json.dumps({'compType': self.compType, 'lastTime': self.lastTime})

    def fromExtraDic(self, extraDic):
        self.compType = extraDic.get('compType', 0)
        self.lastTime = extraDic.get('lastTime', 0)

    def addCnt(self, idx, timeStamp):
        if idx != self.tgtId and timeStamp < self.lastTime:
            return
        self.lastTime = timeStamp
        self.stepCnt += 1
        return self.isTargetCompleted()

    def addMultiCnt(self, idx, cntList):
        for t in cntList:
            self.addCnt(idx, t)
        return self.isTargetCompleted()

    def isTargetCompleted(self):
        if self.compType == self.COMPARE_TYPE_EQUAL and self.stepCnt != self.dstCnt:
            return False
        elif self.compType == self.COMPARE_TYPE_GREATER and self.stepCnt <= self.dstCnt:
            return False
        elif self.compType == self.COMPARE_TYPE_LESS and self.stepCnt >= self.dstCnt:
            return False
        elif self.compType == self.COMPARE_TYPE_GREATER_EQUAL and self.stepCnt < self.dstCnt:
            return False
        elif self.compType == self.COMPARE_TYPE_LESS_EQUAL and self.stepCnt > self.dstCnt:
            return False
        return True

    def setTargetCompleted(self):
        if self.compType == self.COMPARE_TYPE_EQUAL and self.stepCnt != self.dstCnt:
            self.stepCnt = self.dstCnt
        elif self.compType == self.COMPARE_TYPE_GREATER and self.stepCnt <= self.dstCnt:
            self.stepCnt = self.dstCnt + 1
        elif self.compType == self.COMPARE_TYPE_LESS and self.stepCnt >= self.dstCnt:
            self.stepCnt = self.dstCnt - 1
        elif self.compType == self.COMPARE_TYPE_GREATER_EQUAL and self.stepCnt < self.dstCnt:
            self.stepCnt = self.dstCnt + 1
        elif self.compType == self.COMPARE_TYPE_LESS_EQUAL and self.stepCnt > self.dstCnt:
            self.stepCnt = self.dstCnt - 1
        return

    def checkTargetCompleted(self, *args):
        return self.addMultiCnt(*args)


class TaskTargetManual(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_MONSTER_CARD

    def __init__(self):
        super(TaskTargetManual, self).__init__()

    def initTarget(self, tgtId, activated):
        self.tgtId = tgtId
        self.dstCnt = 1
        self.stepCnt = self.dstCnt if activated else 0
        return

    def activeCard(self, tgtId):
        opResult = False
        completed = False
        if self.tgtId != tgtId:
            return opResult, completed
        opResult = True
        self.stepCnt += 1
        if self.stepCnt >= self.dstCnt:
            completed = True
        return opResult, completed

    def checkTargetCompleted(self, *args):
        return self.activeCard(*args)


class TaskTargetRelateTask(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_RELATE_TASK

    def __init__(self):
        super(TaskTargetRelateTask, self).__init__()

    def initTarget(self, taskId, taskStat, taskCurStat):
        self.tgtId = taskId
        self.dstCnt = 1
        self.stepCnt = self.dstCnt if taskStat == taskCurStat else 0
        self.taskStat = taskStat

    def initFromTgtObj(self, tgt):
        super(TaskTargetRelateTask, self).initFromTgtObj(tgt)
        self.taskStat = tgt.taskStat

    def relateTaskReachStat(self, relateTaskId, relateTaskStat):
        if self.tgtId != relateTaskId or self.taskStat != relateTaskStat:
            return False
        self.stepCnt = self.dstCnt
        return True

    def genExtraStr(self):
        return json.dumps({'taskStat': self.taskStat})

    def fromExtraDic(self, extraDic):
        self.taskStat = extraDic.get('taskStat', 0)
        return

    def checkTargetCompleted(self, *args):
        return self.relateTaskReachStat(*args)


class TaskTargetSkillAction(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_ACTION

    def __init__(self):
        super(TaskTargetSkillAction, self).__init__()

    def initTarget(self, actionId, mapId):
        self.tgtId = int(actionId)
        self.stepCnt = 0
        self.dstCnt = 1
        self.mapId = mapId

    def genExtraStr(self):
        return json.dumps({'mapId': self.mapId})

    def fromExtraDic(self, extraDic):
        self.mapId = extraDic.get('mapId', 0)

    def initFromTgtObj(self, tgt):
        super(TaskTargetSkillAction, self).initFromTgtObj(tgt)
        self.mapId = tgt.mapId


class TaskTargetCinemaAction(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_CINEMA

    def __init__(self):
        super(TaskTargetCinemaAction, self).__init__()

    def initTarget(self, cinemaId):
        self.tgtId = int(cinemaId)
        self.stepCnt = 0
        self.dstCnt = 1


class TaskTargetVar(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_VAR

    def __init__(self):
        super(TaskTargetVar, self).__init__()

    def initTarget(self, varFrmId):
        self.tgtId = int(varFrmId)
        self.stepCnt = 0
        self.dstCnt = 1

    def checkVarCond(self, owner, fmlId, paramsStr):
        if dataUtils.checkVariableCond(owner, fmlId, paramsStr):
            self.stepCnt = self.dstCnt
            return self.isTargetCompleted()

    def checkTargetCompleted(self, *args):
        return self.checkVarCond(*args)


class TaskTargetCounter(BaseTarget):
    tgtType = gameconst.TaskTargetType.TASK_TARGET_COUNTER

    def __init__(self):
        super(TaskTargetCounter, self).__init__()
        self.param = ''

    def initTarget(self, tgtId, dstCnt, param, curCnt):
        self.tgtId = tgtId
        self.stepCnt = curCnt
        self.dstCnt = dstCnt
        self.param = param

    def genExtraStr(self):
        return json.dumps({'param': self.param})

    def fromExtraDic(self, extraDic):
        self.param = extraDic.get('param', '')
        return

    def initFromTgtObj(self, tgt):
        super(TaskTargetCounter, self).initFromTgtObj(tgt)
        self.param = tgt.param
        return

    def counter(self, tgtId, param):
        if tgtId != self.tgtId:
            return False
        # if tgtId == TCTTD.couterTargetDic['TaskCounterTargetFengyin'] and int(self.param) != param[0]:
        #     return False
        # elif tgtId == TCTTD.couterTargetDic['TaskCounterTargetActivity'] and int(self.param) != param[0]:
        #     return False
        # elif tgtId == TCTTD.couterTargetDic['TaskCounterTargetXZKY']:
        #     self.stepCnt = min(self.dstCnt, param[0])
        if tgtId == TCTTD.couterTargetDic['TaskCounterTargetUseItem'] and int(self.param) == param[0]:
            self.stepCnt = min(self.dstCnt, self.stepCnt + param[1])
        else:
            if param is tuple:
                self.stepCnt += param[0]
            else:
                self.stepCnt += 1
        return True

    def checkTargetCompleted(self, *args):
        return self.isTargetCompleted()

class BaseTargetFactory(object):
    TgtType2TgtClassMap = {}

    @classmethod
    def createTarget(cls, tgtType, *args):
        tgtClass = cls.TgtType2TgtClassMap.get(tgtType)
        if not tgtClass:
            LOG_ERR('in createTarget, tgtType error:', tgtType, args)
            return
        tgt = tgtClass()
        tgt.initTarget(*args)
        return tgt

    @classmethod
    def createTargetBySavedDic(cls, savedData):
        tgtClass = cls.TgtType2TgtClassMap.get(savedData['tgtType'])
        if not tgtClass:
            gameengine.panicStack('in createTargetBySavedDic, tgtType error:', savedData)
            return
        tgt = tgtClass()
        tgt.fromSavedDict(savedData)
        return tgt

    @classmethod
    def createTargetByObj(cls, tgtObj):
        tgtClass = cls.TgtType2TgtClassMap.get(tgtObj.tgtType)
        if not tgtClass:
            LOG_ERR('in createTargetByObj, tgtType error:', tgtObj.tgtType)
            return
        tgt = tgtClass()
        tgt.initFromTgtObj(tgtObj)
        return tgt


class TaskTgtFactory(BaseTargetFactory):
    TgtType2TgtClassMap = {
        gameconst.TaskTargetType.TASK_TARGET_MONSTERS: TaskTargetMonsters,
        gameconst.TaskTargetType.TASK_TARGET_ITEMS: TaskTargetItems,
        gameconst.TaskTargetType.TASK_TARGET_TALK_NPC: TaskTargetTalkToNPC,
        gameconst.TaskTargetType.TASK_TARGET_REACH_AREA: TaskTargetReachArea,

        gameconst.TaskTargetType.TASK_TARGET_LEVEL: TaskTargetAvatarLevel,
        gameconst.TaskTargetType.TASK_TARGET_COUNT: TaskTargetCount,
        gameconst.TaskTargetType.TASK_TARGET_COLLECT: TaskTargetCollect,
        gameconst.TaskTargetType.TASK_TARGET_MONSTER_CARD: TaskTargetManual,
        gameconst.TaskTargetType.TASK_TARGET_RELATE_TASK: TaskTargetRelateTask,
        gameconst.TaskTargetType.TASK_TARGET_ACTION: TaskTargetSkillAction,
        gameconst.TaskTargetType.TASK_TARGET_CINEMA: TaskTargetCinemaAction,
        gameconst.TaskTargetType.TASK_TARGET_VAR: TaskTargetVar,
        gameconst.TaskTargetType.TASK_TARGET_COUNTER: TaskTargetCounter,
    }
