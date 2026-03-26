# coding: utf-8
# ----------------------------------------------
# EVENTS
# ----------------------------------------------
from KBEDebug import *
import KBEngine

import math

import gameengine
import gametimer
import gamemove
import gameconst
import gametimer
import formula
import random
import utils
import copy
import sMath, math, Math

import ep_ctrl

import userType
import actionContext

import gamePlay_gamePlay as DDI
import creep_base as CBD
import skill_skill as SSD
import buff_buff as BUFF
import NPC_NPC as NPC_DATA

__all__ = [
    'FlowEvent',
    'FlowRandomEvent',
    'ForLoop',
    'ForLoopWithBreak',
    'WhileLoop',
    'DelayExecEvent',

    'DelayDungeonEnd',
    'WaitingTaskCompleteEvent',
    'WaitingTaskFailedEvent',
    'WaitingTaskInProgressEvent',
    'DungeonMonsterReleaseEvent',
    'DungeonNPCReleaseEvent',
    'DungeonCollectionReleaseEvent',
    'DungeonCollectionBeCollectedEvent',
    'DungeonMultiCollectionAllBeCollectedEvent',
    'DungeonBuffPointReleaseEvent',
    'DungeonAirWallReleaseEvent',
    'DungeonTeleporterReleaseEvent',
    'AIEnterAttackEvent',
    'AILeaveAttackEvent',
    'DungeonTrapBeTriggered',
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

    'get_common_release_key',
    'DungeonRebornPosReleaseEvent',
]


def get_common_release_key(eventId, entityGIDs):
    return 'release_common_{}_{}'.format(eventId, '_'.join((str(i) for i in entityGIDs)))


class _GroupMixin(object):

    def makeGroup(self, *events):
        self.eGroup = events


class _DelayCancelMixin(object):

    def cancel(self, ctx, tag):
        tid = ctx.tid
        if tid not in self._timerIdDic:
            return
        self.controller.owner._cancelCallback(self._timerIdDic[tid], tag)
        del self._timerIdDic[tid]


class _WaitingCancelMixin(object):

    def cancel(self, ctx):
        key = self.get_waiting_key(ctx)
        ctrl = self.controller
        popList = []
        if key in ctrl._waitings:
            for idx, (e, e_ctx) in enumerate(ctrl._waitings[key]):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                ctrl._waitings[key].pop(i)


class _ElementHotReloadMixin(userType.UserSoleType):

    def _lateReload(self):
        import inspect
        import sys
        DEBUG_MSG('  |--  {}::_lateReload: {}'.format(self.__class__.__name__, self.id))
        for v in self._params.values():
            if callable(v) and not inspect.isfunction(v):
                DEBUG_MSG('    |-- {}::_lateReload param method: {} {}'.format(
                    self.__class__.__name__, v.__name__, self.id))
                utils.resetCls(v.__self__)
            else:
                getattr(v, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()

        if isinstance(self, ep_ctrl.event.BaseEvent):
            DEBUG_MSG('    |-- {}::_lateReload param handler: {} {}'.format(
                    self.__class__.__name__, self._handler.__name__, self.id))
            self._handler = getattr(sys.modules[self._handler.__module__], self._handler.__name__)


class FlowEvent(ep_ctrl.event.Event, _ElementHotReloadMixin):
    """subclass for Event"""


class FlowRandomEvent(ep_ctrl.event.RandomEvent, _ElementHotReloadMixin):
    """subclass for random event"""


class ForLoop(ep_ctrl.flow.BaseForLoop, _ElementHotReloadMixin, _DelayCancelMixin, _GroupMixin):

    __self_params__ = ('delayTime', )

    def __init__(self, *args, **kwargs):
        super(ForLoop, self).__init__(*args, **kwargs)
        self._timerIdDic = {}

    @property
    def timerTag(self):
        return gametimer.TIMER_TAG_FLOW_CONTROLLER_DELAY_CALLBACK

    def next(self, ctx, **ref_params):
        if self._looping_counters[ctx.tid] > self.get_last_index():
            self._handle_looping(self, self, ctx, **ref_params)
            return
        delayTime = self.get_param('delayTime', 0.1) or 0.1
        _spaceMgr = self.controller.owner
        if ctx.tid in self._timerIdDic:
            _spaceMgr._cancelCallback(self._timerIdDic[ctx.tid], self.timerTag)
        self._timerIdDic[ctx.tid] = _spaceMgr._callback(
            delayTime, 'flowControllerDelayCallback',
            (self, '_handle_looping', (self, self, ctx), ref_params), self.timerTag)

    def _handle_looping(self, this, src_e, ctx, **ref_params):
        self._timerIdDic.pop(ctx.tid, None)
        super(ForLoop, self)._handle_looping(self, src_e, ctx, **ref_params)

    def cancel(self, ctx):
        tid = ctx.tid
        super(ForLoop, self).cancel(ctx, self.timerTag)
        self._looping_counters.pop(tid, None)


class ForLoopWithBreak(ep_ctrl.flow.BaseForLoopWithBreak, _ElementHotReloadMixin, _DelayCancelMixin):

    __self_params__ = ('delayTime', )

    def __init__(self, *args, **kwargs):
        super(ForLoopWithBreak, self).__init__(*args, **kwargs)
        self._timerIdDic = {}

    @property
    def timerTag(self):
        return gametimer.TIMER_TAG_FLOW_CONTROLLER_DELAY_CALLBACK

    def next(self, ctx, **ref_params):
        delayTime = self.get_param('delayTime', 0.1)
        _spaceMgr = self.controller.owner
        if ctx.tid in self._timerIdDic:
            _spaceMgr._cancelCallback(self._timerIdDic[ctx.tid], self.timerTag)
        self._timerIdDic[ctx.tid] = _spaceMgr._callback(
            delayTime, 'flowControllerDelayCallback',
            (self, '_handle_looping', (self, self, ctx), ref_params), self.timerTag)

    def _handle_looping(self, this, src_e, ctx, **ref_params):
        self._timerIdDic.pop(ctx.tid, None)
        super(ForLoopWithBreak, self)._handle_looping(self, src_e, ctx, **ref_params)

    def cancel(self, ctx):
        tid = ctx.tid
        super(ForLoopWithBreak, self).cancel(ctx, self.timerTag)
        self._looping_counters.pop(tid, None)


class WhileLoop(ep_ctrl.flow.BaseWhileLoop, _ElementHotReloadMixin, _DelayCancelMixin):

    __self_params__ = ('delayTime', )

    def __init__(self, *args, **kwargs):
        super(WhileLoop, self).__init__(*args, **kwargs)
        self._timerIdDic = {}

    @property
    def timerTag(self):
        return gametimer.TIMER_TAG_FLOW_CONTROLLER_DELAY_CALLBACK

    def next(self, ctx, **ref_params):
        delayTime = self.get_param('delayTime', 0.1)
        _spaceMgr = self.controller.owner
        if ctx.tid in self._timerIdDic:
            _spaceMgr._cancelCallback(self._timerIdDic[ctx.tid], self.timerTag)
        self._timerIdDic[ctx.tid] = _spaceMgr.owner._callback(
            delayTime, 'flowControllerDelayCallback',
            (self, '_handle_looping', (self, self, ctx), ref_params), self.timerTag)

    def _handle_looping(self, this, src_e, ctx, **ref_params):
        self._timerIdDic.pop(ctx.tid, None)
        super(WhileLoop, self)._handle_looping(self, src_e, ctx, **ref_params)

    def cancel(self, ctx):
        super(WhileLoop, self).cancel(ctx, self.timerTag)


class DelayExecEvent(ep_ctrl.event.BaseDelayedEvent, _ElementHotReloadMixin, _DelayCancelMixin, _GroupMixin):

    def __init__(self, *args, **kwargs):
        super(DelayExecEvent, self).__init__(*args, **kwargs)
        self._timerIdDic = {}

    @property
    def timerTag(self):
        return gametimer.TIMER_TAG_FLOW_CONTROLLER_DELAY_EXECEVENT_CALLBACK

    def next(self, ctx, **ref_params):
        _spaceMgr = self.controller.owner
        if ctx.tid in self._timerIdDic:
            _spaceMgr._cancelCallback(self._timerIdDic[ctx.tid], self.timerTag)
        self._timerIdDic[ctx.tid] = _spaceMgr._callback(
            self._delay_time, 'flowControllerDelayExecEventCallback', (self, ctx), self.timerTag)


    def handle_be_triggered_after_delay(self, obj):
        self._timerIdDic.pop(obj.tid, None)
        super(DelayExecEvent, self).handle_be_triggered_after_delay(obj)

    def cancel(self, ctx):
        super(DelayExecEvent, self).cancel(ctx, self.timerTag)


class DelayDungeonEnd(DelayExecEvent):

    def __init__(self, event_id, controller, dungeonNo, spaceNo, delayTime, preDelayTime,
                 isFail=False, event_handler=None, **kwargs):
        super(DelayDungeonEnd, self).__init__(
            event_id, controller, event_handler, delay_time=preDelayTime, **kwargs)
        self.add_param('dungeonNo', dungeonNo)
        self.add_param('spaceNo', spaceNo)
        self.add_param('delayTime', delayTime)
        self.add_param('preDelayTime', preDelayTime)
        self.add_param('isFail', isFail)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        spaceNo = self.get_param('spaceNo')
        preDelayTime = self.get_param('preDelayTime')
        for pid in self.controller.owner.players:
            pEnt = KBEngine.entities.get(pid)
            pEnt and pEnt.client.changeDungeonRemainTime(spaceNo, int(utils.getNow() + preDelayTime))
        super(DelayDungeonEnd, self).handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)

    def handle_be_triggered_after_delay(self, obj):
        from ._controller import handleEndDungeon

        handleEndDungeon(self, self, obj, **self._pkg_all_ref_params())
        super(DelayDungeonEnd, self).handle_be_triggered_after_delay(obj)


class WaitingTaskCompleteEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, task_id, checknow, checkOnce, event_handler=None, **kwargs):
        super(WaitingTaskCompleteEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('taskId', task_id)
        self.add_param('checkNow', checknow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        super(WaitingTaskCompleteEvent, self).handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)
        checkNow = self.get_param('checkNow')
        checkOnce = self.get_param('checkOnce')
        taskId = self.get_param('taskId')
        if (checkNow or checkOnce) and taskId:
            spaceMgr = self.controller.owner
            if spaceMgr:
                for pid in spaceMgr.players:
                    pEnt = KBEngine.entities.get(pid)
                    pEnt and pEnt.base.getTaskCurrentState(
                        taskId, pEnt, 'flowCtrlIsTaskCompleteCallback',
                        (taskId, self.id, gameconst.TaskStat.TASK_STAT_SUBMITTED, checkOnce))

    def get_waiting_key(self, ctx):
        return self.get_task_key(self.get_param('taskId', 0))

    @staticmethod
    def get_task_key(task_id):
        return 'task_complete_{}'.format(task_id)


class WaitingTaskFailedEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):
    def __init__(self, event_id, controller, task_id, checknow, checkOnce, event_handler=None, **kwargs):
        super(WaitingTaskFailedEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('taskId', task_id)
        self.add_param('checkNow', checknow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        super(WaitingTaskFailedEvent, self).handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)
        checkNow = self.get_param('checkNow')
        checkOnce = self.get_param('checkOnce')
        taskId = self.get_param('taskId')
        if (checkNow or checkOnce) and taskId:
            spaceMgr = self.controller.owner
            if spaceMgr:
                for pid in spaceMgr.players:
                    pEnt = KBEngine.entities.get(pid)
                    pEnt and pEnt.base.getTaskCurrentState(
                        taskId, pEnt, 'flowCtrlIsTaskCompleteCallback',
                        (taskId, self.id, gameconst.TaskStat.TASK_STAT_FAILED, checkOnce))

    def get_waiting_key(self, ctx):
        return self.get_task_key(self.get_param('taskId', 0))

    @staticmethod
    def get_task_key(task_id):
        return 'task_failed_{}'.format(task_id)


class WaitingTaskInProgressEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):
    def __init__(self, event_id, controller, task_id, checknow, checkOnce, event_handler=None, **kwargs):
        super(WaitingTaskInProgressEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('taskId', task_id)
        self.add_param('checkNow', checknow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        super(WaitingTaskInProgressEvent, self).handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)
        checkNow = self.get_param('checkNow')
        checkOnce = self.get_param('checkOnce')
        taskId = self.get_param('taskId')
        if (checkNow or checkOnce) and taskId:
            spaceMgr = self.controller.owner
            if spaceMgr:
                for pid in spaceMgr.players:
                    pEnt = KBEngine.entities.get(pid)
                    pEnt and pEnt.base.getTaskCurrentState(
                        taskId, pEnt, 'flowCtrlIsTaskCompleteCallback',
                        (taskId, self.id, gameconst.TaskStat.TASK_STAT_RUNNING, checkOnce))

    def get_waiting_key(self, ctx):
        return self.get_task_key(self.get_param('taskId', 0))

    @staticmethod
    def get_task_key(task_id):
        return 'task_inprogress_{}'.format(task_id)


class DungeonMonsterReleaseEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('monsterGIDs', 'monsterNum', 'monsterLevel')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, event_id, controller, monsterGIDs, event_handler=None, **kwargs):
        super(DungeonMonsterReleaseEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('monsterGIDs', monsterGIDs)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        dungeonNo = ref_params['dungeonNo']     # dungeonNo get from ref
        spaceNo = ref_params['spaceNo']
        monsterGIDs = self.get_param('monsterGIDs', [])
        monsterNum = self.get_param('monsterNum', 1)
        monsterLevel = self.get_param('monsterLevel', 0)
        overwriteProps = self.get_param('overwriteProps', {})
        ifSetBoss = self.get_param('ifSetBoss', False)
        initState = self.get_param('initState', 0)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.createEntityInDungeonByGameEntityId(spaceNo, monsterGIDs, monsterNum, monsterLevel,
                                                 {'overwriteProps': overwriteProps, 'ifSetBoss': ifSetBoss,
                                                  'initState': initState, 'eventId': self.id})
        super(DungeonMonsterReleaseEvent, self).handle_be_triggered(
            src_e, src_idx, idx, obj, **ref_params)

    def get_waiting_key(self, ctx):
        return self.get_monster_release_key(self.id, self.get_param('monsterGIDs', []))

    @staticmethod
    def get_monster_release_key(eventId, monsterGIDs):
        return get_common_release_key(eventId, monsterGIDs)


class DungeonNPCReleaseEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('npcGIDs', 'npcNum', 'npcLevel')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, event_id, controller, npcGIDs, event_handler=None, **kwargs):
        super(DungeonNPCReleaseEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('npcGIDs', npcGIDs)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        dungeonNo = ref_params['dungeonNo']
        spaceNo = ref_params['spaceNo']
        npcGIDs = self.get_param('npcGIDs', [])
        npcNum = self.get_param('npcNum', 1)
        npcLevel = self.get_param('npcLevel', 0)
        ifSetBoss = self.get_param('ifSetBoss', False)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.createEntityInDungeonByGameEntityId(spaceNo, npcGIDs, npcNum, npcLevel,
                                                 {'ifSetBoss': ifSetBoss, 'eventId': self.id})
        super(DungeonNPCReleaseEvent, self).handle_be_triggered(
            src_e, src_idx, idx, obj, **ref_params)

    def get_waiting_key(self, ctx):
        return self.get_npc_release_key(self.id, self.get_param('npcGIDs', []))

    @staticmethod
    def get_npc_release_key(eventId, npcGIDs):
        return get_common_release_key(eventId, npcGIDs)


class DungeonCollectionReleaseEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('collGIDs', 'collNum', 'randomCollectionNum', 'checkHaveInFixed')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, event_id, controller, collGIDs, event_handler=None, **kwargs):
        super(DungeonCollectionReleaseEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('collGIDs', collGIDs)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        dungeonNo = ref_params['dungeonNo']
        spaceNo = ref_params['spaceNo']
        collGIDs = self.get_param('collGIDs', [])
        collNum = self.get_param('collNum', 1)
        DEBUG_MSG("handle_be_triggered begin ", collGIDs)
        randomCollectionNum = self.get_param('randomCollectionNum', 0)
        checkHaveInFixed = self.get_param('checkHaveInFixed', False)
        if randomCollectionNum and len(collGIDs) >= randomCollectionNum:
            collGIDs = random.sample(collGIDs, randomCollectionNum)

        _spaceMgr = self.controller.owner
        if checkHaveInFixed:
            for _ent in _spaceMgr.getEntitiesByTag("Collection"):
                gid = utils.getGidFromGameEntityId(_ent.gameEntityId)
                if gid in collGIDs:
                    collGIDs.remove(gid)

            if not len(collGIDs):
                WARNING_MSG("DungeonCollectionReleaseEvent not collGIDs")
                return

        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.createEntityInDungeonByGameEntityId(spaceNo, collGIDs, collNum, 0,
                                                 {'eventId': self.id})
        super(DungeonCollectionReleaseEvent, self).handle_be_triggered(
            src_e, src_idx, idx, obj, **ref_params)

    def get_waiting_key(self, ctx):
        return self.get_coll_release_key(self.id, self.get_param('collGIDs', []))

    @staticmethod
    def get_coll_release_key(eventId, collGIDs):
        return get_common_release_key(eventId, collGIDs)


class DungeonCollectionBeCollectedEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('collGIDs', )

    def __init__(self, event_id, controller, collGIDs, checkNow, checkOnce, event_handler=None, **kwargs):
        super().__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('collGIDs', collGIDs)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)
        collGIDs = self.get_param('collGIDs')

        usePrototypeID = self.get_param('usePrototypeID', False)
        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce')
        if not (checkOnce or checkNow):
            for collGID in collGIDs:
                collGID = "cbid{}".format(collGID) if usePrototypeID else collGID
                self._controller.waiting_for_dungeon_collection_be_collected_trigger(self, ctx, collGID)

        else:
            _spaceMgr = self.controller.owner
            _isCollected = False
            for collGID in collGIDs:
                collGID = "cbid{}".format(collGID) if usePrototypeID else collGID
                collNum = _spaceMgr.collBeCollectedDict.get(collGID, 0)
                if collNum > 0:
                    _isCollected = True
                    break

            if _isCollected:
                self.continue_handle_be_triggered(ctx)

            elif checkNow:
                for collGID in collGIDs:
                    collGID = "cbid{}".format(collGID) if usePrototypeID else collGID
                    self._controller.waiting_for_dungeon_collection_be_collected_trigger(self, ctx, collGID)

            else:
                WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: collection be collected checkonce failed --"
                            " collGIDs={}".format(self.id, collGIDs, usePrototypeID))

    def re_handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        self.handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)

    def cancel(self, ctx):
        m_collGIDs = self.get_param('collGIDs', [])

        ctrl = self.controller

        for i_collGID in m_collGIDs:
            popList = []
            eList = ctrl._waitings.get(ctrl.GLOBAL_KEY, {}).get(
                ctrl.DUNGEON_COLL_BE_COLLECT_KEY, {}).get(i_collGID)

            if not eList:
                continue

            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class DungeonMultiCollectionAllBeCollectedEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('collGIDs', )

    def __init__(self, event_id, controller, collGIDs, event_handler=None, **kwargs):
        super().__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('collGIDs', collGIDs)
        self._collectDict = {i: False for i in collGIDs}

    # ----------------------------------------------
    # collection method
    def collected(self, collGID):
        if collGID in self._collectDict:
            self._collectDict[collGID] = True

    def isAllBeCollected(self):
        return all(self._collectDict.values())
    # ----------------------------------------------

    def re_handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        self._collectDict = {i: False for i in self._collectDict}
        self.handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)

        m_collGIDs = self.get_param('collGIDs')
        for i_collGID in m_collGIDs:
            self._controller.waiting_for_dungeon_multi_collection_all_be_colllected(self, ctx, i_collGID)

    def cancel(self, ctx):
        m_collGIDs = self.get_param('collGIDs', [])

        ctrl = self.controller

        for i_collGID in m_collGIDs:
            popList = []
            eList = ctrl._waitings.get(ctrl.GLOBAL_KEY, {}).get(
                ctrl.DUNGEON_MULTI_COLL_BE_COLLTECT_KEY, {}).get(i_collGID)

            if not eList:
                continue

            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class DungeonBuffPointReleaseEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('buffPointGIDs', 'buffPointNum')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, event_id, controller, buffPointGIDs, event_handler=None, **kwargs):
        super(DungeonBuffPointReleaseEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('buffPointGIDs', buffPointGIDs)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        dungeonNo = ref_params['dungeonNo']
        spaceNo = ref_params['spaceNo']
        buffPointGIDs = self.get_param('buffPointGIDs', [])
        buffPointNum = self.get_param('buffPointNum', 1)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.createEntityInDungeonByGameEntityId(spaceNo, buffPointGIDs, buffPointNum, 0,
                                                 {'eventId': self.id})
        super(DungeonBuffPointReleaseEvent, self).handle_be_triggered(
            src_e, src_idx, idx, obj, **ref_params)

    def get_waiting_key(self, ctx):
        return self.get_coll_release_key(self.id, self.get_param('buffPointGIDs', []))

    @staticmethod
    def get_coll_release_key(eventId, buffPointGIDs):
        return get_common_release_key(eventId, buffPointGIDs)


class DungeonAirWallReleaseEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('airWallGIDs', 'airWallNum')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, event_id, controller, airWallGIDs, event_handler=None, **kwargs):
        super(DungeonAirWallReleaseEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('airWallGIDs', airWallGIDs)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        dungeonNo = ref_params['dungeonNo']
        spaceNo = ref_params['spaceNo']
        airWallGIDs = self.get_param('airWallGIDs', [])
        airWallNum = self.get_param('airWallNum', 1)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.createEntityInDungeonByGameEntityId(spaceNo, airWallGIDs, airWallNum, 0,
                                                 {'eventId': self.id})
        super(DungeonAirWallReleaseEvent, self).handle_be_triggered(
            src_e, src_idx, idx, obj, **ref_params)

    def get_waiting_key(self, ctx):
        return self.get_coll_release_key(self.id, self.get_param('airWallGIDs', []))

    @staticmethod
    def get_coll_release_key(eventId, airWallGIDs):
        return get_common_release_key(eventId, airWallGIDs)


class DungeonTeleporterReleaseEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('entityGID', 'targetEntityGID')
    __ref_params__ = ('dungeonNo', 'spaceNo')


    def __init__(self, event_id, controller, entityGID, targetEntityGID, event_handler=None, **kwargs):
        super(DungeonTeleporterReleaseEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('entityGID', entityGID)
        self.add_param('targetEntityGID', targetEntityGID)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        dungeonNo = ref_params['dungeonNo']
        spaceNo = ref_params['spaceNo']
        entityGID = self.get_param('entityGID', -1)
        targetEntityGID = self.get_param('targetEntityGID', 1)
        trapRange = self.get_param('trapRange', 0)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.createEntityInDungeonByGameEntityId(spaceNo, [entityGID, ], 1, 0,
                                                 {'targetEntityGID': targetEntityGID, 'trapRange': trapRange})
        super(DungeonTeleporterReleaseEvent, self).handle_be_triggered(
            src_e, src_idx, idx, obj, **ref_params)

    def get_waiting_key(self, ctx):
        return self.get_coll_release_key(self.get_param('entityGID', -1))

    @staticmethod
    def get_coll_release_key(entityGID):
        return 'dun_tel_release_{}'.format(entityGID)


class AIEnterAttackEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, monsterGID, checkNow, checkOnce, event_handler=None, **kwargs):
        super(AIEnterAttackEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('monsterGID', monsterGID)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def get_waiting_key(self, ctx):
        return self.get_enter_attack_key(self.get_param('monsterGID', 0))

    @staticmethod
    def get_enter_attack_key(monsterGID):
        return 'enter_attack_{}'.format(monsterGID)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)

        monsterGID = self.get_param('monsterGID', 0)
        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waiting_for_trigger(self.get_waiting_key(obj), self, ctx)

        else:
            _spaceMgr = self.controller.owner
            _gidTag = 'gid_{}'.format(monsterGID)
            for _eid in _spaceMgr.taggedEntities.get(_gidTag, ()):
                _ent = KBEngine.entities.get(_eid)
                if not _ent:
                    continue
                if _ent.hasState(gameconst.State.Fighting):
                    _ret = True
                    break
            else:
                _ret = False

            if _ret:
                self.continue_handle_be_triggered(ctx)

            elif checkNow:
                self._controller.waiting_for_trigger(self.get_waiting_key(obj), self, ctx)

            else:
                WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: monster in battle check failed --"
                            " monsterGID={}".format(self.id, monsterGID))


class AILeaveAttackEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin, _GroupMixin):

    def __init__(self, event_id, controller, monsterGID, checkNow, checkOnce, event_handler=None, **kwargs):
        super(AILeaveAttackEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('monsterGID', monsterGID)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def get_waiting_key(self, ctx):
        return self.get_leave_attack_key(self.get_param('monsterGID', 0))

    @staticmethod
    def get_leave_attack_key(monsterGID):
        return 'leave_attack_{}'.format(monsterGID)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)

        monsterGID = self.get_param('monsterGID', 0)
        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waiting_for_trigger(self.get_waiting_key(obj), self, ctx)

        else:
            _spaceMgr = self.controller.owner
            _gidTag = 'gid_{}'.format(monsterGID)
            _entities = _spaceMgr.taggedEntities.get(_gidTag, ())
            for _eid in _entities:
                _ent = KBEngine.entities.get(_eid)
                if not _ent:
                    continue
                if not _ent.hasState(gameconst.State.Fighting):
                    _ret = True
                    break
            else:
                # NOTE(): 没有怪物的话脱战检查必然为True
                _ret = True if not _entities else False

            if _ret:
                self.continue_handle_be_triggered(ctx)

            elif checkNow:
                self._controller.waiting_for_trigger(self.get_waiting_key(obj), self, ctx)

            else:
                WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: monster leave battle check failed --"
                            " monsterGID={}, num={}".format(self.id, monsterGID, len(_entities)))


class DungeonTrapBeTriggered(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, entityGID, checkNow, checkOnce, event_handler=None, **kwargs):
        super().__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('entityGID', entityGID)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def get_waiting_key(self, ctx):
        return self.get_trap_be_triggered_key(self.get_param('entityGID', 0))

    @staticmethod
    def get_trap_be_triggered_key(entityGID):
        return 'trap_be_triggered_{}'.format(entityGID)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)

        entityGID = self.get_param('entityGID', 0)
        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce')
        if not (checkOnce or checkNow):
            self._controller.waiting_for_trigger(self.get_waiting_key(obj), self, ctx)

        else:
            _spaceMgr = self.controller.owner
            _gidTag = 'gid_{}'.format(entityGID)
            _entities = _spaceMgr.taggedEntities.get(_gidTag, ())
            for _eid in _entities:
                _ent = KBEngine.entities.get(_eid)
                if _ent and _ent.getTempMiscProp(gameconst.AvatarProps.trapByTriggerredFlag, False):
                    _ret = True
                    break

            else:
                _ret = False

            if _ret:
                self.continue_handle_be_triggered(ctx)

            elif checkNow:
                self._controller.waiting_for_trigger(self.get_waiting_key(obj), self, ctx)

            else:
                WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: trap by triggered checkonce failed --"
                            " entityGID={}, num={}".format(self.id, entityGID, len(_entities)))


class DungeonMoveEntityToFixPosEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, entityGID, pos_, speed, moveAni, event_handler=None, **kwargs):
        super(DungeonMoveEntityToFixPosEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('entityGID', entityGID)
        self.add_param('pos_', pos_)
        self.add_param('speed', speed)
        self.add_param('moveAni', moveAni)
        self.add_param('moveUUID', utils.getUUID())

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        entityGID = self.get_param('entityGID', 0)
        pos_ = self.get_param('pos_')
        speed = self.get_param('speed', 0)
        moveAni = self.get_param('moveAni', gameconst.DungeonFlowMoveAni.RUN01)
        moveUUID = self.get_param('moveUUID')

        if not pos_:
            WARNING_MSG('FlowController::handleDungeonMoveEntityToFixedPos: unknown position', self.id)
            return

        spaceMgr = self.controller.owner
        gidTag = 'gid_{}'.format(entityGID)
        ents = spaceMgr.getEntitiesByTag(gidTag)
        for ent in ents:

            userData = {'type': gamemove.FLOW_CONTROLLER_FORCE_MOVE, 'moveUUID': moveUUID}

            _newBaseSpeed = _newAdjSpeed = 0.0
            _newMoveAni = ent.moveAni

            # region moveAni
            if moveAni != gameconst.DungeonFlowMoveAni.DEFAULT:
                _newMoveAni = moveAni
            # endregion

            # region spped
            if speed > 0:
                _newBaseSpeed = speed

            elif speed == 0 and ent.IsNpc:
                _d = NPC_DATA.datas.get(ent.npcId, {})
                if moveAni == gameconst.DungeonFlowMoveAni.RUN01:
                    _newBaseSpeed = _d.get('baseSpeed', 0.0)

                elif moveAni == gameconst.DungeonFlowMoveAni.RUN02:
                    _newBaseSpeed = _d.get('baseSpeed', 0.0)
                    _newAdjSpeed = _d.get('adjSpeed', 0.0)
            # endregion

            if _newBaseSpeed > 0:
                userData.update({"fc_OriginBaseSpeed": ent.baseSpeed})
                ent.setProp('baseSpeed', _newBaseSpeed, src=gameconst.SourceType.FlowCtrl)
            if _newAdjSpeed > 0:
                userData.update({"fc_OriginAdjSpeed": ent.adjSpeed})
                ent.setProp('adjSpeed', _newAdjSpeed, src=gameconst.SourceType.FlowCtrl)
            if _newMoveAni != ent.moveAni:
                userData.update({"fc_OriginMoveAni": ent.moveAni})
                ent.moveAni =_newMoveAni

            ent.cancelMoveController()
            if ent.aiController:
                ent.aiController.moveToFixedPositionInForce(pos_, userData)
            else:
                ent.navigateToPosition(pos_, userData)

        super(DungeonMoveEntityToFixPosEvent, self).handle_be_triggered(
            src_e, src_idx, idx, obj, **ref_params)

    def get_waiting_key(self, ctx):
        return self.get_move_key(self.get_param('moveUUID', 0))

    @staticmethod
    def get_move_key(moveUUID):
        return 'move_to_fixpos_{}'.format(moveUUID)


class MonsterHpMonitorTriggerEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('monsterGID', 'symbol', 'hpPercent')

    def __init__(self, event_id, controller, monsterGID, symbol, hpPercent, checkNow, checkOnce, event_handler=None,
                 **kwargs):
        super(MonsterHpMonitorTriggerEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('monsterGID', monsterGID)
        self.add_param('symbol', symbol)
        self.add_param('hpPercent', hpPercent)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)
        monsterGID = self.get_param('monsterGID', 0)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        hp = self.get_param('hpPercent', -1)

        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waiting_for_monster_hp_monitor_trigger(
                self, ctx, monsterGID, symbol, hp)

        else:
            _spaceMgr = self.controller.owner
            _gidTag = 'gid_{}'.format(monsterGID)
            _gitEidList = _spaceMgr.taggedEntities.get(_gidTag, [])
            if not _gitEidList:
                gameengine.reportCritical("MonsterHpMonitorTriggerEvent::ent not found", monsterGID, _gidTag)
                return

            for _eid in _gitEidList:
                _ent = KBEngine.entities.get(_eid)
                if not _ent:
                    continue

                _crtHpPrt = round(_ent.hp/_ent.fullHp*100, 2)
                _ret = gameconst.DungeonFlowCompareSymbol.compare(symbol, _crtHpPrt, hp)
                if _ret:
                    self.continue_handle_be_triggered(ctx)
                    break

                elif checkNow:
                    self._controller.waiting_for_monster_hp_monitor_trigger(
                        self, ctx, monsterGID, symbol, hp)
                    break

                else:
                    WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: entity hp checkonce failed --"
                                " symbol={}, {} {}".format(self.id, symbol, _crtHpPrt, hp, _ent.gameEntityId))


    def cancel(self, ctx):
        monsterGID = self.get_param('monsterGID', 0)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        hp = self.get_param('hpPercent', -1)

        ctrl = self.controller

        popList = []
        eList = ctrl._monster_waitings.get(
            monsterGID, {}).get(
            ctrl.MONSTER_WAITING_HP_MODIFY_KEY, {}).get(symbol, {}).get(hp)

        if eList:
            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class MonsterRestNumberEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('monsterGID', 'symbol', 'restNum')

    def __init__(self, event_id, controller, monsterGID, symbol, number, checkNow, checkOnce, event_handler=None, **kwargs):
        super(MonsterRestNumberEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('monsterGID', monsterGID)
        self.add_param('symbol', symbol)
        self.add_param('restNum', number)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)
        monsterGID = self.get_param('monsterGID', 0)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        number = self.get_param('restNum', -1)
        usePrototypeID = self.get_param('usePrototypeID', False)
        if usePrototypeID:
            monsterGID = "cbid{}".format(monsterGID)

        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waiting_for_monster_rest_number_trigger(
                self, ctx, monsterGID, symbol, number)

        else:
            _spaceMgr = self.controller.owner
            if monsterGID > 0:
                _gidTag = 'gid_{}'.format(monsterGID)
            else:
                # NOTE()(FLOW_CONTROLLER): rest number checkOnce All only support monster
                _gidTag = 'Monster'

            _currentNum = 0
            for _eid in _spaceMgr.taggedEntities.get(_gidTag, ()):
                _ent = KBEngine.entities.get(_eid)
                if _ent and not _ent.isDie():
                    _currentNum += 1
            _ret = gameconst.DungeonFlowCompareSymbol.compare(symbol, _currentNum, number)
            if _ret:
                self.continue_handle_be_triggered(ctx)

            elif checkNow:
                self._controller.waiting_for_monster_rest_number_trigger(
                    self, ctx, monsterGID, symbol, number)

            else:
                WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: rest number checkonce failed --"
                            " symbol={}, {} {}".format(self.id, symbol, _currentNum, number))

    def cancel(self, ctx):
        monsterGID = self.get_param('monsterGID', 0)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        number = self.get_param('restNum', -1)

        ctrl = self.controller

        popList = []
        eList = ctrl._monster_waitings.get(
            monsterGID, {}).get(
            ctrl.MONSTER_WAITING_REST_NUM, {}).get(symbol, {}).get(number)

        if eList:
            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class DungeonMonsterKillerNumberEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('monsterGID', 'symbol', 'killNum', 'checkOnce')

    def __init__(self, event_id, controller, monsterGID, symbol, number, checkNow, checkOnce, event_handler=None, **kwargs):
        super(DungeonMonsterKillerNumberEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('monsterGID', monsterGID)
        self.add_param('symbol', symbol)
        self.add_param('killNum', number)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)
        monsterGID = self.get_param('monsterGID', 0)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        number = self.get_param('killNum', -1)
        usePrototypeID = self.get_param('usePrototypeID', False)
        if usePrototypeID:
            monsterGID = "cbid{}".format(monsterGID)
        self._controller.waiting_for_dungeon_monster_kill_number_trigger(
            self, ctx, monsterGID, symbol, number)

        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce')
        if checkOnce or checkNow:
            spaceNo = ref_params['spaceNo']
            stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
            if monsterGID > 0:
                stub.flowCtrlCheckDungeonEntityKillNumber(spaceNo, monsterGID, symbol, number, usePrototypeID, self.id, obj, checkOnce)
            else:
                stub.flowCtrlCheckDungeonAllEntityKillNumber(spaceNo, symbol, number, self.id, obj, checkOnce)

    def cancel(self, ctx):
        monsterGID = self.get_param('monsterGID', 0)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        number = self.get_param('killNum', -1)

        ctrl = self.controller

        popList = []
        eList = ctrl._monster_waitings.get(
            monsterGID, {}).get(
            ctrl.DUNGEON_MONSTER_WAITING_KILL_NUM, {}).get(symbol, {}).get(number)

        if eList:
            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class DungeonPlayerRestNumEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ()

    def __init__(self, event_id, controller, event_handler=None, **kwargs):
        super().__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('symbol', kwargs['symbol'])
        self.add_param('playerNum', kwargs['number'])
        self.add_param('checkNow', kwargs['checkNow'])
        self.add_param('checkOnce', kwargs['checkOnce'])

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        number = self.get_param('playerNum', -1)

        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce')
        if not (checkOnce or checkNow):
            self._controller.waiting_for_dungeon_player_rest_num_trigger(self, ctx, symbol, number)

        else:
            _currentNum = 0
            for pid in self.controller.owner.players:
                pEnt = KBEngine.entities.get(pid)
                if pEnt:
                    _currentNum += 1

            _ret = gameconst.DungeonFlowCompareSymbol.compare(symbol, _currentNum, number)
            if _ret:
                self.continue_handle_be_triggered(ctx)

            elif checkNow:
                self._controller.waiting_for_dungeon_player_rest_num_trigger(self, ctx, symbol, number)

            else:
                WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: player rest number checkonce failed --"
                            " symbol={}, {} {}".format(self.id, symbol, _currentNum, number))
    def cancel(self, ctx):
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        number = self.get_param('playerNum', -1)

        ctrl = self.controller

        popList = []
        eList = ctrl._waitings.get(ctrl.GLOBAL_KEY, {}).get(
            ctrl.DUNGEON_PLAYER_REST_NUM, {}).get(symbol, {}).get(number)

        if eList:
            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class DungeonAlivePlayerEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('symbol', 'playerNum')

    def __init__(self, event_id, controller, symbol, number, checkNow, checkOnce, event_handler=None, **kwargs):
        super(DungeonAlivePlayerEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('symbol', symbol)
        self.add_param('playerNum', number)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        number = self.get_param('playerNum', -1)

        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce')
        if not (checkOnce or checkNow):
            self._controller.waiting_for_dungeon_alive_player_trigger(self, ctx, symbol, number)

        else:
            _currentNum = 0
            for pid in self.controller.owner.players:
                pEnt = KBEngine.entities.get(pid)
                if pEnt and not pEnt.isDie():
                    _currentNum += 1

            _ret = gameconst.DungeonFlowCompareSymbol.compare(symbol, _currentNum, number)
            if _ret:
                self.continue_handle_be_triggered(ctx)

            elif checkNow:
                self._controller.waiting_for_dungeon_alive_player_trigger(self, ctx, symbol, number)

            else:
                WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: alive player number checkonce failed --"
                            " symbol={}, {} {}".format(self.id, symbol, _currentNum, number))

    def cancel(self, ctx):
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        number = self.get_param('playerNum', -1)

        ctrl = self.controller

        popList = []
        eList = ctrl._waitings.get(ctrl.GLOBAL_KEY, {}).get(
            ctrl.DUNGEON_ALIVE_PLAYER, {}).get(symbol, {}).get(number)

        if eList:
            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class DungeonAnyPlayerHPMonitorTriggerEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    __self_params__ = ('symbol', 'hpPercent')

    def __init__(self, event_id, controller, symbol, hpPercent, checkNow, checkOnce, event_handler=None, **kwargs):
        super(DungeonAnyPlayerHPMonitorTriggerEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('symbol', symbol)
        self.add_param('hpPercent', hpPercent)
        self.add_param('checkNow', checkNow)
        self.add_param('checkOnce', checkOnce)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        hp = self.get_param('hpPercent', -1)

        checkNow = self.get_param('checkNow', False)
        checkOnce = self.get_param('checkOnce', False)
        if not (checkOnce or checkNow):
            self._controller.waiting_for_dungeon_any_player_hp_monitor_trigger(self, ctx, symbol, hp)

        else:
            for pid in self.controller.owner.players:
                pEnt = KBEngine.entities.get(pid)
                _currentHpPrt = round(pEnt.hp/pEnt.fullHp*100, 2)
                if pEnt and gameconst.DungeonFlowCompareSymbol.compare(symbol, _currentHpPrt, hp):
                    _ret = True
                    break
            else:
                _ret = False

            if _ret:
                self.continue_handle_be_triggered(ctx)

            elif checkNow:
                self._controller.waiting_for_dungeon_any_player_hp_monitor_trigger(self, ctx, symbol, hp)

            else:
                WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: check any player hp checkonce failed --"
                            " symbol={}, {} {}".format(self.id, symbol, _currentHpPrt, hp))

    def cancel(self, ctx):
        symbol = self.get_param('symbol', gameconst.DungeonFlowCompareSymbol.un)
        hp = self.get_param('hpPercent', -1)

        ctrl = self.controller

        popList = []
        eList = ctrl._waitings.get(ctrl.GLOBAL_KEY, {}).get(
            ctrl.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY, {}).get(symbol, {}).get(hp)

        if eList:
            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class DungeonValueCheckHoldEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin,
                                 _WaitingCancelMixin):

    def __init__(self, event_id, controller, varIds, event_handler=None, **kwargs):
        super(DungeonValueCheckHoldEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('varIds', varIds)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = ep_ctrl.context.WaitingEventContext(
            obj.tid, waiting_e=self,
            waiting_args=_w_args,
            waiting_kwargs=_w_kwargs)
        m_varIds = self.get_param('varIds', [])
        for m_varId in m_varIds:
            self._controller.waiting_for_dungeon_space_var_change_check(self, ctx, m_varId)


    def cancel(self, ctx):
        m_varIds = self.get_param('varIds', [])

        ctrl = self.controller

        for m_varId in m_varIds:
            popList = []
            eList = ctrl._waitings.get(ctrl.GLOBAL_KEY, {}).get(
                ctrl.DUNGEON_SPACE_VAR_CHECK_KEY, {}).get(m_varId)

            if not eList:
                continue

            for idx, (e, e_ctx) in enumerate(eList):
                if e_ctx.tid == ctx.tid:
                    popList.append(idx)

            for i in reversed(popList):
                eList.pop(i)


class DungeonEntityImmuneDeath(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, entityGID, event_handler=None, **kwargs):
        super(DungeonEntityImmuneDeath, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param("entityGID", entityGID)

    def get_waiting_key(self, ctx):
        return self.get_immune_death_key(self.get_param("entityGID", 0))

    @staticmethod
    def get_immune_death_key(entityGID):
        return "entity_immune_death_{}".format(entityGID)


class EntityRouteFinishedEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, entityGID, pathID, event_handler=None, **kwargs):
        super(EntityRouteFinishedEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('entityGID', entityGID)
        self.add_param('pathID', pathID)

    def get_waiting_key(self, ctx):
        return self.get_route_finished_key(self.get_param('entityGID', 0), self.get_param('pathID', 0))

    @staticmethod
    def get_route_finished_key(entityGID, pathID):
        return 'route_finished_{}_{}'.format(entityGID, pathID)


class EntityRoutingMissingEscortEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, entityGID, pathID, event_handler=None, **kwargs):
        super(EntityRoutingMissingEscortEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('entityGID', entityGID)
        self.add_param('pathID', pathID)

    def continue_handle_be_triggered(self, ctx):
        super().continue_handle_be_triggered(ctx)
        infLoop = self.get_param('infLoop', False)
        if infLoop:
            self.re_handle_be_triggered(*ctx.waiting_args, **ctx.waiting_kwargs)

    def get_waiting_key(self, ctx):
        return self.get_route_missing_escort_key(self.get_param('entityGID', 0), self.get_param('pathID', 0))

    @staticmethod
    def get_route_missing_escort_key(entityGID, pathID):
        return 'route_missing_escort_{}_{}'.format(entityGID, pathID)


class AnyPlayerCinemaPlayEndedEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, cinemaPlayID, delay, event_handler=None, **kwargs):
        super(AnyPlayerCinemaPlayEndedEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('cinemaPlayID', cinemaPlayID)
        self.add_param('delay', delay)
        self.eventCtrlId = 0

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        cinemaPlayID = self.get_param('cinemaPlayID', 0)
        delay = self.get_param('delay', 0)
        if delay <= 0:
            WARNING_MSG("AnyPlayerCinemaPlayEndedEvent::delay <=0, eid={} cid={} delay={}".format(
                self.id, cinemaPlayID, delay))
            delay = 0.1

        spaceMgr = self.controller.owner
        if not spaceMgr:
            ERROR_MSG('FlowController::AnyPlayerCinemaPlayEndedEvent:spaceMgr not found')
        else:
            if self.eventCtrlId > 0:
                spaceMgr._cancelCallback(
                    self.eventCtrlId, gametimer.TIMER_TAG_EPCTRL_PLAYER_CINEMA_PLAY_END_TIMEOUT)
            self.eventCtrlId = spaceMgr.toCallbackAfter(
                delay, gametimer.TIMER_TAG_EPCTRL_PLAYER_CINEMA_PLAY_END_TIMEOUT
            )._onAnyPlayerCinemaPlayEndedTimeout(cinemaPlayID, self.id)

        return super().handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)

    def continue_handle_be_triggered(self, ctx):
        if self.eventCtrlId > 0:
            spaceMgr = self.controller.owner
            spaceMgr and spaceMgr._cancelCallback(
                self.eventCtrlId, gametimer.TIMER_TAG_EPCTRL_PLAYER_CINEMA_PLAY_END_TIMEOUT)
        super().continue_handle_be_triggered(ctx)

    def get_waiting_key(self, ctx):
        return self.get_cinema_play_ended_key(self.get_param('cinemaPlayID', 0))

    @staticmethod
    def get_cinema_play_ended_key(cinemaPlayID):
        return 'cinema_player_ended_{}'.format(cinemaPlayID)


class _CommonCreateRandomlyEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):

    def __init__(self, event_id, controller, entityGIDs, number, rng, event_handler=None, **kwargs):
        super().__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('entityGIDs', entityGIDs)
        self.add_param('number', number)
        self.add_param('rng', rng)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        dungeonNo = ref_params['dungeonNo']
        spaceNo = ref_params['spaceNo']
        entityGIDs = self.get_param('entityGIDs', [])
        number = self.get_param('number', 1)

        filterEntityGIDs, otherEntityGIDs = self.filterEntityGIDs(entityGIDs)

        if len(filterEntityGIDs) < number:
            WARNING_MSG(f"FlowController::{self.__class__.__name__}:: filterEntityGIDs not enough",
                        self.id, entityGIDs, filterEntityGIDs, otherEntityGIDs, number)
            flagIds = [i for i in filterEntityGIDs]
        else:
            flagIds = self._getSampleEntityGIDs(filterEntityGIDs, number)

        if len(flagIds) < number:
            WARNING_MSG(f"FlowController::{self.__class__.__name__}:: flagIds not enough",
                        self.id, entityGIDs, flagIds, filterEntityGIDs, otherEntityGIDs, number)

        _overLimitNum = self.isEntityOverLimit(flagIds)
        if  _overLimitNum > 0:
            WARNING_MSG(f"FlowController::{self.__class__.__name__}:: Entity over limit",
                        self.id, entityGIDs, flagIds, filterEntityGIDs, otherEntityGIDs, number, _overLimitNum)
            flagIds = self._getSampleEntityGIDs(flagIds, max(len(flagIds) - _overLimitNum, 0))

        if not flagIds:
            WARNING_MSG(f"FlowController::{self.__class__.__name__}:: flagIds is Empty",
                        self.id, entityGIDs, flagIds, filterEntityGIDs, otherEntityGIDs, number, _overLimitNum)
            ctx = ep_ctrl.context.WaitingEventContext(
                obj.tid, waiting_e=self,
                waiting_args=(src_e, src_idx, idx, obj),
                waiting_kwargs=ref_params)
            self.continue_handle_be_triggered(ctx)
            return

        rng = self.get_param('rng', 0)
        extra = self.buildDefaultCreateEntityExtra()
        extra.update({'tmpProps': {'createRadius': rng, 'createCount': 1}})
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.createEntityInDungeonByGameEntityId(spaceNo, flagIds, 1, 0, extra)

        setattr(obj, self.get_context_flags_key(), flagIds)
        super().handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)

    def isEntityOverLimit(self, flagIds):
        return False

    def filterEntityGIDs(self, entityGIDs):
        _spaceMgr = self.controller.owner

        filterEntityGIDs, otherEntityGIDs = [], []
        for entityGID in entityGIDs:
            _gidTag = 'gid_{}'.format(entityGID)
            if _gidTag not in _spaceMgr.taggedEntities or not  _spaceMgr.taggedEntities[_gidTag]:
                filterEntityGIDs.append(entityGID)
                continue

            for _eid in _spaceMgr.taggedEntities.get(_gidTag, (0, )):
                _ent = KBEngine.entities.get(_eid)
                filterEntityGIDs.append(entityGID) if not _ent else otherEntityGIDs.append(entityGID)
                break

        return filterEntityGIDs, otherEntityGIDs

    def _getSampleEntityGIDs(self, entityGIDs, number):
        _realEntityGIDs = random.sample(entityGIDs, min(number, len(entityGIDs))) if entityGIDs else entityGIDs
        return _realEntityGIDs

    def get_waiting_key(self, ctx):
        entityGIDs = getattr(ctx, self.get_context_flags_key(), [])
        return get_common_release_key(self.id, entityGIDs)

    def get_context_flags_key(self):
        return f"flags_{self.__class__.__name__}_{self.id}"

    def buildDefaultCreateEntityExtra(self):
        return {'eventId': self.id, 'checkCreateUniqueness': True}

class DungeonRebornPosReleaseEvent(ep_ctrl.event.BaseWaitingEvent, _ElementHotReloadMixin, _WaitingCancelMixin):
    __self_params__ = ('rebornPosGIDs', 'rebornPosNum')
    __ref_params__ = ('dungeonNo', 'spaceNo')

    def __init__(self, event_id, controller, rebornPosGIDs, event_handler=None, **kwargs):
        super(DungeonRebornPosReleaseEvent, self).__init__(event_id, controller, event_handler, **kwargs)
        self.add_param('rebornPosGIDs', rebornPosGIDs)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        dungeonNo = ref_params['dungeonNo']
        spaceNo = ref_params['spaceNo']
        rebornPosGIDs = self.get_param('rebornPosGIDs', [])
        rebornPosNum = self.get_param('rebornPosNum', 1)
        stub = gameengine.getDungeonStubBySpaceNo(spaceNo)
        stub.createEntityInDungeonByGameEntityId(spaceNo, rebornPosGIDs, rebornPosNum, 0,
                                                 {'eventId': self.id})
        super(DungeonRebornPosReleaseEvent, self).handle_be_triggered(
            src_e, src_idx, idx, obj, **ref_params)

    def get_waiting_key(self, ctx):
        return self.get_coll_release_key(self.id, self.get_param('rebornPosGIDs', []))

    @staticmethod
    def get_coll_release_key(eventId, rebornPosGIDs):
        return get_common_release_key(eventId, rebornPosGIDs)
