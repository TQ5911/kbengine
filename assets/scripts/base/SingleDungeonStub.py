# -*- codinf: utf-8 -*-

from KBEDebug import *
import KBEngine

import gameconst
import gameengine
import gamebase
import gametimer
import gamesql
import utils
import gameconfig
import userType
import formula

import iDungeonStub
import iDungeonStubMonster
import dungeon
import gamePlay_gamePlay as DDID

import message_Message_def as M_M_DD


class SingleDungeonStub(iDungeonStub.IDungeonStub, iDungeonStubMonster.IDungeonStubMonster):

    def __init__(self):
        super(SingleDungeonStub, self).__init__()

    def doNext(self):
        super(SingleDungeonStub, self).doNext()
        self.pyAddTimer(60, 60, gametimer.TIMER_DUNGEON_CHECK_DESTROY)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.TIMER_DUNGEON_CHECK_DESTROY:
            self._checkDungeonSpaceDestroy()
        else:
            super(SingleDungeonStub, self).onTimer(tid, userArg)

    def _checkDungeonSpaceDestroy(self):
        spacesToDestory = []
        spacesToKickOut = []
        now = utils.curTS()
        for _spaceNo, _sVal in self.spaces.items():
            if now - _sVal.tCreate > 60*DDID.datas[self.dungeonNo]['timeOut'] + 2:
                spacesToKickOut.append(_spaceNo)
                continue

            fVal = self.founders.getFounderVal(_sVal.ownerGbId, _sVal.spaceUUID)

            if (not (fVal and fVal.hasAvatar())) and _sVal.isCompleted():
                spacesToDestory.append((_spaceNo, _sVal.spaceUUID, 'space complete'))
                continue

            if now - _sVal.tCreate > 60*2:
                if not fVal:
                    spacesToDestory.append((_spaceNo, _sVal.spaceUUID, 'no founder'))
                elif not fVal.hasAvatar():
                    spacesToDestory.append((_spaceNo, _sVal.spaceUUID, 'space no avatar'))

        for _spaceNo, spaceUUID, reason in spacesToDestory:
            self.destoryDungeonSpace(_spaceNo, spaceUUID, reason)

        for _spaceNo in spacesToKickOut:
            self._kickoutPlayer(_spaceNo)

    def onDungeonSpaceGone(self, spaceNo, reason):
        if reason == gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH:
            LOG_ERR("SingleDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                sVal = self.spaces[spaceNo]
                if sVal.destroyTimer:
                    self.cancelTimerCB(sVal.destroyTimer, gametimer.TIMER_TAG_DESTORY_DUNGEON_SPACE_DELAY)
                sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)
                sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
                self.cancelSpaceEntitiesLoadingProcess(spaceNo)
                sVal.spaceBox.doEntireDestroy(False, False)
                self.spaces.pop(spaceNo)

                _fVal = self.founders.getFounderVal(sVal.ownerGbId, sVal.spaceUUID)
                if _fVal:
                    self.founders.destoryFounder(sVal.ownerGbId, sVal.spaceUUID)

    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        LOG_INFO('destoryDungeonSpace', spaceNo, spaceUUID, reason)
        if spaceNo not in self.spaces:
            LOG_ERR('wl: destoryDungeonSpace cannot find space:', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        if _sVal.spaceUUID != spaceUUID:
            LOG_ERR("destoryDungeonSpace:: spaceUUID not match", spaceNo, spaceUUID, _sVal.spaceUUID)
            return

        _fVal = self.founders.getFounderVal(_sVal.ownerGbId, _sVal.spaceUUID)
        if _fVal\
                and _sVal.spaceUUID == _fVal.spaceUUID\
                and _fVal.hasAvatar()\
                and not utils.checkBoxOffline(_fVal.playerBox):

            self._kickoutPlayer(spaceNo)
            if _sVal.destroyTimer:
                self.cancelTimerCB(_sVal.destroyTimer, gametimer.TIMER_TAG_DESTORY_DUNGEON_SPACE_DELAY)
                _sVal.destroyTimer = 0
            _sVal.destroyTimer = self.asyncCallbackAfter(2, gametimer.TIMER_TAG_DESTORY_DUNGEON_SPACE_DELAY)._destoryDungeonSpaceDelay(spaceNo, spaceUUID,
                                                                                              reason)
            return

        # 【副本服务端报错】
        # 销毁时停止所有该space的completeCallback
        _sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)
        _sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
        # 【大量机器人新号登录后立刻下线后副本报错】
        self.cancelSpaceEntitiesLoadingProcess(spaceNo)

        _sVal.spaceBox.doEntireDestroy(False, False)
        self.spaces.pop(spaceNo)

        _fVal = self.founders.getFounderVal(_sVal.ownerGbId, _sVal.spaceUUID)
        if _fVal and _fVal.spaceUUID == spaceUUID:
            self.founders.destoryFounder(_sVal.ownerGbId, _sVal.spaceUUID)

    def _destoryDungeonSpaceDelay(self, spaceNo, spaceUUID, reason):
        LOG_INFO("_destoryDungeonSpaceDelay::", spaceNo, spaceUUID, reason)
        if spaceNo not in self.spaces:
            return

        _sVal = self.spaces[spaceNo]
        if _sVal.spaceUUID != spaceUUID:
            return

        if _sVal.destroyTimer:
            self.cancelTimerCB(_sVal.destroyTimer, gametimer.TIMER_TAG_DESTORY_DUNGEON_SPACE_DELAY)
            _sVal.destroyTimer = 0

        self.destoryDungeonSpace(spaceNo, spaceUUID, reason)

    def _kickoutPlayer(self, spaceNo):
        LOG_INFO('_kickoutPlayer', spaceNo)
        if spaceNo not in self.spaces:
            LOG_ERR('wl: _kickoutPlayer: cannot find space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        fVal = self.founders.getFounderVal(_sVal.ownerGbId, _sVal.spaceUUID)
        if fVal and _sVal.spaceUUID == fVal.spaceUUID and fVal.hasAvatar() and fVal.playerBox and not utils.checkBoxOffline(fVal.playerBox):
            fVal.playerBox.cell.destroyFromNewbieDungeon(self.dungeonNo)
        elif not _sVal.isToDestory():
            self.destoryDungeonSpace(spaceNo, _sVal.spaceUUID, 'force destroy')

    def getDungeonSpaceRange(self):
        enterType = DDID.datas[self.dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.SINGLE)
        if enterType==gameconst.DungeonEnterTypeEnum.BOTH:
            return gameconst.SpaceType.getSingleDungeonSpaceRange(self.dungeonNo)
        else:
            return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)


    def applyCreateDungeon(self, playerBox, gbId, teamUUID, extraData):
        LOG_INFO("applyCreateDungeon::", playerBox, gbId, teamUUID, extraData)
        if self.dungeonNo != extraData['dungeonNo']:
            LOG_ERR('applyCreateDungeon: SingleDungeonStub mismatch')
            return

        def _getEntranceByDungeonNo():
            dunSData = utils.getDunStructModData(self.dungeonNo)
            if 'BornPos' in dunSData:
                d, *_ = dunSData['BornPos'].values()
                return formula.bornPosFromDunData(d)

        if not extraData.get('position'):
            extraData['position'] = _getEntranceByDungeonNo() or ()

        if self.founders.getFounderVal(gbId, 0):
            LOG_ERR("applyCreateDungeon:: try create single dungeon while creating...", playerBox, gbId, teamUUID, extraData)
            return

        if extraData.get('inSpaceUUID') and not extraData.get('dungeonPlayMode', None):
            _fVal = self.founders.getFounderVal(gbId, extraData['inSpaceUUID'])
            if _fVal and _fVal.spaceNo in self.spaces and not self.spaces[_fVal.spaceNo].isCompleted():
                if _fVal.hasAvatar():
                    LOG_INFO('single dungeon not complete', gbId, self.dungeonNo)
                    playerBox.onMessagePre(M_M_DD.datas.dungeonRefused, [])
                else:
                    self.onLoadDungeonSpaceReady(_fVal.spaceNo, playerBox, gbId, teamUUID, extraData)
                return

        self.founders.addFounder(0, 0, gbId, playerBox)
        self.createDungeonSpaceRemote(playerBox, gbId, teamUUID, extraData)

    def _getDungeonSpaceWeight(self, enterNum=1) -> int:
        # 针对新手第一个副本调大
        if self.dungeonNo == gameconst.FIRST_NEWBIE_DUNGEON_NO:
            enterNum = gameconfig.firstDungeonWeight()

        return utils.calcSpaceWeight(enterNum, False, gameconst.EntNumPerPlayerInAOI.singleDungeon)

    def _getDungeonSpaceVal(self, spaceNo, _, gbId, teamUUID, extra):
        return dungeon.SingleDungeonSpaceVal(
            spaceNo, 0, None, None, gbId, spaceLevel=extra.get('spaceLevel',1))

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, gbId, teamUUID, extra):
        if spaceNo not in self.spaces:
            LOG_ERR('wl: createCellEntity cannot find space:', spaceNo)
            return
        _sVal = self.spaces[spaceNo]
        self.founders.destoryFounder(_sVal.ownerGbId, 0)
        self.founders.addFounder(spaceNo, _sVal.spaceUUID, gbId, playerBox)

        # ready enter dungeon first
        self.onLoadDungeonSpaceReady(spaceNo, playerBox, gbId, teamUUID, extra)

        # use iCreateDungeonMonster function
        return super(SingleDungeonStub, self)._loadDungeonSpaceEntities(
            spaceNo, playerBox, gbId, teamUUID, extra)

    def onLoadDungeonSpaceReady(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        _sVal = self.spaces[spaceNo]
        if playerBox:
            # calculate tDungeonLostTime to client
            # endTime = int(_sVal.tCreate + DDID.datas[self.dungeonNo]['timeOut'] * 60)
            # playerBox.client.changeDungeonRemainTime(spaceNo, endTime)
            if 'isNewbie' in extra:
                playerBox.onNewbieDungeonReady(_sVal.spaceBox, _sVal.spaceMgr, _sVal.spaceMgr.id, spaceNo)
            elif 'isTutorialDun' in extra:
                playerBox.onCommTutorialDungeonReady(_sVal.spaceBox, _sVal.spaceMgr, _sVal.spaceMgr.id, spaceNo)
            else:
                playerBox.cell.onSingleDungeonSpaceReady(_sVal.spaceBox, _sVal.spaceMgr, _sVal.spaceMgr.id, spaceNo, playerBox, playerGbId, teamUUID, extra)

    def enterDungeonSpaceSuccess(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        LOG_INFO('wl :enterDungeonSpaceSuccess', spaceNo, playerBox, playerGbId, extra['spaceUUID'])
        if spaceNo not in self.spaces:
            LOG_ERR('wl: enterDungeonSpaceSuccess cannot find space:', spaceNo)
            return

        _fVal = self.founders.getFounderVal(playerGbId, extra['spaceUUID'])
        if not _fVal:
            LOG_ERR('wl: enterDungeonSpaceSuccess cannot find founder', spaceNo, playerGbId, playerBox.id)
            return

        _fVal.onAvatarEnter(playerGbId)

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        LOG_INFO('wl :leaveDungeonSpaceSucc', spaceNo, playerBox, playerGbId, teamUUID, extra)
        _fVal = self.founders.getFounderVal(playerGbId, extra['spaceUUID'])
        if not _fVal:
            #【【服务端log】[SingleDungeonStub(22019)]
            LOG_WARN('wl: leaveDungeonSpaceSucc cannot find founder, reason: re-enter', 
                     spaceNo, playerGbId, playerBox.id)
            return

        _fVal.onAvatarLeave(playerGbId, False)

        if spaceNo in self.spaces:
            _sVal = self.spaces[spaceNo]

            if _sVal.isToDestory():
                self.destoryDungeonSpace(spaceNo, _sVal.spaceUUID, 'leave destroy')
            else:
                self.completeSingleDungeonForce(spaceNo, playerGbId, False)

    def onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp):
        return self._onReliveInDungeon(spaceNo, playerBox, playerGbId, reliveType, reliveHp)

    def onAvatarOffline(self, spaceNo, playerGbId):
        LOG_INFO('wl :onAvatarOffline', spaceNo, playerGbId)
        if spaceNo not in self.spaces:
            LOG_WARN('wl: onAvatarOffline::cannot get space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        _fVal = self.founders.getFounderVal(playerGbId, _sVal.spaceUUID)
        if not _fVal:
            LOG_ERR('wl: onAvatarOffline cannot find Founder', spaceNo, playerGbId)
            return

        _fVal.onAvatarLeave(playerGbId, True)
        self.completeSingleDungeon(spaceNo, playerGbId, False, 0)

    def onDungeonStarted(self, spaceNo, tCreate):
        LOG_INFO('onDungeonStarted::', spaceNo, tCreate)
        if spaceNo not in self.spaces:
            LOG_ERR('onDungeonStarted::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.tCreate = tCreate or utils.curTS()
        sVal.spaceMgr.cell.onDungeonStarted(sVal.tCreate)

    def onDungeonStartChallenge(self, spaceNo, endTime):
        LOG_INFO('onDungeonStartChallenge::', spaceNo, endTime)
        if spaceNo not in self.spaces:
            LOG_ERR('onDungeonStartChallenge::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.challengeEndTime = endTime
        sVal.spaceMgr.cell.onDungeonStartChallenge(sVal.challengeEndTime)

    def completeSingleDungeonForce(self, spaceNo, playerGbId, win):
        LOG_INFO("completeSingleDungeonForce::", spaceNo, playerGbId, win)
        if spaceNo not in self.spaces:
            LOG_WARN('_onSingleDungeonCompleted::cannot get space', spaceNo, playerGbId)
            return

        _sVal = self.spaces[spaceNo]
        if not _sVal.isActive():
            LOG_WARN('completeSingleDungeonForce:: already complete', spaceNo, _sVal.state, playerGbId)
            return

        if _sVal.ownerGbId != playerGbId:
            LOG_WARN("completeSingleDungeonForce:: ownerGbId not match", spaceNo, _sVal.ownerGbId, playerGbId)
            return

        if _sVal.completeDungeonTimer:
            self.cancelTimerCB(_sVal.completeDungeonTimer, gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)

        _sVal.spaceMgr.cell.destroyAllEntities()
        _sVal.spaceMgr.cell.onSingleDungeonCompleted(spaceNo, playerGbId, win, 0, _sVal.getElapsedTime())

        self._onSingleDungeonCompletedCallback(spaceNo, _sVal.spaceUUID, playerGbId, win)

    def _onSingleDungeonCompleted(self, spaceNo, playerGbId, win, delay):
        LOG_INFO('in completeSingleDungeon:', spaceNo, playerGbId, win, delay)
        if spaceNo not in self.spaces:
            if playerGbId:
                LOG_WARN('_onSingleDungeonCompleted::cannot get space', spaceNo, playerGbId)
            else:
                LOG_ERR('_onSingleDungeonCompleted::cannot get space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        if _sVal.completeDungeonTimer:
            LOG_WARN('_onSingleDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return
        if not _sVal.isActive():
            LOG_WARN('_onSingleDungeonCompleted:: already complete', spaceNo, _sVal.state, playerGbId)
            return

        if not playerGbId:
            LOG_WARN("_onSingleDungeonCompleted:: skip playerGbId check", spaceNo, playerGbId, _sVal.ownerGbId, win, delay)
        elif _sVal.ownerGbId != playerGbId:
            LOG_WARN("_onSingleDungeonCompleted:: ownerGbId not match", spaceNo, _sVal.ownerGbId, playerGbId)
            return

        _sVal.spaceMgr.cell.destroyAllEntities()
        _sVal.spaceMgr.cell.onSingleDungeonCompleted(spaceNo, playerGbId, win, delay, _sVal.getElapsedTime())

        if delay:
            _sVal.completeDungeonTimer = self.addTimerCB(delay, '_onSingleDungeonCompletedCallback',
                                                        (spaceNo, _sVal.spaceUUID, playerGbId, win), gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onSingleDungeonCompletedCallback(spaceNo, _sVal.spaceUUID, playerGbId, win)

    def completeSingleDungeon(self, spaceNo, gbId, win, delay):
        return self._onSingleDungeonCompleted(spaceNo, gbId, win, delay)

    def _onSingleDungeonCompletedCallback(self, spaceNo, spaceUUID, playerGbId, win):
        LOG_INFO('_onSingleDungeonCompletedCallback::', spaceNo, spaceUUID, playerGbId, win)
        if spaceNo not in self.spaces:
            LOG_ERR('_onSingleDungeonCompletedCallback::cannot get space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        _sVal.completeDungeonTimer = 0
        if _sVal.spaceUUID != spaceUUID:
            LOG_ERR('_onSingleDungeonCompletedCallback:: spaceUUID not match', _sVal.spaceUUID, spaceUUID)
            return

        if not _sVal.isActive():
            LOG_WARN('_onSingleDungeonCompletedCallback:: already complete', spaceNo, _sVal.state, playerGbId)
            return

        # 【副本服务端报错】
        # completecallback后取消其他completecallback回调
        _sVal.clearCompleteTimer()

        _sVal.completeDungeon(win)
        # self._kickoutPlayer(spaceNo)
        _sVal.toDestoryDungeon()
        self.destoryDungeonSpace(spaceNo, _sVal.spaceUUID, 'space complete' if win else 'space fail')

