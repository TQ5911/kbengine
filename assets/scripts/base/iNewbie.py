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
        _gen = self.newbieIter(stepLimit)
        self._gmFinishedNewbie(_gen, delay, stepLimit)

    def _gmFinishedNewbie(self, gen, delay, stepLimit):
        _isFinished = False
        for i in range(3):
            ret = next(gen, False)
            if not ret:
                _isFinished = True
                break

        if _isFinished:
            delay > 0 and self.addTimerCB(delay, '_gmNewbieFinishOffline', (), gametimer.TIMER_TAG_GM_NEWBIE_FINISH_OFFLINE)
        else:
            self.addTimerCB(0.1, '_gmFinishedNewbie', (gen, delay, stepLimit), gametimer.TIMER_TAG_NEWBIE_GM_ITER)

    def newbieIter(self, stepLimit):
        import antiAddictCategory_antiAddictCategory_def as AACAACDD
        import dropAward

        if not stepLimit:
            stepLimit = max(TCNSD.datas.keys())

        for _step, data in TCNSD.datas.items():
            if self.newbieStep <= _step < stepLimit:
                taskId = data['taskTag']
                if taskId:
                    _subIds = self.taskInfo.getChildTaskIds(taskId)
                    for _subTaskId in _subIds:
                        self.taskInfo.tasks.pop(_subTaskId, None)

                    self.taskInfo.tasks.pop(taskId, None)
                    self.taskInfo.taskRecordDic[taskId] = gameconst.TaskStatEnum.TASK_STAT_SUBMITTED
                    if taskId in V_VD.taskDic:
                        self.updateVisibleByList(V_VD.taskDic[taskId])

                    for _subTaskId in _subIds:
                        if _subTaskId in V_VD.taskDic:
                            self.updateVisibleByList(V_VD.taskDic[_subTaskId])
                            self.unlockSkill(True, 0, _subTaskId)

                    self.unlockSkill(True, 0, taskId)

                rewardId = data['rewardTag']
                if rewardId:
                    ctx = self.getAvatarAwardCtx(rewardId, None)
                    _wealthVal = dropAward.getAward(rewardId, 1, ctx)
                    _srcType = AACAACDD.datas.BONUS_SRC_GM
                    opUUID = KBEngine.genUUID64()
                    self.addWealth(_srcType, _wealthVal, opUUID, None, ctx)

                yield True

        self.newbieStep = stepLimit
        yield False

    def _gmNewbieFinishOffline(self):
        self.backSelectCharacterBase(True)

    def onTaskFinishedForNewbieStep(self, taskId):
        stepId = TCNSTD.datas.get(taskId, 0)
        if not stepId:
            return

        LOG_DBG('onTaskFinishedForNewbieStep:', stepId)
        if stepId > self.newbieStep:
            self.newbieStep = stepId
            self.cell.onNewbieStepModify(self.newbieStep)

    def getNewbieLockDun(self):
        stepData = TCNSD.datas.get(self.newbieStep)
        return stepData['lockDun'] if stepData else 0

    def _enterNewbieDungeon(self):
        LOG_DBG('newbie will enter', self.newbieStep)
        _cellData = self.cellData
        dungeonNo = self.getNewbieLockDun()
        dunData = GPGPD.datas.get(dungeonNo)
        if not dunData:
            LOG_ERR('_enterNewbieDungeon but dun invalid:', dungeonNo)
            return False

        if not gameconst.DungeonTypeJudge.isSingleDungeon(dunData['type'], dunData['enterType']):
            LOG_ERR('_enterNewbieDungeon but dun invalid:', dungeonNo)
            return False

        extra = {'dungeonNo': dungeonNo, 'isNewbie': True, 'spaceLevel': _cellData.get("level", 1)}
        gameengine.getDungeonStubByDungeonNo(dungeonNo, gameconst.DungeonEnterTypeEnum.SINGLE)\
            .applyCreateDungeon(self, self.gbID, 0, extra)
        return True

    def onNewbieDungeonReady(self, spaceBox, spaceMgrBox, spaceMgrId, spaceNo):
        LOG_DBG('onNewbieDungeonReady:', spaceMgrId, spaceNo)
        if self.isDestroyed:
            LOG_WARN('dungeon ready but self destroyed')
            return

        _context = {
            'e': {
                'spaceMgrBox': spaceMgrBox,
                'playerGbId': self.gbID,
                'playerBox': self,
                'teamUUID': 0,
                'extra': {},
            }
        }
        options = complexTeleportOption.ComplexTeleportOpt()
        callback1, args1 = '_afterEnter_singleDungeon', (spaceNo, spaceNo, options, _context)
        self.cellData.setdefault('tempMiscProps', {})
        self.cellData['tempMiscProps'][gameconst.EntityPropsEnum.newbieCreateCellCB] = ((callback1, args1),)
        _dstPos, dstDir = self._getNewbieEntrance(formula.fetchMapId(spaceNo))
        self.cellData['position'] = _dstPos
        self.cellData['direction'] = dstDir
        self.cellData['spaceNo'] = spaceNo
        spaceBox.createCellNearSelf(self)

    def _getNewbieEntrance(self, dungeonNo):
        dunSData = utils.getDunStructModData(dungeonNo)
        _stepData = TCNSD.datas.get(self.newbieStep)
        if _stepData and _stepData['taskTag']\
                and not self.isTaskComplete(_stepData['taskTag'])\
                and _stepData.get('bornPos'):

            LOG_DBG('_getNewbieEntrance, step taskTag not complete:', _stepData)
            _bornRotation = _stepData['bornRotation']
            return _stepData.get('bornPos'), (0, 0, _bornRotation * math.pi / 180)
        elif 'BornPos' in dunSData:
            d, *_ = dunSData['BornPos'].values()
            return formula.bornPosFromDunData(d), (0, 0, d['Dir'] * math.pi / 180)
        else:
            gameengine.panicStack('_getNewbieEntrance but not has pos and dir:', dungeonNo)
            return self.cellData['position'], self.cellData['direction']

    def _claimTaskByNewbieStep(self):
        stepData = TCNSD.datas.get(self.newbieStep)
        if not stepData:
            return

        startTask = stepData['startTask']
        if not startTask:
            return

        LOG_DBG('_claimTaskByNewbieStep:', startTask)
        self.baseTaskClaim(startTask, None, False)

    def setNewbieGuideId(self, exposed, newbieGuideId, val):
        if len(self.newbieGuideIds) > 100:
            LOG_ERR('setNewbieGuideId meet max')

        for _idx, _id in enumerate(self.newbieGuideIds):
            if _id == newbieGuideId:
                self.newbieGuideVals[_idx] = val
                break

        else:
            self.newbieGuideIds.append(newbieGuideId)
            self.newbieGuideVals.append(val)


        self.client.onNewbieGuideId(newbieGuideId, val)
