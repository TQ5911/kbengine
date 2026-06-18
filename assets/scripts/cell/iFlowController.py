# coding: utf-8
from KBEDebug import *
import KBEngine

import utils
import gameconst

import flowController


class IFlowController(object):

    def flowCtrlIsTaskCompleteCallback(self, state, taskId, eid, expect=gameconst.TaskStatEnum.TASK_STAT_UNKNOWN, checkOnce=False):
        """base(impTask).isTaskComplete 回调"""
        # LOG_ERR("flowCtrlIsTaskCompleteCallback::", state, taskId, eid, expect, checkOnce)
        # fix inprogress
        if state in (gameconst.TaskStatEnum.TASK_STAT_RUNNING, gameconst.TaskStatEnum.TASK_STAT_FINISHED):
            LOG_INFO("flowCtrlIsTaskCompleteCallback:: fixed inprogress callback state", state, taskId, eid, expect, checkOnce)
            state = gameconst.TaskStatEnum.TASK_STAT_RUNNING

        if state != expect:
            if checkOnce:
                spaceMgr = self.spaceMgr
                if spaceMgr and spaceMgr.flowController:
                    if state != gameconst.TaskStatEnum.TASK_STAT_SUBMITTED:
                        spaceMgr.flowController.cancelTaskCompleteTriggerEvents(taskId, (eid, ))
                    if state != gameconst.TaskStatEnum.TASK_STAT_FAILED:
                        spaceMgr.flowController.cancelTaskFailedTriggerEvents(taskId, (eid, ))
                    if state != gameconst.TaskStatEnum.TASK_STAT_RUNNING:
                        spaceMgr.flowController.cancelTaskInProgressTriggerEvents(taskId, (eid, ))
            return

        if state == gameconst.TaskStatEnum.TASK_STAT_SUBMITTED:
            self.flowCtrlOnTaskComplete(taskId)
        elif state == gameconst.TaskStatEnum.TASK_STAT_FAILED:
            self.flowCtrlOnTaskFailed(taskId)
        elif state == gameconst.TaskStatEnum.TASK_STAT_RUNNING:
            self.flowCtrlOnTaskInProgress(taskId)
        else:
            LOG_WARN("flowCtrlIsTaskCompleteCallback::unhandled stat", state, taskId, eid, expect, checkOnce)

    def flowCtrlOnTaskComplete(self, taskId):
        """任务完成时向controller汇报, 玩家实体调用"""
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onTaskComplete(taskId)

    def flowCtrlOnTaskFailed(self, taskId):
        """任务完成时向controller汇报, 玩家实体调用"""
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onTaskFailed(taskId)

    def flowCtrlOnTaskInProgress(self, taskId):
        """任务进行时向controller汇报, 玩家实体调用"""
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onTaskInProgress(taskId)

    def flowCtrlDungeonNPCReleaseComplete(self, npcGIDs):
        if self.flowController:
            self.flowController.onDungeonNPCReleaseComplete(npcGIDs)

    def flowCtrlDungeonMonsterReleaseComplete(self, monsterGIDs):
        """释放怪物完成后向controller汇报, spaceMgr调用"""
        if self.flowController:
            self.flowController.onDungeonMonsterReleaseComplete(monsterGIDs)

    def flowCtrlDungeonCollectionBeCollected(self, collGID, collectionId):
        if self.flowController:
            self.flowController.onDunCollectionBeCollected(collGID)
            self.flowController.onDungeonCollectionBeCollectedUsePrototypeID(collectionId)

    def flowCtrlDungeonCollectionReleaseComplete(self, collGIDs):
        if self.flowController:
            self.flowController.onDungeonCollectionReleaseComplete(collGIDs)

    def flowCtrlDungeonTeleporterCreatedComplete(self, teleporterGIDs):
        if self.flowController:
            self.flowController.onDungeonTeleporterCreatedComplete(teleporterGIDs)

    def flowCtrlDungeonAirWallReleaseComplete(self, airWallGIDs):
        if self.flowController:
            self.flowController.onDungeonAirWallReleaseComplete(airWallGIDs)

    def flowCtrlMonsterHpMonitorTrigger(self, monsterGID, oldHp, newHp, fullHp):
        """怪物血量发生变化时向controller汇报, 怪物实体调用"""
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onMonsterHpBeModified(monsterGID, oldHp, newHp, fullHp)

    def triggeredFlowControllerRestNumIncreased(self):
        return self._triggeredFlowControllerRestNumChanged(increased=True)

    def triggeredFlowControllerRestNumDec(self):
        LOG_DBG("triggeredFlowControllerRestNumDec::")
        return self._triggeredFlowControllerRestNumChanged(decreased=True)

    def _triggeredFlowControllerRestNumChanged(self, decreased=False, increased=False):
        _spaceMgr = self.spaceMgr
        if not (_spaceMgr and _spaceMgr.flowController):
            return
        if not self:
            return

        className = self.__class__.__name__
        h, _ = utils.getRealAvatarEntity(self)
        if (h and h.IsAvatar) or not className:
            return

        if hasattr(self, 'gameEntityId') and self.gameEntityId:
            gid = utils.parseGidFromGameEntityId(self.gameEntityId)
            if increased:
                _spaceMgr.flowController.onMonsterRestNumberIncreased(
                    gid, gameconst.FLOW_REST_MONSTER_TAG_GID, _spaceMgr)
                _spaceMgr.flowController.onMonsterRestNumberIncreased(
                    -1, gameconst.FLOW_REST_MONSTER_TAG_ALL, _spaceMgr)

            if decreased:
                _spaceMgr.flowController.onMonsterRestNumberDecreased(
                    gid, gameconst.FLOW_REST_MONSTER_TAG_GID, _spaceMgr)
                _spaceMgr.flowController.onMonsterRestNumberDecreased(
                    -1, gameconst.FLOW_REST_MONSTER_TAG_ALL, _spaceMgr)

        if hasattr(self, 'creepbaseId') and self.creepbaseId:
            if increased:
                _spaceMgr.flowController.onMonsterRestNumberIncreased(
                    self.creepbaseId, gameconst.FLOW_REST_MONSTER_TAG_CBID, _spaceMgr)

            if decreased:
                _spaceMgr.flowController.onMonsterRestNumberDecreased(
                    self.creepbaseId, gameconst.FLOW_REST_MONSTER_TAG_CBID, _spaceMgr)

    def flowCtrlDungeonMonsterKillNumIncreasedByCreepbaseId(self, monsterId, newNumber, newTotalNumber):
        """怪物击杀储量增加时向Controller汇报, spaceMgr 调用(使用原型ID判断)"""
        if self.flowController:
            _monsterGID = 'cbid{}'.format(monsterId)
            self.flowController.onDunMonsterKillNumIncreased(_monsterGID, newNumber, newTotalNumber)

    def flowCtrlDungeonMonsterKillNumIncreased(self, monsterGID, newNumber, newTotalNumber):
        """怪物击杀储量增加时向Controller汇报, spaceMgr调用"""
        if self.flowController:
            self.flowController.onDunMonsterKillNumIncreased(monsterGID, newNumber, newTotalNumber)

    def flowCtrlOnCheckDungeonEntityKillNumber(self, monsterGID, symbol, number, curKillNum, usePrototypeID, eid, ctx, checkOnce):
        """副本内Entity击杀数量立刻检查回调"""
        if not self.flowController:
            return

        _checkResult = gameconst.DungeonFlowCompSym.compare(symbol, curKillNum, number)
        if not _checkResult:
            if checkOnce:
                self.flowController.cancelWaitingTriggerEvents(ctx, (eid, ))
            return

        self.flowController.onCheckDunEntityKillNumberTriggered(
            monsterGID, symbol, number, curKillNum, usePrototypeID, (eid, ))

    def flowCtrlOnCheckDungeonAllEntityKillNumber(self, symbol, number, curKillNum, eid, ctx, checkOnce):
        """副本内所有Entity击杀数量立刻检查回调"""
        if not self.flowController:
            return

        _checkResult = gameconst.DungeonFlowCompSym.compare(symbol, curKillNum, number)
        if not _checkResult:
            if checkOnce:
                self.flowController.cancelWaitingTriggerEvents(ctx, (eid, ))
            return

        self.flowController.onCheckDunEntityKillNumberTriggered(-1, symbol, number, curKillNum, False, (eid, ))

    def flowCtrlDungeonAlivePlayerIncreased(self, newNumber):
        if self.flowController:
            self.flowController.onDungeonAlivePlayerCountIncreased(newNumber)

    def flowCtrlDungeonAlivePlayerDecreased(self, newNumber):
        if self.flowController:
            self.flowController.onDungeonAlivePlayerDecreased(newNumber)

    def flowCtrlDungeonPlayerRestNumChanged(self, newNumber):
        if self.flowController:
            self.flowController.onDungeonPlayerRestNumberChanged(newNumber)

    def flowCtrlMonsterInBattle(self, monsterGID):
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onMonsterInBattle(monsterGID)

    def flowCtrlMonsterLeaveBattle(self, monsterGID):
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onMonsterLeaveBattle(monsterGID)

    def flowCtrlDunAnyPlayerHpMonitorTrigger(self, oldHp, newHp, fullHp):
        """任一副本内玩家血量变化汇报接口"""
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onDunAnyPlayerHpBeModified(oldHp, newHp, fullHp)

    def flowCtrlOnEntityMoveToFixPos(self, moveUUID, succ):
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onEntityMoveToFixPos(moveUUID, succ)

    def flowCtrlDunEntityimmuneDeathTrigger(self, entityGID):
        """Entity进入濒死状态触发"""
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onDungeonEntityimmuneDeathBeTriggered(entityGID)

    def flowCtrlDungeonValueCheckChangedTrigger(self, varId):
        """副本变量被修改"""
        if self.flowController:
            self.flowController.onDunValueCheckChanged(varId)

    def flowCtrlEntityRouteFinished(self, entityGID, pathID):
        """实体完成route寻路"""
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onEntityRouteFinished(entityGID, pathID)
            # global triggerred
            _spaceMgr.flowController.onEntityRouteFinished(-1, pathID)
            _spaceMgr.flowController.onEntityRouteFinished(entityGID, -1)
            _spaceMgr.flowController.onEntityRouteFinished(-1, -1)

    def flowCtrlEntityRoutingMissingEscort(self, entityGID, pathID):
        """实体route过程中玩家距离过远"""
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onEntityRoutingMissingEscort(entityGID, pathID)
            # global triggerred
            _spaceMgr.flowController.onEntityRoutingMissingEscort(-1, pathID)
            _spaceMgr.flowController.onEntityRoutingMissingEscort(entityGID, -1)
            _spaceMgr.flowController.onEntityRoutingMissingEscort(-1, -1)

    def _onAnyPlayerCinemaPlayEndedTimeout(self, cinemaPlayID, eid):
        LOG_INFO("_onAnyPlayerCinemaPlayEndedTimeout::", cinemaPlayID, eid)
        if self.flowController:
            _e = self.flowController.getEventByEventId(eid)
            if _e and isinstance(_e, flowController.AnyPlayerCinemaPlayEndedEvent):
                _e.eventCtrlId = 0
            self.flowController.onPlayerCinemaPlayEnded(cinemaPlayID, eids=(eid, ))

    def flowCtrlPlayerCinemaPlayEnded(self, cinemaPlayID):
        _spaceMgr = self.spaceMgr
        if _spaceMgr and _spaceMgr.flowController:
            _spaceMgr.flowController.onPlayerCinemaPlayEnded(cinemaPlayID)
            _spaceMgr.flowController.onPlayerCinemaPlayEnded(-1)

    def flowCtrrlDungeonEntityReleaseCompleteByEventId(self, flagIds, fromEventId):
        """通用释放Entity事件处理（根据eventId）"""
        if self.flowController:
            self.flowController.onDunEntityReleaseCompleteByEventId(flagIds, fromEventId)

    def flowCtrlDungeonRebornPosCreatedComplete(self, rebornPosGIDs):
        if self.flowController:
            self.flowController.onDungeonRebornPosCreatedComplete(rebornPosGIDs)
