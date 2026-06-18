# coding: utf-8
# ----------------------------------------------
# EVENTS
# ----------------------------------------------
from KBEDebug import *
import KBEngine

import gameengine
import gametimer
import gamemove
import gameconst
import gametimer
import random
import utils
import math
import formula

import ep_ctrl

import userType

import gamePlay_gamePlay as DDI
import creep_base as CBD
import skill_skill as SSD
import buff_buff as BUFF
import NPC_NPC as NPC_DATA

__all__ = [
    'FlowNodeEvent',
    'FlowRandomNodeEvent',
    'ForLoopEvent',
    'ForLoopWithBreakEvent',
    'WhileLoopEvent',
    'DelayExecEvent',

    'DelayDungeonEndEvent',
    'WaitingTaskCompleteEvent',
    'WaitingTaskFailureEvent',
    'WaitingTaskInProgressEvent',
    'DungeonMonsterReleaseEvent',
    'DungeonNPCReleaseEvent',
    'DungeonCollectionReleaseEvent',
    'DungeonCollectionBeCollectedEvent',
    'DungeonMultiCollectionAllBeCollectedEvent',
    'DungeonAirWallReleaseEvent',
    'DungeonTeleporterReleaseEvent',
    'AIEnterAttackEvent',
    'AILeaveAttackEvent',
    'DungeonMoveEntityToFixPosEvent',
    'MonsterHpMonitorTriggerEvent',
    'MonsterRestNumberEvent',
    'DungeonMonsterKillerNumberEvent',
    'DungeonAlivePlayerEvent',
    'DungeonAnyPlayerHPMonitorTriggerEvent',
    'DungeonValueCheckHoldEvent',
    'DungeonPlayerRestNumEvent',

    'DungeonEntityImmuneDeath',
    'EntityRouteFinishedEvent',
    'EntityRoutingMissingEscortEvent',

    'AnyPlayerCinemaPlayEndedEvent',

    'getCommonReleaseKey',
    'DungeonRebornPosReleaseEvent',
    'DungeonInnerDemonReleaseEvent',
]


def getCommonReleaseKey(eventId, entityGIDs):
    return 'common_release_{}_{}'.format(eventId, '_'.join((str(i) for i in entityGIDs)))


class _GroupEventMixin(object):

    def makeEventGroup(self, *events):
        self.eGroup = events


class _DelayCancelMixin(object):

    def cancelDelay(self, ctx, tag):
        tid = ctx.tid
        if tid not in self._timerDict:
            return
        self.controller.owner.cancelTimerCB(self._timerDict[tid], tag)
        del self._timerDict[tid]


class _WaitingCancelMixin(object):

    def cancelWait(self, ctx):
        key = self.fetchWaitingKey(ctx)
        ctrl = self.controller
        _popList = []
        if key in ctrl.waitingsDict:
            for idx, (e, eCtx) in enumerate(ctrl.waitingsDict[key]):
                if eCtx.tid == ctx.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                ctrl.waitingsDict[key].pop(i)


class _ElementHotReloadMixin(userType.UserSingleType):

    def _lateReload(self):
        import inspect
        import sys
        LOG_DBG('  |--  {}::_lateReload: {}'.format(self.__class__.__name__, self.id))
        for v in self.paramsDict.values():
            if callable(v) and not inspect.isfunction(v):
                LOG_DBG('    |-- {}::_lateReload param\'s method: {} id: [{}]'.format(
                    self.classname(), v.__name__, self.id))
                utils.resetClass(v.__self__)
            else:
                getattr(v, 'reloadScript', utils.emptyFunc)()

        if isinstance(self, ep_ctrl.event.BaseEvent):
            LOG_DBG('    |-- {}::_lateReload param\'s handler: {} id: [{}]'.format(
                    self.classname(), self._handlerFunc.__name__, self.id))
            self._handlerFunc = getattr(sys.modules[self._handlerFunc.__module__], self._handlerFunc.__name__)


class FlowNodeEvent(ep_ctrl.event.Event, _ElementHotReloadMixin):
    """subclass for Event"""


class FlowRandomNodeEvent(ep_ctrl.event.RandomEvent, _ElementHotReloadMixin):
    """subclass for random event"""


class ForLoopEvent(ep_ctrl.flow.BaseForLoop, _ElementHotReloadMixin, _DelayCancelMixin, _GroupEventMixin):

    __selfParams__ = ('delayTime', )

    def __init__(self, *args, **kwargs):
        super(ForLoopEvent, self).__init__(*args, **kwargs)
        self._timerDict = {}

    @property
    def timerTag(self):
        return gametimer.TIMER_TAG_FLOW_CONTROLLER_DELAY_CALLBACK

    def next(self, ctx, **refParams):
        if self._looping_counters[ctx.tid] > self.getLastIndex():
            self._handle_looping(self, self, ctx, **refParams)
            return
        delayTime = self.fetchArgument('delayTime', 0.1) or 0.1
        _spaceMgr = self.controller.owner
        if ctx.tid in self._timerDict:
            _spaceMgr.cancelTimerCB(self._timerDict[ctx.tid], self.timerTag)
        self._timerDict[ctx.tid] = _spaceMgr.addTimerCB(
            delayTime, 'flowControllerDelayCallback',
            (self, '_handle_looping', (self, self, ctx), refParams), self.timerTag)

    def _handle_looping(self, this, srcE, ctx, **refParams):
        self._timerDict.pop(ctx.tid, None)
        super(ForLoopEvent, self)._handle_looping(self, srcE, ctx, **refParams)

    def cancelDelay(self, ctx):
        tid = ctx.tid
        super(ForLoopEvent, self).cancelDelay(ctx, self.timerTag)
        self._looping_counters.pop(tid, None)


class ForLoopWithBreakEvent(ep_ctrl.flow.BaseForLoopWithBreak, _ElementHotReloadMixin, _DelayCancelMixin):

    __selfParams__ = ('delayTime', )

    def __init__(self, *args, **kwargs):
        super(ForLoopWithBreakEvent, self).__init__(*args, **kwargs)
        self._timerDict = {}

    @property
    def timerTag(self):
        return gametimer.TIMER_TAG_FLOW_CONTROLLER_DELAY_CALLBACK

    def next(self, ctx, **refParams):
        delayTime = self.fetchArgument('delayTime', 0.1)
        _spaceMgr = self.controller.owner
        if ctx.tid in self._timerDict:
            _spaceMgr.cancelTimerCB(self._timerDict[ctx.tid], self.timerTag)
        self._timerDict[ctx.tid] = _spaceMgr.addTimerCB(
            delayTime, 'flowControllerDelayCallback',
            (self, '_handle_looping', (self, self, ctx), refParams), self.timerTag)

    def _handle_looping(self, this, srcE, ctx, **refParams):
        self._timerDict.pop(ctx.tid, None)
        super(ForLoopWithBreakEvent, self)._handle_looping(self, srcE, ctx, **refParams)

    def cancelDelay(self, ctx):
        tid = ctx.tid
        super(ForLoopWithBreakEvent, self).cancelDelay(ctx, self.timerTag)
        self._looping_counters.pop(tid, None)


class WhileLoopEvent(ep_ctrl.flow.BaseWhileLoop, _ElementHotReloadMixin, _DelayCancelMixin):

    __selfParams__ = ('delayTime', )

    def __init__(self, *args, **kwargs):
        super(WhileLoopEvent, self).__init__(*args, **kwargs)
        self._timerDict = {}

    @property
    def timerTag(self):
        return gametimer.TIMER_TAG_FLOW_CONTROLLER_DELAY_CALLBACK

    def next(self, ctx, **refParams):
        delayTime = self.fetchArgument('delayTime', 0.1)
        _spaceMgr = self.controller.owner
        if ctx.tid in self._timerDict:
            _spaceMgr.cancelTimerCB(self._timerDict[ctx.tid], self.timerTag)
        self._timerDict[ctx.tid] = _spaceMgr.owner.addTimerCB(
            delayTime, 'flowControllerDelayCallback',
            (self, '_handle_looping', (self, self, ctx), refParams), self.timerTag)

    def _handle_looping(self, this, srcE, ctx, **refParams):
        self._timerDict.pop(ctx.tid, None)
        super(WhileLoopEvent, self)._handle_looping(self, srcE, ctx, **refParams)

    def cancelDelay(self, ctx):
        super(WhileLoopEvent, self).cancelDelay(ctx, self.timerTag)


class DelayExecEvent(ep_ctrl.event.BaseDelayedEvent, _ElementHotReloadMixin, _DelayCancelMixin, _GroupEventMixin):

    def __init__(self, *args, **kwargs):
        self._timerDict = {}
        super(DelayExecEvent, self).__init__(*args, **kwargs)

    @property
    def timerTag(self):
        return gametimer.TIMER_TAG_FLOW_CONTROLLER_DELAY_EXECEVENT_CALLBACK

    def next(self, ctx, **refParams):
        _spaceMgr = self.controller.owner
        if ctx.tid in self._timerDict:
            _spaceMgr.cancelTimerCB(self._timerDict[ctx.tid], self.timerTag)
        self._timerDict[ctx.tid] = _spaceMgr.addTimerCB(
            self._delay_time, 'flowControllerDelayExecEventCallback', (self, ctx), self.timerTag)


    def handleBeTriggeredAfterDelay(self, obj):
        self._timerDict.pop(obj.tid, None)
        super(DelayExecEvent, self).handleBeTriggeredAfterDelay(obj)

    def cancelDelay(self, ctx):
        super(DelayExecEvent, self).cancelDelay(ctx, self.timerTag)


class DelayDungeonEndEvent(DelayExecEvent):

    def __init__(self, eventId, controller, dungeonNo, spaceNo, delayTime, preDelayTime,
                 isFail=False, eventHandler=None, **kwargs):
        super(DelayDungeonEndEvent, self).__init__(
            eventId, controller, eventHandler, delay_time=preDelayTime, **kwargs)
        self.putArgument('dungeonNo', dungeonNo)
        self.putArgument('spaceNo', spaceNo)
        self.putArgument('delayTime', delayTime)
        self.putArgument('preDelayTime', preDelayTime)
        self.putArgument('isFail', isFail)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        spaceNo = self.fetchArgument('spaceNo')
        preDelayTime = self.fetchArgument('preDelayTime')
        _sendTime = int(utils.curTS() + preDelayTime)
        self.controller.owner.syncPlayer(lambda box: box.client.changeDungeonRemainTime(spaceNo, _sendTime))
        super(DelayDungeonEndEvent, self).handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)

    def handleBeTriggeredAfterDelay(self, obj):
        from ._controller import handleEndDungeon

        handleEndDungeon(self, self, obj, **self._pkg_all_ref_params())
        super(DelayDungeonEndEvent, self).handleBeTriggeredAfterDelay(obj)


class WaitingTaskCompleteEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, eventId, controller, task_id, checknow, checkOnce, eventHandler=None, **kwargs):
        super(WaitingTaskCompleteEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('taskId', task_id)
        self.putArgument('checkNow', checknow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        super(WaitingTaskCompleteEvent, self).handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)
        checkNow = self.fetchArgument('checkNow')
        checkOnce = self.fetchArgument('checkOnce')
        taskId = self.fetchArgument('taskId')
        if (checkNow or checkOnce) and taskId:
            spaceMgr = self.controller.owner
            if spaceMgr:
                _args = (taskId, self.id, gameconst.TaskStatEnum.TASK_STAT_SUBMITTED, checkOnce)
                spaceMgr.syncPlayer(lambda box: box.base.getTaskCurrentState(taskId, box, 'flowCtrlIsTaskCompleteCallback', _args))

    def fetchWaitingKey(self, ctx):
        return self.getTaskKey(self.fetchArgument('taskId', 0))

    @staticmethod
    def getTaskKey(task_id):
        return 'task_finish_{}'.format(task_id)


class WaitingTaskFailureEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):
    def __init__(self, eventId, controller, task_id, checknow, checkOnce, eventHandler=None, **kwargs):
        super(WaitingTaskFailureEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('taskId', task_id)
        self.putArgument('checkNow', checknow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        super(WaitingTaskFailureEvent, self).handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)
        checkNow = self.fetchArgument('checkNow')
        checkOnce = self.fetchArgument('checkOnce')
        taskId = self.fetchArgument('taskId')
        if not ((checkNow or checkOnce) and taskId):
            return

        spaceMgr = self.controller.owner
        if not spaceMgr:
            return

        _innerArgs = (taskId, self.id, gameconst.TaskStatEnum.TASK_STAT_FAILED, checkOnce)
        spaceMgr.syncPlayer(lambda box: box.base.getTaskCurrentState(taskId, box, 'flowCtrlIsTaskCompleteCallback', _innerArgs))

    def fetchWaitingKey(self, ctx):
        return self.getTaskKey(self.fetchArgument('taskId', 0))

    @staticmethod
    def getTaskKey(task_id):
        return 'task_failure_{}'.format(task_id)


class WaitingTaskInProgressEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):
    def __init__(self, eventId, controller, task_id, checknow, checkOnce, eventHandler=None, **kwargs):
        super(WaitingTaskInProgressEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('taskId', task_id)
        self.putArgument('checkNow', checknow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        super(WaitingTaskInProgressEvent, self).handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)
        checkNow = self.fetchArgument('checkNow')
        checkOnce = self.fetchArgument('checkOnce')
        taskId = self.fetchArgument('taskId')
        if not ((checkNow or checkOnce) and taskId):
            return

        spaceMgr = self.controller.owner
        if not spaceMgr:
            return

        _args = (taskId, self.id, gameconst.TaskStatEnum.TASK_STAT_RUNNING, checkOnce)
        spaceMgr.syncPlayer(lambda box: box.base.getTaskCurrentState(taskId, box, 'flowCtrlIsTaskCompleteCallback', _args))

    def fetchWaitingKey(self, ctx):
        return self.getTaskKey(self.fetchArgument('taskId', 0))

    @staticmethod
    def getTaskKey(task_id):
        return 'task_inprogress_{}'.format(task_id)

class DungeonInnerDemonReleaseEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('innerDemonGIDs',)
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, eventId, controller, innerDemonGIDs, eventHandler=None, **kwargs):
        super(DungeonInnerDemonReleaseEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('innerDemonGIDs', innerDemonGIDs)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        dungeonNo = refParams['dungeonNo']     # dungeonNo get from ref
        spaceNo = refParams['spaceNo']
        innerDemonGIDs = self.fetchArgument('innerDemonGIDs')
        overwriteProps = self.fetchArgument('overwriteProps', {})
        ifSetBoss = self.fetchArgument('ifSetBoss', False)
        initState = self.fetchArgument('initState', 0)
        spaceMgr = self.controller.owner
        dunAllDatas = utils.getDunModuleData(dungeonNo)
        
        LOG_WARN("DungeonInnerDemonReleaseEvent", overwriteProps, innerDemonGIDs, dungeonNo, spaceNo, spaceMgr.dungeonPlayMode)
        if len(innerDemonGIDs) != 1:
            LOG_ERR('DungeonInnerDemonReleaseEvent:: no entityId', spaceMgr.spaceNo, dungeonNo, self.id, innerDemonGIDs)
            return
        if not dunAllDatas:
            LOG_ERR('DungeonInnerDemonReleaseEvent:: no dunAllDatas', spaceMgr.spaceNo, dungeonNo, self.id, innerDemonGIDs)
            return
        flagId = innerDemonGIDs[0]
        dunData = dunAllDatas.get(str(flagId), {})
        if not dunData:
            LOG_ERR('handleReleaseInnerDemon:: no dunData', flagId)
            return
        
        position = (dunData['PosX'], dunData['PosY'], dunData['PosZ'])
        direction = (0.0, 0.0, dunData['Dir'] * math.pi / 180)

        for pid in spaceMgr.players:
            _ent = KBEngine.entities.get(pid)
            if not _ent:
                continue

            cloneProps = _ent.cloneAvatarProps(gameconst.AVATAR_REPLICA_TYPE_INNER_DEMON)
            if True:
                dunDataProps = dunData.get('Props', {})
                mProps = {
                    'spaceNo': spaceNo,
                    'replicaId': dunData['EntityID'],
                    'spaceMgrId': spaceMgr.id,
                    'spaceMgrBox': spaceMgr,
                    'position': position,
                    'direction': direction,
                    'aiName': 0,
                    'pathId': dunDataProps.get('PathID', 0) or 0,
                    'dungeonFlagId': flagId,
                    'gameEntityId': next(utils.genGameEntityId(flagId, 1), 0),
                    'gameEntityIdentifyID': 0,
                    'isBoss': ifSetBoss,
                    'bornState': gameconst.BornStateEnum.flowConvTup[initState] if initState else gameconst.BornStateEnum.none,
                    'isBossHasSetFlag': True,
                    'belongActId': dunData.get('ActivityID', 0),
                    'instanceId': dunData.get('ID'),
                }
                mProps.update(cloneProps)
                #mProps['name'] = mProps.get('avatarName', "") + dunData['DisplayName']
                mProps['name'] = dunData['DisplayName']

                mProps['tmpProps'] = {}
                mProps['tmpProps']['overwriteProps'] = overwriteProps
                for k, v in mProps.items():
                    LOG_DBG("DungeonInnerDemonReleaseEvent genAvatarReplica mProps", k, v)
                spaceMgr.getCurrentSpace().createCellLocally('AvatarReplica', position, direction, mProps)
            else:
                stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
                stub.spawnDungeonEntityByGameEntityId(spaceNo, innerDemonGIDs, 1, _ent.level,
                                                     {'overwriteProps': overwriteProps, 'ifSetBoss': ifSetBoss,
                                                      'initState': initState, 'eventId': self.id, 'cloneProps': cloneProps})

        super(DungeonInnerDemonReleaseEvent, self).handleProcessActivated(
            srcE, srcIdx, idx, obj, **refParams)
        spaceMgr.flowCtrrlDungeonEntityReleaseCompleteByEventId(innerDemonGIDs, self.id)

    def fetchWaitingKey(self, ctx):
        return self.getInnerDemonReleaseKey(self.id, self.fetchArgument('innerDemonGIDs', []))

    @staticmethod
    def getInnerDemonReleaseKey(eventId, innerDemonGIDs):
        return getCommonReleaseKey(eventId, innerDemonGIDs)

class DungeonMonsterReleaseEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('monsterGIDs', 'monsterNum', 'monsterLevel')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, eventId, controller, monsterGIDs, eventHandler=None, **kwargs):
        super(DungeonMonsterReleaseEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('monsterGIDs', monsterGIDs)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        dungeonNo = refParams['dungeonNo']     # dungeonNo get from ref
        spaceNo = refParams['spaceNo']
        monsterGIDs = self.fetchArgument('monsterGIDs', [])
        monsterNum = self.fetchArgument('monsterNum', 1)
        monsterLevel = self.fetchArgument('monsterLevel', 0)
        overwriteProps = self.fetchArgument('overwriteProps', {})
        ifSetBoss = self.fetchArgument('ifSetBoss', False)
        initState = self.fetchArgument('initState', 0)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        _id = self.id
        stub.spawnDungeonEntityByGameEntityId(spaceNo, monsterGIDs, monsterNum, monsterLevel,
                                                 {'overwriteProps': overwriteProps, 'ifSetBoss': ifSetBoss,
                                                  'initState': initState, 'eventId': _id})
        super(DungeonMonsterReleaseEvent, self).handleProcessActivated(
            srcE, srcIdx, idx, obj, **refParams)

    def fetchWaitingKey(self, ctx):
        return self.getMonsterReleaseKey(self.id, self.fetchArgument('monsterGIDs', []))

    @staticmethod
    def getMonsterReleaseKey(eventId, monsterGIDs):
        return getCommonReleaseKey(eventId, monsterGIDs)


class DungeonNPCReleaseEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('npcGIDs', 'npcNum', 'npcLevel')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, eventId, controller, npcGIDs, eventHandler=None, **kwargs):
        super(DungeonNPCReleaseEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('npcGIDs', npcGIDs)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        dungeonNo = refParams['dungeonNo']
        spaceNo = refParams['spaceNo']
        npcGIDs = self.fetchArgument('npcGIDs', [])
        npcNum = self.fetchArgument('npcNum', 1)
        npcLevel = self.fetchArgument('npcLevel', 0)
        ifSetBoss = self.fetchArgument('ifSetBoss', False)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.spawnDungeonEntityByGameEntityId(spaceNo, npcGIDs, npcNum, npcLevel,
                                                 {'ifSetBoss': ifSetBoss, 'eventId': self.id})
        super(DungeonNPCReleaseEvent, self).handleProcessActivated(
            srcE, srcIdx, idx, obj, **refParams)

    def fetchWaitingKey(self, ctx):
        return self.getNpcReleaseKey(self.id, self.fetchArgument('npcGIDs', []))

    @staticmethod
    def getNpcReleaseKey(eventId, npcGIDs):
        return getCommonReleaseKey(eventId, npcGIDs)


class DungeonCollectionReleaseEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('collGIDs', 'collNum', 'randomCollectionNum', 'checkHaveInFixed')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, eventId, controller, collGIDs, eventHandler=None, **kwargs):
        super(DungeonCollectionReleaseEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('collGIDs', collGIDs)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _spaceNo = refParams['spaceNo']
        _collGIDs = self.fetchArgument('collGIDs', [])
        _collNum = self.fetchArgument('collNum', 1)
        LOG_DBG("handleProcessActivated begin ", _collGIDs)
        _randomCollectionNum = self.fetchArgument('randomCollectionNum', 0)
        checkHaveInFixed = self.fetchArgument('checkHaveInFixed', False)
        if _randomCollectionNum and len(_collGIDs) >= _randomCollectionNum:
            _collGIDs = random.sample(_collGIDs, _randomCollectionNum)

        _spaceMgr = self.controller.owner
        if checkHaveInFixed:
            for _entity in _spaceMgr.listEntitiesByTag("Collection"):
                gid = utils.parseGidFromGameEntityId(_entity.gameEntityId)
                if gid in _collGIDs:
                    _collGIDs.remove(gid)

            if not len(_collGIDs):
                LOG_WARN("DungeonCollectionReleaseEvent not _collGIDs")
                return

        stub = gameengine.getDungeonStubBySpaceNo(_spaceNo)
        stub.spawnDungeonEntityByGameEntityId(_spaceNo, _collGIDs, _collNum, 0,
                                                 {'eventId': self.id})
        super(DungeonCollectionReleaseEvent, self).handleProcessActivated(
            srcE, srcIdx, idx, obj, **refParams)

    def fetchWaitingKey(self, ctx):
        return self.getCollReleaseKey(self.id, self.fetchArgument('collGIDs', []))

    @staticmethod
    def getCollReleaseKey(eventId, collGIDs):
        return getCommonReleaseKey(eventId, collGIDs)


class DungeonCollectionBeCollectedEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('collGIDs', )

    def __init__(self, eventId, controller, collGIDs, checkNow, checkOnce, eventHandler=None, **kwargs):
        super().__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('collGIDs', collGIDs)
        self.putArgument('checkNow', checkNow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)
        _collGIDs = self.fetchArgument('collGIDs')

        usePrototypeID = self.fetchArgument('usePrototypeID', False)
        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce')
        if not (checkOnce or checkNow):
            for _collGID in _collGIDs:
                _collGID = "cbid{}".format(_collGID) if usePrototypeID else _collGID
                self._controller.waitingForDungeonCollectionBeCollectedTrigger(self, ctx, _collGID)

        else:
            _spaceMgr = self.controller.owner
            _isCollected = False
            for _collGID in _collGIDs:
                _collGID = "cbid{}".format(_collGID) if usePrototypeID else _collGID
                _collNum = _spaceMgr.collBeCollectedDic.get(_collGID, 0)
                if _collNum > 0:
                    _isCollected = True
                    break

            if _isCollected:
                self.continueHandleBeTriggered(ctx)

            elif checkNow:
                for _collGID in _collGIDs:
                    _collGID = "cbid{}".format(_collGID) if usePrototypeID else _collGID
                    self._controller.waitingForDungeonCollectionBeCollectedTrigger(self, ctx, _collGID)

            else:
                LOG_WARN("DUNGEON FLOW -- EVENT[{}]: collection be collected checkonce failed --"
                            " _collGIDs={}".format(self.id, _collGIDs, usePrototypeID))

    def reHandleBeTriggered(self, srcE, srcIdx, idx, obj, **refParams):
        self.handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)

    def cancelWait(self, context):
        m_collGIDs = self.fetchArgument('collGIDs', [])

        ctrl = self.controller

        for i_collGID in m_collGIDs:
            _popList = []
            _eventList = ctrl.waitingsDict.get(ctrl.GLOBAL_EVENT_KEY, {}).get(
                ctrl.DUNGEON_COLLECTIBLE_KEY, {}).get(i_collGID)

            if not _eventList:
                continue

            for idx, (e, eCtx) in enumerate(_eventList):
                if eCtx.tid == context.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                _eventList.pop(i)


class DungeonMultiCollectionAllBeCollectedEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('collGIDs', )

    def __init__(self, eventId, controller, collGIDs, eventHandler=None, **kwargs):
        super().__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('collGIDs', collGIDs)
        self._collectDict = {i: False for i in collGIDs}

    def collected(self, collGID):
        if collGID in self._collectDict:
            self._collectDict[collGID] = True

    def hasAllCollected(self):
        return all(self._collectDict.values())
    # ----------------------------------------------

    def reHandleBeTriggered(self, srcE, srcIdx, idx, obj, **refParams):
        self._collectDict = {i: False for i in self._collectDict}
        self.handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)

        m_collGIDs = self.fetchArgument('collGIDs')
        for i_collGID in m_collGIDs:
            self._controller.waitingForDungeonMultiCollectionAllBeColllected(self, ctx, i_collGID)

    def cancelWait(self, ctx):
        m_collGIDs = self.fetchArgument('collGIDs', [])

        ctrl = self.controller

        for i_collGID in m_collGIDs:
            _popList = []
            _eventList = ctrl.waitingsDict.get(ctrl.GLOBAL_EVENT_KEY, {}).get(
                ctrl.DUNGEON_MULTI_BE_COLLTECT_KEY, {}).get(i_collGID)

            if not _eventList:
                continue

            for idx, (e, eCtx) in enumerate(_eventList):
                if eCtx.tid == ctx.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                _eventList.pop(i)


class DungeonAirWallReleaseEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('airWallGIDs', 'airWallNum')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, eventId, controller, airWallGIDs, eventHandler=None, **kwargs):
        super(DungeonAirWallReleaseEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('airWallGIDs', airWallGIDs)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        dungeonNo = refParams['dungeonNo']
        spaceNo = refParams['spaceNo']
        airWallGIDs = self.fetchArgument('airWallGIDs', [])
        airWallNum = self.fetchArgument('airWallNum', 1)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.spawnDungeonEntityByGameEntityId(spaceNo, airWallGIDs, airWallNum, 0,
                                                 {'eventId': self.id})
        super(DungeonAirWallReleaseEvent, self).handleProcessActivated(
            srcE, srcIdx, idx, obj, **refParams)

    def fetchWaitingKey(self, ctx):
        return self.getCollReleaseKey(self.id, self.fetchArgument('airWallGIDs', []))

    @staticmethod
    def getCollReleaseKey(eventId, airWallGIDs):
        return getCommonReleaseKey(eventId, airWallGIDs)


class DungeonTeleporterReleaseEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('entityGID', 'targetEntityGID')
    __ref_params__ = ('dungeonNo', 'spaceNo')


    def __init__(self, eventId, controller, entityGID, targetEntityGID, eventHandler=None, **kwargs):
        super(DungeonTeleporterReleaseEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('entityGID', entityGID)
        self.putArgument('targetEntityGID', targetEntityGID)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        dungeonNo = refParams['dungeonNo']
        spaceNo = refParams['spaceNo']
        entityGID = self.fetchArgument('entityGID', -1)
        targetEntityGID = self.fetchArgument('targetEntityGID', 1)
        trapRange = self.fetchArgument('trapRange', 0)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.spawnDungeonEntityByGameEntityId(spaceNo, [entityGID, ], 1, 0,
                                                 {'targetEntityGID': targetEntityGID, 'trapRange': trapRange})
        super(DungeonTeleporterReleaseEvent, self).handleProcessActivated(
            srcE, srcIdx, idx, obj, **refParams)

    def fetchWaitingKey(self, ctx):
        return self.getCollReleaseKey(self.fetchArgument('entityGID', -1))

    @staticmethod
    def getCollReleaseKey(entityGID):
        return 'dun_tel_release_{}'.format(entityGID)


class AIEnterAttackEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, eventId, controller, monsterGID, checkNow, checkOnce, eventHandler=None, **kwargs):
        super(AIEnterAttackEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('monsterGID', monsterGID)
        self.putArgument('checkNow', checkNow)
        self.putArgument('checkOnce', checkOnce)

    def fetchWaitingKey(self, ctx):
        return self.getEnterAttackKey(self.fetchArgument('monsterGID', 0))

    @staticmethod
    def getEnterAttackKey(monsterGID):
        return 'enter_attack_{}'.format(monsterGID)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)

        monsterGID = self.fetchArgument('monsterGID', 0)
        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waitingForTrigger(self.fetchWaitingKey(obj), self, ctx)

        else:
            _spaceMgr = self.controller.owner
            _tagOfGid = 'gid_{}'.format(monsterGID)
            for _eid in _spaceMgr.tagEntities.get(_tagOfGid, ()):
                _entity = KBEngine.entities.get(_eid)
                if not _entity:
                    continue
                if _entity.hasState(gameconst.StateEnum.Fighting):
                    _ret = True
                    break
            else:
                _ret = False

            if _ret:
                self.continueHandleBeTriggered(ctx)

            elif checkNow:
                self._controller.waitingForTrigger(self.fetchWaitingKey(obj), self, ctx)

            else:
                LOG_WARN("DUNGEON FLOW -- EVENT[{}]: monster in battle check failed --"
                            " monsterGID={}".format(self.id, monsterGID))


class AILeaveAttackEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin, _GroupEventMixin):

    def __init__(self, eventId, controller, monsterGID, checkNow, checkOnce, eventHandler=None, **kwargs):
        super(AILeaveAttackEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('monsterGID', monsterGID)
        self.putArgument('checkNow', checkNow)
        self.putArgument('checkOnce', checkOnce)

    def fetchWaitingKey(self, ctx):
        return self.getLeaveAttackKey(self.fetchArgument('monsterGID', 0))

    @staticmethod
    def getLeaveAttackKey(monsterGID):
        return 'leave_attack_{}'.format(monsterGID)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)

        monsterGID = self.fetchArgument('monsterGID', 0)
        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waitingForTrigger(self.fetchWaitingKey(obj), self, ctx)

        else:
            _spaceMgr = self.controller.owner
            _tagOfGid = 'gid_{}'.format(monsterGID)
            _eids = _spaceMgr.tagEntities.get(_tagOfGid, ())
            for _eid in _eids:
                _entity = KBEngine.entities.get(_eid)
                if not _entity:
                    continue
                if not _entity.hasState(gameconst.StateEnum.Fighting):
                    _ret = True
                    break
            else:
                # NOTE(): 没有怪物的话脱战检查必然为True
                _ret = True if not _eids else False

            if _ret:
                self.continueHandleBeTriggered(ctx)

            elif checkNow:
                self._controller.waitingForTrigger(self.fetchWaitingKey(obj), self, ctx)

            else:
                LOG_WARN("DUNGEON FLOW -- EVENT[{}]: monster leave battle check failed --"
                            " monsterGID={}, num={}".format(self.id, monsterGID, len(_eids)))


class DungeonMoveEntityToFixPosEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, eventId, controller, entityGID, _pos, speed, moveAni, eventHandler=None, **kwargs):
        super(DungeonMoveEntityToFixPosEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('entityGID', entityGID)
        self.putArgument('_pos', _pos)
        self.putArgument('speed', speed)
        self.putArgument('moveAni', moveAni)
        self.putArgument('moveUUID', utils.generateUUID())

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        entityGID = self.fetchArgument('entityGID', 0)
        _pos = self.fetchArgument('_pos')
        speed = self.fetchArgument('speed', 0)
        _moveAni = self.fetchArgument('moveAni', gameconst.DunFlowMoveAniEnum.RUN01)
        moveUUID = self.fetchArgument('moveUUID')

        if not _pos:
            LOG_WARN('FlowController::handleDungeonMoveEntityToFixedPos: unknown position', self.id)
            return

        spaceMgr = self.controller.owner
        gidTag = 'gid_{}'.format(entityGID)
        ents = spaceMgr.listEntitiesByTag(gidTag)
        for _entity in ents:

            userData = {'type': gamemove.FLOW_CONTROLLER_FORCE_MOVE, 'moveUUID': moveUUID}

            _newBaseSpeed = _newAdjSpeed = 0.0
            _newMoveAni = _entity.moveAni

            if _moveAni != gameconst.DunFlowMoveAniEnum.DEFAULT:
                _newMoveAni = _moveAni

            if speed > 0:
                _newBaseSpeed = speed

            elif speed == 0 and _entity.IsNpc:
                _npcData = NPC_DATA.datas.get(_entity.npcId, {})
                if _moveAni == gameconst.DunFlowMoveAniEnum.RUN01:
                    _newBaseSpeed = _npcData.get('baseSpeed', 0.0)

                elif _moveAni == gameconst.DunFlowMoveAniEnum.RUN02:
                    _newBaseSpeed = _npcData.get('baseSpeed', 0.0)
                    _newAdjSpeed = _npcData.get('adjSpeed', 0.0)
            # endregion

            if _newBaseSpeed > 0:
                userData.update({"fc_OriginBaseSpeed": _entity.baseSpeed})
                _entity.setProp('baseSpeed', _newBaseSpeed, src=gameconst.SourceType.SrcTpFlowCtrl)
            if _newAdjSpeed > 0:
                userData.update({"fc_OriginAdjSpeed": _entity.adjSpeed})
                _entity.setProp('adjSpeed', _newAdjSpeed, src=gameconst.SourceType.SrcTpFlowCtrl)
            if _newMoveAni != _entity.moveAni:
                userData.update({"fc_OriginMoveAni": _entity.moveAni})
                _entity.moveAni =_newMoveAni

            _entity.removeMoveController()
            if _entity.aiController:
                _entity.aiController.moveToFixedPositionInForce(_pos, userData)
            else:
                _entity.navigateToPosition(_pos, userData)

        super(DungeonMoveEntityToFixPosEvent, self).handleProcessActivated(
            srcE, srcIdx, idx, obj, **refParams)

    def fetchWaitingKey(self, ctx):
        return self.getMoveKey(self.fetchArgument('moveUUID', 0))

    @staticmethod
    def getMoveKey(moveUUID):
        return 'move_to_fixpos_{}'.format(moveUUID)


class MonsterHpMonitorTriggerEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('monsterGID', 'symbol', 'hpPercent')

    def __init__(self, eventId, controller, monsterGID, symbol, hpPercent, checkNow, checkOnce, eventHandler=None,
                 **kwargs):
        super(MonsterHpMonitorTriggerEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('monsterGID', monsterGID)
        self.putArgument('symbol', symbol)
        self.putArgument('hpPercent', hpPercent)
        self.putArgument('checkNow', checkNow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)
        monsterGID = self.fetchArgument('monsterGID', 0)
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        hp = self.fetchArgument('hpPercent', -1)

        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waitingForMonsterHpMonitorTrigger(
                self, ctx, monsterGID, symbol, hp)

        else:
            _spaceMgr = self.controller.owner
            _tagOfGid = 'gid_{}'.format(monsterGID)
            _gidList = _spaceMgr.tagEntities.get(_tagOfGid, [])
            if not _gidList:
                gameengine.panicStack("MonsterHpMonitorTriggerEvent::ent not found", monsterGID, _tagOfGid)
                return

            for _eid in _gidList:
                _entity = KBEngine.entities.get(_eid)
                if not _entity:
                    continue

                _controlHpPrt = round(_entity.hp / _entity.fullHp * 100, 2)
                _ret = gameconst.DungeonFlowCompSym.compare(symbol, _controlHpPrt, hp)
                if _ret:
                    self.continueHandleBeTriggered(ctx)
                    break

                elif checkNow:
                    self._controller.waitingForMonsterHpMonitorTrigger(
                        self, ctx, monsterGID, symbol, hp)
                    break

                else:
                    LOG_WARN("DUNGEON FLOW -- EVENT[{}]: entity hp checkonce failed --"
                                " symbol={}, {} {}".format(self.id, symbol, _controlHpPrt, hp, _entity.gameEntityId))


    def cancelWait(self, ctx):
        _monsterGID = self.fetchArgument('monsterGID', 0)
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        _hp = self.fetchArgument('hpPercent', -1)

        ctrl = self.controller

        _popList = []
        _eList = ctrl.monsterAwaitDic.get(
            _monsterGID, {}).get(
            ctrl.MONSTER_AWAIT_HP_MODIFY_KEY, {}).get(symbol, {}).get(_hp)

        if _eList:
            for idx, (e, eCtx) in enumerate(_eList):
                if eCtx.tid == ctx.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                _eList.pop(i)


class MonsterRestNumberEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('monsterGIDs', 'symbol', 'restNum')

    def __init__(self, eventId, controller, monsterGIDs, symbol, number, checkNow, checkOnce, eventHandler=None, **kwargs):
        super(MonsterRestNumberEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('monsterGIDs', monsterGIDs)
        self.putArgument('symbol', symbol)
        self.putArgument('restNum', number)
        self.putArgument('checkNow', checkNow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)
        monsterGIDs = self.fetchArgument('monsterGIDs', ())
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        number = self.fetchArgument('restNum', -1)
        usePrototypeID = self.fetchArgument('usePrototypeID', False)
        if monsterGIDs[0] == -1:
            _tag = gameconst.FLOW_REST_MONSTER_TAG_ALL
        elif usePrototypeID:
            _tag = gameconst.FLOW_REST_MONSTER_TAG_CBID
        else:
            _tag = gameconst.FLOW_REST_MONSTER_TAG_GID

        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waitingForMonsterRestNumberTrigger(
                self, ctx, monsterGIDs, _tag, symbol, number)

        else:
            _spaceMgr = self.controller.owner
            _currentNum = _spaceMgr.getMonsterNumByGIDsAndTag(monsterGIDs, _tag)

            _ret = gameconst.DungeonFlowCompSym.compare(symbol, _currentNum, number)
            if _ret:
                self.continueHandleBeTriggered(ctx)

            elif checkNow:
                self._controller.waitingForMonsterRestNumberTrigger(
                    self, ctx, monsterGIDs, _tag, symbol, number)

            else:
                LOG_WARN("DUNGEON FLOW -- EVENT[{}]: rest number checkonce failed --"
                            " symbol={}, {} {}".format(self.id, symbol, _currentNum, number))

    def cancelWait(self, ctx):
        self.controller.clearRestMonsterTrigger(self.id)


class DungeonMonsterKillerNumberEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('monsterGID', 'symbol', 'killNum', 'checkOnce')

    def __init__(self, eventId, controller, monsterGID, symbol, number, checkNow, checkOnce, eventHandler=None, **kwargs):
        super(DungeonMonsterKillerNumberEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('monsterGID', monsterGID)
        self.putArgument('symbol', symbol)
        self.putArgument('killNum', number)
        self.putArgument('checkNow', checkNow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)
        _monsterGID = self.fetchArgument('monsterGID', 0)
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        number = self.fetchArgument('killNum', -1)
        usePrototypeID = self.fetchArgument('usePrototypeID', False)
        if usePrototypeID:
            _monsterGID = "cbid{}".format(_monsterGID)
        self._controller.waitingForDungeonMonsterKillNumberTrigger(
            self, ctx, _monsterGID, symbol, number)

        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce')
        if checkOnce or checkNow:
            spaceNo = refParams['spaceNo']
            stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
            if _monsterGID > 0:
                stub.flowCheckDungeonKillCount(spaceNo, _monsterGID, symbol, number, usePrototypeID, self.id, obj, checkOnce)
            else:
                stub.flowCheckDungeonAllKillCount(spaceNo, symbol, number, self.id, obj, checkOnce)

    def cancelWait(self, ctx):
        monsterGID = self.fetchArgument('monsterGID', 0)
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        number = self.fetchArgument('killNum', -1)

        ctrl = self.controller

        _popList = []
        _eventList = ctrl.monsterAwaitDic\
            .get(monsterGID, {})\
            .get(ctrl.DUNGEON_MONSTER_AWAIT_KILL_NUM, {})\
            .get(symbol, {})\
            .get(number)

        if _eventList:
            for idx, (e, eCtx) in enumerate(_eventList):
                if eCtx.tid == ctx.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                _eventList.pop(i)


class DungeonPlayerRestNumEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ()

    def __init__(self, eventId, controller, eventHandler=None, **kwargs):
        super().__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('symbol', kwargs['symbol'])
        self.putArgument('playerNum', kwargs['number'])
        self.putArgument('checkNow', kwargs['checkNow'])
        self.putArgument('checkOnce', kwargs['checkOnce'])

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        number = self.fetchArgument('playerNum', -1)

        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce')
        if not (checkOnce or checkNow):
            self._controller.waitingForDungeonPlayerRestNumTrigger(self, ctx, symbol, number)

        else:
            _currentNum = 0
            for _pid in self.controller.owner.players:
                _pEnt = KBEngine.entities.get(_pid)
                if _pEnt:
                    _currentNum += 1

            _ret = gameconst.DungeonFlowCompSym.compare(symbol, _currentNum, number)
            if _ret:
                self.continueHandleBeTriggered(ctx)

            elif checkNow:
                self._controller.waitingForDungeonPlayerRestNumTrigger(self, ctx, symbol, number)

            else:
                LOG_WARN("DUNGEON FLOW -- EVENT[{}]: player rest number checkonce failed --"
                            " symbol={}, {} {}".format(self.id, symbol, _currentNum, number))
    def cancelWait(self, ctx):
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        number = self.fetchArgument('playerNum', -1)

        ctrl = self.controller

        _popList = []
        _eventList = ctrl.waitingsDict.get(ctrl.GLOBAL_EVENT_KEY, {}).get(
            ctrl.DUNGEON_PLAYER_REST_NUM, {}).get(symbol, {}).get(number)

        if _eventList:
            for idx, (e, eCtx) in enumerate(_eventList):
                if eCtx.tid == ctx.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                _eventList.pop(i)


class DungeonAlivePlayerEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('symbol', 'playerNum')

    def __init__(self, eventId, controller, symbol, number, checkNow, checkOnce, eventHandler=None, **kwargs):
        super(DungeonAlivePlayerEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('symbol', symbol)
        self.putArgument('playerNum', number)
        self.putArgument('checkNow', checkNow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        number = self.fetchArgument('playerNum', -1)

        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce')
        if not (checkOnce or checkNow):
            self._controller.waitingForDungeonAlivePlayerTrigger(self, ctx, symbol, number)

        else:
            _currentNum = 0
            for _pid in self.controller.owner.players:
                _pEnt = KBEngine.entities.get(_pid)
                if _pEnt and not _pEnt.isDie():
                    _currentNum += 1

            _ret = gameconst.DungeonFlowCompSym.compare(symbol, _currentNum, number)
            if _ret:
                self.continueHandleBeTriggered(ctx)

            elif checkNow:
                self._controller.waitingForDungeonAlivePlayerTrigger(self, ctx, symbol, number)

            else:
                LOG_WARN("DUNGEON FLOW -- EVENT[{}]: alive player number checkonce failed --"
                            " symbol={}, {} {}".format(self.id, symbol, _currentNum, number))

    def cancelWait(self, ctx):
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        number = self.fetchArgument('playerNum', -1)

        ctrl = self.controller

        _popList = []
        _eventList = ctrl.waitingsDict.get(ctrl.GLOBAL_EVENT_KEY, {}).get(
            ctrl.DUN_ALIVE_PLAYER, {}).get(symbol, {}).get(number)

        if _eventList:
            for idx, (e, eCtx) in enumerate(_eventList):
                if eCtx.tid == ctx.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                _eventList.pop(i)


class DungeonAnyPlayerHPMonitorTriggerEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __selfParams__ = ('symbol', 'hpPercent')

    def __init__(self, eventId, controller, symbol, hpPercent, checkNow, checkOnce, eventHandler=None, **kwargs):
        super(DungeonAnyPlayerHPMonitorTriggerEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('symbol', symbol)
        self.putArgument('hpPercent', hpPercent)
        self.putArgument('checkNow', checkNow)
        self.putArgument('checkOnce', checkOnce)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        hp = self.fetchArgument('hpPercent', -1)

        checkNow = self.fetchArgument('checkNow', False)
        checkOnce = self.fetchArgument('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waitingForDungeonAnyPlayerHpMonitorTrigger(self, ctx, symbol, hp)

        else:
            for _pid in self.controller.owner.players:
                _pEnt = KBEngine.entities.get(_pid)
                _currentHpPrt = round(_pEnt.hp/_pEnt.fullHp*100, 2)
                if _pEnt and gameconst.DungeonFlowCompSym.compare(symbol, _currentHpPrt, hp):
                    _ret = True
                    break
            else:
                _ret = False

            if _ret:
                self.continueHandleBeTriggered(ctx)

            elif checkNow:
                self._controller.waitingForDungeonAnyPlayerHpMonitorTrigger(self, ctx, symbol, hp)

            else:
                LOG_WARN("DUNGEON FLOW -- EVENT[{}]: check any player hp checkonce failed --"
                            " symbol={}, {} {}".format(self.id, symbol, _currentHpPrt, hp))

    def cancelWait(self, ctx):
        symbol = self.fetchArgument('symbol', gameconst.DungeonFlowCompSym.un)
        hp = self.fetchArgument('hpPercent', -1)

        ctrl = self.controller

        _popList = []
        _eventList = ctrl.waitingsDict\
            .get(ctrl.GLOBAL_EVENT_KEY, {})\
            .get(ctrl.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY, {})\
            .get(symbol, {})\
            .get(hp)

        if _eventList:
            for idx, (e, eCtx) in enumerate(_eventList):
                if eCtx.tid == ctx.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                _eventList.pop(i)


class DungeonValueCheckHoldEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin,
                                 _WaitingCancelMixin):

    def __init__(self, eventId, controller, varIds, eventHandler=None, **kwargs):
        super(DungeonValueCheckHoldEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('varIds', varIds)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waitingE=self,
            waitingArgs=_w_args,
            waitingKwargs=_w_kwargs)
        m_varIds = self.fetchArgument('varIds', [])
        for mVarId in m_varIds:
            self._controller.waitingForDungeonSpaceVarChangeCheck(self, ctx, mVarId)


    def cancelWait(self, ctx):
        m_varIds = self.fetchArgument('varIds', [])

        ctrl = self.controller

        for mVarId in m_varIds:
            _popList = []
            _eventList = ctrl.waitingsDict\
                .get(ctrl.GLOBAL_EVENT_KEY, {})\
                .get(ctrl.DUNGEON_SPACE_VAR_CHECK_KEY, {})\
                .get(mVarId)

            if not _eventList:
                continue

            for idx, (e, eCtx) in enumerate(_eventList):
                if eCtx.tid == ctx.tid:
                    _popList.append(idx)

            for i in reversed(_popList):
                _eventList.pop(i)


class DungeonEntityImmuneDeath(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, eventId, controller, entityGID, eventHandler=None, **kwargs):
        super(DungeonEntityImmuneDeath, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument("entityGID", entityGID)

    def fetchWaitingKey(self, ctx):
        return self.getImmuneDeathKey(self.fetchArgument("entityGID", 0))

    @staticmethod
    def getImmuneDeathKey(entityGID):
        return "entity_immune_death_{}".format(entityGID)


class EntityRouteFinishedEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, eventId, controller, entityGID, pathID, eventHandler=None, **kwargs):
        super(EntityRouteFinishedEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('entityGID', entityGID)
        self.putArgument('pathID', pathID)

    def fetchWaitingKey(self, ctx):
        return self.getRouteFinishedKey(self.fetchArgument('entityGID', 0), self.fetchArgument('pathID', 0))

    @staticmethod
    def getRouteFinishedKey(entityGID, pathID):
        return 'route_finished_{}_{}'.format(entityGID, pathID)


class EntityRoutingMissingEscortEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, eventId, controller, entityGID, pathID, eventHandler=None, **kwargs):
        super(EntityRoutingMissingEscortEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('entityGID', entityGID)
        self.putArgument('pathID', pathID)

    def continueHandleBeTriggered(self, ctx):
        super().continueHandleBeTriggered(ctx)
        infLoop = self.fetchArgument('infLoop', False)
        if infLoop:
            self.reHandleBeTriggered(*ctx.waitingArgs, **ctx.waitingKwargs)

    def fetchWaitingKey(self, ctx):
        return self.getRouteMissingEscortKey(self.fetchArgument('entityGID', 0), self.fetchArgument('pathID', 0))

    @staticmethod
    def getRouteMissingEscortKey(entityGID, pathID):
        return 'route_missing_escort_{}_{}'.format(entityGID, pathID)


class AnyPlayerCinemaPlayEndedEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, eventId, controller, cinemaPlayID, delay, eventHandler=None, **kwargs):
        super(AnyPlayerCinemaPlayEndedEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('cinemaPlayID', cinemaPlayID)
        self.putArgument('delay', delay)
        self.eventCtrlId = 0

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        cinemaPlayID = self.fetchArgument('cinemaPlayID', 0)
        delay = self.fetchArgument('delay', 0)
        if delay <= 0:
            LOG_WARN("AnyPlayerCinemaPlayEndedEvent::delay <=0, eid={} cid={} delay={}".format(
                self.id, cinemaPlayID, delay))
            delay = 0.1

        spaceMgr = self.controller.owner
        if not spaceMgr:
            LOG_ERR('FlowController::AnyPlayerCinemaPlayEndedEvent:spaceMgr not found')
        else:
            if self.eventCtrlId > 0:
                spaceMgr.cancelTimerCB(
                    self.eventCtrlId, gametimer.TIMER_TAG_EP_CINEMA_END_TIMEOUT)
            self.eventCtrlId = spaceMgr.asyncCallbackAfter(
                delay, gametimer.TIMER_TAG_EP_CINEMA_END_TIMEOUT
            )._onAnyPlayerCinemaPlayEndedTimeout(cinemaPlayID, self.id)

        return super().handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)

    def continueHandleBeTriggered(self, ctx):
        if self.eventCtrlId > 0:
            spaceMgr = self.controller.owner
            spaceMgr and spaceMgr.cancelTimerCB(
                self.eventCtrlId, gametimer.TIMER_TAG_EP_CINEMA_END_TIMEOUT)
        super().continueHandleBeTriggered(ctx)

    def fetchWaitingKey(self, ctx):
        return self.getCinemaPlayEndedKey(self.fetchArgument('cinemaPlayID', 0))

    @staticmethod
    def getCinemaPlayEndedKey(cinemaPlayID):
        return 'cinema_player_ended_{}'.format(cinemaPlayID)


class DungeonRebornPosReleaseEvent(ep_ctrl.event.BaseAwaitEvent, _ElementHotReloadMixin, _WaitingCancelMixin):
    __selfParams__ = ('rebornPosGIDs', 'rebornPosNum')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, eventId, controller, rebornPosGIDs, eventHandler=None, **kwargs):
        super(DungeonRebornPosReleaseEvent, self).__init__(eventId, controller, eventHandler, **kwargs)
        self.putArgument('rebornPosGIDs', rebornPosGIDs)

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        dungeonNo = refParams['dungeonNo']
        spaceNo = refParams['spaceNo']
        rebornPosGIDs = self.fetchArgument('rebornPosGIDs', [])
        rebornPosNum = self.fetchArgument('rebornPosNum', 1)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.spawnDungeonEntityByGameEntityId(spaceNo, rebornPosGIDs, rebornPosNum, 0,
                                                 {'eventId': self.id})
        super(DungeonRebornPosReleaseEvent, self).handleProcessActivated(
            srcE, srcIdx, idx, obj, **refParams)

    def fetchWaitingKey(self, ctx):
        return self.getCollReleaseKey(self.id, self.fetchArgument('rebornPosGIDs', []))

    @staticmethod
    def getCollReleaseKey(eventId, rebornPosGIDs):
        return getCommonReleaseKey(eventId, rebornPosGIDs)
