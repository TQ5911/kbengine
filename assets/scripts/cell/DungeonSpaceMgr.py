# -*- coding: utf-8 -*-

import zlib
import random

import KBEngine
from KBEDebug import *

import formula
import gamelog
import gametlog
import gameconst
import gameengine
import utils
import gametimer
import awardContext
import math, sMath
import json

import iCell
import iTimer
import iSpaceMgr
import iFubenSpace
import flowController

import dropAward
import dungeonPlayMode

import gamePlay_gamePlay as DDI
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import activityControl_config as ACCD


class DungeonPlayerReliveRecordMixin(object):
    def __init__(self):
        if not hasattr(self, 'dungeonPlayerReliveRecordDic'):
            self.dungeonPlayerReliveRecordDic = {}

    def getPlayerReliveRecord(self, playerGBID):
        return self.dungeonPlayerReliveRecordDic.get(playerGBID, 0)

    def addPlayerReliveRecord(self, playerGBID):
        self.dungeonPlayerReliveRecordDic.setdefault(playerGBID, 0)
        self.dungeonPlayerReliveRecordDic[playerGBID] += 1

    def clearPlayerReliveRecord(self, playerGBID):
        self.dungeonPlayerReliveRecordDic[playerGBID] = 0

    def clearAllPlayersReliveRecords(self):
        self.dungeonPlayerReliveRecordDic.clear()


class DungeonSpaceMgr(iCell.ICell, iTimer.ITimer, iSpaceMgr.ISpaceMgr, DungeonPlayerReliveRecordMixin):
    def __init__(self):
        INFO_MSG("DungeonSpaceMgr#__init__", self.spaceNo, self.spaceID)

        iCell.ICell.__init__(self)
        iSpaceMgr.ISpaceMgr.__init__(self)

        if not self.dungeonPlayMode:
            self.dungeonPlayMode = dungeonPlayMode.UnknownDungeonPlayMode()

        gameengine.getDungeonStubBySpaceNo(self.spaceNo).onDungeonSpaceMgrReady(self.spaceNo)

    @property
    def dungeonTimeFreezeFlag(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.dungeonTimeFreezeSpaceMgrFlag, default=False)

    @dungeonTimeFreezeFlag.setter
    def dungeonTimeFreezeFlag(self, newFlag):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.dungeonTimeFreezeSpaceMgrFlag, bool(newFlag))

    @property
    def dungeonRewardBossID(self):
        if not self.hasTempMiscProp(gameconst.DungeonSpaceMgrProps.dungeonRewardBossID):
            self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.dungeonRewardBossID, 0)
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.dungeonRewardBossID)

    @dungeonRewardBossID.setter
    def dungeonRewardBossID(self, newVal):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.dungeonRewardBossID, newVal)

    @property
    def singleDungeonBelongPlayerGBID(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.singleDungeonBelongPlayerGBID, 0)

    @property
    def teamDungeonBelongTeamUUID(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.teamDungeonBelongTeamUUID, 0)

    @property
    def raidDungeonBelongRaidUUID(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.raidDungeonBelongRaidUUID, 0)

    @property
    def isDungeonWin(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.dungeonWinFlagSpaceMgrCache, False)

    @isDungeonWin.setter
    def isDungeonWin(self, newFlag: bool):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.dungeonWinFlagSpaceMgrCache, bool(newFlag))

    @property
    def spaceUUID(self):
        return self.dungeonPlayMode.spaceUUID

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(DungeonSpaceMgr, self).onTimer(tid, userData)

    def _checkDungeonTimeout(self):
        tCreate = self.dungeonPlayMode.tCreate
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        endTime = int(tCreate + DDI.datas[dungeonNo]['timeOut'] * 60 + 1)
        if utils.getNow() > endTime:
            WARNING_MSG('_checkDungeonTimeout:: timeout', dungeonNo)
            self.onDungeonTimeout()
            return
        self.toCallbackAfter(1)._checkDungeonTimeout()

    def initAIController(self):
        pass
        # mapId=formula.getMapId(self.spaceNo)
        # aiNo=SSD.datas.get(mapId, {}).get('treeID')
        # if not aiNo:
        #     return
        #
        # self.aiController=spaceMgrAIController.SpaceMgrAIController(self.id, str(aiNo))
        # self.tickAI()

    def initFlowController(self):
        spaceNo = self.spaceNo
        dungeonNo = formula.getMapId(spaceNo)
        if utils.isDunFlowModuleDataExist(dungeonNo):
            self._initFlowController(dungeonNo)
        else:
            # 【【任务】副本支持空副本流程】
            dunStubBox = gameengine.getDungeonStubBySpaceNo(spaceNo)
            dunStubBox.onDungeonStarted(spaceNo, 0)

    def _initFlowController(self, dungeonNo=-1):
        spaceNo = self.spaceNo
        if dungeonNo <= 0:
            dungeonNo = formula.getMapId(spaceNo)
        try:
            self.flowController, nodes = flowController.buildFlowController(dungeonNo, spaceNo, self)
            self.flowController.check_all()
        except Exception as e:
            import traceback
            traceback.print_exc()
            ERROR_MSG('initFlowController::exception got: ', e)
            return

        self._callback(0.5, '_flowStart', (), gametimer.TIMER_TAG_FLOW_START)

    def resetFlowControllerStartByStage(self, dungeonStageID):
        DEBUG_MSG('resetStartNodeByStage::', dungeonStageID)
        assert dungeonStageID >= 0
        import ep_ctrl

        controller = self.flowController
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        for eventId, event in controller._elements.items():
            if event.name == '{}_{}'.format(gameconst.DungeonFlowEventName.dunStageSet, eventId) \
                    and event.get_param('dungeonStageID', -1) == dungeonStageID:
                # 创建头空节点和副本开始节点
                _sentinelEvent = controller.build_element(flowController.FlowEvent, 0)
                newStartEvent = controller.buildStartDungeonEvent(ep_ctrl.utils.gen_uuid(), dungeonNo, self.spaceNo)
                _sentinelEvent.bind_element(newStartEvent, 1, 1)
                newStartEvent.bind_element(event, 1, 1)
                controller.replace_start_node(_sentinelEvent)
                return True
        else:
            ERROR_MSG('resetStartNodeByStage:: dungeonStageID not found', dungeonStageID)
            return False

    def _flowStart(self):
        WARNING_MSG('_flowStart:: NOW')
        # 【【任务】团队副本的创建和进入接口独立】
        if not self.players and not formula.isRaidDungeonSpace(self.spaceNo):
            # 对于一下情况, 直接开始副本流程逻辑(不等待玩家)
            # 1. 团队副本
            self.toCallbackAfter(0.5)._flowStart()
            return

        for pid in self.players:
            ent = KBEngine.entities.get(pid)
            # if not (ent and ent.isReal() and ent.newbieTaskInitFinishe):
            if not (ent and ent.isReal()):
                self.toCallbackAfter(0.5)._flowStart()
                return

        if self.dungeonStage:
            WARNING_MSG('_flowStart:: NOW FROM STAGE, {}'.format(self.dungeonStage))
            r = self.resetFlowControllerStartByStage(self.dungeonStage)
            if not r:
                gameengine.reportCritical('_flowStart:: STAGE NOT FOUND', self.dungeonStage)
                return

        self.flowController.trigger_now()

    def getBossEntity(self):
        return self.getEntitiyByTag(gameconst.HomeEntType.getTypeDesc(gameconst.HomeEntType.Boss))

    def changeDungeonStageSet(self, newStageID):
        DEBUG_MSG('changeDungeonStageSet::', newStageID)
        oldStageID = self.dungeonStage
        self._changeDungeonStageSet(oldStageID, newStageID, toClient=True)

    def _changeDungeonStageSet(self, oldStageID, newStageID, toClient=False, now=None):
        DEBUG_MSG('in _changeDungeonStageSet:', oldStageID, newStageID, self.dungeonPlayMode.__dict__)
        self.dungeonStage = newStageID
        self.dungeonStageStartT = now or utils.getNow()

        _isDongfuWarDungeon = self.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.DONGFU_WAR
        _isSoulCardDungeon = self.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.SOULCARD
        _isQimoCave = self.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.QIMOCAVE
        _isHanQingDungeon = self.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.HANQING

        if _isDongfuWarDungeon:
            self.dungeonPlayMode.guildBox.updateDongfuWarDungeonStage(
                self.spaceNo, oldStageID, newStageID)

        if _isHanQingDungeon:
            for pid in self.players:
                ent = KBEngine.entities.get(pid)
                if not ent:
                    continue
                ent.hanQingDungeonTransform(oldStageID, newStageID)

        if toClient:
            for pid in self.players:
                ent = KBEngine.entities.get(pid)
                if not ent:
                    continue

                if _isSoulCardDungeon:
                    self.getSoulCardDungeonRemainStage(ent.base, ent.gbId)
                    ent.client.onSoulCardDungeonStageChange(self.spaceNo, newStageID)
                elif _isQimoCave:
                    ent.client.onSendQimoCaveDungeonMonsterInfo(newStageID)
                else:
                    ent.client.onChangeDungeonStageSet(self.spaceNo, oldStageID, newStageID)

    def onDungeonStarted(self, tCreate):
        DEBUG_MSG('onDungeonStarted::', tCreate, self.dungeonPlayMode.playMode)
        self.dungeonPlayMode.tCreate = tCreate
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        endTime = int(tCreate + DDI.datas[dungeonNo]['timeOut'] * 60 + 1)
        self.toCallbackAfter(1)._checkDungeonTimeout()
        for pid in self.players:
            ent = KBEngine.entities.get(pid)
            if ent and ent.isReal() and formula.isDungeonSpace(ent.spaceNo):
                if formula.getDungeonNoBySpaceNo(self.spaceNo) == formula.getDungeonNoBySpaceNo(ent.spaceNo):
                    ent.client.changeDungeonRemainTime(self.spaceNo, endTime)

    def onPlayerOffline(self, playerId, playerGbId):
        super(DungeonSpaceMgr, self).onPlayerOffline(playerId, playerGbId)
        self.flowCtrlDungeonAlivePlayerDecreased(self.getAlivePlayerNumber())

    def onPlayerRelogin(self, box, playerGbId):
        super(DungeonSpaceMgr, self).onPlayerRelogin(box, playerGbId)
        if self.transPetId:
            box.client.newTransPetStart(self.transPetId, self.triggerGuideId)

    def onPlayerEnter(self, playerId):
        INFO_MSG('onPlayerEnter', playerId)
        super(DungeonSpaceMgr, self).onPlayerEnter(playerId)
        self.flowCtrlDungeonAlivePlayerIncreased(self.getAlivePlayerNumber())
        self.flowCtrlDungeonPlayerRestNumChanged(len(self.players))
        pent = KBEngine.entities.get(playerId)
        if pent:
            pent.sendDunTimeFreezeFlag()

    def onPlayerLeave(self, playerGbId, playerId, box):
        INFO_MSG('onPlayerLeave', playerGbId, playerId, box)
        super(DungeonSpaceMgr, self).onPlayerLeave(playerGbId, playerId, box)
        self.flowCtrlDungeonAlivePlayerDecreased(self.getAlivePlayerNumber())
        self.flowCtrlDungeonPlayerRestNumChanged(len(self.players))

    def addEntity(self, entId, tags):
        super(DungeonSpaceMgr, self).addEntity(entId, tags)
        ent = KBEngine.entities.get(entId)

        _hostEnt, _ = utils.getRealAvatarEnt(ent)

        if hasattr(ent, 'gameEntityIdentifyID'):
            if ent.gameEntityIdentifyID <= 0:
                WARNING_MSG("DungeonSpaceMgr::addEntity:: gameEntityIdentifyID zero", ent, tags, ent.gameEntityIdentifyID)
                return
            gameengine.getDungeonStubBySpaceNo(self.spaceNo).onEntityCreated(
                self.spaceNo, self.spaceUUID, entId, ent.gameEntityIdentifyID)
            
        if 'RebornPos' in tags:
            gameengine.getDungeonStubBySpaceNo(self.spaceNo).onCreateNewRebornPos(self.spaceNo, ent.position)

    def onPlayerDead(self, box, playerGbId):
        super(DungeonSpaceMgr, self).onPlayerDead(box, playerGbId)
        self.flowCtrlDungeonAlivePlayerDecreased(self.getAlivePlayerNumber())

    def onPlayerRelive(self, box, playerGbId):
        super(DungeonSpaceMgr, self).onPlayerRelive(box, playerGbId)
        self.flowCtrlDungeonAlivePlayerIncreased(self.getAlivePlayerNumber())

    def getAlivePlayerNumber(self):
        return len(list(filter(lambda p: not p.isPlayerDead(), self.players.values())))

    def onDungeonTimeout(self):
        INFO_MSG('onDungeonTimeout::')
        # 【【任务】副本结束逻辑调整】
        # 1.表里配置的副本最长时间结束后，不需要再延迟了，直接销毁副本。
        delay = 0
        # for pid in self.players:
        #     ent = KBEngine.entities.get(pid)
        #     if ent and ent.isReal() and formula.isDungeonSpace(ent.spaceNo):
        #         if formula.getDungeonNoBySpaceNo(self.spaceNo) == formula.getDungeonNoBySpaceNo(ent.spaceNo):
        #             ent.client.changeDungeonRemainTime(self.spaceNo, utils.getNow() + delay)
        stub = gameengine.getDungeonStubBySpaceNo(self.spaceNo)
        if formula.isSingleDungeonSpace(self.spaceNo):
            stub.completeSingleDungeon(self.spaceNo, self.singleDungeonBelongPlayerGBID, False, delay)
        elif formula.isTeamDungeonSpace(self.spaceNo):
            stub.completeTeamDungeon(self.spaceNo, self.teamDungeonBelongTeamUUID, False, delay)
        elif formula.isRaidDungeonSpace(self.spaceNo):
            stub.completeRaidDungeon(self.spaceNo, self.raidDungeonBelongRaidUUID, False, delay)

    def _handlePlayerDungeonFlowTlogWithExtra(self, pEnt, spaceNo, tlogProps):
        _playMode = self.dungeonPlayMode
        extra = {}
        if not _playMode:
            pass

        # tlogProps.update({"vExtra": json.dumps(extra)})
        # tlogProps['iTeamMemNum'] = pEnt.teamInfo.howManyMember() if pEnt.isInTeam(pEnt.gbId) else 0
        # pEnt.base.handleDungeonFlowTlog(spaceNo, tlogProps)

    def onSingleDungeonCompleted(self, spaceNo, playerGbId, win, delay, elapsedTime):
        DEBUG_MSG('onSingleDungeonCompleted::', spaceNo, playerGbId, win, delay, elapsedTime)
        self._onDungeonCompleted(spaceNo, win, delay, elapsedTime)
        self._onSingleDungeonCompleted(spaceNo, playerGbId, win)

    def _onSingleDungeonCompleted(self, spaceNo, playerGbId, win):
        _dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        _tlogDungeonFlowCommon = dict(GameSvrId=None, dtEventTime=None, vGameAppid=None,
                                      iBattleID=formula.getDungeonNoBySpaceNo(spaceNo),
                                      iResult=int(win), SingleOrteam=gametlog.SingleOrteam.SINGLE)

        now = utils.getNow()
        for pid in self.players:
            pEnt = KBEngine.entities.get(pid)
            if not pEnt:
                continue

            _tlogDungeonFlowCommon.update(dict(iRoundTime=max(0, now - pEnt.getSpaceEnterT())))
            self._handlePlayerDungeonFlowTlogWithExtra(pEnt, spaceNo, _tlogDungeonFlowCommon)

    def onTeamDungeonCompleted(self, spaceNo, teamUUID, win, delay, elapsedTime):
        DEBUG_MSG('onTeamDungeonCompleted::', spaceNo, teamUUID, win, delay, elapsedTime)
        self._onDungeonCompleted(spaceNo, win, delay, elapsedTime)
        self._onTeamDungeonCompleted(spaceNo, teamUUID, win)

    def _onTeamDungeonCompleted(self, spaceNo, teamUUID, win):
        _dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        _tlogDungeonFlowCommon = dict(GameSvrId=None, dtEventTime=None, vGameAppid=None,
                                      iBattleID=formula.getDungeonNoBySpaceNo(spaceNo),
                                      iResult=int(win), SingleOrteam=gametlog.SingleOrteam.TEAM)

        now = utils.getNow()
        for pid in self.players:
            pEnt = KBEngine.entities.get(pid)
            if not pEnt:
                continue

            _tlogDungeonFlowCommon.update(dict(iRoundTime=max(0, now - pEnt.getSpaceEnterT())))
            self._handlePlayerDungeonFlowTlogWithExtra(pEnt, spaceNo, _tlogDungeonFlowCommon)

    def onRaidDungeonCompleted(self, spaceNo, raidUUID, win, delay, creepBaseKillDic, playerGbidAndNameList, elapsedTime):
        DEBUG_MSG('onRaidDungeonCompleted::', spaceNo, raidUUID, win, delay, creepBaseKillDic, len(playerGbidAndNameList), elapsedTime)
        self._onDungeonCompleted(spaceNo, win, delay, elapsedTime)
        self._onRaidDungeonCompleted(spaceNo, raidUUID, win, creepBaseKillDic, playerGbidAndNameList)

    def _onRaidDungeonCompleted(self, spaceNo, raidUUID, win, creepBaseKillDic, playerGbidAndNameList):
        _dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        _tlogDungeonFlowCommon = dict(GameSvrId=None, dtEventTime=None, vGameAppid=None,
                                      iBattleID=formula.getDungeonNoBySpaceNo(spaceNo),
                                      iResult=int(win), SingleOrteam=gametlog.SingleOrteam.RAID)

        now = utils.getNow()
        for pid in self.players:
            pEnt = KBEngine.entities.get(pid)
            if not pEnt:
                continue

            _tlogDungeonFlowCommon.update(dict(iRoundTime=max(0, now - pEnt.getSpaceEnterT())))
            self._handlePlayerDungeonFlowTlogWithExtra(pEnt, spaceNo, _tlogDungeonFlowCommon)

    def _onDungeonCompleted(self, spaceNo, win, delay, elapsedTime):
        self.isDungeonWin = win

        _now = utils.getNow()
        _endT = int(_now + delay)
        _pEntList = []
        _allPlayersAreGoodMan = False

        for pid in list(self.players):
            pEnt = KBEngine.entities.get(pid)
            # 【退出副本有5s倒计时存在。】
            # 服务端可以先检测space过滤已经离开副本但还没有从spaceMgr上反注册的玩家
            if pEnt and pEnt.isReal():

                if _allPlayersAreGoodMan:
                    # 【【任务】队伍无助力目标时返回MSG提示】
                    pEnt.showMsg(ACCD.datas["msgId_goodMan_noHelpTarget"]["value"], [])

                dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
                pEnt.client.onDungeonCompleted(dungeonNo, win, elapsedTime)
                pEnt.client.changeDungeonRemainTime(spaceNo, _endT)

                _pEntList.append(pEnt)

            else:
                self.players.pop(pid, None)

        try:

            _tlogRoundEndFlowCommon = dict(GameSvrId=None, dtEventTime=None, vGameAppid=None,
                                           iBattleID=formula.getDungeonNoBySpaceNo(spaceNo),
                                           iResult=int(self.isDungeonWin), iRank=0)
            _tlogRoundFlowCommon = dict(GameSvrId=None, dtEventTime=None, vGameAppid=None,
                                        iBattleID=formula.getDungeonNoBySpaceNo(spaceNo),
                                        iResult=int(self.isDungeonWin), iRank=0, vExtra="")
            for pEnt in _pEntList:
                _tlogRoundEndFlowKWargs = dict(iRoundTime=max(0, utils.getNow() - pEnt.getSpaceEnterT()))
                _tlogRoundEndFlowKWargs.update(_tlogRoundEndFlowCommon)
                _tlogRoundFlowKWargs = dict(iRoundTime=max(0, utils.getNow() - pEnt.getSpaceEnterT()),
                                            teamMemNum=pEnt.teamInfo.howManyMember() if pEnt.isInTeam(pEnt.gbId) else 0)
                _tlogRoundFlowKWargs.update(_tlogRoundFlowCommon)


        finally:
            del _pEntList

    def onUpdateChallengeInfo(self, hpPercent):
        isChallengeDun = bool(self.dungeonPlayMode and self.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CHALLENGE_DUNGEON)
        if not isChallengeDun or self.dungeonPlayMode.easy:
            return

        now = utils.getNow()
        for pid in list(self.players):
            pEnt = KBEngine.entities.get(pid)
            if pEnt and pEnt.isReal():
                costTime = now - pEnt.getSpaceEnterT()
                pEnt.base.updateChallengeSpeedRaceInfo(hpPercent, costTime, self.dungeonPlayMode.dunLevel)

    def doEnterTeamDungeon(self, playerBox, playerGBID, spaceUUID, spaceBox, extra):
        INFO_MSG("doEnterTeamDungeon::", playerBox, playerGBID, spaceUUID, spaceBox, extra)
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        if DDI.datas[dungeonNo]['enterBlockByCombat']:
            for pid in self.players:
                pEnt = KBEngine.entities.get(pid)
                if not pEnt:
                    continue
                if pEnt.hasState(gameconst.State.Fighting):
                    WARNING_MSG("doEnterTeamDungeon:: failed, player is in fighting state", self.spaceNo)
                    return
        playerBox.cell.doEnterTeamDungeon(self.spaceNo, spaceUUID, spaceBox, self.base, extra)

    def enterRaidDungeonDirectly(self, playerBox, playerGBID, spaceUUID, spaceBox, src, extraProps):
        DEBUG_MSG("enterRaidDungeonDirectly::", playerBox, playerGBID, spaceUUID, spaceBox, src, extraProps)
        m_dungeonNo, m_errno = self._enterRaidDungeonDirectly(playerBox, playerGBID, spaceUUID, spaceBox, src)
        if m_errno != gameconst.RaidDungeonErrno.RAIDDUN_OK:
            WARNING_MSG(f"enterRaidDungeonDirectly::failed, errno={m_errno}")
        playerBox.cell.doEnterRaidDungeonAfterCheck(m_dungeonNo, self.spaceNo, spaceUUID, spaceBox, self.base, src, extraProps)

    def _enterRaidDungeonDirectly(self, playerBox, playerGBID, spaceUUID, spaceBox, src):
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        if DDI.datas[dungeonNo]['enterBlockByCombat']:
            for pid in self.players:
                pEnt = KBEngine.entities.get(pid)
                if not pEnt:
                    continue
                if pEnt.hasState(gameconst.State.Fighting):
                    return None, gameconst.RaidDungeonErrno.RAIDDUN_ENTER_BLOCK_BY_COMBAT

        return dungeonNo, gameconst.RaidDungeonErrno.RAIDDUN_OK

    def onCollectionBeCollect(self, entityGID, collectionId):
        super().onCollectionBeCollect(entityGID, collectionId)
        self.flowCtrlDungeonCollectionBeCollected(entityGID, collectionId)


    @property
    def transPetId(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.transPetId, 0)

    @transPetId.setter
    def transPetId(self, newVal):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.transPetId, newVal)

    @property
    def triggerGuideId(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.triggerGuideId, 0)

    @triggerGuideId.setter
    def triggerGuideId(self, newVal):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.triggerGuideId, newVal)

    def startTimeFreeze(self):
        self.dungeonTimeFreezeFlag = True
        # NOTE(): 客户端要求先推送其他Entity的Flag, 最后推送玩家client的协议
        #            不要改变两个循环的顺序
        for eid in self.spaceEntities:
            ent = KBEngine.entities.get(eid)
            if ent and ent.id != self.id:
                ent.startDunTimeFreeze()
        for pid in self.players:
            pent = KBEngine.entities.get(pid)
            if pent and pent.isReal():
                pent.startDunTimeFreeze()

    def stopTimeFreeze(self):
        # NOTE(): 客户端要求先推送其他Entity的Flag, 最后推送玩家client的协议
        #            不要改变两个循环的顺序
        self.dungeonTimeFreezeFlag = False
        for eid in self.spaceEntities:
            ent = KBEngine.entities.get(eid)
            if ent and ent.id != self.id:
                ent.stopDunTimeFreeze()
        for pid in self.players:
            pent = KBEngine.entities.get(pid)
            if pent and pent.isReal():
                pent.stopDunTimeFreeze()
