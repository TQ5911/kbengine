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
        self.pyAddTimer(30, 30, gametimer.TIMER_DUNGEON_CHECK_DESTROY)
        self.pyAddTimer(1, 0.1, gametimer.TIMER_DUNGEON_ENTITY_GENERATOR)
        return

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.TIMER_DUNGEON_CHECK_DESTROY:
            self._checkDungeonSpaceDestroy()
        elif userArg == gametimer.TIMER_DUNGEON_ENTITY_GENERATOR:
            self.onTimerCreateEntity()
        else:
            super(GuildBossDungeonStub, self).onTimer(tid, userArg)

    def _checkDungeonSpaceDestroy(self):
        now = utils.curTS()
        # LOG_DBG('_checkDungeonSpaceDestroy:: {}'.format(now))
        # teamStub.destroyTeamDungeonDelay args list
        needDestroyList = []
        realDestroyList = []
        for spaceNo, _sVal in self.spaces.items():
            if _sVal.nDestoryCnt>3:
                LOG_ERR('_checkDungeonSpaceDestroy: cannot destory space', spaceNo)
                continue

            if _sVal.markCreate:
                # new dungeon, skip destroy once
                _sVal.markCreate = False
                continue

            if _sVal.markDestroy:
                if _sVal.markDestroy < now:
                    realDestroyList.append((spaceNo, _sVal.spaceUUID, 'time destory'))
                continue

            # extra kwargs in `team.TeamDungeonSpaceCacheVal.isDungeonSpaceCanBeDestoried`
            extraInfo = {'tCreate': _sVal.tCreate,
                         'tState': _sVal.state}

            needDestroyList.append((_sVal.guildUUID,
                                    self.dungeonNo,
                                    spaceNo,
                                    'delay timeout destory',
                                    extraInfo))

        for rArgs in realDestroyList:
            self.destoryDungeonSpace(*rArgs)

    def onDungeonSpaceGone(self, spaceNo, reason):
        if reason == gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH:
            LOG_ERR("GuildBossDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                sVal = self.spaces[spaceNo]
                sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_GUILD_BOSS_CHALLENGE_DUNGEON_COMPLETED_CALLBACK)
                sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)

                self.cancelSpaceEntitiesLoadingProcess(spaceNo)

                sVal.spaceBox.doEntireDestroy(False, False)
                self.spaces.pop(spaceNo)

    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        LOG_INFO('destoryDungeonSpace', spaceNo, spaceUUID, reason)
        if spaceNo not in self.spaces:
            LOG_WARN('wl: destoryDungeonSpace cannot find space:', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        if spaceUUID and sVal.spaceUUID!=spaceUUID:
            LOG_WARN('destoryDungeonSpace:: spaceUUID not match {}!={}'.format(sVal.spaceUUID, spaceUUID))
            return

        now = utils.curTS()
        if not sVal.markDestroy:
            sVal.markDestroy = utils.curTS() + 60
            sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_GUILD_BOSS_CHALLENGE_DUNGEON_COMPLETED_CALLBACK)
            sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
            sVal.toDestoryDungeon()

            LOG_INFO('destoryDungeonSpace::space will be destroyed in next check,', spaceNo, sVal.markDestroy)
            return

        # real destroy dungeon
        elif sVal.markDestroy < now:

            # 【大量机器人新号登录后立刻下线后副本报错】
            self.cancelSpaceEntitiesLoadingProcess(spaceNo)

            sVal.spaceBox.doEntireDestroy(False, False)
            self.spaces.pop(spaceNo)

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGBID, guildUUID, extra):
        LOG_INFO("leaveDungeonSpaceSucc::", spaceNo, playerBox, playerGBID, guildUUID, extra)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveDungeonSpaceSucc::cannot get space', spaceNo)
            return
        dungeonVal = self.spaces[spaceNo]
        founderVal = dungeonVal.founders.getFounderVal(playerGBID)
        if founderVal:
            founderVal.onAvatarLeave(playerGBID, isOffline=False)

    def onAvatarOffline(self, spaceNo, playerGbId):
        LOG_INFO('onAvatarOffline::', spaceNo, playerGbId)
        if spaceNo not in self.spaces:
            LOG_ERR('onAvatarOffline::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        founderVal = sVal.founders.getFounderVal(playerGbId)
        if founderVal:
            founderVal.onAvatarLeave(playerGbId, isOffline=True)

    def onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp):
        return self._onReliveInDungeon(spaceNo, playerBox, playerGbId, reliveType, reliveHp)

    def onDungeonStarted(self, spaceNo, tCreate):
        LOG_INFO('onDungeonStarted::', spaceNo, tCreate)
        if spaceNo not in self.spaces:
            LOG_ERR('onDungeonStarted::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.tCreate = tCreate or utils.curTS()
        sVal.spaceMgr.cell.onDungeonStarted(sVal.tCreate)

    def completeGuildBossDungeon(self, spaceNo, guildUUID, win, delay, reasonType):
        LOG_INFO('in completeGuildBossDungeon:', spaceNo, guildUUID, win, delay, reasonType)
        self._onGuildBossDungeonCompleted(spaceNo, guildUUID, win, delay, reasonType)

    def _onGuildBossDungeonCompleted(self, spaceNo, guildUUID, win, delay, reasonType):
        LOG_INFO('in _onGuildBossDungeonCompleted:', spaceNo, guildUUID, win, delay, reasonType)
        if spaceNo not in self.spaces:
            if guildUUID:
                LOG_WARN('_onGuildBossDungeonCompleted:: cannot get space', spaceNo, guildUUID)
            else:
                LOG_ERR('_onGuildBossDungeonCompleted:: cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        if sVal.completeDungeonTimer:
            LOG_WARN('_onGuildBossDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return
        if sVal.markDestroy:
            LOG_WARN("_onGuildBossDungeonCompleted:: dungeon already mark destroy", spaceNo, guildUUID, win, delay)
            return
        if not sVal.isActive():
            LOG_WARN('_onGuildBossDungeonCompleted:: already complete', spaceNo, sVal.state)
            return
        if not guildUUID:
            LOG_WARN("_onGuildBossDungeonCompleted:: skip guildUUID check", spaceNo, guildUUID, sVal.guildUUID, win, delay)
        elif sVal.guildUUID != guildUUID:
            LOG_WARN("_onGuildBossDungeonCompleted:: taemUUID not match", spaceNo, sVal.guildUUID, guildUUID)
            return
        sVal.spaceMgr.cell.destroyAllEntities()

        sVal.completedReasonType = reasonType

        sVal.spaceMgr.cell.onGuildBossDungeonCompleted(spaceNo, sVal.guildUUID, win, delay, sVal.getElapsedTime(), sVal.completedReasonType)
        if delay:
            sVal.completeDungeonTimer = self.addTimerCB(
                delay, '_onGuildBossDungeonCompletedCallback',
                (spaceNo, sVal.spaceUUID, sVal.guildUUID, win, 'dungeon complete'), gametimer.TIMER_TAG_ON_GUILD_BOSS_CHALLENGE_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onGuildBossDungeonCompletedCallback(spaceNo, sVal.spaceUUID, sVal.guildUUID, win, 'dungeon complete')

    def _onGuildBossDungeonCompletedCallback(self, spaceNo, spaceUUID, guildUUID, win, reason):
        LOG_INFO('_onGuildBossDungeonCompletedCallback::', spaceNo, spaceUUID, guildUUID, win, reason)
        if spaceNo not in self.spaces:
            LOG_ERR('_onGuildBossDungeonCompletedCallback::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.completeDungeonTimer = 0
        if sVal.spaceUUID != spaceUUID:
            LOG_ERR('_onGuildBossDungeonCompletedCallback:: spaceUUID not match', sVal.spaceUUID, spaceUUID)
            return

        if not sVal.isActive():
            LOG_WARN('_onGuildBossDungeonCompletedCallback:: already complete', spaceNo, sVal.state)
            return
        
        sVal.spaceMgr.cell.dungeonCompleted()
        extra = {}
        extra['guildUUID'] = guildUUID
        self._kickOutAllFounders(spaceNo, extra)
        
        sVal.clearCompleteTimer()
        sVal.completeDungeon(win)
        sVal.toDestoryDungeon()

    def _kickOutAllFounders(self, spaceNo, extra):
        LOG_INFO('RaidDungeonStub _kickOutAllFounders:: kickout', spaceNo, extra)
        spaceVal = self.spaces[spaceNo]
        _needDestoryGBIDs = []
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        for gbId, founderVal in spaceVal.founders.items():
            base = founderVal.playerBox
            if founderVal.hasAvatar() and base and not utils.checkBoxOffline(base) and base.cell:
                LOG_INFO('GuildBossDungeonStub _kickoutAllFounders:: kickout', founderVal.playerGBID)
                founderVal.playerBox.cell.doLeaveGuildBossDungeon(extra)
                founderVal.playerBox.cell.clearGuildBossDungeonID(dungeonNo)
            else:
                LOG_INFO('GuildBossDungeonStub _kickoutAllFounders:: destroy', founderVal.playerGBID)
                _needDestoryGBIDs.append(gbId)
        for i in _needDestoryGBIDs:
            spaceVal.founders.destoryFounder(i)

    def doEnterDungeon(self, box, gbId, guildUUID, spaceNo, extra):
        if spaceNo not in self.spaces:
            LOG_ERR('spaceNo "{}" not found in spaces'.format(spaceNo))
            return

        spaceVal = self.spaces[spaceNo]

        if spaceVal.isCompleted():
            LOG_ERR("space already completed", spaceNo, spaceVal.spaceUUID)
            return

        if spaceVal.markDestroy:
            LOG_ERR('spaceNo "{}" already be destroy delay'.format(spaceNo))
            return

        spaceUUID = spaceVal.spaceUUID
        spaceBox = spaceVal.spaceBox
        spaceMgr = spaceVal.spaceMgr

        spaceMgr.cell.doEnterGuildBossDungeon(box, gbId, spaceUUID, spaceBox, extra)

    def enterDungeonSpaceSuccess(self, spaceNo, playerBox, playerGbId, guildUUID, extra):
        """进入副本成功后回调"""
        LOG_INFO('enterDungeonSpaceSuccess::', spaceNo, playerBox, playerGbId, guildUUID, extra)
        if not self._checkAfterEnterDungeon(spaceNo, playerBox, playerGbId, guildUUID, extra):
            extra = {}
            extra['guildUUID'] = guildUUID
            playerBox.cell.doLeaveGuildBossDungeon(extra)
        else:
            dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
            playerBox.cell.setGuildBossDungeonID(dungeonNo)

    def _checkAfterEnterDungeon(self, spaceNo, playerBox, playerGbId, guildUUID, extra):
        if spaceNo not in self.spaces:
            LOG_ERR('spaceNo "{}" is missing'.format(spaceNo))
            return False

        dungeonVal = self.spaces[spaceNo]
        if not dungeonVal.isActive():
            LOG_ERR('spaceNo "{}" not active'.format(spaceNo))
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

    def getDungeonSpaceRange(self):
        enterType = DDI.datas[self.dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.SINGLE)
        if enterType==gameconst.DungeonEnterTypeEnum.BOTH:
            return gameconst.SpaceType.getTeamDungeonSpaceRange(self.dungeonNo)
        else:
            return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, guildUUID, extra):
        LOG_INFO('_loadDungeonSpaceEntities::')
        # ready first
        self.onLoadDungeonSpaceReady(playerBox, playerGbId, spaceNo, guildUUID, extra)
        # use iCreateDungeonMonster function
        return super(GuildBossDungeonStub, self)._loadDungeonSpaceEntities(
            spaceNo, playerBox, playerGbId, guildUUID, extra)

    def onLoadDungeonSpaceReady(self, playerBox, playerGbId, spaceNo, guildUUID, extra):
        LOG_INFO('onLoadDungeonSpaceReady::', playerBox, playerGbId, spaceNo, guildUUID, extra)
        
        if spaceNo not in self.spaces:
            LOG_ERR('onLoadDungeonSpaceReady:: failed, missing space data', playerBox, playerGbId, spaceNo, guildUUID, extra)
            return
        opUUID = extra.get('opUUID')
        spaceVal = self.spaces[spaceNo]
        spaceVal.spaceMgr.cell.setGuildBox(playerBox, opUUID)
        playerBox.onGuildChallengeDungeonCreated(guildUUID, self.dungeonNo, spaceNo, spaceVal.spaceUUID, spaceVal.spaceBox, spaceVal.spaceMgr, extra)

    def leaveGuildBossDungeon(self, spaceNo, guildUUID, src, playerBox, playerGBID):
        LOG_INFO("leaveGuildBossDungeon~ ", spaceNo, guildUUID, src, playerBox)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveGuildBossDungeon:: failed, missing space data', spaceNo, src, playerBox)
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
        LOG_DBG('syncGuildBossHP:: ', spaceNo, curHP, fullHP)
        if spaceNo not in self.spaces:
            LOG_ERR('syncGuildBossHP:: failed, missing space data', spaceNo)
            return
        spaceVal = self.spaces[spaceNo]
        spaceVal.guildBox.syncGuildBossHP(curHP, fullHP)
