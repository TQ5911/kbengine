# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst
import utils

import flowController


class IFlowController(object):

    def flowCtrlIsTaskCompleteCallback(self, state, taskId, eid, expect=gameconst.TaskStat.TASK_STAT_UNKNOWN, checkOnce=False):
        """base(impTask).isTaskComplete 回调"""
        # LOG_ERR("flowCtrlIsTaskCompleteCallback::", state, taskId, eid, expect, checkOnce)
        # fix inprogress
        if state in (gameconst.TaskStat.TASK_STAT_RUNNING, gameconst.TaskStat.TASK_STAT_FINISHED):
            LOG_IFO("flowCtrlIsTaskCompleteCallback:: fixed inprogress callback state", state, taskId, eid, expect, checkOnce)
            state = gameconst.TaskStat.TASK_STAT_RUNNING

        if state != expect:
            if checkOnce:
                spaceMgr = self.spaceMgr
                if spaceMgr and spaceMgr.flowController:
                    if state != gameconst.TaskStat.TASK_STAT_SUBMITTED:
                        spaceMgr.flowController.cancelTaskCompleteTriggerEvents(taskId, (eid, ))
                    if state != gameconst.TaskStat.TASK_STAT_FAILED:
                        spaceMgr.flowController.cancelTaskFailedTriggerEvents(taskId, (eid, ))
                    if state != gameconst.TaskStat.TASK_STAT_RUNNING:
                        spaceMgr.flowController.cancelTaskInProgressTriggerEvents(taskId, (eid, ))
            return

        if state == gameconst.TaskStat.TASK_STAT_SUBMITTED:
            self.flowCtrlOnTaskComplete(taskId)
        elif state == gameconst.TaskStat.TASK_STAT_FAILED:
            self.flowCtrlOnTaskFailed(taskId)
        elif state == gameconst.TaskStat.TASK_STAT_RUNNING:
            self.flowCtrlOnTaskInProgress(taskId)
        else:
            LOG_WARN("flowCtrlIsTaskCompleteCallback::unhandled stat", state, taskId, eid, expect, checkOnce)

    def flowCtrlOnTaskComplete(self, taskId):
        """任务完成时向controller汇报, 玩家实体调用"""
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onTaskComplete(taskId)

    def flowCtrlOnTaskFailed(self, taskId):
        """任务完成时向controller汇报, 玩家实体调用"""
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onTaskFailed(taskId)

    def flowCtrlOnTaskInProgress(self, taskId):
        """任务进行时向controller汇报, 玩家实体调用"""
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onTaskInProgress(taskId)

    def flowCtrlDungeonMonsterReleaseComplete(self, monsterGIDs):
        """释放怪物完成后向controller汇报, spaceMgr调用"""
        if self.flowController:
            self.flowController.onDungeonMonsterReleaseComplete(monsterGIDs)

    def flowCtrlDungeonNPCReleaseComplete(self, npcGIDs):
        if self.flowController:
            self.flowController.onDungeonNPCReleaseComplete(npcGIDs)

    def flowCtrlDungeonCollectionReleaseComplete(self, collGIDs):
        if self.flowController:
            self.flowController.onDungeonCollectionReleaseComplete(collGIDs)

    def flowCtrlDungeonCollectionBeCollected(self, collGID, collectionId):
        if self.flowController:
            self.flowController.onDungeonCollectionBeCollected(collGID)
            self.flowController.onDungeonCollectionBeCollectedUsePrototypeID(collectionId)

    def flowCtrlDungeonAirWallReleaseComplete(self, airWallGIDs):
        if self.flowController:
            self.flowController.onDungeonAirWallReleaseComplete(airWallGIDs)

    def flowCtrlDungeonTeleporterCreatedComplete(self, teleporterGIDs):
        if self.flowController:
            self.flowController.onDungeonTeleporterCreatedComplete(teleporterGIDs)

    def flowCtrlMonsterHpMonitorTrigger(self, monsterGID, oldHp, newHp, fullHp):
        """怪物血量发生变化时向controller汇报, 怪物实体调用"""
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onMonsterHpBeModified(monsterGID, oldHp, newHp, fullHp)

    def flowCtrlMonsterRestNumIncreased(self, monsterGID, newNumber, newTotalNumber):
        """怪物数量增加时向controller汇报, spaceMgr调用"""
        if self.flowController:
            self.flowController.onMonsterRestNumberIncreased(monsterGID, newNumber, newTotalNumber)

    def flowCtrlMonsterRestNumIncreasedByCreepbaseId(self, monsterId, newNumber, newTotalNumber):
        if self.flowController:
            monsterGID = 'cbid{}'.format(monsterId)
            self.flowController.onMonsterRestNumberIncreased(monsterGID, newNumber, newTotalNumber)

    def flowCtrlMonsterRestNumDecreased(self, monsterGID, newNumber, newTotalNumber):
        """怪物数量减少时向Controller汇报, spaceMgr调用"""
        if self.flowController:
            self.flowController.onMonsterRestNumberDecreased(monsterGID, newNumber, newTotalNumber)

    def flowCtrlMonsterRestNumDecreasedByCreepbaseId(self, monsterId, newNumber, newTotalNumber):
        if self.flowController:
            monsterGID = 'cbid{}'.format(monsterId)
            self.flowController.onMonsterRestNumberDecreased(monsterGID, newNumber, newTotalNumber)

    def triggeredFlowControllerRestNumIncreased(self):
        # LOG_IFO("triggeredFlowControllerRestNumIncreased::")
        return self._triggeredFlowControllerRestNumChanged(increased=True)

    def triggeredFlowControllerRestNumDecreased(self):
        LOG_DBG("triggeredFlowControllerRestNumDecreased::")
        return self._triggeredFlowControllerRestNumChanged(decreased=True)

    def _triggeredFlowControllerRestNumChanged(self, decreased=False, increased=False):
        spaceMgr = self.spaceMgr
        if not (spaceMgr and spaceMgr.flowController):
            return
        if not self:
            return

        className = self.__class__.__name__
        h, _ = utils.getRealAvatarEntity(self)
        if (h and h.IsAvatar) or not className:
            return

        entTotalNum = 0
        for i in spaceMgr.tagEntities.get(className, []):
            _ent = KBEngine.entities.get(i)
            if not (_ent and not _ent.isDie()):
                continue
            _enth, _ = utils.getRealAvatarEntity(_ent)
            if _enth and _enth.IsAvatar:
                continue
            entTotalNum += 1

        if hasattr(self, 'gameEntityId') and self.gameEntityId:
            gid = utils.parseGidFromGameEntityId(self.gameEntityId)
            gid_tag = 'gid_{}'.format(gid)
            gidLen = 0
            if gid and gid_tag in spaceMgr.tagEntities:
                for i in spaceMgr.tagEntities[gid_tag]:
                    _ent = KBEngine.entities.get(i)
                    if not (_ent and not _ent.isDie()):
                        continue
                    _enth, _ = utils.getRealAvatarEntity(_ent)
                    if _enth and _enth.IsAvatar:
                        continue
                    gidLen += 1
            if decreased:
                spaceMgr.flowCtrlMonsterRestNumDecreased(gid, gidLen, entTotalNum)
            if increased:
                spaceMgr.flowCtrlMonsterRestNumIncreased(gid, gidLen, entTotalNum)

        if hasattr(self, 'creepBaseId') and self.creepBaseId:
            creepIdStr = str(self.creepBaseId)
            cidLen = 0
            if creepIdStr in spaceMgr.tagEntities:
                for i in spaceMgr.tagEntities[creepIdStr]:
                    _ent = KBEngine.entities.get(i)
                    if not (_ent and not _ent.isDie()):
                        continue
                    _enth, _ = utils.getRealAvatarEntity(_ent)
                    if _enth and _enth.IsAvatar:
                        continue
                    cidLen += 1
            if decreased:
                spaceMgr.flowCtrlMonsterRestNumDecreasedByCreepbaseId(creepIdStr, cidLen, entTotalNum)
            if increased:
                spaceMgr.flowCtrlMonsterRestNumIncreasedByCreepbaseId(creepIdStr, cidLen, entTotalNum)

    def flowCtrlDungeonMonsterKillNumIncreased(self, monsterGID, newNumber, newTotalNumber):
        """怪物击杀储量增加时向Controller汇报, spaceMgr调用"""
        if self.flowController:
            self.flowController.onDungeonMonsterKillNumIncreased(monsterGID, newNumber, newTotalNumber)

    def flowCtrlDungeonMonsterKillNumIncreasedByCreepbaseId(self, monsterId, newNumber, newTotalNumber):
        """怪物击杀储量增加时向Controller汇报, spaceMgr调用(使用原型ID判断)"""
        if self.flowController:
            monsterGID = 'cbid{}'.format(monsterId)
            self.flowController.onDungeonMonsterKillNumIncreased(monsterGID, newNumber, newTotalNumber)

    def flowCtrlOnCheckDungeonEntityKillNumber(self, monsterGID, symbol, number, currentKillNum, usePrototypeID, eid, ctx, checkOnce):
        """副本内Entity击杀数量立刻检查回调"""
        if not self.flowController:
            return

        checkResult = gameconst.DungeonFlowCompSym.compare(symbol, currentKillNum, number)
        if not checkResult:
            if checkOnce:
                self.flowController.cancelWaitingTriggerEvents(ctx, (eid, ))
            return

        self.flowController.onCheckDungeonEntityKillNumberTriggered(monsterGID, symbol, number, currentKillNum, usePrototypeID, (eid, ))

    def flowCtrlOnCheckDungeonAllEntityKillNumber(self, symbol, number, currentKillNum, eid, ctx, checkOnce):
        """副本内所有Entity击杀数量立刻检查回调"""
        if not self.flowController:
            return

        checkResult = gameconst.DungeonFlowCompSym.compare(symbol, currentKillNum, number)
        if not checkResult:
            if checkOnce:
                self.flowController.cancelWaitingTriggerEvents(ctx, (eid, ))
            return

        self.flowController.onCheckDungeonEntityKillNumberTriggered(-1, symbol, number, currentKillNum, False, (eid, ))

    def flowCtrlDungeonAlivePlayerIncreased(self, newNumber):
        if self.flowController:
            self.flowController.onDungeonAlivePlayerCountIncreased(newNumber)

    def flowCtrlDungeonPlayerRestNumChanged(self, newNumber):
        if self.flowController:
            self.flowController.onDungeonPlayerRestNumberChanged(newNumber)

    def flowCtrlDungeonAlivePlayerDecreased(self, newNumber):
        if self.flowController:
            self.flowController.onDungeonAlivePlayerDecreased(newNumber)

    def flowCtrlMonsterInBattle(self, monsterGID):
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onMonsterInBattle(monsterGID)

    def flowCtrlMonsterLeaveBattle(self, monsterGID):
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onMonsterLeaveBattle(monsterGID)

    def flowCtrlDunAnyPlayerHpMonitorTrigger(self, oldHp, newHp, fullHp):
        """任一副本内玩家血量变化汇报接口"""
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onDunAnyPlayerHpBeModified(oldHp, newHp, fullHp)

    def flowCtrlOnEntityMoveToFixPos(self, moveUUID, succ):
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onEntityMoveToFixPos(moveUUID, succ)

    def flowCtrlDunEntityimmuneDeathTrigger(self, entityGID):
        """Entity进入濒死状态触发"""
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onDungeonEntityimmuneDeathBeTriggered(entityGID)

    def flowCtrlDungeonValueCheckChangedTrigger(self, varId):
        """副本变量被修改"""
        if self.flowController:
            self.flowController.onDungeonValueCheckChanged(varId)

    def flowCtrlEntityRouteFinished(self, entityGID, pathID):
        """实体完成route寻路"""
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onEntityRouteFinished(entityGID, pathID)
            # global triggerred
            spaceMgr.flowController.onEntityRouteFinished(-1, pathID)
            spaceMgr.flowController.onEntityRouteFinished(entityGID, -1)
            spaceMgr.flowController.onEntityRouteFinished(-1, -1)

    def flowCtrlEntityRoutingMissingEscort(self, entityGID, pathID):
        """实体route过程中玩家距离过远"""
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onEntityRoutingMissingEscort(entityGID, pathID)
            # global triggerred
            spaceMgr.flowController.onEntityRoutingMissingEscort(-1, pathID)
            spaceMgr.flowController.onEntityRoutingMissingEscort(entityGID, -1)
            spaceMgr.flowController.onEntityRoutingMissingEscort(-1, -1)

    def _onAnyPlayerCinemaPlayEndedTimeout(self, cinemaPlayID, eid):
        LOG_IFO("_onAnyPlayerCinemaPlayEndedTimeout::", cinemaPlayID, eid)
        if self.flowController:
            e = self.flowController.getEventByEventId(eid)
            if e and isinstance(e, flowController.AnyPlayerCinemaPlayEndedEvent):
                e.eventCtrlId = 0
            self.flowController.onPlayerCinemaPlayEnded(cinemaPlayID, eids=(eid, ))

    def flowCtrlPlayerCinemaPlayEnded(self, cinemaPlayID):
        spaceMgr = self.spaceMgr
        if spaceMgr and spaceMgr.flowController:
            spaceMgr.flowController.onPlayerCinemaPlayEnded(cinemaPlayID)
            spaceMgr.flowController.onPlayerCinemaPlayEnded(-1)

    def flowCtrrlDungeonEntityReleaseCompleteByEventId(self, flagIds, fromEventId):
        """通用释放Entity事件处理（根据eventId）"""
        if self.flowController:
            self.flowController.onDungeonEntityReleaseCompleteByEventId(flagIds, fromEventId)

    def flowCtrlDungeonRebornPosCreatedComplete(self, rebornPosGIDs):
        if self.flowController:
            self.flowController.onDungeonRebornPosCreatedComplete(rebornPosGIDs)
