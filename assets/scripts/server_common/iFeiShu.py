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
        if len(self.msgList) == 0:
            self.msgList.append("time: %s\n" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.msgList.append("%s \n\n" % msg)
        if not self.timerId:
            self.timerId = KBEngine.addTimer(INTERVAL, 0, lambda tId: self.sendMsg())

    def sendMsg(self):
        self.timerId = None
        msgs = []
        msgs.append("serverId: %d, 服务器: %s  " % (gameconfig.serverId(), gameglobal.curServerName))
        while len(msgs) < LIMIT:
            if len(self.msgList) > 0:
                msgs.append(self.msgList.pop(0))
            else:
                break
        if len(msgs) <= 0:
            return

        self.msgList = []
        #
        self.goBlinReport(msgs)

    def wxReportDirect(self, msgs):
        if gameglobal.curServerAlias:
            _serverName = gameglobal.curServerAlias
        else:
            _serverName = gameglobal.curServerName
        datas = {
            "msgtype": "text",
            "text": {
                "content": ''.join(msgs),
                'mentioned_mobile_list':[_serverName]
            },
        }
        url = gameconfig.wxReportUrl()
        if not url:
            return
        # if gameconfig.serverId() == 10001:
        #     url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=72713252-20ea-4ef8-976a-0befb867d20f"

        cbFunc = lambda httpcode, data, headers, success, url: \
            self.onReportResult(httpcode, data, headers, success, url, msgs, 'wechat')
        
        KBEngine.urlopenv2(url, cbFunc, method='POST',
                           postData=json.dumps(datas).encode('utf-8'),
                           headers={"Content-Type": "application/json"},
                           timeoutSec=1)
    
    def goBlinReport(self, msgs):
        debugErrorLogHost = gameconfig.debugErrorLogHost()
        if not debugErrorLogHost:
            self.wxReportDirect(msgs)
            return

        url = '{}/logs'.format(debugErrorLogHost)
        if gameglobal.curServerAlias:
            _serverName = gameglobal.curServerAlias
        else:
            _serverName = gameglobal.curServerName
        
        sendMsg = [_serverName]
        sendMsg.extend(msgs)
        datas = {
            'raw': '$-$'.join(sendMsg)
        }

        cbFunc = lambda httpcode, data, headers, success, url: \
            self.onReportResult(httpcode, data, headers, success, url, msgs, 'goblin')
        KBEngine.urlopenv2(url, cbFunc, method='POST',
                           postData=json.dumps(datas).encode('utf-8'),
                           headers={"Content-Type": "application/json"},
                           timeoutSec=1)

    def onReportResult(self, httpcode, data, headers, success, url, msgs, channel):
        LOG_INFO('onReportResult: code: {}, data: {}, headers: {}, success: {}, url: {}, channel: {}'.format(httpcode, data, headers, success, url, channel))
        if channel != 'wechat' and (httpcode != 200 or KBEngine.publish()):
            # report to wechat
            self.wxReportDirect(msgs)

def instance():
    return IFeiShu.instance()
