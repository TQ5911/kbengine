# -*- codinf: utf-8 -*-

from KBEDebug import *
import KBEngine

import gameconst
import gameengine
import gamebase
import gametimer
import gamesql
import utils
import userType
import formula

import iDungeonStub
import iDungeonStubMonster
import dungeon
import gamePlay_gamePlay as DDID

import message_Message_def as MMD


class SingleDungeonStub(iDungeonStub.IDungeonStub, iDungeonStubMonster.IDungeonStubMonster):

    def __init__(self):
        super(SingleDungeonStub, self).__init__()

        return

    def doNext(self):
        super(SingleDungeonStub, self).doNext()
        self.pyAddTimer(60, 60, gametimer.DUNGEON_CHECK_DESTROY)
        self.pyAddTimer(1, 0.1, gametimer.DUNGEON_ENTITY_GENERATOR)
        return

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if userArg == gametimer.DUNGEON_CHECK_DESTROY:
            self._checkDestroyDungeonSpace()
        elif userArg == gametimer.DUNGEON_ENTITY_GENERATOR:
            self.onTimerCreateEntity()
        else:
            super(SingleDungeonStub, self).onTimer(tid, userArg)

    def _checkDestroyDungeonSpace(self):
        spacesToDestory = []
        spacesToKickOut = []
        now = utils.curTS()
        for spaceNo, sVal in self.spaces.items():
            if now - sVal.tCreate > 60*DDID.datas[self.dungeonNo]['timeOut'] + 2:
                spacesToKickOut.append(spaceNo)
                continue

            fVal = self.founders.getFounderVal(sVal.ownerGbId, sVal.spaceUUID)

            if (not (fVal and fVal.hasAvatar())) and sVal.isCompleted():
                spacesToDestory.append((spaceNo, sVal.spaceUUID, 'space complete'))
                continue

            if now - sVal.tCreate > 60*2:
                if not fVal:
                    spacesToDestory.append((spaceNo, sVal.spaceUUID, 'no founder'))
                elif not fVal.hasAvatar():
                    spacesToDestory.append((spaceNo, sVal.spaceUUID, 'space no avatar'))

        for spaceNo, spaceUUID, reason in spacesToDestory:
            self.destoryDungeonSpace(spaceNo, spaceUUID, reason)

        for spaceNo in spacesToKickOut:
            self._kickoutPlayer(spaceNo)

    def onDungeonSpaceGone(self, spaceNo, reason):
        if reason == gameconst.OnLoseCellReason.CELLAPP_DEATH:
            LOG_ERR("SingleDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                sVal = self.spaces[spaceNo]
                if sVal.destroyTimer:
                    self.cancelTimerCB(sVal.destroyTimer, gametimer.TIMER_TAG_DESTORY_DUNGEON_SPACE_DELAY)
                sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)
                sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
                self.cancelSpaceEntitiesLoadingProcess(spaceNo)
                sVal.spaceBox.entireDestroy(False, False)
                self.spaces.pop(spaceNo)

                fVal = self.founders.getFounderVal(sVal.ownerGbId, sVal.spaceUUID)
                if fVal:
                    self.founders.destoryFounder(sVal.ownerGbId, sVal.spaceUUID)

    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        LOG_IFO('destoryDungeonSpace', spaceNo, spaceUUID, reason)
        if spaceNo not in self.spaces:
            LOG_ERR('wl: destoryDungeonSpace cannot find space:', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        if sVal.spaceUUID != spaceUUID:
            LOG_ERR("destoryDungeonSpace:: spaceUUID not match", spaceNo, spaceUUID, sVal.spaceUUID)
            return

        fVal = self.founders.getFounderVal(sVal.ownerGbId, sVal.spaceUUID)
        if fVal and sVal.spaceUUID == fVal.spaceUUID and fVal.hasAvatar() and not utils.checkBoxOffline(fVal.playerBox):
            self._kickoutPlayer(spaceNo)
            if sVal.destroyTimer:
                self.cancelTimerCB(sVal.destroyTimer, gametimer.TIMER_TAG_DESTORY_DUNGEON_SPACE_DELAY)
                sVal.destroyTimer = 0
            sVal.destroyTimer = self.toCallbackAfter(2, gametimer.TIMER_TAG_DESTORY_DUNGEON_SPACE_DELAY)._destoryDungeonSpaceDelay(spaceNo, spaceUUID,
                                                                                              reason)
            return

        # 【副本服务端报错】
        # 销毁时停止所有该space的completeCallback
        sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)
        sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
        # 【大量机器人新号登录后立刻下线后副本报错】
        self.cancelSpaceEntitiesLoadingProcess(spaceNo)

        sVal.spaceBox.entireDestroy(False, False)
        self.spaces.pop(spaceNo)

        fVal = self.founders.getFounderVal(sVal.ownerGbId, sVal.spaceUUID)
        if fVal and fVal.spaceUUID == spaceUUID:
            self.founders.destoryFounder(sVal.ownerGbId, sVal.spaceUUID)

    def _destoryDungeonSpaceDelay(self, spaceNo, spaceUUID, reason):
        LOG_IFO("_destoryDungeonSpaceDelay::", spaceNo, spaceUUID, reason)
        if spaceNo not in self.spaces:
            return

        sVal = self.spaces[spaceNo]
        if sVal.spaceUUID != spaceUUID:
            return

        if sVal.destroyTimer:
            self.cancelTimerCB(sVal.destroyTimer, gametimer.TIMER_TAG_DESTORY_DUNGEON_SPACE_DELAY)
            sVal.destroyTimer = 0

        self.destoryDungeonSpace(spaceNo, spaceUUID, reason)

    def _kickoutPlayer(self, spaceNo):
        LOG_IFO('_kickoutPlayer', spaceNo)
        if spaceNo not in self.spaces:
            LOG_ERR('wl: _kickoutPlayer: cannot find space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        fVal = self.founders.getFounderVal(sVal.ownerGbId, sVal.spaceUUID)
        if fVal and sVal.spaceUUID == fVal.spaceUUID and fVal.hasAvatar() and fVal.playerBox and not utils.checkBoxOffline(fVal.playerBox):
            fVal.playerBox.cell.destroyFromNewbieDungeon(self.dungeonNo)
        elif not sVal.isToDestory():
            self.destoryDungeonSpace(spaceNo, sVal.spaceUUID, 'force destroy')

    def getDungeonSpaceRange(self):
        enterType = DDID.datas[self.dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.SINGLE)
        if enterType==gameconst.DungeonEnterTypeEnum.BOTH:
            return gameconst.SpaceType.getSingleDungeonSpaceRange(self.dungeonNo)
        else:
            return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)


    def applyCreateDungeon(self, playerBox, gbId, teamUUID, extra):
        LOG_IFO("applyCreateDungeon::", playerBox, gbId, teamUUID, extra)
        if self.dungeonNo != extra['dungeonNo']:
            LOG_ERR('applyCreateDungeon: SingleDungeonStub mismatch')
            return

        def _getEntranceByDungeonNo():
            dunSData = utils.getDunStructModData(self.dungeonNo)
            if 'BornPos' in dunSData:
                d, *_ = dunSData['BornPos'].values()
                return formula.bornPosFromDunData(d)

        if not extra.get('position'):
            extra['position'] = _getEntranceByDungeonNo() or ()

        if self.founders.getFounderVal(gbId, 0):
            LOG_ERR("applyCreateDungeon:: try create single dungeon while creating...", playerBox, gbId, teamUUID, extra)
            return

        if extra.get('inSpaceUUID') and not extra.get('dungeonPlayMode', None):
            fVal = self.founders.getFounderVal(gbId, extra['inSpaceUUID'])
            if fVal and fVal.spaceNo in self.spaces and not self.spaces[fVal.spaceNo].isCompleted():
                if fVal.hasAvatar():
                    LOG_IFO('single dungeon not complete', gbId, self.dungeonNo)
                    playerBox.onMessagePre(MMD.datas.dungeonRefused, [])
                else:
                    self.onLoadDungeonSpaceReady(fVal.spaceNo, playerBox, gbId, teamUUID, extra)
                return

        self.founders.addFounder(0, 0, gbId, playerBox)
        self.createDungeonSpaceRemote(playerBox, gbId, teamUUID, extra)

    def _getDungeonSpaceVal(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        return dungeon.SingleDungeonSpaceVal(spaceNo, 0, None, None, playerGbId, spaceLevel=extra.get('spaceLevel',1))

    def _getDungeonSpaceWeight(self, enterNum=1) -> int:
        return utils.calcSpaceWeight(enterNum, False, gameconst.EntNumPerPlayerInAOI.singleDungeon)

    def _needSpaceMgr(self, spaceNo):
        return True

    # def _dungeonSpaceEntitiesGen(self, dungeonEntities):
    #     for entType, mProps in dungeonEntities:
    #         yield (entType, mProps)

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        if spaceNo not in self.spaces:
            LOG_ERR('wl: createCellEntity cannot find space:', spaceNo)
            return
        sVal = self.spaces[spaceNo]
        self.founders.destoryFounder(sVal.ownerGbId, 0)
        self.founders.addFounder(spaceNo, sVal.spaceUUID, playerGbId, playerBox)

        # ready enter dungeon first
        self.onLoadDungeonSpaceReady(spaceNo, playerBox, playerGbId, teamUUID, extra)

        # use iCreateDungeonMonster function
        return super(SingleDungeonStub, self)._loadDungeonSpaceEntities(
            spaceNo, playerBox, playerGbId, teamUUID, extra)

    def onLoadDungeonSpaceReady(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        sVal = self.spaces[spaceNo]
        if playerBox:
            # calculate tDungeonLostTime to client
            # endTime = int(sVal.tCreate + DDID.datas[self.dungeonNo]['timeOut'] * 60)
            # playerBox.client.changeDungeonRemainTime(spaceNo, endTime)
            if 'isNewbie' in extra:
                playerBox.onNewbieDungeonReady(sVal.spaceBox, sVal.spaceMgr, sVal.spaceMgr.id, spaceNo)
            elif 'isTutorialDun' in extra:
                playerBox.onCommTutorialDungeonReady(sVal.spaceBox, sVal.spaceMgr, sVal.spaceMgr.id, spaceNo)
            else:
                playerBox.cell.onSingleDungeonSpaceReady(sVal.spaceBox, sVal.spaceMgr, sVal.spaceMgr.id, spaceNo, playerBox, playerGbId, teamUUID, extra)

    def enterDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        LOG_IFO('wl :enterDungeonSpaceSucc', spaceNo, playerBox, playerGbId, extra['spaceUUID'])
        if spaceNo not in self.spaces:
            LOG_ERR('wl: enterDungeonSpaceSucc cannot find space:', spaceNo)
            return

        fVal = self.founders.getFounderVal(playerGbId, extra['spaceUUID'])
        if not fVal:
            LOG_ERR('wl: enterDungeonSpaceSucc cannot find founder', spaceNo, playerGbId, playerBox.id)
            return

        fVal.onAvatarEnter(playerGbId)

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        LOG_IFO('wl :leaveDungeonSpaceSucc', spaceNo, playerBox, playerGbId, teamUUID, extra)
        fVal = self.founders.getFounderVal(playerGbId, extra['spaceUUID'])
        if not fVal:
            #【【服务端log】[SingleDungeonStub(22019)]
            LOG_WARN('wl: leaveDungeonSpaceSucc cannot find founder, reason: re-enter', spaceNo, playerGbId, playerBox.id)
            return

        fVal.onAvatarLeave(playerGbId, False)

        if spaceNo in self.spaces:
            sVal = self.spaces[spaceNo]

            if sVal.isToDestory():
                self.destoryDungeonSpace(spaceNo, sVal.spaceUUID, 'leave destroy')
            else:
                self.completeSingleDungeonForce(spaceNo, playerGbId, False)

    def onAvatarOffline(self, spaceNo, playerGbId):
        LOG_IFO('wl :onAvatarOffline', spaceNo, playerGbId)
        if spaceNo not in self.spaces:
            LOG_WARN('wl: onAvatarOffline::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        fVal = self.founders.getFounderVal(playerGbId, sVal.spaceUUID)
        if not fVal:
            LOG_ERR('wl: onAvatarOffline cannot find Founder', spaceNo, playerGbId)
            return

        fVal.onAvatarLeave(playerGbId, True)
        self.completeSingleDungeon(spaceNo, playerGbId, False, 0)

    def onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp):
        return self._onReliveInDungeon(spaceNo, playerBox, playerGbId, reliveType, reliveHp)

    def onDungeonStarted(self, spaceNo, tCreate):
        LOG_IFO('onDungeonStarted::', spaceNo, tCreate)
        if spaceNo not in self.spaces:
            LOG_ERR('onDungeonStarted::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.tCreate = tCreate or utils.curTS()
        sVal.spaceMgr.cell.onDungeonStarted(sVal.tCreate)

    def completeSingleDungeonForce(self, spaceNo, playerGbId, win):
        LOG_IFO("completeSingleDungeonForce::", spaceNo, playerGbId, win)
        if spaceNo not in self.spaces:
            LOG_WARN('_onSingleDungeonCompleted::cannot get space', spaceNo, playerGbId)
            return

        sVal = self.spaces[spaceNo]
        if not sVal.isActive():
            LOG_WARN('completeSingleDungeonForce:: already complete', spaceNo, sVal.state, playerGbId)
            return

        if sVal.ownerGbId != playerGbId:
            LOG_WARN("completeSingleDungeonForce:: ownerGbId not match", spaceNo, sVal.ownerGbId, playerGbId)
            return

        if sVal.completeDungeonTimer:
            self.cancelTimerCB(sVal.completeDungeonTimer, gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)

        sVal.spaceMgr.cell.destroyAllEntities()
        sVal.spaceMgr.cell.onSingleDungeonCompleted(spaceNo, playerGbId, win, 0, sVal.getElapsedTime())

        self._onSingleDungeonCompletedCallback(spaceNo, sVal.spaceUUID, playerGbId, win)

    def completeSingleDungeon(self, spaceNo, playerGbId, win, delay):
        return self._onSingleDungeonCompleted(spaceNo, playerGbId, win, delay)

    def _onSingleDungeonCompleted(self, spaceNo, playerGbId, win, delay):
        LOG_IFO('in completeSingleDungeon:', spaceNo, playerGbId, win, delay)
        if spaceNo not in self.spaces:
            if playerGbId:
                LOG_WARN('_onSingleDungeonCompleted::cannot get space', spaceNo, playerGbId)
            else:
                LOG_ERR('_onSingleDungeonCompleted::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        if sVal.completeDungeonTimer:
            LOG_WARN('_onSingleDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return
        if not sVal.isActive():
            LOG_WARN('_onSingleDungeonCompleted:: already complete', spaceNo, sVal.state, playerGbId)
            return

        if not playerGbId:
            LOG_WARN("_onSingleDungeonCompleted:: skip playerGbId check", spaceNo, playerGbId, sVal.ownerGbId, win, delay)
        elif sVal.ownerGbId != playerGbId:
            LOG_WARN("_onSingleDungeonCompleted:: ownerGbId not match", spaceNo, sVal.ownerGbId, playerGbId)
            return

        sVal.spaceMgr.cell.destroyAllEntities()
        sVal.spaceMgr.cell.onSingleDungeonCompleted(spaceNo, playerGbId, win, delay, sVal.getElapsedTime())

        if delay:
            sVal.completeDungeonTimer = self.addTimerCB(delay, '_onSingleDungeonCompletedCallback',
                                                        (spaceNo, sVal.spaceUUID, playerGbId, win), gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onSingleDungeonCompletedCallback(spaceNo, sVal.spaceUUID, playerGbId, win)

    def _onSingleDungeonCompletedCallback(self, spaceNo, spaceUUID, playerGbId, win):
        LOG_IFO('_onSingleDungeonCompletedCallback::', spaceNo, spaceUUID, playerGbId, win)
        if spaceNo not in self.spaces:
            LOG_ERR('_onSingleDungeonCompletedCallback::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.completeDungeonTimer = 0
        if sVal.spaceUUID != spaceUUID:
            LOG_ERR('_onSingleDungeonCompletedCallback:: spaceUUID not match', sVal.spaceUUID, spaceUUID)
            return

        if not sVal.isActive():
            LOG_WARN('_onSingleDungeonCompletedCallback:: already complete', spaceNo, sVal.state, playerGbId)
            return

        # 【副本服务端报错】
        # completecallback后取消其他completecallback回调
        sVal.clearCompleteTimer()

        sVal.completeDungeon(win)
        # self._kickoutPlayer(spaceNo)
        sVal.toDestoryDungeon()
        self.destoryDungeonSpace(spaceNo, sVal.spaceUUID, 'space complete' if win else 'space fail')
