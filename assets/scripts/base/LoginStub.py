# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import urllib.parse
import collections
import hashlib
import json
import http

import gameconst
import gameengine
import gamebase
import gametimer
import gamesql
import utils
import userType
import gameconfig
import gameglobal
import gamelog
import globalDataSum

import iBaseNoCell
import iGlobal
import iCentralLogin
import iTimer
import globalDataCounter
from Crypto.Cipher import AES
import LogTrackingMgr
import redisUtils


class LoginStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer,
                iCentralLogin.ICentralLogin):

    def __init__(self):
        super(LoginStub, self).__init__()
        self.accountNumCounter = globalDataSum.GloalDataSum(gameconst.GLOBALDATA_KEY_ONLINE_NUM,
                                                    gameglobal.localBaseApp.registerBaseappDataCallback, globalDataSum.DATA_BASEAPP, cd=2)

        self.accountRegNum = globalDataSum.GloalDataSum(gameconst.GLOBALDATA_KEY_REG_NUM,
                                                    gameglobal.localBaseApp.registerBaseappDataCallback, globalDataSum.DATA_BASEAPP, cd=2)

        self.accountTodayRegNum = globalDataSum.GloalDataSum(gameconst.GLOBALDATA_KEY_TODAY_REG_NUM,
                                                    gameglobal.localBaseApp.registerBaseappDataCallback, globalDataSum.DATA_BASEAPP, cd=2)
        
        self.SVIPOnlineNum = globalDataSum.GloalDataSum(gameconst.GLOBALDATA_KEY_SVIP_ONLINE_NUM,
                                                    gameglobal.localBaseApp.registerBaseappDataCallback, globalDataSum.DATA_BASEAPP, cd=2)

        # 注册人数
        gamesql.queryCountAccountNum(self._initAccountRegNum)

        self.todayAccountRegNumTs= utils.curTS()
        self.accountTodayRegNum.setSum(self, 0)

    def doNext(self):
        self._fullPrepare()
        return

    def _fullPrepare(self):
        self.pyAddTimer(1, 1, gametimer.LOGIN_STUB_ASYNC_TICK)
        self.pyAddTimer(20, 1, gametimer.LOGIN_STUB_SERVERINFO_SYNC)
        #TODO： upload online number to line service

        # 注册人数同步到 interface
        self.pyAddTimer(60, 60, gametimer.LOGIN_STUB_SYNC_INTERFACE_REGNUM)
        if gameglobal.isBootstrap:  
            self.pyAddTimer(1, 30, gametimer.LOGIN_STUB_LOG_TRACKING_PCU)

        gameglobal.localBaseApp.initAysncore()

    def onTimer(self, timerID, userData):
        self._onTimer(timerID, userData)
        if userData == gametimer.LOGIN_STUB_ASYNC_TICK:
            self.connectAllCentralServer()

        elif userData == gametimer.LOGIN_STUB_SERVERINFO_SYNC:
            if gameconfig.enableCentralLogin():
                self.updateServerInfo()
                if gameglobal.isBootstrap:
                    self.updateSVIPOnlineNum()

        elif userData == gametimer.LOGIN_STUB_ACTIVE_TICK:
            if gameconfig.enableCentralLogin():
                self.checkAllCentralServerActive()

        elif utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)

        elif userData == gametimer.LOGIN_STUB_TLOG_GAMESVR_STATE:
            serverid = gameconfig.serverId()
            iZoneAreaID = gameconfig.serverId()
            gamelog.makeGameSvrStateLog(iZoneAreaID)

        elif userData == gametimer.LOGIN_STUB_SYNC_INTERFACE_REGNUM:
            gameglobal.localBaseApp.notifyInterfaceSyncRegisterCount(self.accountRegNum.dataSum)
        
        elif userData == gametimer.LOGIN_STUB_LOG_TRACKING_PCU:
            LogTrackingMgr.LogTrackingMgr.Server_Pcu(
                self.getGlobalAccountNum(),
            )

        return

    def getConfig(self):
        return gameconfig

    def onCentralServerConnected(self, centralServerId):
        LOG_IFO('onCentralServerConnected', centralServerId, KBEngine.getComponentGroupOrder())
        if KBEngine.getComponentGroupOrder()==1:
            self.tryRegisterServer(centralServerId)

        if self.heartBeatTimer:
            self.pyDelTimer(self.heartBeatTimer, gametimer.LOGIN_STUB_ACTIVE_TICK)

        self.heartBeatTimer = self.pyAddTimer(gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVER_HEARTBEAT_INTERVAL, gametimer.LOGIN_STUB_ACTIVE_TICK)

    def tryRegisterServer(self, centralServerId):
        if not KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_GAME_READY):
            self.addTimerCB(5, 'tryRegisterServer', (centralServerId,), gametimer.TIMER_TAG_TRY_REGISTER_SERVER)
        else:
            self.registerServer(centralServerId)

    def onAccountDestroy(self, accountName, accountType, devicePlatId, centralServerId, channelId, sessionIdStr):
        LOG_IFO("onAccountDestroy", accountName, accountType, devicePlatId, centralServerId, channelId, sessionIdStr)
        realAccountName = utils.mixRealAccountName(accountType, accountName)
        self.account2box.pop(realAccountName, None)
        # deduct account online num
        self.accountNumCounter.decSum(self)

        curPlat = self.playerNumPlat.setdefault(devicePlatId, {})
        curNum = curPlat.get(channelId, 0)
        self.playerNumPlat[devicePlatId][channelId] = max(curNum - 1, 0)

        if gameconfig.enableCentralLogin():
            self.notifyCentralServerOffline(accountName, accountType, centralServerId, sessionIdStr)
        
        redisUtils.RedisUtils.getSVIPFlag(accountName, self._onDecSVIPAccount)

    def incSVIPOnlineNumBySetSVIP(self):
        LOG_IFO("incSVIPOnlineNumBySetSVIP")
        self.SVIPOnlineNum.incSum(self)

    def _onIncSVIPAccount(self, cid, err, res):
        LOG_IFO("_onIncSVIPAccount", "cid", cid, "err", err, "res", res)
        if err:
            LOG_ERR("_onIncSVIPAccount", "err", err)
            return

        if res and res.decode() == '1':
            self.SVIPOnlineNum.incSum(self)

    def _onDecSVIPAccount(self, cid, err, res):
        LOG_IFO("_onDecSVIPAccount", "cid", cid, "err", err, "res", res)
        if err:
            LOG_ERR("_onDecSVIPAccount", "err", err)
            return

        if res and res.decode() == '1':
            self.SVIPOnlineNum.decSum(self)

    def updateSVIPOnlineNum(self):
        redisUtils.RedisUtils.set(gameconst.RedisKey.NORMAL_ONLINE_NUM + str(gameconfig.serverId()), self.accountNumCounter.dataSum - self.SVIPOnlineNum.dataSum)

    def onAccountLogin(self, accountName, devicePlatId, box, accountType, centralServerId, sessionIdStr):
        LOG_IFO("onAccountLogin::", accountName, devicePlatId, box, accountType, centralServerId, sessionIdStr)
        realAccountName = utils.mixRealAccountName(accountType, accountName)
        if realAccountName in self.kickAccountSet:
            self.onKickAccount(accountType, accountName, gameconst.OFFLINE_REASON_KICK_BY_CENTRAL_SERVER)
        else:
            self.account2box[realAccountName] = box

        if gameconfig.enableCentralLogin():
            self.notifyCentralServerOnline(accountName, accountType, centralServerId, sessionIdStr)

    def onAccountCreated(self, accountName, devicePlatId, isNew, channelId):
        LOG_IFO("onAccountCreated::", accountName, devicePlatId, isNew, channelId)
        # add account online num
        self.accountNumCounter.incSum(self)

        # 统计注册人数
        if isNew:
            self.accountRegNum.incSum(self)
            self.updateTodayRegNum()

        curPlat = self.playerNumPlat.setdefault(devicePlatId, {})
        curNum = curPlat.get(channelId, 0)
        self.playerNumPlat[devicePlatId][channelId] = curNum + 1
        
        redisUtils.RedisUtils.getSVIPFlag(accountName, self._onIncSVIPAccount)

    def onKickAccount(self, accountType, accountName, kickReason):
        realAccountName = utils.mixRealAccountName(accountType, accountName)
        self.kickAccountSet.discard(realAccountName)
        self.doOnOthersBaseByAccountName([realAccountName, ], 'kickAccount',
            (kickReason, accountName, accountType), self, 'onKickAccountFail',
                                         (realAccountName,))

    def onKickAccountFail(self, failOpenIds, realAccountName):
        LOG_WARN("onKickAccountFail", failOpenIds, realAccountName)
        self.kickAccountSet = set.union(self.kickAccountSet, set(realAccountName))
        self.addTimerCB(30, 'rmFromKickAccountSet', (realAccountName,), gametimer.TIMER_TAG_REMOVE_FROM_KICK_ACCOUNT_SET)

    def rmFromKickAccountSet(self, realAccountName):
        self.kickAccountSet.discard(realAccountName)

    def doOnOthersBaseByAccountName(self, otherAccountNames, otherMethod, otherArgs, failCallbackBox, failCallbackMethod, failCallbackArgs):
        failAccounts = []
        for accName in otherAccountNames:
            if accName not in self.account2box:
                failAccounts.append(accName)
                continue

            otherBox = self.account2box[accName]
            getattr(otherBox, otherMethod)(*otherArgs)

        if failAccounts and failCallbackBox:
            failArgs = [failAccounts]
            if failCallbackArgs:
                failArgs.extend(failCallbackArgs)

            getattr(failCallbackBox, failCallbackMethod)(*failArgs)

    def getGlobalAccountNum(self):
        return self.accountNumCounter.dataSum

    def globalDataCounterCallback(self, counter, callback, args):
        getattr(counter, callback)(*args)

    def _initAccountRegNum(self, ret, num, insertId, err):
        if err:
            LOG_ERR('LoginStub::_initAccountRegSet query db err.', err)
            return

        self.accountRegNum.setSum(self, int(ret[0][0]))
        LOG_IFO('LoginStub::_initAccountRegSet init reg num:', self.accountRegNum.dataSum)

    def gmLookUpAccount(self, cbBox, realAccountName, uid, index, raw):
        accountBox = self.account2box.get(realAccountName, None)
        cbBox.onGmFindAccount(accountBox, realAccountName, index, raw, uid)

    def updateTodayRegNum(self):
        LOG_DBG("updateTodayRegNum", self.todayAccountRegNumTs)
        if utils.checkDiffDay(self.todayAccountRegNumTs, utils.curTS(), gameconst.GENERAL_CYCLE_TIME):
            self.accountTodayRegNum.setSum(self, 0)
            self.todayAccountRegNumTs = utils.curTS()
            LOG_DBG("reset")

        self.accountTodayRegNum.incSum(self)

