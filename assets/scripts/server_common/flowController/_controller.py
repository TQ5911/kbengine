# coding: utf-8
from KBEDebug import *
import KBEngine

import gameengine
import gametimer
import gamemove
import gameconst
import formula
import random
import utils
import copy
import sMath, math, Math

import ep_ctrl

import skillInfo
import userType
import actionContext

import gamePlay_gamePlay as DDI
import creep_base as CBD
import skill_skill as SSD
import buff_buff as BUFF
import NPC_NPC as NPC_DATA
import formula_generalFormula as F_GFD

from ._conditions import *
from ._events import *


__all__ = [
    'FlowController'
]


class _FlowControllerBeTriggeredMixin(object):
    """callbacks"""

    def onTaskComplete(self, taskId):
        DEBUG_MSG('FlowController::onTaskComplete -> {}'.format(taskId))
        self.to_be_trigger(WaitingTaskCompleteEvent.get_task_key(taskId))

    def cancelTaskCompleteTriggerEvents(self, taskId, eids):
        DEBUG_MSG('FlowController::cancelTaskCompleteTriggerEvents => {}'.format(taskId))
        self.cancel_trigger_events(WaitingTaskCompleteEvent.get_task_key(taskId), ids=eids)

    def onTaskFailed(self, taskId):
        DEBUG_MSG('FlowController::onTaskFailed -> {}'.format(taskId))
        self.to_be_trigger(WaitingTaskFailedEvent.get_task_key(taskId))

    def cancelTaskFailedTriggerEvents(self, taskId, eids):
        DEBUG_MSG('FlowController::cancelTaskFailedTriggerEvents => {}'.format(taskId))
        self.cancel_trigger_events(WaitingTaskFailedEvent.get_task_key(taskId), ids=eids)

    def onTaskInProgress(self, taskId):
        DEBUG_MSG('FlowController::onTaskInProgress -> {}'.format(taskId))
        self.to_be_trigger(WaitingTaskInProgressEvent.get_task_key(taskId))

    def cancelTaskInProgressTriggerEvents(self, taskId, eids):
        DEBUG_MSG('FlowController::cancelTaskInProgressTriggerEvents => {}'.format(taskId))
        self.cancel_trigger_events(WaitingTaskInProgressEvent.get_task_key(taskId), ids=eids)

    def onDungeonMonsterReleaseComplete(self, monsterGIDs):
        gameengine.reportCritical("onDungeonMonsterReleaseComplete::deprecated",
                                  monsterGIDs, self.owner.spaceNo)

    def onDungeonNPCReleaseComplete(self, npcGIDs):
        gameengine.reportCritical("onDungeonNPCReleaseComplete::deprecated",
                                  npcGIDs, self.owner.spaceNo)

    def onDungeonCollectionReleaseComplete(self, collGIDs):
        gameengine.reportCritical("onDungeonCollectionReleaseComplete::deprecated",
                                  collGIDs, self.owner.spaceNo)

    def onDungeonCollectionBeCollected(self, collGID):
        DEBUG_MSG('FlowController::onDungeonCollectionBeCollected -> {}'.format(collGID))
        self._onCollectionBeCollected(collGID)
        self._onMultiCollectionAllBeCollected(collGID)

    def onDungeonCollectionBeCollectedUsePrototypeID(self, collID):
        DEBUG_MSG('FlowController::onDungeonCollectionBeCollectedUsePrototypeID -> {}'.format(collID))
        self._onCollectionBeCollected(collID, usePrototypeID=True)

    def _onCollectionBeCollected(self, collGID, usePrototypeID=False):
        m_events = self.getDungeonCollectionBeCollectedEvents()
        if not m_events:
            return

        collGID = 'cbid{}'.format(collGID) if usePrototypeID else collGID
        DEBUG_MSG('FlowController::_onCollectionBeCollected -> {}'.format(collGID))
        triggerEvents = []
        for i_collGID, i_events in m_events.items():
            if i_collGID == collGID:
                triggerEvents.extend(copy.copy(i_events))
                i_events.clear()
                break

        _re_triggerred_events = []
        for e, e_ctx in triggerEvents:
            _etuple = (e, e_ctx)
            e.continue_handle_be_triggered(e_ctx)
            for i_collGID in e.get_param('collGIDs', []):
                i_collGID = 'cbid{}'.format(i_collGID) if usePrototypeID else i_collGID
                i_list = m_events.get(i_collGID, [])
                if _etuple in i_list:
                    i_list.remove(_etuple)
            if e.get_param('infLoop'):
                e.re_handle_be_triggered(*e_ctx.waiting_args, **e_ctx.waiting_kwargs)

    def _onMultiCollectionAllBeCollected(self, collGID):
        m_events = self.getDungeonMultiCollectionBeCollectedEvents()
        if not m_events:
            return

        DEBUG_MSG('FlowController::_onMultiCollectionAllBeCollected -> {}'.format(collGID))
        triggerEvents = []
        for i_collGID, i_events in m_events.items():
            if i_collGID == collGID:
                triggerEvents.extend(copy.copy(i_events))
                i_events.clear()
                break

        _re_triggerred_events = []
        for e, e_ctx in triggerEvents:
            e.collected(collGID)
            if not e.isAllBeCollected():
                continue
            _etuple = (e, e_ctx)
            e.continue_handle_be_triggered(e_ctx)
            for i_collGID in e.get_param('collGIDs', []):
                i_list = m_events.get(i_collGID, [])
                if _etuple in i_list:
                    i_list.remove(_etuple)
            if e.get_param('infLoop'):
                e.re_handle_be_triggered(*e_ctx.waiting_args, **e_ctx.waiting_kwargs)

    def onDungeonBuffPointReleaseComplete(self, buffPointGIDs):
        gameengine.reportCritical("onDungeonBuffPointReleaseComplete::deprecated",
                                  buffPointGIDs, self.owner.spaceNo)

    def onDungeonAirWallReleaseComplete(self, airWallGIDs):
        gameengine.reportCritical("onDungeonAirWallReleaseComplete::deprecated",
                                  airWallGIDs, self.owner.spaceNo)

    def onDungeonTeleporterCreatedComplete(self, telGIDs):
        DEBUG_MSG('FlowController::onDungeonTeleporterCreatedComplete -> {}'.format(telGIDs))
        for telGID in telGIDs:
            self.to_be_trigger(DungeonTeleporterReleaseEvent.get_coll_release_key(telGID))

    def onMonsterInBattle(self, monsterGID):
        DEBUG_MSG('FlowController::onMonsterInBattle -> {}'.format(monsterGID))
        self.to_be_trigger(AIEnterAttackEvent.get_enter_attack_key(monsterGID))

    def onMonsterLeaveBattle(self, monsterGID):
        DEBUG_MSG('FlowController::onMonsterLeaveBattle -> {}'.format(monsterGID))
        self.to_be_trigger(AILeaveAttackEvent.get_leave_attack_key(monsterGID))

    def onDungeonTrapBeTriggered(self, entityGID):
        DEBUG_MSG('FlowController::onDungeonTrapBeTriggered -> {}'.format(entityGID))
        self.to_be_trigger(DungeonTrapBeTriggered.get_trap_be_triggered_key(entityGID))

    def onEntityMoveToFixPos(self, moveUUID, succ):
        DEBUG_MSG('FlowController::onEntityMoveToFixPos -> {} {}'.format(moveUUID, succ))
        succ and self.to_be_trigger(DungeonMoveEntityToFixPosEvent.get_move_key(moveUUID))

    def onDungeonEntityimmuneDeathBeTriggered(self, entityGID):
        DEBUG_MSG('FlowController::onDungeonEntityimmuneDeathBeTriggered -> {}'.format(entityGID))
        self.to_be_trigger(DungeonEntityImmuneDeath.get_immune_death_key(entityGID))

    def onEntityRouteFinished(self, entityGID, pathID):
        DEBUG_MSG('FlowController::onEntityRouteFinished -> {} {}'.format(entityGID, pathID))
        self.to_be_trigger(EntityRouteFinishedEvent.get_route_finished_key(entityGID, pathID))

    def onEntityRoutingMissingEscort(self, entityGID, pathID):
        DEBUG_MSG('FlowController::onEntityRoutingMissingEscort -> {} {}'.format(entityGID, pathID))
        self.to_be_trigger(EntityRoutingMissingEscortEvent.get_route_missing_escort_key(entityGID, pathID))

    def onPlayerCinemaPlayEnded(self, cinemaPlayID, eids=()):
        DEBUG_MSG('FlowController::onPlayerCinemaPlayEnded -> {} eids={}'.format(cinemaPlayID, eids))
        _key = AnyPlayerCinemaPlayEndedEvent.get_cinema_play_ended_key(cinemaPlayID)
        if not eids:
            self.to_be_trigger(_key)
        else:
            self.to_be_trigger_with_eids(_key, eids)

    def onDungeonEntityReleaseCompleteByEventId(self, flagIds, fromEventId):
        DEBUG_MSG(f"FlowController::onDungeonEntityReleaseCompleteByEventId -> {flagIds} {fromEventId}")
        self.to_be_trigger(get_common_release_key(fromEventId, flagIds))


    def onEntityRouteFinished(self, entityGID, pathID):
        DEBUG_MSG('FlowController::onEntityRouteFinished -> {} {}'.format(entityGID, pathID))
        self.to_be_trigger(EntityRouteFinishedEvent.get_route_finished_key(entityGID, pathID))

    def onMonsterHpBeModified(self, monsterGID, oldHp, crtHp, fullHp):
        _hpSymbol = int(crtHp - oldHp)
        if not _hpSymbol:
            return

        monsterHPEvents = self.getMonsterHpModifyEvents(monsterGID)
        if not monsterHPEvents:
            return

        fullHp = float(fullHp)
        oldHpPrt = round(oldHp/fullHp*100, 2)
        crtHpPrt = round(crtHp/fullHp*100, 2)

        DEBUG_MSG('FlowController::onMonsterHpBeModified {}: {} -> {}'.format(
            monsterGID, oldHpPrt, crtHpPrt))
        if _hpSymbol > 0:
            fns = (self._cm_handle_hp_eq, self._cm_handle_hp_gt, self._cm_handle_hp_ge)
        else:
            fns = (self._cm_handle_hp_eq, self._cm_handle_hp_lt, self._cm_handle_hp_le)

        for fn in fns:
            fn(monsterHPEvents, oldHpPrt, crtHpPrt)

    def _cm_handle_hp_ge(self, hpEvents, oldHpPrt, crtHpPrt):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        hpEvents = hpEvents.get(symbolEnum.ge, {})
        if hpEvents:
            triggerList = []
            for hpPrt, events in hpEvents.items():
                if oldHpPrt <= hpPrt <= crtHpPrt:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvent:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_hp_gt(self, hpEvents, oldHpPrt, crtHpPrt):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        hpEvents = hpEvents.get(symbolEnum.gt, {})
        if hpEvents:
            triggerList = []
            for hpPrt, events in hpEvents.items():
                if oldHpPrt <= hpPrt < crtHpPrt:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_hp_eq(self, hpEvents, oldHpPrt, crtHpPrt):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        hpEvents = hpEvents.get(symbolEnum.eq, {})
        if hpEvents:
            triggerList = []
            for hpPrt, events in hpEvents.items():
                if hpPrt == crtHpPrt:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_hp_le(self, hpEvents, oldHpPrt, crtHpPrt):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        hpEvents = hpEvents.get(symbolEnum.le, {})
        if hpEvents:
            triggerList = []
            for hpPrt, events in hpEvents.items():
                if oldHpPrt >= hpPrt >= crtHpPrt:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_hp_lt(self, hpEvents, oldHpPrt, crtHpPrt):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        hpEvents = hpEvents.get(symbolEnum.lt, {})
        if hpEvents:
            triggerList = []
            for hpPrt, events in hpEvents.items():
                if oldHpPrt >= hpPrt > crtHpPrt:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_num_ge(self, _restNumEvents, _newNumber):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        if symbolEnum.ge in _restNumEvents:
            triggerList = []
            restNumEvents = _restNumEvents[symbolEnum.ge]
            for cNumber, events in restNumEvents.items():
                if _newNumber >= cNumber:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_num_gt(self, _restNumEvents, _newNumber):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        if symbolEnum.gt in _restNumEvents:
            triggerList = []
            restNumEvents = _restNumEvents[symbolEnum.gt]
            for cNumber, events in restNumEvents.items():
                if _newNumber > cNumber:
                    copyEvents = copy.copy(events)
                    events.clear()
                    triggerList.extend(copyEvents)
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_num_eq(self, _restNumEvents, _newNumber):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        if symbolEnum.eq in _restNumEvents:
            triggerList = []
            restNumEvents = _restNumEvents[symbolEnum.eq]
            for cNumber, events in restNumEvents.items():
                if _newNumber == cNumber:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_num_le(self, _restNumEvents, _newNumber):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        if symbolEnum.le in _restNumEvents:
            triggerList = []
            restNumEvents = _restNumEvents[symbolEnum.le]
            for cNumber, events in restNumEvents.items():
                if _newNumber <= cNumber:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def _cm_handle_num_lt(self, _restNumEvents, _newNumber):
        symbolEnum = gameconst.DungeonFlowCompareSymbol
        if symbolEnum.lt in _restNumEvents:
            triggerList = []
            restNumEvents = _restNumEvents[symbolEnum.lt]
            for cNumber, events in restNumEvents.items():
                if _newNumber < cNumber:
                    copyEvents = copy.copy(events)
                    triggerList.extend(copyEvents)
                    events.clear()
                    # for e, e_ctx in copyEvents:
                    #     e.continue_handle_be_triggered(e_ctx)
            for e, e_ctx in triggerList:
                e.continue_handle_be_triggered(e_ctx)

    def onMonsterRestNumberIncreased(self, monsterGID, newNumber, newTotalNumber):
        monsterRestNumEvents, globalMonsterRestNumEvents = self.getMonsterRestNumEvents(monsterGID)
        if not (monsterRestNumEvents or globalMonsterRestNumEvents):
            return

        DEBUG_MSG('FlowController::onMonsterNestNumberIncreased {}: {}'.format(
            monsterGID, newNumber, newTotalNumber))

        for fn in (self._cm_handle_num_ge, self._cm_handle_num_gt, self._cm_handle_num_eq):
            monsterRestNumEvents and fn(monsterRestNumEvents, newNumber)
            globalMonsterRestNumEvents and fn(globalMonsterRestNumEvents, newTotalNumber)

    def onMonsterRestNumberDecreased(self, monsterGID, newNumber, newTotalNumber):
        monsterRestNumEvents, globalMonsterRestNumEvents = self.getMonsterRestNumEvents(monsterGID)
        if not (monsterRestNumEvents or globalMonsterRestNumEvents):
            return

        DEBUG_MSG('FlowController::onMonsterNestNumberDecreased {}: {} {}'.format(
            monsterGID, newNumber, newTotalNumber))

        for fn in (self._cm_handle_num_le, self._cm_handle_num_lt, self._cm_handle_num_eq):
            monsterRestNumEvents and fn(monsterRestNumEvents, newNumber)
            globalMonsterRestNumEvents and fn(globalMonsterRestNumEvents, newTotalNumber)

    def onDungeonMonsterKillNumIncreased(self, monsterGID, newNumber, newTotalNumber):
        monsterKillNumEvents, globalMonsterKillNumEvents = self.getDungeonMonsterKillNumEvents(monsterGID)
        if not (monsterKillNumEvents or globalMonsterKillNumEvents):
            return

        DEBUG_MSG('FlowController::onDungeonMonsterKillNumIncreased {}: {} {}'.format(
            monsterGID, newNumber, newTotalNumber))

        for fn in (self._cm_handle_num_ge, self._cm_handle_num_gt, self._cm_handle_num_eq):
            monsterKillNumEvents and fn(monsterKillNumEvents, newNumber)
            globalMonsterKillNumEvents and fn(globalMonsterKillNumEvents, newTotalNumber)

    def onCheckDungeonEntityKillNumberTriggered(self, monsterGID, symbol, number, currentKillNum, usePrototypeID, eids):
        _checkAll = monsterGID < 0
        _monsterGID = 'cbid{}'.format(monsterGID) if (monsterGID > 0 and usePrototypeID) else monsterGID
        monsterKillNumEvents, globalMonsterKillNumEvents = self.getDungeonMonsterKillNumEvents(_monsterGID)
        if not (monsterKillNumEvents or globalMonsterKillNumEvents):
            return

        DEBUG_MSG('FlowController::onCheckDungeonEntityKillNumberTriggered {}: symbol={} new->{} old->{} eids={}'.format(
            _monsterGID, symbol, currentKillNum, number, eids))

        triggerList = []
        if _checkAll:
            for killNum, events in globalMonsterKillNumEvents.get(symbol, {}).items():
                _ret = gameconst.DungeonFlowCompareSymbol.compare(symbol, currentKillNum, killNum)
                if not _ret:
                    continue
                triggerList.extend(events)

        else:
            for killNum, events in monsterKillNumEvents.get(symbol, {}).items():
                _ret = gameconst.DungeonFlowCompareSymbol.compare(symbol, currentKillNum, killNum)
                if not _ret:
                    continue
                triggerList.extend(events)

        for e, e_ctx in triggerList:
            e.continue_handle_be_triggered(e_ctx)

    def onDungeonPlayerRestNumberChanged(self, newNumber):
        restNumEvents = self.getDungeonPlayerRestNumEvents()
        if not restNumEvents:
            return

        DEBUG_MSG('FlowController::onDungeonPlayerRestNumberChanged: {}'.format(newNumber))

        for fn in (self._cm_handle_num_ge, self._cm_handle_num_gt, self._cm_handle_num_eq):
            restNumEvents and fn(restNumEvents, newNumber)

    def onDungeonAlivePlayerIncreased(self, newNumber):
        alivePlayerEvents = self.getDungeonAlivePlayerEvents()
        if not alivePlayerEvents:
            return

        DEBUG_MSG('FlowController::onDungeonAlivePlayerIncreased: {}'.format(newNumber))

        for fn in (self._cm_handle_num_ge, self._cm_handle_num_gt, self._cm_handle_num_eq):
            alivePlayerEvents and fn(alivePlayerEvents, newNumber)

    def onDungeonAlivePlayerDecreased(self, newNumber):
        alivePlayerEvents = self.getDungeonAlivePlayerEvents()
        if not alivePlayerEvents:
            return

        DEBUG_MSG('FlowController::onDungeonAlivePlayerDecreased: {}'.format(newNumber))

        for fn in (self._cm_handle_num_le, self._cm_handle_num_lt, self._cm_handle_num_eq):
            alivePlayerEvents and fn(alivePlayerEvents, newNumber)

    def onDunAnyPlayerHpBeModified(self, oldHp, crtHp, fullHp):
        _hpSymbol = int(crtHp - oldHp)
        if not _hpSymbol:
            return

        hpEvents = self.getDungeonAnyPlayerHpModifyEvents()
        if not hpEvents:
            return

        DEBUG_MSG('FlowController::onDunAnyPlayerHpBeModified: {} -> {}'.format(oldHp, crtHp))
        fullHp = float(fullHp)
        oldHpPrt = round(oldHp/fullHp*100, 2)
        crtHpPrt = round(crtHp/fullHp*100, 2)
        WARNING_MSG('FlowController::onDunAnyPlayerHpBeModified: pcg {} -> {}'.format(oldHpPrt, crtHpPrt))
        if _hpSymbol > 0:
            fns = (self._cm_handle_hp_eq, self._cm_handle_hp_gt, self._cm_handle_hp_ge)
        else:
            fns = (self._cm_handle_hp_eq, self._cm_handle_hp_lt, self._cm_handle_hp_le)

        for fn in fns:
            fn(hpEvents, oldHpPrt, crtHpPrt)

    def onDungeonValueCheckChanged(self, varId):
        m_events = self.getDungeonValueCheckHoldEvents()
        if not m_events:
            return

        DEBUG_MSG('FlowController::onDungeonValueCheckChanged -> {}'.format(varId))
        triggerEvents = []
        for i_varId, i_events in m_events.items():
            if i_varId == varId:
                triggerEvents.extend(copy.copy(i_events))
                i_events.clear()
                break

        for e, e_ctx in triggerEvents:
            e.continue_handle_be_triggered(e_ctx)
            for i_vid in e.get_param('varIds', []):
                i_list = m_events.get(i_vid, [])
                if (e, e_ctx) in i_list:
                    i_list.remove((e, e_ctx))

    def onDungeonRebornPosCreatedComplete(self, rebornPosGIDs):
        gameengine.reportCritical("onDungeonRebornPosCreatedComplete::deprecated",
                                  rebornPosGIDs, self.owner.spaceNo)


class _FlowControllerCustomEventsMixin(object):

    MONSTER_WAITING_HP_MODIFY_KEY = '_hp_modify'
    MONSTER_WAITING_REST_NUM = '_rest_num'
    DUNGEON_MONSTER_WAITING_KILL_NUM = '_d_kill_num'
    DUNGEON_ALIVE_PLAYER = '_d_alive_plr'
    DUNGEON_PLAYER_REST_NUM = '_d_player_rest_num'
    DUNGEON_ANY_PLAYER_HP_MODIFY_KEY = '_d_ap_hp_modify'
    DUNGEON_SPACE_VAR_CHECK_KEY = '_d_dunvar_check'
    DUNGEON_COLL_BE_COLLECT_KEY = '_d_coll_be_coll'
    DUNGEON_MULTI_COLL_BE_COLLTECT_KEY = '_d_mult_coll_be_coll'
    GLOBAL_KEY = '__GLOBAL__'

    def getMonsterHpModifyEvents(self, monsterGID):
        return self._getMonsterEvents(monsterGID, self.MONSTER_WAITING_HP_MODIFY_KEY)

    def getMonsterRestNumEvents(self, monsterGID):
        t = self._getMonsterEvents(monsterGID, self.MONSTER_WAITING_REST_NUM)
        a = self._getMonsterEvents(-1, self.MONSTER_WAITING_REST_NUM)
        return t, a

    def getDungeonMonsterKillNumEvents(self, monsterGID):
        t = self._getMonsterEvents(monsterGID, self.DUNGEON_MONSTER_WAITING_KILL_NUM)
        a = self._getMonsterEvents(-1, self.DUNGEON_MONSTER_WAITING_KILL_NUM)
        return t, a

    def getDungeonAlivePlayerEvents(self):
        return self._getWaitingsEvents(self._waitings, self.GLOBAL_KEY, self.DUNGEON_ALIVE_PLAYER)

    def getDungeonPlayerRestNumEvents(self):
        return self._getWaitingsEvents(self._waitings, self.GLOBAL_KEY, self.DUNGEON_PLAYER_REST_NUM)

    def getDungeonAnyPlayerHpModifyEvents(self):
        return self._getWaitingsEvents(self._waitings, self.GLOBAL_KEY, self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY)

    def getDungeonValueCheckHoldEvents(self):
        return self._getWaitingsEvents(self._waitings, self.GLOBAL_KEY, self.DUNGEON_SPACE_VAR_CHECK_KEY)

    def getDungeonCollectionBeCollectedEvents(self):
        return self._getWaitingsEvents(self._waitings, self.GLOBAL_KEY, self.DUNGEON_COLL_BE_COLLECT_KEY)

    def getDungeonMultiCollectionBeCollectedEvents(self):
        return self._getWaitingsEvents(self._waitings, self.GLOBAL_KEY, self.DUNGEON_MULTI_COLL_BE_COLLTECT_KEY)

    def _getMonsterEvents(self, monsterGID, key):
        return self._getWaitingsEvents(self._monster_waitings, monsterGID, key)

    def waiting_for_monster_hp_monitor_trigger(self, e, e_ctx, monsterGID, symbol, hp):
        self._monster_waitings.setdefault(monsterGID, {})
        self._monster_waitings[monsterGID].setdefault(self.MONSTER_WAITING_HP_MODIFY_KEY, {})
        self._monster_waitings[monsterGID][self.MONSTER_WAITING_HP_MODIFY_KEY].setdefault(symbol, {})
        self._monster_waitings[monsterGID][self.MONSTER_WAITING_HP_MODIFY_KEY][symbol].setdefault(hp, [])
        self._monster_waitings[monsterGID][self.MONSTER_WAITING_HP_MODIFY_KEY][symbol][hp].append((e, e_ctx))

    def waiting_for_monster_rest_number_trigger(self, e, e_ctx, monsterGID, symbol, restNum):
        self._monster_waitings.setdefault(monsterGID, {})
        self._monster_waitings[monsterGID].setdefault(self.MONSTER_WAITING_REST_NUM, {})
        self._monster_waitings[monsterGID][self.MONSTER_WAITING_REST_NUM].setdefault(symbol, {})
        self._monster_waitings[monsterGID][self.MONSTER_WAITING_REST_NUM][symbol].setdefault(restNum, [])
        self._monster_waitings[monsterGID][self.MONSTER_WAITING_REST_NUM][symbol][restNum].append((e, e_ctx))

    def waiting_for_dungeon_monster_kill_number_trigger(self, e, e_ctx, monsterGID, symbol, killNum):
        self._monster_waitings.setdefault(monsterGID, {})
        self._monster_waitings[monsterGID].setdefault(self.DUNGEON_MONSTER_WAITING_KILL_NUM, {})
        self._monster_waitings[monsterGID][self.DUNGEON_MONSTER_WAITING_KILL_NUM].setdefault(symbol, {})
        self._monster_waitings[monsterGID][self.DUNGEON_MONSTER_WAITING_KILL_NUM][symbol].setdefault(killNum, [])
        self._monster_waitings[monsterGID][self.DUNGEON_MONSTER_WAITING_KILL_NUM][symbol][killNum].append((e, e_ctx))

    def waiting_for_dungeon_alive_player_trigger(self, e, e_ctx, symbol, playerNum):
        self._waitings.setdefault(self.GLOBAL_KEY, {})
        self._waitings[self.GLOBAL_KEY].setdefault(self.DUNGEON_ALIVE_PLAYER, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_ALIVE_PLAYER].setdefault(symbol, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_ALIVE_PLAYER][symbol].setdefault(playerNum, [])
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_ALIVE_PLAYER][symbol][playerNum].append((e, e_ctx))

    def waiting_for_dungeon_player_rest_num_trigger(self, e, e_ctx, symbol, playerNum):
        self._waitings.setdefault(self.GLOBAL_KEY, {})
        self._waitings[self.GLOBAL_KEY].setdefault(self.DUNGEON_PLAYER_REST_NUM, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_PLAYER_REST_NUM].setdefault(symbol, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_PLAYER_REST_NUM][symbol].setdefault(playerNum, [])
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_PLAYER_REST_NUM][symbol][playerNum].append((e, e_ctx))

    def waiting_for_dungeon_any_player_hp_monitor_trigger(self, e, e_ctx, symbol, hp):
        self._waitings.setdefault(self.GLOBAL_KEY, {})
        self._waitings[self.GLOBAL_KEY].setdefault(self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY].setdefault(symbol, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY][symbol].setdefault(hp, [])
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY][symbol][hp].append((e, e_ctx))

    def waiting_for_dungeon_space_var_change_check(self, e, e_ctx, varId):
        self._waitings.setdefault(self.GLOBAL_KEY, {})
        self._waitings[self.GLOBAL_KEY].setdefault(self.DUNGEON_SPACE_VAR_CHECK_KEY, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_SPACE_VAR_CHECK_KEY].setdefault(varId, [])
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_SPACE_VAR_CHECK_KEY][varId].append((e, e_ctx))

    def waiting_for_dungeon_collection_be_collected_trigger(self, e, e_ctx, collGID):
        self._waitings.setdefault(self.GLOBAL_KEY, {})
        self._waitings[self.GLOBAL_KEY].setdefault(self.DUNGEON_COLL_BE_COLLECT_KEY, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_COLL_BE_COLLECT_KEY].setdefault(collGID, [])
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_COLL_BE_COLLECT_KEY][collGID].append((e, e_ctx))

    def waiting_for_dungeon_multi_collection_all_be_colllected(self, e, e_ctx, collGID):
        self._waitings.setdefault(self.GLOBAL_KEY, {})
        self._waitings[self.GLOBAL_KEY].setdefault(self.DUNGEON_MULTI_COLL_BE_COLLTECT_KEY, {})
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_MULTI_COLL_BE_COLLTECT_KEY].setdefault(collGID, [])
        self._waitings[self.GLOBAL_KEY][self.DUNGEON_MULTI_COLL_BE_COLLTECT_KEY][collGID].append((e, e_ctx))


class FlowController(ep_ctrl.controller.Controller, userType.UserSoleType,
                     _FlowControllerBeTriggeredMixin,
                     _FlowControllerCustomEventsMixin):

    # -----------------------------------------------------------------

    def _lateReload(self):
        DEBUG_MSG('Controller::_lateReload')
        self._lateReloadVariables()
        self._lateReloadElements()
        self._lateReloadWaitings()
        self._lateReloadMonsterWaitins()
        self._lateReloadReWaitings()
        self._lateReloadStartNode()

    def _lateReloadVariables(self):
        DEBUG_MSG(' - Controller::_lateReloadVariables')
        for v in self._variables.values():
            getattr(v, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()

    def _lateReloadElements(self):
        DEBUG_MSG(' - Controller::_lateReloadElements')
        for v in self._elements.values():
            getattr(v, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()

    def _lateReloadWaitings(self):
        DEBUG_MSG(' - Controller::_lateReloadWaitings')

        def _lateReloadGlobalWaitings(data):
            DEBUG_MSG(' -\ Controller::_lateReloadGlobalWaitings')
            for _k, _v in data.items():
                # data[self.DUNGEON_ALIVE_PLAYER][symbol][playerNum][(e, e_ctx), ...]
                for symbolNumDic in _v.values():
                    for eList in symbolNumDic.values():
                        for _e, _ctx in eList:
                            getattr(_e, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()
                            getattr(_ctx, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()

        for k, v in self._waitings.items():
            if k == self.GLOBAL_KEY:
                _lateReloadGlobalWaitings(v)
            else:
                for e, ctx in v:
                    getattr(e, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()
                    getattr(ctx, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()

    def _lateReloadMonsterWaitins(self):
        DEBUG_MSG(' - Controller::_lateReloadMonsterWaitins')
        # _monster_waitings[monsterGID][self.MONSTER_WAITING_HP_MODIFY_KEY][symbol][hp][(e, e_ctx), ...]
        for v in self._monster_waitings.values():
            for key, val in v.items():
                for symbolDic in val.values():
                    for eList in symbolDic.values():
                        for e, ctx in eList:
                            getattr(e, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()
                            getattr(ctx, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()

    def _lateReloadReWaitings(self):
        DEBUG_MSG(' - Controller::_lateReloadReWaitings')
        for v in self._re_waitings_cache.values():
            for e, ctx in v:
                getattr(e, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()
                getattr(ctx, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()

    def _lateReloadStartNode(self):
        DEBUG_MSG(' - Controller::_lateReloadStartNode')
        getattr(self._start_node, 'reloadScript', ep_ctrl.utils.EMPTY_FUNC)()

    # -----------------------------------------------------------------

    def __init__(self, owner, start_node=None):
        super(FlowController, self).__init__(start_node=start_node)
        self._monster_waitings = {}
        self._owner = owner.id

    def to_be_trigger_with_eids(self, key, eids):
        if key not in self._waitings:
            return
        events = self._waitings[key]
        copy_events = []
        dels_eventids = []
        for idx, (e, e_ctx) in enumerate(events):
            if e.id in eids:
                copy_events.append((e, e_ctx))
                dels_eventids.append(idx)
        for i in reversed(dels_eventids):
            del events[i]
        try:
            for e, e_ctx in copy_events:
                e.continue_handle_be_triggered(e_ctx)
        finally:
            if not self._waitings[key]:
                del self._waitings[key]
            if key in self._re_waitings_cache:
                re_events = self._re_waitings_cache[key]
                dels_rmeventids = []
                for idx, (e, e_ctx) in enumerate(re_events):
                    if e.id in eids:
                        self.waiting_for_trigger(key, e, e_ctx)
                        dels_rmeventids.append(idx)
                for i in reversed(dels_rmeventids):
                    del re_events[i]
                if not self._re_waitings_cache[key]:
                    del self._re_waitings_cache[key]

    @property
    def owner(self):
        return KBEngine.entities.get(self._owner)

    def _buildName(self, name, eid):
        return "{}_{}".format(name, eid)

    def getEventByEventId(self, eid, default=None):
        return self._elements.get(eid, default)

    @staticmethod
    def _getWaitingsEvents(waitings, mKey, key):
        if mKey not in waitings:
            return
        monsterEvents = waitings[mKey]
        if not monsterEvents:
            return

        if key not in monsterEvents:
            return
        return monsterEvents[key]

    def cancelWaitingTriggerEvents(self, ctx, eids):
        for eid in eids:
            e = self._elements.get(eid)
            e and e.cancel(ctx)

    def buildStopDelayEvent(self, eventId, eventIDs):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleStopDelayEvent,
                               name=gameconst.DungeonFlowEventName.stopDelayEvent)
        e.add_param('eventIDs', eventIDs)
        return e

    def buildStartDungeonEvent(self, eventId, dungeonNo, spaceNo):
        """开始副本事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleStartDungeon,
                               name=gameconst.DungeonFlowEventName.dunStart)
        e.add_param('dungeonNo', dungeonNo)
        e.add_param('spaceNo', spaceNo)
        return e

    def buildDelayEndDungeonEvent(self, eventId, dungeonNo, spaceNo, delayTime, preDelayTime, isFail=False):
        """延迟结束副本事件"""
        e = self.build_element(DelayDungeonEnd, element_id=eventId,
                               event_handler=handleDelayEndDungeon,
                               name=gameconst.DungeonFlowEventName.dunDelayEnd,
                               dungeonNo=dungeonNo, spaceNo=spaceNo, delayTime=delayTime,
                               isFail=isFail, preDelayTime=preDelayTime)
        return e

    def buildEndDungeonEvent(self, eventId, dungeonNo, spaceNo, delayTime, isFail=False):
        """结束副本事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleEndDungeon,
                               name=gameconst.DungeonFlowEventName.dunFailed if isFail else gameconst.DungeonFlowEventName.dunEnd)
        e.add_param('dungeonNo', dungeonNo)
        e.add_param('spaceNo', spaceNo)
        e.add_param('delayTime', delayTime)
        e.add_param('isFail', isFail)
        return e

    def buildReleaseDungeonMonsterEvent(self, eventId, monsterGIDs, monsterNum, monsterLevel,
                                        overwriteProps, ifSetBoss, initState):
        """释放怪物事件"""
        e = self.build_element(DungeonMonsterReleaseEvent, element_id=eventId,
                               event_handler=handleReleaseMonster, monsterGIDs=monsterGIDs,
                               name=gameconst.DungeonFlowEventName.createMonster)
        e.add_param('monsterNum', monsterNum)
        e.add_param('monsterLevel', monsterLevel)
        e.add_param('overwriteProps', overwriteProps)
        e.add_param('ifSetBoss', ifSetBoss)
        e.add_param('initState', initState)
        return e


    def buildMonsterChangeInitState(self, eventId, monsterGIDs, initState):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleMonsterChangeInitState,
                               name=gameconst.DungeonFlowEventName.monsterChangeInitState)
        e.add_param('monsterGIDs', monsterGIDs)
        e.add_param('initState', initState)
        return e

    def buildMonsterAddHateValue(self, eventId, entityIds, chooseType, hateValue):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleMonsterAddHateValue,
                               name=gameconst.DungeonFlowEventName.monsterAddHateValue)
        e.add_param('monsterGIDs', entityIds)
        e.add_param('chooseType', chooseType)
        e.add_param('hateValue', hateValue)
        return e

    def buildRecycleDungeonMonsterEvent(self, eventId, monsterGIDs):
        """回收怪物事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRecycleMonster,
                               name=gameconst.DungeonFlowEventName.removeMonster)
        e.add_param('monsterGIDs', monsterGIDs)
        return e

    def buildDungeonRemoveNoHostCreation(self, eventId, creationGIDs, userPrototypeID):
        """回收创生事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonRemoveNoHostCreation,
                               name=gameconst.DungeonFlowEventName.removeNoHostCreation)
        e.add_param('creationGIDs', creationGIDs)
        e.add_param('userPrototypeID', userPrototypeID)
        return e

    def buildReleaseDungeonNPCEvent(self, eventId, npcGIDs, npcNum, npcLevel, ifSetBoss):
        """释放NPC事件"""
        e = self.build_element(DungeonNPCReleaseEvent, element_id=eventId,
                               npcGIDs=npcGIDs, event_handler=handleReleaseNPC,
                               name=gameconst.DungeonFlowEventName.createNPC)
        e.add_param('npcNum', npcNum)
        e.add_param('npcLevel', npcLevel)
        e.add_param('ifSetBoss', ifSetBoss)
        return e

    def buildRecycleDungeonNPCEvent(self, eventId, npcGIDs):
        """回收NPC事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRecycleNPC,
                               name=gameconst.DungeonFlowEventName.removeNPC)
        e.add_param('npcGIDs', npcGIDs)
        return e

    def buildReleaseDungeonCollectionEvent(self, eventId, collGIDs, collNum, randomCollectionNum, checkHaveInFixed):
        """释放采集物事件"""
        e = self.build_element(DungeonCollectionReleaseEvent, element_id=eventId,
                               collGIDs=collGIDs, event_handler=handleReleaseCollection,
                               name=gameconst.DungeonFlowEventName.createCollection)
        e.add_param('collNum', collNum)
        e.add_param('randomCollectionNum', randomCollectionNum)
        e.add_param('checkHaveInFixed', checkHaveInFixed)
        return e

    def buildDungeonCollectionBeCollectedEvent(self, eventId, collGIDs, usePrototypeID, infLoop, checkNow, checkOnce):
        e = self.build_element(DungeonCollectionBeCollectedEvent, element_id=eventId,
                               collGIDs=collGIDs, checkNow=checkNow, checkOnce=checkOnce,
                               event_handler=handleCollBeCollected,
                               name=gameconst.DungeonFlowEventName.collBeCollected)
        e.add_param('usePrototypeID', usePrototypeID)
        e.add_param('infLoop', infLoop)
        return e

    def buildDungeonMultiCollectionAllBeCollectedEvent(self, eventId, collGIDs, infLoop):
        e = self.build_element(DungeonMultiCollectionAllBeCollectedEvent, element_id=eventId,
                               collGIDs=collGIDs, event_handler=handleMultiCollAllBeCollected,
                               name=gameconst.DungeonFlowEventName.multiCollAllBeCollected)
        e.add_param('infLoop', infLoop)
        return e

    def buildRecycleDungeonCollectionEvent(self, eventId, collGIDs):
        """回收采集物事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRecycleCollection,
                               name=gameconst.DungeonFlowEventName.removeCollection)
        e.add_param('collGIDs', collGIDs)
        return e

    def buildReleaseDungeonBuffPointEvent(self, eventId, buffPointGIDs, buffPointNum):
        """释放buff刷新点事件"""
        e = self.build_element(DungeonBuffPointReleaseEvent, element_id=eventId,
                               buffPointGIDs=buffPointGIDs, event_handler=handleReleaseBuffPoint,
                               name=gameconst.DungeonFlowEventName.createBuffPoint)
        e.add_param('buffPointNum', buffPointNum)
        return e

    def buildRecycleDungeonBuffPointEvent(self, eventId, buffPointGIDs):
        """回收buff刷新点事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRecycleBuffPoint,
                               name=gameconst.DungeonFlowEventName.removeBuffPoint)
        e.add_param('buffPointGIDs', buffPointGIDs)
        return e

    def buildReleaseDungeonAirWallEvent(self, eventId, airWallGIDs, airWallNum):
        """释放空气墙事件"""
        e = self.build_element(DungeonAirWallReleaseEvent, element_id=eventId,
                               airWallGIDs=airWallGIDs, event_handler=handleReleaseAirWall,
                               name=gameconst.DungeonFlowEventName.createAirWall)
        e.add_param('airWallNum', airWallNum)
        return e

    def buildRecycleDungeonAirWallEvent(self, eventId, airWallGIDs):
        """回收空气墙事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRecycleAirWall,
                               name=gameconst.DungeonFlowEventName.removeAirWall)
        e.add_param('airWallGIDs', airWallGIDs)
        return e

    def buildWaitingTaskCompleteEvent(self, eventId, taskId, checkNow, checkOnce):
        """等待任务完成事件"""
        e = self.build_element(WaitingTaskCompleteEvent, element_id=eventId,
                               event_handler=handleWaitingTaskCompleteEvent,
                               task_id=taskId, checknow=checkNow, checkOnce=checkOnce,
                               name=gameconst.DungeonFlowEventName.taskFinished)
        return e

    def buildWaitingTaskFailedEvent(self, eventId, taskId, checkNow, checkOnce):
        """等待任务失败事件"""
        e = self.build_element(WaitingTaskFailedEvent, element_id=eventId,
                               event_handler=handleWaitingTaskFailedEvent,
                               task_id=taskId, checknow=checkNow, checkOnce=checkOnce,
                               name=gameconst.DungeonFlowEventName.taskFailed)
        return e

    def buildMonsterHpEvent(self, eventId, monsterGID, symbol, hpPercent, checkNow, checkOnce):
        """怪物血量变化触发"""
        e = self.build_element(MonsterHpMonitorTriggerEvent, element_id=eventId,
                               monsterGID=monsterGID, symbol=symbol, hpPercent=hpPercent,
                               checkNow=checkNow, checkOnce=checkOnce,
                               event_handler=handleMonsterHpEvent,
                               name=gameconst.DungeonFlowEventName.monsterHp)
        return e

    def buildMonsterRestNumEvent(self, eventId, monsterGID, symbol, number, usePrototypeID, checkNow, checkOnce):
        e = self.build_element(MonsterRestNumberEvent, element_id=eventId,
                               monsterGID=monsterGID, symbol=symbol, number=number,
                               checkNow=checkNow, checkOnce=checkOnce,
                               event_handler=handleMonsterRestNumEvent,
                               name=gameconst.DungeonFlowEventName.monsterRestNum)
        e.add_param('usePrototypeID', usePrototypeID)
        return e

    def buildDungeonMonsterKillNumEvent(self, eventId, monsterGID, symbol, number, usePrototypeID, checkNow, checkOnce):
        e = self.build_element(DungeonMonsterKillerNumberEvent, element_id=eventId,
                               monsterGID=monsterGID, symbol=symbol, number=number,
                               checkNow=checkNow, checkOnce=checkOnce,
                               name=gameconst.DungeonFlowEventName.killMonsterNum)
        e.add_param('usePrototypeID', usePrototypeID)
        return e

    def buildDungeonMonsterCastSkill(self, eventId, monsterGID, skillID, skillLevel, forceToUse):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonMonsterCastSkill,
                               name=gameconst.DungeonFlowEventName.castSkill)
        e.add_param('monsterGID', monsterGID)
        e.add_param('skillID', skillID)
        e.add_param('skillLevel', skillLevel)
        e.add_param('forceToUse', forceToUse)
        return e

    def buildDungeonAddBuffToMonster(self, eventId, monsterGIDs, buffIDs, buffLevel, buffLevelLimit, duration):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonAddBuffToMonster,
                               name=gameconst.DungeonFlowEventName.addBuffToMonster)
        e.add_param('monsterGIDs', monsterGIDs)
        e.add_param('buffIDs', buffIDs)
        e.add_param('buffLevel', buffLevel)
        e.add_param('buffLevelLimit', buffLevelLimit)
        e.add_param('duration', duration)
        return e

    def buildDungeonRemoveBuffFromMonster(self, eventId, monsterGID, buffID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonRemoveBuffFromMonster,
                               name=gameconst.DungeonFlowEventName.removeBuffFromMonster)
        e.add_param('monsterGID', monsterGID)
        e.add_param('buffID', buffID)
        return e

    def buildDungeonAddBuffToAllPlayer(self, eventId, buffIDs, buffLevel, messageID, buffLevelLimit, duration):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonAddBuffToAllPlayer,
                               name=gameconst.DungeonFlowEventName.addBuffToAllPlayer)
        e.add_param('buffIDs', buffIDs)
        e.add_param('buffLevel', buffLevel)
        e.add_param('messageID', messageID)
        e.add_param('buffLevelLimit', buffLevelLimit)
        e.add_param('duration', duration)
        return e

    def buildDungeonRemoveBuffFromAllPlayer(self, eventId, buffID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonRemoveBuffFromAllPlayer,
                               name=gameconst.DungeonFlowEventName.removeBuffFromAllPlayer)
        e.add_param('buffID', buffID)
        return e

    def buildDungeonAddBuffToPlayer(self, eventId, monsterGID, positionType,
                                    buffIDs, buffLevel, buffLevelLimit, duration,
                                    number, messageID, rng, minRng, exceptHighestHate):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonAddBuffToPlayer,
                               name=gameconst.DungeonFlowEventName.addBuffToPlayer)
        e.add_param('monsterGID', monsterGID)
        e.add_param('positionType', positionType)
        e.add_param('buffIDs', buffIDs)
        e.add_param('buffLevel', buffLevel)
        e.add_param('buffLevelLimit', buffLevelLimit)
        e.add_param('duration', duration)
        e.add_param('number', number)
        e.add_param('messageID', messageID)
        e.add_param('rng', rng)
        e.add_param('minRng', minRng)
        e.add_param('exceptHighestHate', exceptHighestHate)
        return e

    def buildDungeonSummonMonsterInFixedPosition(self, eventId, monsterGID, summonGIDs, summonIDs, summonNum,
                                                 pos_, dir_, dieWithHost):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonSummonMonsterInFixedPosition,
                               name=gameconst.DungeonFlowEventName.summonMonsterInFixedPosition)
        e.add_param('monsterGID', monsterGID)
        e.add_param('summonGIDs', summonGIDs)
        e.add_param('summonIDs', summonIDs)
        e.add_param('summonNum', summonNum)
        e.add_param('pos', pos_)
        e.add_param('dir', dir_)
        e.add_param('dieWithHost', dieWithHost)
        return e

    def buildDungeonCreateCreationInFixedPosition(self, eventId, monsterGID, creationGIDs, creationIDs, creationNum,
                                                  pos_, dir_):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonCreateCreationInFixedPosition,
                               name=gameconst.DungeonFlowEventName.createCreationInFixedPosition)
        e.add_param('monsterGID', monsterGID)
        e.add_param('creationGIDs', creationGIDs)
        e.add_param('creationIDs', creationIDs)
        e.add_param('creationNum', creationNum)
        e.add_param('pos', pos_)
        e.add_param('dir', dir_)
        return e

    def buildDungeonBroadcastMsg(self, eventId, messageID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleBroadcastMsg,
                               name=gameconst.DungeonFlowEventName.broadcastMsg)
        e.add_param('messageID', messageID)
        return e

    def buildClearDungeon(self, eventId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleClearDungeon,
                               name=gameconst.DungeonFlowEventName.clearDungeon)
        return e

    def buildMonsterInBattle(self, eventId, monsterGID, checkNow, checkOnce):
        e = self.build_element(AIEnterAttackEvent, element_id=eventId,
                               checkNow=checkNow, checkOnce=checkOnce,
                               event_handler=handleMonsterInBattle,
                               name=gameconst.DungeonFlowEventName.monsterInBattle,
                               monsterGID=monsterGID)
        return e

    def buildMonsterLeaveBattle(self, eventId, monsterGID, checkNow, checkOnce):
        e = self.build_element(AILeaveAttackEvent, element_id=eventId,
                               checkNow=checkNow, checkOnce=checkOnce,
                               event_handler=handleMonsterLeaveBattle,
                               name=gameconst.DungeonFlowEventName.monsterLeaveBattle,
                               monsterGID=monsterGID)
        return e

    def buildDungeonAlivePlayer(self, eventId, symbol, number, checkNow, checkOnce):
        return self.build_element(DungeonAlivePlayerEvent, element_id=eventId,
                                  event_handler=handleDungeonAlivePlayerEvent,
                                  name=gameconst.DungeonFlowEventName.alivePlayer,
                                  symbol=symbol, number=number,
                                  checkNow=checkNow, checkOnce=checkOnce)

    def buildDungeonPlayerRestNum(self, eventId, symbol, number, checkNow, checkOnce):
        return self.build_element(
            DungeonPlayerRestNumEvent,
            element_id=eventId,
            event_handler=handlePlayerRestNumEvent,
            name=gameconst.DungeonFlowEventName.playerRestNum,
            symbol=symbol,
            number=number,
            checkNow=checkNow,
            checkOnce=checkOnce
        )


    def buildTaskUndertake(self, eventId, taskID):
        e = self.build_element(
            FlowEvent,
            element_id=eventId,
            event_handler=handleTaskUndertake,
            name=gameconst.DungeonFlowEventName.taskUndertake,
            taskID=taskID,
        )
        e.add_param('taskID', taskID)
        return e


    def buildCreateSummonInPlayerPosition(self, eventId, monsterGID, summonIDs,
                                          positionType, rng, minRng, number, exceptHighestHate,
                                          dieWithHost):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonCreateSummonInPlayerPosition,
                               name=gameconst.DungeonFlowEventName.createSummonInPlayerPosition)
        e.add_param('monsterGID', monsterGID)
        e.add_param('summonIDs', summonIDs)
        e.add_param('positionType', positionType)
        e.add_param('rng', rng)
        e.add_param('minRng', minRng)
        e.add_param('number', number)
        e.add_param('exceptHighestHate', exceptHighestHate)
        e.add_param('dieWithHost', dieWithHost)
        return e

    def buildCreateCreationInPlayerPosition(self, eventId, monsterGID, creationIDs,
                                            positionType, rng, minRng, number, exceptHighestHate):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonCreateCreationInPlayerPosition,
                               name=gameconst.DungeonFlowEventName.createCreationInPlayerPosition)
        e.add_param('monsterGID', monsterGID)
        e.add_param('creationIDs', creationIDs)
        e.add_param('positionType', positionType)
        e.add_param('rng', rng)
        e.add_param('minRng', minRng)
        e.add_param('number', number)
        e.add_param('exceptHighestHate', exceptHighestHate)
        return e

    def buildCreateCreationInMonsterPosition(self, eventId, monsterGID, creationIDs, targetMonsterGID, rng, number):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleCreateCreationInMonsterPosition,
                               name=gameconst.DungeonFlowEventName.createCreationInMonsterPosition)
        e.add_param('monsterGID', monsterGID)
        e.add_param('creationIDs', creationIDs)
        e.add_param('targetMonsterGID', targetMonsterGID)
        e.add_param('rng', rng)
        e.add_param('number', number)
        return e

    def buildDungeonMonsterCastSkillToPlayer(self, eventId, monsterGID, skillID,
                                             positionType, boardMessageID, number,
                                             rng, minRng, exceptHighestHate):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonMonsterCastSkillToPlayer,
                               name=gameconst.DungeonFlowEventName.castSkillToPlayer)
        e.add_param('monsterGID', monsterGID)
        e.add_param('skillID', skillID)
        e.add_param('positionType', positionType)
        e.add_param('boardMessageID', boardMessageID)
        e.add_param('number', number)
        e.add_param('rng', rng)
        e.add_param('minRng', minRng)
        e.add_param('exceptHighestHate', exceptHighestHate)
        return e

    def buildMoveDungeonEntityToFixedPos(self, eventId, entityGID, pos_, speed, moveAni):
        e = self.build_element(DungeonMoveEntityToFixPosEvent, element_id=eventId,
                               event_handler=handleDungeonMoveEntityToFixedPos,
                               entityGID=entityGID, pos_=pos_, speed=speed, moveAni=moveAni,
                               name=gameconst.DungeonFlowEventName.moveEntityToFixedPosition,)
        return e

    def buildCreateAvatarMirrorFromRandomPlayer(self, eventId, entityGID, ratio):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleCreateAvatarMirrorFromRandomPlayer,
                               name=gameconst.DungeonFlowEventName.createAvatarMirrorFromRandomPlayer)
        e.add_param('entityGID', entityGID)
        e.add_param('ratio', ratio)
        return e

    def buildDungeonRemoveCreation(self, eventId, monsterGID, creationID, rng):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRemoveCreation,
                               name=gameconst.DungeonFlowEventName.removeCreation)
        e.add_param('monsterGID', monsterGID)
        e.add_param('creationID', creationID)
        e.add_param('rng', rng)
        return e

    def buildDungeonHaveCreationInRange(self, eventId, monsterGID, creationID, rng):
        e = self.build_element(ep_ctrl.flow.Branch, element_id=eventId,
                               event_handler=ep_ctrl.utils.BASE_EVENT_TRIGGER_FUNC,
                               name=gameconst.DungeonFlowEventName.haveCreationInRange)
        e.add_param('__CONDITION__', conditionDungeonHaveCreationInRange(self, monsterGID, creationID, rng))
        e.bind_condition(e, '__CONDITION__')
        return e

    def buildSetDungeonStage(self, eventId, dungeonStageID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleSetDungeonStage,
                               name=gameconst.DungeonFlowEventName.dunStageSet)
        e.add_param('dungeonStageID', dungeonStageID)
        return e

    def buildShowPopoverMsg(self, eventId, entityID, messageID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleShowPopOverMsg,
                               name=gameconst.DungeonFlowEventName.showPopoverMsg)
        e.add_param('entityGID', entityID)
        e.add_param('messageID', messageID)
        return e

    def buildPopDialog(self, eventId, entityID, dialogID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handlePopDialog,
                               name=gameconst.DungeonFlowEventName.showPopoverMsg)
        e.add_param('entityGID', entityID)
        e.add_param('dialogID', dialogID)
        return e

    def buildDungeonTaskForceComplete(self, eventId, taskID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonTaskForceComplete,
                               name=gameconst.DungeonFlowEventName.dungeonTaskForceComplete)
        e.add_param('taskID', taskID)
        return e

    def buildDungeonTaskForceFailed(self, eventId, taskID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonTaskForceFailed,
                               name=gameconst.DungeonFlowEventName.dungeonTaskForceFailed)
        e.add_param('taskID', taskID)
        return e

    def buildChangeDunNPCToBattle(self, eventId, npcIDs, ifSetBoss):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeDungeonNPCToBattle,
                               name=gameconst.DungeonFlowEventName.changeDunNPCToBattle)
        e.add_param('npcIDs', npcIDs)
        e.add_param('ifSetBoss', ifSetBoss)
        return e

    def buildChangeDunNPCToNeutral(self, eventId, npcIDs, resetDir):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeDungeonNPCToNeutral,
                               name=gameconst.DungeonFlowEventName.changeDunNPCToNeutral)
        e.add_param('npcIDs', npcIDs)
        e.add_param('resetDir', resetDir)
        return e

    def buildChangeDunNPCToFriendly(self, eventId, npcIDs, resetDir):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeDungeonNPCToFriendly,
                               name=gameconst.DungeonFlowEventName.changeDunNPCToFriendly)
        e.add_param('npcIDs', npcIDs)
        e.add_param('resetDir', resetDir)
        return e

    def buildChangeDunNPCDialog(self, eventId, npcID, dialogID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeDungeonNPCDialog,
                               name=gameconst.DungeonFlowEventName.changeDunNPCDialog)
        e.add_param('npcID', npcID)
        e.add_param('dialogID', dialogID)
        return e

    def buildDungeonAnyPlayerHpEvent(self, eventId, symbol, hp, checkNow, checkOnce):
        e = self.build_element(DungeonAnyPlayerHPMonitorTriggerEvent, element_id=eventId,
                               event_handler=handleDungeonAnyPlayerHpTrigger,
                               symbol=symbol, hpPercent=hp,
                               checkNow=checkNow, checkOnce=checkOnce,
                               name=gameconst.DungeonFlowEventName.dunAnyPlayerHP)
        return e

    def buildAddEntityArrowTracker(self, eventId, entityGID, priority, triggerType):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleAddEntityArrowTracker,
                               name=gameconst.DungeonFlowEventName.addEntityArrowTracker)
        e.add_param('entityGID', entityGID)
        e.add_param('priority', priority)
        e.add_param('triggerType', triggerType)
        return e

    def buildRemoveEntityArrowTracker(self, eventId, entityGID, triggerType):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRemoveEntityArrowTracker,
                               name=gameconst.DungeonFlowEventName.removeEntityArrowTracker)
        e.add_param('entityGID', entityGID)
        e.add_param('triggerType', triggerType)
        return e

    def buildClearEntityHate(self, eventId, entityGIDs):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleClearEntityHate,
                               name=gameconst.DungeonFlowEventName.clearEntityHate)
        e.add_param('entityGIDs', entityGIDs)
        return e

    def buildForceSelectEntityTarget(self, eventId, entityGIDs, positionType, rng, minRng,
                                     exceptHighestHate):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleForceSelectEntityTarget,
                               name=gameconst.DungeonFlowEventName.forceSelectEntityTarget)
        e.add_param('entityGIDs', entityGIDs)
        e.add_param('positionType', positionType)
        e.add_param('rng', rng)
        e.add_param('minRng', minRng)
        e.add_param('exceptHighestHate', exceptHighestHate)
        return e

    def buildRandomTrigger(self, eventId, randomArray):
        # 【【功能点】副本编辑器概率随机触发事件修改】
        # FIXME(): 这类概率问题可以考虑使用decimal重构，不然损失精度问题无法避免
        _prec = 2
        _totalWeight = sum(randomArray)
        probabilities = [(idx, p * 1/_totalWeight) for idx, p in enumerate(randomArray, 1)]
        e = self.build_element(FlowRandomEvent, element_id=eventId,
                               probability=probabilities, prec=_prec,
                               name=gameconst.DungeonFlowEventName.randomTrigger)
        return e

    def buildDungeonTrapBeTriggered(self, eventId, entityGID, checkNow, checkOnce):
        e = self.build_element(DungeonTrapBeTriggered, element_id=eventId,
                               entityGID=entityGID, checkNow=checkNow, checkOnce=checkOnce,
                               event_handler=handleDungeonTrapBeTriggered,
                               name=gameconst.DungeonFlowEventName.trapBeTriggered)
        return e

    def buildDungeonTeleportToPosition(self, eventId, entityGIDs, pos, dir_):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonTeleportToPosition,
                               name=gameconst.DungeonFlowEventName.teleportToPosition)
        e.add_param('entityGIDs', entityGIDs)
        e.add_param('pos', pos)
        e.add_param('dir_', dir_)
        return e

    def buildDungeonChangeEntityForce(self, eventId, entityGIDs, force):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonChangeEntityForce,
                               name=gameconst.DungeonFlowEventName.changeEntityForce)
        e.add_param('entityGIDs', entityGIDs)
        e.add_param('force', force)
        return e

    def buildIntegrationEvent(self, eventId):
        return self.build_element(FlowEvent, element_id=eventId,
                                  name=gameconst.DungeonFlowEventName.integrationEvent)

    def buildChangeSpaceVar(self, eventId, varID, formula, paramVarIDs):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeSpaceVar,
                               name=gameconst.DungeonFlowEventName.changeSpaceVar)
        e.add_param('varID', varID)
        e.add_param('formula', formula)
        e.add_param('paramVarIDs', paramVarIDs)
        return e

    def buildDungeonKillEntities(self, eventId, entityGIDs):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonKillEntities,
                               name=gameconst.DungeonFlowEventName.killEntities)
        e.add_param("entityGIDs", entityGIDs)
        return e

    def buildDungeonEntityImmuneDeath(self, eventId, entityGID):
        e = self.build_element(DungeonEntityImmuneDeath, element_id=eventId,
                               entityGID=entityGID,
                               event_handler=handleDungeonEntityImmuneDeath,
                               name=gameconst.DungeonFlowEventName.dungeonEntityImmuneDeath)
        return e

    def buildIfAllSelectEntityImmuneDeath(self, eventId, entityGIDs):
        e = self.build_element(AllDungeonSelectedEntitiesImmuneDeath, element_id=eventId,
                               event_handler=handleIfAllSelectEntityImmuneDeath,
                               name=gameconst.DungeonFlowEventName.ifAllSelectEntityImmuneDeath)
        e.add_param("entityGIDs", entityGIDs)
        return e

    def buildCreateDungeonTeleporter(self, eventId, entityGID, targetEntityGID, trapRange):
        e = self.build_element(DungeonTeleporterReleaseEvent, element_id=eventId,
                               entityGID=entityGID, targetEntityGID=targetEntityGID,
                               event_handler=handleCreateDugneonTeleporter,
                               name=gameconst.DungeonFlowEventName.createDungeonTeleporter)
        e.add_param('trapRange', trapRange)
        return e

    def buildStopAiTick(self, eventId, entityGIDs):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleStopAiTick,
                               name=gameconst.DungeonFlowEventName.stopAiTick)
        e.add_param("entityGIDs", entityGIDs)
        return e

    def buildStartAiTick(self, eventId, entityGIDs):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleStartAiTick,
                               name=gameconst.DungeonFlowEventName.startAiTick)
        e.add_param("entityGIDs", entityGIDs)
        return e

    def buildEntityStartRouting(self, eventId, entityGID, pathID, speed, moveAni, escortDistance):
        """副本实体延路点寻路"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleEntityStartRouting,
                               name=gameconst.DungeonFlowEventName.entityStartRouting)
        e.add_param('entityGID', entityGID)
        e.add_param('pathID', pathID)
        e.add_param('speed', speed)
        e.add_param('moveAni', moveAni)
        e.add_param('escortDistance', escortDistance)
        return e

    def buildEntityRouteFinished(self, eventId, entityGID, pathID):
        """副本实体路点寻路完成事件"""
        e = self.build_element(EntityRouteFinishedEvent, element_id=eventId,
                               entityGID=entityGID, pathID=pathID,
                               event_handler=handleEntityRouteFinished,
                               name=gameconst.DungeonFlowEventName.entityStartRouting)
        return e

    def buildEntityRoutingMissingEscort(self, eventId, entityGID, pathID, infLoop):
        """副本实体路点寻路距离玩家过远事件"""
        e = self.build_element(EntityRoutingMissingEscortEvent, element_id=eventId,
                               entityGID=entityGID, pathID=pathID,
                               event_handler=handleEntityRoutingMissingEscort,
                               name=gameconst.DungeonFlowEventName.entityStartRouting)
        e.add_param("infLoop", infLoop)
        return e

    def buildAnyPlayerCinemaPlayEnded(self, eventId, cinemaPlayID, delay):
        """副本内任一玩家动画播放结束触发事件"""
        e = self.build_element(AnyPlayerCinemaPlayEndedEvent, element_id=eventId,
                               cinemaPlayID=cinemaPlayID, delay=delay,
                               event_handler=handleAnyPlayerCinemaPlayEnded,
                               name=gameconst.DungeonFlowEventName.anyPlayerCinemaPlayEnded)
        return e

    def buildCastCinemaPlay(self, eventId, cinemaPlayID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleCastCinemaPlay,
                               name=gameconst.DungeonFlowEventName.castCinemaPlay)
        e.add_param("cinemaPlayID", cinemaPlayID)
        return e

    def buildDungeonStopCurTrans(self, eventId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonStopCurTrans,
                               name=gameconst.DungeonFlowEventName.stopCurTrans)
        return e

    def buildDungeonTriggerGuide(self, eventId, triggerGuideId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonTriggerGuide,
                               name=gameconst.DungeonFlowEventName.triggerGuide)
        e.add_param('triggerGuideId', triggerGuideId)
        return e

    def buildNewTransPetStart(self, eventId, transPetId, triggerGuideId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleNewTransPetStart,
                               name=gameconst.DungeonFlowEventName.newTransPetStart)
        e.add_param('transPetId', transPetId)
        e.add_param('triggerGuideId', triggerGuideId)
        return e

    def buildNewTransPetEnd(self, eventId, transPetId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleNewTransPetEnd,
                               name=gameconst.DungeonFlowEventName.newTransPetEnd)
        e.add_param('transPetId', transPetId)
        return e

    def buildChangeAllPlayerCameraStatus(self, eventId, cameraId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeAllPlayerCameraStatus,
                               name=gameconst.DungeonFlowEventName.changeAllPlayerCameraStatus)
        e.add_param('cameraId', cameraId)
        return e

    def buildChangeAllPlayerCameraLookPos(self, eventId, entityGID):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeAllPlayerCameraLookPos,
                               name=gameconst.DungeonFlowEventName.changeAllPlayerCameraLookPos)
        e.add_param('entityGID', entityGID)
        return e

    def buildRevertAllPlayerCameraStatus(self, eventId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRevertAllPlayerCameraStatus,
                                 name=gameconst.DungeonFlowEventName.revertAllPlayerCameraStatus)
        return e

    def buildDungeonPlayerForceTrans(self, eventId, transPetId, chooseType):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleDungeonPlayerForceTrans,
                               name=gameconst.DungeonFlowEventName.playerForceTrans)
        e.add_param('transPetId', transPetId)
        e.add_param('chooseType', chooseType)
        return e

    def buildChangeNPCSelectableStatus(self, eventId, entityGIDs, isSelectable):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeNPCSelectableStatus,
                               name=gameconst.DungeonFlowEventName.changeNPCSelectableStatus)
        e.add_param('entityGIDs', entityGIDs)
        e.add_param('isSelectable', isSelectable)
        return e

    def buildWaitingTaskInProgress(self, eventId, taskId):
        e = self.build_element(WaitingTaskInProgressEvent, element_id=eventId,
                               event_handler=handleWaitingTaskInProgressEvent,
                               task_id=taskId, checknow=True, checkOnce=True,
                               name=gameconst.DungeonFlowEventName.taskFailed)
        return e

    def buildChangeEntityDirection(self, eventId, entityGIDs, dir_):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleChangeEntityDirection,
                               name=gameconst.DungeonFlowEventName.changeEntityDirection)
        e.add_param('entityGIDs', entityGIDs)
        e.add_param('dir_', dir_)
        return e

    def buildTimeFreezeStart(self, eventId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleTimeFreezeStart,
                               name=gameconst.DungeonFlowEventName.timeFreezeStart)
        return e

    def buildTimeFreezeEnd(self, eventId):
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleTimeFreezeEnd,
                               name=gameconst.DungeonFlowEventName.timeFreezeEnd)
        return e

    def buildReleaseDungeonRebornPosEvent(self, eventId, rebornPosGIDs, rebornPosNum):
        """释放复活点事件"""
        e = self.build_element(DungeonRebornPosReleaseEvent, element_id=eventId,
                               rebornPosGIDs=rebornPosGIDs, event_handler=handleReleaseRebornPos,
                               name=gameconst.DungeonFlowEventName.createRebornPos)
        e.add_param('rebornPosNum', rebornPosNum)
        return e

    def buildRecycleDungeonRebornPosEvent(self, eventId, rebornPosGIDs):
        """回收复活点事件"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleRecycleRebornPos,
                               name=gameconst.DungeonFlowEventName.removeRebornPos)
        e.add_param('rebornPosGIDs', rebornPosGIDs)
        return e

    def buildTransferToTheDesignatedMap(self, eventId, lineNo, pos, angle):
        """传送到大世界目标点"""
        e = self.build_element(
            FlowEvent,
            element_id=eventId,
            event_handler=handleTransferToTheDesignatedMap,
            name=gameconst.DungeonFlowEventName.transferToTheDesignatedMap,
        )
        e.add_param('lineNo', lineNo)
        e.add_param('pos', pos)
        e.add_param('angle', angle)
        return e

    def buildNotifyStartBattleCD(self, eventId, dungeonNo, spaceNo, cdTime):
        """开始战斗前cd"""
        e = self.build_element(
            FlowEvent,
            element_id=eventId,
            event_handler=handleNotifyStartBattleCD,
            name=gameconst.DungeonFlowEventName.notifyStartBattleCD,
        )
        e.add_param('dungeonNo', dungeonNo)
        e.add_param('spaceNo', spaceNo)
        e.add_param('cdTime', cdTime)
        return e
    
    def buildCreateBreakAwayStuckPosEvent(self, eventId, entityId, entityNum):
        """脱离卡死点"""
        e = self.build_element(FlowEvent, element_id=eventId,
                               event_handler=handleCreateBreakAwayStuckPos,
                               name=gameconst.DungeonFlowEventName.createBreakAwayStuckPos)
        e.add_param('entityId', entityId)
        e.add_param('entityNum', entityNum)
        return e

def _createNoHostCreation(spaceID, target, context, *args, spaceMgrId=0, spaceNo=0, extraProps=None):
    ttl, cnt, dirOffset, posOffset = 0, 0, None, None
    creationLv, skillLv = 1, 0

    argsCnt = len(args)
    if argsCnt == 1:
        creationId, = args
    elif argsCnt == 2:
        creationId, creationLv = args
    elif argsCnt ==3:
        creationId, creationLv, skillLv = args
    elif argsCnt == 4:
        creationId, creationLv, skillLv, ttl = args
    elif argsCnt == 5:
        creationId, creationLv, skillLv, ttl, cnt = args
    elif argsCnt == 6:
        creationId, creationLv, skillLv, ttl, cnt, dirOffset = args
    elif argsCnt == 7:
        creationId, creationLv, skillLv, ttl, cnt, dirOffset, posOffset = args
    else:
        raise Exception('create no host Creation args error: %s' % args)

    props = {'creationId': creationId,
             'level': creationLv,
             'spaceNo': spaceNo,
             'ttl': float(ttl),
             'targetId': 0}
    if target:
        props['selectedTargetId'] = target.id

    createRadius, createCount = 0, 0
    if context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED:
        fixedPos = context.position
        fixedDir = Math.Vector3(0.0, 0.0, context.direction*math.pi/180)
        fixedDir.normalise()
        createRadius = context.radius
        createCount = context.number
        # 【【任务】指定位置召唤创生物、怪物（召唤物）】
        rawGameEntityId = context.rawGameEntityId
    else:
        ERROR_MSG('createNoHostCreation:: create no host creation must set context', context)
        return

    direction = (0.0, 0.0, sMath.getYawFromDirection(fixedDir))
    position = fixedPos

    if fixedDir and posOffset:
        position = sMath.posByOffset(position, fixedDir*posOffset)

    # 【【任务】回收创生物-服务端】
    props.update({'fbEntityId': rawGameEntityId})
    spaceMgrId and props.update({'spaceMgrId': spaceMgrId})

    extraProps and props.update(extraProps)

    creations = []
    gameEntityIdGen = utils.generateGameEntityId(rawGameEntityId, createCount)
    for i in range(createCount):
        if rawGameEntityId:
            # 【【任务】指定位置召唤创生物、怪物（召唤物）】
            props = props.copy()
            props['gameEntityId'] = next(gameEntityIdGen, 0)
        props.setdefault('tmpProps', {}).update(
            {'createRadius': createRadius, 'createCount': createCount,
             'createIndex': i+1})
        creation = KBEngine.createEntity('Creation', spaceID, position, tuple(direction), props)
        DEBUG_MSG('create creation', creation.creationId, position, creation.direction)

        if not creation:
            ERROR_MSG('create Error', creationId, position, spaceID)
            continue

        creations.append(creation)

        if skillLv:
            creation.setAllSkillLv(skillLv)

    return creations


def _handlePlayerChooseType(positionType, spaceMgr, monsterEntity=None,
                            range_=0, range_min_=0, number=1, exceptHighestHate=0,
                            **kwargs):
    """ 根据playerChooseType选择相应的实体对象

    # range/range_min参数
    # 【【任务】目标选择扩展：设置目标距离范围-后端】

    :param positionType: 在 gameconst.DungeonFlowPlayerChooseType 中定义
    :param spaceMgr: 当前spaceMgr
    :param monsterEntity: (可选参数) 怪物当前entity
    :param range_: (可选参数) 选取范围最大值
    :param range_min_: (可选参数) 选取范围最小值
    :param number:  (可选参数) 选取数量
    :param exceptHighestHate: (可选参数) 排除仇恨列表前N个目标
    :param kwargs: 兼容参数
    :return:
    """
    _ents = []

    def _handleEnts(_l_eids):
        nonlocal _ents

        _l_entDic = {}
        for _l_eid in _l_eids:
            _l_ent = KBEngine.entities.get(_l_eid)
            _l_realEnt = utils.getEntityRealEntity(_l_ent) if _l_ent else None
            if _l_realEnt and _l_realEnt.id not in _l_entDic:
                _l_entDic[_l_realEnt.id] = _l_realEnt

        _ents.extend(_l_entDic.values())

    if number < 0:
        return False, '_handlePlayerChooseType::number must ge than 0, got {}'.format(number), _ents

    if positionType == gameconst.DungeonFlowPlayerChooseType.RAND_IN_ALL_PLAYERS:
        allAlivePlayers = list(i for i in (KBEngine.entities.get(i) for i in spaceMgr.players) if i and not i.isDie())
        if not allAlivePlayers:
            return False, '_handlePlayerChooseType::RAND_IN_ALL_PLAYERS: no alive player in spaceMgr', _ents
        for _ent in random.sample(allAlivePlayers, number) if len(allAlivePlayers) >= number else allAlivePlayers:
            _ent and _ents.append(_ent)

    elif monsterEntity and positionType == gameconst.DungeonFlowPlayerChooseType.MONSTER_CURRENT_TARGET:
        _ent = KBEngine.entities.get(monsterEntity.selectedTargetId)
        _ent and _ents.append(utils.getEntityRealEntity(_ent))

    elif monsterEntity and monsterEntity.aiController \
            and positionType == gameconst.DungeonFlowPlayerChooseType.RAND_IN_MONSTER_HATRED_LIST:
        _eids = monsterEntity.aiController.hateDict.getRandomHatredTargetIds(
            number=number, minRange=range_min_, maxRange=range_)
        _handleEnts(_eids)

    elif monsterEntity and monsterEntity.aiController \
            and positionType == gameconst.DungeonFlowPlayerChooseType.RAND_IN_MONSTER_HATRED_LIST_EXCEPT_HIGHEST:
        _eids = monsterEntity.aiController.hateDict.getRandomHatredTargetIds(
            exceptHighest=exceptHighestHate, number=number, minRange=range_min_, maxRange=range_)
        _handleEnts(_eids)
    elif monsterEntity and monsterEntity.aiController and \
            positionType == gameconst.DungeonFlowPlayerChooseType.MONSTER_HATRED_LIST_MONSTER:
        _eids = monsterEntity.aiController.hateDict.getMaxHaterdMonsterTarget()
        _handleEnts(_eids)
    else:
        return False, '_handlePlayerChooseType::posType not allowed', _ents

    if not _ents:
        return False, '_handlePlayerChooseType::player not found', _ents

    return True, 'OK', _ents


def handleStopDelayEvent(e, src_e, ctx, **ref_params):
    eventIDs = e.get_param('eventIDs', [])
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: stop delayEvent -> {}'.format(e.id, eventIDs))
    for eid in eventIDs:
        se = e.controller._elements.get(eid, None)
        if not se:
            continue

        def _cancel(_e):
            if callable(getattr(_e, 'cancel', None)):
                DEBUG_MSG('DUNGEON FLOW -- EVENT: stop delayEvent Cancel {} {}'.format(_e.id, _e.name))
                _e.cancel(ctx)

        _cancel(se)
        if hasattr(se, 'eGroup'):
            for sge in se.eGroup:
                _cancel(sge)


def handleStartDungeon(e, src_e, ctx, **ref_params):
    dungeonNo = e.get_param('dungeonNo')
    spaceNo = e.get_param('spaceNo')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: start dungeon -> {} {}'.format(e.id, dungeonNo, spaceNo))
    dungeonSpaceType = DDI.datas[dungeonNo].get('type', 0)
    if gameconst.DungeonType.isDungeon(dungeonSpaceType):
        tCreate = utils.getNow()
        spaceMgr = e.controller.owner
        spaceMgr.dungeonPlayMode.tCreate = tCreate
        dunStubBox = gameengine.getDungeonStubBySpaceNo(spaceNo)
        dunStubBox.onDungeonStarted(spaceNo, tCreate)
    else:
        ERROR_MSG('flowController::handleStartDungeon: err', dungeonNo, dungeonSpaceType)
        return


def handleEndDungeon(e, src_e, ctx, **ref_params):
    dungeonNo = e.get_param('dungeonNo')
    spaceNo = e.get_param('spaceNo')
    delayTime = int(e.get_param('delayTime', 0))
    isFail = e.get_param('isFail', True)

    spaceMgr = e.controller.owner
    if not spaceMgr:
        ERROR_MSG('handleEndDungeon:: spaceMgr not found')
        return

    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: end dungeon -> {} {}'.format(e.id, dungeonNo, spaceNo))
    dunStubBox = gameengine.getDungeonStubBySpaceNo(spaceNo)
    e.controller.stop_all()
    if formula.isSingleDungeonSpace(spaceNo):
        dunStubBox.completeSingleDungeon(spaceNo, spaceMgr.singleDungeonBelongPlayerGBID, not isFail, delayTime)
    elif formula.isTeamDungeonSpace(spaceNo):
        dunStubBox.completeTeamDungeon(spaceNo, spaceMgr.teamDungeonBelongTeamUUID, not isFail, delayTime, gameconst.DunegonCompleteReasonType.FINISHED)
    elif formula.isRaidDungeonSpace(spaceNo):
        dunStubBox.completeRaidDungeon(spaceNo, spaceMgr.raidDungeonBelongRaidUUID, not isFail, delayTime, gameconst.DunegonCompleteReasonType.FINISHED)
    elif formula.isGuildBossDungeonSpace(spaceNo):
        dunStubBox.completeGuildBossDungeon(spaceNo, spaceMgr.guildBossDungeonBelongGuildUUID, not isFail, delayTime, gameconst.DunegonCompleteReasonType.FINISHED)
    else:
        ERROR_MSG('flowController::handleEndDungeon:', dungeonNo, spaceNo)
        return

    for pid in e.controller.owner.players:
        pEnt = KBEngine.entities.get(pid)
        pEnt and pEnt.client.changeDungeonRemainTime(spaceNo, int(utils.getNow() + delayTime))


def handleDelayEndDungeon(e, src_e, ctx, **ref_params):
    dungeonNo = e.get_param('dungeonNo')
    spaceNo = e.get_param('spaceNo')
    delayTime = int(e.get_param('delayTime', 0))
    preDelayTime = int(e.get_param('preDelayTime', 0))
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}]: end dungeon delay -> {} {} {}--{}".format(
        e.id, dungeonNo, spaceNo, delayTime, preDelayTime))


def _handleRecycleInDungeon(e, entityGIDs):
    spaceMgr = e.controller.owner
    if not spaceMgr:
        ERROR_MSG('_handleRecycleInDungeon:: spaceMgr not found')
        return

    for gid in entityGIDs:
        tag = 'gid_{}'.format(gid)
        for ent in spaceMgr.getEntitiesByTag(tag):
            if ent.IsCombatUnit:
                ent.destroyAllSummon()
                ent.destoryAllCreation()
            ent.delaySafeDestroy(round(random.uniform(0.1, 0.3), 1))
        # spaceMgr.removeEntitiesByTag(tag)


def _handleMonsterChangeInitState(e, entityGIDs, bornState):
    spaceMgr = e.controller.owner
    if not spaceMgr:
        ERROR_MSG('_handleRecycleInDungeon:: spaceMgr not found')
        return

    for gid in entityGIDs:
        tag = 'gid_{}'.format(gid)
        for ent in spaceMgr.getEntitiesByTag(tag):
            if ent.IsCombatUnit:
                ent.changeBornStateByFlow(bornState)


def _handleMonsterAddHateValue(e, monsterGIDs, chooseType, hateValue):
    spaceMgr = e.controller.owner
    if not spaceMgr:
        ERROR_MSG('_handleRecycleInDungeon:: spaceMgr not found')
        return

    pIds = [pid for pid in spaceMgr.players if pid in KBEngine.entities]

    def _addHateAll(monster, pids):
        if not monster.aiController:
            return

        aiController = monster.aiController
        for pid in pids:
            aiController.increaseHate(pid, hateValue)

    def _addRandHate(monster, pids):
        if not monster.aiController:
            return

        monster.aiController.increaseHate(random.choice(pids), hateValue)

    if chooseType == gameconst.FlowAddHateType.all:
        _func = _addHateAll
    elif chooseType == gameconst.FlowAddHateType.rand:
        _func = _addRandHate
    else:
        ERROR_MSG('_handleMonsterAddHateValue but type invalid:', chooseType, hateValue)
        return

    for gid in monsterGIDs:
        tag = 'gid_{}'.format(gid)
        for ent in spaceMgr.getEntitiesByTag(tag):
            if ent.IsCombatUnit:
                _func(ent, pIds)


def _handleRecycleByPrototypeIdInDungeon(e, entityIDs):
    spaceMgr = e.controller.owner
    if not spaceMgr:
        ERROR_MSG('_handleRecycleByPrototypeIdInDungeon:: spaceMgr not found')
        return

    for cpid in entityIDs:
        tag = str(cpid)
        for ent in spaceMgr.getEntitiesByTag(tag):
            ent.delaySafeDestroy(round(random.uniform(0.1, 0.3), 1))
        # spaceMgr.removeEntitiesByTag(tag)


def handleReleaseMonster(e, src_e, ctx, **ref_params):
    monsterGIDs = e.get_param('monsterGIDs')
    monsterNum = e.get_param('monsterNum')
    overwriteProps = e.get_param('overwriteProps')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: release monster -> {}:{}(op={})'.format(
        e.id, monsterGIDs, monsterNum, overwriteProps))


def handleRecycleMonster(e, src_e, ctx, **ref_params):
    monsterGIDs = e.get_param('monsterGIDs')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: recycle monster -> {}'.format(e.id, monsterGIDs))
    _handleRecycleInDungeon(e, monsterGIDs)


def handleDungeonRemoveNoHostCreation(e, src_e, ctx, **ref_params):
    creationGIDs = e.get_param('creationGIDs')
    userPrototypeID = e.get_param('userPrototypeID', True)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: recycle not host creation -> {}(userPrototypeID={})'.format(
        e.id, creationGIDs, userPrototypeID))
    if not userPrototypeID:
        _handleRecycleInDungeon(e, creationGIDs)
    else:
        _handleRecycleByPrototypeIdInDungeon(e, creationGIDs)


def handleMonsterChangeInitState(e, src_e, ctx, **ref_params):
    monsterGIDs = e.get_param('monsterGIDs')
    bornState = e.get_param('initState')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: monster change stone state -> {}:{}'.format(e.id, monsterGIDs, bornState))
    _handleMonsterChangeInitState(e, monsterGIDs, bornState)


def handleMonsterAddHateValue(e, src_e, ctx,  **ref_params):
    monsterGIDs = e.get_param('monsterGIDs')
    chooseType = e.get_param('chooseType')
    hateValue = e.get_param('hateValue')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: monster add hate state -> {}:{}:{}'.format(e.id, monsterGIDs, chooseType,
                                                                                       hateValue))
    _handleMonsterAddHateValue(e, monsterGIDs, chooseType, hateValue)


def handleReleaseNPC(e, src_e, ctx, **ref_params):
    npcGIDs = e.get_param('npcGIDs')
    npcNum = e.get_param('npcNum')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: release npc -> {}:{}'.format(e.id, npcGIDs, npcNum))


def handleRecycleNPC(e, src_e, ctx, **ref_params):
    npcGIDs = e.get_param('npcGIDs')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: recycle npc -> {}'.format(e.id, npcGIDs))
    _handleRecycleInDungeon(e, npcGIDs)


def handleReleaseCollection(e, src_e, ctx, **ref_params):
    collGIDs = e.get_param('collGIDs')
    collNum = e.get_param('collNum')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: release collection -> {}:{}'.format(e.id, collGIDs, collNum))


def handleCollBeCollected(e, src_e, ctx, **ref_params):
    collGIDs = e.get_param('collGIDs')
    usePrototypeID = e.get_param('usePrototypeID', False)
    infLoop = e.get_param('infLoop', False)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: collection be collected -> {}(usePrototypeID={},inf={})'.format(
        e.id, collGIDs, usePrototypeID, infLoop))


def handleMultiCollAllBeCollected(e, src_e, ctx, **ref_params):
    collGIDs = e.get_param('collGIDs')
    infLoop = e.get_param('infLoop', False)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: multi collection all be collected -> {}(inf={})'.format(
        e.id, collGIDs, infLoop))


def handleRecycleCollection(e, src_e, ctx, **ref_params):
    collGIDs = e.get_param('collGIDs')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: recycle collection -> {}'.format(e.id, collGIDs))
    _handleRecycleInDungeon(e, collGIDs)


def handleReleaseBuffPoint(e, src_e, ctx, **ref_params):
    buffPointGIDs = e.get_param('buffPointGIDs')
    buffPointNum = e.get_param('buffPointNum')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: release buff point -> {}:{}'.format(
        e.id, buffPointGIDs, buffPointNum))


def handleRecycleBuffPoint(e, src_e, ctx, **ref_params):
    buffPointGIDs = e.get_param('buffPointGIDs')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: recycle buff point -> {}'.format(e.id, buffPointGIDs))
    _handleRecycleInDungeon(e, buffPointGIDs)


def handleReleaseAirWall(e, src_e, ctx, **ref_params):
    airWallGIDs = e.get_param('airWallGIDs')
    airWallNum = e.get_param('airWallNum')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: release air wall -> {}:{}'.format(
        e.id, airWallGIDs, airWallNum))


def handleRecycleAirWall(e, src_e, ctx, **ref_params):
    airWallGIDs = e.get_param('airWallGIDs')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: recycle air wall -> {}'.format(e.id, airWallGIDs))
    _handleRecycleInDungeon(e, airWallGIDs)


def handleMonsterHpEvent(e, src_e, ctx, **ref_params):
    monsterGID = e.get_param('monsterGID')
    symbol = e.get_param('symbol')
    hpPrt = e.get_param('hpPercent')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after monster HP condition -> {}: {} {}'.format(
        e.id, monsterGID, symbol, hpPrt))


def handleMonsterRestNumEvent(e, src_e, ctx, **ref_params):
    monsterGID = e.get_param('monsterGID')
    symbol = e.get_param('symbol')
    number = e.get_param('restNum')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after monster RestNum condition -> {}: {} {}'.format(
        e.id, monsterGID, symbol, number))


def handleDungeonMonsterKillNumEvent(e, src_e, ctx, **ref_params):
    monsterGID = e.get_param('monsterGID')
    symbol = e.get_param('symbol')
    number = e.get_param('killNum')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after dungeon monster killNum condition -> {}: {} {}'.format(
        e.id, monsterGID, symbol, number))


def handleDungeonAlivePlayerEvent(e, src_e, ctx, **ref_params):
    symbol = e.get_param('symbol')
    number = e.get_param('playerNum')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after dungeon player alive number --> {} {}'.format(
        e.id, symbol, number))


def handlePlayerRestNumEvent(e, src_e, ctx, **ref_params):
    symbol = e.get_param('symbol')
    number = e.get_param('playerNum')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after player RestNum condition -> {}: {}'.format(
        e.id, symbol, number))


def handleTaskUndertake(e, src_e, ctx, **ref_params):
    taskId = e.get_param('taskID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after task undertake -> {}'.format(e.id, taskId))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        return

    spaceMgr.syncPlayer(lambda boxCell: boxCell.startClaimTask(taskId))


def handleWaitingTaskCompleteEvent(e, src_e, ctx, **ref_params):
    taskId = e.get_param('taskId', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after waiting task complete -> {}'.format(e.id, taskId))


def handleWaitingTaskFailedEvent(e, src_e, ctx, **ref_params):
    taskId = e.get_param('taskId', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after waiting task failed -X {}'.format(e.id, taskId))


def handleWaitingTaskInProgressEvent(e, src_e, ctx, **ref_params):
    taskId = e.get_param('taskId', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after waiting task inprogress -X {}'.format(e.id, taskId))


def handleDungeonMonsterCastSkill(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    skillID = e.get_param('skillID', 0)
    skillLevel = e.get_param('skillLevel', 1)
    forceToUse = e.get_param('forceToUse', False)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: monster cast skill -> {}: {}(lvl={},force={})'.format(
        e.id, monsterGID, skillID, skillLevel, forceToUse))

    if skillID not in SSD.datas:
        ERROR_MSG("handleDungeonMonsterCastSkill:: skillid invalid", e.id, skillID)
        return

    skillCategory = SSD.datas[skillID]['category']

    gidTag = 'gid_{}'.format(monsterGID)
    ents = e.controller.owner.getEntitiesByTag(gidTag)
    for ent in ents:
        if skillCategory == gameconst.SkillCategory.CAST_SKILL_WITHOUT_ACTION:
            context = actionContext.FlowControllerCtx()
            ent.castSkill(0, context, skillID, skillLevel)
        else:
            aiCtrl = ent.aiController
            aiCtrl and aiCtrl.regrTempSkillId(skillID, skillLevel, forceUse=forceToUse, interruptCrt=forceToUse)


def handleDungeonMonsterCastSkillToPlayer(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    skillID = e.get_param('skillID', 0)
    positionType = e.get_param('positionType', gameconst.DungeonFlowPlayerChooseType.UNKNOWN)
    boardMessageID = e.get_param('boardMessageID', 0)
    number = e.get_param('number', 1)
    minRng = e.get_param('minRng', 0)
    rng = e.get_param('rng', 0)
    exceptHighestHate = e.get_param('exceptHighestHate', 1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{0}]: monster cast skill to player -> '
                '{1}: {2}(type={3},msg={4},num={5},rng={6},minrng={7},exceptHighestHate={8})'.format(
                    e.id, monsterGID, skillID, positionType, boardMessageID, number, rng, minRng, exceptHighestHate))

    if skillID not in SSD.datas:
        ERROR_MSG("handleDungeonMonsterCastSkillToPlayer:: skillid invalid", e.id, monsterGID, skillID)
        return

    skillCategory = SSD.datas[skillID]['category']

    spaceMgr = e.controller.owner
    gidTag = 'gid_{}'.format(monsterGID)
    ents = spaceMgr.getEntitiesByTag(gidTag)

    _players = []
    if boardMessageID:
        for pid in e.controller.owner.players:
            ent = KBEngine.entities.get(pid)
            ent and _players.append(ent)

    for ent in ents:
        _params = dict(monsterEntity=ent, number=number, exceptHighestHate=exceptHighestHate)
        minRng and _params.update({'range_min_': minRng})
        rng and _params.update({'range_': rng})
        r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
        if not r:
            WARNING_MSG('FlowController::handleDungeonMonsterCastSkillToPlayer: ', rs, positionType)
            continue
        aiCtrl = ent.aiController
        for tEnt_ in tEnts_:
            if skillCategory == gameconst.SkillCategory.CAST_SKILL_WITHOUT_ACTION:
                context = actionContext.FlowControllerCtx()
                ent.castSkill(tEnt_, context, skillID, ent.level)
            else:
                aiCtrl and aiCtrl.regrTempSkillId(skillID, ent.level, tEnt_.id, boardMessageID=boardMessageID)
            # if boardMessageID:
            #     for pEnt in _players:
            #         pEnt.base.onMessagePre(boardMessageID, [tEnt_.name, SSD.datas[skillID]['name']])


def handleDungeonMoveEntityToFixedPos(e, src_e, ctx, **ref_param):
    entityGID = e.get_param('entityGID', 0)
    pos_ = e.get_param('pos_')
    moveUUID = e.get_param('moveUUID')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{0}]: after move entity to fixed pos -> {1}(pos={2},uuid={3})'.format(
        e.id, entityGID, pos_, moveUUID))


def handleCreateAvatarMirrorFromRandomPlayer(e, src_e, ctx, **ref_param):
    dungeonNo = ref_param['dungeonNo']
    entityGID = e.get_param('entityGID')
    ratio = e.get_param('ratio', 0.1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{0}]: create AvatarMirror from random player '
                '-> {1} {2}'.format(e.id, entityGID, ratio))

    if ratio <= 0:
        ratio = 1.0
        usePlayerProps = False
    else:
        usePlayerProps = True

    dunEntityData = utils.getGamePlayModuleData(int(dungeonNo)).get(str(entityGID), {})
    if not dunEntityData:
        WARNING_MSG('FlowController::handleCreateAvatarMirrorFromRandomPlayer: entityData not found',
                    dungeonNo, entityGID)
        return
    position = dunEntityData['PosX'], dunEntityData['PosY'], dunEntityData['PosZ']
    creepBaseID = dunEntityData.get('EntityID', 0)
    if creepBaseID not in CBD.datas:
        WARNING_MSG('FlowController::handleCreateAvatarMirrorFromRandomPlayer: creepBaseID not found',
                    dungeonNo, entityGID)
        return
    force = CBD.datas[creepBaseID]['force']

    spaceMgr = e.controller.owner
    if not spaceMgr.players:
        WARNING_MSG('FlowController::handleCreateAvatarMirrorFromRandomPlayer: no player in dungeon')
        return

    pid = random.choice(list(spaceMgr.players))
    pEnt = KBEngine.entities.get(pid)
    if pEnt:
        op = {'force': force, 'gameEntityId': next(utils.generateGameEntityId(entityGID, 1)),
              'dungeonFlagId': entityGID,
              'hostId': pEnt.id if usePlayerProps else 0,
              'avatarMirrorCreateType': gameconst.AvatarMirrorCreateType.FROM_CONTROLLER if usePlayerProps else gameconst.AvatarMirrorCreateType.FROM_CONTROLLER_NOHOST}

        randomTempBotId = 0
        _schoolList = []
        # TODO(): 或许可以针对玩家身上的技能情况来选取最合适的技能搭配robot职业
        # for k, v in RBTD_RBTD.datas.items():
        #     if v["schoolID"] == pEnt.school:
        #         _schoolList.append(k)
        if _schoolList:
            randomTempBotId = random.choice(_schoolList)
        if randomTempBotId:
            _robotProps = utils.getRobotPropDict(randomTempBotId, pEnt.name, pEnt.school, pEnt.level)
            op.update(_robotProps)

        pEnt._addClone(creepBaseID, position, pEnt.direction, 0, 1, False, 0.0, ratio, 0, 0, op)


def handleDungeonAddBuffToMonster(e, src_e, ctx, **ref_param):
    monsterGIDs = e.get_param('monsterGIDs', ())
    buffIDs = e.get_param('buffIDs', ())
    buffLv = e.get_param('buffLevel', 1)
    buffLvLimit = e.get_param('buffLevelLimit', -1)
    duration = e.get_param('duration', -1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: monster add buff -> {}: {}(lvl={},lvllmt={},duration={})'.format(
        e.id, monsterGIDs, buffIDs, buffLv, buffLvLimit, duration))
    for monsterGID in monsterGIDs:
        gidTag = 'gid_{}'.format(monsterGID)
        ents = e.controller.owner.getEntitiesByTag(gidTag)
        for ent in ents:
            for buffID in buffIDs:
                if buffLvLimit < 0:
                    ent.addBuff(buffID, buffLv, ent.id)
                else:
                    ent.changeBuffLevel(buffID, buffLv, ent.id, duration=duration, levelLimit=buffLvLimit)


def handleDungeonRemoveBuffFromMonster(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    buffID = e.get_param('buffID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: monster remove buff -> {}: {}'.format(
        e.id, monsterGID, buffID))
    gidTag = 'gid_{}'.format(monsterGID)
    ents = e.controller.owner.getEntitiesByTag(gidTag)
    for ent in ents:
        ent.removeBuff(buffID, ())


def handleDungeonAddBuffToAllPlayer(e, src_e, ctx, **ref_param):
    buffIDs = e.get_param('buffIDs', ())
    buffLv = e.get_param('buffLevel', 1)
    messageID = e.get_param('messageID', 0)
    buffLvLimit = e.get_param('buffLevelLimit', -1)
    duration = e.get_param('duration', -1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: all player add buff -> {}(lvl={},msg={},lvllmt={},duration={})'.format(
        e.id, buffIDs, buffLv, messageID, buffLvLimit, duration))
    spaceMgr = e.controller.owner
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if not ent:
            ERROR_MSG('flowController::handleDungeonAddBuffToAllPlayer::player ent not found Avatar({})'.format(pid))
            continue
        for buffID in buffIDs:
            if buffLvLimit < 0:
                ent.addBuff(buffID, buffLv, ent.id)
            else:
                ent.changeBuffLevel(buffID, buffLv, ent.id, duration=duration, levelLimit=buffLvLimit)
            messageID and ent.base.onMessagePre(messageID, [ent.name, BUFF.datas[buffID]['name']])


def handleDungeonRemoveBuffFromAllPlayer(e, src_e, ctx, **ref_param):
    buffID = e.get_param('buffID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: all player remove buff -> {}'.format(e.id, buffID))
    spaceMgr = e.controller.owner
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if not ent:
            ERROR_MSG('flowController::handleDungeonRemoveBuffToAllPlayer::player ent not found Avatar({})'.format(pid))
            continue
        ent.removeBuff(buffID, ())


def handleDungeonAddBuffToPlayer(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    positionType = e.get_param('positionType', gameconst.DungeonFlowPlayerChooseType.UNKNOWN)
    buffIDs = e.get_param('buffIDs', 0)
    buffLevel = e.get_param('buffLevel', 1)
    buffLvLimit = e.get_param('buffLevelLimit', -1)
    duration = e.get_param('duration', -1)
    number = e.get_param('number', 1)
    messageID = e.get_param('messageID', 0)
    minRng = e.get_param('minRng', 0)
    rng = e.get_param('rng', 0)
    exceptHighestHate = e.get_param('exceptHighestHate', 1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{0}]: add buff to player -> '
                '{1}: {2}(lvl={3},lvllmt={9},duration={10},num={4},msg={5},rng={6},minrng={7},exceptHighestHate={8})'.format(
                    e.id, positionType, buffIDs, buffLevel, number, messageID, rng, minRng, exceptHighestHate, buffLvLimit, duration))

    spaceMgr = e.controller.owner
    gidTag = 'gid_{}'.format(monsterGID)
    ents = e.controller.owner.getEntitiesByTag(gidTag)

    for ent in ents:
        _params = dict(monsterEntity=ent, number=number, exceptHighestHate=exceptHighestHate)
        minRng and _params.update({'range_min_': minRng})
        rng and _params.update({'range_': rng})
        for buffID in buffIDs:
            r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
            if not r:
                WARNING_MSG('FlowController::handleDungeonAddBuffInPlayerPosition: ', rs, positionType)
                continue
            for tEnt_ in tEnts_:
                if buffLvLimit < 0:
                    tEnt_.addBuff(buffID, buffLevel, ent.id)
                else:
                    tEnt_.changeBuffLevel(buffID, buffLevel, ent.id, duration=duration, levelLimit=buffLvLimit)
                messageID and tEnt_.base.onMessagePre(messageID, [tEnt_.name, BUFF.datas[buffID]['name']])


def handleDungeonSummonMonsterInFixedPosition(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    summonNum = e.get_param('summonNum', 0)
    # options params
    dieWithHost = e.get_param('dieWithHost', False)
    # options
    summonGIDs = e.get_param('summonGIDs')
    summonIDs = e.get_param('summonIDs')
    pos_ = e.get_param('pos')
    dir_ = e.get_param('dir')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: dungeon summon monster in fixed position -> {}: {} {} (pos={},dir={},ids={},dwh={})'.format(
        e.id, monsterGID, summonGIDs, summonNum, pos_, dir_, summonIDs, dieWithHost))

    gidTag = 'gid_{}'.format(monsterGID)
    ents = e.controller.owner.getEntitiesByTag(gidTag)

    def _createBySummonGIDs():
        # 【【任务】指定位置召唤创生物、怪物（召唤物）】
        dungeonNo = ref_param['dungeonNo']
        dunAllDatas = utils.getDunModuleData(dungeonNo)
        for _gid in summonGIDs:
            dunData = dunAllDatas[str(_gid)]
            summonID = dunData['EntityID']
            _pos = dunData['PosX'], dunData['PosY'], dunData['PosZ']
            _dir = dunData['Dir']
            context = actionContext.FlowControllerCtx(position=_pos, direction=_dir, number=summonNum, rawGameEntityId=_gid)
            for ent in ents:
                if ent.isDie():
                    continue
                ent.summon(None, context,
                           summonID, summonNum, None, ent.level, 0, dieWithHost)

    def _createDefault():
        context = actionContext.FlowControllerCtx(position=pos_, direction=dir_)
        for ent in ents:
            if ent.isDie():
                continue
            for summonID in summonIDs:
                ent.summon(None, context,
                           summonID, summonNum, None, ent.level, 0, dieWithHost)

    if summonGIDs is not None:
        _createBySummonGIDs()
    else:
        _createDefault()


def handleDungeonCreateCreationInFixedPosition(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    creationNum = e.get_param('creationNum', 0)
    # options
    creationGIDs = e.get_param('creationGIDs')
    creationIDs = e.get_param('creationIDs')
    pos_ = e.get_param('pos')
    dir_ = e.get_param('dir')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: dungeon create creation in fixed position -> {}: {} {} (pos={},dir={},ids={})'.format(
        e.id, monsterGID, creationIDs, creationNum, pos_, dir_, creationGIDs))

    spaceMgr = e.controller.owner
    noHostCreation = monsterGID == -1

    gidTag = 'gid_{}'.format(monsterGID)
    ents = e.controller.owner.getEntitiesByTag(gidTag) if not noHostCreation else [None]

    def _createByCreationGIDs():
        # 【【任务】指定位置召唤创生物、怪物（召唤物）】
        dungeonNo = ref_param['dungeonNo']
        dunAllDatas = utils.getDunModuleData(dungeonNo)
        for _gid in creationGIDs:
            dunData = dunAllDatas[str(_gid)]
            creationID = dunData['EntityID']
            _pos = dunData['PosX'], dunData['PosY'], dunData['PosZ']
            _dir = dunData['Dir']
            context = actionContext.FlowControllerCtx(position=_pos, direction=_dir, number=creationNum, rawGameEntityId=_gid)
            for ent in ents:
                args = (creationID, ent.level if ent else 1, 1, 0, -1)
                if noHostCreation:
                    _createNoHostCreation(spaceMgr.spaceID, None, context, *args,
                                          spaceMgrId=spaceMgr.id, spaceNo=spaceMgr.spaceNo)
                else:
                    ent.createCreation(None, context, *args)


    def _createDefault():
        context = actionContext.FlowControllerCtx(position=pos_, direction=dir_, number=creationNum)
        for ent in ents:
            for creationID in creationIDs:
                args = (creationID, ent.level if ent else 1, 1, 0, -1)
                if noHostCreation:
                    _createNoHostCreation(spaceMgr.spaceID, None, context, *args,
                                          spaceMgrId=spaceMgr.id, spaceNo=spaceMgr.spaceNo)
                else:
                    ent.createCreation(None, context, *args)

    if creationGIDs is not None:
        _createByCreationGIDs()
    else:
        _createDefault()


def handleDungeonCreateSummonInPlayerPosition(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    summonIDs = e.get_param('summonIDs', ())
    positionType = e.get_param('positionType', gameconst.DungeonFlowPlayerChooseType.UNKNOWN)
    minRng = e.get_param('minRng', 0)
    rng = e.get_param('rng', 0)
    number = e.get_param('number', 1)
    exceptHighestHate = e.get_param('exceptHighestHate', 1)
    dieWithHost = e.get_param('dieWithHost', False)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{0}]: dungeon create summon in player position -> '
                '{1}: {2}(t={3},rng={4},minrng={5},num={6},exceptHighestHate={7},dieWithHost={8})'.format(
                    e.id, monsterGID, summonIDs, positionType, rng, minRng, number, exceptHighestHate, dieWithHost))

    spaceMgr = e.controller.owner
    gidTag = 'gid_{}'.format(monsterGID)
    ents = e.controller.owner.getEntitiesByTag(gidTag)
    for ent in ents:
        if ent.isDie():
            continue
        _params = dict(monsterEntity=ent, number=number, exceptHighestHate=exceptHighestHate)
        minRng and _params.update({'range_min_': minRng})
        rng and _params.update({'range_': rng})
        for summonID in summonIDs:
            r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
            if not r:
                WARNING_MSG('FlowController::handleDungeonCreateSummonInPlayerPosition: ', rs, positionType)
                continue

            for tEnt_ in tEnts_:
                pos_, dir_ = tEnt_.position, tEnt_.direction[2]
                context = actionContext.FlowControllerCtx(position=pos_, direction=dir_, number=1)
                ent.summon(tEnt_, context,
                           summonID, 1, None, ent.level, 0, dieWithHost)


def handleDungeonCreateCreationInPlayerPosition(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    creationIDs = e.get_param('creationIDs', ())
    positionType = e.get_param('positionType', gameconst.DungeonFlowPlayerChooseType.UNKNOWN)
    minRng = e.get_param('minRng', 0)
    rng = e.get_param('rng', 0)
    number = e.get_param('number', 1)
    exceptHighestHate = e.get_param('exceptHighestHate', 1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{0}]: dungeon create creation in player position -> '
                '{1}: {2}(t={3},rng={4},minrng={5},num={6},exceptHighestHate={7})'.format(
                    e.id, monsterGID, creationIDs, positionType, rng, minRng, number, exceptHighestHate))

    spaceMgr = e.controller.owner
    noHostCreation = monsterGID == -1

    gidTag = 'gid_{}'.format(monsterGID)
    ents = e.controller.owner.getEntitiesByTag(gidTag) if not noHostCreation else [None]
    for ent in ents:
        _params = dict(monsterEntity=ent, number=number, exceptHighestHate=exceptHighestHate)
        minRng and _params.update({'range_min_': minRng})
        rng and _params.update({'range_': rng})
        for creationID in creationIDs:
            r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
            if not r:
                WARNING_MSG('FlowController::handleDungeonCreateCreationInPlayerPosition: ', rs, positionType)
                continue

            args = (creationID, ent.level if ent else 1, 1, 0, -1)

            for tEnt_ in tEnts_:
                # pos_, dir_ = utils.getRandomPos(tEnt_.position, rng) if rng else tEnt_.position, tEnt_.direction[2]
                pos_, dir_ = tEnt_.position, tEnt_.direction[2]
                context = actionContext.FlowControllerCtx(position=pos_, direction=dir_, number=1)

                if noHostCreation:
                    _createNoHostCreation(spaceMgr.spaceID, tEnt_, context, *args,
                                          spaceMgrId=spaceMgr.id, spaceNo=spaceMgr.spaceNo)
                else:
                    ent.createCreation(tEnt_, context, *args)


def handleCreateCreationInMonsterPosition(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID')
    creationIDs = e.get_param('creationIDs')
    targetMonsterGID = e.get_param('targetMonsterGID')
    rng = e.get_param('rng')
    number = e.get_param('number', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{0}]: dungeon create creation in monster position -> '
                '{1}: {2}(t={3},rng={4},num={5})'.format(e.id, monsterGID, creationIDs, targetMonsterGID, rng, number))

    spaceMgr = e.controller.owner
    noHostCreation = monsterGID == -1

    gidTag = 'gid_{}'.format(monsterGID)
    ents = spaceMgr.getEntitiesByTag(gidTag) if not noHostCreation else [None]
    tGidTag = 'gid_{}'.format(targetMonsterGID)
    tEnts = spaceMgr.getEntitiesByTag(tGidTag)

    if 0 < number < len(tEnts):
        tEnts = random.sample(tEnts, number)

    for ent in ents:
        for creationID in creationIDs:
            for tEnt in tEnts:
                _pos, _dir = tEnt.position, tEnt.direction[2]
                # if rng:
                #     _pos = utils.getRandomPos(_pos, rng)
                context = actionContext.FlowControllerCtx(position=_pos, direction=_dir, number=1, radius=rng)
                args = (creationID, ent.level if ent else 1, 1, 0, -1)
                if noHostCreation:
                    _createNoHostCreation(spaceMgr.spaceID, tEnt, context, *args,
                                          spaceMgrId=spaceMgr.id, spaceNo=spaceMgr.spaceNo)
                else:
                    ent.createCreation(tEnt, context, *args)


def handleRemoveCreation(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID')
    rng = e.get_param('rng')
    creationID = e.get_param('creationID')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: dungeon remove creation for monster in range -> {}: {}(rng={})'.format(
        e.id, monsterGID, creationID, rng))

    spaceMgr = e.controller.owner
    gidTag = 'gid_{}'.format(monsterGID)

    for ent in spaceMgr.getEntitiesByTag(gidTag):
        for cEnt in ent.entitiesInRange(rng, 'Creation'):
            if cEnt.creationId != creationID:
                continue
            cEnt.destroySelf(True)


def handleBroadcastMsg(e, src_e, ctx, **ref_param):
    messageID = e.get_param('messageID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: dungeon broad cast message to all players -> {}'.format(
        e.id, messageID))
    messageBody = []
    for pid in e.controller.owner.players:
        ent = KBEngine.entities.get(pid)
        ent and ent.base.onMessagePre(messageID, messageBody)


def handleClearDungeon(e, src_e, ctx, **ref_param):
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: clear dungeon'.format(e.id))
    import SkillManager
    spaceMgr = e.controller.owner
    for eid in [_ for _ in spaceMgr.spaceEntities]:
        if eid == spaceMgr.id:
            continue
        ent = KBEngine.entities.get(eid)
        if not (ent and isinstance(ent, SkillManager.SkillManager) and not ent.IsPet):
            continue
        if ent and ent.IsMonster and ent.isBoss:
            hpPercent = math.ceil((ent.hp / ent.fullHp if ent.fullHp else 1) * 100)
            if 0 == int(ent.hp) and ent.fullHp:
                hpPercent = 0
            spaceMgr.onUpdateChallengeInfo(hpPercent)
            INFO_MSG("DUNGEON FLOW -- EVENT[{}]: clear dungeon BossId {} BossHp {} BossFullHp {} hpPercent {}".format(e.id, ent.id, ent.hp, ent.fullHp, hpPercent))
        ent.destroyAllSummon()
        ent.destoryAllCreation()
        ent.delaySafeDestroy(round(random.uniform(0.1, 0.3), 1))


def handleSetDungeonStage(e, src_e, ctx, **ref_param):
    stageID = e.get_param('dungeonStageID', 1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: set dungeon stage -> {}'.format(e.id, stageID))
    spaceMgr = e.controller.owner
    spaceMgr.changeDungeonStageSet(stageID)


def handleMonsterInBattle(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: monster in battle event -> {}'.format(e.id, monsterGID))


def handleMonsterLeaveBattle(e, src_e, ctx, **ref_param):
    monsterGID = e.get_param('monsterGID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: monster leave battle event -> {}'.format(e.id, monsterGID))
    spaceMgr = e.controller.owner
    if spaceMgr:
        spaceMgr.clearAllPlayersReliveRecords()


def handleShowPopOverMsg(e, src_e, ctx, **ref_param):
    entityGID = e.get_param('entityGID', 0)
    msgID = e.get_param('messageID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: show pop over message event -> {}: {}'.format(e.id, entityGID, msgID))

    if not msgID:
        ERROR_MSG('handleShowPopOverMsg:: no msgID', e.id, entityGID, msgID)
        return

    spaceMgr = e.controller.owner
    # if entityGID == -1:
    #     # TODO(): 暂时无此需求
    #     # for pid in spaceMgr.players:
    #     #     ent = KBEngine.entities.get(pid)
    #     #     if ent and ent.isReal():
    #     #         ent.client.showPopoverMsg(msgID)
    #     return

    gidTag = 'gid_{}'.format(entityGID)

    for ent in spaceMgr.getEntitiesByTag(gidTag):
        ent._showPopoverMsg(msgID)


def handlePopDialog(e, src_e, ctx, **ref_param):
    entityGID = e.get_param('entityGID', 0)
    dlogID = e.get_param('dialogID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: show pop dialog event -> {}: {}'.format(e.id, entityGID, dlogID))

    if not dlogID:
        ERROR_MSG('handleShowPopOverMsg:: no dlogID', e.id, entityGID, dlogID)
        return

    spaceMgr = e.controller.owner
    if entityGID == -1:
        for pid in spaceMgr.players:
            ent = KBEngine.entities.get(pid)
            if ent and ent.isReal():
                pass
        return

    gidTag = 'gid_{}'.format(entityGID)

    for ent in spaceMgr.getEntitiesByTag(gidTag):
        ent._popDialog(dlogID)


def handleDungeonTaskForceComplete(e, src_e, ctx, **ref_param):
    taskID = e.get_param('taskID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: dungeon task force complete {}'.format(e.id, taskID))
    for pid in e.controller.owner.players:
        ent = KBEngine.entities.get(pid)
        ent.base.forceCompleteTaskNoCond(taskID)


def handleDungeonTaskForceFailed(e, src_e, ctx, **ref_param):
    taskID = e.get_param('taskID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: dungeon task force failed {}'.format(e.id, taskID))
    for pid in e.controller.owner.players:
        ent = KBEngine.entities.get(pid)
        ent.base.startTaskFailed(taskID, gameconst.TaskNotSuccReason.DUNGEON_CTRL)


def handleChangeDungeonNPCToBattle(e, src_e, ctx, **ref_param):
    npcIDs = e.get_param('npcIDs', 0)
    ifSetBoss = e.get_param('ifSetBoss', False)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: change dungeon NPC to battle state, {}'.format(e.id, npcIDs))
    spaceMgr = e.controller.owner
    for npcID in npcIDs:
        gidTag = 'gid_{}'.format(npcID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if not ent or not (ent.IsNpc and ent.IsCombatUnit):
                gameengine.reportCritical('flowController:handleChangeDungeonNPCToBattle:: is not valid CNpc', npcID)
                return
            ent.setToBattle(ifSetBoss)


def handleChangeDungeonNPCToNeutral(e, src_e, ctx, **ref_param):
    npcIDs = e.get_param('npcIDs', 0)
    resetDir = e.get_param('resetDir', True)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: change dungeon NPC to neutral state, {} resetDir={}'.format(e.id, npcIDs, resetDir))
    spaceMgr = e.controller.owner
    for npcID in npcIDs:
        gidTag = 'gid_{}'.format(npcID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if not ent or not (ent.IsNpc and ent.IsCombatUnit):
                gameengine.reportCritical('flowController:handleChangeDungeonNPCToNeutral:: is not valid CNpc', npcID)
                return
            ent.setToNeutral(resetDir=resetDir)


def handleChangeDungeonNPCToFriendly(e, src_e, ctx, **ref_param):
    npcIDs = e.get_param('npcIDs', 0)
    resetDir = e.get_param('resetDir', True)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: change dungeon NPC to friend state, {} resetDir={}'.format(e.id, npcIDs, resetDir))
    spaceMgr = e.controller.owner
    for npcID in npcIDs:
        gidTag = 'gid_{}'.format(npcID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if not ent or not (ent.IsNpc and ent.IsCombatUnit):
                gameengine.reportCritical('flowController:handleChangeDungeonNPCToFriendly:: is not valid CNpc', npcID)
                return
            ent.setToFriendly(resetDir=resetDir)


def handleChangeDungeonNPCDialog(e, src_e, ctx, **ref_param):
    npcID = e.get_param('npcID', 0)
    dialogID = e.get_param('dialogID', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: change dungeon NPC dialogID, {} {}'.format(e.id, npcID, dialogID))
    spaceMgr = e.controller.owner
    gidTag = 'gid_{}'.format(npcID)

    for ent in spaceMgr.getEntitiesByTag(gidTag):
        if not ent or not (ent.IsNpc and ent.IsCombatUnit):
            gameengine.reportCritical('flowController:handleChangeDungeonNPCToBattle:: is not valid CNpc', npcID)
            return
        ent.dialogID = dialogID


def handleDungeonAnyPlayerHpTrigger(e, src_e, ctx, **ref_param):
    symbol = e.get_param('symbol', 0)
    hpPrt = e.get_param('hpPercent', -1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: after any dungeon player HP condition -> {} {}'.format(
        e.id, symbol, hpPrt))


def handleAddEntityArrowTracker(e, src_e, ctx, **ref_param):
    entityGID = e.get_param('entityGID', 0)
    priority = e.get_param('priority', 255)
    triggerType = e.get_param('triggerType', gameconst.ArrowTrackingType.NORMAL)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: add entity arrow tracker. {} {} {}'.format(
        e.id, entityGID, priority, triggerType))

    spaceMgr = e.controller.owner
    gidTag = 'gid_{}'.format(entityGID)
    for ent in spaceMgr.getEntitiesByTag(gidTag):
        arrowUUID = KBEngine.genUUID64()
        spaceMgr.startEntityCrtPosArrowTracking(arrowUUID, ent.id, priority, triggerType)


def handleRemoveEntityArrowTracker(e, src_e, ctx, **ref_param):
    entityGID = e.get_param('entityGID', 0)
    triggerType = e.get_param('triggerType', gameconst.ArrowTrackingType.NORMAL)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: remove entity arrow tracker. {} {}'.format(
        e.id, entityGID, triggerType))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        ERROR_MSG("handleRemoveEntityArrowTracker::spaceMgr not found", e, src_e, ctx, ref_param)
        return

    spaceMgr.stopArrowTrackingByEntityId(int(entityGID), triggerType)


def handleClearEntityHate(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param('entityGIDs', [])
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: clear entity hate. {}'.format(e.id, entityGIDs))

    spaceMgr = e.controller.owner
    for gid in entityGIDs:
        gidTag = 'gid_{}'.format(gid)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            ent and ent.aiController and ent.aiController.hateDict.clearHate(ent)


def handleForceSelectEntityTarget(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param('entityGIDs', [])
    positionType = e.get_param('positionType', gameconst.DungeonFlowPlayerChooseType.UNKNOWN)
    minRng = e.get_param('minRng', 0)
    rng = e.get_param('rng', 0)
    exceptHighestHate = e.get_param('exceptHighestHate', 1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{0}] force select entity target -> '
                '{1}(t={2},rng={3},minrng={4},exceptHighestHate={5}'.format(
                    e.id, entityGIDs, positionType, rng, minRng, exceptHighestHate))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleForceSelectEntityTarget:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if not ent.aiController:
                continue
            _params = dict(monsterEntity=ent, exceptHighestHate=exceptHighestHate)
            minRng and _params.update({'range_min_': minRng})
            rng and _params.update({'range_': rng})

            r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
            if not r or not tEnts_:
                WARNING_MSG('FlowController::handleForceSelectEntityTarget: ', rs, positionType)
                continue

            tEnt_ = tEnts_[0]
            ent.aiController.regrTempTargetId(tEnt_.id)


def handleDungeonTrapBeTriggered(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param('entityGIDs', [])
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}] dungeon trap be triggered {}'.format(
        e.id, entityGIDs))


def handleDungeonTeleportToPosition(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param('entityGIDs', [])
    pos = e.get_param('pos', None)
    dir_ = e.get_param('dir', None)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}] dungeon teleport to position {} {}'.format(
        e.id, pos, dir_))

    if not pos or pos[0] is None or pos[1] is None or pos[2] is None:
        ERROR_MSG('FlowController::handleForceSelectEntityTarget:no pos', entityGIDs, pos, dir_)
        return

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleForceSelectEntityTarget:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            ent and ent.telToPos(pos, toDir=dir_ if dir_ is not None else ent.direction)


def handleDungeonChangeEntityForce(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param('entityGIDs', [])
    force = e.get_param('force', 0)
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] dungoen change entity force {} {}".format(
        e.id, entityGIDs, force))

    if force not in (gameconst.ForceType.Monster,
                     gameconst.ForceType.NPC,
                     gameconst.ForceType.Neutrality,
                     gameconst.ForceType.Friend):
        WARNING_MSG('FlowController::handleDungeonChangeEntityForce:force error', force)
        return

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleDungeonChangeEntityForce:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if force == gameconst.ForceType.Monster:
                ent.setToBattle()
            elif force in (gameconst.ForceType.NPC, gameconst.ForceType.Neutrality):
                ent.setToNeutral()
            elif force == gameconst.ForceType.Friend:
                ent.setToFriendly()


def handleChangeSpaceVar(e, src_e, ctx, **ref_param):
    varID = e.get_param('varID', 0)
    formula_ = e.get_param('formula', '')
    paramVarIDs = e.get_param('paramVarIDs', [])
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] change dungeon space var {} = {}({})".format(
        e.id, varID, formula_, paramVarIDs))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleChangeSpaceVar:spaceMgr not found')
        return

    # build params
    m_params = {}
    for _i_varID in paramVarIDs:
        _i_varVal = spaceMgr.getSpaceVar(_i_varID)
        if _i_varVal is not None:
            m_params[_i_varID] = _i_varVal

    # calc new val
    formula_func = F_GFD.datas[int(formula_)]['serverFormula']
    m_varVal = formula_func(m_params)

    # set var val
    m_opUUID = KBEngine.genUUID64()
    m_varSrc = gameconst.VarChangeSrc.VAR_SRC_SPACE
    m_desc = "flowController -> handleChangeSpaceVar {} {} {}, spaceNo={}".format(
        varID, formula_, paramVarIDs, spaceMgr.spaceNo)
    spaceMgr.setSpaceVar(varID, m_varVal, m_opUUID, m_varSrc, m_desc)


def handleDungeonKillEntities(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param("entityGIDs", [])
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] dungoen kill entities force {}".format(
        e.id, entityGIDs))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleDungeonKillEntities:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            ent.killSelf(gameconst.SourceType.Default)


def handleDungeonEntityImmuneDeath(e, src_e, ctx, **ref_param):
    entityGID = e.get_param("entityGID", 0)
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] dungeon entity immune death {}".format(
        e.id, entityGID))


def handleIfAllSelectEntityImmuneDeath(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param("entityGIDs", [])
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] if all select entity immune death {}".format(
        e.id, entityGIDs))


def handleCreateDugneonTeleporter(e, src_e, ctx, **ref_param):
    creationGID = e.get_param("creationGID", 0)
    targetEntityGID = e.get_param("targetEntityGID", 0)
    trapRange = e.get_param("trapRange", 0)
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] create dungeon teleporter {} (te={},rng={})".format(
        e.id, creationGID, targetEntityGID, trapRange))


def handleStopAiTick(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param("entityGIDs", [])
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] dungoen stop ai tick {}".format(
        e.id, entityGIDs))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleStopAiTick:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if not ent.thinkTimer:
                WARNING_MSG("FlowController::handleStopAiTick:skip entity AItick already stopped", entityGID, ent.id)
                continue
            ent.stopByFuben = True
            ent.stopThink()


def handleStartAiTick(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param("entityGIDs", [])
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] dungoen start ai tick {}".format(
        e.id, entityGIDs))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleStartAiTick:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if ent.thinkTimer:
                WARNING_MSG("FlowController::handleStartAiTick:skip entity already thinking", entityGID, ent.id)
                continue
            ent.stopByFuben = False
            ent.startThink()


def handleEntityStartRouting(e, src_e, ctx, **ref_params):
    entityGID = e.get_param('entityGID')
    pathID = e.get_param('pathID')
    speed = e.get_param('speed')
    moveAni = e.get_param('moveAni', gameconst.DungeonFlowMoveAni.RUN01)
    escortDistance = e.get_param('escortDistance')
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] entity start routing -> {} {} {} {} {}".format(
        e.id, pathID, pathID, speed, moveAni, escortDistance))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::buildEntityStartRouting:spaceMgr not found')
        return

    gidTag = 'gid_{}'.format(entityGID)
    for ent in spaceMgr.getEntitiesByTag(gidTag):
        if not ent:
            continue

        userData = {}

        _newBaseSpeed = _newAdjSpeed = 0.0
        _newMoveAni = ent.moveAni

        # region moveAni
        if moveAni != gameconst.DungeonFlowMoveAni.DEFAULT:
            _newMoveAni = moveAni
        # endregion

        # region speed
        if speed > 0:
            _newBaseSpeed = speed

        elif speed == 0:
            if ent.IsNpc:
                _d = NPC_DATA.datas.get(ent.npcId, {})
            else:
                _d = CBD.datas.get(ent.creepBaseId, {})
            if moveAni == gameconst.DungeonFlowMoveAni.RUN01:
                _newBaseSpeed = _d.get('baseSpeed', 0.0)

            elif moveAni == gameconst.DungeonFlowMoveAni.RUN02:
                _newBaseSpeed = _d.get('baseSpeed', 0.0)
                _newAdjSpeed = _d.get('adjSpeed', 0.0)
        # endregion

        if _newBaseSpeed > 0:
            userData.update({"baseSpeed": _newBaseSpeed})
        if _newAdjSpeed > 0:
            userData.update({"adjSpeed": _newAdjSpeed})
        if _newMoveAni != ent.moveAni:
            userData.update({"moveAni": _newMoveAni})

        escortLeaveDistance = round(escortDistance*1.5)+1 if escortDistance > 0 else 0
        _ret = ent.setRoute(pathID, escortDistance=escortDistance,
                                    escortLeaveDistance=escortLeaveDistance,
                                    speedOverwrite=userData)
        if not _ret:
            WARNING_MSG("handleEntityStartRouting:: set route failed")


def handleEntityRouteFinished(e, src_e, ctx, **ref_params):
    entityGID = e.get_param('entityGID')
    pathID = e.get_param('pathID')
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] after entity route finished -> {} {}".format(
        e.id, entityGID, pathID))


def handleEntityRoutingMissingEscort(e, src_e, ctx, **ref_params):
    entityGID = e.get_param('entityGID')
    pathID = e.get_param('pathID')
    infLoop = e.get_param('infLoop')
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] after entity routing missing rescort -> {} {} {}".format(
        e.id, entityGID, pathID, infLoop))


def handleAnyPlayerCinemaPlayEnded(e, src_e, ctx, **ref_param):
    WARNING_MSG("DUNGEON FLOW -- EVENT[{}] if any player cinema play ended".format(e.id))


def handleCastCinemaPlay(e, src_e, ctx, **ref_params):
    cinemaPlayID = e.get_param('cinemaPlayID', -1)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: cinema play:{}'.format(e.id, cinemaPlayID))
    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('handleCastCinemaPlay:spaceMgr not found')
        return
    spaceMgr.cinemaPlay(cinemaPlayID)

def handleDungeonStopCurTrans(e, src_e, ctx, **ref_param):
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: all player stop current transform'.format(e.id))
    spaceMgr = e.controller.owner
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if not ent:
            ERROR_MSG('flowController::handleDungeonStopCurTrans::player ent not found Avatar({})'.format(pid))
            continue

def handleDungeonTriggerGuide(e, src_e, ctx, **ref_param):
    triggerGuideId = e.get_param('triggerGuideId')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: all player trigger guide -> {}'.format(e.id, triggerGuideId))
    spaceMgr = e.controller.owner
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if not ent:
            ERROR_MSG('flowController::handleDungeonTriggerGuide::player ent not found Avatar({})'.format(pid))
            continue

        ent.client.onTriggerGuide(triggerGuideId)

def handleNewTransPetStart(e, src_e, ctx, **ref_param):
    transPetId = e.get_param('transPetId')
    triggerGuideId = e.get_param('triggerGuideId')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: all player new transPet start -> {}, {}'.format(e.id, transPetId, triggerGuideId))
    spaceMgr = e.controller.owner
    spaceMgr.transPetId = transPetId
    spaceMgr.triggerGuideId = triggerGuideId
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if not ent:
            ERROR_MSG('flowController::handleNewTransPetStart::player ent not found Avatar({})'.format(pid))
            continue
        ent.client.newTransPetStart(transPetId, triggerGuideId)

def handleNewTransPetEnd(e, src_e, ctx, **ref_param):
    transPetId = e.get_param('transPetId')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: all player new transPet end -> {}'.format(e.id, transPetId))
    spaceMgr = e.controller.owner
    spaceMgr.transPetId = 0
    spaceMgr.triggerGuideId = 0
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if not ent:
            ERROR_MSG('flowController::handleNewTransPetEnd::player ent not found Avatar({})'.format(pid))
            continue
        ent.client.newTransPetEnd(transPetId)

def handleDungeonPlayerForceTrans(e, src_e, ctx, **ref_param):
    transPetId = e.get_param('transPetId')
    chooseType = e.get_param('chooseType')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: player force trans -> {}, {}'.format(e.id, transPetId, chooseType))
    spaceMgr = e.controller.owner
    if chooseType == gameconst.PlayerForceTransType.ALL_PLAYERS:
        for pid in spaceMgr.players:
            ent = KBEngine.entities.get(pid)
            if not ent:
                ERROR_MSG('flowController::handleDungeonPlayerForceTrans::player ent not found Avatar({})'.format(pid))
                continue
            ent.transformMonster(transPetId, True)
    elif chooseType == gameconst.PlayerForceTransType.RAND_PLAYER:
        pid = random.choice( spaceMgr.players)
        ent = KBEngine.entities.get(pid)
        if not ent:
            ERROR_MSG('flowController::handleDungeonPlayerForceTrans::player ent not found Avatar({})'.format(pid))
            return
        ent.transformMonster(transPetId, True)


def handleChangeAllPlayerCameraStatus(e, src_e, ctx, **ref_param):
    cameraId = e.get_param('cameraId', 0)
    spaceMgr = e.controller.owner

    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: change all player camera status -> {}'.format(e.id, cameraId))
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if ent and ent.isReal():
            ent.client.changeSelfCameraStatus(cameraId)


def handleChangeAllPlayerCameraLookPos(e, src_e, ctx, **ref_param):
    entityGID = e.get_param('entityGID', 0)
    spaceMgr = e.controller.owner

    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: change all player camera lookPos -> {}'.format(e.id, entityGID))

    dungeonNo = ref_param['dungeonNo']
    dunAllDatas = utils.getDunModuleData(dungeonNo)
    dunData = dunAllDatas[str(entityGID)]

    entityPos = (dunData['PosX'], dunData['PosY'], dunData['PosZ'])
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if ent and ent.isReal():
            ent.client.changeSelfCameraLookPos(entityPos)

def handleRevertAllPlayerCameraStatus(e, src_e, ctx, **ref_param):
    spaceMgr = e.controller.owner

    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: revert all player camera status'.format(e.id))
    for pid in spaceMgr.players:
        ent = KBEngine.entities.get(pid)
        if ent and ent.isReal():
            ent.client.revertSelfCameraStatus()

def handleChangeNPCSelectableStatus(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param('entityGIDs', [])
    isSelectable = e.get_param('isSelectable', False)

    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: change npc selectable status -> {} {}'.format(e.id, entityGIDs, isSelectable))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleChangeNPCSelectableStatus:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if not ent.IsNpc:
                continue
            ent.isSelectable = isSelectable


def handleChangeEntityDirection(e, src_e, ctx, **ref_param):
    entityGIDs = e.get_param('entityGIDs', [])
    dir_ = e.get_param('dir_', None)

    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: change entities direction -> {} {}'.format(e.id, entityGIDs, dir_))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleChangeEntityDirection:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for ent in spaceMgr.getEntitiesByTag(gidTag):
            if dir_ is not None:
                ent.direction = (0.0, 0.0, dir_ * math.pi / 180)


def handleTimeFreezeStart(e, src_e, ctx, **ref_param):
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: dungeon time freeze start -> {}'.format(e.id, utils.getNow()))
    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleTimeFreezeStart:spaceMgr not found')
        return

    spaceMgr.startTimeFreeze()


def handleTimeFreezeEnd(e, src_e, ctx, **ref_param):
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: dungeon time freeze end -> {}'.format(e.id, utils.getNow()))
    spaceMgr = e.controller.owner
    if not spaceMgr:
        WARNING_MSG('FlowController::handleTimeFreezeEnd:spaceMgr not found')
        return

    spaceMgr.stopTimeFreeze()

def handleReleaseAppearanceNPC(e, src_e, ctx, **ref_params):
    npcId = e.get_param('npcId')
    randomType = e.get_param('randomType')
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: release npc -> {}:{}'.format(e.id, npcId, randomType))

def handleReleaseRebornPos(e, src_e, ctx, **ref_params):
    rebornPosGIDs = e.get_param('rebornPosGIDs', [])
    rebornPosNum = e.get_param('rebornPosNum', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: release reborn point -> {}:{}'.format(e.id, rebornPosGIDs, rebornPosNum))

def handleRecycleRebornPos(e, src_e, ctx, **ref_params):
    rebornPosGIDs = e.get_param('rebornPosGIDs', [])
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: recycle reborn point -> {}'.format(e.id, rebornPosGIDs))
    _handleRecycleInDungeon(e, rebornPosGIDs)

def handleTransferToTheDesignatedMap(e, src_e, ctx, **ref_params):
    lineNo = e.get_param('lineNo', [])
    pos = e.get_param('pos', [])
    angle = e.get_param('angle', [])
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: transfer to the designated map -> {}'.format(e.id, lineNo, pos))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        return

    spaceMgr.syncPlayer(lambda boxCell: boxCell.transferToTheDesignatedMap(lineNo, pos, angle))


def handleNotifyStartBattleCD(e, src_e, ctx, **ref_params):
    dungeonNo = e.get_param('dungeonNo', 0)
    spaceNo = e.get_param('spaceNo', 0)
    cdTime = e.get_param('cdTime', 0)

    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: notify start battle cd -> space:{} dungeon:{} cdTime:{}'.format(e.id, spaceNo, dungeonNo, cdTime))

    spaceMgr = e.controller.owner
    if not spaceMgr:
        return
    
    spaceMgr.doDungeonStartBattleCD(spaceNo, dungeonNo, cdTime)

def handleCreateBreakAwayStuckPos(e, src_e, ctx, **ref_params):
    entityId = e.get_param('entityId', 0)
    eneityNum = e.get_param('eneityNum', 0)
    WARNING_MSG('DUNGEON FLOW -- EVENT[{}]: create break away stuck pos -> {}:{}'.format(e.id, entityId, eneityNum))

    spaceMgr = e.controller.owner
    dungeonNo = formula.getDungeonNoBySpaceNo(spaceMgr.spaceNo)
    if len(entityId) == 0:
        ERROR_MSG('handleCreateBreakAwayStuckPos:: no entityId', spaceMgr.spaceNo, dungeonNo, e.id, entityId, eneityNum)
        return

    dunAllDatas = utils.getDunModuleData(dungeonNo)
    entityData = dunAllDatas.get(str(entityId[0]), {})
    if entityData:
        spaceMgr.breakStuckPos = (entityData['PosX'], entityData['PosY'], entityData['PosZ'])
        spaceMgr.breakStuckDir = entityData['Dir']



    
