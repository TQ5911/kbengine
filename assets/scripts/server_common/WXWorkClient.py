# -*- coding: utf-8 -*-

import SocketClient
import time
import gameglobal


class WXWorkClient(SocketClient.SocketClient):
    _instance = None

    MSG_FLAG = "!@#"

    totalCount = 0
    lastWXTime = 0

    @classmethod
    def instance(cls):
        if cls._instance is None:
            import gameconfig
            _ip = gameconfig.socketConnectServerIP()
            _port = gameconfig.socketConnectServerPort()
            cls._instance = WXWorkClient((
                _ip, 
                _port,
            ))
            cls._instance.sendServerName()
        return cls._instance

    def handle_expt(self):
        super().handle_expt()
        WXWorkClient._instance = None

    def handle_close(self):
        super().handle_close()
        WXWorkClient._instance = None

    def sendServerName(self):
        import gameconfig
        if gameglobal.curServerAlias:
            _serverName = gameglobal.curServerAlias
        else:
            _serverName = gameglobal.curServerName

        sendMsg = self.MSG_FLAG + 'serverName\n%s||%s' % (_serverName, gameconfig.serverId())
        self.buffer += sendMsg.encode('utf-8')

    def sendOnlineMsg(self, msg):
        _sendMsg = self.MSG_FLAG + 'team_say\nutf-8\n%d\n%s\n' % (6, msg)
        self.buffer += _sendMsg.encode('utf-8')

    def sendErrorMsg(self, msg, prefix='exception', **kwargs):
        import gameconfig
        if not gameconfig.wxErrFlag():
            return
        if gameglobal.refreshCount > 0:
            return
        _sendMsg = self.MSG_FLAG + '%s\n%s\n' % (prefix, msg,)
        if int(time.time()) == self.lastWXTime:
            if self.totalCount >= gameconfig.wxErrNumPerSecond():
                return
            else:
                self.totalCount += 1
        else:
            self.totalCount = 1
            self.lastWXTime = int(time.time())
        self.buffer += _sendMsg.encode('utf-8')


def instance():
    return WXWorkClient.instance()
