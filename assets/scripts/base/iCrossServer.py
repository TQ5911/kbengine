# coding: utf-8
from KBEDebug import *
import KBEngine

import collections

import LogTrackingMgr
import gameengine
import gameconfig
import gameconst
import gametimer
import utils

import iRouter

import AvatarScores
import cityBattle_config as CBC
import abyss_floor as AB_FD
import formula

class ICrossServer(object):
    CROSSSERVER_TIMEOUT = 10

    def __init__(self):
        self.serverOpenTime = gameconfig.serverOpenTime()

    def putCrossServerMethodSyncToLocalServer(self, funcName, args=None):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase, dict())
        _tempDic = self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase)
        _tempDic.setdefault(funcName, collections.deque()).append(args)

    def popleftCrossServerMethodSyncToLocalServer(self, funcName):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase, dict())
        _tempDic = self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase)
        _fnqueue = _tempDic.setdefault(funcName, collections.deque())
        if not _fnqueue:
            return ()
        return _fnqueue.popleft()

    @property
    def crossServerEntityCall(self):
        _serverId = gameconfig.serverId()
        if not _serverId:
            return
        return iRouter.RemoteServerBoxEntityCall(_serverId, self)

    #客户端当前连的cell
    @property
    def localCrossCell(self):
        return self.localCrossBase.cell

    #当前连接的客户端
    @property
    def localCrossClient(self):
        return self.localCrossBase.client

    #客户端当前连的base
    @property
    def localCrossBase(self):
        if self.isCrossServerInLocalServer:
            _otherSrvAvatarBox = self.otherServerAvatarBox
            if _otherSrvAvatarBox:
                return self.otherServerAvatarBox
            else:
                return utils.Swallower()
        else:
            return self

    #跨服base
    @property
    def crossBase(self):
        if self.isCrossServerInOtherServer:
            return self
        else:
            return self.otherServerAvatarBox


    #本服base
    @property
    def localBase(self):
        if self.isCrossServerInOtherServer:
            return self.otherServerAvatarBox
        else:
            return self

    @property
    def isCrossServer(self):
        return self.crossServerState != gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER

    @property
    def crossServerId(self):
        if not self.otherServerAvatarBox:
            return 0
        return self.otherServerAvatarBox.serverId

    @property
    def isCrossServerInLocalServer(self):
        if self.isCrossServer:
            return not self.accountEntity.isCrossServer
        return False

    @property
    def isCrossServerInOtherServer(self):
        if self.isCrossServer:
            return self.accountEntity.isCrossServer
        return False

    def stopCrossServerHeartbeat(self):
        if self.crossServerHeartbeatTimer:
            self.pyDelTimer(self.crossServerHeartbeatTimer, gametimer.TIMER_CROSS_SERVER_HEARTBEAT)
            self.crossServerHeartbeatTimer = 0
            self.crossServerTickStartTime = 0

    def setCrossServerState(self, state):
        if self.crossServerState != state:
            self.crossServerState = state
            self.cell.onCrossServerStateChanged(state)

    def startCrossServerHeartbeat(self):
        self.stopCrossServerHeartbeat()
        self.crossServerHeartbeatTimer = self.pyAddTimer(1, 120, gametimer.TIMER_CROSS_SERVER_HEARTBEAT)

    def startBagFnvHashCheck(self):
        self.stopBagFnvHashCheck()
        self.fnvFirstOverDict = {}
        self.bagFnvHashCheckTimer = self.pyAddTimer(5, 5, gametimer.TIMER_BAG_FNV_HASH_CHECK)

    def stopBagFnvHashCheck(self):
        if self.bagFnvHashCheckTimer:
            self.pyDelTimer(self.bagFnvHashCheckTimer, gametimer.TIMER_BAG_FNV_HASH_CHECK)
            self.bagFnvHashCheckTimer = 0

    def crossServerHeartbeat(self):
        if not self.otherServerAvatarBox:
            LOG_ERR("crossServerHeartbeat no otherServerAvatarBox")
            self.stopCrossServerHeartbeat()
            self.destroySelf(gameconst.OFFLINE_REASON_END_CROSS_SERVER, False)
            return

        if self.crossServerTickStartTime > 0 and self.crossServerTickBackTime < self.crossServerTickStartTime:
            LOG_WARN("crossServerHeartbeat overTime", self.crossServerTickStartTime, self.crossServerTickBackTime)
            self.stopCrossServerHeartbeat()
            self.destroySelf(gameconst.OFFLINE_REASON_END_CROSS_SERVER, False)
            return

        self.crossServerTickStartTime = utils.curTS()
        self.otherServerAvatarBox.onCrossServerHeartbeat()
        LOG_DBG('[lj]crossServerHeartbeat', self.crossServerTickStartTime, self.crossServerTickBackTime)

    def onCrossServerHeartbeat(self):
        if not self.otherServerAvatarBox:
            LOG_ERR("onCrossServerHeartbeat no otherServerAvatarBox")
            return

        self.otherServerAvatarBox.onCrossServerHeartbeatBack()

    def onCrossServerHeartbeatBack(self):
        self.crossServerTickBackTime = utils.curTS()
        LOG_DBG('[lj]onCrossServerHeartbeatBack', self.crossServerTickBackTime)

    def _beforeReqCrossServer(self):
        self.leaveGuildMics(self.id)

    def reqCrossServer(self, toServerId, reasonNo, callbackComponent, callbackName, args, crossServerToSpaceNo, goBackTime=0, extra=None):
        LOG_INFO("reqGotoServer",toServerId, reasonNo, callbackComponent, callbackName, args, goBackTime, self.crossServerState, crossServerToSpaceNo)
        if self.crossServerState != gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER:
            LOG_ERR("reqCrossServer repeat", self.crossServerState)
            return

        self.cell.beforeReqCrossServer(toServerId, reasonNo)

        self.setCrossServerState(gameconst.CrossServerState.ENUM_GOTO_CROSS_SERVER)
        self.crossServerDict = {
            'crossServerId': toServerId,
            'reasonNo': reasonNo,
            'callbackComponent': callbackComponent,
            'callbackName': callbackName,
            'args': args,
            'goBackTime': goBackTime,
        }
        self.crossServerToSpaceNo = crossServerToSpaceNo
        self.crossServerFromSpaceNo = self.baseSpaceNo

        if extra:
            self.setPersistentMiscProp(gameconst.EntityPropsEnum.crossServerExtra, extra)

        _r = iRouter.RemoteServerStubEntityCall(toServerId, "CrossServerStub")
        _r.onReqCrossServer(self.accountEntity.accountName, reasonNo, self.crossServerEntityCall)
        self.endCrossServerTimerId = self.addTimerCB(
            self.CROSSSERVER_TIMEOUT, 
            '_endCrossServerCB', 
            (),
            gametimer.TIMER_TAG_END_CROSS_SERVER, 
            'endCrossServerTimerId')

    def _endCrossServerCB(self):
        self.setCrossServerState(gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER)
        toServerId = self.crossServerDict['crossServerId']
        _r = iRouter.RemoteServerStubEntityCall(toServerId, "CrossServerStub")
        _r.onEndCrossServer(self.accountEntity.accountName)

    def onCrossServerResp(self, ret, token, reasonNo):
        LOG_INFO("onCrossServerResp", ret, token, reasonNo)
        if ret:
            # 用 fetchMapId 而非 parseLineType：跨服讨伐传的是裸 dungeonNo（副本场景非分线），
            # parseLineType 会得 0 导致客户端预加载落空；对分线空间号（深渊/城战）结果不变
            mapId = formula.fetchMapId(self.crossServerToSpaceNo)
            crossServerId = self.crossServerDict['crossServerId']
            self.crossServerDict['token'] = token
            self.crossServerDict['spaceNo'] = mapId
            self.client.onCrossServerTokenResp(token, mapId, crossServerId)
            LOG_DBG('[lj]onCrossServerResp', token, mapId, crossServerId)

            LogTrackingMgr.LogTrackingMgr.teleport(
                self.gbID,
                self.accountEntity.clientDistinctId,
                self.accountEntity.accountName,
                formula.parseLineType(self.baseSpaceNo),
                mapId,
            )

    def onReqGetAvatarPorperties(self, token, otherServerAccountBox):
        LOG_INFO("onReqGetAvatarPorperties", token, otherServerAccountBox)
        if token != self.crossServerDict.get("token"):
            LOG_ERR("onReqGetAvatarPorperties token error", token, self.crossServerDict.get("token"))
            otherServerAccountBox and otherServerAccountBox.onGetAvatarPorpertiesFail()
            return

        if self.endCrossServerTimerId:
            self.cancelTimerCB(self.endCrossServerTimerId, gametimer.TIMER_TAG_END_CROSS_SERVER)
            self.endCrossServerTimerId = 0

        self.crossServerDict['otherServerAccountBox'] = otherServerAccountBox
        self.addAllPropertiesToStream()

    def onGetAllProperties(self, baseMemoryStream, cellMemoryStream):
        otherServerAccountBox = self.crossServerDict.get('otherServerAccountBox')
        LOG_INFO("onGetAllProperties", otherServerAccountBox, len(baseMemoryStream), len(cellMemoryStream))
        if otherServerAccountBox:
            otherServerAccountBox.onGetAvatarPorpertiesResp(baseMemoryStream, cellMemoryStream)

    def crossServerSuccess(self):
        LOG_INFO("crossServerSuccess")
        if self.otherServerAvatarBox:
            self.otherServerAvatarBox.onCrossServerSuc(self.crossServerEntityCall)

        self.startCrossServerHeartbeat()

    def onCrossServerSuc(self, otherServerAvatarBox):
        LOG_INFO("onCrossServerSuc", otherServerAvatarBox)
        self.startBagFnvHashCheck()
        if self.crossServerState != gameconst.CrossServerState.ENUM_GOTO_CROSS_SERVER:
            LOG_WARN("onCrossServerSuc state is not GOTO_CROSS_SERVER", self.crossServerState)

        self.setCrossServerState(gameconst.CrossServerState.ENUM_IN_CROSS_SERVER)
        self.otherServerAvatarBox = otherServerAvatarBox
        self.crossServerSyncOtherInitedDataFromLocalServer(None)
        if self.endCrossServerTimerId:
            self.cancelTimerCB(self.endCrossServerTimerId, gametimer.TIMER_TAG_END_CROSS_SERVER)
            self.endCrossServerTimerId = 0
        self.disconnect(gameconst.ClientCallChannel.MAIN_CHANNEL)
        self.cell.onCrossServerSuc(self.crossServerDict["reasonNo"])

        self.accountEntity.changeDinghaoLock(False)

    def crossServerCallBack(self, callbackComponent, callbackName, args, extra):
        LOG_INFO("crossServerCallBack", callbackComponent, callbackName, args, extra)
        _crossData = extra.get('crossData')
        _baseInitData = extra.get('baseInitData')
        _cellInitData = extra.get('cellInitData')
        self.onCrossServerSyncOtherInitedDataToCrossServer(_crossData, _baseInitData, _cellInitData)

        if callbackComponent == gameconst.CrossServerCBComponent.ENUM_BASE:
            getattr(self, callbackName)(*args)
        elif callbackComponent == gameconst.CrossServerCBComponent.ENUM_CELL:
            if self.cell:
                getattr(self.cell, callbackName)(*args)

        _goBackTime = extra.get('goBackTime', 0)
        if _goBackTime:
            self.goBackServerTimerId = self.addTimerCB(
                _goBackTime, 
                'gobackServer',
                (
                    gameconst.CrossServerCBComponent.ENUM_NONE, '', ()),
                gametimer.TIMER_TAG_GOBACK_SERVER, 'goBackServerTimerId'
            )

    def gobackServer(self, callbackComponent, callbackName, args):
        LOG_INFO("gobackServer", callbackComponent, callbackName, args)
        if self.goBackServerTimerId:
            self.cancelTimerCB(self.goBackServerTimerId, gametimer.TIMER_TAG_GOBACK_SERVER)
            self.goBackServerTimerId = 0

        if not self.otherServerAvatarBox:
            LOG_ERR("gobackServer has no otherServerAvatarBox")
            return

        self.otherServerAvatarBox.onCrossServerEnd(callbackComponent, callbackName, args)

        #TODO未来如果有多个跨服玩法，需要再配表设计每个玩法goback的场景
        LOG_INFO("gobackServer", self.crossServerFromSpaceNo)
        self.client.onGobackServer(formula.parseLineType(self.crossServerFromSpaceNo))
        gameengine.getGlobalBase('CrossServerStub').onGobackServer(self.accountEntity.accountName)

        self.cell.offline(gameconst.OFFLINE_REASON_END_CROSS_SERVER)
        
        LogTrackingMgr.LogTrackingMgr.teleport(
            self.gbID,
            self.accountEntity.clientDistinctId,
            self.accountEntity.accountName,
            formula.parseLineType(self.crossServerToSpaceNo),
            formula.parseLineType(self.crossServerFromSpaceNo),
        )

    def onCrossServerEnd(self, callbackComponent, callbackName, args):
        LOG_INFO("onCrossServerEnd", callbackComponent, callbackName, args)
        if self.guildBox:
            self.guildBox.getUnionAndEnemyInfo(self.gbID, self)
        self.stopBagFnvHashCheck()
        if self.crossServerState != gameconst.CrossServerState.ENUM_IN_CROSS_SERVER:
            LOG_ERR("onCrossServerSuc state is not IN_CROSS_SERVER", self.crossServerState)
            return

        self.setCrossServerState(gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER)
        self.crossServerDict = {}

        if callbackComponent == gameconst.CrossServerCBComponent.ENUM_BASE:
            getattr(self, callbackName)(*args)
        elif callbackComponent == gameconst.CrossServerCBComponent.ENUM_CELL:
            self.cell and getattr(self.cell, callbackName)(*args)
        
        self.startDestroyCountDown()
        self.accountEntity.changeDinghaoLock(False)

    def onReloginInCrossServerState(self):
        LOG_INFO("onReloginInCrossServerState", self.crossServerDict['crossServerId'], self.crossServerDict['token'])
        r = iRouter.RemoteServerStubEntityCall(self.crossServerDict['crossServerId'], "CrossServerStub")
        r.onCheckCrossServerToken(self.accountEntity.accountName, self.crossServerDict['token'],
                                  self.crossServerEntityCall)

        self.checkCSTokenTimerId = self.addTimerCB(120, '_onCheckCSTokenTimeout', (),
                                                    gametimer.TIMER_TAG_CHECK_CROSS_SERVER_TOKEN, 'checkCSTokenTimerId')

    def _onCheckCSTokenTimeout(self):
        LOG_INFO("_onCheckCSTokenTimeout")
        self.setCrossServerState(gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER)

    def onCheckCrossServerTokenResp(self, ret):
        LOG_INFO("onCheckCrossServerTokenResp", ret, self.isCrossServerInLocalServer)
        if self.checkCSTokenTimerId:
            self.cancelTimerCB(self.checkCSTokenTimerId, gametimer.TIMER_TAG_CHECK_CROSS_SERVER_TOKEN)
            self.checkCSTokenTimerId = 0

        if ret:
            if self.isCrossServerInLocalServer:
                self.client.onCrossServerTokenResp(self.crossServerDict['token'], self.crossServerDict['spaceNo'], self.crossServerDict['crossServerId'])
        else:
            self.setCrossServerState(gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER)

    # localServer
    def crossServerSyncOtherInitedDataFromLocalServer(self, crossData):
        LOG_WARN("crossServerSyncOtherInitedDataFromLocalServer::", crossData)
        self.cell.crossServerSyncOtherInitedDataFromLocalServerCell(crossData)

    # localServer
    def onCrossServerSyncOtherInitedDataFromLocalServer(self, crossData, cellInitData):
        LOG_WARN("onCrossServerSyncOtherInitedDataFromLocalServer::", crossData, cellInitData)
        if self.isCrossServerInLocalServer and self.otherServerAvatarBox:
            baseInitData = dict(
                scoresInfo=AvatarScores.avatarScoresInstance.getDictFromObj(self.baseScoreInfo),
                guildUUID=self.guildUUIDBase,
                guildName=self.guildNameBase,
                serverOpenTime=self.serverOpenTime
            )
            callbackComponent = self.crossServerDict.get('callbackComponent')
            callbackName = self.crossServerDict.get('callbackName')
            args = self.crossServerDict.get('args')
            extra = {
                'goBackTime': self.crossServerDict.get('goBackTime', 0),
                'crossData': crossData,
                'cellInitData': cellInitData,
                'baseInitData': baseInitData,
            }
            self.otherServerAvatarBox.crossServerCallBack(callbackComponent, callbackName, args, extra)

    # CrossServer
    def onCrossServerSyncOtherInitedDataToCrossServer(self, crossData, baseInitData, cellInitData):
        LOG_WARN("onCrossServerSyncOtherInitedDataToCrossServer::", crossData, baseInitData, cellInitData)
        self.scoresInfo = AvatarScores.avatarScoresInstance.createObjFromDict(baseInitData['scoresInfo'])
        self.serverOpenTime = baseInitData['serverOpenTime']
        self.cell.onCrossServerSyncOtherInitedDataToCrossServerCell(crossData, cellInitData)
        self.onSetGuildInfoCross(baseInitData['guildUUID'], baseInitData['guildName'], cellInitData['leagueUUID'], True)
        self.onUpdateUseCoinTimesTicketInfoCross()

    # localServer
    def beSyncMethodCallFromLocalClient(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromLocalClient::", fnname, fnargs)
        getattr(self.client, fnname)(*fnargs)

    # CrossServer
    def syncMethodCallToCrossClient(self, fnname, fnargs):
        LOG_DBG("syncMethodCallToCrossClient::", fnname, fnargs)
        if self.isCrossServerInLocalServer and self.otherServerAvatarBox:
            LOG_DBG("syncMethodCallToCrossClient::", fnname, fnargs)
            self.otherServerAvatarBox.beSyncMethodCallFromLocalClient(fnname, fnargs)

    # localServer
    def beSyncMethodCallFromCrossServerBase(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromCrossServerBase::", fnname, fnargs)
        getattr(self, fnname)(*fnargs)

    # CrossServer
    def syncMethodCallToLocalServerBase(self, fnname, fnargs):
        if self.isCrossServerInOtherServer and self.otherServerAvatarBox:
            LOG_DBG("syncMethodCallToLocalServerBase::", fnname, fnargs)
            self.otherServerAvatarBox.beSyncMethodCallFromCrossServerBase(fnname, fnargs)

    # CrossServer
    def syncMethodCallToCrossServerBase(self, fnname, fnargs):
        if self.isCrossServerInLocalServer and self.otherServerAvatarBox:
            LOG_DBG("syncMethodCallToCrossServerBase::", fnname, fnargs)
            self.otherServerAvatarBox.beSyncMethodCallFromLocalServerBase(fnname, fnargs)
        else:
            # 回传静默失败排查用：跨服期间正常必有镜像 mailbox，缺失即异常
            LOG_WARN('syncMethodCallToCrossServerBase skipped', fnname,
                     self.isCrossServerInLocalServer, bool(self.otherServerAvatarBox), self.gbID)

    # localServer
    def beSyncMethodCallFromLocalServerBase(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromLocalServerBase::", fnname, fnargs)
        getattr(self, fnname)(*fnargs)

    # localServer
    def beSyncMethodCallFromCrossServerCell(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromCrossServerCell::", fnname, fnargs)
        self.cell.beSyncMethodCallFromCrossServerCell(fnname, fnargs)

    # CrossServer
    def syncMethodCallToLocalServerCell(self, fnname, fnargs):
        if self.isCrossServerInOtherServer and self.otherServerAvatarBox:
            LOG_DBG("syncMethodCallToLocalServerCell::", fnname, fnargs)
            self.otherServerAvatarBox.beSyncMethodCallFromCrossServerCell(fnname, fnargs)

    # localServer
    def syncMethodCallToCrossServerCell(self, fnname, fnargs):
        if self.isCrossServerInLocalServer and self.otherServerAvatarBox:
            LOG_DBG("syncMethodCallToCrossServerCell::", fnname, fnargs)
            self.otherServerAvatarBox.beSyncMethodCallFromLocalServerCell(fnname, fnargs)
    
    def beSyncMethodCallFromLocalServerCell(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromLocalServerCell::", fnname, fnargs)
        self.cell.beSyncMethodCallFromLocalServerCell(fnname, fnargs)

    def onPlayerGetExp_localCrossClient(self, src, expVal, realExpVal, chaseExp):
        LOG_INFO("onPlayerGetExp_localCrossClient::", src, expVal, realExpVal, chaseExp)
        self.localCrossClient.onPlayerGetExp(src, expVal, realExpVal, chaseExp)

    def onMessagePre_localCross(self, msgId, args):
        LOG_INFO("onMessagePre_localCross::", msgId, args)
        self.localCrossBase.onMessagePre(msgId, args)

    def onAvatarLevelUp_localCrossClient(self, oldLevel, level):
        LOG_INFO("onAvatarLevelUp_localCrossClient::", oldLevel, level)

    def setCrossGhostReturnSpaceNo(self, citySpaceNo):
        # 本服幽灵已回城（跨服组队副本）：回程落点改为主城，
        # gobackServer 的客户端预加载图/埋点取 crossServerFromSpaceNo
        LOG_INFO("setCrossGhostReturnSpaceNo::", self.gbID, self.crossServerFromSpaceNo, '->', citySpaceNo)
        self.crossServerFromSpaceNo = citySpaceNo

    def onAfterSyncLeagueUUID(self, leagueUUID, guildUUID):
        LOG_INFO("onAfterSyncLeagueUUID::", leagueUUID, guildUUID)
        if leagueUUID > 0:
            gameengine.getGlobalBase('AllianceStub').getUnionList(guildUUID, self)
        gameengine.getGlobalBase('AllianceStub').getEnemyAllianceList(leagueUUID, guildUUID, self)
        
    def getServerOpenTimestamp(self):
        return self.serverOpenTime if self.serverOpenTime else gameconfig.serverOpenTime()