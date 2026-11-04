# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import json
import random
import urllib.parse

import utils
import gamedecorator
import gameconfig
import gametimer

import proto.centralLogin_pb2 as centralLogin

class IPromoter(object):

    def __init__(self):
        if gameconfig.isCrossServer():
            return
        if self.accountType != centralLogin.ACCOUNT_OFFICIAL:
            return
        if not self.isPromoterInited:
            self.startIntervalPromoterRequest()

    def doPromoterInit(self):
        url = gameconfig.promoterAPI()
        _paramDic = {
            "gameId"    : gameconfig.gameId(),
            "month"     : '',
        }
        # 该接口只接受 GET（服务端 405 响应里的 Allow 头给的就是 GET）。
        # urlopenv2 只要带了 postData 就会强制走 POST，GET 带 body 会被服务端
        # 判成 405 Method Not Allowed，所以参数必须拼在 query string 上，不能放进 body。
        _param = urllib.parse.urlencode(_paramDic, encoding='utf-8')
        url = f'{url}?{_param}'
        LOG_INFO("IPromoter request promoter info url", url, _param)
        KBEngine.urlopenv2(url, self.promoterResponse, method='GET',
                headers={"satoken": self.webToken},
                timeoutSec=2)
        
    def promoterResponse(self, httpCode, data, headers, success, *args):
        LOG_INFO("promoterResponse", httpCode, data, headers, success)
        if self.isDestroyed:
            LOG_INFO("promoterResponse account is destroyed")
            return
        
        if not data:
            self.startIntervalPromoterRequest()
            LOG_ERR("promoterResponse but data is empty")
            return
        
        data = json.loads(data)
        if data.get('code', 0) != 200:
            self.startIntervalPromoterRequest()
            LOG_ERR("promoterResponse fail!, delay request~", httpCode, data)
            return
        
        promoterTime = str(data.get('data', {}).get('benefit', {}).get('expiresAt', 0))
        if not promoterTime.isdigit():
            self.startIntervalPromoterRequest()
            LOG_ERR("promoterResponse wrong format, delay request~", httpCode, data, promoterTime)
            return
        
        self.stopIntervalPromoterRequest()
        
        self.gmSetPromoter(int(promoterTime), False)
        self.isPromoterInited = True

    def startIntervalPromoterRequest(self):
        self.stopIntervalPromoterRequest()
        LOG_INFO("startIntervalPromoterRequest~")
        interval = random.randint(3, 7)
        self.promoterRequestTimerId = self.pyAddTimer(interval, interval, gametimer.TIMER_PROMOTER_REQUEST_DELAY)

    def stopIntervalPromoterRequest(self):
        if self.promoterRequestTimerId:
            LOG_INFO("stopIntervalPromoterRequest~")
            self.pyDelTimer(self.promoterRequestTimerId, gametimer.TIMER_PROMOTER_REQUEST_DELAY)
            self.promoterRequestTimerId = 0

    @gamedecorator.offlineCallback
    def gmSetPromoter(self, cdTime, isOffline):
        LOG_INFO("gmSetPromoter::", cdTime, isOffline)
        if cdTime <= self.promoterTime:
            return
        
        self.promoterTime = cdTime
        if self.avatar:
            self.syncPromoterInfo()

    def checkPromoterCD(self):
        return utils.curTS() < self.promoterTime
    
    def syncPromoterInfo(self):
        LOG_INFO("account syncPromoterInfo::", self.promoterTime)
        self.avatar.cell.syncPromoterInfo(self.promoterTime)