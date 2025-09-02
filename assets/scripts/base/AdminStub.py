# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import gameengine
import iGlobal
import iBaseNoCell
import iTimer
import gamesql
import gametimer
import gameconfig
import hashlib

from rpc import RpcChannel, TcpClient
from proto.adminServer_pb2 import (
    Admin_Stub, GameServer, ServerInfoMessage, CommandResult, Void,
    HttpAPICommandResponse)

import gmCommand
import gameglobal
import gameconst
import gmGroup
import json
import random


class AdminStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        iGlobal.IGlobal.__init__(self)
        iBaseNoCell.IBaseNoCell.__init__(self)
        iTimer.ITimer.__init__(self)

        self.gmClient = {}

    def doNext(self):
        self._fullPrepare()

    def _fullPrepare(self):
        self.pyAddTimer(1, 1, gametimer.ADMIN_STUB_ASYNC_TICK)
        gameglobal.localBaseApp.initAysncore()

        self.pyAddTimer(gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL,
                        gametimer.ADMIN_STUB_ACTIVE_TICK)

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if userArg == gametimer.ADMIN_STUB_ASYNC_TICK:
            self._connectGmCenter()
        elif userArg == gametimer.ADMIN_STUB_ACTIVE_TICK:
            self._checkGmCenterActive()

    def reloadScript(self):
        super(AdminStub, self).reloadScript()

    def gmCenterClosed(self):
        DEBUG_MSG('in AdminStub.gmCenterClosed')
        self.gmClient = {}

    def popGmClient(self, tag):
        self.gmClient.pop(tag, None)

    def _connectGmCenter(self):
        if not gameconfig.enableAdminServer():
            return

        hostList = gameconfig.gmHostList()
        for host in hostList:
            key = '{}:{}'.format(host['addr'], host['port'])
            client = self.gmClient.get(key, None)
            if client and client.channel.dispatcher: continue

            addr, port = host['addr'], int(host['port'])
            INFO_MSG('connect admincenter:', addr, port)
            self.gmClient[key] = AdminStubService(self, (addr, port))

    def _checkGmCenterActive(self):
        if not gameconfig.enableAdminServer():
            return

        for client in self.gmClient.values():
            if client and client.channel.dispatcher:
                client.serviceStub.activeTick(None, Void(), None)

    def replyCommand(self, tag, account, cmdUUID, message, success):
        client = self.gmClient.get(tag, None)
        if client and client.channel.dispatcher:
            cmdResult = CommandResult()
            cmdResult.account = account
            cmdResult.uuid = cmdUUID
            cmdResult.resultCode = success
            cmdResult.result = message
            client.serviceStub.replyCommand(None, cmdResult, None)

    def replyHttpCommand(self, tag, cmdUUID, result, retErrMsg, bodyBytes):
        DEBUG_MSG('in AdminStub.replyHttpCommand ', tag, cmdUUID, result, retErrMsg, bodyBytes)
        client = self.gmClient.get(tag, None)
        if client and client.channel.dispatcher:
            resp = HttpAPICommandResponse()
            resp.uuid = cmdUUID
            resp.result = result
            resp.retErrMsg = retErrMsg
            resp.body = bodyBytes
            client.serviceStub.replyHttpCommand(None, resp, None)

    def sendGmCenterPeek(self, url, callback, message, timeoutSec = 1):
        key, client = random.choice(list(self.gmClient.items()))
        if client and client.channel.dispatcher:  # 有效的client
            hostList = gameconfig.gmHostList()
            for host in hostList:
                if '{}:{}'.format(host['addr'], host['port']) == key:  # 对应的http端口
                    urlBase = 'http://{}:{}'.format(host['addr'], host['httpApi'])
                    KBEngine.urlopenv2(urlBase + url, callback, method='POST',
                           postData=message,
                           headers={'Content-Type': 'application/octet-stream'},
                           timeoutSec=timeoutSec)
                    return

    def callHttApi(self, action, callback, dataDic):
        body = json.dumps(dataDic).encode('utf-8')

        header = {
            'Content-Type': 'application/json;charset=utf-8',
        }

        cfg = random.choice(gameconfig.gmHostList())
        apiSecret = gameconfig.gmHttpAPISecret()
        urlBase = 'http://{}:{}'.format(cfg['addr'], cfg['httpApi'])

        if apiSecret:
            content = body + bytes(apiSecret, 'ascii')
            signStr = hashlib.md5(content).hexdigest()
            url = '%s%s?sign=%s' % (urlBase, action, signStr)
        else:
            url = urlBase + action

        KBEngine.urlopenv2(url, callback, method='POST', postData=body, headers=header, timeoutSec=3)


class AdminStubService(GameServer):
    # adminStub: callback obj
    # address: tuple of (ip, port)
    def __init__(self, adminStub, address):
        self.tag = '{}:{}'.format(address[0], address[1])
        self.adminStub = adminStub
        self.channel = RpcChannel.RpcChannel(self)
        self.serviceStub = Admin_Stub(self.channel)

        self.channel.connect(address)

    def on_connected(self):
        self._reportServerId()

    def on_disconnected(self):
        self.adminStub.popGmClient(self.tag)

    def _reportServerId(self):
        request = ServerInfoMessage()
        request.serverId = gameconfig.serverId()
        request.compId = KBEngine.getComponentGroupOrder()
        request.serverName = gameconfig.serverName()

        self.serviceStub.registerServer(None, request, None)

    def doCommand(self, rpc_controller, request, done):
        if not gameconfig.enableOutsideCommand():
            return

        account = request.account
        command = request.command
        cmdUUID = request.uuid
        agent = gmCommand.GMAgent(self.adminStub, self.tag, account, gmGroup.MANAGER_GROUP_GOD, cmdUUID)

        gmCommand.doCommandOutside(agent, command, 'from gmt')

    def doHttpCommand(self, rpc_controller, request, done):
        seqIdStr = str(request.seqId)
        cmdStr = request.cmd.lower()
        if gameconfig.shouldCheckAdminCmdSerial() and cmdStr in gameconfig.httpCmdIdempotent():
            gamesql.checkAdminCmdSerial(seqIdStr, lambda result, rows, insertid, error:
            self.onCheckHttpCommandSerial(result, rows, insertid, error, request, cmdStr))
        else:
            self._doHttpCommand(request)

    def onCheckHttpCommandSerial(self, result, rows, insertid, error, request, cmdStr):
        if error:
            ERROR_MSG('onCheckHttpCommandSerial err:', request.seqId, request.cmd, error, cmdStr)
            self._reportHttpCmdError(request, gameconst.GMCommandErr.DB_OP_ERR, 'internal error')
            return

        if result:
            _, bRetCode, bRetErrMsg, bRetStr = result[0]
            retCode = int(bRetCode)
            retErrMsg = bRetErrMsg.decode('uft-8')
            INFO_MSG("onCheckHttpCommandSerial---", bRetErrMsg, bRetStr)
            if cmdStr == '$notifymallaction':
                self._reportHttpCmdError(request, gameconst.GMCommandErr.CMD_SERIAL_EXISTS, 'seqId duplicated')
            else:
                self._reportHttpCmd(request, retCode, retErrMsg, bRetStr)
            return

        self._doHttpCommand(request)

    def _doHttpCommand(self, request):
        cmdUUID = request.uuid
        cmdName = request.cmd
        seqIdStr = str(request.seqId)

        try:
            cmdArgs = bytes.fromhex(request.args).decode('utf-8')
        except Exception as e:
            ERROR_MSG('doHttpCommand: parse command args err:', e, request.args)
            self._reportHttpCmdError(request, gameconst.GMCommandErr.ARGS_ERR, 'invalid command args')
            return

        INFO_MSG('_doHttpCommand', cmdName, cmdArgs, seqIdStr)

        agent = gmCommand.HTTPAgent(self.adminStub, self.tag, 'HTTP', gmGroup.MANAGER_GROUP_GOD, cmdUUID, seqIdStr,
                                    cmdName.lower())
        gmCommand.doCommandOutside(agent, cmdName + ' ' + cmdArgs, 'HTTP')

    def _reportHttpCmd(self, request, result, msg, retMsgBytes):
        resp = HttpAPICommandResponse()
        resp.uuid = request.uuid
        resp.result = result
        resp.retErrMsg = msg
        resp.body = retMsgBytes
        self.serviceStub.replyHttpCommand(None, resp, None)

    def _reportHttpCmdError(self, request, result, msg):
        resp = HttpAPICommandResponse()
        resp.uuid = request.uuid
        resp.result = result
        resp.retErrMsg = msg
        resp.body = b''
        self.serviceStub.replyHttpCommand(None, resp, None)

    def activeTickCallback(self, rpc_controller, request, done):
        pass
