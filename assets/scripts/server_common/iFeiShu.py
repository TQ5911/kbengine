# -*- coding: utf-8 -*-

import gameglobal
import time
import gameconfig
import json
import KBEngine
from KBEDebug import *
LIMIT = 15
INTERVAL = 1


class IFeiShu():
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = IFeiShu()
        return cls._instance

    def __init__(self):
        self.timerId = None
        self.msgList = []
        self.lastFSTime = int(time.time())

    def reportErrorMsg(self, msg):
        # if "engine can't find navigate point" in msg:
        #     return

        if len(self.msgList) == 0:
            self.msgList.append("time: %s\n" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.msgList.append("%s \n\n" % msg)
        if not self.timerId:
            self.timerId = KBEngine.addTimer(INTERVAL, 0, lambda tId: self.sendMsg())

    def sendMsg(self):
        self.timerId = None
        msgs = []
        while len(msgs) < LIMIT:
            if len(self.msgList) > 0:
                msgs.append(self.msgList.pop(0))
            else:
                break
        if len(msgs) <= 0:
            return

        if gameglobal.curServerAlias:
            _serverName = gameglobal.curServerAlias
        else:
            _serverName = gameconfig.serverName()
        msgs.append("serverId: %d, 服务器: %s" % (gameconfig.serverId(), gameconfig.serverName()))

        datas = {
            "msgtype": "text",
            "text": {
                "content": ''.join(msgs),
                'mentioned_mobile_list':[_serverName]
            },
        }
        self.msgList = []
        url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=92de3ed1-9bfe-4428-afc6-f1488f9bb452"
        if gameconfig.serverId() == 10001:
            url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=72713252-20ea-4ef8-976a-0befb867d20f"

        cbFunc = lambda httpcode, data, headers, success, url: \
            self.onReportResult(httpcode, data, headers, success, url)

        KBEngine.urlopenv2(url, cbFunc, method='POST',
                           postData=json.dumps(datas).encode('utf-8'),
                           headers={"Content-Type": "application/json"},
                           timeoutSec=1)

        debugErrorLogHost = gameconfig.debugErrorLogHost()
        if not debugErrorLogHost:
            return

        url = '{}/logs'.format(debugErrorLogHost)
        datas = {
            'raw': '$-$'.join(msgs)
        }
        KBEngine.urlopenv2(url, cbFunc, method='POST',
                           postData=json.dumps(datas).encode('utf-8'),
                           headers={"Content-Type": "application/json"},
                           timeoutSec=1)


    def onReportResult(self, httpcode, data, headers, success, url):
        pass


def instance():
    return IFeiShu.instance()
