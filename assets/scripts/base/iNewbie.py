# coding: utf-8
from KBEDebug import *
import KBEngine
import gameconst
import gametimer
import tutorConst_newbieStep as TCNSD
import tutorConst_newbieStep_task2Step as TCNSTD
import gamePlay_gamePlay as GPGPD
import gameengine
import complexTeleportOption
import utils
import math
import formula
import visible_visible as V_VD


class INewbie(object):
    def gmFinishedNewbie(self, stepLimit, delay=1):
        gen = self.newbieIter(stepLimit)
        self._gmFinishedNewbie(gen, delay, stepLimit)

    def _gmFinishedNewbie(self, gen, delay, stepLimit):
        isFinished = False
        for i in range(3):
            ret = next(gen, False)
            if not ret:
                isFinished = True
                break

        if isFinished:
            delay > 0 and self._callback(delay, '_gmNewbieFinishOffline', (), gametimer.TIMER_TAG_GM_NEWBIE_FINISH_OFFLINE)
        else:
            self._callback(0.1, '_gmFinishedNewbie', (gen, delay, stepLimit), gametimer.TIMER_TAG_NEWBIE_GM_ITER)

    def newbieIter(self, stepLimit):
        import dropAward
        import antiAddictCategory_antiAddictCategory_def as AACAACDD

        if not stepLimit:
            stepLimit = max(TCNSD.datas.keys())

        for step, data in TCNSD.datas.items():
            if self.newbieStep <= step < stepLimit:
                taskId = data['taskTag']
                if taskId:
                    _subIds = self.taskInfo.getChildTaskIds(taskId)
                    for subTaskId in _subIds:
                        self.taskInfo.tasks.pop(subTaskId, None)

                    self.taskInfo.tasks.pop(taskId, None)
                    self.taskInfo.taskRecordDic[taskId] = gameconst.TaskStat.TASK_STAT_SUBMITTED
                    if taskId in V_VD.taskDic:
                        self.updateVisibleByList(V_VD.taskDic[taskId])

                    for subTaskId in _subIds:
                        if subTaskId in V_VD.taskDic:
                            self.updateVisibleByList(V_VD.taskDic[subTaskId])
                            self.unlockSkill(True, 0, subTaskId)

                    self.unlockSkill(True, 0, taskId)

                rewardId = data['rewardTag']
                if rewardId:
                    ctx = self._getAvatarAwardCtx(rewardId, None)
                    wealthVal = dropAward.getAward(rewardId, 1, ctx)
                    srcType = AACAACDD.datas.BONUS_SRC_GM
                    opUUID = KBEngine.genUUID64()
                    self.addWealth(srcType, wealthVal, opUUID, None, ctx)

                yield True

        self.newbieStep = stepLimit
        yield False

    def _gmNewbieFinishOffline(self):
        self.backSelectCharacterBase(True)

    def onTaskFinishedForNewbieStep(self, taskId):
        stepId = TCNSTD.datas.get(taskId, 0)
        if not stepId:
            return

        DEBUG_MSG('onTaskFinishedForNewbieStep:', stepId)
        if stepId > self.newbieStep:
            self.newbieStep = stepId
            self.cell.onNewbieStepModify(self.newbieStep)

    def getNewbieLockDun(self):
        stepData = TCNSD.datas.get(self.newbieStep)
        return stepData['lockDun'] if stepData else 0

    def _enterNewbieDungeon(self):
        DEBUG_MSG('newbie will enter', self.newbieStep)
        cellData = self.cellData
        dungeonNo = self.getNewbieLockDun()
        dunData = GPGPD.datas.get(dungeonNo)
        if not dunData:
            ERROR_MSG('_enterNewbieDungeon but dun invalid:', dungeonNo)
            return False

        if not gameconst.DungeonType.isSingleDungeon(dunData['type'], dunData['enterType']):
            ERROR_MSG('_enterNewbieDungeon but dun invalid:', dungeonNo)
            return False

        extra = {'dungeonNo': dungeonNo, 'isNewbie': True, 'spaceLevel': cellData.get("level", 1)}
        gameengine.getDungeonStubByDungeonNo(dungeonNo, gameconst.DungeonEnterType.SINGLE)\
            .applyCreateDungeon(self, self.gbID, 0, extra)
        return True

    def onNewbieDungeonReady(self, spaceBox, spaceMgrBox, spaceMgrId, spaceNo):
        DEBUG_MSG('onNewbieDungeonReady:', spaceMgrId, spaceNo)
        if self.isDestroyed:
            WARNING_MSG('dungeon ready but self destroyed')
            return

        context = {'e': {'spaceMgrBox': spaceMgrBox,
                         'playerBox': self,
                         'playerGbId': self.gbID,
                         'teamUUID': 0,
                         'extra': {}}}
        options = complexTeleportOption.ComplexTeleportOptions()
        callback1, args1 = '_afterEnter_singleDungeon', (spaceNo, spaceNo, options, context)
        self.cellData.setdefault('tempMiscProps', {})
        self.cellData['tempMiscProps'][gameconst.AvatarProps.newbieCreateCellCB] = ((callback1, args1),)
        dstPos, dstDir = self._getNewbieEntrance(formula.getMapId(spaceNo))
        self.cellData['position'] = dstPos
        self.cellData['direction'] = dstDir
        self.cellData['spaceNo'] = spaceNo
        spaceBox.createCellNearSelf(self)

    def _getNewbieEntrance(self, dungeonNo):
        dunSData = utils.getDunStructureModuleData(dungeonNo)
        stepData = TCNSD.datas.get(self.newbieStep)
        if stepData and stepData['taskTag'] and not self.isTaskComplete(stepData['taskTag']) and stepData.get('bornPos'):
            DEBUG_MSG('_getNewbieEntrance, step taskTag not complete:', stepData)
            bornRotation = stepData['bornRotation']
            return stepData.get('bornPos'), (0, 0, bornRotation * math.pi / 180)
        elif 'BornPos' in dunSData:
            d, *_ = dunSData['BornPos'].values()
            return formula.bornPosFromData(d), (0, 0, d['Dir'] * math.pi / 180)
        else:
            gameengine.reportCritical('_getNewbieEntrance but not has pos and dir:', dungeonNo)
            return self.cellData['position'], self.cellData['direction']

    def _claimTaskByNewbieStep(self):
        stepData = TCNSD.datas.get(self.newbieStep)
        if not stepData:
            return

        startTask = stepData['startTask']
        if not startTask:
            return

        DEBUG_MSG('_claimTaskByNewbieStep:', startTask)
        self.baseTaskClaim(startTask, None, False)

    def addNewbieGuideId(self, exposed, newbieGuideId):
        if len(self.newbieGuideIds) > 1000:
            ERROR_MSG('addNewbieGuideId meet max')
            return

        if newbieGuideId in self.newbieGuideIds:
            WARNING_MSG('addNewbieGuideId has added')
            return

        self.newbieGuideIds.append(newbieGuideId)
        self.client.onNewbieGuideId(newbieGuideId)
