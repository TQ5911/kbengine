# -*- coding: utf-8 -*-
import random
import KBEngine
from KBEDebug import *

import gameglobal
import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import gameconfig
import gameconst

import utils
import redisUtils


class WaitMapSpaceStub(iBaseNoCell.IBaseNoCell, iTimer.ITimer, iGlobal.IGlobal):
    def __init__(self):
        super(WaitMapSpaceStub, self).__init__()

        self.spaceFinder = WaitSpaceFinder(self)
        self.loginAccount = {}

    def doNext(self):
        LOG_INFO('WaitMapSpaceStub::doNext~')
        self._waitMapReportTimer = self.pyAddTimer(10, 10, gametimer.TIMER_ID_REPORT_WAITMAP_STATUS)

        cellAppCount = gameconfig.cellAppCount()
        baseMapId = gameconst.MapIdDef.mapWaitingServer
        for i in range(cellAppCount):
            spaceNo = baseMapId * gameconst.SPACE_NO_INTERVAL + i
            cellappIndex = i + 1
            KBEngine.createEntityAnywhere(
                'WaitMapSpace',
                {
                    'spaceno': spaceNo,
                    'spaceNo': spaceNo,
                    'position': gameconst.SPACE_FIX_POS,
                    'cellappIndex': cellappIndex,
                },
                lambda spaceBox, spaceNo=spaceNo: self._onCreateWaitMapSpace(spaceBox, spaceNo)
            )

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_ID_REPORT_WAITMAP_STATUS:
            self._reportWaitMapStatus()
        else:
            self._onTimerTrigger(tid, userArg)

    def _onCreateWaitMapSpace(self, spaceBox, spaceNo):
        LOG_INFO("WaitMapSpaceStub::_onCreateWaitMapSpace~", spaceNo)
        if spaceBox:
            self.spaceFinder.spaceCreated(spaceNo, spaceBox)
        else:
            LOG_INFO(f"WaitMapSpaceStub::_onCreateWaitMapSpace failed to create space: {spaceNo}.")

    def onWaitMapSpaceReady(self, spaceNo):
        LOG_INFO('WaitMapSpaceStub::onWaitMapSpaceReady', spaceNo)
        self.spaceFinder.spaceReady(spaceNo)

    def onWaitMapSpaceGone(self, spaceNo):
        LOG_INFO('WaitMapSpaceStub::onWaitMapSpaceGone', spaceNo)
        self.spaceFinder.spaceGone(spaceNo)

    def accountingLogin(self, accountName, accounting):
        if accountName in self.loginAccount:
            accounting.accountingLoginResult(gameconst.WaitMapLoginResult.OK)
            return

        accountLimit = utils.getWaitmapMaxOnline()
        if len(self.loginAccount) >= accountLimit:
            accounting.accountingLoginResult(gameconst.WaitMapLoginResult.ACCOUNT_LIMIT)
            return
        
        self.loginAccount[accountName] = {
            'box': accounting,
            'ts': utils.curTS()
        }
        accounting.accountingLoginResult(gameconst.WaitMapLoginResult.OK)

    def enterWaitMap(self, gbid, avataring):
        LOG_INFO("WaitMapSpaceStub::enterWaitMap~", gbid)
        spaceNo, spaceBox = self.spaceFinder.enterSpace(gbid, avataring)
        if not spaceNo or not spaceBox:
            return

        avataring.onEnterWaitMapSpace(spaceNo, spaceBox)

    def onPlayerLeave(self, gbid, spaceNo):
        LOG_INFO('WaitMapSpaceStub::onPlayerLeave~', gbid, spaceNo)
        self.spaceFinder.leaveSpace(gbid, spaceNo)

    def onPlayerLogout(self, accountName):
        LOG_INFO('WaitMapSpaceStub::opPlayerLogout~', accountName)
        self.loginAccount.pop(accountName, None)

    def _reportWaitMapStatus(self):
        serverId = gameconfig.serverId()
        actual = len(self.loginAccount)
        freeNum = max(0, utils.getWaitmapMaxOnline() - actual)
        nowTs = utils.curTS()
        LOG_DBG('WaitMapSpaceStub::_reportWaitMapStatus', serverId, actual, freeNum, nowTs)

        # 心跳保活：zset member=serverId, score=当前时间戳
        gameglobal.localBaseApp.getRedisClient().add(
            gameconst.RedisKey.WAITMAP_HEARTBEAT_KEY,
            {serverId: nowTs}
        )

        # 空闲人数：每 10s 快照一次，不实时更新
        redisUtils.RedisUtils.cmdSet(
            gameconst.RedisKey.WAITMAP_FREE_PREFIX + str(serverId),
            str(freeNum)
        )

class WaitSpaceFinder(object):
    def __init__(self, stub):
        self.stub = stub
        self.spaces = {}

    def spaceCreated(self, spaceNo, spaceBox):
        if spaceNo in self.spaces:
            LOG_ERR('WaitSpaceFinder::spaceCreated space exist.')
            return
        
        self.spaces[spaceNo] = {
            'spaceNo': spaceNo,
            'spaceBox': spaceBox,
            'ready': False,
            'avataring': {},
        }

    def spaceReady(self, spaceNo):
        if spaceNo not in self.spaces:
            LOG_ERR('WaitSpaceFinder::spaceReady no space:', spaceNo)
            return
        
        self.spaces[spaceNo]['ready'] = True

    def spaceGone(self, spaceNo):
        self.spaces.pop(spaceNo, None)

    def enterSpace(self, gbid, avataring):
        cellMaxPlayerNum = gameconfig.maxCellAvatarCount()
        countList = [len(spaceInfo['avataring']) for spaceInfo in self.spaces.values() if spaceInfo['ready']]
        minCount = min(countList) if countList else 0

        perCount = 20
        startCount = (minCount // perCount) * perCount

        # 线性填充
        for i in range(startCount, cellMaxPlayerNum+1, perCount):
            for spaceNo, spaceInfo in self.spaces.items():
                if not spaceInfo['ready']: continue
                if len(spaceInfo['avataring']) >= i: continue

                spaceInfo['avataring'][gbid] = {
                    'gbid': gbid,
                    'box': avataring,
                    'ts': utils.curTS(),
                }

                spaceBox = spaceInfo['spaceBox']
                if not spaceBox:
                    LOG_ERR('WaitSpaceFinder::enterSpace no space box:', spaceNo)
                    return 0, None

                return spaceNo, spaceBox

        LOG_ERR('WaitSpaceFinder::enterSpace no ready space yet.')
        return 0, None

    def leaveSpace(self, gbid, spaceNo):
        if spaceNo not in self.spaces:
            return
        self.spaces[spaceNo]['avataring'].pop(gbid, None)
