# coding: utf-8
import KBEngine
from KBEDebug import *

import gameengine
import gameconst
import gametimer

import iDungeonStub
import iDungeonStubMonster

import userType
import dungeon
import dungeonSrc

import DungeonSettlement

import utils


class _Record(userType.UserSingleType):
    def __init__(self, raidUUID, playerGBID):
        self.raidUUID = raidUUID
        self.timerId = 0
        self.playerGBID = playerGBID


class RaidDungeonCreatingMixin(object):

    def __init__(self):
        self.creatingRaidDict = {}

    def checkRaidDungeonCreating(self, raidUUID):
        return raidUUID in self.creatingRaidDict

    def addRaidDungeonCreatingRecord(self, raidUUID, playerGBID, timeout=3):
        if raidUUID in self.creatingRaidDict:
            LOG_WARN('addRaidDungeonCreatingRecord:: overwrite creating record',
                        raidUUID, self.creatingRaidDict[playerGBID], playerGBID)
        self.creatingRaidDict[raidUUID] = _Record(raidUUID, playerGBID)
        if timeout:
            self.asyncCallbackAfter(3)._releaseRaidDungeonCreatingLockTimeout(raidUUID)

    def _releaseRaidDungeonCreatingLockTimeout(self, raidUUID):
        LOG_WARN('_rmRaidDungeonCreatingRecordTimeout:: timeout rm timerId', raidUUID)
        self.releaseRaidDungeonCreatingLock(raidUUID)

    def popRaidDungeonCreatingRecord(self, raidUUID, default=None):
        return self.creatingRaidDict.pop(raidUUID, default)

    def getRaidDungeonCreatingLock(self, raidUUID, playerGBID, timeout=3):
        """获得raidCreating锁"""
        LOG_INFO('lockRaidCreating::', raidUUID, playerGBID, timeout)
        if self.checkRaidDungeonCreating(raidUUID):
            return 0
        self.addRaidDungeonCreatingRecord(raidUUID, playerGBID)
        return raidUUID

    def releaseRaidDungeonCreatingLock(self, raidUUID):
        """释放raidCreating锁"""
        LOG_INFO('unlockRaidCreating::', raidUUID)
        self.popRaidDungeonCreatingRecord(raidUUID, None)


class RaidDungeonStub(iDungeonStub.IDungeonStub, iDungeonStubMonster.IDungeonStubMonster,
                      RaidDungeonCreatingMixin,):
    """"Raid Dungeon Stub Class"""

    def __init__(self):
        super(RaidDungeonStub, self).__init__()
        if not hasattr(self, 'creatingRaidDict'):
            self.creatingRaidDict = {}   # type: dict[int, _Record]
        if not hasattr(self, 'spaces'):
            self.spaces = {}    # type: dict[int, dungeon.RaidDungeonSpaceVal]
        if not hasattr(self, 'dungeonNo'):
            self.dungeonNo = 0

    @property
    def delayDestroyTimeout(self):
        return 60

    def doNext(self):
        super(RaidDungeonStub, self).doNext()
        # add check destroy cycle tick
        self.pyAddTimer(30, 30, gametimer.TIMER_DUNGEON_CHECK_DESTROY)
        self.pyAddTimer(1, 0.1, gametimer.TIMER_DUNGEON_ENTITY_GENERATOR)

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.TIMER_DUNGEON_CHECK_DESTROY:
            self._checkDungeonSpaceDestroy()
        elif userArg == gametimer.TIMER_DUNGEON_ENTITY_GENERATOR:
            self.onTimerCreateEntity()
        else:
            super(RaidDungeonStub, self).onTimer(tid, userArg)

    def _checkDungeonSpaceDestroy(self):
        # LOG_DBG('_checkDungeonSpaceDestroy::~~~~~~~~~~~~~~~~~')
        now = utils.curTS()
        _needDestroyList = []
        realDestroyList = []
        for spaceNo, _sVal in self.spaces.items():
            # CASE_1: 超过最大清理次數, 報錯
            if _sVal.nDestoryCnt > 3:
                LOG_WARN('_checkDungeonSpaceDestroy:: cannot destroy space currently', spaceNo)
                # reset nDestoryCnt
                _sVal.nDestoryCnt = 0
                continue

            # CASE_2: 副本已经被标记删除
            if _sVal.isToDestory():
                # CASE_2.1: 副本需要被真正删除
                if _sVal.tMarkDestroy < now:
                    realDestroyList.append((spaceNo, _sVal.spaceUUID, 'time destroy'))
                continue

            _needDestroyList.append((spaceNo, _sVal.spaceUUID, 'time delay destroy'))

        self.asyncCallbackAfter(0.1)._checkTryMarkDestroyDungeonSpaces(_needDestroyList)
        self.asyncCallbackAfter(0.2)._checkRealDestroyDungeonSpaces(realDestroyList)

    def _checkRealDestroyDungeonSpaces(self, realDestroyList):
        for _rArgs in realDestroyList:
            self.destoryDungeonSpace(*_rArgs)

    def _checkTryMarkDestroyDungeonSpaces(self, needDestroyList):
        for _nArgs in needDestroyList:
            self.tryDestroyRaidDungeonDelay(*_nArgs)

    def onDungeonSpaceGone(self, spaceNo, reason):
        if reason == gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH:
            LOG_ERR("RaidDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                _spaceVal = self.spaces[spaceNo]
                _spaceVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)
                _spaceVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_spaceVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
                _raidStub = gameengine.getRaidStub(_spaceVal.raidUUID)
                _raidStub.clearRaidDungeonInfo(_spaceVal.raidUUID, self.dungeonNo, spaceNo, _spaceVal.spaceUUID)

                self.cancelSpaceEntitiesLoadingProcess(spaceNo)

                _spaceVal.spaceBox.doEntireDestroy(False, False)
                self.spaces.pop(spaceNo)


    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        LOG_INFO('destoryDungeonSpace::', spaceNo, spaceUUID, reason)
        _spaceVal, err = self._destroyRaidDungeonSpace(spaceNo, spaceUUID)
        if err == gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            # 强制清除raid中副本cache(如果有的话)
            gameengine.getRaidStub(_spaceVal.raidUUID).clearRaidDungeonInfo(
                _spaceVal.raidUUID, self.dungeonNo, spaceNo, spaceUUID)

        elif err == gameconst.RaidDunErrno.ENUM_RAIDDUN_FOUNDER_IN_DUNGEON:
            self._kickOutAllFounders(spaceNo)

        else:
            LOG_ERR(f'destoryDungeonSpace[raid]:: failed, {err}')

    def _destroyRaidDungeonSpace(self, spaceNo, spaceUUID):
        if spaceNo not in self.spaces:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND

        spaceVal = self.spaces[spaceNo]
        if spaceVal.spaceUUID != spaceUUID:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_SPACE_UUID_NOT_MATCH

        if not spaceVal.founders.isNoFounders():
            LOG_WARN('_destroyRaidDungeonSpace:: founders in space', self.dungeonNo, spaceNo)
            spaceVal.nDestoryCnt += 1
            return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_FOUNDER_IN_DUNGEON

        # 【大量机器人新号登录后立刻下线后副本报错】
        self.cancelSpaceEntitiesLoadingProcess(spaceNo)

        spaceVal.spaceBox.doEntireDestroy(False, False)
        del self.spaces[spaceNo]
        return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    def tryDestroyRaidDungeonDelay(self, spaceNo, spaceUUID, reason):
        LOG_DBG('tryDestroyRaidDungeonDelay::', spaceNo, spaceUUID, reason)
        _spaceVal, err = self._tryDestroyRaidDungeonDelay(spaceNo, spaceUUID)
        if err not in (gameconst.RaidDunErrno.ENUM_RAIDDUN_OK, gameconst.RaidDunErrno.ENUM_RAIDDUN_SKIP):
            gameengine.panicStack('tryDestroyRaidDungeonDelay:: failed, {}'.format(err), spaceNo, spaceUUID)
            return

        if err == gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            # 强制踢出所有玩家
            self._kickOutAllFounders(spaceNo)

            # 【副本服务端报错】
            # 销毁时停止所有该space的completeCallback
            # 【【上灵试炼】组队进入单人副本，打完boss后再次进入副本，会出现报错】
            # 提前cancel的时机到markDestroy
            _spaceVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_RAID_DUNGEON_COMPLETED_CALLBACK)
            _spaceVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_spaceVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
            gameengine.getRaidStub(_spaceVal.raidUUID).clearRaidDungeonInfo(
                _spaceVal.raidUUID, self.dungeonNo, spaceNo, spaceUUID)

    def _kickOutAllFounders(self, spaceNo):
        LOG_INFO('RaidDungeonStub _kickOutAllFounders:: kickout', spaceNo)
        spaceVal = self.spaces[spaceNo]     # type: dungeon.RaidDungeonSpaceVal
        _needDestoryGBIDs = []
        src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.TIMEOUT)
        for gbId, founderVal in spaceVal.founders.items():
            base = founderVal.playerBox
            if founderVal.hasAvatar() and base and not utils.checkBoxOffline(base) and base.cell:
                LOG_INFO('RaidDungeonStub _kickoutAllFounders:: kickout', founderVal.playerGBID)
                founderVal.playerBox.cell.selfLeaveRaidDungeon(src)
            else:
                LOG_INFO('RaidDungeonStub _kickoutAllFounders:: destroy', founderVal.playerGBID)
                _needDestoryGBIDs.append(gbId)
        for i in _needDestoryGBIDs:
            spaceVal.founders.destoryFounder(i)

    def _tryDestroyRaidDungeonDelay(self, spaceNo, spaceUUID):
        if spaceNo not in self.spaces:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND

        spaceVal = self.spaces[spaceNo]
        if spaceVal.spaceUUID != spaceUUID:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_SPACE_UUID_NOT_MATCH

        if spaceVal.isToDestory():
            LOG_WARN('_tryDestroyRaidDungeonDelay:: already mark destroyed', spaceNo, spaceUUID)
            return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_SKIP

        if spaceVal.isCompleted():
            spaceVal.tMarkDestroy = utils.curTS() + self.delayDestroyTimeout
            spaceVal.toDestoryDungeon()
            return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

        return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_SKIP

    def onAvatarOffline(self, spaceNo, playerGbId):
        """玩家下线时回调"""
        LOG_INFO('onAvatarOffline::', spaceNo, playerGbId)

        def _check():
            if spaceNo not in self.spaces:
                return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

        _, err = _check()
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('onAvatarOffline:: check failed, {}'.format(err))
            return

        sVal = self.spaces[spaceNo]
        founderVal = sVal.founders.getFounderVal(playerGbId)    # type: dungeon.RaidDungeonFounderVal
        if founderVal:
            founderVal.onAvatarLeave(playerGbId, isOffline=True)

    def onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp):
        """玩家复活时回调"""
        self._onReliveInDungeon(spaceNo, playerBox, playerGbId, reliveType, reliveHp)

    def onDungeonStarted(self, spaceNo, tCreate):
        """副本开始时回调"""
        LOG_INFO('onDungeonStarted::', spaceNo, tCreate)

        def _check():
            if spaceNo not in self.spaces:
                return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

        _, err = _check()
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('onDungeonStarted:: check failed, {}'.format(err))
            return

        sVal = self.spaces[spaceNo]
        sVal.tCreate = tCreate or utils.curTS()
        sVal.spaceMgr.cell.onDungeonStarted(sVal.tCreate)

    def completeRaidDungeon(self, spaceNo, raidUUID, win, delay, reasonType):
        return self._onRaidDungeonCompleted(spaceNo, raidUUID, win, delay, reasonType)

    def _onRaidDungeonCompleted(self, spaceNo, raidUUID, win, delay, reasonType):
        LOG_INFO('_onRaidDungeonCompleted:', spaceNo, raidUUID, win, delay, reasonType)
        def _check():
            if spaceNo not in self.spaces:
                return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

        _, err = _check()
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            if raidUUID:
                LOG_WARN('_onRaidDungeonCompleted:: check failed, {} {}'.format(err, raidUUID))
            else:
                LOG_ERR('_onRaidDungeonCompleted:: check failed, {}'.format(err))
            return

        _sVal = self.spaces[spaceNo]
        if _sVal.completeDungeonTimer:
            LOG_WARN('_onRaidDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return
        if not _sVal.isActive():
            LOG_WARN('_onRaidDungeonCompleted:: already complete', spaceNo, _sVal.state)
            return
        if not raidUUID:
            LOG_WARN('_onRaidDungeonCompleted:: skip raidUUID check', spaceNo, raidUUID, _sVal.raidUUID, win, delay)
        elif _sVal.raidUUID != raidUUID:
            LOG_WARN("_onRaidDungeonCompleted:: raidUUID not match", spaceNo, _sVal.raidUUID, raidUUID)
            return
        
        gameengine.getRaidStub(raidUUID).setInDungeon(raidUUID, False)
        
        _sVal.spaceMgr.cell.destroyAllEntities()
        _sVal.completedReasonType = reasonType
        _sVal.spaceMgr.cell.onRaidDungeonCompleted(
            spaceNo, 
            raidUUID, 
            win, 
            delay, 
            _sVal.dungeonCreepBaseKillDic, 
            _sVal.getAllPlayerGbidAndNamePair(), 
            _sVal.getElapsedTime(), 
            0, 
            _sVal.completedReasonType)

        
        # 副本完成后倒计时
        if delay > 0:
            lastDungeonFinishedTime = utils.curTS() + delay
            _raidStub = gameengine.getRaidStub(_sVal.raidUUID)
            _raidStub.refreshLastDungeonFinishedTime(_sVal.raidUUID, lastDungeonFinishedTime)
            _sVal.completeDungeonTimer = self.addTimerCB(
                delay, '_onRaidDungeonCompletedCallback',
                (spaceNo, _sVal.spaceUUID, 'dungeon complete', win), gametimer.TIMER_TAG_ON_RAID_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onRaidDungeonCompletedCallback(spaceNo, _sVal.spaceUUID, 'dungeon complete', win)

    def _onRaidDungeonCompletedCallback(self, spaceNo, spaceUUID, reason, win):
        LOG_INFO('_onRaidDungeonCompletedCallback::', spaceNo, spaceUUID, reason, win)
        if spaceNo not in self.spaces:
            LOG_ERR('_onRaidDungeonCompletedCallback::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.completeDungeonTimer = 0
        if sVal.spaceUUID != spaceUUID:
            LOG_ERR('_onRaidDungeonCompletedCallback:: spaceUUID not match', sVal.spaceUUID, spaceUUID)
            return

        if not sVal.isActive():
            LOG_WARN('_onRaidDungeonCompletedCallback:: already complete', spaceNo, sVal.state)
            return

        sVal.clearCompleteTimer()
        sVal.completeDungeon(win)
        sVal.toDestoryDungeon()
        self._kickOutAllFounders(spaceNo)
        gameengine.getRaidStub(sVal.raidUUID).onRaidDungeonCompletedCB(sVal.raidUUID, self.dungeonNo, spaceNo, sVal.spaceUUID)

    def applyCreateDungeon(self, box, gbId, raidUUID, extra):
        """真正创建副本时调用"""
        # TRY GETTING LOCK ------------------------------------------------
        if not self.getRaidDungeonCreatingLock(raidUUID, gbId):
            LOG_ERR('applyCreateDungeon:: creating...', raidUUID)
            return
        # -----------------------------------------------------------------
        self.createDungeonSpaceRemote(box, gbId, raidUUID, extra)

    def doEnterDungeon(self, box, gbId, raidUUID, spaceNo, extra):
        """玩家执行进入副本时调用"""
        raise DeprecationWarning('In raid dungeon, doEnterDungeon logic move to raidStub')

    def getDungeonSpaceRange(self):
        return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)

    def _getDungeonSpaceVal(self, spaceNo, _, playerGbId, raidUUID, extra):
        spaceVal = dungeon.RaidDungeonSpaceVal(
            spaceNo=spaceNo, 
            spaceUUID=0,
            spaceMgr=None,
            spaceBox=None, 
            raidUUID=raidUUID, 
            spaceLevel=extra.get('spaceLevel', 1))
        return spaceVal

    def _getDungeonSpaceWeight(self, enterNum=40) -> int:
        return utils.calcSpaceWeight(enterNum, False, gameconst.EntNumPerPlayerInAOI.teamDungeon)

    def onLoadDungeonSpaceReady(self, playerBox, playerGBID, spaceNo, raidUUID, extra):
        """团队副本准备完毕后回调"""
        LOG_INFO('onLoadDungeonSpaceReady::')
        _spaceVal = self.spaces[spaceNo]
        spaceUUID = _spaceVal.spaceUUID
        spaceBox = _spaceVal.spaceBox
        _spaceMgrBox = _spaceVal.spaceMgr
        gameengine.getRaidStub(raidUUID).onLoadRaidDungeonSpaceReady(
            playerBox, playerGBID, raidUUID, self.dungeonNo,
            spaceNo, spaceUUID, spaceBox, _spaceMgrBox, extra)

    def enterDungeonSpaceSuccess(self, spaceNo, playerBox, playerGbId, raidUUID, extra):
        """团队成员进入副本成功后回调"""
        LOG_INFO('enterDungeonSpaceSuccess::', spaceNo, playerBox, playerGbId, raidUUID, extra)
        _src = extra.pop('src')  # 这里一定要有dungeonSrc
        founderVal, err = self._enterDungeonSpaceSucc(spaceNo, playerBox, playerGbId, raidUUID, _src)
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('enterDungeonSpaceSuccess:: failed, {}'.format(err))
            # NOTE: 进入团队副本后出现问题, 执行离开逻辑
            playerBox.cell.leaveRaidDungeon()
        else:
            founderVal.playerName = extra.pop('playerName', '')

            dungeonVal = self.spaces[spaceNo]

            # 把数据带过去
            data = DungeonSettlement.DungeonExtraData()
            data.loadDatas(extra)
            dungeonVal.spaceMgr.cell.notifyDungeonExtarData(playerGbId, data)

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGBID, raidUUID, extraData):
        self.onLoadDungeonSpaceReady(playerBox, playerGBID, spaceNo, raidUUID, extraData)

    def _enterDungeonSpaceSucc(self, spaceNo, playerBox, playerGBID, _, src):
        if spaceNo not in self.spaces:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND

        dungeonVal = self.spaces[spaceNo]
        if not dungeonVal.isActive():
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_IS_NOT_ACTIVE

        _founderVal = dungeonVal.founders.getFounderVal(playerGBID)  # type: dungeon.RaidDungeonFounderVal
        if not _founderVal:
            dungeonVal.founders.addFounder(spaceNo, dungeonVal.spaceUUID, playerGBID, playerBox)
            _founderVal = dungeonVal.founders.getFounderVal(playerGBID)
        _founderVal.onAvatarEnter(playerGBID)
        _founderVal.playerBox = playerBox

        return _founderVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, raidUUID, extra):
        """团队成员离开副本成功后回调"""
        LOG_INFO('leaveDungeonSpaceSucc::', spaceNo, playerBox, playerGbId, raidUUID, extra)
        dungeonVal, founderVla, err = self._leaveDungeonSpaceSucc(spaceNo, playerBox, playerGbId, raidUUID)
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('leaveDungeonSpaceSucc:: failed, {}'.format(err))
        src = extra.get('src', None)
        # 来自客户端的主动退出
        if src and src.srcId==gameconst.DunSrcEnum.FROM_CLIENT:
            # 副本还在进行中退出的，直接退出队伍
            if dungeonVal.completedReasonType == gameconst.DunegonCompleteReasonType.DEFAULT:
                # 退出团队
                extraProps = {'leaveDungen':True}
                gameengine.getRaidStub(raidUUID).leaveRaid(playerBox, playerGbId, raidUUID, extraProps)

    def _leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGBID, raidUUID):
        if spaceNo not in self.spaces:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND
        dungeonVal = self.spaces[spaceNo]
        founderVal = dungeonVal.founders.getFounderVal(playerGBID)  # type: dungeon.RaidDungeonFounderVal
        if not founderVal:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_FOUNDER_VAL_NOT_FOUND
        founderVal.onAvatarLeave(playerGBID, isOffline=False)
        return dungeonVal, founderVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    def leaveRaidDungeon(self, spaceNo, raidUUID, src, playerBox):
        LOG_INFO("leaveRaidDungeon~ ", spaceNo, raidUUID, src, playerBox)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveRaidDungeon:: failed, missing space data', spaceNo, src, playerBox)
            return
        dungeonVal = self.spaces[spaceNo]
        founders = len(dungeonVal.founders)
        if founders <= 1:
            self.completeRaidDungeon(spaceNo, raidUUID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)
        else:
            playerBox.cell.selfLeaveRaidDungeon(src)
