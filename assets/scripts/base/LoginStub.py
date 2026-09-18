# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import urllib.parse
import collections
import json
import http
import functools

import gameconst
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
import LogTrackingMgr
import redisUtils
import proto.centralLogin_pb2 as centralLogin


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
        self.cacheSVIPSet = set()

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

    def onTimer(self, timerID, userArg):
        self._onTimerTrigger(timerID, userArg)
        if userArg == gametimer.LOGIN_STUB_ASYNC_TICK:
            self.connectAllCentralServer()

        elif userArg == gametimer.LOGIN_STUB_SERVERINFO_SYNC:
            if gameconfig.enableCentralLogin():
                self.updateServerInfo()
                if gameglobal.isBootstrap:
                    self.updateSVIPOnlineNum()

        elif userArg == gametimer.TIMER_LOGIN_STUB_ACTIVE_TICK:
            if gameconfig.enableCentralLogin():
                self.checkAllCentralServerActive()

        elif utils.isBelongTimerTag(userArg):
            self._onTimerCallback(timerID)

        elif userArg == gametimer.LOGIN_STUB_TLOG_GAMESVR_STATE:
            iZoneAreaID = gameconfig.serverId()
            gamelog.makeGameSvrStateLog(iZoneAreaID)

        elif userArg == gametimer.LOGIN_STUB_SYNC_INTERFACE_REGNUM:
            gameglobal.localBaseApp.notifyInterfaceSyncRegisterCount(self.accountRegNum.dataSum)
        
        elif userArg == gametimer.LOGIN_STUB_LOG_TRACKING_PCU:
            LogTrackingMgr.LogTrackingMgr.Server_Pcu(
                'LoginStub',
                '', 
                gameconfig.serverId(),
                self.getGlobalAccountNum(),
            )

    def getConfig(self):
        return gameconfig

    def onCentralServerConnected(self, centralServerId):
        LOG_INFO('onCentralServerConnected', centralServerId, KBEngine.getComponentGroupOrder())
        if KBEngine.getComponentGroupOrder()==1:
            self.tryRegisterLoginServer(centralServerId)

        if self.heartBeatTimer:
            self.pyDelTimer(self.heartBeatTimer, gametimer.TIMER_LOGIN_STUB_ACTIVE_TICK)

        self.heartBeatTimer = self.pyAddTimer(gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gameconst.CENTRAL_SERVICE_HEARTBEAT_INTERVAL, gametimer.TIMER_LOGIN_STUB_ACTIVE_TICK)

    def tryRegisterLoginServer(self, centralServerId):
        if KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_GAME_READY):
            self.registerServer(centralServerId)
        else:
            self.addTimerCB(
                5, 
                'tryRegisterLoginServer', 
                (centralServerId,), 
                gametimer.TIMER_TAG_TRY_REGISTER_SERVER)

    def onAccountDestroy(self, accountName, accountType, devicePlatId, centralServerId, channelId, sessionIdStr, userInfoId):
        LOG_INFO("onAccountDestroy", accountName, accountType, devicePlatId, centralServerId, channelId, sessionIdStr, userInfoId)
        realAccountName = utils.mixRealAccountName(accountType, accountName)
        self.account2box.pop(realAccountName, None)
        # deduct account online num
        self.accountNumCounter.decSum(self)

        _curPlat = self.playerNumPlat.setdefault(devicePlatId, {})
        _curNum = _curPlat.get(channelId, 0)
        self.playerNumPlat[devicePlatId][channelId] = max(_curNum - 1, 0)

        if gameconfig.enableCentralLogin():
            self.notifyCentralServerOffline(accountName, accountType, centralServerId, sessionIdStr, userInfoId)

        if accountName in self.cacheSVIPSet:
            self.cacheSVIPSet.remove(accountName)
            self.SVIPOnlineNum.decSum(self)
            LOG_INFO("remove from cacheSVIPSet", accountName, self.SVIPOnlineNum.dataSum)

    def _onIncSVIPAccount(self, accountName, cid, err, res):
        LOG_INFO("_onIncSVIPAccount", accountName, "cid", cid, "err", err, "res", res)
        if err:
            LOG_ERR("_onIncSVIPAccount", "err", err)
            return

        if res:
            resData = set(res.decode().split(','))
            if str(gameconst.UserTagType.GREEN_CODE) in resData:
                self.cacheSVIPSet.add(accountName)
                self.SVIPOnlineNum.incSum(self)
                LOG_INFO("_onIncSVIPAccount", "add to cacheSVIPSet", accountName, self.SVIPOnlineNum.dataSum)

    def updateSVIPOnlineNum(self):
        redisUtils.RedisUtils.cmdSet(gameconst.RedisKey.NORMAL_ONLINE_NUM + str(gameconfig.serverId()), self.accountNumCounter.dataSum - self.SVIPOnlineNum.dataSum)

    def onAccountLogin(self, accountName, devicePlatId, box, accountType, centralServerId, sessionIdStr, userInfoId):
        LOG_INFO("onAccountLogin::", accountName, devicePlatId, box, accountType, centralServerId, sessionIdStr, userInfoId)
        realAccountName = utils.mixRealAccountName(accountType, accountName)
        if realAccountName in self.kickAccountSet:
            self.onKickAccount(accountType, accountName, gameconst.OFFLINE_REASON_KICK_BY_CENTRAL_SERVER)
        else:
            self.account2box[realAccountName] = box

        if gameconfig.enableCentralLogin():
            self.notifyCentralServerOnline(accountName, accountType, centralServerId, sessionIdStr, userInfoId)

        self._checkQueuePass(accountName, accountType)

    def _checkQueuePass(self, accountName, accountType):
        if gameconfig.isWaitMapServer() or gameconfig.isCrossServer():
            return
        if accountType in (centralLogin.ACCOUNT_UNKNOW, centralLogin.ACCOUNT_BOT,
                           centralLogin.ACCOUNT_CROSS_SERVER, centralLogin.ACCOUNT_PASSWD):
            return
        redisUtils.RedisUtils.getQueuePass(accountName, functools.partial(self._onCheckQueuePass, accountName))

    def _onCheckQueuePass(self, accountName, cid, err, res):
        LOG_INFO("_onCheckQueuePass", accountName, cid, err, res)
        serverId = str(gameconfig.serverId())
        if err:
            LOG_WARN('checkQueuePass redis err', accountName, serverId, err)
            return

        passServerId = res.decode() if res else ''
        if passServerId == serverId:
            return

        redisUtils.RedisUtils.getTagTypeFlag(accountName, functools.partial(
            self._onCheckQueuePassTag, accountName, passServerId, serverId))

    def _onCheckQueuePassTag(self, accountName, passServerId, serverId, cid, err, res):
        LOG_INFO("_onCheckQueuePassTag", accountName, passServerId, serverId, cid, err, res)
        if res:
            tags = set(res.decode().split(','))
            if str(gameconst.UserTagType.WHITE_LIST) in tags or str(gameconst.UserTagType.GREEN_CODE) in tags:
                return
        LOG_WARN('checkQueuePass failed', accountName, 'passServerId', passServerId, 'serverId', serverId)

    def onAccountCreated(self, accountName, devicePlatId, isNew, channelId):
        LOG_INFO("onAccountCreated::", accountName, devicePlatId, isNew, channelId)
        # add account online num
        self.accountNumCounter.incSum(self)

        # 统计注册人数
        if isNew:
            self.accountRegNum.incSum(self)
            self.updateTodayRegNum()

        curPlat = self.playerNumPlat.setdefault(devicePlatId, {})
        _curNum = curPlat.get(channelId, 0)
        self.playerNumPlat[devicePlatId][channelId] = _curNum + 1
        
        redisUtils.RedisUtils.getTagTypeFlag(accountName, functools.partial(self._onIncSVIPAccount, accountName))

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

    def rmFromKickAccountSet(self, realAccountName):
        self.kickAccountSet.discard(realAccountName)

    def globalDataCounterCallback(self, counter, callback, args):
        getattr(counter, callback)(*args)

    def getGlobalAccountNum(self):
        return self.accountNumCounter.dataSum

    def _initAccountRegNum(self, ret, num, _, err):
        if err:
            LOG_ERR('LoginStub::_initAccountRegSet query db err.', err)
            return

        self.accountRegNum.setSum(self, int(ret[0][0]))
        LOG_INFO('LoginStub::_initAccountRegSet init reg num:', self.accountRegNum.dataSum)

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

