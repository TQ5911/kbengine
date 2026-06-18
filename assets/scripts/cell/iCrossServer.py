# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import collections

import gameconst
import gametimer
import formula
import utils

import AvatarScores
import dungeonSrc

CrossServerWaitingClientInitTuple = collections.namedtuple(
    "CrossServerWaitingClientInitTuple", ("reasonId", "reasonArgs"),
    defaults = (gameconst.CrossServerWaitingClientInitTuple.DEFAULT, ())
)

class ICrossServer(object):
    CROSSSERVER_TIMEOUT = 10

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
                                 CrossServerWaitingClientInitTuple())
        return self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTuple)

    @crossServerWaitingClientInitTuple.setter
    def crossServerWaitingClientInitTuple(self, newVal: crossServerWaitingClientInitTuple):
        self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerWaitingClientInitTuple, newVal)

    def setCrossServerWaitingClientInitReason(self, reasonId, reasonArgs=None, timeout=-1):
        self.crossServerWaitingClientInitTuple = CrossServerWaitingClientInitTuple(reasonId, reasonArgs or ())
        if timeout <= 0:
            # NOTE(QZZ)(CROSS_SERVER): 经验时间， 需要尽量保证在正常情况下客户端在该时间内loading完数据并回调initClientOnCell
            timeout = 40

        self.crossServerWaitingClientInitTimerId = self.asyncCallbackAfter(
            timeout, gametimer.TIMER_TAG_CROSS_SERVER_WAITING_CLIENT_INIT
        ).handleCrossServerWaitingClientInitReasonTimeout(timeout)

    def resetCrossServerWaitingClientInitReason(self):
        self.crossServerWaitingClientInitTuple = CrossServerWaitingClientInitTuple()
        if self.crossServerWaitingClientInitTimerId > 0:
            self.cancelTimerCB(self.crossServerWaitingClientInitTimerId,
                                 gametimer.TIMER_TAG_CROSS_SERVER_WAITING_CLIENT_INIT)
        self.crossServerWaitingClientInitTimerId = 0

    def handleCrossServerWaitingClientInitReasonTimeout(self, timeout):
        _crossServerWaitingClientInitTuple = self.crossServerWaitingClientInitTuple
        LOG_ERR("handleCrossServerWaitingClientInitReasonTimeout::", timeout, _crossServerWaitingClientInitTuple)
        self.crossServerWaitingClientInitTimerId = 0
        self.handleCrossServerWaitingClientInitReason()

    def handleCrossServerWaitingClientInitReason(self):
        _crossServerWaitingClientInitTuple = self.crossServerWaitingClientInitTuple
        LOG_INFO("handleCrossServerWaitingClientInitReason::", _crossServerWaitingClientInitTuple)

        if _crossServerWaitingClientInitTuple.reasonId == gameconst.CrossServerWaitingClientInitTuple.BACKSELECTCHARACTER:
            self.resetCrossServerWaitingClientInitReason()
            self.base.backSelectCharacterBase(True)

        elif _crossServerWaitingClientInitTuple.reasonId == gameconst.CrossServerWaitingClientInitTuple.OFFLINE:
            _reason, *_ = _crossServerWaitingClientInitTuple.reasonArgs
            self.resetCrossServerWaitingClientInitReason()
            self._offline(_reason)

        else:
            self.resetCrossServerWaitingClientInitReason()

    def __init__(self):
        pass

    def putCrossServerMethodSyncToLocalServer(self, fnname, args=None):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell, dict())
        _tempDict = self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell)
        _tempDict.setdefault(fnname, collections.deque()).append(args)

    def popleftCrossServerMethodSyncToLocalServer(self, fnname):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell, dict())
        _tempDict = self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerCell)
        _fnqueue = _tempDict.setdefault(fnname, collections.deque())
        if not _fnqueue:
            return ()
        return _fnqueue.popleft()

    @property
    def isCrossServer(self):
        return self.cellCrossServerState not in (gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER, gameconst.CrossServerState.ENUM_GOTO_CROSS_SERVER)

    @property
    def isCrossServerInOtherServer(self):
        return self.isCrossServer and not self.isInLocalServer

    @property
    def isCrossServerInLocalServer(self):
        return self.isCrossServer and self.isInLocalServer

    def onCrossServerStateChanged(self, state):
        LOG_INFO("onCrossServerStateChanged", state)
        if self.cellCrossServerState != state:
            isCrossServerStart = self.cellCrossServerState == gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER
            isCrossServerEnd = state == gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER
            if isCrossServerStart:
                for e in self.getWitnessesWithHide():
                    e and e.onCrossServerStart(self)

            if isCrossServerEnd:
                for e in self.getWitnessesWithHide():
                    e and e.onCrossServerEnd(self)

            self.cellCrossServerState = state

    # LocalServer
    def crossServerSyncOtherInitedDataFromLocalServerCell(self, crossData):
        LOG_WARN("crossServerSyncOtherInitedDataFromLocalServerCell::", crossData)
        cellInitData = dict(
            scoresInfo=AvatarScores.avatarScoresInstance.getDictFromObj(self.scoresInfo),
            totalScore=self.totalScore
        )
        self.base.onCrossServerSyncOtherInitedDataFromLocalServer(crossData, cellInitData)

    # CrossServer
    def onCrossServerSyncOtherInitedDataToCrossServerCell(self, crossData, cellInitData):
        LOG_WARN("onCrossServerSyncOtherInitedDataToCrossServerCell::", crossData, cellInitData)
        self.scoresInfo = AvatarScores.avatarScoresInstance.createObjFromDict(cellInitData["scoresInfo"])
        self.totalScore = cellInitData["totalScore"]
        self.onAllAvatarScoreBeInited()

    # CrossServer
    def syncMethodCallToLocalServerCell(self, fnname, fnargs):
        LOG_DBG("syncMethodCallToLocalServerCell::", fnname, fnargs)
        if self.isCrossServerInOtherServer:
            self.base.syncMethodCallToLocalServerCell(fnname, fnargs)
    
    def beSyncMethodCallFromCrossServerCell(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromCrossServerCell::", fnname, fnargs)
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
        self.applyLeaveTeam(self.id)
        self.leaveRaid(self.id)

    def onCrossServerSuc(self, reasonNo):
        LOG_INFO("onCrossServerSuc::", reasonNo)
        # 【【跨服战场】在进入跨服前需要先退出一些临时的场景（比如副本、帮战分线）】
