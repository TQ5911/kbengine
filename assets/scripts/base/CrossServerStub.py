# coding: utf-8

import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import SwitchServer
import utils
import gameglobal
import gameengine
import gameconfig
import iRouter
import gameconst
import message_chatMessage as MCMD
import iRouter
import gameconfig


# 游戏服上报间隔，跨服超过 3 次没收到就从广播名单里摘掉
_HEARTBEAT_INTERVAL = 10
_HEARTBEAT_TIMEOUT = _HEARTBEAT_INTERVAL * 3


class CrossServerStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        pass

    def doNext(self):
        super().doNext()
        self.pyAddTimer(1, _HEARTBEAT_INTERVAL, gametimer.TIMER_GAME_CROSS_HEARTBEAT)

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.TIMER_GAME_CROSS_HEARTBEAT:
            self._onGameCrossHeartBeatTick()
        else:
            self._onTimerTrigger(tid, userArg)

    def _onGameCrossHeartBeatTick(self):
        if gameconfig.isCrossServer():
            self._sweepGameServerHeartBeat()
            return

        crossId = int(gameconfig.getCrossServerId())
        if crossId <= 0:
            return
        _stub = iRouter.RemoteServerStubEntityCall(crossId, 'CrossServerStub')
        _stub.onGameServerHeartBeat(int(gameconfig.serverId()))

    def onGameServerHeartBeat(self, serverId):
        if not gameconfig.isCrossServer():
            return

        serverId = int(serverId)
        if serverId <= 0 or serverId == int(gameconfig.serverId()):
            return

        now = utils.curTS()
        isNew = serverId not in self.gameServerHeartBeat
        self.gameServerHeartBeat[serverId] = now
        self._publishGroupGameServerIds()
        if isNew:
            LOG_INFO('game server heartbeat register', serverId)

    def _sweepGameServerHeartBeat(self):
        if not self.gameServerHeartBeat:
            return

        now = utils.curTS()
        expired = [sid for sid, ts in self.gameServerHeartBeat.items() if now - ts > _HEARTBEAT_TIMEOUT]
        if not expired:
            return
        for sid in expired:
            self.gameServerHeartBeat.pop(sid, None)
            LOG_INFO('game server heartbeat timeout', sid)
        self._publishGroupGameServerIds()

    def _aliveGameServerIds(self):
        if not self.gameServerHeartBeat:
            return []

        now = utils.curTS()
        return [sid for sid, ts in self.gameServerHeartBeat.items() if now - ts <= _HEARTBEAT_TIMEOUT]

    def _publishGroupGameServerIds(self):
        KBEngine.globalData[gameconst.GLOBALDATA_KEY_CROSS_GROUP_SERVERS] = self._aliveGameServerIds()

    def test(self):
        LOG_INFO("CrossServerStub test")

    def onGetSwitchServerData(self, data):
        LOG_INFO("onGetSwitchServerData: {}".format(len(data)))
        SwitchServer.SwitchServerUtils.saveData(data)

    def onPing(self, serverId, msg):
        INFO_MSG('onPing', serverId, msg)
        _r = iRouter.RemoteServerStubEntityCall(serverId, "CrossServerStub")
        _r.onPong(gameconfig.serverId(), 'hello world pong')

    def onPong(self, serverId, msg):
        INFO_MSG('onPong', serverId, msg)

    def onReqCrossServer(self, accountName, reasonNo, crossServerEntityCall):
        LOG_INFO("onReqCrossServer", accountName, reasonNo)
        ret = True
        if accountName in self.accountDic:
            LOG_WARN("onReqCrossServer accountName has in accountDic", accountName)

        token = utils.generateUUID()
        self.accountDic[accountName] = {
            "box": crossServerEntityCall,
            "token": token
        }
        crossServerEntityCall.onCrossServerResp(ret, token, reasonNo)

    def onEndCrossServer(self, accountName):
        LOG_INFO("onEndCrossServer", accountName)
        if accountName not in self.accountDic:
            LOG_ERR("onGobackServer accountName not in accountDic", accountName)
            return

        self.accountDic.pop(accountName)

    def onCheckCrossServerToken(self, accountName, token, crossServerEntityCall):
        LOG_INFO("onCheckCrossServerToken", accountName, token, crossServerEntityCall)
        _ret, _ = self._checkCrossServerToken(accountName, token)
        crossServerEntityCall.onCheckCrossServerTokenResp(_ret)

    def _checkCrossServerToken(self, accountName, token):
        _ret = False
        crossServerEntityCall = None

        if accountName not in self.accountDic:
            LOG_ERR("_checkCrossServerToken accountName not in accountDic", accountName)
        else:
            crossServerToken = self.accountDic[accountName].get("token")
            if crossServerToken != token:
                LOG_ERR("_checkCrossServerToken token err", crossServerToken, token)
            else:
                _ret = True
                crossServerEntityCall = self.accountDic[accountName].get("box")
        return _ret, crossServerEntityCall

    def checkCrossServerToken(self, accountName, token, box, callBackFunc, callBackArgs):
        LOG_INFO("checkCrossServerToken", accountName, token, box, callBackFunc, callBackArgs)
        _ret, crossServerEntityCall = self._checkCrossServerToken(accountName, token)
        _args = [_ret, crossServerEntityCall]
        _args.extend(callBackArgs)
        getattr(box, callBackFunc)(*_args)

    def onGobackServer(self, accountName):
        LOG_INFO("onGobackServer", accountName)
        if accountName not in self.accountDic:
            LOG_WARN("onGobackServer accountName not in accountDic", accountName)
            return

        self.accountDic.pop(accountName)

    def doGmModifyServertime(self, su, modifyTime):
        LOG_INFO("doGmModifyServertime", su, modifyTime)
        import gameconfig
        import iRouter
        import gmCommand
        if gameconfig.serverId() not in gameglobal.mapleServerInfo:
            LOG_ERR("onGmModifyAllServertimeInCrossGroup gameconfig.serverId() not in maple", gameconfig.serverId())
            return


        if KBEngine.publish():
            LOG_ERR("onGmModifyAllServertimeInCrossGroup KBEngine.publish()", KBEngine.publish())
            return
        if '.' and '-' not in modifyTime:
            return
        forwardGMCommand = gmCommand.forwardGMCommand
        forwardGMCommand(su, '$modifyServertime-cell', modifyTime)
        forwardGMCommand(su, '$modifyServertime-base', modifyTime)

        LOG_DBG("doGmModifyServertime success", gameconfig.serverId(), modifyTime)

    # 改跨服和当前心跳在线的游戏服时间
    def onGmModifyAllServertimeInCrossGroup(self, su, modifyTime):
        LOG_INFO("onGmModifyAllServertimeInCrossGroup", su, modifyTime)
        if not gameconfig.isCrossServer():
            return

        self.doGmModifyServertime(su, modifyTime)
        for serverID in self._aliveGameServerIds():
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'CrossServerStub')
            _stub.onGmModifyAllServertimeInCrossGroupResp(su, modifyTime)

        LOG_DBG("onGmModifyAllServertimeInCrossGroup success", gameconfig.serverId(), modifyTime)

    def onGmModifyAllServertimeInCrossGroupResp(self, su, modifyTime):
        LOG_DBG("onGmModifyAllServertimeInCrossGroupResp", su, modifyTime)
        self.doGmModifyServertime(su, modifyTime)

    def onGlobalEventTips(self, crossServerType, msgId, msgArgs):
        LOG_DBG("onGlobalEventTips", crossServerType, msgId, msgArgs)
        if crossServerType == gameconst.EventTipCrossServerType.CrossAllServer and gameconfig.isCrossServer():
            for serverID in self._aliveGameServerIds():
                LOG_INFO('broadcastTips', gameconst.EventTipCrossServerType.Default, msgId, msgArgs, gameconfig.isCrossServer(), serverID)
                _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'CrossServerStub')
                _stub.onGlobalEventTips(gameconst.EventTipCrossServerType.Default, msgId, msgArgs)
            gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onEventTips', (msgId, msgArgs)))
            return
        gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onEventTips', (msgId, msgArgs)))

    def crossBroadcastMsg(self, msgId):
        LOG_DBG("crossBroadcastMsg", msgId)
        mcData = MCMD.datas.get(msgId)
        conveyType = mcData.get('conveyType', 0)
        if conveyType == gameconst.ChatMsgConveyType.NULL:
            return
        serverId = gameconfig.serverId()
        serverIds = utils.crossGroupGameServerIdsEx(serverId)
        if conveyType == gameconst.ChatMsgConveyType.CROSS_LOCAL or \
            conveyType == gameconst.ChatMsgConveyType.CROSS_GROUP:
            for sid in serverIds:
                iRouter.RemoteServerStubEntityCall(sid, "CrossServerStub").onCrossBroadcastMsg(serverId, msgId, conveyType)

    def onCrossBroadcastMsg(self, fromServerId, msgId, conveyType):
        LOG_DBG("onCrossBroadcastMsg", fromServerId, msgId, conveyType)
        gameengine.broadcastBaseapp(
            'broadcastToAllAvatar',
            (
                gameconst.BASE,
                'onCrossMessagePre',
                (fromServerId, conveyType, msgId, []),
                (),
            )
        )