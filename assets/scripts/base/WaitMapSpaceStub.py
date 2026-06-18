# -*- coding: utf-8 -*-
import random
import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import gameconfig
import gameconst
import gameengine
import formula

import utils


class WaitMapSpaceStub(iBaseNoCell.IBaseNoCell, iTimer.ITimer, iGlobal.IGlobal):
    def __init__(self):
        super(WaitMapSpaceStub, self).__init__()

        self.spaceFinder = WaitSpaceFinder(self)
        self.loginAccount = {}

    def doNext(self):
        LOG_INFO('WaitMapSpaceStub::doNext~')
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

        accountLimit = 2000
        if len(self.loginAccount) > accountLimit:
            accounting.accountingLoginResult(gameconst.WaitMapLoginResult.ACCOUNT_LIMIT)
            return
        
        self.loginAccount[accountName] = {
            'box': accounting,
            'ts': utils.curTS()
        }
        accounting.accountingLoginResult(gameconst.WaitMapLoginResult.OK)

    def enterWaitMap(self, gbid, avataring):
        LOG_INFO("WaitMapSpaceStub::enterWaitMap~", gbid)
        spaceNo = self.spaceFinder.preEnterSpace(gbid, avataring)
        spaceNo and avataring.onEnterWaitMapSpace(spaceNo)

    def doEnterWaitMap(self, gbid, spaceNo):
        LOG_INFO("WaitMapSpaceStub::doEnterWaitMap~", gbid, spaceNo)
        self.spaceFinder.enterSpace(spaceNo, gbid)

    def onPlayerLeave(self, gbid, spaceNo):
        self.spaceFinder.leaveSpace(gbid, spaceNo)

    def onPlayerLogout(self, accountName):
        LOG_INFO('WaitMapSpaceStub::opPlayerLogout~', accountName)
        self.loginAccount.pop(accountName, None)

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

    def preEnterSpace(self, gbid, avataring):
        cellMaxPlayerNum = 2000
        # 线性填充
        for i in range(0, cellMaxPlayerNum, 50):
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
                    return 0

                return spaceNo

        LOG_ERR('WaitSpaceFinder::enterSpace no ready space yet.')
        return 0

    def enterSpace(self, spaceNo, gbid):
        if spaceNo not in self.spaces:
            LOG_ERR('WaitSpaceFinder::enterSpace no space:', spaceNo)
            return
        
        player = self.spaces[spaceNo]['avataring'].get(gbid, None)
        space = self.spaces[spaceNo]['spaceBox']
        if space and player:
            space.createCellNearSelf(player['box'])


    def leaveSpace(self, spaceNo, gbid):
        if spaceNo not in self.spaces:
            return
        self.spaces[spaceNo]['avataring'].discard(gbid)
