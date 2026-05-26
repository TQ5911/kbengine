# coding: utf-8
from KBEDebug import *
import KBEngine

import collections

import gameengine
import gameconfig
import gameconst
import gametimer
import utils

import iRouter

import AvatarScores
import cityBattle_config as CBC

class ICrossServer(object):
    CROSSSERVER_TIMEOUT = 120

    def __init__(self):
        pass

    def putCrossServerMethodSyncToLocalServer(self, fnname, args=None):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase, dict())
        _tempDict = self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase)
        _tempDict.setdefault(fnname, collections.deque()).append(args)

    def popleftCrossServerMethodSyncToLocalServer(self, fnname):
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase):
            self.setTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase, dict())
        _tempDict = self.getTempMiscProp(gameconst.EntityPropsEnum.crossServerMethodSyncToLocalServerBase)
        _fnqueue = _tempDict.setdefault(fnname, collections.deque())
        if not _fnqueue:
            return ()
        return _fnqueue.popleft()

    @property
    def crossServerEntityCall(self):
        serverId = gameconfig.serverId()
        if not serverId:
            return
        return iRouter.RemoteServerBoxEntityCall(serverId, self)

    #当前连接的客户端
    @property
    def localCrossClient(self):
        return self.localCrossBase.client

    #客户端当前连的cell
    @property
    def localCrossCell(self):
        return self.localCrossBase.cell

    #客户端当前连的base
    @property
    def localCrossBase(self):
        if self.isCrossServerInLocalServer:
            _otherServerAvatarBox = self.otherServerAvatarBox
            if _otherServerAvatarBox:
                return self.otherServerAvatarBox
            else:
                return utils.Swallower()
        else:
            return self

    #本服base
    @property
    def localBase(self):
        if self.isCrossServerInOtherServer:
            return self.otherServerAvatarBox
        else:
            return self

    #跨服base
    @property
    def crossBase(self):
        if self.isCrossServerInOtherServer:
            return self
        else:
            return self.otherServerAvatarBox


    @property
    def crossServerId(self):
        if not self.otherServerAvatarBox:
            return 0
        return self.otherServerAvatarBox.serverId

    @property
    def isCrossServer(self):
        return self.crossServerState != gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER

    @property
    def isCrossServerInOtherServer(self):
        if self.isCrossServer:
            return self.accountEntity.isCrossServer
        return False

    @property
    def isCrossServerInLocalServer(self):
        if self.isCrossServer:
            return not self.accountEntity.isCrossServer
        return False

    def setCrossServerState(self, state):
        if self.crossServerState != state:
            self.crossServerState = state
            self.cell.onCrossServerStateChanged(state)

    def stopCrossServerHeartbeat(self):
        if self.crossServerHeartbeatTimer:
            self.pyDelTimer(self.crossServerHeartbeatTimer, gametimer.CROSS_SERVER_HEARTBEAT_TIMER)
            self.crossServerHeartbeatTimer = 0
            self.crossServerTickStartTime = 0

    def startCrossServerHeartbeat(self):
        self.stopCrossServerHeartbeat()
        self.crossServerHeartbeatTimer = self.pyAddTimer(1, 300, gametimer.CROSS_SERVER_HEARTBEAT_TIMER)

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

    def reqCrossServer(self, toServerId, reasonNo, callbackComponent, callbackName, args, goBackTime=0):
        LOG_INFO("reqGotoServer",toServerId, reasonNo, callbackComponent, callbackName, args, goBackTime, self.crossServerState)
        if self.crossServerState != gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER:
            LOG_ERR("reqCrossServer repeat", self.crossServerState)
            return

        self.cell.beforeReqCrossServer(toServerId, reasonNo)

        self.setCrossServerState(gameconst.CrossServerState.ENUM_GOTO_CROSS_SERVER)
        self.crossServerDic = {
            'crossServerId': toServerId,
            'reasonNo': reasonNo,
            'callbackComponent': callbackComponent,
            'callbackName': callbackName,
            'args': args,
            'goBackTime': goBackTime
        }

        r = iRouter.RemoteServerStubEntityCall(toServerId, "CrossServerStub")
        r.onReqCrossServer(self.accountEntity.accountName, reasonNo, self.crossServerEntityCall)
        self.endCrossServerTimerId = self.addTimerCB(self.CROSSSERVER_TIMEOUT, '_endCrossServer', (),
                       gametimer.TIMER_TAG_END_CROSS_SERVER, 'endCrossServerTimerId')

    def _endCrossServer(self):
        self.setCrossServerState(gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER)
        toServerId = self.crossServerDic['crossServerId']
        r = iRouter.RemoteServerStubEntityCall(toServerId, "CrossServerStub")
        r.onEndCrossServer(self.accountEntity.accountName)

    def onCrossServerResp(self, ret, token, reasonNo):
        LOG_INFO("onCrossServerResp", ret, token, reasonNo)
        if ret:
            spaceNo = 0
            if reasonNo == gameconst.CrossServerReasonNo.ENTER_CROSS_SIEGE_WAR:
                spaceNo = CBC.datas['cityBattle_MapID']['value']
            crossServerId = self.crossServerDic['crossServerId']
            self.crossServerDic['token'] = token
            self.crossServerDic['spaceNo'] = spaceNo
            self.client.onCrossServerTokenResp(token, spaceNo, crossServerId)
            LOG_DBG('[lj]onCrossServerResp', token, spaceNo, crossServerId)

    def onReqGetAvatarPorperties(self, token, otherServerAccountBox):
        LOG_INFO("onReqGetAvatarPorperties", token, otherServerAccountBox)
        if token != self.crossServerDic.get("token"):
            LOG_ERR("onReqGetAvatarPorperties token error", token, self.crossServerDic.get("token"))
            otherServerAccountBox and otherServerAccountBox.onGetAvatarPorpertiesFail()
            return

        if self.endCrossServerTimerId:
            self.cancelTimerCB(self.endCrossServerTimerId, gametimer.TIMER_TAG_END_CROSS_SERVER)
            self.endCrossServerTimerId = 0

        self.crossServerDic['otherServerAccountBox'] = otherServerAccountBox
        self.addAllPropertiesToStream()

    def onGetAllProperties(self, baseMemoryStream, cellMemoryStream):
        otherServerAccountBox = self.crossServerDic.get('otherServerAccountBox')
        LOG_INFO("onGetAllProperties", otherServerAccountBox, len(baseMemoryStream), len(cellMemoryStream))
        otherServerAccountBox and otherServerAccountBox.onGetAvatarPorpertiesResp(baseMemoryStream, cellMemoryStream)

    def crossServerSuccess(self):
        LOG_INFO("crossServerSuccess")
        self.otherServerAvatarBox and self.otherServerAvatarBox.onCrossServerSuc(self.crossServerEntityCall)
        self.startCrossServerHeartbeat()

    def onCrossServerSuc(self, otherServerAvatarBox):
        LOG_INFO("onCrossServerSuc", otherServerAvatarBox)
        if self.crossServerState != gameconst.CrossServerState.ENUM_GOTO_CROSS_SERVER:
            LOG_WARN("onCrossServerSuc state is not GOTO_CROSS_SERVER", self.crossServerState)

        self.setCrossServerState(gameconst.CrossServerState.ENUM_IN_CROSS_SERVER)
        self.otherServerAvatarBox = otherServerAvatarBox
        self.crossServerSyncOtherInitedDataFromLocalServer(None)
        if self.endCrossServerTimerId:
            self.cancelTimerCB(self.endCrossServerTimerId, gametimer.TIMER_TAG_END_CROSS_SERVER)
            self.endCrossServerTimerId = 0
        self.disconnect(gameconst.ClientCallChannel.MAIN_CHANNEL)
        self.cell.onCrossServerSuc(self.crossServerDic["reasonNo"])

    def crossServerCallBack(self, callbackComponent, callbackName, args, extra):
        LOG_INFO("crossServerCallBack", callbackComponent, callbackName, args, extra)
        crossData = extra.get('crossData')
        baseInitData = extra.get('baseInitData')
        cellInitData = extra.get('cellInitData')
        self.onCrossServerSyncOtherInitedDataToCrossServer(crossData, baseInitData, cellInitData)

        if callbackComponent == gameconst.CrossServerCBComponent.ENUM_BASE:
            getattr(self, callbackName)(*args)
        elif callbackComponent == gameconst.CrossServerCBComponent.ENUM_CELL:
            self.cell and getattr(self.cell, callbackName)(*args)

        goBackTime = extra.get('goBackTime', 0)
        if goBackTime:
            self.goBackServerTimerId = self.addTimerCB(goBackTime, 'gobackServer',
                                                      (gameconst.CrossServerCBComponent.ENUM_NONE, '', ()),
                                                        gametimer.TIMER_TAG_GOBACK_SERVER, 'goBackServerTimerId')

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
        self.client.onGobackServer(gameconst.SIEGEWAR_GO_BACK_LINENO)
        gameengine.getGlobalBase('CrossServerStub').onGobackServer(self.accountEntity.accountName)

        self.cell.offline(gameconst.OFFLINE_REASON_END_CROSS_SERVER)

    def onCrossServerEnd(self, callbackComponent, callbackName, args):
        LOG_INFO("onCrossServerEnd", callbackComponent, callbackName, args)
        if self.crossServerState != gameconst.CrossServerState.ENUM_IN_CROSS_SERVER:
            LOG_ERR("onCrossServerSuc state is not IN_CROSS_SERVER", self.crossServerState)
            return

        self.setCrossServerState(gameconst.CrossServerState.ENUM_IN_CURRENT_SERVER)
        self.crossServerDic = {}

        if callbackComponent == gameconst.CrossServerCBComponent.ENUM_BASE:
            getattr(self, callbackName)(*args)
        elif callbackComponent == gameconst.CrossServerCBComponent.ENUM_CELL:
            self.cell and getattr(self.cell, callbackName)(*args)

    def onReloginInCrossServerState(self):
        LOG_INFO("onReloginInCrossServerState", self.crossServerDic['crossServerId'], self.crossServerDic['token'])
        r = iRouter.RemoteServerStubEntityCall(self.crossServerDic['crossServerId'], "CrossServerStub")
        r.onCheckCrossServerToken(self.accountEntity.accountName, self.crossServerDic['token'],
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
                self.client.onCrossServerTokenResp(self.crossServerDic['token'], self.crossServerDic['spaceNo'], self.crossServerDic['crossServerId'])
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
            )
            callbackComponent = self.crossServerDic.get('callbackComponent')
            callbackName = self.crossServerDic.get('callbackName')
            args = self.crossServerDic.get('args')
            extra = {
                'goBackTime': self.crossServerDic.get('goBackTime', 0),
                'crossData': crossData,
                'baseInitData': baseInitData,
                'cellInitData': cellInitData,
            }
            self.otherServerAvatarBox.crossServerCallBack(callbackComponent, callbackName, args, extra)

    # CrossServer
    def onCrossServerSyncOtherInitedDataToCrossServer(self, crossData, baseInitData, cellInitData):
        LOG_WARN("onCrossServerSyncOtherInitedDataToCrossServer::", crossData, baseInitData, cellInitData)
        self.scoresInfo = AvatarScores.avatarScoresInstance.createObjFromDict(baseInitData["scoresInfo"])
        self.cell.onCrossServerSyncOtherInitedDataToCrossServerCell(crossData, cellInitData)
        self.onSetGuildInfoCross(baseInitData['guildUUID'], baseInitData['guildName'], True)

    # CrossServer
    def syncMethodCallToLocalServerBase(self, fnname, fnargs):
        LOG_DBG("syncMethodCallToLocalServerBase::", fnname, fnargs)
        if self.isCrossServerInOtherServer and self.otherServerAvatarBox:
            self.otherServerAvatarBox.beSyncMethodCallFromCrossServerBase(fnname, fnargs)

    # localServer
    def beSyncMethodCallFromCrossServerBase(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromCrossServerBase::", fnname, fnargs)
        getattr(self, fnname)(*fnargs)

    # CrossServer
    def syncMethodCallToLocalServerCell(self, fnname, fnargs):
        LOG_DBG("syncMethodCallToLocalServerCell::", fnname, fnargs)
        if self.isCrossServerInOtherServer and self.otherServerAvatarBox:
            self.otherServerAvatarBox.beSyncMethodCallFromCrossServerCell(fnname, fnargs)

    # localServer
    def beSyncMethodCallFromCrossServerCell(self, fnname, fnargs):
        LOG_DBG("beSyncMethodCallFromCrossServerCell::", fnname, fnargs)
        getattr(self.cell, fnname)(*fnargs)

    def onMessagePre_localCross(self, msgId, args):
        LOG_INFO("onMessagePre_localCross::", msgId, args)
        self.localCrossBase.onMessagePre(msgId, args)

    def onPlayerGetExp_localCrossClient(self, src, expVal, realExpVal, chaseExp):
        LOG_INFO("onPlayerGetExp_localCrossClient::", src, expVal, realExpVal, chaseExp)
        self.localCrossClient.onPlayerGetExp(src, expVal, realExpVal, chaseExp)

    def onAvatarLevelUp_localCrossClient(self, oldLevel, level):
        LOG_INFO("onAvatarLevelUp_localCrossClient::", oldLevel, level)
