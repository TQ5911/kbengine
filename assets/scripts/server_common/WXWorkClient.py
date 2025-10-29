# -*- coding: utf-8 -*-

import SocketClient
import gameglobal
import time


class WXWorkClient(SocketClient.SocketClient):
    _instance = None

    MSG_FLAG = "!@#"

    lastWXTime = 0
    totalCount = 0

    @classmethod
    def instance(cls):
        if cls._instance is None:
            import gameconfig
            cls._instance = WXWorkClient((gameconfig.socketConnectServerIP(), gameconfig.socketConnectServerPort()))
            cls._instance.sendServerName()
        return cls._instance

    def handle_close(self):
        super().handle_close()
        WXWorkClient._instance = None

    def handle_expt(self):
        super().handle_expt()
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
        # msg = 'login_remind\n%s\n%s\n%s' % (ID, serverName, ip)
        sendMsg = self.MSG_FLAG + 'team_say\nutf-8\n%d\n%s\n' % (6, msg)
        self.buffer += sendMsg.encode('utf-8')

    def sendErrorMsg(self, msg, prefix='exception'):
        import gameconfig
        if not gameconfig.wxErrFlag():
            return
        if gameglobal.refreshCount > 0:
            return
        sendMsg = self.MSG_FLAG + '%s\n%s\n' % (prefix, msg,)
        if self.lastWXTime == int(time.time()):
            if self.totalCount >= gameconfig.wxErrNumPerSecond():
                return
            else:
                self.totalCount += 1
        else:
            self.lastWXTime = int(time.time())
            self.totalCount = 1
        self.buffer += sendMsg.encode('utf-8')


def instance():
    return WXWorkClient.instance()
