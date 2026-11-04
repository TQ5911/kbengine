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
    
    def criticalReportDirect(self, msgs):
        """紧急告警直发, 走 gameconfig.criticalReportUrl() 配置的独立群机器人。

        和 wxReportDirect 的差异:
            1. url 独立配置(criticalReportUrl), 不与普通错误上报抢同一个群;
            2. 上报失败不回落到 wxReportDirect, 避免两路报警重复/互相淹没;
            3. 超时放宽到 3 秒, 紧急告警允许稍微多等一会儿。
        """
        url = gameconfig.criticalReportUrl()
        if not url:
            LOG_ERR('criticalReportDirect: criticalReportUrl is empty, skip report')
            return

        if gameglobal.curServerAlias:
            _serverName = gameglobal.curServerAlias
        else:
            _serverName = gameglobal.curServerName

        datas = {
            "msgtype": "text",
            "text": {
                "content": ''.join(msgs),
                'mentioned_mobile_list': [_serverName]
            },
        }

        cbFunc = lambda httpcode, data, headers, success, url: \
            self.onReportResult(httpcode, data, headers, success, url, msgs, 'wechat_critical')

        KBEngine.urlopenv2(url, cbFunc, method='POST',
                           postData=json.dumps(datas).encode('utf-8'),
                           headers={"Content-Type": "application/json"},
                           timeoutSec=3)

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
        # wechat / wechat_critical 本身就是走微信机器人, 失败不再回落到 wxReportDirect, 免重复
        if channel not in ('wechat', 'wechat_critical') and (httpcode != 200 or KBEngine.publish()):
            # report to wechat
            self.wxReportDirect(msgs)

def instance():
    return IFeiShu.instance()
