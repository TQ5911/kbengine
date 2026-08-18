# -*- encoding:utf-8 -*-

from KBEDebug import *
import json
import formula
import math
import userType
import gameconst
import gameengine
import dataUtils

import taskClass_taskTarget as TCTTD


MAX_JSON_STR_LENGTH = 1024


class BaseTarget(userType.UserSingleType):
    tgtType = gameconst.TaskTargetEnum.TARGET_UNKNOWN

    def __init__(self):
        self.tgtId = 0
        self.stepCnt = 0
        self.dstCnt = 0

    def __getstate__(self):
        return self.toTargetSavedDict()

    def __setstate__(self, state):
        self.__init__()
        self.fromSavedDict(state)

    def genTaskExtraStr(self):
        return ''

    @staticmethod
    def loadsExtraJson(extraJsonStr):
        if not extraJsonStr:
            return {}
        try:
            return json.loads(extraJsonStr)
        except Exception as e:
            gameengine.panicStack('in loadsExtraJson:', e, extraJsonStr)
            return {}

    def fromExtraDic(self, extraStr):
        return

    def cliExtra(self):
        return ''

    def setTaskTargetCompleted(self):
        self.stepCnt = self.dstCnt

    def toClientDict(self):
        return {
            'tgtId': self.tgtId,
            'tgtType': self.tgtType,
            'dstCnt': self.dstCnt,
            'stepCnt': self.stepCnt,
            'cliExtra': self.cliExtra(),
        }

    def toTargetSavedDict(self):
        extraStr = self.genTaskExtraStr()
        if len(extraStr) >= MAX_JSON_STR_LENGTH:
            gameengine.panicStack('toTargetSavedDict, json str reach max limit:', self.__dict__)
        return {
            'tgtId': self.tgtId,
            'tgtType': self.tgtType,
            'stepCnt': self.stepCnt,
            'extraStr': extraStr,
            'dstCnt': self.dstCnt,
        }

    def fromSavedDict(self, dataDic):
        try:
            self.tgtId = dataDic['tgtId']
            self.tgtType = dataDic['tgtType']
            self.dstCnt = dataDic['dstCnt']
            self.stepCnt = dataDic['stepCnt']
            extraDic = self.loadsExtraJson(dataDic['extraStr'])
            self.fromExtraDic(extraDic)
        except Exception as e:
            gameengine.panicStack('in BaseTarget.fromSavedDict:', e)
        return

    def initFromTgtObject(self, tgt):
        self.tgtId = tgt.tgtId
        self.tgtType = tgt.tgtType
        self.dstCnt = tgt.dstCnt
        self.stepCnt = tgt.stepCnt

    @property
    def dungeonNo(self):
        if hasattr(self, 'mapId'):
            return getattr(self, 'mapId')
        else:
            return 0

    def isTaskTargetCompleted(self):
        return self.stepCnt >= self.dstCnt

    def checkTargetCompleted(self, *args):
        return self.isTaskTargetCompleted()


class TaskTargetMonsters(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_MONSTERS

    def __init__(self):
        super(TaskTargetMonsters, self).__init__()
        self.mapId = 0
        self.stepCnt = 0
        self.targetUIDs = []
        self.killMode = 0
        self.killTotalCountTarget = 0
        self.monsterIDsTarget = []
        self.killedTotalCount = 0

    def initTarget(self, tgtId, dstCnt, mapId, killMode, killTotalCount, monsterIDs):
        self.tgtId = tgtId
        self.dstCnt = dstCnt
        self.mapId = mapId
        self.killMode = killMode
        self.killTotalCountTarget = killTotalCount
        self.monsterIDsTarget = list(monsterIDs)

    def initFromTgtObject(self, tgt):
        super(TaskTargetMonsters, self).initFromTgtObject(tgt)
        self.mapId = tgt.mapId

    def genTaskExtraStr(self):
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
        _opResult = False
        completed = False
        if mapId != self.mapId:
            return _opResult, completed

        if monsterGBId in self.targetUIDs:
            return _opResult, completed

        if self.killMode == 0:
            if monsterId != self.tgtId:
                return _opResult, completed

            if self.stepCnt < self.dstCnt:
                self.stepCnt += 1
                self.targetUIDs.append(monsterGBId)
                _opResult = True

        elif self.killMode == 1:
            if monsterId not in self.monsterIDsTarget:
                return _opResult, completed

            if self.killedTotalCount < self.killTotalCountTarget:
                self.killedTotalCount += 1
                if monsterId == self.tgtId:
                    self.stepCnt += 1
                self.targetUIDs.append(monsterGBId)
                _opResult = True

        completed = self.isTaskTargetCompleted()
        LOG_INFO('in TargetMonsters::killOneMonster:end, ', 
                 spaceNo, 
                 mapId, 
                 self.tgtId, 
                 self.dstCnt, 
                 self.stepCnt, 
                 self.killedTotalCount, 
                 self.killMode, 
                 _opResult, 
                 completed)

        return _opResult, completed

    def checkTargetCompleted(self, *args):
        return self.killOneMonster(*args)

    def isTaskTargetCompleted(self):
        completed = False
        if self.killMode == 0:
            completed = self.stepCnt == self.dstCnt
        elif self.killMode == 1:
            completed = self.killedTotalCount == self.killTotalCountTarget
        return completed

class TaskTargetItems(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_ITEMS

    def __init__(self):
        super(TaskTargetItems, self).__init__()
        self.mapId = 0
        self.stepCnt = 0
        self.srcIdList = 0
        self.state = 0  # 0:物品尚未扣除, 1:物品已经扣除
        self.srcRatio = 0.0

    def initTarget(self, tgtId, dstCnt, srcIdList, srcRatio, mapId, itemCurNum):
        self.dstCnt = dstCnt
        self.tgtId = tgtId
        self.stepCnt = min(itemCurNum, dstCnt)
        self.srcIdList = [int(srcId) for srcId in srcIdList]
        self.mapId = mapId
        self.state = 0
        self.srcRatio = int(100 * srcRatio)

    def initFromTgtObject(self, tgt):
        super(TaskTargetItems, self).initFromTgtObject(tgt)
        self.srcIdList = tgt.srcIdList
        self.mapId = tgt.mapId
        self.state = tgt.state
        self.srcRatio = tgt.srcRatio

    def genTaskExtraStr(self):
        return json.dumps(
            {
                'srcIdList': self.srcIdList, 
                'mapId': self.mapId, 
                'state': self.state,
                'srcRatio': self.srcRatio, 
            })

    def fromExtraDic(self, extraDic):
        self.srcIdList = extraDic.get('srcIdList', [])
        self.mapId = extraDic.get('mapId', 0)
        self.state = extraDic.get('state', 0)
        self.srcRatio = extraDic.get('srcRatio', 0)

    def gottenItems(self, itemId, num):
        LOG_INFO('in TargetItems::gottenItems:', self.tgtId, self.dstCnt, self.stepCnt)
        _opResult = False
        _completed = False
        if itemId != self.tgtId:
            return _opResult, _completed

        if self.stepCnt < self.dstCnt:
            self.stepCnt += num
            _opResult = True

        if self.stepCnt >= self.dstCnt:
            _completed = True
        return _opResult, _completed

    def deductItemsSucc(self):
        self.state = 1

    def isTaskTargetCompleted(self):
        return 1 == self.state

    def checkTargetCompleted(self, *args):
        if not self.gottenItems(*args):
            return False
        return self.isTaskTargetCompleted()


class TaskTargetTalkToNPC(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_TALK_NPC

    def __init__(self):
        super(TaskTargetTalkToNPC, self).__init__()
        self.npcIdList = []
        self.dialogIdList = []
        self.stepCnt = 0

    def initTarget(self, npcIdList, dialogIdList, mapId):
        self.tgtId = npcIdList[0]
        self.stepCnt = 0
        self.dstCnt = 1
        self.mapId = mapId

        self.npcIdList = npcIdList
        self.dialogIdList = dialogIdList

    def doTgtTalkToNpc(self, npcId, dialogId):
        LOG_INFO('in TargetTalkToNPC::doTgtTalkToNpc:', npcId, dialogId, self.tgtId)
        dialogId = dialogId // 1000
        if not (npcId in self.npcIdList and dialogId in self.dialogIdList):
            return False

        elif self.npcIdList.index(npcId) != self.dialogIdList.index(dialogId):
            return False

        else:
            self.stepCnt = self.dstCnt
            return True

    def initFromTgtObject(self, tgt):
        super(TaskTargetTalkToNPC, self).initFromTgtObject(tgt)
        self.npcIdList = [_npcId for _npcId in tgt.npcIdList]
        self.dialogIdList = [_dialogId for _dialogId in tgt.dialogIdList]
        self.mapId = tgt.mapId

    def genTaskExtraStr(self):
        return json.dumps({
            'dialogIdList': self.dialogIdList,
            'npcIdList': self.npcIdList,
            'mapId': self.mapId,
        })

    def fromExtraDic(self, extraDic):
        self.dialogIdList = extraDic.get('dialogIdList', [])
        self.npcIdList = extraDic.get('npcIdList', [])
        self.mapId = extraDic.get('mapId', 0)

    def checkTargetCompleted(self, *args):
        return self.doTgtTalkToNpc(*args)


class TaskTargetCollect(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_COLLECT

    def __init__(self):
        super(TaskTargetCollect, self).__init__()
        self.stepCnt = 0
        self.mapId = 0

    def initTarget(self, collectId, dstCnt, mapId):
        self.dstCnt = dstCnt
        self.tgtId = collectId
        self.mapId = mapId
        self.stepCnt = 0

    def genTaskExtraStr(self):
        return json.dumps({'mapId': self.mapId,})

    def fromExtraDic(self, extraDic):
        self.mapId = extraDic.get('mapId', 0)

    def initFromTgtObject(self, tgt):
        super(TaskTargetCollect, self).initFromTgtObject(tgt)
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
        return self.isTaskTargetCompleted()


class TaskTargetReachArea(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_REACH_AREA

    def __init__(self):
        super(TaskTargetReachArea, self).__init__()
        self.dstCnt = 0
        self.stepCnt = 0

        self.mapId = 0
        self.posZ = 0.0
        self.posX = 0.0
        self.width = 0.0
        self.length = 0.0
        self.triggerDis = 0.0
        self.sinTheta = 0.0
        self.cosTheta = 1.0

    def initTarget(self, dstAreaData, rdPoint):
        self.mapId = dstAreaData['MapId']
        self.dstCnt = 1
        self.posX = dstAreaData['X']
        self.posZ = dstAreaData['Z']
        self.length = dstAreaData['Length']
        self.width = dstAreaData['Width']
        self.triggerDis = dstAreaData.get('TriggerDis', 0)
        if self.triggerDis > 0 and rdPoint:
            self.posZ = rdPoint[2]
            self.posX = rdPoint[0]

        _angle = dstAreaData.get('Angles', None)
        if _angle is not None:
            _rad = math.radians(_angle)
            self.cosTheta = math.cos(_rad)
            self.sinTheta = math.sin(_rad)

    def initFromTgtObject(self, tgt):
        super(TaskTargetReachArea, self).initFromTgtObject(tgt)
        self.mapId = tgt.mapId
        if 0 == self.mapId:
            gameengine.panicStack('TASK_TARGET_REACH_AREA, initFromTgtObject mapId is 0')
        self.posZ = tgt.posZ
        self.posX = tgt.posX
        self.width = tgt.width
        self.length = tgt.length
        self.triggerDis = tgt.triggerDis
        self.sinTheta = tgt.sinTheta
        self.cosTheta = tgt.cosTheta

    def genTaskExtraStr(self):
        return json.dumps({
            'posX': self.posX,
            'mapId': self.mapId,
            'posZ': self.posZ,
            'width': self.width,
            'length': self.length,
            'triggerDis': self.triggerDis,
            'sinTheta': self.sinTheta,
            'cosTheta': self.cosTheta,
        })

    def fromExtraDic(self, extraDic):
        self.posX = extraDic.get('posX', 0.0)
        self.mapId = extraDic.get('mapId', 0)
        self.posZ = extraDic.get('posZ', 0.0)
        self.length = extraDic.get('length', 0.0)
        self.width = extraDic.get('width', 0.0)
        self.triggerDis = extraDic.get('triggerDis', 0.0)
        self.sinTheta = extraDic.get('sinTheta', 0.0)
        self.cosTheta = extraDic.get('cosTheta', 1.0)

    def reachArea(self, posX, posZ, isForceComplete=False):
        if isForceComplete:
            self.stepCnt = self.dstCnt
            return self.isTaskTargetCompleted()

        if self.stepCnt != self.dstCnt\
                and self.isInArea(posX, posZ):
            self.stepCnt = self.dstCnt

        return self.isTaskTargetCompleted()

    def isInArea(self, posX, posZ):
        if self.triggerDis > 0:
            _widthDelta = abs(self.posX - posX)
            _lenthDelta = abs(self.posZ - posZ)
            if math.pow(_widthDelta, 2) + math.pow(_lenthDelta, 2) <= math.pow(self.triggerDis + 1, 2):
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
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_LEVEL

    def __init__(self):
        super(TaskTargetAvatarLevel, self).__init__()
        self.dstCnt = 0
        self.stepCnt = 1

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
        return self.isTaskTargetCompleted()

    def checkTargetCompleted(self, *args):
        return self.avatarLevelUp(*args)


class TaskTargetCount(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_COUNT

    COMPARE_TYPE_EQUAL = 0 # 数量一定要相等
    COMPARE_TYPE_GREATER = 1 # 计数要大于等于完成值
    COMPARE_TYPE_LESS = 2 # 计数要小于等于完成值
    COMPARE_TYPE_GREATER_EQUAL = 3 # 计数要大于完成值
    COMPARE_TYPE_LESS_EQUAL = 4 # 计数要小于完成值

    def __init__(self):
        super(TaskTargetCount, self).__init__()

    def initTarget(self, tgtId, dstCnt, compType):
        LOG_DBG('in initTargetCount:', tgtId, dstCnt, compType)
        self.stepCnt = 0
        self.tgtId = tgtId
        self.dstCnt = dstCnt

        self.compType = compType
        self.lastTime = 0

    def initFromTgtObject(self, tgt):
        super(TaskTargetCount, self).initFromTgtObject(tgt)
        self.compType = tgt.compType
        self.lastTime = tgt.lastTime

    def genTaskExtraStr(self):
        return json.dumps({
            'compType': self.compType, 
            'lastTime': self.lastTime,
        })

    def fromExtraDic(self, extraDic):
        self.lastTime = extraDic.get('lastTime', 0)
        self.compType = extraDic.get('compType', 0)

    def addCnt(self, idx, timeStamp):
        if idx != self.tgtId and timeStamp < self.lastTime:
            return
        self.stepCnt += 1
        self.lastTime = timeStamp
        return self.isTaskTargetCompleted()

    def addMultiCnt(self, idx, cntList):
        for t in cntList:
            self.addCnt(idx, t)
        return self.isTaskTargetCompleted()

    def isTaskTargetCompleted(self):
        if self.compType == self.COMPARE_TYPE_EQUAL and self.stepCnt != self.dstCnt:
            return False
        if self.compType == self.COMPARE_TYPE_GREATER and self.stepCnt <= self.dstCnt:
            return False
        if self.compType == self.COMPARE_TYPE_LESS and self.stepCnt >= self.dstCnt:
            return False
        if self.compType == self.COMPARE_TYPE_GREATER_EQUAL and self.stepCnt < self.dstCnt:
           return False
        if self.compType == self.COMPARE_TYPE_LESS_EQUAL and self.stepCnt > self.dstCnt:
            return False
        return True

    def setTaskTargetCompleted(self):
        if self.compType == self.COMPARE_TYPE_EQUAL and self.stepCnt != self.dstCnt:
            self.stepCnt = self.dstCnt
            return
        elif self.compType == self.COMPARE_TYPE_GREATER and self.stepCnt <= self.dstCnt:
            self.stepCnt = self.dstCnt + 1
            return
        elif self.compType == self.COMPARE_TYPE_LESS and self.stepCnt >= self.dstCnt:
            self.stepCnt = self.dstCnt - 1
            return
        elif self.compType == self.COMPARE_TYPE_GREATER_EQUAL and self.stepCnt < self.dstCnt:
            self.stepCnt = self.dstCnt + 1
            return
        elif self.compType == self.COMPARE_TYPE_LESS_EQUAL and self.stepCnt > self.dstCnt:
            self.stepCnt = self.dstCnt - 1
            return

    def checkTargetCompleted(self, *args):
        return self.addMultiCnt(*args)


class TaskTargetManual(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_MONSTER_CARD

    def __init__(self, *args):
        super(TaskTargetManual, self).__init__()

    def initTarget(self, tgtId, activated):
        self.dstCnt = 1
        self.tgtId = tgtId
        self.stepCnt = self.dstCnt if activated else 0

    def activeCard(self, tgtId):
        _opResult = False
        _completed = False
        if self.tgtId != tgtId:
            return _opResult, _completed
        _opResult = True
        self.stepCnt += 1
        if self.stepCnt >= self.dstCnt:
            _completed = True
        return _opResult, _completed

    def checkTargetCompleted(self, *args):
        return self.activeCard(*args)


class TaskTargetRelateTask(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_RELATE_TASK

    def __init__(self, *args):
        super(TaskTargetRelateTask, self).__init__()

    def initTarget(self, taskId, taskStat, taskCurStat):
        self.dstCnt = 1
        self.tgtId = taskId
        self.taskStat = taskStat
        self.stepCnt = self.dstCnt if taskStat == taskCurStat else 0

    def initFromTgtObject(self, tgt):
        super(TaskTargetRelateTask, self).initFromTgtObject(tgt)
        self.taskStat = tgt.taskStat

    def relateTaskReachStat(self, relateTaskId, relateTaskStat):
        if not (self.tgtId == relateTaskId and self.taskStat == relateTaskStat):
            return False
        else:
            self.stepCnt = self.dstCnt
            return True

    def genTaskExtraStr(self):
        return json.dumps({'taskStat': self.taskStat,})

    def fromExtraDic(self, extraDic):
        self.taskStat = extraDic.get('taskStat', 0)
        return

    def checkTargetCompleted(self, *args):
        return self.relateTaskReachStat(*args)


class TaskTargetSkillAction(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_ACTION

    def __init__(self, *args):
        super(TaskTargetSkillAction, self).__init__()

    def initTarget(self, actionId, mapId):
        self.stepCnt = 0
        self.tgtId = int(actionId)
        self.mapId = mapId
        self.dstCnt = 1

    def genTaskExtraStr(self):
        return json.dumps({'mapId': self.mapId,})

    def fromExtraDic(self, extraDic):
        self.mapId = extraDic.get('mapId', 0)

    def initFromTgtObject(self, tgt):
        super(TaskTargetSkillAction, self).initFromTgtObject(tgt)
        self.mapId = tgt.mapId


class TaskTargetCinemaAction(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_CINEMA

    def __init__(self, *args):
        super(TaskTargetCinemaAction, self).__init__()

    def initTarget(self, cinemaId):
        self.stepCnt = 0
        self.tgtId = int(cinemaId)
        self.dstCnt = 1


class TaskTargetVar(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_VAR

    def __init__(self, *args):
        super(TaskTargetVar, self).__init__()

    def initTarget(self, varFrmId):
        self.stepCnt = 0
        self.tgtId = int(varFrmId)
        self.dstCnt = 1

    def checkVarCond(self, owner, fomulaId, paramsStr):
        if dataUtils.checkVariableCond(owner, fomulaId, paramsStr):
            self.stepCnt = self.dstCnt
            return self.isTaskTargetCompleted()

    def checkTargetCompleted(self, *args):
        return self.checkVarCond(*args)


class TaskTargetCounter(BaseTarget):
    tgtType = gameconst.TaskTargetEnum.TASK_TARGET_COUNTER

    def __init__(self, *args):
        super(TaskTargetCounter, self).__init__()
        self.param = ''

    def genTaskExtraStr(self):
        return json.dumps({'param': self.param})

    def initTarget(self, tgtId, dstCnt, param, curCnt):
        self.stepCnt = curCnt
        self.tgtId = tgtId
        self.param = param
        self.dstCnt = dstCnt

    def fromExtraDic(self, extraDic):
        self.param = extraDic.get('param', '')
        return

    def initFromTgtObject(self, tgt):
        super(TaskTargetCounter, self).initFromTgtObject(tgt)
        self.param = tgt.param

    def counter(self, tgtId, param):
        if tgtId != self.tgtId:
            return False
        ids = {
            TCTTD.couterTargetDic['TaskCounterTargetUseItem'],
            TCTTD.couterTargetDic['MakeEquipmentOnce'],
            TCTTD.couterTargetDic['CompleteACertainInstance']
        }
        if tgtId in ids:
            if int(self.param) == param[0]:
                cnt = param[1] if len(param) > 1 else 1
                self.stepCnt = min(self.dstCnt, self.stepCnt + cnt)
            else:
                return False
        else:
            if param is tuple:
                self.stepCnt += param[0]
            else:
                self.stepCnt += 1
        return True

    def checkTargetCompleted(self, *args):
        return self.isTaskTargetCompleted()

class BaseTargetFactory(object):
    TgtType2TgtClassDic = {}

    @classmethod
    def createTarget(cls, tgtType, *args):
        _tgtClass = cls.TgtType2TgtClassDic.get(tgtType)
        if not _tgtClass:
            LOG_ERR('in createTarget, tgtType error:', tgtType, args)
            return
        tgt = _tgtClass()
        tgt.initTarget(*args)
        return tgt

    @classmethod
    def createTargetBySavedDic(cls, savedData):
        _tgtClass = cls.TgtType2TgtClassDic.get(savedData['tgtType'])
        if not _tgtClass:
            gameengine.panicStack('in createTargetBySavedDic, tgtType error:', savedData)
            return
        tgt = _tgtClass()
        tgt.fromSavedDict(savedData)
        return tgt

    @classmethod
    def createTargetByObj(cls, tgtObj):
        tgtClass = cls.TgtType2TgtClassDic.get(tgtObj.tgtType)
        if not tgtClass:
            LOG_ERR('in createTargetByObj, tgtType error:', tgtObj.tgtType)
            return
        tgt = tgtClass()
        tgt.initFromTgtObject(tgtObj)
        return tgt


class TaskTgtFactory(BaseTargetFactory):
    TgtType2TgtClassDic = {
        gameconst.TaskTargetEnum.TASK_TARGET_MONSTERS: TaskTargetMonsters,
        gameconst.TaskTargetEnum.TASK_TARGET_ITEMS: TaskTargetItems,
        gameconst.TaskTargetEnum.TASK_TARGET_TALK_NPC: TaskTargetTalkToNPC,
        gameconst.TaskTargetEnum.TASK_TARGET_REACH_AREA: TaskTargetReachArea,

        gameconst.TaskTargetEnum.TASK_TARGET_LEVEL: TaskTargetAvatarLevel,
        gameconst.TaskTargetEnum.TASK_TARGET_COUNT: TaskTargetCount,
        gameconst.TaskTargetEnum.TASK_TARGET_COLLECT: TaskTargetCollect,
        gameconst.TaskTargetEnum.TASK_TARGET_MONSTER_CARD: TaskTargetManual,
        gameconst.TaskTargetEnum.TASK_TARGET_RELATE_TASK: TaskTargetRelateTask,
        gameconst.TaskTargetEnum.TASK_TARGET_ACTION: TaskTargetSkillAction,
        gameconst.TaskTargetEnum.TASK_TARGET_CINEMA: TaskTargetCinemaAction,
        gameconst.TaskTargetEnum.TASK_TARGET_VAR: TaskTargetVar,
        gameconst.TaskTargetEnum.TASK_TARGET_COUNTER: TaskTargetCounter,
    }
