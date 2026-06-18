# coding: utf-8
from KBEDebug import *
import KBEngine

import gameengine
import gameglobal
import gameconst
import formula
import random
import utils
import copy
import sMath, math, Math

import ep_ctrl

import userType
import actionContext

import gamePlay_gamePlay as GP_GPD
import creep_base as CBD
import skill_skill as SSD
import buff_buff as BUFF
import NPC_NPC as NPC_DATA
import formula_generalFormula as F_GFD
import cube_config as CC

from ._conditions import *
from ._events import *


__all__ = [
    'FlowController'
]


class _FlowControllerBeTriggeredMixin(object):
    """callbacks"""

    def onTaskComplete(self, taskId):
        LOG_DBG('FlowController::onTaskComplete -> {}'.format(taskId))
        self.toBeTrigger(WaitingTaskCompleteEvent.getTaskKey(taskId))

    def cancelTaskCompleteTriggerEvents(self, taskId, eids):
        LOG_DBG('FlowController::cancelTaskCompleteTriggerEvents => {}'.format(taskId))
        self.cancel_trigger_events(WaitingTaskCompleteEvent.getTaskKey(taskId), ids=eids)

    def onTaskFailed(self, taskId):
        LOG_DBG('FlowController::onTaskFailed -> {}'.format(taskId))
        self.toBeTrigger(WaitingTaskFailureEvent.getTaskKey(taskId))

    def cancelTaskFailedTriggerEvents(self, taskId, eids):
        LOG_DBG('FlowController::cancelTaskFailedTriggerEvents => {}'.format(taskId))
        self.cancel_trigger_events(WaitingTaskFailureEvent.getTaskKey(taskId), ids=eids)

    def onTaskInProgress(self, taskId):
        LOG_DBG('FlowController::onTaskInProgress -> {}'.format(taskId))
        self.toBeTrigger(WaitingTaskInProgressEvent.getTaskKey(taskId))

    def cancelTaskInProgressTriggerEvents(self, taskId, eids):
        LOG_DBG('FlowController::cancelTaskInProgressTriggerEvents => {}'.format(taskId))
        self.cancel_trigger_events(WaitingTaskInProgressEvent.getTaskKey(taskId), ids=eids)

    def onDungeonMonsterReleaseComplete(self, monsterGIDs):
        gameengine.panicStack("onDungeonMonsterReleaseComplete::deprecated",
                                  monsterGIDs, self.owner.spaceNo)

    def onDungeonNPCReleaseComplete(self, npcGIDs):
        gameengine.panicStack("onDungeonNPCReleaseComplete::deprecated",
                                  npcGIDs, self.owner.spaceNo)

    def onDungeonCollectionReleaseComplete(self, collGIDs):
        gameengine.panicStack("onDungeonCollectionReleaseComplete::deprecated",
                                  collGIDs, self.owner.spaceNo)

    def onDunCollectionBeCollected(self, collGID):
        LOG_DBG('FlowController::onDunCollectionBeCollected -> {}'.format(collGID))
        self._onBeCollected(collGID)
        self._onMultiCollectionAllBeCollected(collGID)

    def onDungeonCollectionBeCollectedUsePrototypeID(self, collID):
        LOG_DBG('FlowController::onDungeonCollectionBeCollectedUsePrototypeID -> {}'.format(collID))
        self._onBeCollected(collID, usePrototypeID=True)

    def _onBeCollected(self, collGID, usePrototypeID=False):
        mEvents = self.getDungeonCollectionBeCollectedEvents()
        if not mEvents:
            return

        collGID = 'cbid{}'.format(collGID) if usePrototypeID else collGID
        LOG_DBG('FlowController::_onBeCollected -> {}'.format(collGID))
        triggerEvents = []
        for _iCollGID, _iEvents in mEvents.items():
            if _iCollGID != collGID:
                continue

            triggerEvents.extend(copy.copy(_iEvents))
            _iEvents.clear()
            break

        for event, eCtx in triggerEvents:
            _etuple = (event, eCtx)
            event.continueHandleBeTriggered(eCtx)
            for _iCollGID in event.fetchArgument('collGIDs', []):
                _iCollGID = 'cbid{}'.format(_iCollGID) if usePrototypeID else _iCollGID
                i_list = mEvents.get(_iCollGID, [])
                if _etuple in i_list:
                    i_list.remove(_etuple)
            if event.fetchArgument('infLoop'):
                event.reHandleBeTriggered(*eCtx.waitingArgs, **eCtx.waitingKwargs)

    def _onMultiCollectionAllBeCollected(self, collGID):
        mEvents = self.getDungeonMultiCollectionBeCollectedEvents()
        if not mEvents:
            return

        LOG_DBG('FlowController::_onMultiCollectionAllBeCollected -> {}'.format(collGID))
        triggerEvents = []
        for _iCollGID, _iEvents in mEvents.items():
            if _iCollGID != collGID:
                continue

            triggerEvents.extend(copy.copy(_iEvents))
            _iEvents.clear()
            break

        for event, eCtx in triggerEvents:
            event.collected(collGID)
            if not event.hasAllCollected():
                continue

            _etuple = (event, eCtx)
            event.continueHandleBeTriggered(eCtx)
            for _iCollGID in event.fetchArgument('collGIDs', []):
                i_list = mEvents.get(_iCollGID, [])
                if _etuple in i_list:
                    i_list.remove(_etuple)
            if event.fetchArgument('infLoop'):
                event.reHandleBeTriggered(*eCtx.waitingArgs, **eCtx.waitingKwargs)

    def onDungeonAirWallReleaseComplete(self, airWallGIDs):
        gameengine.panicStack("onDungeonAirWallReleaseComplete::deprecated",
                                  airWallGIDs, self.owner.spaceNo)

    def onDungeonTeleporterCreatedComplete(self, telGIDs):
        LOG_DBG('FlowController::onDungeonTeleporterCreatedComplete -> {}'.format(telGIDs))
        for telGID in telGIDs:
            self.toBeTrigger(DungeonTeleporterReleaseEvent.getCollReleaseKey(telGID))

    def onMonsterInBattle(self, monsterGID):
        LOG_DBG('FlowController::onMonsterInBattle -> {}'.format(monsterGID))
        self.toBeTrigger(AIEnterAttackEvent.getEnterAttackKey(monsterGID))

    def onMonsterLeaveBattle(self, monsterGID):
        LOG_DBG('FlowController::onMonsterLeaveBattle -> {}'.format(monsterGID))
        self.toBeTrigger(AILeaveAttackEvent.getLeaveAttackKey(monsterGID))

    def onEntityMoveToFixPos(self, moveUUID, succ):
        LOG_DBG('FlowController::onEntityMoveToFixPos -> {} {}'.format(moveUUID, succ))
        succ and self.toBeTrigger(DungeonMoveEntityToFixPosEvent.getMoveKey(moveUUID))

    def onDungeonEntityimmuneDeathBeTriggered(self, entityGID):
        LOG_DBG('FlowController::onDungeonEntityimmuneDeathBeTriggered -> {}'.format(entityGID))
        self.toBeTrigger(DungeonEntityImmuneDeath.getImmuneDeathKey(entityGID))

    def onEntityRouteFinished(self, entityGID, pathID):
        LOG_DBG('FlowController::onEntityRouteFinished -> {} {}'.format(entityGID, pathID))
        self.toBeTrigger(EntityRouteFinishedEvent.getRouteFinishedKey(entityGID, pathID))

    def onEntityRoutingMissingEscort(self, entityGID, pathID):
        LOG_DBG('FlowController::onEntityRoutingMissingEscort -> {} {}'.format(entityGID, pathID))
        self.toBeTrigger(EntityRoutingMissingEscortEvent.getRouteMissingEscortKey(entityGID, pathID))

    def onPlayerCinemaPlayEnded(self, cinemaPlayID, eids=()):
        LOG_DBG('FlowController::onPlayerCinemaPlayEnded -> {} eids={}'.format(cinemaPlayID, eids))
        _key = AnyPlayerCinemaPlayEndedEvent.getCinemaPlayEndedKey(cinemaPlayID)
        if not eids:
            self.toBeTrigger(_key)
        else:
            self.toBeTriggerWithEids(_key, eids)

    def onDunEntityReleaseCompleteByEventId(self, flagIds, fromEventId):
        LOG_DBG(f"FlowController::onDunEntityReleaseCompleteByEventId -> {flagIds} {fromEventId}")
        self.toBeTrigger(getCommonReleaseKey(fromEventId, flagIds))


    def onEntityRouteFinished(self, entityGID, pathID):
        LOG_DBG('FlowController::onEntityRouteFinished -> {} {}'.format(entityGID, pathID))
        self.toBeTrigger(EntityRouteFinishedEvent.getRouteFinishedKey(entityGID, pathID))

    def onMonsterHpBeModified(self, monsterGID, oldHp, curHp, fullHp):
        _delta = int(curHp - oldHp)
        if not _delta:
            return

        monsterHPEvents = self.getMonsterHpModifyEvents(monsterGID)
        if not monsterHPEvents:
            return

        fullHp = float(fullHp)
        oldHpPercent = round(oldHp / fullHp * 100, 2)
        curHpPercent = round(curHp / fullHp * 100, 2)

        LOG_DBG('FlowController::onMonsterHpBeModified {}: {} -> {}'.format(
            monsterGID, oldHpPercent, curHpPercent))
        if _delta > 0:
            fns = (self.cmHandleHpEq, self.cmHandleHpGt, self.cmHandleHpGe)
        else:
            fns = (self.cmHandleHpEq, self.cmHandleHpLt, self.cmHandleHpLe)

        for fn in fns:
            fn(monsterHPEvents, oldHpPercent, curHpPercent)

    def cmHandleHpGe(self, hpEvents, oldHpPercent, curHpPercent):
        _symbolEnum = gameconst.DungeonFlowCompSym
        hpEvents = hpEvents.get(_symbolEnum.ge, {})
        if hpEvents:
            _triggerList = []
            for hpPrt, events in hpEvents.items():
                if oldHpPercent <= hpPrt <= curHpPercent:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()
                    # for event, eCtx in copyEvent:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleHpGt(self, hpEvents, oldHpPercent, curHpPercent):
        _symbolEnum = gameconst.DungeonFlowCompSym
        hpEvents = hpEvents.get(_symbolEnum.gt, {})
        if hpEvents:
            _triggerList = []
            for hpPrt, events in hpEvents.items():
                if oldHpPercent <= hpPrt < curHpPercent:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()
                    # for event, eCtx in copyEvents:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleHpEq(self, hpEvents, oldHpPercent, curHpPercent):
        _symbolEnum = gameconst.DungeonFlowCompSym
        hpEvents = hpEvents.get(_symbolEnum.eq, {})
        if hpEvents:
            _triggerList = []
            for hpPrt, events in hpEvents.items():
                if hpPrt == curHpPercent:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()
                    # for event, eCtx in copyEvents:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleHpLe(self, hpEvents, oldHpPercent, curHpPercent):
        _symbolEnum = gameconst.DungeonFlowCompSym
        hpEvents = hpEvents.get(_symbolEnum.le, {})
        if hpEvents:
            _triggerList = []
            for hpPrt, events in hpEvents.items():
                if oldHpPercent >= hpPrt >= curHpPercent:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()
                    # for event, eCtx in copyEvents:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleHpLt(self, hpEvents, oldHpPercent, curHpPercent):
        _symbolEnum = gameconst.DungeonFlowCompSym
        hpEvents = hpEvents.get(_symbolEnum.lt, {})
        if hpEvents:
            _triggerList = []
            for hpPrt, events in hpEvents.items():
                if oldHpPercent >= hpPrt > curHpPercent:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()
                    # for event, eCtx in copyEvents:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleNumGe(self, _restNumEvents, _newNumber):
        _symbolEnum = gameconst.DungeonFlowCompSym
        if _symbolEnum.ge in _restNumEvents:
            _triggerList = []
            _restNumEvents = _restNumEvents[_symbolEnum.ge]
            for _cNumber, events in _restNumEvents.items():
                if _newNumber >= _cNumber:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()
                    # for event, eCtx in copyEvents:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleNumGt(self, _restNumEvents, _newNumber):
        _symbolEnum = gameconst.DungeonFlowCompSym
        if _symbolEnum.gt in _restNumEvents:
            _triggerList = []
            _restNumEvents = _restNumEvents[_symbolEnum.gt]
            for _cNumber, events in _restNumEvents.items():
                if _newNumber > _cNumber:
                    copyEvents = copy.copy(events)
                    events.clear()
                    _triggerList.extend(copyEvents)
                    # for event, eCtx in copyEvents:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleNumEq(self, _restNumEvents, _newNumber):
        _symbolEnum = gameconst.DungeonFlowCompSym
        if _symbolEnum.eq in _restNumEvents:
            _triggerList = []
            _restNumEvents = _restNumEvents[_symbolEnum.eq]
            for _cNumber, events in _restNumEvents.items():
                if _newNumber == _cNumber:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()
                    # for event, eCtx in copyEvents:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleNumLe(self, _restNumEvents, _newNumber):
        _symbolEnum = gameconst.DungeonFlowCompSym
        if _symbolEnum.le in _restNumEvents:
            _triggerList = []
            _restNumEvents = _restNumEvents[_symbolEnum.le]
            for _cNumber, events in _restNumEvents.items():
                if _newNumber <= _cNumber:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()
                    # for event, eCtx in copyEvents:
                    #     event.continueHandleBeTriggered(eCtx)
            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def cmHandleNumLt(self, _restNumEvents, _newNumber):
        _symbolEnum = gameconst.DungeonFlowCompSym
        if _symbolEnum.lt in _restNumEvents:
            _triggerList = []
            _restNumEvents = _restNumEvents[_symbolEnum.lt]
            for _cNumber, events in _restNumEvents.items():
                if _newNumber < _cNumber:
                    copyEvents = copy.copy(events)
                    _triggerList.extend(copyEvents)
                    events.clear()

            for event, eCtx in _triggerList:
                event.continueHandleBeTriggered(eCtx)

    def onMonsterRestNumberIncreased(self, monsterGID, tag, spaceMgr):
        _key = (monsterGID, tag)
        _set = self.monsterRestToSumDic.get(_key)
        if not _set:
            return

        for _eventId in list(_set):
            _datas = self.monsterRestAwaitDic.get(_eventId)
            if not _datas:
                continue
            
            _gids, _tag, _dic = _datas 
            _restNum = spaceMgr.getMonsterNumByGIDsAndTag(_gids, _tag)
            LOG_DBG('onMonsterRestNumberIncreased', _gids, _tag, _eventId, _restNum)
            for fn in (self.cmHandleNumGe, self.cmHandleNumGt, self.cmHandleNumEq):
                fn(_dic, _restNum)

    def onMonsterRestNumberDecreased(self, monsterGID, tag, spaceMgr):
        _key = (monsterGID, tag)
        _set = self.monsterRestToSumDic.get(_key)
        if not _set:
            return

        for _eventId in list(_set):
            _datas = self.monsterRestAwaitDic.get(_eventId)
            if not _datas:
                continue
            
            _gids, _tag, _dic = _datas 
            _restNum = spaceMgr.getMonsterNumByGIDsAndTag(_gids, _tag)
            LOG_DBG('onMonsterRestNumberDecreased', _gids, _tag, _eventId, _restNum)
            for fn in (self.cmHandleNumLe, self.cmHandleNumLt, self.cmHandleNumEq):
                fn(_dic, _restNum)

    def onDunMonsterKillNumIncreased(self, monsterGID, newNumber, newTotalNumber):
        _monsterKillNumEvents, _globalMonsterKillNumEvents = self.getDungeonMonsterKillNumEvents(monsterGID)
        if not (_monsterKillNumEvents or _globalMonsterKillNumEvents):
            return

        LOG_DBG('FlowController::onDunMonsterKillNumIncreased {}: {} {}'.format(
            monsterGID, newNumber, newTotalNumber))

        for fn in (self.cmHandleNumGe, self.cmHandleNumGt, self.cmHandleNumEq):
            _monsterKillNumEvents and fn(_monsterKillNumEvents, newNumber)
            _globalMonsterKillNumEvents and fn(_globalMonsterKillNumEvents, newTotalNumber)

    def onCheckDunEntityKillNumberTriggered(self, monsterGID, symbol, number, curKillNum, usePrototypeID, eids):
        _checkAll = monsterGID < 0
        if (monsterGID > 0 and usePrototypeID):
            _monsterGID = 'cbid{}'.format(monsterGID)
        else:
            _monsterGID = monsterGID

        _monsterKillNumEvents, _globalMonsterKillNumEvents = self.getDungeonMonsterKillNumEvents(_monsterGID)
        if not (_monsterKillNumEvents or _globalMonsterKillNumEvents):
            return

        LOG_DBG('FlowController::onCheckDunEntityKillNumberTriggered {}: symbol={} new->{} old->{} eids={}'.format(
            _monsterGID, symbol, curKillNum, number, eids))

        _triggerList = []
        if _checkAll:
            for _killNum, events in _globalMonsterKillNumEvents.get(symbol, {}).items():
                _ret = gameconst.DungeonFlowCompSym.compare(symbol, curKillNum, _killNum)
                if not _ret:
                    continue
                _triggerList.extend(events)

        else:
            for _killNum, events in _monsterKillNumEvents.get(symbol, {}).items():
                _ret = gameconst.DungeonFlowCompSym.compare(symbol, curKillNum, _killNum)
                if not _ret:
                    continue
                _triggerList.extend(events)

        for event, eCtx in _triggerList:
            event.continueHandleBeTriggered(eCtx)

    def onDungeonPlayerRestNumberChanged(self, newNumber):
        _restNumEvents = self.getDungeonPlayerRestNumEvents()
        if not _restNumEvents:
            return

        LOG_DBG('FlowController::onDungeonPlayerRestNumberChanged: {}'.format(newNumber))

        for fn in (self.cmHandleNumGe, self.cmHandleNumGt, self.cmHandleNumEq):
            _restNumEvents and fn(_restNumEvents, newNumber)

    def onDungeonAlivePlayerCountIncreased(self, newNumber):
        _alivePlayerEvents = self.getDungeonAlivePlayerEvents()
        if not _alivePlayerEvents:
            return

        LOG_DBG('FlowController::onDungeonAlivePlayerCountIncreased: {}'.format(newNumber))

        for fn in (self.cmHandleNumGe, self.cmHandleNumGt, self.cmHandleNumEq):
            _alivePlayerEvents and fn(_alivePlayerEvents, newNumber)

    def onDungeonAlivePlayerDecreased(self, newNumber):
        _alivePlayerEvents = self.getDungeonAlivePlayerEvents()
        if not _alivePlayerEvents:
            return

        LOG_DBG('FlowController::onDungeonAlivePlayerDecreased: {}'.format(newNumber))

        for fn in (self.cmHandleNumLe, self.cmHandleNumLt, self.cmHandleNumEq):
            _alivePlayerEvents and fn(_alivePlayerEvents, newNumber)

    def onDunAnyPlayerHpBeModified(self, oldHp, crtHp, fullHp):
        _delta = int(crtHp - oldHp)
        if not _delta:
            return

        hpEvents = self.getDungeonAnyPlayerHpModifyEvents()
        if not hpEvents:
            return

        LOG_DBG('FlowController::onDunAnyPlayerHpBeModified: {} -> {}'.format(oldHp, crtHp))
        fullHp = float(fullHp)
        oldHpPercent = round(oldHp/fullHp*100, 2)
        curHpPercent = round(crtHp/fullHp*100, 2)
        LOG_WARN('FlowController::onDunAnyPlayerHpBeModified: pcg {} -> {}'.format(oldHpPercent, curHpPercent))
        if _delta > 0:
            fns = (self.cmHandleHpEq, self.cmHandleHpGt, self.cmHandleHpGe)
        else:
            fns = (self.cmHandleHpEq, self.cmHandleHpLt, self.cmHandleHpLe)

        for fn in fns:
            fn(hpEvents, oldHpPercent, curHpPercent)

    def onDunValueCheckChanged(self, varId):
        mEvents = self.getDungeonValueCheckHoldEvents()
        if not mEvents:
            return

        LOG_DBG('FlowController::onDunValueCheckChanged -> {}'.format(varId))
        triggerEvents = []
        for _iVarId, _iEvents in mEvents.items():
            if _iVarId == varId:
                triggerEvents.extend(copy.copy(_iEvents))
                _iEvents.clear()
                break

        for event, eCtx in triggerEvents:
            event.continueHandleBeTriggered(eCtx)
            for i_vid in event.fetchArgument('varIds', []):
                i_list = mEvents.get(i_vid, [])
                if (event, eCtx) in i_list:
                    i_list.remove((event, eCtx))

    def onDungeonRebornPosCreatedComplete(self, rebornPosGIDs):
        gameengine.panicStack("onDungeonRebornPosCreatedComplete::deprecated",
                                  rebornPosGIDs, self.owner.spaceNo)


class _FlowControllerCustomEventsMixin(object):

    MONSTER_AWAIT_HP_MODIFY_KEY = '_hp_modify'
    MONSTER_AWAIT_REST_NUM = '_rest_num'
    DUNGEON_MONSTER_AWAIT_KILL_NUM = '_d_kill_num'
    DUN_ALIVE_PLAYER = '_d_alive_plr'
    DUNGEON_PLAYER_REST_NUM = '_d_player_rest_num'
    DUNGEON_ANY_PLAYER_HP_MODIFY_KEY = '_d_ap_hp_modify'
    DUNGEON_SPACE_VAR_CHECK_KEY = '_d_dunvar_check'
    DUNGEON_COLLECTIBLE_KEY = '_d_coll_be_coll' # 被收集的key
    DUNGEON_MULTI_BE_COLLTECT_KEY = '_d_mult_coll_be_coll'
    GLOBAL_EVENT_KEY = '__GLOBAL__'

    def getMonsterHpModifyEvents(self, monsterGID):
        return self._getMonsterEvents(monsterGID, self.MONSTER_AWAIT_HP_MODIFY_KEY)

    def getMonsterRestNumEvents(self, monsterGID):
        t = self._getMonsterEvents(monsterGID, self.MONSTER_AWAIT_REST_NUM)
        a = self._getMonsterEvents(-1, self.MONSTER_AWAIT_REST_NUM)
        return t, a

    def getDungeonMonsterKillNumEvents(self, monsterGID):
        t = self._getMonsterEvents(monsterGID, self.DUNGEON_MONSTER_AWAIT_KILL_NUM)
        a = self._getMonsterEvents(-1, self.DUNGEON_MONSTER_AWAIT_KILL_NUM)
        return t, a

    def getDungeonAlivePlayerEvents(self):
        return self._getAwaitEvents(self.waitingsDict, self.GLOBAL_EVENT_KEY, self.DUN_ALIVE_PLAYER)

    def getDungeonPlayerRestNumEvents(self):
        return self._getAwaitEvents(self.waitingsDict, self.GLOBAL_EVENT_KEY, self.DUNGEON_PLAYER_REST_NUM)

    def getDungeonAnyPlayerHpModifyEvents(self):
        return self._getAwaitEvents(self.waitingsDict, self.GLOBAL_EVENT_KEY, self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY)

    def getDungeonValueCheckHoldEvents(self):
        return self._getAwaitEvents(self.waitingsDict, self.GLOBAL_EVENT_KEY, self.DUNGEON_SPACE_VAR_CHECK_KEY)

    def getDungeonCollectionBeCollectedEvents(self):
        return self._getAwaitEvents(self.waitingsDict, self.GLOBAL_EVENT_KEY, self.DUNGEON_COLLECTIBLE_KEY)

    def getDungeonMultiCollectionBeCollectedEvents(self):
        return self._getAwaitEvents(self.waitingsDict, self.GLOBAL_EVENT_KEY, self.DUNGEON_MULTI_BE_COLLTECT_KEY)

    def _getMonsterEvents(self, monsterGID, key):
        return self._getAwaitEvents(self.monsterAwaitDic, monsterGID, key)

    def waitingForMonsterHpMonitorTrigger(self, event, eCtx, monsterGID, symbol, hp):
        self.monsterAwaitDic.setdefault(monsterGID, {})
        self.monsterAwaitDic[monsterGID].setdefault(self.MONSTER_AWAIT_HP_MODIFY_KEY, {})
        self.monsterAwaitDic[monsterGID][self.MONSTER_AWAIT_HP_MODIFY_KEY].setdefault(symbol, {})
        self.monsterAwaitDic[monsterGID][self.MONSTER_AWAIT_HP_MODIFY_KEY][symbol].setdefault(hp, [])
        self.monsterAwaitDic[monsterGID][self.MONSTER_AWAIT_HP_MODIFY_KEY][symbol][hp].append((event, eCtx))

    def clearRestMonsterTrigger(self, eventId):
        _datas = self.monsterRestAwaitDic.pop(eventId, None)
        if not _datas:
            return

        _monsterGIDs, _tag, _ = _datas
        for _gid in _monsterGIDs:
            _key = (_gid, _tag)
            self.monsterRestToSumDic\
                .get(_key, set())\
                .discard(eventId)

    def waitingForMonsterRestNumberTrigger(self, event, eCtx, monsterGIDs, tagType, symbol, restNum):
        _dic = {
            symbol: {
                restNum: [(event, eCtx)]
            }
        }
        self.monsterRestAwaitDic[event.id] = (monsterGIDs, tagType, _dic)
        for _gid in monsterGIDs:
            _key = (_gid, tagType)
            self.monsterRestToSumDic\
                .setdefault(_key, set())\
                .add(event.id)

    def waitingForDungeonMonsterKillNumberTrigger(self, event, eCtx, monsterGID, symbol, killNum):
        self.monsterAwaitDic.setdefault(monsterGID, {})
        self.monsterAwaitDic[monsterGID].setdefault(self.DUNGEON_MONSTER_AWAIT_KILL_NUM, {})
        self.monsterAwaitDic[monsterGID][self.DUNGEON_MONSTER_AWAIT_KILL_NUM].setdefault(symbol, {})
        self.monsterAwaitDic[monsterGID][self.DUNGEON_MONSTER_AWAIT_KILL_NUM][symbol].setdefault(killNum, [])
        self.monsterAwaitDic[monsterGID][self.DUNGEON_MONSTER_AWAIT_KILL_NUM][symbol][killNum].append((event, eCtx))

    def waitingForDungeonAlivePlayerTrigger(self, event, eCtx, symbol, playerNum):
        self.waitingsDict.setdefault(self.GLOBAL_EVENT_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY].setdefault(self.DUN_ALIVE_PLAYER, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUN_ALIVE_PLAYER].setdefault(symbol, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUN_ALIVE_PLAYER][symbol].setdefault(playerNum, [])
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUN_ALIVE_PLAYER][symbol][playerNum].append((event, eCtx))

    def waitingForDungeonPlayerRestNumTrigger(self, event, eCtx, symbol, playerNum):
        self.waitingsDict.setdefault(self.GLOBAL_EVENT_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY].setdefault(self.DUNGEON_PLAYER_REST_NUM, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_PLAYER_REST_NUM].setdefault(symbol, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_PLAYER_REST_NUM][symbol].setdefault(playerNum, [])
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_PLAYER_REST_NUM][symbol][playerNum].append((event, eCtx))

    def waitingForDungeonAnyPlayerHpMonitorTrigger(self, event, eCtx, symbol, hp):
        self.waitingsDict.setdefault(self.GLOBAL_EVENT_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY].setdefault(self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY].setdefault(symbol, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY][symbol].setdefault(hp, [])
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_ANY_PLAYER_HP_MODIFY_KEY][symbol][hp].append((event, eCtx))

    def waitingForDungeonSpaceVarChangeCheck(self, event, eCtx, varId):
        self.waitingsDict.setdefault(self.GLOBAL_EVENT_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY].setdefault(self.DUNGEON_SPACE_VAR_CHECK_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_SPACE_VAR_CHECK_KEY].setdefault(varId, [])
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_SPACE_VAR_CHECK_KEY][varId].append((event, eCtx))

    def waitingForDungeonCollectionBeCollectedTrigger(self, event, eCtx, collGID):
        self.waitingsDict.setdefault(self.GLOBAL_EVENT_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY].setdefault(self.DUNGEON_COLLECTIBLE_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_COLLECTIBLE_KEY].setdefault(collGID, [])
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_COLLECTIBLE_KEY][collGID].append((event, eCtx))

    def waitingForDungeonMultiCollectionAllBeColllected(self, event, eCtx, collGID):
        self.waitingsDict.setdefault(self.GLOBAL_EVENT_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY].setdefault(self.DUNGEON_MULTI_BE_COLLTECT_KEY, {})
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_MULTI_BE_COLLTECT_KEY].setdefault(collGID, [])
        self.waitingsDict[self.GLOBAL_EVENT_KEY][self.DUNGEON_MULTI_BE_COLLTECT_KEY][collGID].append((event, eCtx))


class FlowController(ep_ctrl.controller.Controller, userType.UserSingleType,
                     _FlowControllerBeTriggeredMixin,
                     _FlowControllerCustomEventsMixin):

    # -----------------------------------------------------------------

    def _lateReload(self):
        LOG_DBG('Controller::_lateReload')
        self._lateReloadElements()
        self._lateReloadVariables()
        self._lateReloadMonsterWaitins()
        self._lateReloadWaitings()
        self._lateReloadStartNode()
        self._lateReloadReWaitings()

    def _lateReloadVariables(self):
        LOG_DBG(' - Controller::_lateReloadVariables')
        for v in self._variables.values():
            getattr(v, 'reloadScript', utils.emptyFunc)()

    def _lateReloadElements(self):
        LOG_DBG(' - Controller::_lateReloadElements')
        for v in self.elementsDic.values():
            getattr(v, 'reloadScript', utils.emptyFunc)()

    def _lateReloadWaitings(self):
        LOG_DBG(' - Controller::_lateReloadWaitings')

        def _lateReloadGlobalWaitings(data):
            LOG_DBG(' -\ Controller::_lateReloadGlobalWaitings')
            for _k, _v in data.items():
                # data[self.DUN_ALIVE_PLAYER][symbol][playerNum][(event, eCtx), ...]
                for _symbolNumDic in _v.values():
                    for _eventList in _symbolNumDic.values():
                        for _e, _ctx in _eventList:
                            getattr(_e, 'reloadScript', utils.emptyFunc)()
                            getattr(_ctx, 'reloadScript', utils.emptyFunc)()

        for k, v in self.waitingsDict.items():
            if k == self.GLOBAL_EVENT_KEY:
                _lateReloadGlobalWaitings(v)
            else:
                for event, ctx in v:
                    getattr(event, 'reloadScript', utils.emptyFunc)()
                    getattr(ctx, 'reloadScript', utils.emptyFunc)()

    def _lateReloadMonsterWaitins(self):
        LOG_DBG(' - Controller::_lateReloadMonsterWaitins')
        for v in self.monsterAwaitDic.values():
            for key, val in v.items():
                for symbolDic in val.values():
                    for _eventList in symbolDic.values():
                        for event, ctx in _eventList:
                            getattr(event, 'reloadScript', utils.emptyFunc)()
                            getattr(ctx, 'reloadScript', utils.emptyFunc)()

    def _lateReloadReWaitings(self):
        LOG_DBG(' - Controller::_lateReloadReWaitings')
        for v in self._reAwaitCache.values():
            for event, ctx in v:
                getattr(event, 'reloadScript', utils.emptyFunc)()
                getattr(ctx, 'reloadScript', utils.emptyFunc)()

    def _lateReloadStartNode(self):
        LOG_DBG(' - Controller::_lateReloadStartNode')
        getattr(self._start_node, 'reloadScript', utils.emptyFunc)()

    def __init__(self, owner, start_node=None):
        super(FlowController, self).__init__(start_node=start_node)
        self.monsterAwaitDic = {}
        self.monsterRestAwaitDic = {}
        self.monsterRestToSumDic = {}
        self._owner = owner.id

    def toBeTriggerWithEids(self, key, eids):
        if key not in self.waitingsDict:
            return
        events = self.waitingsDict[key]
        copy_events = []
        dels_eventids = []
        for idx, (event, eCtx) in enumerate(events):
            if event.id in eids:
                copy_events.append((event, eCtx))
                dels_eventids.append(idx)
        for i in reversed(dels_eventids):
            del events[i]
        try:
            for event, eCtx in copy_events:
                event.continueHandleBeTriggered(eCtx)
        finally:
            if not self.waitingsDict[key]:
                del self.waitingsDict[key]
            if key in self._reAwaitCache:
                _reEvents = self._reAwaitCache[key]
                _rmEvents = []
                for idx, (event, eCtx) in enumerate(_reEvents):
                    if event.id not in eids:
                        continue

                    self.waitingForTrigger(key, event, eCtx)
                    _rmEvents.append(idx)

                for i in reversed(_rmEvents):
                    del _reEvents[i]

                if not self._reAwaitCache[key]:
                    del self._reAwaitCache[key]

    @property
    def owner(self):
        return KBEngine.entities.get(self._owner)

    def _buildName(self, name, eventId):
        return "{}_{}".format(name, eventId)

    def getEventByEventId(self, eventId, default=None):
        return self.elementsDic.get(eventId, default)

    @staticmethod
    def _getAwaitEvents(waitings, mKey, key):
        if mKey not in waitings:
            return None
        monsterEvents = waitings[mKey]
        if not monsterEvents:
            return None

        if key not in monsterEvents:
            return None
        return monsterEvents[key]

    def cancelWaitingTriggerEvents(self, ctx, eids):
        for eventId in eids:
            event = self.elementsDic.get(eventId)
            event and event.cancelWait(ctx)

    def buildStopDelayEvent(self, eventId, eventIDs):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleStopDelayEvent,
                               name=gameconst.DungeonFlowEventType.EVstopDelayEvent)
        event.putArgument('eventIDs', eventIDs)
        return event

    def buildStartDungeonEvent(self, eventId, dungeonNo, spaceNo):
        """开始副本事件"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleStartDungeon,
                               name=gameconst.DungeonFlowEventType.EVdunStart)
        event.putArgument('dungeonNo', dungeonNo)
        event.putArgument('spaceNo', spaceNo)
        return event

    def buildDelayEndDungeonEvent(self, eventId, dungeonNo, spaceNo, delayTime, preDelayTime, isFail):
        """延迟结束副本事件"""
        event = self.buildElement(
            DelayDungeonEndEvent, 
            element_id=eventId,
            eventHandler=handleDelayEndDungeon,
            name=gameconst.DungeonFlowEventType.EVdunDelayEnd,
            spaceNo=spaceNo, 
            dungeonNo=dungeonNo, 
            delayTime=delayTime,
            isFail=isFail, 
            preDelayTime=preDelayTime)
        return event

    def buildEndDungeonEvent(self, eventId, dungeonNo, spaceNo, delayTime, isFail=False):
        """结束副本事件"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleEndDungeon,
                               name=gameconst.DungeonFlowEventType.EVdunFailed if isFail else gameconst.DungeonFlowEventType.EVdunEnd)
        event.putArgument('dungeonNo', dungeonNo)
        event.putArgument('spaceNo', spaceNo)
        event.putArgument('delayTime', delayTime)
        event.putArgument('isFail', isFail)
        return event

    def buildReleaseDungeonMonsterEvent(self, eventId, monsterGIDs, monsterNum, monsterLevel,
                                        overwriteProps, ifSetBoss, initState):
        """释放怪物事件"""
        event = self.buildElement(DungeonMonsterReleaseEvent, element_id=eventId,
                               eventHandler=handleReleaseMonster, monsterGIDs=monsterGIDs,
                               name=gameconst.DungeonFlowEventType.EVcreateMonster)
        event.putArgument('monsterNum', monsterNum)
        event.putArgument('monsterLevel', monsterLevel)
        event.putArgument('overwriteProps', overwriteProps)
        event.putArgument('ifSetBoss', ifSetBoss)
        event.putArgument('initState', initState)
        return event

    def buildReleaseDungeonInnerDemonEvent(self, eventId, innerDemonGIDs, overwriteProps, ifSetBoss, initState):
        event = self.buildElement(DungeonInnerDemonReleaseEvent, element_id=eventId,
                               eventHandler=handleReleaseInnerDemon, innerDemonGIDs=innerDemonGIDs,
                               name=gameconst.DungeonFlowEventType.EVcreateInnerDemon)
        event.putArgument('innerDemonGIDs', innerDemonGIDs)
        event.putArgument('overwriteProps', overwriteProps)
        event.putArgument('ifSetBoss', ifSetBoss)
        event.putArgument('initState', initState)
        return event

    def buildNotifyInnerDemonDataEvent(self, eventId, innerDemonGIDs, dungeonNo, spaceNo):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleNotifyInnerDemonData, innerDemonGIDs=innerDemonGIDs,
                               name=gameconst.DungeonFlowEventType.EVnotifyInnerDemonData)
        event.putArgument('innerDemonGIDs', innerDemonGIDs)
        event.putArgument('dungeonNo', dungeonNo)
        event.putArgument('spaceNo', spaceNo)
        return event
    
    def buildMonsterChangeInitState(self, eventId, monsterGIDs, initState):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleMonsterChangeInitState,
                               name=gameconst.DungeonFlowEventType.EVmonsterChangeInitState)
        event.putArgument('monsterGIDs', monsterGIDs)
        event.putArgument('initState', initState)
        return event

    def buildMonsterAddHateValue(self, eventId, entityIdList, chooseType, hateValue):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleMonsterAddHateValue,
                               name=gameconst.DungeonFlowEventType.EVmonsterAddHateValue)
        event.putArgument('monsterGIDs', entityIdList)
        event.putArgument('chooseType', chooseType)
        event.putArgument('hateValue', hateValue)
        return event

    def buildRecycleDungeonMonsterEvent(self, eventId, monsterGIDs):
        """回收怪物事件"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleRecycleMonster,
                               name=gameconst.DungeonFlowEventType.EVremoveMonster)
        event.putArgument('monsterGIDs', monsterGIDs)
        return event

    def buildDungeonRemoveNoHostCreation(self, eventId, creationGIDs, userPrototypeID):
        """回收创生事件"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonRemoveNoHostCreation,
                               name=gameconst.DungeonFlowEventType.EVremoveNoHostCreation)
        event.putArgument('creationGIDs', creationGIDs)
        event.putArgument('userPrototypeID', userPrototypeID)
        return event

    def buildReleaseDungeonNPCEvent(self, eventId, npcGIDs, npcNum, npcLevel, ifSetBoss):
        """释放NPC事件"""
        event = self.buildElement(DungeonNPCReleaseEvent, element_id=eventId,
                               npcGIDs=npcGIDs, eventHandler=handleReleaseNPC,
                               name=gameconst.DungeonFlowEventType.EVcreateNPC)
        event.putArgument('npcNum', npcNum)
        event.putArgument('npcLevel', npcLevel)
        event.putArgument('ifSetBoss', ifSetBoss)
        return event

    def buildRecycleDungeonNPCEvent(self, eventId, npcGIDs):
        """回收NPC事件"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleRecycleNPC,
                               name=gameconst.DungeonFlowEventType.EVremoveNPC)
        event.putArgument('npcGIDs', npcGIDs)
        return event

    def buildReleaseDungeonCollectionEvent(self, eventId, collGIDs, collNum, randomCollectionNum, checkHaveInFixed):
        """释放采集物事件"""
        event = self.buildElement(DungeonCollectionReleaseEvent, element_id=eventId,
                               collGIDs=collGIDs, eventHandler=handleReleaseCollection,
                               name=gameconst.DungeonFlowEventType.EVcreateCollection)
        event.putArgument('collNum', collNum)
        event.putArgument('randomCollectionNum', randomCollectionNum)
        event.putArgument('checkHaveInFixed', checkHaveInFixed)
        return event

    def buildDungeonCollectionBeCollectedEvent(self, eventId, collGIDs, usePrototypeID, infLoop, checkNow, checkOnce):
        event = self.buildElement(DungeonCollectionBeCollectedEvent, element_id=eventId,
                               collGIDs=collGIDs, checkNow=checkNow, checkOnce=checkOnce,
                               eventHandler=handleCollBeCollected,
                               name=gameconst.DungeonFlowEventType.EVcollBeCollected)
        event.putArgument('usePrototypeID', usePrototypeID)
        event.putArgument('infLoop', infLoop)
        return event

    def buildDungeonMultiCollectionAllBeCollectedEvent(self, eventId, collGIDs, infLoop):
        event = self.buildElement(DungeonMultiCollectionAllBeCollectedEvent, element_id=eventId,
                               collGIDs=collGIDs, eventHandler=handleMultiCollAllBeCollected,
                               name=gameconst.DungeonFlowEventType.EVmultiCollAllBeCollected)
        event.putArgument('infLoop', infLoop)
        return event

    def buildRecycleDungeonCollectionEvent(self, eventId, collGIDs):
        """回收采集物事件"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleRecycleCollection,
                               name=gameconst.DungeonFlowEventType.EVremoveCollection)
        event.putArgument('collGIDs', collGIDs)
        return event

    def buildReleaseDungeonAirWallEvent(self, eventId, airWallGIDs, airWallNum):
        """释放空气墙事件"""
        event = self.buildElement(DungeonAirWallReleaseEvent, element_id=eventId,
                               airWallGIDs=airWallGIDs, eventHandler=handleReleaseAirWall,
                               name=gameconst.DungeonFlowEventType.EVcreateAirWall)
        event.putArgument('airWallNum', airWallNum)
        return event

    def buildRecycleDungeonAirWallEvent(self, eventId, airWallGIDs):
        """回收空气墙事件"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleRecycleAirWall,
                               name=gameconst.DungeonFlowEventType.EVremoveAirWall)
        event.putArgument('airWallGIDs', airWallGIDs)
        return event

    def buildWaitingTaskCompleteEvent(self, eventId, taskId, checkNow, checkOnce):
        """等待任务完成事件"""
        event = self.buildElement(WaitingTaskCompleteEvent, element_id=eventId,
                               eventHandler=handleWaitingTaskCompleteEvent,
                               task_id=taskId, checknow=checkNow, checkOnce=checkOnce,
                               name=gameconst.DungeonFlowEventType.EVtaskFinished)
        return event

    def buildWaitingTaskFailedEvent(self, eventId, taskId, checkNow, checkOnce):
        """等待任务失败事件"""
        event = self.buildElement(WaitingTaskFailureEvent, element_id=eventId,
                               eventHandler=handleWaitingTaskFailedEvent,
                               task_id=taskId, checknow=checkNow, checkOnce=checkOnce,
                               name=gameconst.DungeonFlowEventType.EVtaskFailed)
        return event

    def buildMonsterHpEvent(self, eventId, monsterGID, symbol, hpPercent, checkNow, checkOnce):
        """怪物血量变化触发"""
        event = self.buildElement(MonsterHpMonitorTriggerEvent, element_id=eventId,
                               monsterGID=monsterGID, symbol=symbol, hpPercent=hpPercent,
                               checkNow=checkNow, checkOnce=checkOnce,
                               eventHandler=handleMonsterHpEvent,
                               name=gameconst.DungeonFlowEventType.EVmonsterHp)
        return event

    def buildMonsterRestNumEvent(self, eventId, monsterGIDs, symbol, number, usePrototypeID, checkNow, checkOnce):
        event = self.buildElement(MonsterRestNumberEvent, element_id=eventId,
                               monsterGIDs=monsterGIDs, symbol=symbol, number=number,
                               checkNow=checkNow, checkOnce=checkOnce,
                               eventHandler=handleMonsterRestNumEvent,
                               name=gameconst.DungeonFlowEventType.EVmonsterRestNum)
        event.putArgument('usePrototypeID', usePrototypeID)
        return event

    def buildDungeonMonsterKillNumEvent(self, eventId, monsterGID, symbol, number, usePrototypeID, checkNow, checkOnce):
        event = self.buildElement(
            DungeonMonsterKillerNumberEvent, 
            element_id=eventId,
            monsterGID=monsterGID, 
            number=number,
            symbol=symbol, 
            checkNow=checkNow, 
            checkOnce=checkOnce,
            name=gameconst.DungeonFlowEventType.EVkillMonsterNum)
        event.putArgument('usePrototypeID', usePrototypeID)
        return event

    def buildDungeonMonsterCastSkill(self, eventId, monsterGID, skillID, skillLevel, forceToUse):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonMonsterCastSkill,
                               name=gameconst.DungeonFlowEventType.EVcastSkill)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('skillID', skillID)
        event.putArgument('skillLevel', skillLevel)
        event.putArgument('forceToUse', forceToUse)
        return event

    def buildDungeonAddBuffToMonster(self, eventId, monsterGIDs, buffIDs, buffLevel, buffMaxLevel, duration):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonAddBuffToMonster,
                               name=gameconst.DungeonFlowEventType.EVaddBuffToMonster)
        event.putArgument('monsterGIDs', monsterGIDs)
        event.putArgument('buffIDs', buffIDs)
        event.putArgument('buffLevel', buffLevel)
        event.putArgument('buffMaxLevel', buffMaxLevel)
        event.putArgument('duration', duration)
        return event

    def buildDungeonRemoveBuffFromMonster(self, eventId, monsterGID, buffID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonRemoveBuffFromMonster,
                               name=gameconst.DungeonFlowEventType.EVremoveBuffFromMonster)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('buffID', buffID)
        return event

    def buildDungeonAddBuffToAllPlayer(self, eventId, buffIDs, buffLevel, messageID, buffMaxLevel, duration):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonAddBuffToAllPlayer,
                               name=gameconst.DungeonFlowEventType.EVaddBuffToAllPlayer)
        event.putArgument('buffIDs', buffIDs)
        event.putArgument('buffLevel', buffLevel)
        event.putArgument('messageID', messageID)
        event.putArgument('buffMaxLevel', buffMaxLevel)
        event.putArgument('duration', duration)
        return event

    def buildDungeonRemoveBuffFromAllPlayer(self, eventId, buffID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonRemoveBuffFromAllPlayer,
                               name=gameconst.DungeonFlowEventType.EVremoveBuffFromAllPlayer)
        event.putArgument('buffID', buffID)
        return event

    def buildDungeonAddBuffToPlayer(self, eventId, monsterGID, positionType,
                                    buffIDs, buffLevel, buffMaxLevel, duration,
                                    number, messageID, iRange, minRng, exceptHighestHate):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonAddBuffToPlayer,
                               name=gameconst.DungeonFlowEventType.EVaddBuffToPlayer)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('positionType', positionType)
        event.putArgument('buffIDs', buffIDs)
        event.putArgument('buffLevel', buffLevel)
        event.putArgument('buffMaxLevel', buffMaxLevel)
        event.putArgument('duration', duration)
        event.putArgument('number', number)
        event.putArgument('messageID', messageID)
        event.putArgument('iRange', iRange)
        event.putArgument('minRng', minRng)
        event.putArgument('exceptHighestHate', exceptHighestHate)
        return event

    def buildDungeonSummonMonsterInFixedPosition(self, eventId, monsterGID, summonGIDs, summonIDs, summonNum,
                                                 _pos, _dir, dieWithHost):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonSummonMonsterInFixedPosition,
                               name=gameconst.DungeonFlowEventType.EVsummonMonsterInFixedPosition)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('summonGIDs', summonGIDs)
        event.putArgument('summonIDs', summonIDs)
        event.putArgument('summonNum', summonNum)
        event.putArgument('pos', _pos)
        event.putArgument('dir', _dir)
        event.putArgument('dieWithHost', dieWithHost)
        return event

    def buildDungeonCreateCreationInFixedPosition(self, eventId, monsterGID, creationGIDs, creationIDs, creationNum,
                                                  _pos, _dir):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonCreateCreationInFixedPosition,
                               name=gameconst.DungeonFlowEventType.EVcreateCreationInFixedPosition)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('creationGIDs', creationGIDs)
        event.putArgument('creationIDs', creationIDs)
        event.putArgument('creationNum', creationNum)
        event.putArgument('pos', _pos)
        event.putArgument('dir', _dir)
        return event

    def buildDungeonBroadcastMsg(self, eventId, messageID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleBroadcastMsg,
                               name=gameconst.DungeonFlowEventType.EVbroadcastMsg)
        event.putArgument('messageID', messageID)
        return event

    def buildClearDungeon(self, eventId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleClearDungeon,
                               name=gameconst.DungeonFlowEventType.EVclearDungeon)
        return event

    def buildMonsterInBattle(self, eventId, monsterGID, checkNow, checkOnce):
        event = self.buildElement(AIEnterAttackEvent, element_id=eventId,
                               checkNow=checkNow, checkOnce=checkOnce,
                               eventHandler=handleMonsterInBattle,
                               name=gameconst.DungeonFlowEventType.EVmonsterInBattle,
                               monsterGID=monsterGID)
        return event

    def buildMonsterLeaveBattle(self, eventId, monsterGID, checkNow, checkOnce):
        event = self.buildElement(AILeaveAttackEvent, element_id=eventId,
                               checkNow=checkNow, checkOnce=checkOnce,
                               eventHandler=handleMonsterLeaveBattle,
                               name=gameconst.DungeonFlowEventType.EVmonsterLeaveBattle,
                               monsterGID=monsterGID)
        return event

    def buildDungeonAlivePlayer(self, eventId, symbol, number, checkNow, checkOnce):
        return self.buildElement(DungeonAlivePlayerEvent, element_id=eventId,
                                  eventHandler=handleDungeonAlivePlayerEvent,
                                  name=gameconst.DungeonFlowEventType.EValivePlayer,
                                  symbol=symbol, number=number,
                                  checkNow=checkNow, checkOnce=checkOnce)

    def buildDungeonPlayerRestNum(self, eventId, symbol, number, checkNow, checkOnce):
        return self.buildElement(
            DungeonPlayerRestNumEvent,
            element_id=eventId,
            eventHandler=handlePlayerRestNumEvent,
            name=gameconst.DungeonFlowEventType.EVplayerRestNum,
            symbol=symbol,
            number=number,
            checkNow=checkNow,
            checkOnce=checkOnce
        )


    def buildTaskUndertake(self, eventId, taskID):
        event = self.buildElement(
            FlowNodeEvent,
            element_id=eventId,
            eventHandler=handleTaskUndertake,
            name=gameconst.DungeonFlowEventType.EVtaskUndertake,
            taskID=taskID,
        )
        event.putArgument('taskID', taskID)
        return event


    def buildCreateSummonInPlayerPosition(self, eventId, monsterGID, summonIDs,
                                          positionType, iRange, minRng, number, exceptHighestHate,
                                          dieWithHost):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonCreateSummonInPlayerPosition,
                               name=gameconst.DungeonFlowEventType.EVcreateSummonInPlayerPosition)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('summonIDs', summonIDs)
        event.putArgument('positionType', positionType)
        event.putArgument('iRange', iRange)
        event.putArgument('minRng', minRng)
        event.putArgument('number', number)
        event.putArgument('exceptHighestHate', exceptHighestHate)
        event.putArgument('dieWithHost', dieWithHost)
        return event

    def buildCreateCreationInPlayerPosition(self, eventId, monsterGID, creationIDs,
                                            positionType, iRange, minRng, number, exceptHighestHate):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonCreateCreationInPlayerPosition,
                               name=gameconst.DungeonFlowEventType.EVcreateCreationInPlayerPosition)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('creationIDs', creationIDs)
        event.putArgument('positionType', positionType)
        event.putArgument('iRange', iRange)
        event.putArgument('minRng', minRng)
        event.putArgument('number', number)
        event.putArgument('exceptHighestHate', exceptHighestHate)
        return event

    def buildCreateCreationInMonsterPosition(self, eventId, monsterGID, creationIDs, targetMonsterGID, iRange, number):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleCreateCreationInMonsterPosition,
                               name=gameconst.DungeonFlowEventType.EVcreateCreationInMonsterPosition)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('creationIDs', creationIDs)
        event.putArgument('targetMonsterGID', targetMonsterGID)
        event.putArgument('iRange', iRange)
        event.putArgument('number', number)
        return event

    def buildDungeonMonsterCastSkillToPlayer(self, eventId, monsterGID, skillID,
                                             positionType, boardMessageID, number,
                                             iRange, minRng, exceptHighestHate):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonMonsterCastSkillToPlayer,
                               name=gameconst.DungeonFlowEventType.EVcastSkillToPlayer)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('skillID', skillID)
        event.putArgument('positionType', positionType)
        event.putArgument('boardMessageID', boardMessageID)
        event.putArgument('number', number)
        event.putArgument('iRange', iRange)
        event.putArgument('minRng', minRng)
        event.putArgument('exceptHighestHate', exceptHighestHate)
        return event

    def buildMoveDungeonEntityToFixedPos(self, eventId, entityGID, _pos, speed, moveAni):
        event = self.buildElement(DungeonMoveEntityToFixPosEvent, element_id=eventId,
                               eventHandler=handleDungeonMoveEntityToFixedPos,
                               entityGID=entityGID, _pos=_pos, speed=speed, moveAni=moveAni,
                               name=gameconst.DungeonFlowEventType.EVmoveEntityToFixedPosition,)
        return event

    def buildDungeonRemoveCreation(self, eventId, monsterGID, creationID, iRange):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleRemoveCreation,
                               name=gameconst.DungeonFlowEventType.EVremoveCreation)
        event.putArgument('monsterGID', monsterGID)
        event.putArgument('creationID', creationID)
        event.putArgument('iRange', iRange)
        return event

    def buildDungeonHaveCreationInRange(self, eventId, monsterGID, creationID, iRange):
        event = self.buildElement(ep_ctrl.flow.Branch, element_id=eventId,
                               eventHandler=ep_ctrl.utils.BASE_EVENT_TRIGGER_FUNC,
                               name=gameconst.DungeonFlowEventType.EVhaveCreationInRange)
        event.putArgument('__CONDITION__', conditionDungeonHaveCreationInRange(self, monsterGID, creationID, iRange))
        event.bind_condition(event, '__CONDITION__')
        return event

    def buildSetDungeonStage(self, eventId, dungeonStageID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleSetDungeonStage,
                               name=gameconst.DungeonFlowEventType.EVdunStageSet)
        event.putArgument('dungeonStageID', dungeonStageID)
        return event

    def buildShowPopoverMsg(self, eventId, entityID, messageID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleShowPopOverMsg,
                               name=gameconst.DungeonFlowEventType.EVshowPopoverMsg)
        event.putArgument('entityGID', entityID)
        event.putArgument('messageID', messageID)
        return event

    def buildPopDialog(self, eventId, entityID, dialogID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handlePopDialog,
                               name=gameconst.DungeonFlowEventType.EVshowPopoverMsg)
        event.putArgument('entityGID', entityID)
        event.putArgument('dialogID', dialogID)
        return event

    def buildDungeonTaskForceComplete(self, eventId, taskID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonTaskForceComplete,
                               name=gameconst.DungeonFlowEventType.EVdungeonTaskForceComplete)
        event.putArgument('taskID', taskID)
        return event

    def buildDungeonTaskForceFailed(self, eventId, taskID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonTaskForceFailed,
                               name=gameconst.DungeonFlowEventType.EVdungeonTaskForceFailed)
        event.putArgument('taskID', taskID)
        return event

    def buildChangeDunNPCToBattle(self, eventId, npcIDs, ifSetBoss):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeDungeonNPCToBattle,
                               name=gameconst.DungeonFlowEventType.EVchangeDunNPCToBattle)
        event.putArgument('npcIDs', npcIDs)
        event.putArgument('ifSetBoss', ifSetBoss)
        return event

    def buildChangeDunNPCToNeutral(self, eventId, npcIDs, resetDir):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeDungeonNPCToNeutral,
                               name=gameconst.DungeonFlowEventType.EVchangeDunNPCToNeutral)
        event.putArgument('npcIDs', npcIDs)
        event.putArgument('resetDir', resetDir)
        return event

    def buildChangeDunNPCToFriendly(self, eventId, npcIDs, resetDir):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeDungeonNPCToFriendly,
                               name=gameconst.DungeonFlowEventType.EVchangeDunNPCToFriendly)
        event.putArgument('npcIDs', npcIDs)
        event.putArgument('resetDir', resetDir)
        return event

    def buildChangeDunNPCDialog(self, eventId, npcID, dialogID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeDungeonNPCDialog,
                               name=gameconst.DungeonFlowEventType.EVchangeDunNPCDialog)
        event.putArgument('npcID', npcID)
        event.putArgument('dialogID', dialogID)
        return event

    def buildDungeonAnyPlayerHpEvent(self, eventId, symbol, hp, checkNow, checkOnce):
        event = self.buildElement(DungeonAnyPlayerHPMonitorTriggerEvent, element_id=eventId,
                               eventHandler=handleDungeonAnyPlayerHpTrigger,
                               symbol=symbol, hpPercent=hp,
                               checkNow=checkNow, checkOnce=checkOnce,
                               name=gameconst.DungeonFlowEventType.EVdunAnyPlayerHP)
        return event

    def buildAddEntityArrowTracker(self, eventId, entityGID, priority, triggerType):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleAddEntityArrowTracker,
                               name=gameconst.DungeonFlowEventType.EVaddEntityArrowTracker)
        event.putArgument('entityGID', entityGID)
        event.putArgument('priority', priority)
        event.putArgument('triggerType', triggerType)
        return event

    def buildRemoveEntityArrowTracker(self, eventId, entityGID, triggerType):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleRemoveEntityArrowTracker,
                               name=gameconst.DungeonFlowEventType.EVremoveEntityArrowTracker)
        event.putArgument('entityGID', entityGID)
        event.putArgument('triggerType', triggerType)
        return event

    def buildClearEntityHate(self, eventId, entityGIDs):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleClearEntityHate,
                               name=gameconst.DungeonFlowEventType.EVclearEntityHate)
        event.putArgument('entityGIDs', entityGIDs)
        return event

    def buildForceSelectEntityTarget(self, eventId, entityGIDs, positionType, iRange, minRng,
                                     exceptHighestHate):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleForceSelectEntityTarget,
                               name=gameconst.DungeonFlowEventType.EVforceSelectEntityTarget)
        event.putArgument('entityGIDs', entityGIDs)
        event.putArgument('positionType', positionType)
        event.putArgument('iRange', iRange)
        event.putArgument('minRng', minRng)
        event.putArgument('exceptHighestHate', exceptHighestHate)
        return event

    def buildRandomTrigger(self, eventId, randomArray):
        _prec = 2
        _totalWeight = sum(randomArray)
        _probabilities = []
        for  idx, p in enumerate(randomArray, 1):
            _probabilities.append((idx, p * 1 / _totalWeight))

        event = self.buildElement(FlowRandomNodeEvent, element_id=eventId,
                               probability=_probabilities, prec=_prec,
                               name=gameconst.DungeonFlowEventType.EVrandomTrigger)
        return event

    def buildDungeonTeleportToPosition(self, eventId, entityGIDs, pos, _dir):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonTeleportToPosition,
                               name=gameconst.DungeonFlowEventType.EVteleportToPosition)
        event.putArgument('entityGIDs', entityGIDs)
        event.putArgument('pos', pos)
        event.putArgument('_dir', _dir)
        return event

    def buildDungeonChangeEntityForce(self, eventId, entityGIDs, force):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonChangeEntityForce,
                               name=gameconst.DungeonFlowEventType.EVchangeEntityForce)
        event.putArgument('entityGIDs', entityGIDs)
        event.putArgument('force', force)
        return event

    def buildIntegrationEvent(self, eventId):
        return self.buildElement(FlowNodeEvent, element_id=eventId,
                                  name=gameconst.DungeonFlowEventType.EVintegrationEvent)

    def buildChangeSpaceVar(self, eventId, varID, formula, paramVarIDs):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeSpaceVar,
                               name=gameconst.DungeonFlowEventType.EVchangeSpaceVar)
        event.putArgument('varID', varID)
        event.putArgument('formula', formula)
        event.putArgument('paramVarIDs', paramVarIDs)
        return event

    def buildDungeonKillEntities(self, eventId, entityGIDs):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonKillEntities,
                               name=gameconst.DungeonFlowEventType.EVkillEntities)
        event.putArgument("entityGIDs", entityGIDs)
        return event

    def buildDungeonEntityImmuneDeath(self, eventId, entityGID):
        event = self.buildElement(DungeonEntityImmuneDeath, element_id=eventId,
                               entityGID=entityGID,
                               eventHandler=handleDungeonEntityImmuneDeath,
                               name=gameconst.DungeonFlowEventType.EVdungeonEntityImmuneDeath)
        return event


    def buildCreateDungeonTeleporter(self, eventId, entityGID, targetEntityGID, trapRange):
        event = self.buildElement(DungeonTeleporterReleaseEvent, element_id=eventId,
                               entityGID=entityGID, targetEntityGID=targetEntityGID,
                               eventHandler=handleCreateDugneonTeleporter,
                               name=gameconst.DungeonFlowEventType.EVcreateDungeonTeleporter)
        event.putArgument('trapRange', trapRange)
        return event

    def buildStopAiTick(self, eventId, entityGIDs):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleStopAiTick,
                               name=gameconst.DungeonFlowEventType.EVstopAiTick)
        event.putArgument("entityGIDs", entityGIDs)
        return event

    def buildStartAiTick(self, eventId, entityGIDs):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleStartAiTick,
                               name=gameconst.DungeonFlowEventType.EVstartAiTick)
        event.putArgument("entityGIDs", entityGIDs)
        return event

    def buildEntityStartRouting(self, eventId, entityGID, pathID, speed, moveAni, escortDistance):
        """副本实体延路点寻路"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleEntityStartRouting,
                               name=gameconst.DungeonFlowEventType.EVentityStartRouting)
        event.putArgument('entityGID', entityGID)
        event.putArgument('pathID', pathID)
        event.putArgument('speed', speed)
        event.putArgument('moveAni', moveAni)
        event.putArgument('escortDistance', escortDistance)
        return event

    def buildEntityRouteFinished(self, eventId, entityGID, pathID):
        """副本实体路点寻路完成事件"""
        event = self.buildElement(EntityRouteFinishedEvent, element_id=eventId,
                               entityGID=entityGID, pathID=pathID,
                               eventHandler=handleEntityRouteFinished,
                               name=gameconst.DungeonFlowEventType.EVentityStartRouting)
        return event

    def buildEntityRoutingMissingEscort(self, eventId, entityGID, pathID, infLoop):
        """副本实体路点寻路距离玩家过远事件"""
        event = self.buildElement(EntityRoutingMissingEscortEvent, element_id=eventId,
                               entityGID=entityGID, pathID=pathID,
                               eventHandler=handleEntityRoutingMissingEscort,
                               name=gameconst.DungeonFlowEventType.EVentityStartRouting)
        event.putArgument("infLoop", infLoop)
        return event

    def buildAnyPlayerCinemaPlayEnded(self, eventId, cinemaPlayID, delay):
        """副本内任一玩家动画播放结束触发事件"""
        event = self.buildElement(AnyPlayerCinemaPlayEndedEvent, element_id=eventId,
                               cinemaPlayID=cinemaPlayID, delay=delay,
                               eventHandler=handleAnyPlayerCinemaPlayEnded,
                               name=gameconst.DungeonFlowEventType.EVanyPlayerCinemaPlayEnded)
        return event

    def buildCastCinemaPlay(self, eventId, cinemaPlayID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleCastCinemaPlay,
                               name=gameconst.DungeonFlowEventType.EVcastCinemaPlay)
        event.putArgument("cinemaPlayID", cinemaPlayID)
        return event

    def buildDungeonStopCurTrans(self, eventId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonStopCurTrans,
                               name=gameconst.DungeonFlowEventType.EVstopCurTrans)
        return event

    def buildDungeonTriggerGuide(self, eventId, triggerGuideId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonTriggerGuide,
                               name=gameconst.DungeonFlowEventType.EVtriggerGuide)
        event.putArgument('triggerGuideId', triggerGuideId)
        return event

    def buildNewTransPetStart(self, eventId, transPetId, triggerGuideId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleNewTransPetStart,
                               name=gameconst.DungeonFlowEventType.EVnewTransPetStart)
        event.putArgument('transPetId', transPetId)
        event.putArgument('triggerGuideId', triggerGuideId)
        return event

    def buildNewTransPetEnd(self, eventId, transPetId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleNewTransPetEnd,
                               name=gameconst.DungeonFlowEventType.EVnewTransPetEnd)
        event.putArgument('transPetId', transPetId)
        return event

    def buildChangeAllPlayerCameraStatus(self, eventId, cameraId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeAllPlayerCameraStatus,
                               name=gameconst.DungeonFlowEventType.EVchangeAllPlayerCameraStatus)
        event.putArgument('cameraId', cameraId)
        return event

    def buildChangeAllPlayerCameraLookPos(self, eventId, entityGID):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeAllPlayerCameraLookPos,
                               name=gameconst.DungeonFlowEventType.EVchangeAllPlayerCameraLookPos)
        event.putArgument('entityGID', entityGID)
        return event

    def buildRevertAllPlayerCameraStatus(self, eventId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleRevertAllPlayerCameraStatus,
                                 name=gameconst.DungeonFlowEventType.EVrevertAllPlayerCameraStatus)
        return event

    def buildDungeonPlayerForceTrans(self, eventId, transPetId, chooseType):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleDungeonPlayerForceTrans,
                               name=gameconst.DungeonFlowEventType.EVplayerForceTrans)
        event.putArgument('transPetId', transPetId)
        event.putArgument('chooseType', chooseType)
        return event

    def buildChangeNPCSelectableStatus(self, eventId, entityGIDs, isSelectable):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeNPCSelectableStatus,
                               name=gameconst.DungeonFlowEventType.EVchangeNPCSelectableStatus)
        event.putArgument('entityGIDs', entityGIDs)
        event.putArgument('isSelectable', isSelectable)
        return event

    def buildWaitingTaskInProgress(self, eventId, taskId):
        event = self.buildElement(WaitingTaskInProgressEvent, element_id=eventId,
                               eventHandler=handleWaitingTaskInProgressEvent,
                               task_id=taskId, checknow=True, checkOnce=True,
                               name=gameconst.DungeonFlowEventType.EVtaskFailed)
        return event

    def buildChangeEntityDirection(self, eventId, entityGIDs, _dir):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleChangeEntityDirection,
                               name=gameconst.DungeonFlowEventType.EVchangeEntityDirection)
        event.putArgument('entityGIDs', entityGIDs)
        event.putArgument('_dir', _dir)
        return event

    def buildTimeFreezeStart(self, eventId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleTimeFreezeStart,
                               name=gameconst.DungeonFlowEventType.EVtimeFreezeStart)
        return event

    def buildTimeFreezeEnd(self, eventId):
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleTimeFreezeEnd,
                               name=gameconst.DungeonFlowEventType.EVtimeFreezeEnd)
        return event

    def buildReleaseDungeonRebornPosEvent(self, eventId, rebornPosGIDs, rebornPosNum):
        """释放复活点事件"""
        event = self.buildElement(DungeonRebornPosReleaseEvent, element_id=eventId,
                               rebornPosGIDs=rebornPosGIDs, eventHandler=handleReleaseRebornPos,
                               name=gameconst.DungeonFlowEventType.EVcreateRebornPos)
        event.putArgument('rebornPosNum', rebornPosNum)
        return event

    def buildRecycleDungeonRebornPosEvent(self, eventId, rebornPosGIDs):
        """回收复活点事件"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleRecycleRebornPos,
                               name=gameconst.DungeonFlowEventType.EVremoveRebornPos)
        event.putArgument('rebornPosGIDs', rebornPosGIDs)
        return event

    def buildTransferToTheDesignatedMap(self, eventId, lineNo, pos, angle):
        """传送到大世界目标点"""
        event = self.buildElement(
            FlowNodeEvent,
            element_id=eventId,
            eventHandler=handleTransferToTheDesignatedMap,
            name=gameconst.DungeonFlowEventType.EVtransferToTheDesignatedMap,
        )
        event.putArgument('lineNo', lineNo)
        event.putArgument('pos', pos)
        event.putArgument('angle', angle)
        return event

    def buildNotifyStartBattleCD(self, eventId, dungeonNo, spaceNo, cdTime):
        """开始战斗前cd"""
        event = self.buildElement(
            FlowNodeEvent,
            element_id=eventId,
            eventHandler=handleNotifyStartBattleCD,
            name=gameconst.DungeonFlowEventType.EVnotifyStartBattleCD,
        )
        event.putArgument('dungeonNo', dungeonNo)
        event.putArgument('spaceNo', spaceNo)
        event.putArgument('cdTime', cdTime)
        return event
    
    def buildCreateBreakAwayStuckPosEvent(self, eventId, entityId, entityNumber):
        """脱离卡死点"""
        event = self.buildElement(FlowNodeEvent, element_id=eventId,
                               eventHandler=handleCreateBreakAwayStuckPos,
                               name=gameconst.DungeonFlowEventType.EVcreateBreakAwayStuckPos)
        event.putArgument('entityId', entityId)
        event.putArgument('entityNumber', entityNumber)
        return event

def _createNoHostCreation(spaceID, target, context, *args, spaceMgrId=0, spaceNo=0, extraProps=None):
    creationLv, skillLv = 1, 0
    ttl, cnt, dirOffset, posOffset = 0, 0, None, None

    argsCnt = len(args)
    if not 1 <= argsCnt <= 7:
        raise Exception(f'create no host Creation args error: {args}')

    # 极简解包（自动覆盖传入的参数，没传的保留默认值）
    creationId, *rest = args
    if len(rest) >= 1: creationLv = rest[0]
    if len(rest) >= 2: skillLv = rest[1]
    if len(rest) >= 3: ttl = rest[2]
    if len(rest) >= 4: cnt = rest[3]
    if len(rest) >= 5: dirOffset = rest[4]
    if len(rest) >= 6: posOffset = rest[5]

    props = {
        'creationId': creationId,
        'ttl': float(ttl),
        'spaceNo': spaceNo,
        'level': creationLv,
        'targetId': 0
    }

    if target:
        props['selectedTargetId'] = target.id

    if context.actionType == actionContext.ACTION_FLOW_CONTROLLER_CALLED:
        createRadius = context.radius
        _createCount = context.number
        fixedPos, fixedDir = context.position, Math.Vector3(0.0, 0.0, context.direction*math.pi/180)
        fixedDir.normalise()
        rawGameEntityId = context.rawGameEntityId
    else:
        LOG_ERR('createNoHostCreation:: create nohost creation must set context', context)
        return

    direction = (0.0, 0.0, sMath.getYawFromDirection(fixedDir))

    if fixedDir and posOffset:
        position = sMath.posByOffset(fixedPos, fixedDir * posOffset)
    else:
        position = fixedPos

    props['fbEntityId'] = rawGameEntityId
    if spaceMgrId:
        props['spaceMgrId'] = spaceMgrId

    if extraProps:
        props.update(extraProps)

    _creations = []
    _gameEntityIdGen = utils.genGameEntityId(rawGameEntityId, _createCount)
    for i in range(_createCount):
        if rawGameEntityId:
            props = props.copy()
            props['gameEntityId'] = next(_gameEntityIdGen, 0)

        props.setdefault('tmpProps', {}).update(
            {'createRadius': createRadius, '_createCount': _createCount,
             'createIndex': i+1})
        creation = KBEngine.createEntity('Creation', spaceID, position, tuple(direction), props)
        LOG_DBG('create creation', creation.creationId, position, creation.direction)

        if not creation:
            LOG_ERR('create Error', creationId, position, spaceID)
            continue

        _creations.append(creation)

        if skillLv:
            creation.setAllSkillLv(skillLv)

    return _creations


def _handlePlayerChooseType(posType, spaceMgr, monsterEntity=None,
                            range_=0, range_min_=0, number=1, exceptHighestHate=0,
                            **kwargs):
    """ 根据playerChooseType选择相应的实体对象

    # range/range_min参数
    # 【【任务】目标选择扩展：设置目标距离范围-后端】

    :arg posType: 在 gameconst.DungeonFlowPlayerChooseEnum 中定义
    :arg monsterEntity: (可选参数) 怪物当前entity
    :arg spaceMgr: 当前spaceMgr
    :arg range_: (可选参数) 选取范围最大值
    :arg range_min_: (可选参数) 选取范围最小值
    :arg number:  (可选参数) 选取数量
    :arg exceptHighestHate: (可选参数) 排除仇恨列表前N个目标
    :arg kwargs: 兼容参数
    :return:
    """
    _entities = []

    def _processEnts(_l_eids):
        nonlocal _entities

        _l_entDic = dict()
        for _l_eid in _l_eids:
            _l_ent = KBEngine.entities.get(_l_eid)
            if _l_ent:
                _l_realEnt = utils.getEntityRealEntity(_l_ent)
            else:
                _l_realEnt = None

            if not (_l_realEnt and _l_realEnt.id not in _l_entDic):
                continue

            _l_entDic[_l_realEnt.id] = _l_realEnt

        for i in _l_entDic.values():
            _entities.append(i)

    if number < 0:
        return False, '_handlePlayerChooseType::number must ge than 0, got {}'.format(number), _entities

    if posType == gameconst.DungeonFlowPlayerChooseEnum.RAND_IN_ALL_PLAYERS:
        _pEnts = (KBEngine.entities.get(i) for i in spaceMgr.players)
        _allAlivePlayers = list(i for i in _pEnts if i and not i.isDie())
        if not _allAlivePlayers:
            return False, '_handlePlayerChooseType::RAND_IN_ALL_PLAYERS: no alive player in spaceMgr', _entities
        for _ent in random.sample(_allAlivePlayers, number) if len(_allAlivePlayers) >= number else _allAlivePlayers:
            _ent and _entities.append(_ent)

    elif monsterEntity and posType == gameconst.DungeonFlowPlayerChooseEnum.MONSTER_CURRENT_TARGET:
        _ent = KBEngine.entities.get(monsterEntity.selectedTargetId)
        if _ent:
            _entities.append(utils.getEntityRealEntity(_ent))

    elif monsterEntity and monsterEntity.aiController \
            and posType == gameconst.DungeonFlowPlayerChooseEnum.RAND_IN_MONSTER_HATRED_LIST:
        _eids = monsterEntity\
            .aiController\
            .hateDict\
            .pickRandomHatredTargetIds(
                number=number, 
                minRange=range_min_, 
                maxRange=range_)

        _processEnts(_eids)

    elif monsterEntity and monsterEntity.aiController \
            and posType == gameconst.DungeonFlowPlayerChooseEnum.RAND_IN_MONSTER_HATRED_LIST_EXCEPT_HIGHEST:
        _eids = monsterEntity\
            .aiController\
            .hateDict\
            .pickRandomHatredTargetIds(
                exceptHighest=exceptHighestHate, 
                number=number, 
                minRange=range_min_, 
                maxRange=range_)

        _processEnts(_eids)
    elif monsterEntity and monsterEntity.aiController and \
            posType == gameconst.DungeonFlowPlayerChooseEnum.MONSTER_HATRED_LIST_MONSTER:
        _eids = monsterEntity.aiController.hateDict.pickMaxHaterdMonsterTarget()
        _processEnts(_eids)
    else:
        return False, '_handlePlayerChooseType::posType not allowed', _entities

    if not len(_entities):
        return False, '_handlePlayerChooseType::player not found', _entities

    return True, 'OK', _entities


def handleStopDelayEvent(event, srcE, ctx, **refParams):
    eventIDs = event.fetchArgument('eventIDs', [])
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: stop delayEvent -> {}'.format(event.id, eventIDs))
    for eventId in eventIDs:
        se = event.controller.elementsDic.get(eventId, None)
        if not se:
            continue

        def _cancel(_e):
            if callable(getattr(_e, 'cancelDelay', None)):
                LOG_DBG('DUNGEON FLOW -- EVENT: stop delayEvent Cancel {} {}'.format(_e.id, _e.name))
                _e.cancelDelay(ctx)

        _cancel(se)
        if hasattr(se, 'eGroup'):
            for sge in se.eGroup:
                _cancel(sge)


def handleStartDungeon(event, srcE, ctx, **refParams):
    dungeonNo = event.fetchArgument('dungeonNo')
    spaceNo = event.fetchArgument('spaceNo')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: start dungeon -> {} {}'.format(event.id, dungeonNo, spaceNo))
    _dungeonSpaceType = GP_GPD.datas[dungeonNo].get('type', 0)
    if gameconst.DungeonTypeJudge.isDungeon(_dungeonSpaceType):
        tCreate = utils.curTS()
        spaceMgr = event.controller.owner
        spaceMgr.dungeonPlayMode.tCreate = tCreate
        dunStubBox = gameengine.getDungeonStubBySpaceNo(spaceNo)
        dunStubBox.onDungeonStarted(spaceNo, tCreate)
    else:
        LOG_ERR('flowController::handleStartDungeon: err', dungeonNo, _dungeonSpaceType)
        return


def handleEndDungeon(event, srcE, ctx, **refParams):
    dungeonNo = event.fetchArgument('dungeonNo')
    spaceNo = event.fetchArgument('spaceNo')
    delayTime = int(event.fetchArgument('delayTime', 0))
    isFail = event.fetchArgument('isFail', True)

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_ERR('handleEndDungeon:: spaceMgr not found')
        return

    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: end dungeon -> {} {}'.format(event.id, dungeonNo, spaceNo))
    dunStubBox = gameengine.getDungeonStubBySpaceNo(spaceNo)
    event.controller.stop_all()
    if formula.inSingleDungeonScene(spaceNo):
        dunStubBox.completeSingleDungeon(spaceNo, spaceMgr.singleDungeonBelongPlayerGBID, not isFail, delayTime)
    elif formula.inTeamDungeonScene(spaceNo):
        dunStubBox.completeTeamDungeon(spaceNo, spaceMgr.teamDungeonBelongTeamUUID, not isFail, delayTime, gameconst.DunegonCompleteReasonType.FINISHED)
    elif formula.inRaidDungeonScene(spaceNo):
        dunStubBox.completeRaidDungeon(spaceNo, spaceMgr.raidDungeonBelongRaidUUID, not isFail, delayTime, gameconst.DunegonCompleteReasonType.FINISHED)
    elif formula.inGuildBossDungeonScene(spaceNo):
        dunStubBox.completeGuildBossDungeon(spaceNo, spaceMgr.guildBossDungeonBelongGuildUUID, not isFail, delayTime, gameconst.DunegonCompleteReasonType.FINISHED)
    else:
        LOG_ERR('flowController::handleEndDungeon:', dungeonNo, spaceNo)
        return

    for _pid in event.controller.owner.players:
        _pEnt = KBEngine.entities.get(_pid)
        _pEnt and _pEnt.client.changeDungeonRemainTime(spaceNo, int(utils.curTS() + delayTime))


def handleDelayEndDungeon(event, srcE, ctx, **refParams):
    dungeonNo = event.fetchArgument('dungeonNo')
    spaceNo = event.fetchArgument('spaceNo')
    delayTime = int(event.fetchArgument('delayTime', 0))
    preDelayTime = int(event.fetchArgument('preDelayTime', 0))
    LOG_WARN("DUNGEON FLOW -- EVENT[{}]: end dungeon delay -> {} {} {}--{}".format(
        event.id, dungeonNo, spaceNo, delayTime, preDelayTime))


def _handleRecycleInDungeon(event, entityGIDs):
    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_ERR('_handleRecycleInDungeon:: spaceMgr not found')
        return

    for gid in entityGIDs:
        tag = 'gid_{}'.format(gid)
        for _ent in spaceMgr.listEntitiesByTag(tag):
            if _ent.IsCombatUnit:
                _ent.destroyAllSummon()
                _ent.destoryAllCreation()
            _ent.delaySafeDestroy(round(random.uniform(0.1, 0.3), 1))


def _handleMonsterChangeInitState(event, entityGIDs, bornState):
    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_ERR('_handleRecycleInDungeon:: spaceMgr not found')
        return

    for gid in entityGIDs:
        tag = 'gid_{}'.format(gid)
        for _ent in spaceMgr.listEntitiesByTag(tag):
            if _ent.IsCombatUnit:
                _ent.changeBornStateByFlow(bornState)


def _handleMonsterAddHateValue(event, monsterGIDs, chooseType, hateValue):
    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_ERR('_handleRecycleInDungeon:: spaceMgr not found')
        return

    _pIds = [pid for pid in spaceMgr.players if pid in KBEngine.entities]

    def _addHateAll(monster, _pids):
        if not monster.aiController:
            return

        aiController = monster.aiController
        for _pid in _pids:
            aiController.doIncreaseHate(_pid, hateValue)

    def _addRandHate(monster, _pids):
        if not monster.aiController:
            return

        monster.aiController.doIncreaseHate(random.choice(_pids), hateValue)

    if chooseType == gameconst.FlowAddHateEnum.all:
        _func = _addHateAll
    elif chooseType == gameconst.FlowAddHateEnum.rand:
        _func = _addRandHate
    else:
        LOG_ERR('_handleMonsterAddHateValue but type invalid:', chooseType, hateValue)
        return

    for gid in monsterGIDs:
        tag = 'gid_{}'.format(gid)
        for _ent in spaceMgr.listEntitiesByTag(tag):
            if _ent.IsCombatUnit:
                _func(_ent, _pIds)


def _handleRecycleByPrototypeIdInDungeon(event, entityIDs):
    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_ERR('_handleRecycleByPrototypeIdInDungeon:: spaceMgr not found')
        return

    for cpid in entityIDs:
        tag = str(cpid)
        for _ent in spaceMgr.listEntitiesByTag(tag):
            _ent.delaySafeDestroy(round(random.uniform(0.1, 0.3), 1))
        # spaceMgr.removeEntitiesByTag(tag)


def handleReleaseMonster(event, srcE, ctx, **refParams):
    monsterGIDs = event.fetchArgument('monsterGIDs')
    monsterNum = event.fetchArgument('monsterNum')
    overwriteProps = event.fetchArgument('overwriteProps')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: release monster -> {}:{}(op={})'.format(
        event.id, monsterGIDs, monsterNum, overwriteProps))

def handleReleaseInnerDemon(event, srcE, ctx, **refParams):
    innerDemonGIDs = event.fetchArgument('innerDemonGIDs')
    overwriteProps = event.fetchArgument('overwriteProps')
    spaceNo = refParams['spaceNo']
    dungeonNo = refParams['dungeonNo']
    spaceMgr = event.controller.owner
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: release inner demon -> {}:{}(op={}, dungeonNo={}, spaceNo={}, playerMode={})'.format(event.id, innerDemonGIDs, 1, overwriteProps, dungeonNo, spaceNo, spaceMgr.dungeonPlayMode))
    
    # 通知stub
    _dungeonSpaceType = GP_GPD.datas[dungeonNo].get('type', 0)
    if gameconst.DungeonTypeJudge.isDungeon(_dungeonSpaceType):
        endTime = utils.curTS() + CC.datas.get('cube_innerDemonTime', {}).get('value', 300)
        spaceMgr.dungeonPlayMode.challengeEndTime = endTime
        dunStubBox = gameengine.getDungeonStubBySpaceNo(spaceNo)
        dunStubBox.onDungeonStartChallenge(spaceNo, endTime)
    else:
        LOG_ERR('flowController::handleReleaseInnerDemon: err', dungeonNo, _dungeonSpaceType)
        return

def handleNotifyInnerDemonData(event, srcE, ctx, **refParams):
    innerDemonGIDs = event.fetchArgument('innerDemonGIDs')
    dungeonNo = event.fetchArgument('dungeonNo')
    spaceNo = event.fetchArgument('spaceNo')
    spaceMgr = event.controller.owner
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: notify inner demon data-> {}:{}(dungeonNo={}, spaceNo={}, playerMode={})'.format(event.id, innerDemonGIDs, 1, dungeonNo, spaceNo, spaceMgr.dungeonPlayMode))
    
    spaceMgr.notifyInnerDemonData(dungeonNo, spaceNo)
    
def handleRecycleMonster(event, srcE, ctx, **refParams):
    monsterGIDs = event.fetchArgument('monsterGIDs')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: recycle monster -> {}'.format(event.id, monsterGIDs))
    _handleRecycleInDungeon(event, monsterGIDs)


def handleDungeonRemoveNoHostCreation(event, srcE, ctx, **refParams):
    creationGIDs = event.fetchArgument('creationGIDs')
    userPrototypeID = event.fetchArgument('userPrototypeID', True)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: recycle not host creation -> {}(userPrototypeID={})'.format(
        event.id, creationGIDs, userPrototypeID))
    if not userPrototypeID:
        _handleRecycleInDungeon(event, creationGIDs)
    else:
        _handleRecycleByPrototypeIdInDungeon(event, creationGIDs)


def handleMonsterChangeInitState(event, srcE, ctx, **refParams):
    monsterGIDs = event.fetchArgument('monsterGIDs')
    bornState = event.fetchArgument('initState')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: monster change stone state -> {}:{}'.format(event.id, monsterGIDs, bornState))
    _handleMonsterChangeInitState(event, monsterGIDs, bornState)


def handleMonsterAddHateValue(event, srcE, ctx,  **refParams):
    monsterGIDs = event.fetchArgument('monsterGIDs')
    chooseType = event.fetchArgument('chooseType')
    hateValue = event.fetchArgument('hateValue')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: monster add hate state -> {}:{}:{}'.format(event.id, monsterGIDs, chooseType,
                                                                                       hateValue))
    _handleMonsterAddHateValue(event, monsterGIDs, chooseType, hateValue)


def handleReleaseNPC(event, srcE, ctx, **refParams):
    npcGIDs = event.fetchArgument('npcGIDs')
    npcNum = event.fetchArgument('npcNum')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: release npc -> {}:{}'.format(event.id, npcGIDs, npcNum))


def handleRecycleNPC(event, srcE, ctx, **refParams):
    npcGIDs = event.fetchArgument('npcGIDs')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: recycle npc -> {}'.format(event.id, npcGIDs))
    _handleRecycleInDungeon(event, npcGIDs)


def handleReleaseCollection(event, srcE, ctx, **refParams):
    collGIDs = event.fetchArgument('collGIDs')
    collNum = event.fetchArgument('collNum')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: release collection -> {}:{}'.format(event.id, collGIDs, collNum))


def handleCollBeCollected(event, srcE, ctx, **refParams):
    collGIDs = event.fetchArgument('collGIDs')
    usePrototypeID = event.fetchArgument('usePrototypeID', False)
    infLoop = event.fetchArgument('infLoop', False)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: collection be collected -> {}(usePrototypeID={},inf={})'.format(
        event.id, collGIDs, usePrototypeID, infLoop))


def handleMultiCollAllBeCollected(event, srcE, ctx, **refParams):
    collGIDs = event.fetchArgument('collGIDs')
    infLoop = event.fetchArgument('infLoop', False)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: multi collection all be collected -> {}(inf={})'.format(
        event.id, collGIDs, infLoop))


def handleRecycleCollection(event, srcE, ctx, **refParams):
    collGIDs = event.fetchArgument('collGIDs')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: recycle collection -> {}'.format(event.id, collGIDs))
    _handleRecycleInDungeon(event, collGIDs)


def handleReleaseAirWall(event, srcE, ctx, **refParams):
    airWallGIDs = event.fetchArgument('airWallGIDs')
    airWallNum = event.fetchArgument('airWallNum')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: release air wall -> {}:{}'.format(
        event.id, airWallGIDs, airWallNum))


def handleRecycleAirWall(event, srcE, ctx, **refParams):
    airWallGIDs = event.fetchArgument('airWallGIDs')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: recycle air wall -> {}'.format(event.id, airWallGIDs))
    _handleRecycleInDungeon(event, airWallGIDs)


def handleMonsterHpEvent(event, srcE, ctx, **refParams):
    monsterGID = event.fetchArgument('monsterGID')
    symbol = event.fetchArgument('symbol')
    hpPrt = event.fetchArgument('hpPercent')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after monster HP condition -> {}: {} {}'.format(
        event.id, monsterGID, symbol, hpPrt))


def handleMonsterRestNumEvent(event, srcE, ctx, **refParams):
    monsterGIDs = event.fetchArgument('monsterGIDs')
    symbol = event.fetchArgument('symbol')
    number = event.fetchArgument('restNum')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after monster RestNum condition -> {}: {} {}'.format(
        event.id, monsterGIDs, symbol, number))


def handleDungeonMonsterKillNumEvent(event, srcE, ctx, **refParams):
    monsterGID = event.fetchArgument('monsterGID')
    symbol = event.fetchArgument('symbol')
    number = event.fetchArgument('killNum')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after dungeon monster killNum condition -> {}: {} {}'.format(
        event.id, monsterGID, symbol, number))


def handleDungeonAlivePlayerEvent(event, srcE, ctx, **refParams):
    symbol = event.fetchArgument('symbol')
    number = event.fetchArgument('playerNum')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after dungeon player alive number --> {} {}'.format(
        event.id, symbol, number))


def handlePlayerRestNumEvent(event, srcE, ctx, **refParams):
    symbol = event.fetchArgument('symbol')
    number = event.fetchArgument('playerNum')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after player RestNum condition -> {}: {}'.format(
        event.id, symbol, number))


def handleTaskUndertake(event, srcE, ctx, **refParams):
    taskId = event.fetchArgument('taskID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after task undertake -> {}'.format(event.id, taskId))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        return

    spaceMgr.syncPlayer(lambda boxCell: boxCell.doStartClaimTask(taskId))


def handleWaitingTaskCompleteEvent(event, srcE, ctx, **refParams):
    taskId = event.fetchArgument('taskId', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after waiting task complete -> {}'.format(event.id, taskId))


def handleWaitingTaskFailedEvent(event, srcE, ctx, **refParams):
    taskId = event.fetchArgument('taskId', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after waiting task failed -X {}'.format(event.id, taskId))


def handleWaitingTaskInProgressEvent(event, srcE, ctx, **refParams):
    taskId = event.fetchArgument('taskId', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after waiting task inprogress -X {}'.format(event.id, taskId))


def handleDungeonMonsterCastSkill(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    skillID = event.fetchArgument('skillID', 0)
    skillLevel = event.fetchArgument('skillLevel', 1)
    forceToUse = event.fetchArgument('forceToUse', False)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: monster cast skill -> {}: {}(lvl={},force={})'.format(
        event.id, monsterGID, skillID, skillLevel, forceToUse))

    if skillID not in SSD.datas:
        LOG_ERR("handleDungeonMonsterCastSkill:: skillid invalid", event.id, skillID)
        return

    skillCategory = SSD.datas[skillID]['category']

    gidTag = 'gid_{}'.format(monsterGID)
    _ents = event.controller.owner.listEntitiesByTag(gidTag)
    for _ent in _ents:
        if skillCategory == gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITHOUT_ACTION:
            _context = actionContext.FlowCtrlCtx()
            _ent.castSkill(0, _context, skillID, skillLevel)
        else:
            aiCtrl = _ent.aiController
            aiCtrl and aiCtrl.regrTempSkillId(skillID, skillLevel, forceUse=forceToUse, interruptCrt=forceToUse)


def handleDungeonMonsterCastSkillToPlayer(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    skillID = event.fetchArgument('skillID', 0)
    positionType = event.fetchArgument('positionType', gameconst.DungeonFlowPlayerChooseEnum.UNKNOWN)
    boardMessageID = event.fetchArgument('boardMessageID', 0)
    number = event.fetchArgument('number', 1)
    minRng = event.fetchArgument('minRng', 0)
    iRange = event.fetchArgument('iRange', 0)
    exceptHighestHate = event.fetchArgument('exceptHighestHate', 1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{0}]: monster cast skill to player -> '
                '{1}: {2}(type={3},msg={4},num={5},iRange={6},minrng={7},exceptHighestHate={8})'.format(
                    event.id, monsterGID, skillID, positionType, boardMessageID, number, iRange, minRng, exceptHighestHate))

    if skillID not in SSD.datas:
        LOG_ERR("handleDungeonMonsterCastSkillToPlayer:: skillid invalid", event.id, monsterGID, skillID)
        return

    skillCategory = SSD.datas[skillID]['category']

    spaceMgr = event.controller.owner
    gidTag = 'gid_{}'.format(monsterGID)
    ents = spaceMgr.listEntitiesByTag(gidTag)

    _players = []
    if boardMessageID:
        for _pid in event.controller.owner.players:
            _ent = KBEngine.entities.get(_pid)
            _ent and _players.append(_ent)

    for _ent in ents:
        _params = dict(monsterEntity=_ent, number=number, exceptHighestHate=exceptHighestHate)
        if minRng:
            _params['range_min_'] = minRng

        if iRange:
            _params['range_'] = iRange

        r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
        if not r:
            LOG_WARN('FlowController::handleDungeonMonsterCastSkillToPlayer: ', rs, positionType)
            continue
        aiCtrl = _ent.aiController
        for tEnt_ in tEnts_:
            if skillCategory == gameconst.SkillCategory.CATEGORY_CAST_SKILL_WITHOUT_ACTION:
                context = actionContext.FlowCtrlCtx()
                _ent.castSkill(tEnt_, context, skillID, _ent.level)
            else:
                aiCtrl and aiCtrl.regrTempSkillId(skillID, _ent.level, tEnt_.id, boardMessageID=boardMessageID)


def handleDungeonMoveEntityToFixedPos(event, srcE, ctx, **referenceArgument):
    entityGID = event.fetchArgument('entityGID', 0)
    _pos = event.fetchArgument('_pos')
    moveUUID = event.fetchArgument('moveUUID')
    LOG_WARN('DUNGEON FLOW -- EVENT[{0}]: after move entity to fixed pos -> {1}(pos={2},uuid={3})'.format(
        event.id, entityGID, _pos, moveUUID))


def handleDungeonAddBuffToMonster(event, srcE, ctx, **referenceArgument):
    monsterGIDs = event.fetchArgument('monsterGIDs', ())
    buffIDs = event.fetchArgument('buffIDs', ())
    buffLv = event.fetchArgument('buffLevel', 1)
    buffLvLimit = event.fetchArgument('buffMaxLevel', -1)
    duration = event.fetchArgument('duration', -1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: monster add buff -> {}: {}(lvl={},lvllmt={},duration={})'.format(
        event.id, monsterGIDs, buffIDs, buffLv, buffLvLimit, duration))
    for monsterGID in monsterGIDs:
        gidTag = 'gid_{}'.format(monsterGID)
        _ents = event.controller.owner.listEntitiesByTag(gidTag)
        for _ent in _ents:
            for buffID in buffIDs:
                if buffLvLimit < 0:
                    _ent.addBuff(buffID, buffLv, _ent.id)
                else:
                    _ent.changeBuffLevel(buffID, buffLv, _ent.id, duration=duration, levelLimit=buffLvLimit)


def handleDungeonRemoveBuffFromMonster(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    buffID = event.fetchArgument('buffID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: monster remove buff -> {}: {}'.format(
        event.id, monsterGID, buffID))
    gidTag = 'gid_{}'.format(monsterGID)
    ents = event.controller.owner.listEntitiesByTag(gidTag)
    for _ent in ents:
        _ent.removeBuff(buffID, ())


def handleDungeonAddBuffToAllPlayer(event, srcE, ctx, **referenceArgument):
    buffIDs = event.fetchArgument('buffIDs', ())
    buffLv = event.fetchArgument('buffLevel', 1)
    messageID = event.fetchArgument('messageID', 0)
    buffLvLimit = event.fetchArgument('buffMaxLevel', -1)
    duration = event.fetchArgument('duration', -1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: all player add buff -> {}(lvl={},msg={},lvllmt={},duration={})'.format(
        event.id, buffIDs, buffLv, messageID, buffLvLimit, duration))
    spaceMgr = event.controller.owner
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR('flowController::handleDungeonAddBuffToAllPlayer::player _ent not found Avatar({})'.format(pid))
            continue
        for buffID in buffIDs:
            if buffLvLimit < 0:
                _ent.addBuff(buffID, buffLv, _ent.id)
            else:
                _ent.changeBuffLevel(buffID, buffLv, _ent.id, duration=duration, levelLimit=buffLvLimit)
            messageID and _ent.base.onMessagePre(messageID, [_ent.name, BUFF.datas[buffID]['name']])


def handleDungeonRemoveBuffFromAllPlayer(event, srcE, ctx, **referenceArgument):
    buffID = event.fetchArgument('buffID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: all player remove buff -> {}'.format(event.id, buffID))
    spaceMgr = event.controller.owner
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR('flowController::handleDungeonRemoveBuffToAllPlayer::player _ent not found Avatar({})'.format(pid))
            continue
        _ent.removeBuff(buffID, ())


def handleDungeonAddBuffToPlayer(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    positionType = event.fetchArgument('positionType', gameconst.DungeonFlowPlayerChooseEnum.UNKNOWN)
    buffIDs = event.fetchArgument('buffIDs', 0)
    buffLevel = event.fetchArgument('buffLevel', 1)
    buffLvLimit = event.fetchArgument('buffMaxLevel', -1)
    duration = event.fetchArgument('duration', -1)
    number = event.fetchArgument('number', 1)
    messageID = event.fetchArgument('messageID', 0)
    minRng = event.fetchArgument('minRng', 0)
    iRange = event.fetchArgument('iRange', 0)
    exceptHighestHate = event.fetchArgument('exceptHighestHate', 1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{0}]: add buff to player -> '
                '{1}: {2}(lvl={3},lvllmt={9},duration={10},num={4},msg={5},iRange={6},minrng={7},exceptHighestHate={8})'.format(
                    event.id, positionType, buffIDs, buffLevel, number, messageID, iRange, minRng, exceptHighestHate, buffLvLimit, duration))

    spaceMgr = event.controller.owner
    gidTag = 'gid_{}'.format(monsterGID)
    ents = event.controller.owner.listEntitiesByTag(gidTag)

    for _ent in ents:
        _params = dict(monsterEntity=_ent, number=number, exceptHighestHate=exceptHighestHate)
        if minRng:
            _params['range_min_'] = minRng

        if iRange:
            _params['range_'] = iRange

        for _buffID in buffIDs:
            r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
            if not r:
                LOG_WARN('FlowController::handleDungeonAddBuffInPlayerPosition: ', rs, positionType)
                continue
            for tEnt_ in tEnts_:
                if buffLvLimit < 0:
                    tEnt_.addBuff(_buffID, buffLevel, _ent.id)
                else:
                    tEnt_.changeBuffLevel(_buffID, buffLevel, _ent.id, duration=duration, levelLimit=buffLvLimit)

                if messageID: 
                    tEnt_.base.onMessagePre(messageID, [tEnt_.name, BUFF.datas[_buffID]['name']])


def handleDungeonSummonMonsterInFixedPosition(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    summonNum = event.fetchArgument('summonNum', 0)
    # options params
    dieWithHost = event.fetchArgument('dieWithHost', False)
    # options
    _summonGIDs = event.fetchArgument('summonGIDs')
    summonIDs = event.fetchArgument('summonIDs')
    _pos = event.fetchArgument('pos')
    _dir = event.fetchArgument('dir')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: dungeon summon monster in fixed position -> {}: {} {} (pos={},dir={},ids={},dwh={})'.format(
        event.id, monsterGID, _summonGIDs, summonNum, _pos, _dir, summonIDs, dieWithHost))

    gidTag = 'gid_{}'.format(monsterGID)
    ents = event.controller.owner.listEntitiesByTag(gidTag)

    if _summonGIDs is not None:
        dungeonNo = referenceArgument['dungeonNo']
        dunAllDatas = utils.getDunModuleData(dungeonNo)
        for _gid in _summonGIDs:
            dunData = dunAllDatas[str(_gid)]
            summonID = dunData['EntityID']
            _pos, _dir = (dunData['PosX'], dunData['PosY'], dunData['PosZ']), dunData['Dir']
            context = actionContext.FlowCtrlCtx(position=_pos, direction=_dir, number=summonNum, rawGameEntityId=_gid)
            for _ent in filter(lambda x: not x.isDie(), ents):
                _ent.summon(None, context,
                           summonID, summonNum, None, _ent.level, 0, dieWithHost)
    else:
        context = actionContext.FlowCtrlCtx(position=_pos, direction=_dir)
        for _ent in filter(lambda x: not x.isDie(), ents):
            for summonID in summonIDs:
                _ent.summon(None, context,
                           summonID, summonNum, None, _ent.level, 0, dieWithHost)


def handleDungeonCreateCreationInFixedPosition(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    creationNum = event.fetchArgument('creationNum', 0)
    # options
    creationGIDs = event.fetchArgument('creationGIDs')
    creationIDs = event.fetchArgument('creationIDs')
    _pos = event.fetchArgument('pos')
    _dir = event.fetchArgument('dir')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: dungeon create creation in fixed position -> {}: {} {} (pos={},dir={},ids={})'.format(
        event.id, monsterGID, creationIDs, creationNum, _pos, _dir, creationGIDs))

    spaceMgr = event.controller.owner
    noHostCreation = monsterGID == -1

    gidTag = 'gid_{}'.format(monsterGID)
    ents = event.controller.owner.listEntitiesByTag(gidTag) if not noHostCreation else [None]

    if creationGIDs is not None:
        _dungeonNo = referenceArgument['dungeonNo']
        dunAllDatas = utils.getDunModuleData(_dungeonNo)
        for _gid in creationGIDs:
            _dunData = dunAllDatas[str(_gid)]
            creationID = _dunData['EntityID']
            _pos = _dunData['PosX'], _dunData['PosY'], _dunData['PosZ']
            _dir = _dunData['Dir']
            context = actionContext.FlowCtrlCtx(position=_pos, direction=_dir, number=creationNum, rawGameEntityId=_gid)
            for _ent in ents:
                _args = (creationID, _ent.level if _ent else 1, 1, 0, -1)
                if noHostCreation:
                    _createNoHostCreation(spaceMgr.spaceID, None, context, *_args,
                                          spaceMgrId=spaceMgr.id, spaceNo=spaceMgr.spaceNo)
                else:
                    _ent.createCreation(None, context, *_args)
    else:
        context = actionContext.FlowCtrlCtx(position=_pos, direction=_dir, number=creationNum)
        for _ent in ents:
            for creationID in creationIDs:
                _args = (creationID, _ent.level if _ent else 1, 1, 0, -1)
                if noHostCreation:
                    _createNoHostCreation(spaceMgr.spaceID, None, context, *_args,
                                          spaceMgrId=spaceMgr.id, spaceNo=spaceMgr.spaceNo)
                else:
                    _ent.createCreation(None, context, *_args)


def handleDungeonCreateSummonInPlayerPosition(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    summonIDs = event.fetchArgument('summonIDs', ())
    positionType = event.fetchArgument('positionType', gameconst.DungeonFlowPlayerChooseEnum.UNKNOWN)
    minRng = event.fetchArgument('minRng', 0)
    iRange = event.fetchArgument('iRange', 0)
    number = event.fetchArgument('number', 1)
    exceptHighestHate = event.fetchArgument('exceptHighestHate', 1)
    dieWithHost = event.fetchArgument('dieWithHost', False)
    LOG_WARN('DUNGEON FLOW -- EVENT[{0}]: dungeon create summon in player position -> '
                '{1}: {2}(t={3},iRange={4},minrng={5},num={6},exceptHighestHate={7},dieWithHost={8})'.format(
                    event.id, monsterGID, summonIDs, positionType, iRange, minRng, number, exceptHighestHate, dieWithHost))

    spaceMgr = event.controller.owner
    gidTag = 'gid_{}'.format(monsterGID)
    ents = event.controller.owner.listEntitiesByTag(gidTag)

    for _ent in ents:
        if _ent.isDie():
            continue

        _params = {
            "monsterEntity": _ent,
            "number": number,
            "exceptHighestHate": exceptHighestHate
        }

        if minRng:
            _params["range_min_"] = minRng

        if iRange:
            _params["range_"] = iRange

        for summonID in summonIDs:
            r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
            if not r:
                LOG_WARN('FlowController::handleDungeonCreateSummonInPlayerPosition: ', rs, positionType)
                continue

            for tEnt_ in tEnts_:
                _pos = tEnt_.position
                _dir = tEnt_.direction[2]
                context = actionContext.FlowCtrlCtx(position=_pos, direction=_dir, number=1)
                _ent.summon(tEnt_, context,
                           summonID, 1, None, _ent.level, 0, dieWithHost)


def handleDungeonCreateCreationInPlayerPosition(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    creationIDs = event.fetchArgument('creationIDs', ())
    positionType = event.fetchArgument('positionType', gameconst.DungeonFlowPlayerChooseEnum.UNKNOWN)
    minRng = event.fetchArgument('minRng', 0)
    iRange = event.fetchArgument('iRange', 0)
    number = event.fetchArgument('number', 1)
    exceptHighestHate = event.fetchArgument('exceptHighestHate', 1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{0}]: dungeon create creation in player position -> '
                '{1}: {2}(t={3},iRange={4},minrng={5},num={6},exceptHighestHate={7})'.format(
                    event.id, monsterGID, creationIDs, positionType, iRange, minRng, number, exceptHighestHate))

    spaceMgr = event.controller.owner
    noHostCreation = monsterGID == -1

    gidTag = 'gid_{}'.format(monsterGID)
    ents = event.controller.owner.listEntitiesByTag(gidTag) if not noHostCreation else [None]
    for _ent in ents:
        _params = {
            "monsterEntity": _ent,
            "number": number,
            "exceptHighestHate": exceptHighestHate
        }

        if minRng:
            _params["range_min_"] = minRng

        if iRange:
            _params["range_"] = iRange

        for creationID in creationIDs:
            r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
            if not r:
                LOG_WARN('FlowController::handleDungeonCreateCreationInPlayerPosition: ', rs, positionType)
                continue

            _args = (creationID, _ent.level if _ent else 1, 1, 0, -1)

            for tEnt_ in tEnts_:
                _pos = tEnt_.position
                _dir = tEnt_.direction[2]

                context = actionContext.FlowCtrlCtx(position=_pos, direction=_dir, number=1)

                if noHostCreation:
                    _createNoHostCreation(spaceMgr.spaceID, tEnt_, context, *_args,
                                          spaceMgrId=spaceMgr.id, spaceNo=spaceMgr.spaceNo)
                    continue

                _ent.createCreation(tEnt_, context, *_args)


def handleCreateCreationInMonsterPosition(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID')
    creationIDs = event.fetchArgument('creationIDs')
    targetMonsterGID = event.fetchArgument('targetMonsterGID')
    iRange = event.fetchArgument('iRange')
    number = event.fetchArgument('number', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{0}]: dungeon create creation in monster position -> '
                '{1}: {2}(t={3},iRange={4},num={5})'.format(event.id, monsterGID, creationIDs, targetMonsterGID, iRange, number))

    spaceMgr = event.controller.owner
    noHostCreation = monsterGID == -1

    gidTag = 'gid_{}'.format(monsterGID)
    ents = spaceMgr.listEntitiesByTag(gidTag) if not noHostCreation else [None]
    tGidTag = 'gid_{}'.format(targetMonsterGID)
    tEnts = spaceMgr.listEntitiesByTag(tGidTag)

    if 0 < number < len(tEnts):
        tEnts = random.sample(tEnts, number)

    for _ent in ents:
        _level = _ent.level if _ent else 1

        for creationID in creationIDs:
            for tEnt in tEnts:
                _pos = tEnt.position, 
                _dir = tEnt.direction[2]
                context = actionContext.FlowCtrlCtx(position=_pos, direction=_dir, number=1, radius=iRange)
                _args = (creationID, _level, 1, 0, -1)
                if noHostCreation:
                    _createNoHostCreation(spaceMgr.spaceID, tEnt, context, *_args,
                                          spaceMgrId=spaceMgr.id, spaceNo=spaceMgr.spaceNo)
                else:
                    _ent.createCreation(tEnt, context, *_args)


def handleRemoveCreation(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID')
    iRange = event.fetchArgument('iRange')
    creationID = event.fetchArgument('creationID')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: dungeon remove creation for monster in range -> {}: {}(iRange={})'.format(
        event.id, monsterGID, creationID, iRange))

    spaceMgr = event.controller.owner
    gidTag = 'gid_{}'.format(monsterGID)

    for _ent in spaceMgr.listEntitiesByTag(gidTag):
        for cEnt in _ent.entitiesInRange(iRange, 'Creation'):
            if cEnt.creationId != creationID:
                continue
            cEnt.destroySelf(True)


def handleBroadcastMsg(event, srcE, ctx, **referenceArgument):
    messageID = event.fetchArgument('messageID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: dungeon broad cast message to all players -> {}'.format(
        event.id, messageID))
    messageBody = []
    for pid in event.controller.owner.players:
        _ent = KBEngine.entities.get(pid)
        _ent and _ent.base.onMessagePre(messageID, messageBody)


def handleClearDungeon(event, srcE, ctx, **referenceArgument):
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: clear dungeon'.format(event.id))
    import SkillManager
    spaceMgr = event.controller.owner
    for eventId in [_ for _ in spaceMgr.spaceEntitiesDic]:
        if eventId == spaceMgr.id:
            continue
        _ent = KBEngine.entities.get(eventId)
        if not (_ent and isinstance(_ent, SkillManager.SkillManager)):
            continue
        if _ent and _ent.IsMonster and _ent.isBoss:
            hpPercent = math.ceil((_ent.hp / _ent.fullHp if _ent.fullHp else 1) * 100)
            if 0 == int(_ent.hp) and _ent.fullHp:
                hpPercent = 0
            spaceMgr.onUpdateChallengeInfo(hpPercent)
            LOG_INFO("DUNGEON FLOW -- EVENT[{}]: clear dungeon BossId {} BossHp {} BossFullHp {} hpPercent {}".format(event.id, _ent.id, _ent.hp, _ent.fullHp, hpPercent))
        _ent.destroyAllSummon()
        _ent.destoryAllCreation()
        _ent.delaySafeDestroy(round(random.uniform(0.1, 0.3), 1))


def handleSetDungeonStage(event, srcE, ctx, **referenceArgument):
    stageID = event.fetchArgument('dungeonStageID', 1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: set dungeon stage -> {}'.format(event.id, stageID))
    spaceMgr = event.controller.owner
    spaceMgr.changeDungeonStageSet(stageID)


def handleMonsterInBattle(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: monster in battle event -> {}'.format(event.id, monsterGID))


def handleMonsterLeaveBattle(event, srcE, ctx, **referenceArgument):
    monsterGID = event.fetchArgument('monsterGID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: monster leave battle event -> {}'.format(event.id, monsterGID))
    spaceMgr = event.controller.owner
    if spaceMgr:
        spaceMgr.clearAllPlayersReliveRecords()


def handleShowPopOverMsg(event, srcE, ctx, **referenceArgument):
    entityGID = event.fetchArgument('entityGID', 0)
    msgID = event.fetchArgument('messageID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: show pop over message event -> {}: {}'.format(event.id, entityGID, msgID))

    if not msgID:
        LOG_ERR('handleShowPopOverMsg:: no msgID', event.id, entityGID, msgID)
        return

    spaceMgr = event.controller.owner

    gidTag = 'gid_{}'.format(entityGID)

    for _ent in spaceMgr.listEntitiesByTag(gidTag):
        _ent._showPopoverMsg(msgID)


def handlePopDialog(event, srcE, ctx, **referenceArgument):
    entityGID = event.fetchArgument('entityGID', 0)
    dlogID = event.fetchArgument('dialogID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: show pop dialog event -> {}: {}'.format(event.id, entityGID, dlogID))

    if not dlogID:
        LOG_ERR('handleShowPopOverMsg:: no dlogID', event.id, entityGID, dlogID)
        return

    spaceMgr = event.controller.owner
    if entityGID == -1:
        for pid in spaceMgr.players:
            _ent = KBEngine.entities.get(pid)
            if _ent and _ent.isReal():
                pass
        return

    gidTag = 'gid_{}'.format(entityGID)

    for _ent in spaceMgr.listEntitiesByTag(gidTag):
        _ent._popDialog(dlogID)


def handleDungeonTaskForceComplete(event, srcE, ctx, **referenceArgument):
    taskID = event.fetchArgument('taskID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: dungeon task force complete {}'.format(event.id, taskID))
    for pid in event.controller.owner.players:
        _ent = KBEngine.entities.get(pid)
        _ent.base.forceCompleteTaskNoCond(taskID)


def handleDungeonTaskForceFailed(event, srcE, ctx, **referenceArgument):
    taskID = event.fetchArgument('taskID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: dungeon task force failed {}'.format(event.id, taskID))
    for pid in event.controller.owner.players:
        _ent = KBEngine.entities.get(pid)
        _ent.base.startTaskFailed(taskID, gameconst.TaskNotSuccReasonEnum.DUNGEON_CTRL)


def handleChangeDungeonNPCToBattle(event, srcE, ctx, **referenceArgument):
    npcIDs = event.fetchArgument('npcIDs', 0)
    ifSetBoss = event.fetchArgument('ifSetBoss', False)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: change dungeon NPC to battle state, {}'.format(event.id, npcIDs))
    spaceMgr = event.controller.owner
    for npcID in npcIDs:
        gidTag = 'gid_{}'.format(npcID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if not _ent or not (_ent.IsNpc and _ent.IsCombatUnit):
                gameengine.panicStack('flowController:handleChangeDungeonNPCToBattle:: is not valid CNpc', npcID)
                return
            _ent.setToBattle(ifSetBoss)


def handleChangeDungeonNPCToNeutral(event, srcE, ctx, **referenceArgument):
    npcIDs = event.fetchArgument('npcIDs', 0)
    resetDir = event.fetchArgument('resetDir', True)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: change dungeon NPC to neutral state, {} resetDir={}'.format(event.id, npcIDs, resetDir))
    spaceMgr = event.controller.owner
    for npcID in npcIDs:
        gidTag = 'gid_{}'.format(npcID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if not _ent or not (_ent.IsNpc and _ent.IsCombatUnit):
                gameengine.panicStack('flowController:handleChangeDungeonNPCToNeutral:: is not valid CNpc', npcID)
                return
            _ent.setToNeutral(resetDir=resetDir)


def handleChangeDungeonNPCToFriendly(event, srcE, ctx, **referenceArgument):
    npcIDs = event.fetchArgument('npcIDs', 0)
    resetDir = event.fetchArgument('resetDir', True)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: change dungeon NPC to friend state, {} resetDir={}'.format(event.id, npcIDs, resetDir))
    spaceMgr = event.controller.owner
    for npcID in npcIDs:
        gidTag = 'gid_{}'.format(npcID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if not _ent or not (_ent.IsNpc and _ent.IsCombatUnit):
                gameengine.panicStack('flowController:handleChangeDungeonNPCToFriendly:: is not valid CNpc', npcID)
                return
            _ent.setToFriendly(resetDir=resetDir)


def handleChangeDungeonNPCDialog(event, srcE, ctx, **referenceArgument):
    npcID = event.fetchArgument('npcID', 0)
    dialogID = event.fetchArgument('dialogID', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: change dungeon NPC dialogID, {} {}'.format(event.id, npcID, dialogID))
    spaceMgr = event.controller.owner
    gidTag = 'gid_{}'.format(npcID)

    for _ent in spaceMgr.listEntitiesByTag(gidTag):
        if not _ent or not (_ent.IsNpc and _ent.IsCombatUnit):
            gameengine.panicStack('flowController:handleChangeDungeonNPCToBattle:: is not valid CNpc', npcID)
            return
        _ent.dialogID = dialogID


def handleDungeonAnyPlayerHpTrigger(event, srcE, ctx, **referenceArgument):
    symbol = event.fetchArgument('symbol', 0)
    hpPrt = event.fetchArgument('hpPercent', -1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: after any dungeon player HP condition -> {} {}'.format(
        event.id, symbol, hpPrt))


def handleAddEntityArrowTracker(event, srcE, ctx, **referenceArgument):
    entityGID = event.fetchArgument('entityGID', 0)
    priority = event.fetchArgument('priority', 255)
    triggerType = event.fetchArgument('triggerType', gameconst.ArrowTrackingType.NORMAL)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: add entity arrow tracker. {} {} {}'.format(
        event.id, entityGID, priority, triggerType))

    spaceMgr = event.controller.owner
    gidTag = 'gid_{}'.format(entityGID)
    for _ent in spaceMgr.listEntitiesByTag(gidTag):
        arrowUUID = KBEngine.genUUID64()
        spaceMgr.startEntityCrtPosArrowTracking(arrowUUID, _ent.id, priority, triggerType)


def handleRemoveEntityArrowTracker(event, srcE, ctx, **referenceArgument):
    entityGID = event.fetchArgument('entityGID', 0)
    triggerType = event.fetchArgument('triggerType', gameconst.ArrowTrackingType.NORMAL)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: remove entity arrow tracker. {} {}'.format(
        event.id, entityGID, triggerType))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_ERR("handleRemoveEntityArrowTracker::spaceMgr not found", event, srcE, ctx, referenceArgument)
        return

    spaceMgr.stopArrowTrackingByEntityId(int(entityGID), triggerType)


def handleClearEntityHate(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument('entityGIDs', [])
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: clear entity hate. {}'.format(event.id, entityGIDs))

    spaceMgr = event.controller.owner
    for gid in entityGIDs:
        gidTag = 'gid_{}'.format(gid)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            _ent and _ent.aiController and _ent.aiController.hateDict.clearHate(_ent)


def handleForceSelectEntityTarget(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument('entityGIDs', [])
    positionType = event.fetchArgument('positionType', gameconst.DungeonFlowPlayerChooseEnum.UNKNOWN)
    minRng = event.fetchArgument('minRng', 0)
    iRange = event.fetchArgument('iRange', 0)
    exceptHighestHate = event.fetchArgument('exceptHighestHate', 1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{0}] force select entity target -> '
                '{1}(t={2},iRange={3},minrng={4},exceptHighestHate={5}'.format(
                    event.id, entityGIDs, positionType, iRange, minRng, exceptHighestHate))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleForceSelectEntityTarget:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if not _ent.aiController:
                continue
            _params = {
                "monsterEntity": _ent,
                "exceptHighestHate": exceptHighestHate
            }

            if minRng:
                _params["range_min_"] = minRng

            if iRange:
                _params["range_"] = iRange

            r, rs, tEnts_ = _handlePlayerChooseType(positionType, spaceMgr, **_params)
            if not r or not tEnts_:
                LOG_WARN('FlowController::handleForceSelectEntityTarget: ', rs, positionType)
                continue

            tEnt_ = tEnts_[0]
            _ent.aiController.regrTempTargetId(tEnt_.id)


def handleDungeonTrapBeTriggered(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument('entityGIDs', [])
    LOG_WARN('DUNGEON FLOW -- EVENT[{}] dungeon trap be triggered {}'.format(
        event.id, entityGIDs))


def handleDungeonTeleportToPosition(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument('entityGIDs', [])
    pos = event.fetchArgument('pos', None)
    _dir = event.fetchArgument('dir', None)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}] dungeon teleport to position {} {}'.format(
        event.id, pos, _dir))

    if not utils.checkPosValid(pos):
        LOG_ERR('FlowController::handleForceSelectEntityTarget:no pos', entityGIDs, pos, _dir)
        return

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleForceSelectEntityTarget:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            _ent and _ent.telToPos(pos, toDir=_dir if _dir is not None else _ent.direction)


def handleDungeonChangeEntityForce(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument('entityGIDs', [])
    force = event.fetchArgument('force', 0)
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] dungoen change entity force {} {}".format(
        event.id, entityGIDs, force))

    if force not in gameconst.ForceTypeEnum.dunForce:
        LOG_WARN('FlowController::handleDungeonChangeEntityForce:force error', force)
        return

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleDungeonChangeEntityForce:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if force == gameconst.ForceTypeEnum.Monster:
                _ent.setToBattle()
            elif force in (gameconst.ForceTypeEnum.NPC, gameconst.ForceTypeEnum.Neutrality):
                _ent.setToNeutral()
            elif force == gameconst.ForceTypeEnum.Friend:
                _ent.setToFriendly()


def handleChangeSpaceVar(event, srcE, ctx, **referenceArgument):
    varID = event.fetchArgument('varID', 0)
    formula_ = event.fetchArgument('formula', '')
    paramVarIDs = event.fetchArgument('paramVarIDs', [])
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] change dungeon space var {} = {}({})".format(
        event.id, varID, formula_, paramVarIDs))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleChangeSpaceVar:spaceMgr not found')
        return

    mParams = {}
    for _i_varID in paramVarIDs:
        _i_varVal = spaceMgr.getSpaceVar(_i_varID)
        if _i_varVal is not None:
            mParams[_i_varID] = _i_varVal

    # calc new val
    formula_func = F_GFD.datas[int(formula_)]['serverFormula']
    m_varVal = formula_func(mParams)

    _opUUID = KBEngine.genUUID64()
    _src = gameconst.VarChangeSrcEnum.VAR_SRC_SPACE
    _desc = "flowController -> handleChangeSpaceVar {} {} {}, spaceNo={}".format(
        varID, formula_, paramVarIDs, spaceMgr.spaceNo)
    spaceMgr.setSpaceVar(varID, m_varVal, _opUUID, _src, _desc)


def handleDungeonKillEntities(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument("entityGIDs", [])
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] dungoen kill entities force {}".format(
        event.id, entityGIDs))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleDungeonKillEntities:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            _ent.killSelf(gameconst.SourceType.SrcTpDefault)


def handleDungeonEntityImmuneDeath(event, srcE, ctx, **referenceArgument):
    entityGID = event.fetchArgument("entityGID", 0)
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] dungeon entity immune death {}".format(
        event.id, entityGID))


def handleIfAllSelectEntityImmuneDeath(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument("entityGIDs", [])
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] if all select entity immune death {}".format(
        event.id, entityGIDs))


def handleCreateDugneonTeleporter(event, srcE, ctx, **referenceArgument):
    creationGID = event.fetchArgument("creationGID", 0)
    targetEntityGID = event.fetchArgument("targetEntityGID", 0)
    trapRange = event.fetchArgument("trapRange", 0)
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] create dungeon teleporter {} (te={},iRange={})".format(
        event.id, creationGID, targetEntityGID, trapRange))


def handleStopAiTick(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument("entityGIDs", [])
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] dungoen stop ai tick {}".format(
        event.id, entityGIDs))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleStopAiTick:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if not _ent.thinkTimer:
                LOG_WARN("FlowController::handleStopAiTick:skip entity AItick already stopped", entityGID, _ent.id)
                continue
            _ent.stopByFuben = True
            _ent.stopThink()


def handleStartAiTick(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument("entityGIDs", [])
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] dungoen start ai tick {}".format(
        event.id, entityGIDs))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleStartAiTick:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if _ent.thinkTimer:
                LOG_WARN("FlowController::handleStartAiTick:skip entity already thinking", entityGID, _ent.id)
                continue
            _ent.stopByFuben = False
            _ent.startThink()


def handleEntityStartRouting(event, srcE, ctx, **refParams):
    entityGID = event.fetchArgument('entityGID')
    pathID = event.fetchArgument('pathID')
    speed = event.fetchArgument('speed')
    moveAni = event.fetchArgument('moveAni', gameconst.DunFlowMoveAniEnum.RUN01)
    escortDistance = event.fetchArgument('escortDistance')
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] entity start routing -> {} {} {} {} {}".format(
        event.id, pathID, pathID, speed, moveAni, escortDistance))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::buildEntityStartRouting:spaceMgr not found')
        return

    gidTag = 'gid_{}'.format(entityGID)
    for _ent in spaceMgr.listEntitiesByTag(gidTag):
        if not _ent:
            continue

        userData = {}

        _newBaseSpeed = _newAdjSpeed = 0.0
        _newMoveAni = _ent.moveAni

        # region moveAni
        if moveAni != gameconst.DunFlowMoveAniEnum.DEFAULT:
            _newMoveAni = moveAni
        # endregion

        # region speed
        if speed > 0:
            _newBaseSpeed = speed

        elif speed == 0:
            if _ent.IsNpc:
                _d = NPC_DATA.datas.get(_ent.npcId, {})
            else:
                _d = CBD.datas.get(_ent.creepbaseId, {})
            if moveAni == gameconst.DunFlowMoveAniEnum.RUN01:
                _newBaseSpeed = _d.get('baseSpeed', 0.0)

            elif moveAni == gameconst.DunFlowMoveAniEnum.RUN02:
                _newBaseSpeed, _newAdjSpeed = _d.get('baseSpeed', 0.0), _d.get('adjSpeed', 0.0)

        if _newBaseSpeed > 0:
            userData['baseSpeed'] = _newBaseSpeed
        if _newAdjSpeed > 0:
            userData['adjSpeed'] = _newAdjSpeed
        if _newMoveAni != _ent.moveAni:
            userData['moveAni'] = _newMoveAni

        if escortDistance > 0:
            escortLeaveDistance = round(escortDistance * 1.5) + 1
        else:
            escortLeaveDistance = 0

        _ret = _ent.setRoute(pathID, escortDistance=escortDistance,
                                    escortLeaveDistance=escortLeaveDistance,
                                    speedOverwrite=userData)
        if not _ret:
            LOG_WARN("handleEntityStartRouting:: set route failed")


def handleEntityRouteFinished(event, srcE, ctx, **refParams):
    entityGID = event.fetchArgument('entityGID')
    pathID = event.fetchArgument('pathID')
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] after entity route finished -> {} {}".format(
        event.id, entityGID, pathID))


def handleEntityRoutingMissingEscort(event, srcE, ctx, **refParams):
    entityGID = event.fetchArgument('entityGID')
    pathID = event.fetchArgument('pathID')
    infLoop = event.fetchArgument('infLoop')
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] after entity routing missing rescort -> {} {} {}".format(
        event.id, entityGID, pathID, infLoop))


def handleAnyPlayerCinemaPlayEnded(event, srcE, ctx, **referenceArgument):
    LOG_WARN("DUNGEON FLOW -- EVENT[{}] if any player cinema play ended".format(event.id))


def handleCastCinemaPlay(event, srcE, ctx, **refParams):
    cinemaPlayID = event.fetchArgument('cinemaPlayID', -1)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: cinema play:{}'.format(event.id, cinemaPlayID))
    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('handleCastCinemaPlay:spaceMgr not found')
        return
    spaceMgr.cinemaPlay(cinemaPlayID)

def handleDungeonStopCurTrans(event, srcE, ctx, **referenceArgument):
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: all player stop current transform'.format(event.id))
    spaceMgr = event.controller.owner
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR('flowController::handleDungeonStopCurTrans::player _ent not found Avatar({})'.format(pid))
            continue

def handleDungeonTriggerGuide(event, srcE, ctx, **referenceArgument):
    triggerGuideId = event.fetchArgument('triggerGuideId')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: all player trigger guide -> {}'.format(event.id, triggerGuideId))
    spaceMgr = event.controller.owner
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR('flowController::handleDungeonTriggerGuide::player _ent not found Avatar({})'.format(pid))
            continue

        _ent.client.onTriggerGuide(triggerGuideId)

def handleNewTransPetStart(event, srcE, ctx, **referenceArgument):
    transPetId = event.fetchArgument('transPetId')
    triggerGuideId = event.fetchArgument('triggerGuideId')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: all player new transPet start -> {}, {}'.format(event.id, transPetId, triggerGuideId))
    spaceMgr = event.controller.owner
    spaceMgr.transPetId = transPetId
    spaceMgr.triggerGuideId = triggerGuideId
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR('flowController::handleNewTransPetStart::player _ent not found Avatar({})'.format(pid))
            continue
        _ent.client.newTransPetStart(transPetId, triggerGuideId)

def handleNewTransPetEnd(event, srcE, ctx, **referenceArgument):
    transPetId = event.fetchArgument('transPetId')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: all player new transPet end -> {}'.format(event.id, transPetId))
    spaceMgr = event.controller.owner
    spaceMgr.transPetId = 0
    spaceMgr.triggerGuideId = 0
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR('flowController::handleNewTransPetEnd::player _ent not found Avatar({})'.format(pid))
            continue
        _ent.client.newTransPetEnd(transPetId)

def handleDungeonPlayerForceTrans(event, srcE, ctx, **referenceArgument):
    transPetId = event.fetchArgument('transPetId')
    chooseType = event.fetchArgument('chooseType')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: player force trans -> {}, {}'.format(event.id, transPetId, chooseType))
    spaceMgr = event.controller.owner
    if chooseType == gameconst.PlayerForceTransType.ALL_PLAYERS:
        for pid in spaceMgr.players:
            _ent = KBEngine.entities.get(pid)
            if not _ent:
                LOG_ERR('flowController::handleDungeonPlayerForceTrans::player _ent not found Avatar({})'.format(pid))
                continue
            _ent.transformMonster(transPetId, True)
    elif chooseType == gameconst.PlayerForceTransType.RAND_PLAYER:
        pid = random.choice( spaceMgr.players)
        _ent = KBEngine.entities.get(pid)
        if not _ent:
            LOG_ERR('flowController::handleDungeonPlayerForceTrans::player _ent not found Avatar({})'.format(pid))
            return
        _ent.transformMonster(transPetId, True)


def handleChangeAllPlayerCameraStatus(event, srcE, ctx, **referenceArgument):
    cameraId = event.fetchArgument('cameraId', 0)
    spaceMgr = event.controller.owner

    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: change all player camera status -> {}'.format(event.id, cameraId))
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if _ent and _ent.isReal():
            _ent.client.changeSelfCameraStatus(cameraId)


def handleChangeAllPlayerCameraLookPos(event, srcE, ctx, **referenceArgument):
    entityGID = event.fetchArgument('entityGID', 0)
    spaceMgr = event.controller.owner

    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: change all player camera lookPos -> {}'.format(event.id, entityGID))

    dungeonNo = referenceArgument['dungeonNo']
    dunAllDatas = utils.getDunModuleData(dungeonNo)
    _dunData = dunAllDatas[str(entityGID)]

    entityPos = (_dunData['PosX'], _dunData['PosY'], _dunData['PosZ'])
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if _ent and _ent.isReal():
            _ent.client.changeSelfCameraLookPos(entityPos)

def handleRevertAllPlayerCameraStatus(event, srcE, ctx, **referenceArgument):
    spaceMgr = event.controller.owner

    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: revert all player camera status'.format(event.id))
    for pid in spaceMgr.players:
        _ent = KBEngine.entities.get(pid)
        if _ent and _ent.isReal():
            _ent.client.revertSelfCameraStatus()

def handleChangeNPCSelectableStatus(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument('entityGIDs', [])
    isSelectable = event.fetchArgument('isSelectable', False)

    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: change npc selectable status -> {} {}'.format(event.id, entityGIDs, isSelectable))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleChangeNPCSelectableStatus:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if not _ent.IsNpc:
                continue
            _ent.isSelectable = isSelectable


def handleChangeEntityDirection(event, srcE, ctx, **referenceArgument):
    entityGIDs = event.fetchArgument('entityGIDs', [])
    _dir = event.fetchArgument('_dir', None)

    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: change entities direction -> {} {}'.format(event.id, entityGIDs, _dir))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleChangeEntityDirection:spaceMgr not found')
        return

    for entityGID in entityGIDs:
        gidTag = 'gid_{}'.format(entityGID)
        for _ent in spaceMgr.listEntitiesByTag(gidTag):
            if _dir is not None:
                _ent.direction = (0.0, 0.0, _dir * math.pi / 180)


def handleTimeFreezeStart(event, srcE, ctx, **referenceArgument):
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: dungeon time freeze start -> {}'.format(event.id, utils.curTS()))
    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleTimeFreezeStart:spaceMgr not found')
        return

    spaceMgr.startTimeFreeze()


def handleTimeFreezeEnd(event, srcE, ctx, **referenceArgument):
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: dungeon time freeze end -> {}'.format(event.id, utils.curTS()))
    spaceMgr = event.controller.owner
    if not spaceMgr:
        LOG_WARN('FlowController::handleTimeFreezeEnd:spaceMgr not found')
        return

    spaceMgr.stopTimeFreeze()

def handleReleaseAppearanceNPC(event, srcE, ctx, **refParams):
    npcId = event.fetchArgument('npcId')
    randomType = event.fetchArgument('randomType')
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: release npc -> {}:{}'.format(event.id, npcId, randomType))

def handleReleaseRebornPos(event, srcE, ctx, **refParams):
    rebornPosGIDs = event.fetchArgument('rebornPosGIDs', [])
    rebornPosNum = event.fetchArgument('rebornPosNum', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: release reborn point -> {}:{}'.format(event.id, rebornPosGIDs, rebornPosNum))

def handleRecycleRebornPos(event, srcE, ctx, **refParams):
    rebornPosGIDs = event.fetchArgument('rebornPosGIDs', [])
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: recycle reborn point -> {}'.format(event.id, rebornPosGIDs))
    _handleRecycleInDungeon(event, rebornPosGIDs)

def handleTransferToTheDesignatedMap(event, srcE, ctx, **refParams):
    lineNo = event.fetchArgument('lineNo', [])
    pos = event.fetchArgument('pos', [])
    angle = event.fetchArgument('angle', [])
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: transfer to the designated map -> {}'.format(event.id, lineNo, pos))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        return

    spaceMgr.syncPlayer(lambda boxCell: boxCell.transferToTheDesignatedMap(lineNo, pos, angle))


def handleNotifyStartBattleCD(event, srcE, ctx, **refParams):
    dungeonNo = event.fetchArgument('dungeonNo', 0)
    spaceNo = event.fetchArgument('spaceNo', 0)
    cdTime = event.fetchArgument('cdTime', 0)

    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: notify start battle cd -> space:{} dungeon:{} cdTime:{}'.format(event.id, spaceNo, dungeonNo, cdTime))

    spaceMgr = event.controller.owner
    if not spaceMgr:
        return
    
    spaceMgr.doDungeonStartBattleCD(spaceNo, dungeonNo, cdTime)

def handleCreateBreakAwayStuckPos(event, srcE, ctx, **refParams):
    entityId = event.fetchArgument('entityId', 0)
    eneityNum = event.fetchArgument('eneityNum', 0)
    LOG_WARN('DUNGEON FLOW -- EVENT[{}]: create break away stuck pos -> {}:{}'.format(event.id, entityId, eneityNum))

    spaceMgr = event.controller.owner
    dungeonNo = formula.parseDungeonNoBySpaceNo(spaceMgr.spaceNo)
    if len(entityId) == 0:
        LOG_ERR('handleCreateBreakAwayStuckPos:: no entityId', spaceMgr.spaceNo, dungeonNo, event.id, entityId, eneityNum)
        return

    dunAllDatas = utils.getDunModuleData(dungeonNo)
    entityData = dunAllDatas.get(str(entityId[0]), {})
    if entityData:
        spaceMgr.breakStuckPos = (entityData['PosX'], entityData['PosY'], entityData['PosZ'])
        spaceMgr.breakStuckDir = entityData['Dir']



    
