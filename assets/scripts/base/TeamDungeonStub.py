# coding: utf-8
import KBEngine
from KBEDebug import *

import gameengine
import gameconst
import gametimer

import iDungeonStub
import iDungeonStubMonster

import dungeon

import formula
import utils
import dungeonSrc

import gamePlay_gamePlay as DDI


class TeamDungeonStub(iDungeonStubMonster.IDungeonStubMonster, iDungeonStub.IDungeonStub):
    """Implement of TeamDungeonStub"""

    def doNext(self):
        super(TeamDungeonStub, self).doNext()
        self.pyAddTimer(30, 30, gametimer.DUNGEON_CHECK_DESTROY)
        self.pyAddTimer(1, 0.1, gametimer.DUNGEON_ENTITY_GENERATOR)
        return

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if userArg == gametimer.DUNGEON_CHECK_DESTROY:
            self._checkDestroyDungeonSpace()
        elif userArg == gametimer.DUNGEON_ENTITY_GENERATOR:
            self.onTimerCreateEntity()
        else:
            super(TeamDungeonStub, self).onTimer(tid, userArg)

    def _checkDestroyDungeonSpace(self):
        now = utils.curTS()
        # LOG_DBG('_checkDestroyDungeonSpace:: {}'.format(now))
        # teamStub.destroyTeamDungeonDelay args list
        needDestroyList = []
        realDestroyList = []
        for spaceNo, sVal in self.spaces.items():
            if sVal.nDestoryCnt>3:
                LOG_ERR('_checkDestroyDungeonSpace: cannot destory space', spaceNo)
                continue

            if sVal.markCreate:
                # new dungeon, skip destroy once
                sVal.markCreate = False
                continue

            if sVal.markDestroy:
                if sVal.markDestroy < now:
                    realDestroyList.append((spaceNo, sVal.spaceUUID, 'time destory'))
                continue

            # extra kwargs in `team.TeamDungeonSpaceCacheVal.isDungeonSpaceCanBeDestoried`
            extraInfo = {'tCreate': sVal.tCreate,
                         'tState': sVal.state}

            needDestroyList.append((sVal.teamUUID,
                                    self.dungeonNo,
                                    spaceNo,
                                    'delay timeout destory',
                                    extraInfo))

        for nArgs in needDestroyList:
            _teamStub = gameengine.getTeamStub(nArgs[0])
            _teamStub.destroyTeamDungeonDelay(*nArgs)

        for rArgs in realDestroyList:
            self.destoryDungeonSpace(*rArgs)

    def onDungeonSpaceGone(self, spaceNo, reason):
        if reason == gameconst.OnLoseCellReason.CELLAPP_DEATH:
            LOG_ERR("TeamDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                sVal = self.spaces[spaceNo]
                sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
                sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
                _teamStub = gameengine.getTeamStub(sVal.teamUUID)
                _teamStub.onDestroyTeamDungeon(sVal.teamUUID, self.dungeonNo, spaceNo, sVal.spaceUUID)

                self.cancelSpaceEntitiesLoadingProcess(spaceNo)

                sVal.spaceBox.entireDestroy(False, False)
                self.spaces.pop(spaceNo)

    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        LOG_IFO('destoryDungeonSpace', spaceNo, reason)
        if spaceNo not in self.spaces:
            LOG_WARN('wl: destoryDungeonSpace cannot find space:', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        if spaceUUID and sVal.spaceUUID!=spaceUUID:
            LOG_WARN('destoryDungeonSpace:: spaceUUID not match {}!={}'.format(sVal.spaceUUID, spaceUUID))
            return

        now = utils.curTS()
        if not sVal.markDestroy:
            # delay destroy space
            sVal.markDestroy = utils.curTS() + 60
            # 【副本服务端报错】
            # 销毁时停止所有该space的completeCallback
            # 【【上灵试炼】组队进入单人副本，打完boss后再次进入副本，会出现报错】
            # 提前cancel的时机到markDestroy
            sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
            sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
            sVal.toDestoryDungeon()

            LOG_IFO('destoryDungeonSpace::space will be destroyed in next check,', spaceNo, sVal.markDestroy)
            _teamStub = gameengine.getTeamStub(sVal.teamUUID)
            _teamStub.onDestroyTeamDungeon(sVal.teamUUID, self.dungeonNo, spaceNo, spaceUUID)
            return

        # real destroy dungeon
        elif sVal.markDestroy < now:

            # 【大量机器人新号登录后立刻下线后副本报错】
            self.cancelSpaceEntitiesLoadingProcess(spaceNo)

            sVal.spaceBox.entireDestroy(False, False)
            self.spaces.pop(spaceNo)

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        LOG_IFO("leaveDungeonSpaceSucc::", spaceNo, playerBox, playerGbId, teamUUID, extra)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveDungeonSpaceSucc::cannot get space', spaceNo)
            return
        sVal = self.spaces[spaceNo]
        _teamStub = gameengine.getTeamStub(sVal.teamUUID)
        _teamStub.leaveTeamDungeon(playerBox, playerGbId, sVal.teamUUID, self.dungeonNo)

    def onAvatarOffline(self, spaceNo, playerGbId):
        LOG_IFO('onAvatarOffline::', spaceNo, playerGbId)
        if spaceNo not in self.spaces:
            LOG_ERR('onAvatarOffline::cannot get space', spaceNo)
            return
        sVal = self.spaces[spaceNo]
        _teamStub = gameengine.getTeamStub(sVal.teamUUID)
        _teamStub.onAvatarOffline(playerGbId, sVal.teamUUID, self.dungeonNo)

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

    def completeTeamDungeon(self, spaceNo, teamUUID, win, delay, reasonType):
        return self._onTeamDungeonCompleted(spaceNo, teamUUID, win, delay, reasonType)

    def _onTeamDungeonCompleted(self, spaceNo, teamUUID, win, delay, reasonType):
        LOG_IFO('in completeTeamDungeon:', spaceNo, teamUUID, win, delay, reasonType)
        if spaceNo not in self.spaces:
            if teamUUID:
                LOG_WARN('completeTeamDungeon:: cannot get space', spaceNo, teamUUID)
            else:
                LOG_ERR('completeTeamDungeon:: cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        if sVal.completeDungeonTimer:
            LOG_WARN('_onTeamDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return
        
        if sVal.markDestroy:
            LOG_WARN("_onTeamDungeonCompleted:: dungeon already mark destroy", spaceNo, teamUUID, win, delay)
            return

        if not sVal.isActive():
            LOG_WARN('_onTeamDungeonCompleted:: already complete', spaceNo, sVal.state)
            return

        if not teamUUID:
            LOG_WARN("_onTeamDungeonCompleted:: skip teamUUID check", spaceNo, teamUUID, sVal.teamUUID, win, delay)

        elif sVal.teamUUID != teamUUID:
            LOG_WARN("_onTeamDungeonCompleted:: taemUUID not match", spaceNo, sVal.teamUUID, teamUUID)
            return

        sVal.spaceMgr.cell.destroyAllEntities()
        sVal.completedReasonType = reasonType
        sVal.spaceMgr.cell.onTeamDungeonCompleted(spaceNo, teamUUID, win, delay, sVal.getElapsedTime(), 0, sVal.completedReasonType)
        if win:
            sVal.spaceMgr.cell.finishGuildDungeonTask()

        if delay:
            sVal.completeDungeonTimer = self.addTimerCB(
                delay, '_onTeamDungeonCompletedCallback',
                (spaceNo, sVal.spaceUUID, 'dungeon complete', win), gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onTeamDungeonCompletedCallback(spaceNo, sVal.spaceUUID, 'dungeon complete', win)

    def _onTeamDungeonCompletedCallback(self, spaceNo, spaceUUID, reason, win):
        LOG_IFO('_onTeamDungeonCompletedCallback::', spaceNo, spaceUUID, reason, win)
        if spaceNo not in self.spaces:
            LOG_ERR('_onTeamDungeonCompletedCallback::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.completeDungeonTimer = 0
        if sVal.spaceUUID != spaceUUID:
            LOG_ERR('_onTeamDungeonCompletedCallback:: spaceUUID not match', sVal.spaceUUID, spaceUUID)
            return

        if not sVal.isActive():
            LOG_WARN('_onTeamDungeonCompletedCallback:: already complete', spaceNo, sVal.state)
            return

        # 【副本服务端报错】
        # completecallback后取消其他completecallback回调
        sVal.clearCompleteTimer()

        sVal.completeDungeon(win)
        _teamStub = gameengine.getTeamStub(sVal.teamUUID)
        extraInfo = {
            'tCreate': sVal.tCreate,
            'tState': sVal.state,
            'forceDestroy': True,
            }
                     
        _teamStub.destroyTeamDungeonDelay(sVal.teamUUID, self.dungeonNo, spaceNo, reason, extraInfo)

    def doEnterDungeon(self, box, gbId, teamUUID, spaceNo, extra):
        if spaceNo not in self.spaces:
            LOG_ERR('spaceNo "{}" not found in spaces'.format(spaceNo))
            _teamStub = gameengine.getTeamStub(teamUUID)
            _teamStub.onEnterDungeonFailedSpaceNotFound(box, gbId, teamUUID, self.dungeonNo, spaceNo, extra)
            return

        spaceVal = self.spaces[spaceNo]

        if spaceVal.isCompleted():
            LOG_ERR("space already completed", spaceNo, spaceVal.spaceUUID)
            return

        if spaceVal.markDestroy:
            LOG_ERR('spaceNo "{}" already be destroy delay'.format(spaceNo))
            return

        # calculate tDungeonLostTime to client
        # endTime = int(spaceVal.tCreate + DDI.datas[self.dungeonNo]['timeOut'] * 60)
        # box.client.changeDungeonRemainTime(spaceNo, endTime)

        spaceBox = spaceVal.spaceBox
        spaceMgr = spaceVal.spaceMgr
        spaceMgr.cell.doEnterTeamDungeon(box, gbId, spaceVal.spaceUUID, spaceBox, extra)

    def applyCreateDungeon(self, box, gbId, teamUUID, extra):
        self.createDungeonSpaceRemote(box, gbId, teamUUID, extra)

    def _getDungeonSpaceVal(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        return dungeon.TeamDungeonSpaceVal(spaceNo=spaceNo,
                                           spaceUUID=0, spaceBox=None, spaceMgr=None,
                                           teamUUID=teamUUID, spaceLevel=extra['spaceLevel'], extraDic={'maxLevel':extra['maxLevel']})

    def _getDungeonSpaceWeight(self, enterNum=5) -> int:
        return utils.calcSpaceWeight(enterNum, False, gameconst.EntNumPerPlayerInAOI.teamDungeon)

    def _needSpaceMgr(self, spaceNo):
        return True

    def getDungeonSpaceRange(self):
        enterType = DDI.datas[self.dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.SINGLE)
        if enterType==gameconst.DungeonEnterTypeEnum.BOTH:
            return gameconst.SpaceType.getTeamDungeonSpaceRange(self.dungeonNo)
        else:
            return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        # ready first
        self.onLoadDungeonSpaceReady(playerBox, spaceNo, teamUUID, extra)
        # use iCreateDungeonMonster function
        return super(TeamDungeonStub, self)._loadDungeonSpaceEntities(
            spaceNo, playerBox, playerGbId, teamUUID, extra)

    def onLoadDungeonSpaceReady(self, playerBox, spaceNo, teamUUID, extra):
        LOG_IFO('onLoadDungeonSpaceReady::')
        _teamStub = gameengine.getTeamStub(teamUUID)
        _teamStub.onCreateTeamDungeon(teamUUID, self.dungeonNo, spaceNo, self.spaces[spaceNo].spaceUUID, playerBox, extra)

    def leaveTeamDungeon(self, spaceNo, teamID, src, playerBox):
        LOG_IFO("leaveTeamDungeon~ ", spaceNo, teamID, src, playerBox)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveTeamDungeon:: failed, missing space data', spaceNo, src, playerBox)
            return
        dungeonVal = self.spaces[spaceNo]
        founders = len(dungeonVal.founders)
        if founders <= 1:
            self.completeTeamDungeon(spaceNo, teamID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)
        else:
            playerBox.cell.selfLeaveTeamDungeon(src)

