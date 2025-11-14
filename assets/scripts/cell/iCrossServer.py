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
    CROSSSERVER_TIMEOUT = 120

    @property
    def crossServerWaitingClientInitTimerId(self):
        if not self.hasTempMiscProp(gameconst.AvatarProps.crossServerWaitingClientInitTimerId):
            self.setTempMiscProp(gameconst.AvatarProps.crossServerWaitingClientInitTimerId, 0)
        return self.getTempMiscProp(gameconst.AvatarProps.crossServerWaitingClientInitTimerId)

    @crossServerWaitingClientInitTimerId.setter
    def crossServerWaitingClientInitTimerId(self, newVal: int):
        self.setTempMiscProp(gameconst.AvatarProps.crossServerWaitingClientInitTimerId, int(newVal))

    @property
    def crossServerWaitingClientInitTuple(self):
        if not self.hasTempMiscProp(gameconst.AvatarProps.crossServerWaitingClientInitTuple):
            self.setTempMiscProp(gameconst.AvatarProps.crossServerWaitingClientInitTuple,
                                 CrossServerWaitingClientInitTuple())
        return self.getTempMiscProp(gameconst.AvatarProps.crossServerWaitingClientInitTuple)

    @crossServerWaitingClientInitTuple.setter
    def crossServerWaitingClientInitTuple(self, newVal: crossServerWaitingClientInitTuple):
        self.setTempMiscProp(gameconst.AvatarProps.crossServerWaitingClientInitTuple, newVal)

    def setCrossServerWaitingClientInitReason(self, reasonId, reasonArgs=None, timeout=-1):
        self.crossServerWaitingClientInitTuple = CrossServerWaitingClientInitTuple(reasonId, reasonArgs or ())
        if timeout <= 0:
            # NOTE(QZZ)(CROSS_SERVER): 经验时间， 需要尽量保证在正常情况下客户端在该时间内loading完数据并回调initClientOnCell
            timeout = 40

        self.crossServerWaitingClientInitTimerId = self.toCallbackAfter(
            timeout, gametimer.TIMER_TAG_CROSS_SERVER_WAITING_CLIENT_INIT
        ).handleCrossServerWaitingClientInitReasonTimeout(timeout)

    def resetCrossServerWaitingClientInitReason(self):
        self.crossServerWaitingClientInitTuple = CrossServerWaitingClientInitTuple()
        if self.crossServerWaitingClientInitTimerId > 0:
            self._cancelCallback(self.crossServerWaitingClientInitTimerId,
                                 gametimer.TIMER_TAG_CROSS_SERVER_WAITING_CLIENT_INIT)
        self.crossServerWaitingClientInitTimerId = 0

    def handleCrossServerWaitingClientInitReasonTimeout(self, timeout):
        _crossServerWaitingClientInitTuple = self.crossServerWaitingClientInitTuple
        ERROR_MSG("handleCrossServerWaitingClientInitReasonTimeout::", timeout, _crossServerWaitingClientInitTuple)
        self.crossServerWaitingClientInitTimerId = 0
        self.handleCrossServerWaitingClientInitReason()

    def handleCrossServerWaitingClientInitReason(self):
        _crossServerWaitingClientInitTuple = self.crossServerWaitingClientInitTuple
        INFO_MSG("handleCrossServerWaitingClientInitReason::", _crossServerWaitingClientInitTuple)

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
        if not self.hasTempMiscProp(gameconst.AvatarProps.crossServerMethodSyncToLocalServerCell):
            self.setTempMiscProp(gameconst.AvatarProps.crossServerMethodSyncToLocalServerCell, dict())
        _tempDict = self.getTempMiscProp(gameconst.AvatarProps.crossServerMethodSyncToLocalServerCell)
        _tempDict.setdefault(fnname, collections.deque()).append(args)

    def popleftCrossServerMethodSyncToLocalServer(self, fnname):
        if not self.hasTempMiscProp(gameconst.AvatarProps.crossServerMethodSyncToLocalServerCell):
            self.setTempMiscProp(gameconst.AvatarProps.crossServerMethodSyncToLocalServerCell, dict())
        _tempDict = self.getTempMiscProp(gameconst.AvatarProps.crossServerMethodSyncToLocalServerCell)
        _fnqueue = _tempDict.setdefault(fnname, collections.deque())
        if not _fnqueue:
            return ()
        return _fnqueue.popleft()

    @property
    def isCrossServer(self):
        return self.cellCrossServerState not in (gameconst.CrossServerState.IN_CURRENT_SERVER, gameconst.CrossServerState.GOTO_CROSS_SERVER)

    @property
    def isCrossServerInOtherServer(self):
        return self.isCrossServer and not self.isInLocalServer

    @property
    def isCrossServerInLocalServer(self):
        return self.isCrossServer and self.isInLocalServer

    def onCrossServerStateChanged(self, state):
        INFO_MSG("onCrossServerStateChanged", state)
        if self.cellCrossServerState != state:
            isCrossServerStart = self.cellCrossServerState == gameconst.CrossServerState.IN_CURRENT_SERVER
            isCrossServerEnd = state == gameconst.CrossServerState.IN_CURRENT_SERVER
            if isCrossServerStart:
                for e in self.getWitnessesWithHide():
                    e and e.onCrossServerStart(self)

            if isCrossServerEnd:
                for e in self.getWitnessesWithHide():
                    e and e.onCrossServerEnd(self)

            self.cellCrossServerState = state

    # LocalServer
    def crossServerSyncOtherInitedDataFromLocalServerCell(self, crossData):
        WARNING_MSG("crossServerSyncOtherInitedDataFromLocalServerCell::", crossData)
        cellInitData = dict(
            scoresInfo=AvatarScores.avatarScoresInstance.getDictFromObj(self.scoresInfo),
            totalScore=self.totalScore
        )
        self.base.onCrossServerSyncOtherInitedDataFromLocalServer(crossData, cellInitData)

    # CrossServer
    def onCrossServerSyncOtherInitedDataToCrossServerCell(self, crossData, cellInitData):
        WARNING_MSG("onCrossServerSyncOtherInitedDataToCrossServerCell::", crossData, cellInitData)
        self.scoresInfo = AvatarScores.avatarScoresInstance.createObjFromDict(cellInitData["scoresInfo"])
        self.totalScore = cellInitData["totalScore"]
        self.onAllAvatarScoreBeInited()

    # CrossServer
    def syncMethodCallToLocalServerCell(self, fnname, fnargs):
        DEBUG_MSG("syncMethodCallToLocalServerCell::", fnname, fnargs)
        if self.isCrossServerInOtherServer:
            self.base.syncMethodCallToLocalServerCell(fnname, fnargs)

    def beforeReqCrossServer(self, toServerId, reasonNo):
        INFO_MSG("beforeReqCrossServer::", toServerId, reasonNo)
        self.destroyAllSummon()
        self.destoryAllCreation()
        # NOTE(QZZ)(CROSS_SERVER): 灵兽隐藏, 不销毁
        # self.destoryLingShouOnCell()
        self.removeAllClones()
        self.unsetAllHateRecord(gameconst.UnsetAllHateReason.teleport)

        self.resetUsingSkills(gameconst.ResetSkillReason.Teleport)
        self.clearAllTargetTypeCache(True)

        # self.suspendFollow(gameconst.SuspendFollowReason.Teleport)
        self.setFollowCaptain(False)
        self.selfStopAutoCombat(gameconst.SuspendAutoCombatReason.Teleport)
        self.endApplyGather(gameconst.CancelGatherReason.CrossServer)
        self.applyLeaveTeam(self.id)
        self.leaveRaid(self.id)

    def onCrossServerSuc(self, reasonNo):
        INFO_MSG("onCrossServerSuc::", reasonNo)
        # 【【跨服战场】在进入跨服前需要先退出一些临时的场景（比如副本、帮战分线）】
