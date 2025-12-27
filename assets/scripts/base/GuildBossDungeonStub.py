# coding: utf-8
import KBEngine
from KBEDebug import *

import functools

import gameengine
import gameconst
import gametimer

import DungeonSettlement

import iDungeonStub
import iDungeonStubMonster

import dungeon

import formula
import utils

import gamePlay_gamePlay as DDI


class GuildBossDungeonStub(iDungeonStubMonster.IDungeonStubMonster, iDungeonStub.IDungeonStub):
    """Implement of GuildBossDungeonStub"""

    def doNext(self):
        super(GuildBossDungeonStub, self).doNext()
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
            super(GuildBossDungeonStub, self).onTimer(tid, userArg)

    def _checkDestroyDungeonSpace(self):
        now = utils.getNow()
        # DEBUG_MSG('_checkDestroyDungeonSpace:: {}'.format(now))
        # teamStub.destroyTeamDungeonDelay args list
        needDestroyList = []
        realDestroyList = []
        for spaceNo, sVal in self.spaces.items():
            if sVal.nDestoryCnt>3:
                ERROR_MSG('_checkDestroyDungeonSpace: cannot destory space', spaceNo)
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

            needDestroyList.append((sVal.guildUUID,
                                    self.dungeonNo,
                                    spaceNo,
                                    'delay timeout destory',
                                    extraInfo))

        for rArgs in realDestroyList:
            self.destoryDungeonSpace(*rArgs)

    def onDungeonSpaceGone(self, spaceNo, reason):
        if reason == gameconst.OnLoseCellReason.CELLAPP_DEATH:
            ERROR_MSG("GuildBossDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                sVal = self.spaces[spaceNo]
                sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_GUILD_BOSS_CHALLENGE_DUNGEON_COMPLETED_CALLBACK)
                sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)

                self.cancelSpaceEntitiesLoadingProcess(spaceNo)

                sVal.spaceBox.entireDestroy(False, False)
                self.spaces.pop(spaceNo)

    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        DEBUG_MSG('destoryDungeonSpace', spaceNo, reason)
        if spaceNo not in self.spaces:
            WARNING_MSG('wl: destoryDungeonSpace cannot find space:', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        if spaceUUID and sVal.spaceUUID!=spaceUUID:
            WARNING_MSG('destoryDungeonSpace:: spaceUUID not match {}!={}'.format(sVal.spaceUUID, spaceUUID))
            return

        now = utils.getNow()
        if not sVal.markDestroy:
            sVal.markDestroy = utils.getNow() + 60
            sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_GUILD_BOSS_CHALLENGE_DUNGEON_COMPLETED_CALLBACK)
            sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
            sVal.toDestoryDungeon()

            DEBUG_MSG('destoryDungeonSpace::space will be destroyed in next check,', spaceNo, sVal.markDestroy)
            return

        # real destroy dungeon
        elif sVal.markDestroy < now:

            # 【大量机器人新号登录后立刻下线后副本报错】
            self.cancelSpaceEntitiesLoadingProcess(spaceNo)

            sVal.spaceBox.entireDestroy(False, False)
            self.spaces.pop(spaceNo)

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGBID, guildUUID, extra):
        DEBUG_MSG("leaveDungeonSpaceSucc::", spaceNo, playerBox, playerGBID, guildUUID, extra)
        if spaceNo not in self.spaces:
            ERROR_MSG('leaveDungeonSpaceSucc::cannot get space', spaceNo)
            return
        dungeonVal = self.spaces[spaceNo]
        founderVal = dungeonVal.founders.getFounderVal(playerGBID)
        if founderVal:
            founderVal.onAvatarLeave(playerGBID, isOffline=False)

    def onAvatarOffline(self, spaceNo, playerGbId):
        DEBUG_MSG('onAvatarOffline::', spaceNo, playerGbId)
        if spaceNo not in self.spaces:
            ERROR_MSG('onAvatarOffline::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        founderVal = sVal.founders.getFounderVal(playerGbId)
        founderVal.onAvatarLeave(playerGbId, isOffline=True)

    def onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp):
        return self._onReliveInDungeon(spaceNo, playerBox, playerGbId, reliveType, reliveHp)

    def onDungeonStarted(self, spaceNo, tCreate):
        DEBUG_MSG('onDungeonStarted::', spaceNo, tCreate)
        if spaceNo not in self.spaces:
            ERROR_MSG('onDungeonStarted::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.tCreate = tCreate or utils.getNow()
        sVal.spaceMgr.cell.onDungeonStarted(sVal.tCreate)

    def completeGuildBossDungeon(self, spaceNo, guildUUID, win, delay):
        INFO_MSG('in completeGuildBossDungeon:', spaceNo, guildUUID, win, delay)
        self._onGuildBossDungeonCompleted(spaceNo, guildUUID, win, delay)

    def _onGuildBossDungeonCompleted(self, spaceNo, guildUUID, win, delay):
        INFO_MSG('in _onGuildBossDungeonCompleted:', spaceNo, guildUUID, win, delay)
        if spaceNo not in self.spaces:
            if guildUUID:
                WARNING_MSG('_onGuildBossDungeonCompleted:: cannot get space', spaceNo, guildUUID)
            else:
                ERROR_MSG('_onGuildBossDungeonCompleted:: cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        if sVal.completeDungeonTimer:
            WARNING_MSG('_onGuildBossDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return
        if sVal.markDestroy:
            WARNING_MSG("_onGuildBossDungeonCompleted:: dungeon already mark destroy", spaceNo, guildUUID, win, delay)
            return
        if not sVal.isActive():
            WARNING_MSG('_onGuildBossDungeonCompleted:: already complete', spaceNo, sVal.state)
            return
        if not guildUUID:
            WARNING_MSG("_onGuildBossDungeonCompleted:: skip guildUUID check", spaceNo, guildUUID, sVal.guildUUID, win, delay)
        elif sVal.guildUUID != guildUUID:
            WARNING_MSG("_onGuildBossDungeonCompleted:: taemUUID not match", spaceNo, sVal.guildUUID, guildUUID)
            return
        sVal.spaceMgr.cell.destroyAllEntities()

        sVal = self.spaces[spaceNo]
        sVal.spaceMgr.cell.onGuildBossDungeonCompleted(spaceNo, sVal.guildUUID, win, delay, sVal.getElapsedTime())
        if delay:
            sVal.completeDungeonTimer = self._callback(
                delay, '_onGuildBossDungeonCompletedCallback',
                (spaceNo, sVal.spaceUUID, sVal.guildUUID, win, 'dungeon complete'), gametimer.TIMER_TAG_ON_GUILD_BOSS_CHALLENGE_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onGuildBossDungeonCompletedCallback(spaceNo, sVal.spaceUUID, sVal.guildUUID, win, 'dungeon complete')

    def _onGuildBossDungeonCompletedCallback(self, spaceNo, spaceUUID, guildUUID, win, reason):
        DEBUG_MSG('_onGuildBossDungeonCompletedCallback::', spaceNo, spaceUUID, guildUUID, win, reason)
        if spaceNo not in self.spaces:
            ERROR_MSG('_onGuildBossDungeonCompletedCallback::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.completeDungeonTimer = 0
        if sVal.spaceUUID != spaceUUID:
            ERROR_MSG('_onGuildBossDungeonCompletedCallback:: spaceUUID not match', sVal.spaceUUID, spaceUUID)
            return

        if not sVal.isActive():
            WARNING_MSG('_onGuildBossDungeonCompletedCallback:: already complete', spaceNo, sVal.state)
            return
        
        sVal.spaceMgr.cell.dungeonCompleted()
        extra = {}
        extra['guildUUID'] = guildUUID
        self._kickOutAllFounders(spaceNo, extra)
        
        sVal.clearCompleteTimer()
        sVal.completeDungeon(win)
        sVal.toDestoryDungeon()

    def _kickOutAllFounders(self, spaceNo, extra):
        spaceVal = self.spaces[spaceNo]
        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        for gbId, founderVal in spaceVal.founders.items():
            if founderVal.hasAvatar():
                INFO_MSG('_kickoutAllFounders:: kickout', founderVal.playerGBID, extra)
                founderVal.playerBox.cell.doLeaveGuildBossDungeon(extra)
                founderVal.playerBox.cell.clearGuildBossDungeonID(dungeonNo)

    def doEnterDungeon(self, box, gbId, guildUUID, spaceNo, extra):
        if spaceNo not in self.spaces:
            ERROR_MSG('spaceNo "{}" not found in spaces'.format(spaceNo))
            return

        spaceVal = self.spaces[spaceNo]

        if spaceVal.isCompleted():
            ERROR_MSG("space already completed", spaceNo, spaceVal.spaceUUID)
            return

        if spaceVal.markDestroy:
            ERROR_MSG('spaceNo "{}" already be destroy delay'.format(spaceNo))
            return

        spaceUUID = spaceVal.spaceUUID
        spaceBox = spaceVal.spaceBox
        spaceMgr = spaceVal.spaceMgr

        spaceMgr.cell.doEnterGuildBossDungeon(box, gbId, spaceUUID, spaceBox, extra)

    def enterDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, guildUUID, extra):
        """进入副本成功后回调"""
        DEBUG_MSG('enterDungeonSpaceSucc::', spaceNo, playerBox, playerGbId, guildUUID, extra)
        if not self._checkAfterEnterDungeon(spaceNo, playerBox, playerGbId, guildUUID, extra):
            extra = {}
            extra['guildUUID'] = guildUUID
            playerBox.cell.doLeaveGuildBossDungeon(extra)
        else:
            dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
            playerBox.cell.setGuildBossDungeonID(dungeonNo)

    def _checkAfterEnterDungeon(self, spaceNo, playerBox, playerGbId, guildUUID, extra):
        if spaceNo not in self.spaces:
            ERROR_MSG('spaceNo "{}" is missing'.format(spaceNo))
            return False

        dungeonVal = self.spaces[spaceNo]
        if not dungeonVal.isActive():
            ERROR_MSG('spaceNo "{}" not active'.format(spaceNo))
            return False

        founderVal = dungeonVal.founders.getFounderVal(playerGbId)
        if not founderVal:
            dungeonVal.founders.addFounder(spaceNo, dungeonVal.spaceUUID, playerGbId, playerBox)
            founderVal = dungeonVal.founders.getFounderVal(playerGbId)
        founderVal.onAvatarEnter(playerGbId)
        founderVal.playerBox = playerBox

        data = DungeonSettlement.DungeonExtraData()
        data.loadDatas(extra)
        dungeonVal.spaceMgr.cell.notifyDungeonExtarData(playerGbId, data)
        return True
    
    def applyCreateDungeon(self, box, gbId, guildUUID, extra):
        self.createDungeonSpaceRemote(box, gbId, guildUUID, extra)

    def _getDungeonSpaceVal(self, spaceNo, playerBox, playerGbId, guildUUID, extra):
        return dungeon.GuildBossDungeonSpaceVal(spaceNo=spaceNo,
                                           spaceUUID=0, spaceBox=None, spaceMgr=None,
                                           guildUUID=guildUUID, guildBox = playerBox)

    def _getDungeonSpaceWeight(self, enterNum=5) -> int:
        return utils.calcSpaceWeight(enterNum, False, gameconst.EntNumPerPlayerInAOI.teamDungeon)

    def _needSpaceMgr(self, spaceNo):
        return True

    def getDungeonSpaceNoRange(self):
        enterType = DDI.datas[self.dungeonNo].get('enterType', gameconst.DungeonEnterType.SINGLE)
        if enterType==gameconst.DungeonEnterType.BOTH:
            return gameconst.SpaceType.getTeamDungeonSpaceNoRange(self.dungeonNo)
        else:
            return gameconst.SpaceType.getCopiedSpaceNoRange(self.dungeonNo)

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, guildUUID, extra):
        DEBUG_MSG('_loadDungeonSpaceEntities::')
        # ready first
        self.onLoadDungeonSpaceReady(playerBox, playerGbId, spaceNo, guildUUID, extra)
        # use iCreateDungeonMonster function
        return super(GuildBossDungeonStub, self)._loadDungeonSpaceEntities(
            spaceNo, playerBox, playerGbId, guildUUID, extra)

    def onLoadDungeonSpaceReady(self, playerBox, playerGbId, spaceNo, guildUUID, extra):
        DEBUG_MSG('onLoadDungeonSpaceReady::', playerBox, playerGbId, spaceNo, guildUUID, extra)
        
        if spaceNo not in self.spaces:
            ERROR_MSG('onLoadDungeonSpaceReady:: failed, missing space data', playerBox, playerGbId, spaceNo, guildUUID, extra)
            return
        
        spaceVal = self.spaces[spaceNo]
        spaceVal.spaceMgr.cell.setGuildBox(playerBox)
        playerBox.onGuildChallengeDungeonCreated(guildUUID, self.dungeonNo, spaceNo, spaceVal.spaceUUID, spaceVal.spaceBox, spaceVal.spaceMgr, extra)

    def leaveGuildBossDungeon(self, spaceNo, guildUUID, src, playerBox, playerGBID):
        DEBUG_MSG("leaveGuildBossDungeon~ ", spaceNo, guildUUID, src, playerBox)
        if spaceNo not in self.spaces:
            ERROR_MSG('leaveGuildBossDungeon:: failed, missing space data', spaceNo, src, playerBox)
            return
        
        dungeonVal = self.spaces[spaceNo]
        founderVal = dungeonVal.founders.getFounderVal(playerGBID)
        if founderVal:
            extra = {}
            extra['guildUUID'] = guildUUID
            playerBox.cell.doLeaveGuildBossDungeon(extra)

    def getExtraData(self, spaceNo, gbId):
        dungeonVal = self.spaces[spaceNo]
        founderVal = dungeonVal.founders.getFounderVal(gbId)
        return founderVal.firstPass
    
    def syncGuildBossHP(self, spaceNo, curHP, fullHP):
        DEBUG_MSG('syncGuildBossHP:: ', spaceNo, curHP, fullHP)
        if spaceNo not in self.spaces:
            ERROR_MSG('syncGuildBossHP:: failed, missing space data', spaceNo)
            return
        spaceVal = self.spaces[spaceNo]
        spaceVal.guildBox.syncGuildBossHP(curHP, fullHP)