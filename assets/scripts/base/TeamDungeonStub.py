# coding: utf-8
import KBEngine
from KBEDebug import *

import gameengine
import gameconst
import gametimer

import iDungeonStub
import iDungeonStubMonster

import dungeon
import team

import DungeonSettlement

import formula
import utils
import dungeonSrc

import gamePlay_gamePlay as DDI


class TeamDungeonStub(iDungeonStubMonster.IDungeonStubMonster, iDungeonStub.IDungeonStub):
    """Implement of TeamDungeonStub"""

    def doNext(self):
        super(TeamDungeonStub, self).doNext()
        self.pyAddTimer(30, 30, gametimer.TIMER_DUNGEON_CHECK_DESTROY)
        return

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.TIMER_DUNGEON_CHECK_DESTROY:
            self._checkDungeonSpaceDestroy()
        else:
            super(TeamDungeonStub, self).onTimer(tid, userArg)

    def _checkDungeonSpaceDestroy(self):
        now = utils.curTS()
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

            # 跨服讨伐空间无本服 TeamStub 队伍缓存可咨询，仅按完成/标记流程销毁
            if _sVal.isCrossDungeon():
                continue

            # extra kwargs in `team.TeamDungeonSpaceCacheVal.isDungeonSpaceCanBeDestoried`
            extraInfo = {'tCreate': _sVal.tCreate,
                         'tState': _sVal.state}

            needDestroyList.append((_sVal.teamUUID,
                                    self.dungeonNo,
                                    spaceNo,
                                    'delay timeout destory',
                                    extraInfo))

        for _nArgs in needDestroyList:
            _teamStub = gameengine.getTeamStub(_nArgs[0])
            _teamStub.destroyTeamDungeonDelay(*_nArgs)

        for _rArgs in realDestroyList:
            self.destoryDungeonSpace(*_rArgs)

    def onDungeonSpaceGone(self, spaceNo, reason):
        if reason == gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH:
            LOG_ERR("TeamDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                _sVal = self.spaces[spaceNo]
                _sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
                _sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
                if not _sVal.isCrossDungeon():
                    # 跨服讨伐空间无本服 TeamStub 联动，仅本地清理
                    _teamStub = gameengine.getTeamStub(_sVal.teamUUID)
                    _teamStub.onDestroyTeamDungeon(_sVal.teamUUID, self.dungeonNo, spaceNo, _sVal.spaceUUID)

                self.cancelSpaceEntitiesLoadingProcess(spaceNo)

                _sVal.spaceBox.doEntireDestroy(False, False)
                self.spaces.pop(spaceNo)

    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        LOG_INFO('destoryDungeonSpace', spaceNo, reason)
        if spaceNo not in self.spaces:
            LOG_WARN('wl: destoryDungeonSpace cannot find space:', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        if spaceUUID and _sVal.spaceUUID!=spaceUUID:
            LOG_WARN('destoryDungeonSpace:: spaceUUID not match {}!={}'.format(_sVal.spaceUUID, spaceUUID))
            return

        now = utils.curTS()
        if not _sVal.markDestroy:
            # delay destroy space
            _sVal.markDestroy = utils.curTS() + 60
            # 【副本服务端报错】
            # 销毁时停止所有该space的completeCallback
            # 【【上灵试炼】组队进入单人副本，打完boss后再次进入副本，会出现报错】
            # 提前cancel的时机到markDestroy
            _sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
            _sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
            _sVal.toDestoryDungeon()

            LOG_INFO('destoryDungeonSpace::space will be destroyed in next check,', spaceNo, _sVal.markDestroy)
            if not _sVal.isCrossDungeon():
                # 跨服讨伐空间无本服 TeamStub 联动，仅本地清理
                _teamStub = gameengine.getTeamStub(_sVal.teamUUID)
                _teamStub.onDestroyTeamDungeon(_sVal.teamUUID, self.dungeonNo, spaceNo, spaceUUID)
            return

        # real destroy dungeon
        elif _sVal.markDestroy < now:

            # 【大量机器人新号登录后立刻下线后副本报错】
            self.cancelSpaceEntitiesLoadingProcess(spaceNo)

            if _sVal.isCrossDungeon():
                # 跨服讨伐：销毁前先把仍在副本内的成员逐个送回本服
                # （否则镜像 cell 随空间销毁走 SPACE_GONE 离线，本服会进
                # offlineFromCrossServer 的下线销毁流程，回程中的客户端登录失败）
                for _gbId, _founderVal in _sVal.founders.items():
                    if _founderVal.isEnter and _founderVal.playerBox:
                        _founderVal.playerBox.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())

            _sVal.spaceBox.doEntireDestroy(False, False)
            self.spaces.pop(spaceNo)

    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        LOG_INFO("leaveDungeonSpaceSucc::", spaceNo, playerBox, playerGbId, teamUUID, extra)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveDungeonSpaceSucc::cannot get space', spaceNo)
            return
        sVal = self.spaces[spaceNo]

        if sVal.isCrossDungeon():
            self._leaveCrossDungeonSpaceSucc(spaceNo, playerBox, playerGbId, teamUUID, extra)
            return

        leaveTeam = False
        src = extra.get('src', None)
        # 来自客户端的主动退出
        if src and src.srcId==gameconst.DunSrcEnum.FROM_CLIENT:
            # 副本还在进行中退出的，直接退出队伍
            if sVal.completedReasonType == gameconst.DunegonCompleteReasonType.DEFAULT:
                leaveTeam = True

        _teamStub = gameengine.getTeamStub(sVal.teamUUID)
        _teamStub.leaveTeamDungeon(playerBox, playerGbId, sVal.teamUUID, self.dungeonNo, leaveTeam)

    def _leaveCrossDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        # 跨服讨伐离开副本（对照本服 TeamStub.leaveTeamDungeon 语义）：
        # founders 离岗 + 进行中主动退出=退队（通知中心）+ 最后一人离开自动完成 + 返回本服
        _sVal = self.spaces[spaceNo]
        _founderVal = _sVal.founders.getFounderVal(playerGbId)
        if _founderVal:
            _founderVal.tLeave = utils.curTS()
            _founderVal.isEnter = False
            _founderVal.playerBox = None

        src = (extra or {}).get('src', None)
        if src and src.srcId == gameconst.DunSrcEnum.FROM_CLIENT:
            if _sVal.completedReasonType == gameconst.DunegonCompleteReasonType.DEFAULT:
                # 进行中主动退出 = 退出跨服小队（通知中心）
                gameengine.getCrossTeamStub(teamUUID).leaveTeam(playerBox, teamUUID, playerGbId)

        # 最后一人离开自动完成副本
        if _sVal.isActive() and not any([_f.isEnter for _f in _sVal.founders.values()]):
            self.completeTeamDungeon(spaceNo, teamUUID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)

        # 退出副本后返回本服（队伍不解散）；
        # 用 ENUM_NONE：onCrossServerEnd 对 ENUM_BASE 会直接 getattr(self, '') 分发，
        # 空方法名会抛 AttributeError（归墟回程即用 ENUM_NONE 无回调形态）
        playerBox.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())

    def onAvatarOffline(self, spaceNo, playerGbId):
        LOG_INFO('onAvatarOffline::', spaceNo, playerGbId)
        if spaceNo not in self.spaces:
            LOG_ERR('onAvatarOffline::cannot get space', spaceNo)
            return
        _sVal = self.spaces[spaceNo]
        if _sVal.isCrossDungeon():
            # 跨服讨伐副本内掉线 = 离线退队（通知中心移除成员）；重连回本服不回副本
            gameengine.getCrossTeamStub(_sVal.teamUUID).memberOffline(_sVal.teamUUID, playerGbId)
            return
        _teamStub = gameengine.getTeamStub(_sVal.teamUUID)
        _teamStub.onAvatarOffline(playerGbId, _sVal.teamUUID, self.dungeonNo)

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

    def completeTeamDungeon(self, spaceNo, teamUUID, win, delay, reasonType):
        return self._onTeamDungeonCompleted(spaceNo, teamUUID, win, delay, reasonType)

    def _onTeamDungeonCompleted(self, spaceNo, teamUUID, win, delay, reasonType):
        LOG_INFO('in completeTeamDungeon:', spaceNo, teamUUID, win, delay, reasonType)
        
        if spaceNo not in self.spaces:
            if teamUUID:
                LOG_WARN('completeTeamDungeon:: cannot get space', spaceNo, teamUUID)
            else:
                LOG_ERR('completeTeamDungeon:: cannot get space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        if _sVal.completeDungeonTimer:
            LOG_WARN('_onTeamDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return
        
        if _sVal.markDestroy:
            LOG_WARN("_onTeamDungeonCompleted:: dungeon already mark destroy", spaceNo, teamUUID, win, delay)
            return

        if not _sVal.isActive():
            LOG_WARN('_onTeamDungeonCompleted:: already complete', spaceNo, _sVal.state)
            return

        if not teamUUID:
            LOG_WARN("_onTeamDungeonCompleted:: skip teamUUID check", spaceNo, teamUUID, _sVal.teamUUID, win, delay)

        elif _sVal.teamUUID != teamUUID:
            LOG_WARN("_onTeamDungeonCompleted:: taemUUID not match", spaceNo, _sVal.teamUUID, teamUUID)
            return

        _isCross = _sVal.isCrossDungeon()
        if not _isCross:
            gameengine.getTeamStub(teamUUID).setInDungeon(teamUUID, False)

        _sVal.spaceMgr.cell.destroyAllEntities()
        _sVal.completedReasonType = reasonType
        _sVal.spaceMgr.cell.onTeamDungeonCompleted(spaceNo, teamUUID, win, delay, _sVal.getElapsedTime(), 0, _sVal.completedReasonType)
        # 跨服讨伐无本服公会副本任务联动
        if win and not _isCross:
            _sVal.spaceMgr.cell.finishGuildDungeonTask()

        if delay:
            if not _isCross:
                lastDungeonFinishedTime = utils.curTS() + delay
                _teamStub = gameengine.getTeamStub(_sVal.teamUUID)
                _teamStub.refreshLastDungeonFinishedTime(_sVal.teamUUID, lastDungeonFinishedTime)
            _sVal.completeDungeonTimer = self.addTimerCB(
                delay, '_onTeamDungeonCompletedCallback',
                (spaceNo, _sVal.spaceUUID, 'dungeon complete', win), gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onTeamDungeonCompletedCallback(spaceNo, _sVal.spaceUUID, 'dungeon complete', win)

    def _onTeamDungeonCompletedCallback(self, spaceNo, spaceUUID, reason, win):
        LOG_INFO('_onTeamDungeonCompletedCallback::', spaceNo, spaceUUID, reason, win)
        if spaceNo not in self.spaces:
            LOG_ERR('_onTeamDungeonCompletedCallback::cannot get space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        _sVal.completeDungeonTimer = 0
        if _sVal.spaceUUID != spaceUUID:
            LOG_ERR('_onTeamDungeonCompletedCallback:: spaceUUID not match', _sVal.spaceUUID, spaceUUID)
            return

        if not _sVal.isActive():
            LOG_WARN('_onTeamDungeonCompletedCallback:: already complete', spaceNo, _sVal.state)
            return

        # 【副本服务端报错】
        # completecallback后取消其他completecallback回调
        _sVal.clearCompleteTimer()

        _sVal.completeDungeon(win)

        if _sVal.isCrossDungeon():
            # 跨服讨伐：通知中心复位 InDungeon（队伍不解散），空间销毁由本 stub 自行处理
            # （本服线由 TeamStub.onTeamDungeonCompletedCB 负责后续销毁）
            gameengine.getCrossTeamStub(_sVal.teamUUID).crusadeFinished(_sVal.teamUUID, 1 if win else 0)
            self.destoryDungeonSpace(spaceNo, spaceUUID, reason)
            return

        extra = {
            'tCreate': _sVal.tCreate,
            'tState': _sVal.state,
            'forceDestroy': True,
            }

        gameengine.getTeamStub(_sVal.teamUUID).onTeamDungeonCompletedCB(_sVal.teamUUID, self.dungeonNo, spaceNo, reason, extra)

    def doEnterDungeon(self, box, gbId, teamUUID, spaceNo, extra):
        if spaceNo not in self.spaces:
            LOG_ERR(f'spaceNo "{spaceNo}" not found in spaces')
            if extra and extra.get('crossTeamId'):
                # 跨服讨伐进本失败：无本服 TeamStub 可回退，仅记录（镜像由中心中止/超时流程回收）
                return
            _teamStub = gameengine.getTeamStub(teamUUID)
            _teamStub.onEnterDungeonFailedSpaceNotFound(box, gbId, teamUUID, self.dungeonNo, spaceNo, extra)
            return

        _spaceVal = self.spaces[spaceNo]

        if _spaceVal.isCompleted():
            LOG_ERR("space already completed", spaceNo, _spaceVal.spaceUUID)
            return

        if _spaceVal.markDestroy:
            LOG_ERR('spaceNo "{}" already be destroy delay'.format(spaceNo))
            return

        spaceBox = _spaceVal.spaceBox
        spaceMgr = _spaceVal.spaceMgr
        spaceMgr.cell.doEnterTeamDungeon(box, gbId, _spaceVal.spaceUUID, spaceBox, extra)

    def enterDungeonSpaceSuccess(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        # 本服 team 线成员登记由 TeamStub.onEnterTeamDungeon 完成（不走这里）；
        # 仅跨服讨伐（CROSS_CRUSADE）需要：founders 簿记（最后一人离开自动完成用）
        # + 结算数据登记（对照本服 DungeonSpaceMgr.doEnterTeamDungeon 的 notifyDungeonExtarData；
        # 直进副本路径不经过 doEnterTeamDungeon，统一在这里补登记）
        _sVal = self.spaces.get(spaceNo)
        if not _sVal or not _sVal.isCrossDungeon():
            return

        _sVal.founders.addFounder(spaceNo, playerGbId, playerBox)
        _founderVal = _sVal.founders.getFounderVal(playerGbId)
        _founderVal.tEnter = utils.curTS()
        _founderVal.tLeave = 0
        _founderVal.isEnter = True

        _data = DungeonSettlement.DungeonExtraData()
        _data.loadDatas(extra or {})
        _sVal.spaceMgr.cell.notifyDungeonExtarData(playerGbId, _data)

    def _getDungeonSpaceVal(self, spaceNo, playerBox, _, teamUUID, extra):
        _spaceVal = dungeon.TeamDungeonSpaceVal(
            spaceNo=spaceNo,
            spaceUUID=0, 
            spaceMgr=None,
            spaceBox=None, 
            teamUUID=teamUUID, 
            spaceLevel=extra['spaceLevel'], 
            extraDic={
                'maxLevel':extra['maxLevel'],
            }
        )
        # 跨服讨伐（CROSS_CRUSADE）：playMode 记到 SpaceVal 供各回调分支判断；
        # founders 簿记挂 SpaceVal（本服线 founders 在 TeamStub 侧，跨服无 TeamStub）
        _playMode = extra.get('dungeonPlayMode')
        if _playMode and _playMode.playMode in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            _spaceVal.playMode = _playMode.playMode
            _spaceVal.founders = team.TeamDungeonFounders()
        return _spaceVal

    def applyCreateDungeon(self, box, gbId, teamUUID, extra):
        self.createDungeonSpaceRemote(box, gbId, teamUUID, extra)

    def getDungeonSpaceRange(self):
        enterType = DDI.datas[self.dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.SINGLE)
        if enterType==gameconst.DungeonEnterTypeEnum.BOTH:
            return gameconst.SpaceType.getTeamDungeonSpaceRange(self.dungeonNo)
        else:
            return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)

    def _getDungeonSpaceWeight(self, enterNum=5) -> int:
        return utils.calcSpaceWeight(enterNum, False, gameconst.EntNumPerPlayerInAOI.teamDungeon)

    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, teamUUID, extraData):
        # ready first
        self.onLoadDungeonSpaceReady(playerBox, spaceNo, teamUUID, extraData)
        # use iCreateDungeonMonster function
        return super(TeamDungeonStub, self)._loadDungeonSpaceEntities(
            spaceNo, playerBox, playerGbId, teamUUID, extraData)

    def onLoadDungeonSpaceReady(self, playerBox, spaceNo, teamUUID, extra):
        LOG_INFO('onLoadDungeonSpaceReady::')
        _spaceVal = self.spaces[spaceNo]
        if _spaceVal.isCrossDungeon():
            # 跨服讨伐：回报 CrossTeamStub（更新簿记并上报中心），不走本服 TeamStub；
            # spaceBox/spaceMgrBox 随簿记保存（镜像登录直进副本建 cell 用）
            gameengine.getCrossTeamStub(teamUUID).onCrossCrusadeSpaceReady(
                teamUUID,
                spaceNo,
                _spaceVal.spaceUUID,
                True,
                _spaceVal.spaceBox,
                _spaceVal.spaceMgr
            )
            return
        _teamStub = gameengine.getTeamStub(teamUUID)
        _teamStub.afterCreateTeamDungeon(teamUUID, self.dungeonNo, spaceNo, _spaceVal.spaceUUID, playerBox, extra)

    def leaveTeamDungeon(self, spaceNo, teamID, src, playerBox):
        LOG_INFO("leaveTeamDungeon~ ", spaceNo, teamID, src, playerBox)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveTeamDungeon:: failed, missing space data', spaceNo, src, playerBox)
            return
        dungeonVal = self.spaces[spaceNo]
        founders = len(dungeonVal.founders)
        if founders <= 1:
            self.completeTeamDungeon(spaceNo, teamID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)
        else:
            playerBox.cell.selfLeaveTeamDungeon(src)

