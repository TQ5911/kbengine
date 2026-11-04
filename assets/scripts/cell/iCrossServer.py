# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import collections
import gameengine
import gameconst
import gametimer
import formula
import utils

import AvatarScores
import dungeonSrc
import conflict_conflict_def as C_C_DD
import const_const as CONST

CrossServerWaitClientInitTuple = collections.namedtuple(
    "CrossServerWaitClientInitTuple", 
    ("reasonId", "reasonArgs"),
    defaults = (gameconst.CrossServerWaitClientInitTuple.DEFAULT, ())
)

class ICrossServer(object):
    @property
    def crossServerWaitingClientInitTimerId(self):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTimerId):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTimerId, 0)
        return self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTimerId)

    @crossServerWaitingClientInitTimerId.setter
    def crossServerWaitingClientInitTimerId(self, newVal: int):
        self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTimerId, int(newVal))

    @property
    def crossServerWaitingClientInitTuple(self):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTuple):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTuple,
                                 CrossServerWaitClientInitTuple())
        return self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTuple)

    @crossServerWaitingClientInitTuple.setter
    def crossServerWaitingClientInitTuple(self, newVal: crossServerWaitingClientInitTuple):
        self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTuple, newVal)

    def setCrossServerWaitingClientInitReason(self, reasonId, reasonArgs=None, timeout=-1):
        self.crossServerWaitingClientInitTuple = CrossServerWaitClientInitTuple(reasonId, reasonArgs or ())
        if timeout <= 0:
            # NOTE(QZZ)(CROSS_SERVER): 经验时间， 需要尽量保证在正常情况下客户端在该时间内loading完数据并回调initClientOnCell
            timeout = 40

        self.crossServerWaitingClientInitTimerId = self.asyncCallbackAfter(
            timeout, gametimer.TIMER_TAG_CROSS_SERVER_WAITING_CLIENT_INIT
        ).handleCrossServerWaitingClientInitReasonTimeout(timeout)

    def resetCrossServerWaitClientInitReason(self):
        self.crossServerWaitingClientInitTuple = CrossServerWaitClientInitTuple()
        if self.crossServerWaitingClientInitTimerId > 0:
            self.cancelTimerCB(self.crossServerWaitingClientInitTimerId,
                                 gametimer.TIMER_TAG_CROSS_SERVER_WAITING_CLIENT_INIT)
        self.crossServerWaitingClientInitTimerId = 0

    def handleCrossServerWaitingClientInitReasonTimeout(self, timeout):
        _crossServerWaitingClientInitTuple = self.crossServerWaitingClientInitTuple
        LOG_INFO("handleCrossServerWaitingClientInitReasonTimeout::", timeout, _crossServerWaitingClientInitTuple)
        self.crossServerWaitingClientInitTimerId = 0
        self.handleCrossServerWaitingClientInitReason()

    def handleCrossServerWaitingClientInitReason(self):
        _crossServerWaitingClientInitTuple = self.crossServerWaitingClientInitTuple
        LOG_INFO("handleCrossServerWaitingClientInitReason::", _crossServerWaitingClientInitTuple)

        if _crossServerWaitingClientInitTuple.reasonId == gameconst.CrossServerWaitClientInitTuple.BACKSELECTCHARACTER:
            self.resetCrossServerWaitClientInitReason()
            self.base.backSelectCharacterBase(True)

        elif _crossServerWaitingClientInitTuple.reasonId == gameconst.CrossServerWaitClientInitTuple.OFFLINE:
            _reason, *_ = _crossServerWaitingClientInitTuple.reasonArgs
            self.resetCrossServerWaitClientInitReason()
            self._offline(_reason)

        else:
            self.resetCrossServerWaitClientInitReason()

    def __init__(self):
        pass

    def popleftCrossServerMethodSyncToLocalServer(self, fnname):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell, dict())
        _tempDic = self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell)
        _fnqueue = _tempDic.setdefault(fnname, collections.deque())
        if not _fnqueue:
            return ()
        return _fnqueue.popleft()

    def putCrossServerMethodSyncToLocalServer(self, fnname, args=None):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell, dict())
        _tempDic = self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell)
        _tempDic.setdefault(fnname, collections.deque()).append(args)

    @property
    def isCrossServerInOtherServer(self):
        return self.isCrossServer and not self.isInLocalServer

    @property
    def isCrossServer(self):
        return self.cellCrossServerState not in (gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER, gameconst.CrossServerState.ENUM_GOTO_CROSS_SERVER)

    @property
    def isCrossServerInLocalServer(self):
        return self.isCrossServer and self.isInLocalServer

    def onCrossServerStateChanged(self, state):
        LOG_INFO("onCrossServerStateChanged", state)
        if self.cellCrossServerState != state:
            isCrossServerStart = self.cellCrossServerState == gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER
            isCrossServerEnd = state == gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER
            if isCrossServerStart:
                for _e in self.getWitnessesWithHide():
                    _e and _e.onCrossServerStart(self)

            if isCrossServerEnd:
                for _e in self.getWitnessesWithHide():
                    _e and _e.onCrossServerEnd(self)

            self.cellCrossServerState = state

    # LocalServer
    def crossServerSyncOtherInitedDataFromLocalServerCell(self, crossData):
        LOG_WARN("crossServerSyncOtherInitedDataFromLocalServerCell::", crossData)
        cellInitData = dict(
            scoresInfo=AvatarScores.avatarScoresInstance.getDictFromObj(self.scoresInfo),
            totalScore=self.totalScore,
            leagueUUID = self.leagueUUID,
            guildDspFlag=self.guildDspFlag,
            guildIcon=self.guildIcon,
        )
        self.base.onCrossServerSyncOtherInitedDataFromLocalServer(crossData, cellInitData)

    # CrossServer
    def onCrossServerSyncOtherInitedDataToCrossServerCell(self, crossData, cellInitData):
        LOG_WARN("onCrossServerSyncOtherInitedDataToCrossServerCell::", cellInitData, crossData)
        self.scoresInfo = AvatarScores.avatarScoresInstance.createObjFromDict(cellInitData["scoresInfo"])
        self.totalScore = cellInitData["totalScore"]
        self.onAllAvatarScoreBeInited()

    # CrossServer
    def syncMethodCallToLocalServerCell(self, fnname, fnargs):
        if self.isCrossServerInOtherServer:
            LOG_DBG("syncMethodCallToLocalServerCell::", fnname, fnargs)
            self.base.syncMethodCallToLocalServerCell(fnname, fnargs)
    
    def beSyncMethodCallFromCrossServerCell(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromCrossServerCell::", fnname, fnargs)
        getattr(self, fnname)(*fnargs)

    # LocalServer
    def syncMethodCallToCrossServerCell(self, fnname, fnargs):
        if self.isCrossServerInLocalServer:
            LOG_DBG("syncMethodCallToCrossServerCell::", fnname, fnargs)
            self.base.syncMethodCallToCrossServerCell(fnname, fnargs)
    
    def beSyncMethodCallFromLocalServerCell(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromLocalServerCell::", fnname, fnargs)
        getattr(self, fnname)(*fnargs)

    def beforeReqCrossServer(self, toServerId, reasonNo):
        LOG_INFO("beforeReqCrossServer::", toServerId, reasonNo)
        self.destroyAllSummon()
        self.destoryAllCreation()
        # NOTE(QZZ)(CROSS_SERVER): 灵兽隐藏, 不销毁
        # self.destoryLingShouOnCell()
        self.removeAllClones()
        self.unsetAllHateRecord(gameconst.UnsetAllHateReason.teleport)

        self.resetUsingSkills(gameconst.ResetSkillReason.ReasonTeleport)
        self.doClearAllTargetTypeCache(True)

        self.selfStopAutoCombat(gameconst.SuspendAutoCombatReasonEnum.Teleport)
        self.endApplyGather(gameconst.CancelGatherReason.CrossServer)
        self.stopPlayEmote(gameconst.StopPlayEmoteReason.CrossServer)

    def onCrossServerSuc(self, reasonNo):
        LOG_INFO("onCrossServerSuc::", reasonNo)
        # 【【跨服战场】在进入跨服前需要先退出一些临时的场景（比如副本、帮战分线）】
        savedBuffDic = {}
        for buffId in list(self.buffMgrDic.keys()):
            buffMap = self.buffMgrDic.get(buffId)
            if not buffMap:
                continue
            for buffSrcKey in list(buffMap.keys()):
                _buffVal = buffMap.get(buffSrcKey)
                if _buffVal.getOfflineKeep(_buffVal.buffId):
                    savedBuffDic.setdefault(buffId, {})[buffSrcKey] = _buffVal
        
        self.syncMethodCallToCrossServerCell('_syncSaveBuffs', (savedBuffDic, ))
        self.syncMethodCallToCrossServerCell('_afterCrossServerSuc', ())

        # 跨服组队副本：迁移已彻底完成（进本流程结束），本服幽灵回城
        # （野外无客户端挂机防被打）；失败仅报错、幽灵留原地，不影响进本/回程
        if reasonNo in (
                gameconst.CrossServerReasonNo.ENTER_CROSS_CRUSADE, 
                gameconst.CrossServerReasonNo.ENTER_CROSS_WORLD, 
                gameconst.CrossServerReasonNo.ENTER_CROSS_CHIEF):
            self.applyCrossGhostReturnCity()

    def _syncSaveBuffs(self, buffMgrDic):
        LOG_DBG('_syncSaveBuffs', buffMgrDic)
        # NOTE(CROSS_SERVER): buff 的 tStartTime 是源服墙钟，跨服迁移耗时可能超过短 buff 的 duration，
        # 到达本进程时它已经过期。若不在此处剔除，initBuff 会先挂 effect 再走 getBuffRemainTime()<=0 分支，
        # 以 RTEnumDefault 而非 RTEnumEndByTime 移除（endByTimeAction 不执行），并刷一条 initBuff error ERROR 日志。
        # getBuffRemainTime(): 永久/非限时 buff 返回 inf，已过期返回 0.0，故 <=0 即「已过期」。
        _dropNum = 0
        for buffId in list(buffMgrDic.keys()):
            buffMap = buffMgrDic.get(buffId)
            if not buffMap:
                buffMgrDic.pop(buffId, None)
                continue
            for buffSrcKey in list(buffMap.keys()):
                _buffVal = buffMap.get(buffSrcKey)
                if _buffVal and _buffVal.getBuffRemainTime() <= 0:
                    buffMap.pop(buffSrcKey, None)
                    _dropNum += 1
            if not buffMap:
                buffMgrDic.pop(buffId, None)
        if _dropNum:
            LOG_INFO('_syncSaveBuffs drop expired buffs', self.id, _dropNum)

        self.buffMgrDic.update(buffMgrDic)

        for buffId in list(self.buffMgrDic.keys()):
            buffMap = self.buffMgrDic.get(buffId)
            if not buffMap:
                continue
            for buffSrcKey in list(buffMap.keys()):
                _buffVal = buffMap.get(buffSrcKey)
                if _buffVal:
                    _buffVal.initBuff(self)
                    _buffVal.onRestored(self)
        self.client.onUpdateBuffs(self.buffMgrDic.getClientData(self))

    def _afterCrossServerSuc(self):
        LOG_INFO('_afterCrossServerSuc')
        self._checkAndAddTeleportProtectionBuff()

    def onAllianceWarStarted(self, datas):
        if self.guildUUID > 0:
            self.client.onAllianceWarStarted(datas)
            LOG_INFO('onAllianceWarStarted ', datas)

    def onAllianceWarEnded(self, datas):
        if self.guildUUID > 0:
            self.client.onAllianceWarEnded(datas)
            LOG_INFO('onAllianceWarEnded ', datas)

    def crossWorldLeave(self):
        self._commonNeedCast(
            C_C_DD.datas.teleportCast,
            gameconst.StateEnum.Teleporting,
            gameconst.CastEnum.teleportAnchor,
            '_crossWorldLeave',
            (),
            CONST.datas['teleportTime'].get("value", gameconst.ANCHOR_CAST_DUR),
            '_crossServerUnlock',
            ()
        )

    def _crossServerUnlock(self):
        LOG_DBG("_crossServerUnlock")
        self.base.onCrossServerUnlock()
        self.syncMethodCallToLocalServerCell('_crossServerUnlock', ())

    def _crossWorldLeave(self):
        LOG_DBG("_crossWorldLeave")
        self.base.onDoLeaveCrossWorld()

    def onLeaveCrossWorld(self):
        LOG_INFO('onLeaveCrossWorld')