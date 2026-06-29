# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import formula
import gameconst
import gameengine
import utils
import gametimer

import iCell
import iTimer
import iSpaceMgr
import flowController
import dungeonPlayMode
import DungeonSettlement
import LogTrackingMgr

import gamePlay_gamePlay as DDI
import activityControl_config as ACCD
import teamMatch_matchConfig as TMMCD
import teamMatch_pointsRanking as TM_PR
import creep_base as CBD

class DungeonPlayerReliveRecordMixin(object):
    def __init__(self):
        if not hasattr(self, 'dunPlayerReliveRecordDic'):
            self.dunPlayerReliveRecordDic = {}

    def getPlayerReliveRecord(self, playerGBID):
        return self.dunPlayerReliveRecordDic.get(playerGBID, 0)

    def addPlayerReliveRecord(self, playerGBID):
        self.dunPlayerReliveRecordDic.setdefault(playerGBID, 0)
        self.dunPlayerReliveRecordDic[playerGBID] += 1

    def clearPlayerReliveRecord(self, playerGBID):
        self.dunPlayerReliveRecordDic[playerGBID] = 0

    def clearAllPlayersReliveRecords(self):
        self.dunPlayerReliveRecordDic.clear()

class DungeonCompleteDelayNotifyMixin(object):
    def __init__(self):
        if not hasattr(self, 'dungeonCompleteDelayNotifyTimer'):
            self.dungeonCompleteDelayNotifyTimer = 0
    
    def cancelCompleteDelayNotifyTimer(self, owner, tag):
        LOG_INFO('cancelCompleteDelayNotifyTimer~', owner, tag)
        if self.dungeonCompleteDelayNotifyTimer:
            owner.cancelTimerCB(self.dungeonCompleteDelayNotifyTimer, tag)
        self.clearCompleteDelayNotifyTimer()

    def clearCompleteDelayNotifyTimer(self):
        self.dungeonCompleteDelayNotifyTimer = 0

    def getCompleteDelayNotifyTime(self):
        return int(TMMCD.datas['copySettlementInterval']['value'])


class DungeonSpaceMgr(iCell.ICell, iTimer.ITimer, iSpaceMgr.ISpaceMgr, DungeonPlayerReliveRecordMixin, DungeonCompleteDelayNotifyMixin):
    def __init__(self):
        LOG_INFO("DungeonSpaceMgr#__init__", self.spaceNo, self.spaceID)

        iCell.ICell.__init__(self)
        iSpaceMgr.ISpaceMgr.__init__(self)
        # 副本不用定刷
        #self.initDatetimeTimerTick()

        self.dungeonSettlementDataCache = {}
        if not self.dungeonPlayMode:
            self.dungeonPlayMode = dungeonPlayMode.UnknownDungeonPlayMode()

        gameengine.getDungeonStubBySpaceNo(self.spaceNo).onDunSpaceMgrReady(self.spaceNo)

    @property
    def dungeonTimeFreezeFlag(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumdungeonTimeFreezeSpaceMgrFlag, default=False)

    @dungeonTimeFreezeFlag.setter
    def dungeonTimeFreezeFlag(self, newFlag):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumdungeonTimeFreezeSpaceMgrFlag, bool(newFlag))

    @property
    def dungeonRewardBossID(self):
        if not self.hasTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumdungeonRewardBossID):
            self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumdungeonRewardBossID, 0)
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumdungeonRewardBossID)

    @dungeonRewardBossID.setter
    def dungeonRewardBossID(self, newVal):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumdungeonRewardBossID, newVal)

    @property
    def singleDungeonBelongPlayerGBID(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumsingleDungeonBelongPlayerGBID, 0)

    @property
    def teamDungeonBelongTeamUUID(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumteamDungeonBelongTeamUUID, 0)

    @property
    def raidDungeonBelongRaidUUID(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumraidDungeonBelongRaidUUID, 0)

    @property
    def guildBossDungeonBelongGuildUUID(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumguildBossDungeonBelongGuildUUID, 0)
    
    @property
    def isDungeonWin(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumdungeonWinFlagSpaceMgrCache, False)

    @isDungeonWin.setter
    def isDungeonWin(self, newFlag: bool):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumdungeonWinFlagSpaceMgrCache, bool(newFlag))

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        else:
            super(DungeonSpaceMgr, self).onTimer(tid, userData)

    @property
    def spaceUUID(self):
        return self.dungeonPlayMode.spaceUUID

    def _checkDungeonTimeout(self):
        tCreate = self.dungeonPlayMode.tCreate
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        endTime = int(tCreate + DDI.datas[dungeonNo]['timeOut'] * 60 + 1)
        if utils.curTS() > endTime:
            LOG_WARN('_checkDungeonTimeout:: timeout', dungeonNo)
            self.onDungeonTimeout()
            return
        self.asyncCallbackAfter(1)._checkDungeonTimeout()

    def initFlowController(self):
        spaceNo = self.spaceNo
        dungeonNo = formula.fetchMapId(spaceNo)
        if utils.checkDunFlowModuleDataExist(dungeonNo):
            self._initFlowController(dungeonNo)
        else:
            # 【【任务】副本支持空副本流程】
            _dunStubBox = gameengine.getDungeonStubBySpaceNo(spaceNo)
            _dunStubBox.onDungeonStarted(spaceNo, 0)

    def _initFlowController(self, dungeonNo=-1):
        _spaceNo = self.spaceNo
        if dungeonNo <= 0:
            dungeonNo = formula.fetchMapId(_spaceNo)
        try:
            self.flowController, _ = flowController.buildFlowController(dungeonNo, _spaceNo, self)
            self.flowController.check_all()
        except Exception as e:
            import traceback
            traceback.print_exc()
            LOG_ERR('initFlowController::exception got: ', e)
            return

        self.addTimerCB(0.5, '_flowStart', (), gametimer.TIMER_TAG_FLOW_START)

    def resetFlowControllerStartByStage(self, dungeonStageID):
        LOG_INFO('resetStartNodeByStage::', dungeonStageID)
        assert dungeonStageID >= 0
        import ep_ctrl

        controller = self.flowController
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        for eventId, event in controller.elementsDic.items():
            if event.name == '{}_{}'.format(gameconst.DungeonFlowEventType.EVdunStageSet, eventId) \
                    and event.fetchArgument('dungeonStageID', -1) == dungeonStageID:
                # 创建头空节点和副本开始节点
                _sentinelEvent = controller.buildElement(flowController.FlowNodeEvent, 0)
                _newStartEvent = controller.buildStartDungeonEvent(ep_ctrl.utils.gen_uuid(), dungeonNo, self.spaceNo)
                _sentinelEvent.bind_element(_newStartEvent, 1, 1)
                _newStartEvent.bind_element(event, 1, 1)
                controller.replace_start_node(_sentinelEvent)
                return True
        else:
            LOG_ERR('resetStartNodeByStage:: dungeonStageID not found', dungeonStageID)
            return False

    def _flowStart(self):
        LOG_WARN('_flowStart:: NOW')
        # 帮会副本直接开始流程
        if formula.inGuildBossDungeonScene(self.spaceNo):
            self.flowController.trigger_now()
            return
        
        # 【【任务】团队副本的创建和进入接口独立】
        if not self.players and not formula.inRaidDungeonScene(self.spaceNo):
            # 对于一下情况, 直接开始副本流程逻辑(不等待玩家)
            # 1. 团队副本
            self.asyncCallbackAfter(0.5)._flowStart()
            return

        for pid in self.players:
            ent = KBEngine.entities.get(pid)
            # if not (ent and ent.isReal() and ent.newbieTaskInitFinishe):
            if not (ent and ent.isReal()):
                self.asyncCallbackAfter(0.5)._flowStart()
                return

        if self.dungeonStage:
            LOG_WARN('_flowStart:: NOW FROM STAGE, {}'.format(self.dungeonStage))
            r = self.resetFlowControllerStartByStage(self.dungeonStage)
            if not r:
                gameengine.panicStack('_flowStart:: STAGE NOT FOUND', self.dungeonStage)
                return

        self.flowController.trigger_now()

    def changeDungeonStageSet(self, newStageID):
        LOG_INFO('changeDungeonStageSet::', newStageID)
        oldStageID = self.dungeonStage
        self._changeDungeonStageSet(oldStageID, newStageID, toClient=True)

    def getBossEntity(self):
        return self.getEntitiyByTag(gameconst.HomeEntType.fetchTypeDesc(gameconst.HomeEntType.Boss))

    def _changeDungeonStageSet(self, oldStageID, newStageID, toClient=False, now=None):
        LOG_INFO('in _changeDungeonStageSet:', oldStageID, newStageID, self.dungeonPlayMode.__dict__)
        self.dungeonStage = newStageID
        self.dungeonStageStartT = now or utils.curTS()

    def onDungeonStarted(self, tCreate):
        LOG_INFO('onDungeonStarted::', tCreate, self.dungeonPlayMode.playMode)
        self.dungeonPlayMode.tCreate = tCreate
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        endTime = int(tCreate + DDI.datas[dungeonNo]['timeOut'] * 60 + 1)
        self.asyncCallbackAfter(1)._checkDungeonTimeout()
        for _pid in self.players:
            _ent = KBEngine.entities.get(_pid)
            if _ent and _ent.isReal() and formula.inDungeonScene(_ent.spaceNo):
                if formula.parseDungeonNoBySpaceNo(self.spaceNo) == formula.parseDungeonNoBySpaceNo(_ent.spaceNo):
                    _ent.client.changeDungeonRemainTime(self.spaceNo, endTime)

    def onDungeonStartChallenge(self, endTime):
        LOG_INFO('onDungeonStartChallenge::', endTime, self.dungeonPlayMode)
        self.dungeonPlayMode.challengeEndTime = endTime
        for pid in self.players:
            ent = KBEngine.entities.get(pid)
            if ent and ent.isReal() and formula.inDungeonScene(ent.spaceNo):
                if formula.parseDungeonNoBySpaceNo(self.spaceNo) == formula.parseDungeonNoBySpaceNo(ent.spaceNo):
                    ent.client.changeDungeonChallengeRemainTime(self.spaceNo, endTime, -1)

    def onPlayerRelogin(self, box, playerGbId):
        super(DungeonSpaceMgr, self).onPlayerRelogin(box, playerGbId)
        if not self.transPetId:
            return

        box.client.newTransPetStart(self.transPetId, self.triggerGuideId)

    def onPlayerOffline(self, playerId, gbId):
        super(DungeonSpaceMgr, self).onPlayerOffline(playerId, gbId)
        self.flowCtrlDungeonAlivePlayerDecreased(self.getAlivePlayerNumber())

    def onPlayerEnter(self, playerId):
        LOG_INFO('onPlayerEnter', playerId)
        super(DungeonSpaceMgr, self).onPlayerEnter(playerId)
        self.flowCtrlDungeonAlivePlayerIncreased(self.getAlivePlayerNumber())
        self.flowCtrlDungeonPlayerRestNumChanged(len(self.players))
        pent = KBEngine.entities.get(playerId)
        if pent:
            pent.sendDunTimeFreezeFlag()

    def onPlayerLeave(self, gbId, playerId, box):
        LOG_INFO('onPlayerLeave', gbId, playerId, box)
        super(DungeonSpaceMgr, self).onPlayerLeave(gbId, playerId, box)
        self.flowCtrlDungeonAlivePlayerDecreased(self.getAlivePlayerNumber())
        self.flowCtrlDungeonPlayerRestNumChanged(len(self.players))

    def addEntity(self, entId, tags):
        super(DungeonSpaceMgr, self).addEntity(entId, tags)
        _ent = KBEngine.entities.get(entId)

        if hasattr(_ent, 'gameEntityIdentifyID'):
            if _ent.gameEntityIdentifyID <= 0:
                LOG_WARN("DungeonSpaceMgr::addEntity:: gameEntityIdentifyID zero", 
                         _ent, tags, _ent.gameEntityIdentifyID)
                return
            gameengine.getDungeonStubBySpaceNo(self.spaceNo).onEntityCreated(
                self.spaceNo, self.spaceUUID, entId, _ent.gameEntityIdentifyID)

        if 'RebornPos' in tags:
            gameengine.getDungeonStubBySpaceNo(self.spaceNo).onCreateNewRebornPos(self.spaceNo, _ent.position)

    def onPlayerRelive(self, box, gbId):
        super(DungeonSpaceMgr, self).onPlayerRelive(box, gbId)
        self.flowCtrlDungeonAlivePlayerIncreased(self.getAlivePlayerNumber())

    def onPlayerDead(self, box, gbId):
        super(DungeonSpaceMgr, self).onPlayerDead(box, gbId)
        self.flowCtrlDungeonAlivePlayerDecreased(self.getAlivePlayerNumber())

    def getAlivePlayerNumber(self):
        return len(list(filter(lambda pVal: not pVal.isPlayerDead(), self.players.values())))

    def onDungeonTimeout(self):
        LOG_INFO('onDungeonTimeout::')
        # 【【任务】副本结束逻辑调整】
        # 1.表里配置的副本最长时间结束后，不需要再延迟了，直接销毁副本。
        delay = 0
        stub = gameengine.getDungeonStubBySpaceNo(self.spaceNo)
        if formula.inSingleDungeonScene(self.spaceNo):
            stub.completeSingleDungeon(self.spaceNo, self.singleDungeonBelongPlayerGBID, False, delay)
        elif formula.inTeamDungeonScene(self.spaceNo):
            stub.completeTeamDungeon(self.spaceNo, self.teamDungeonBelongTeamUUID, False, delay, gameconst.DunegonCompleteReasonType.TIMEOUT)
        elif formula.inRaidDungeonScene(self.spaceNo):
            stub.completeRaidDungeon(self.spaceNo, self.raidDungeonBelongRaidUUID, False, delay, gameconst.DunegonCompleteReasonType.TIMEOUT)
        elif formula.inGuildBossDungeonScene(self.spaceNo):
            stub.completeGuildBossDungeon(self.spaceNo, self.guildBossDungeonBelongGuildUUID, False, delay, gameconst.DunegonCompleteReasonType.TIMEOUT)

    def onSingleDungeonCompleted(self, spaceNo, playerGbId, win, delay, elapsedTime):
        LOG_INFO('onSingleDungeonCompleted::', spaceNo, playerGbId, win, delay, elapsedTime, self.dungeonPlayMode)
        if self.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.INNER_DEMON:
            LOG_DBG('onSingleDungeonCompleted:: inner demon play mode')
            self._doDungeonPreSettlement(playerGbId, spaceNo, win, delay, elapsedTime, gameconst.DungeonPlayModeEnum.INNER_DEMON, gameconst.DunegonCompleteReasonType.DEFAULT)
            return

        self._onDungeonCompleted(spaceNo, win, delay, elapsedTime, playerGbId)

    def onTeamDungeonCompleted(self, spaceNo, teamUUID, win, delay, elapsedTime, playerGbId, completedReasonType):
        LOG_INFO('onTeamDungeonCompleted::', spaceNo, teamUUID, win, delay, elapsedTime, playerGbId, completedReasonType)

        self._doDungeonPreSettlement(teamUUID, spaceNo, win, delay, elapsedTime, gameconst.DungeonPlayModeEnum.CRUSADE, completedReasonType)

    def finishGuildDungeonTask(self):
        self.syncPlayer(lambda box: box.doFinishGuildDungeonTask())

    def onRaidDungeonCompleted(self, spaceNo, raidUUID, win, delay, creepBaseKillDic, playerGbidAndNameList, elapsedTime, playerGbId, completedReasonType):
        LOG_INFO('onRaidDungeonCompleted::', spaceNo, raidUUID, win, delay, creepBaseKillDic, len(playerGbidAndNameList), elapsedTime, playerGbId, completedReasonType)

        self._doDungeonPreSettlement(raidUUID, spaceNo, win, delay, elapsedTime, gameconst.DungeonPlayModeEnum.CHIEF, completedReasonType)

    def onGuildBossDungeonCompleted(self, spaceNo, guildUUID, win, delay, elapsedTime, completedReasonType):
        LOG_INFO('onGuildBossDungeonCompleted::', spaceNo, guildUUID, win, delay, elapsedTime, completedReasonType)
        # 标记结算阶段
        self.guildBox.onGuildChallengeDungeonSettlement(utils.curTS())

        self._doDungeonPreSettlement(guildUUID, spaceNo, win, delay, elapsedTime, gameconst.DungeonPlayModeEnum.GUILD_BOSS, completedReasonType)
    # 副本预结算
    def _doDungeonPreSettlement(self, uniqueID, spaceNo, win, delay, elapsedTime, playMode, completedReasonType):
        opUUID = uniqueID
        LOG_INFO('_doDungeonPreSettlement:: start settlement 1', opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playMode, completedReasonType)
        if playMode not in gameconst.DungeonPlayModeEnum.COLL_ALL:
            LOG_INFO('_doDungeonPreSettlement::unknow play mode ', opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playMode)
            return
        
        _now = utils.curTS()
        _endT = int(_now + delay)
        players = {}
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        # 置副本输赢状态
        self.isDungeonWin = win
        # 筛选有效的玩家
        for pid in list(self.players):
            pEnt = KBEngine.entities.get(pid)
            if pEnt and pEnt.isReal():
                players[pEnt.gbId] = pEnt
            else:
                self.players.pop(pid, None)
        if len(players) == 0:
            LOG_WARN('_doDungeonPreSettlement::no player is left in dungeon ', opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playMode)
            return
        
        # 记录异步操作需要的缓存数据
        self.dungeonSettlementDataCache['opUUID'] = opUUID
        self.dungeonSettlementDataCache['completedReasonType'] = completedReasonType
        self.dungeonSettlementDataCache['uniqueID'] = uniqueID
        self.dungeonSettlementDataCache['players'] = players
        self.dungeonSettlementDataCache['batchCount'] = 0
        self.dungeonSettlementDataCache['spaceNo'] = spaceNo
        self.dungeonSettlementDataCache['elapsedTime'] = elapsedTime
        self.dungeonSettlementDataCache['endTime'] = _endT
        self.dungeonSettlementDataCache['win'] = win
        self.dungeonSettlementDataCache['delay'] = delay
        self.dungeonSettlementDataCache['dungeonNo'] = dungeonNo
        self.dungeonSettlementDataCache['playMode'] = playMode
        # 记录需要获取的排名数据类型
        if playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            self.dungeonSettlementDataCache['statisticTypes'] = [gameconst.StatisticEnum.STA_TYPE_DAMAGE]
        elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE or playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            self.dungeonSettlementDataCache['statisticTypes'] = [
                gameconst.StatisticEnum.STA_TYPE_DAMAGE,
                gameconst.StatisticEnum.STA_TYPE_HEAL,
                gameconst.StatisticEnum.STA_TYPE_HURT,
                gameconst.StatisticEnum.STA_TYPE_DEAD,
            ]
        elif playMode == gameconst.DungeonPlayModeEnum.INNER_DEMON:
            self.dungeonSettlementDataCache['statisticTypes'] = []
            if "innerDemonTime" not in self.dungeonSettlementDataCache:
                innerDemonTime = max(self.dungeonPlayMode.challengeEndTime - _now, 0)
                self.dungeonSettlementDataCache['innerDemonTime'] = innerDemonTime

        # 计算发送批次
        batchSize = 20
        validEntities = list(players.values())
        allCount = len(validEntities)
        if allCount > batchSize:
            batchCount = allCount // batchSize
            if allCount > batchCount * batchSize:
                batchCount += 1
            totalBatchCount = batchCount
        else:
            batchSize = allCount
            totalBatchCount = 1
        LOG_INFO('_doDungeonPreSettlement:: start settlement 2', opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playMode, totalBatchCount, batchSize, allCount, players.keys(), self.dungeonSettlementDataCache)
        # 发送玩家副本结束消息
        def _notifyDungeonCompleted(allCount, batchSize):
            for idx in range(0, allCount, batchSize):
                entities = validEntities[idx:idx+batchSize]
                for entity in entities:
                    entity.client and entity.client.onDungeonCompleted(dungeonNo, win, elapsedTime, _endT)
                LOG_INFO('_doDungeonPreSettlement:: do settlement', opUUID, uniqueID, spaceNo, allCount, totalBatchCount, batchSize, idx, len(entities))
                yield lambda *args:None
            # 通知完成之后开始请求排名数据    
            self._doDungeonStartSettlement(opUUID, uniqueID, spaceNo, win, delay, elapsedTime, 0, playMode)
        # 间隔0.1秒处理一次
        self.batchlyCall(_notifyDungeonCompleted(allCount, batchSize), 1, 0.1)
                                  
    def _doDungeonStartSettlement(self, opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playerGbId, playMode):
        LOG_INFO("_doDungeonStartSettlement::", opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playerGbId, playMode)
        # 通知统计数据stub获取数据
        self.addTimerCB(0.1, '_getDungeonRankData', (opUUID, uniqueID, spaceNo), gametimer.TIMER_TAG_DUNGEON_SETTLEMENT_TIMER)

    def _getDungeonRankData(self, opUUID, uniqueID, spaceNo):
        LOG_INFO("_getDungeonRankData::", opUUID, uniqueID, spaceNo)
        if len(self.dungeonSettlementDataCache.get('statisticTypes', [])) == 0:
            self._doDungeonEndSettlement(opUUID, uniqueID, spaceNo)
            return
        
        statisticDataType = self.dungeonSettlementDataCache['statisticTypes'].pop(0) 
        stub = gameengine.getStatisticStub(self.spaceNo)
        stub.getDungeonStatisticData(spaceNo, opUUID, self, statisticDataType)

    def _doDungeonEndSettlement(self, opUUID, uniqueID, spaceNo):
        LOG_INFO("_doDungeonEndSettlement::", opUUID, uniqueID, spaceNo, len(self.dungeonSettlementDataCache))
        uniqueID = self.dungeonSettlementDataCache['uniqueID']
        players = self.dungeonSettlementDataCache['players']
        spaceNo = self.dungeonSettlementDataCache['spaceNo']
        elapsedTime = self.dungeonSettlementDataCache['elapsedTime']
        endTime = self.dungeonSettlementDataCache['endTime']
        win = self.dungeonSettlementDataCache['win']
        opUUID = self.dungeonSettlementDataCache['opUUID']
        dungeonNo = self.dungeonSettlementDataCache['dungeonNo']
        playMode = self.dungeonSettlementDataCache['playMode']
        # 获取所有的统计数据类型
        statisticTypes = list(self.dungeonStatisticRecords.keys())
        for statisticType in statisticTypes:
            statisticDatas = self.dungeonStatisticRecords[statisticType]
            # 获取参与玩家的统计数据
            statisticDataRecords = []
            for gbId in players.keys():
                statisticDataRecord = statisticDatas.get(gbId, None)
                if not statisticDataRecord:
                    continue
                # 排除没有贡献的
                if statisticDataRecord['statisticsNum'] <= 0:
                    continue
                statisticDataRecords.append(statisticDataRecord)
            # 按照统计数据排序
            sortedStatisticDataRecords = sorted(statisticDataRecords, key=lambda v: v['statisticsNum'], reverse=True)
            # 重新给排名
            newStatisticDatas = {}
            rank = 0
            for sortedStatisticDataRecord in sortedStatisticDataRecords:
                rank += 1
                sortedStatisticDataRecord['rank'] = rank
                newStatisticDatas[sortedStatisticDataRecord['gbId']] = sortedStatisticDataRecord
            # 刷新统计数据
            self.dungeonStatisticRecords[statisticType] = newStatisticDatas
            rankCountList = self.dungeonSettlementDataCache.get('rankCountList')
            rankCountList[statisticType] = len(newStatisticDatas)
            LOG_INFO("_doDungeonEndSettlement:: 1", opUUID, uniqueID, statisticType, rankCountList[statisticType])
        # 公会副本需要支持拉取伤害排名
        if playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            records = list(self.dungeonStatisticRecords.get(gameconst.StatisticEnum.STA_TYPE_DAMAGE, {}).values())
            self.dungeonStatisticSortedRecords[gameconst.StatisticEnum.STA_TYPE_DAMAGE] = sorted(records, key=lambda v: v['rank'])
        
        # 根据排名计算奖励
        self.addTimerCB(0.1, '_doDungeonCalcReward', (opUUID, uniqueID, players, dungeonNo, spaceNo, elapsedTime, endTime, win, True), gametimer.TIMER_TAG_DUNGEON_SETTLEMENT_TIMER)

    def _doDungeonCalcReward(self, opUUID, uniqueID, players, dungeonNo, spaceNo, elapsedTime, endTime, win, needDungeonData):
        LOG_INFO("_doDungeonCalcReward::", opUUID, uniqueID, players, dungeonNo, spaceNo, elapsedTime, endTime, win, needDungeonData)
        # 开始计算有多少人能获得奖励
        players = self.dungeonSettlementDataCache['players']
        playMode = self.dungeonSettlementDataCache['playMode']
        if playMode == gameconst.DungeonPlayModeEnum.CRUSADE or playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            self._calcStatisticPoints(playMode)
        batchSize = 20
        validEntities = list(players.values())
        allCount = len(validEntities)
        if allCount > batchSize:
            batchCount = allCount // batchSize
            if allCount > batchCount * batchSize:
                batchCount += 1
            totalBatchCount = batchCount
        else:
            batchSize = allCount
            totalBatchCount = 1
        # 计算玩家副本结束奖励
        def _calcReward(allCount, batchSize):
            for idx in range(0, allCount, batchSize):
                entities = validEntities[idx:idx+batchSize]
                for entity in entities:
                    if not entity:
                        continue

                    dungeonExtraDatas = self.dungeonExtraDatas.get(entity.gbId, None)
                    if not dungeonExtraDatas:
                        LOG_WARN("_calcReward::  player extra data is missing", opUUID, uniqueID, entity.gbId, self.spaceNo)
                        continue
                    
                    if playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
                        settlement = DungeonSettlement.DungeonSettlementData()
                        settlement._calcGuildBossSettlement(self.base, self.dungeonRewardDatas, opUUID, uniqueID, entity, spaceNo, dungeonNo, dungeonExtraDatas, win, self.dungeonStatisticRecords)
                    elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE or playMode == gameconst.DungeonPlayModeEnum.CHIEF:
                        score, deadCount = self._calcPlayerStatisticScore(playMode, dungeonExtraDatas.gbId)
                        extra = {}
                        extra['elaspedTime'] = self.dungeonSettlementDataCache['elapsedTime']
                        extra['uniqueID'] = self.dungeonSettlementDataCache['uniqueID']
                        extra['playerCount'] = len(self.dungeonSettlementDataCache['players'])
                        extra['autoCombatTimes'] = self.dungeonAutoBattleTimes.get(entity.gbId, 0)
                        extra['deadCount'] = deadCount
                        extra['spaceUUID'] = self.dungeonPlayMode.spaceUUID
                        extra['completedReasonType'] = self.dungeonSettlementDataCache['completedReasonType']
                        
                        if playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
                            settlement = DungeonSettlement.DungeonSettlementData()
                            settlement._calcCrusadeSettlement(self.base, self.dungeonRewardDatas, opUUID, uniqueID, entity, spaceNo, dungeonNo, dungeonExtraDatas, win, score, extra)
                        elif playMode == gameconst.DungeonPlayModeEnum.CHIEF:
                            settlement = DungeonSettlement.DungeonSettlementData()
                            settlement._calcChiefSettlement(self.base, self.dungeonRewardDatas, opUUID, uniqueID, entity, spaceNo, dungeonNo, dungeonExtraDatas, win, score, extra)
                    elif playMode == gameconst.DungeonPlayModeEnum.INNER_DEMON:
                        score = self.dungeonSettlementDataCache['innerDemonTime']
                        settlement = DungeonSettlement.DungeonSettlementData()
                        settlement._calcInnerDemonSettlement(self.base, self.dungeonRewardDatas, opUUID, uniqueID, entity, spaceNo, dungeonNo, dungeonExtraDatas, win, score)
                LOG_INFO('_calcReward', opUUID, uniqueID, allCount, totalBatchCount, batchSize, self.spaceNo)
                yield lambda *args:None
            # 通知完成之后开始请求排名数据    
            self._doCheckSettlementData(opUUID, uniqueID)
        # 间隔0.1秒处理一次
        self.batchlyCall(_calcReward(allCount, batchSize), 1, 0.1)

    def _doCheckSettlementData(self, opUUID, uniqueID):
        LOG_INFO("_doCheckSettlementData::", opUUID, uniqueID)
        def _check():
            while True:
                hasWait = False
                for key, data in self.dungeonRewardDatas.items():
                    if data['wait']:
                        hasWait = True
                        break
                if not hasWait:
                    break
                else:
                    yield lambda *args:None
            self._doDungeonRewards(opUUID, uniqueID)
        # 间隔0.1秒处理一次
        self.batchlyCall(_check(), 1, 0.1)

    def _doDungeonRewards(self, opUUID, uniqueID):
        LOG_INFO("_doDungeonRewards::", opUUID, uniqueID)
        uniqueID = self.dungeonSettlementDataCache['uniqueID']
        players = self.dungeonSettlementDataCache['players']
        spaceNo = self.dungeonSettlementDataCache['spaceNo']
        elapsedTime = self.dungeonSettlementDataCache['elapsedTime']
        endTime = self.dungeonSettlementDataCache['endTime']
        win = self.dungeonSettlementDataCache['win']
        opUUID = self.dungeonSettlementDataCache['opUUID']
        dungeonNo = self.dungeonSettlementDataCache['dungeonNo']
        playMode = self.dungeonSettlementDataCache['playMode']

        cliDungeonData = {}
        cliDungeonData['win'] = win
        cliDungeonData['elapsedTime'] = elapsedTime
        cliDungeonData['endTime'] = endTime
        cliDungeonData['dungeonNo'] = dungeonNo
        cliDungeonData['playMode'] = playMode
        cliDungeonData['playMode'] = playMode
        cliDungeonData['rankCount'] = 0
        cliDungeonData['rewardCount'] = 0
        cliDungeonData['innerDemonTime'] = 0
        if playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            # 公会副本只需要展示自己的奖励
            cliDungeonData['rewardCount'] = 1
            # 通知客户端伤害排行榜数量
            rankCountList = self.dungeonSettlementDataCache.get('rankCountList')
            cliDungeonData['rankCount'] = rankCountList.get(gameconst.StatisticEnum.STA_TYPE_DAMAGE)
        elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE or playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            rankCountList = self.dungeonSettlementDataCache.get('rankCountList')
            rewardCount = 0
            for count in rankCountList.values():
                if count > rewardCount:
                    rewardCount = count
            cliDungeonData['rewardCount'] = rewardCount
        elif playMode == gameconst.DungeonPlayModeEnum.INNER_DEMON:
            cliDungeonData['rewardCount'] = 1
            cliDungeonData['innerDemonTime'] = self.dungeonSettlementDataCache['innerDemonTime']

        if playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS or playMode == gameconst.DungeonPlayModeEnum.INNER_DEMON:
            # 计算发送批次
            batchSize = 10
            gbIds = list(self.dungeonRewardDatas.keys())
            allCount = len(gbIds)
            if allCount > batchSize:
                batchCount = allCount // batchSize
                if allCount > batchCount * batchSize:
                    batchCount += 1
                totalBatchCount = batchCount
            else:
                batchSize = allCount
                totalBatchCount = 1
            LOG_INFO("_doDungeonRewards::", opUUID, uniqueID, allCount, totalBatchCount, batchSize)
            # 发送玩家副本结束消息
            def _notifyDungeonSettlement(allCount, batchSize):
                for idx in range(0, allCount, batchSize):
                    datas = gbIds[idx:idx+batchSize]
                    for gbId in datas:
                        settlementData = self.dungeonRewardDatas.get(gbId)
                        entity = settlementData['entity']
                        clientData = settlementData['client']
                        if playMode != gameconst.DungeonPlayModeEnum.INNER_DEMON or not win:
                            entity.client.onDungeonCompleteDungeonData(opUUID, cliDungeonData)
                        entity.client.changeDungeonRemainTime(spaceNo, endTime)
                        entity.client.onDungeonCompleteSettlementData(opUUID, [clientData])
                        LOG_INFO('_doDungeonRewards', cliDungeonData, clientData)
                    LOG_INFO('_doDungeonRewards', allCount, totalBatchCount, batchSize, self.spaceNo)
                    yield lambda *args:None
            # 间隔0.1秒处理一次
            self.batchlyCall(_notifyDungeonSettlement(allCount, batchSize), 1, 0.1)
        elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE or playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            gbIds = list(self.dungeonRewardDatas.keys())
            # 计算发送批次
            batchSize = 10
            allCount = len(gbIds)
            if allCount > batchSize:
                batchCount = allCount // batchSize
                if allCount > batchCount * batchSize:
                    batchCount += 1
                totalBatchCount = batchCount
            else:
                batchSize = allCount
                totalBatchCount = 1
            LOG_INFO("_doDungeonRewards::", opUUID, uniqueID, allCount, totalBatchCount, batchSize)
            def _doDungeonFinalReward():
                for gbId in gbIds:
                    playerData = self.dungeonRewardDatas.get(gbId)
                    entity = playerData['entity']
                    entity.client.onDungeonCompleteDungeonData(opUUID, cliDungeonData)
                    entity.client.changeDungeonRemainTime(spaceNo, endTime)
                    # 发送玩家副本结束消息
                    def _notifyDungeonSettlement(allCount, batchSize):
                        sendCount = 0
                        for idx in range(0, allCount, batchSize):
                            datas = gbIds[idx:idx+batchSize]
                            clientDatas = []
                            for gbId in datas:
                                settlementData = self.dungeonRewardDatas.get(gbId)
                                clientData = settlementData['client']
                                clientDatas.append(clientData)
                            entity.client.onDungeonCompleteSettlementData(opUUID, clientDatas)
                            LOG_INFO('_doDungeonRewards', allCount, totalBatchCount, batchSize, self.spaceNo)
                            sendCount += 1
                            # 这里如果大于batchSize
                            if sendCount > batchSize:
                                sendCount = 0
                                LOG_INFO('_doDungeonRewards 1', allCount, totalBatchCount, batchSize, self.spaceNo)
                                yield lambda *args:None
                    yield from _notifyDungeonSettlement(allCount, batchSize)
            # 间隔0.01秒处理一次
            self.batchlyCall(_doDungeonFinalReward(), 1, 0.1)

    def _onDungeonCompleted(self, spaceNo, win, delay, elapsedTime, playerGbId):
        LOG_INFO("_onDungeonCompleted::", spaceNo, win, delay, elapsedTime, playerGbId)
        self.isDungeonWin = win
        _now = utils.curTS()
        _endT = int(_now + delay)
        _allPlayersAreGoodMan = False
        pids = []
        for pid in list(self.players):
            pEnt = KBEngine.entities.get(pid)
            # 【退出副本有5s倒计时存在。】
            # 服务端可以先检测space过滤已经离开副本但还没有从spaceMgr上反注册的玩家
            if pEnt and pEnt.isReal():
                if playerGbId and pEnt.gbId != playerGbId:
                    continue
                if _allPlayersAreGoodMan:
                    # 【【任务】队伍无助力目标时返回MSG提示】
                    pEnt.showMsg(ACCD.datas["msgId_goodMan_noHelpTarget"]["value"], [])

                dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
                LOG_INFO("_onDungeonCompleted:: 0", dungeonNo, spaceNo, win, elapsedTime, _endT, playerGbId)
                pEnt.client.changeDungeonRemainTime(spaceNo, _endT)
                pids.append(pid)
            else:
                self.players.pop(pid, None)
                
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        # 延迟通知客户端副本结束
        completeDelayNotifyTime = self.getCompleteDelayNotifyTime()
        if delay > 0 and delay > completeDelayNotifyTime:
            LOG_INFO("_onDungeonCompleted:: 1", dungeonNo, spaceNo, win, elapsedTime, _endT, delay, completeDelayNotifyTime, playerGbId)
            self.addTimerCB(completeDelayNotifyTime, '_onDungenCompleteDelayNotifyCallback',
                (pids, dungeonNo, win, elapsedTime, _endT, playerGbId), gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
        else:
            LOG_INFO("_onDungeonCompleted:: 2", dungeonNo, spaceNo, win, elapsedTime, _endT, delay, completeDelayNotifyTime, playerGbId)
            self._onDungenCompleteDelayNotifyCallback(pids, dungeonNo, win, elapsedTime, _endT, playerGbId)
                
    def _onDungenCompleteDelayNotifyCallback(self, pids, dungeonNo, win, elapsedTime, _endT, playerGbId):
        self.clearCompleteDelayNotifyTimer()
        temp = {'dmgList':[], 'healList': [], 'hurtList': [], 'deadList': []}
        for pid in pids:
            pEnt = KBEngine.entities.get(pid)
            if pEnt and pEnt.isReal():
                if playerGbId and pEnt.gbId != playerGbId:
                    continue
                LOG_INFO("_onDungenCompleteDelayNotifyCallback:: ", pid, dungeonNo, win, elapsedTime, _endT, playerGbId)
                pEnt.client and pEnt.client.onDungeonCompleted(dungeonNo, win, elapsedTime, _endT)

    def onUpdateChallengeInfo(self, hpPercent):
        _isChallengeDun = bool(self.dungeonPlayMode and self.dungeonPlayMode.playMode == gameconst.DungeonPlayModeEnum.CHALLENGE_DUNGEON)
        if not _isChallengeDun or self.dungeonPlayMode.easy:
            return

        now = utils.curTS()
        for pid in list(self.players):
            _pEnt = KBEngine.entities.get(pid)
            if _pEnt and _pEnt.isReal():
                costTime = now - _pEnt.getSpaceEnterT()
                _pEnt.base.updateChallengeSpeedRaceInfo(hpPercent, costTime, self.dungeonPlayMode.dunLevel)

    def doEnterSingleDungeon(self, playerBox, playerGBID, spaceUUID, spaceBox, extra):
        LOG_INFO("doEnterSingleDungeon::", playerBox, playerGBID, spaceUUID, spaceBox, extra)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if DDI.datas[dungeonNo]['enterBlockByCombat']:
            for pid in self.players:
                _pEnt = KBEngine.entities.get(pid)
                if not _pEnt:
                    continue
                if _pEnt.hasState(gameconst.StateEnum.Fighting):
                    LOG_WARN("doEnterSingleDungeon:: failed, player is in fighting state", self.spaceNo)
                    return
        data = DungeonSettlement.DungeonExtraData()
        data.loadDatas(extra)
        self.notifyDungeonExtarData(playerGBID, data)

    def doEnterTeamDungeon(self, playerBox, playerGBID, spaceUUID, spaceBox, extra):
        LOG_INFO("doEnterTeamDungeon::", playerBox, playerGBID, spaceUUID, spaceBox, extra)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if DDI.datas[dungeonNo]['enterBlockByCombat']:
            for pid in self.players:
                _pEnt = KBEngine.entities.get(pid)
                if not _pEnt:
                    continue
                if _pEnt.hasState(gameconst.StateEnum.Fighting):
                    LOG_WARN("doEnterTeamDungeon:: failed, player is in fighting state", self.spaceNo)
                    return
        # 记录组队副本结算需要的相关数据
        data = DungeonSettlement.DungeonExtraData()
        data.loadDatas(extra)
        self.notifyDungeonExtarData(playerGBID, data)

        playerBox.cell.doEnterTeamDungeon(self.spaceNo, spaceUUID, spaceBox, self.base, extra)

    def enterRaidDunDirectly(self, playerBox, playerGBID, spaceUUID, spaceBox, src, extraProps):
        LOG_INFO("enterRaidDunDirectly::", playerBox, playerGBID, spaceUUID, spaceBox, src, extraProps)
        m_dungeonNo, mErrno = self._enterRaidDunDirectly(playerBox, playerGBID, spaceUUID, spaceBox, src)
        if mErrno != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_WARN(f"enterRaidDunDirectly::failed, errno={mErrno}")
        playerBox.cell.doEnterRaidDungeonAfterCheck(m_dungeonNo, self.spaceNo, spaceUUID, spaceBox, self.base, src, extraProps)

    def _enterRaidDunDirectly(self, playerBox, playerGBID, spaceUUID, spaceBox, src):
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if DDI.datas[dungeonNo]['enterBlockByCombat']:
            for pid in self.players:
                _pEnt = KBEngine.entities.get(pid)
                if not _pEnt:
                    continue
                if _pEnt.hasState(gameconst.StateEnum.Fighting):
                    return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_ENTER_BLOCK_BY_COMBAT

        return dungeonNo, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    def onCollectionBeCollect(self, entityGID, collectionId):
        super().onCollectionBeCollect(entityGID, collectionId)
        self.flowCtrlDungeonCollectionBeCollected(entityGID, collectionId)

    @property
    def transPetId(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumtransPetId, 0)

    @transPetId.setter
    def transPetId(self, newVal):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumtransPetId, newVal)

    @property
    def triggerGuideId(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumtriggerGuideId, 0)

    @triggerGuideId.setter
    def triggerGuideId(self, newVal):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumtriggerGuideId, newVal)

    @property
    def breakStuckPos(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumbreakStuckPos, None)
    
    @breakStuckPos.setter
    def breakStuckPos(self, newVal):
        LOG_INFO('set breakStuckPos:', newVal)
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumbreakStuckPos, newVal)

    @property
    def breakStuckDir(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumbreakStuckDir, 0)
    
    @breakStuckDir.setter
    def breakStuckDir(self, newVal):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.DSMPEnumbreakStuckDir, newVal)

    def startTimeFreeze(self):
        self.dungeonTimeFreezeFlag = True
        # NOTE(): 客户端要求先推送其他Entity的Flag, 最后推送玩家client的协议
        #            不要改变两个循环的顺序
        for eid in self.spaceEntitiesDic:
            _ent = KBEngine.entities.get(eid)
            if _ent and _ent.id != self.id:
                _ent.startDunTimeFreeze()
        for pid in self.players:
            _pent = KBEngine.entities.get(pid)
            if _pent and _pent.isReal():
                _pent.startDunTimeFreeze()

    def stopTimeFreeze(self):
        # NOTE(): 客户端要求先推送其他Entity的Flag, 最后推送玩家client的协议
        #            不要改变两个循环的顺序
        self.dungeonTimeFreezeFlag = False
        for eid in self.spaceEntitiesDic:
            _ent = KBEngine.entities.get(eid)
            if _ent and _ent.id != self.id:
                _ent.stopDunTimeFreeze()
        for pid in self.players:
            _pent = KBEngine.entities.get(pid)
            if _pent and _pent.isReal():
                _pent.stopDunTimeFreeze()

    def doEnterGuildBossDungeon(self, playerBox, playerGBID, spaceUUID, spaceBox, extra):
        LOG_INFO("doEnterGuildBossDungeon::", playerBox, playerGBID, spaceUUID, spaceBox, extra)
        dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
        if DDI.datas[dungeonNo]['enterBlockByCombat']:
            for pid in self.players:
                _pEnt = KBEngine.entities.get(pid)
                if not _pEnt:
                    continue
                if _pEnt.hasState(gameconst.StateEnum.Fighting):
                    LOG_WARN("doEnterGuildBossDungeon:: failed, player is in fighting state", self.spaceNo)
                    return
        playerBox.cell.doEnterGuildBossDungeon(self.spaceNo, spaceUUID, spaceBox, self.base, extra)

    def onDungeonStatisticData(self, totalBatchCount, currentBatchID, spaceNo, uniqueID, statisticType, dungeonStatisticRecords):
        LOG_INFO("onDungeonStatisticData::",self.dungeonSettlementDataCache['opUUID'], uniqueID, totalBatchCount, currentBatchID, self.spaceNo, spaceNo, statisticType, dungeonStatisticRecords)
        if totalBatchCount == 0:
            rankCountList = self.dungeonSettlementDataCache.setdefault('rankCountList', {})
            rankCountList[statisticType] = 0
            self.addTimerCB(0.1, '_getDungeonRankData', (self.dungeonSettlementDataCache['opUUID'], uniqueID, spaceNo), gametimer.TIMER_TAG_DUNGEON_SETTLEMENT_TIMER)
            return
        
        dataRecords = self.dungeonStatisticRecords.setdefault(statisticType, {})
        for dungeonStatisticRecord in dungeonStatisticRecords:
            dataRecords[dungeonStatisticRecord['gbId']] = dungeonStatisticRecord
        
        self.dungeonStatisticBatchCount += 1
        if totalBatchCount == self.dungeonStatisticBatchCount:
            rankCountList = self.dungeonSettlementDataCache.setdefault('rankCountList', {})
            rankCountList[statisticType] = len(dataRecords)
            self.dungeonStatisticBatchCount = 0
            self.addTimerCB(0.1, '_getDungeonRankData', (self.dungeonSettlementDataCache['opUUID'], uniqueID, spaceNo), gametimer.TIMER_TAG_DUNGEON_SETTLEMENT_TIMER)
            return

    def setGuildBox(self, box, opUUID):
        LOG_INFO("setGuildBox::", opUUID, self.spaceNo)
        self.guildBox = box
        self.opUUID = opUUID
    
    def getGuildBox(self):
        return self.guildBox
    
    def dungeonCompleted(self):
        LOG_INFO("dungeonCompleted::", self.spaceNo)
        self.guildBox.onGuildChallengeDungeonCompleted()

    def notifyDungeonExtarData(self, gbId, datas):
        self.dungeonExtraDatas[gbId] = datas
        
    def onGetSettlementRankList(self, rankType, spaceNo, uniqueID, playerBox, gbID, idx, offset):
        LOG_INFO("onGetSettlementRankList:: 1", self.dungeonSettlementDataCache['opUUID'], uniqueID, rankType, spaceNo, playerBox, gbID, idx, offset)
        results = []
        rankDatas = self.dungeonStatisticSortedRecords.get(rankType)
        if not rankDatas:
            LOG_WARN("onGetSettlementRankList:: 2 no rank data, ", self.dungeonSettlementDataCache['opUUID'], uniqueID, rankType, spaceNo, playerBox, gbID, idx, offset)
            playerBox.client.onGetSettlementRankList(rankType, dungeonNo, idx, offset, results)
            return
        # 限制单次拉取的最大数量
        if offset > 10:
            offset = 10

        datas = rankDatas[idx:idx+offset]

        LOG_INFO("onGetSettlementRankList:: 3", self.dungeonSettlementDataCache['opUUID'], uniqueID, rankType, spaceNo, playerBox, gbID, idx, offset, len(datas), len(rankDatas))

        for data in datas:
            result = {
                'name':data['name'],
                'rank':data['rank'],
                'dmg':data['statisticsNum']
            }
            results.append(result)

        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        playerBox.client.onGetSettlementRankList(rankType, dungeonNo, idx, offset, results)
    
    def _calcPointsRanking(self, playMode, statisticType):
        LOG_INFO('_calcPointsRanking: 1', playMode, statisticType)
        results = {}
        statisticRecords = self.dungeonStatisticRecords.setdefault(statisticType, {})
        if len(statisticRecords) == 0:
            LOG_INFO('_calcPointsRanking: 2', playMode, statisticType)
            return results
        
        playerDiedScore = int(TM_PR.datas['playerDiedScore']['value'])
        if statisticType == gameconst.StatisticEnum.STA_TYPE_DEAD:
            for data in statisticRecords.values():
                results[data['gbId']] = data['statisticsNum'] * playerDiedScore
            return results
        datas = statisticRecords.values()
        datas = sorted(datas, key=lambda v: v['rank'])

        lastMinScore = None
        rankCfgData = None
        rankDiffRatio = float(TM_PR.datas['upLevelValuePercent']['value'])
        for data in datas:
            curRank = data['rank']
            LOG_DBG('_calcPointsRanking: 3', curRank, data, playMode, statisticType)
            # 首次找
            if rankCfgData is None:
                LOG_DBG('_calcPointsRanking: 4', curRank, playMode, statisticType)
                rankCfgData = self._doGetValidPointRankCfg(curRank, playMode, statisticType)
                if not rankCfgData:
                    return results
            LOG_DBG('_calcPointsRanking: 5', curRank, rankCfgData, data, playMode, statisticType)
            # 不在范围，重新找
            if not (curRank >= rankCfgData[0] and curRank <= rankCfgData[1]):
                LOG_DBG('_calcPointsRanking: 6', curRank, rankCfgData, data, playMode, statisticType)
                rankCfgData = self._doGetValidPointRankCfg(curRank, playMode, statisticType)
                if not rankCfgData:
                    return results
            LOG_DBG('_calcPointsRanking: 7', curRank, rankCfgData, data, playMode, statisticType)
            # 首个区间计算
            if lastMinScore is None:
                LOG_DBG('_calcPointsRanking: 8', curRank, rankCfgData, data, playMode, statisticType)
                results[data['gbId']] = rankCfgData[2]
            else:
                if data['statisticsNum'] > 0:
                    if data['statisticsNum'] >= rankDiffRatio * lastMinScore:
                        LOG_DBG('_calcPointsRanking: 9', curRank, rankCfgData, data, playMode, statisticType)
                        results[data['gbId']] = rankCfgData[2]
                    else:
                        LOG_DBG('_calcPointsRanking: 10', curRank, rankCfgData, data, playMode, statisticType)
                        results[data['gbId']] = rankCfgData[3]
                else:
                    LOG_DBG('_calcPointsRanking: 11', curRank, rankCfgData, data, playMode, statisticType)
                    results[data['gbId']] = 0
                
            # 当前范围的最后一名，更新一下上个区间的最小值                
            if curRank == rankCfgData[1]:
                LOG_DBG('_calcPointsRanking: 12', curRank, rankCfgData, data, playMode, statisticType)
                lastMinScore = data['statisticsNum']

        return results
    
    def _calcDeadCount(self, gbId, playMode, statisticType):
        LOG_INFO('_calcDeadCount: 1', gbId, playMode, statisticType)
        statisticRecords = self.dungeonStatisticRecords.setdefault(statisticType, {})
        if len(statisticRecords) == 0:
            LOG_INFO('_calcDeadCount: 2', gbId, playMode, statisticType)
            return 0
        
        for data in statisticRecords.values():
            if data['gbId'] == gbId:
                LOG_DBG('_calcDeadCount: 3', gbId, playMode, statisticType, data['statisticsNum'])
                return data['statisticsNum']
        return 0
        
    def _doGetValidPointRankCfg(self, rank, playMode, statisticType):
        rankCfgDatas = self.getStatisticRankCfg(playMode, statisticType)
        if not rankCfgDatas:
            LOG_ERR("_doGetValidPointRankCfg:: no rank cfg data, ", rank, playMode, statisticType)
            return None
        
        for rankCfgData in rankCfgDatas:
            if len(rankCfgData) != 4:
                LOG_ERR("_doGetValidPointRankCfg:: wrong rank cfg data, ", rank, playMode, statisticType, rankCfgDatas, rankCfgData)
                return None
            if rank >= rankCfgData[0] and rank <= rankCfgData[1]:
                return rankCfgData
        LOG_WARN("_doGetValidPointRankCfg:: no rank cfg data, ", rank, playMode, statisticType, rankCfgDatas)
        return None
        
    def getStatisticRankCfg(self, playMode, statisticType):
        if statisticType == gameconst.StatisticEnum.STA_TYPE_DAMAGE:
            if playMode == gameconst.DungeonPlayModeEnum.CHIEF:
                return self._doGetStatisticRankCfg('dmg_level2Score15')
            elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
                return self._doGetStatisticRankCfg('dmg_level2Score5')
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HEAL:
            if playMode == gameconst.DungeonPlayModeEnum.CHIEF:
                return self._doGetStatisticRankCfg('addHp_level2Score_15')
            elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
                return self._doGetStatisticRankCfg('addHp_level2Score_5')
        elif statisticType == gameconst.StatisticEnum.STA_TYPE_HURT:
            if playMode == gameconst.DungeonPlayModeEnum.CHIEF:
                return self._doGetStatisticRankCfg('hurt_level2Score_15')
            elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
                return self._doGetStatisticRankCfg('hurt_level2Score_5')
        return None
    
    def _doGetStatisticRankCfg(self, dataKey):
        datas = TM_PR.datas.get(dataKey, None)
        if datas:
            return datas['value']
        return None
        
    def _calcStatisticPoints(self, playMode):
        self.dungeonSettlementDataCache['dmgPoints'] = self._calcPointsRanking(playMode, gameconst.StatisticEnum.STA_TYPE_DAMAGE)
        self.dungeonSettlementDataCache['healPoints'] = self._calcPointsRanking(playMode, gameconst.StatisticEnum.STA_TYPE_HEAL)
        self.dungeonSettlementDataCache['hurtPoints'] = self._calcPointsRanking(playMode, gameconst.StatisticEnum.STA_TYPE_HURT)
        self.dungeonSettlementDataCache['deadPoints'] = self._calcPointsRanking(playMode, gameconst.StatisticEnum.STA_TYPE_DEAD)
    
    def _calcPlayerStatisticScore(self, playMode, gbId):
        score = self.dungeonSettlementDataCache['dmgPoints'].get(gbId, 0) \
                + self.dungeonSettlementDataCache['healPoints'].get(gbId, 0) \
                + self.dungeonSettlementDataCache['hurtPoints'].get(gbId, 0) \
                + self.dungeonSettlementDataCache['deadPoints'].get(gbId, 0)
        deadCount = self._calcDeadCount(gbId, playMode, gameconst.StatisticEnum.STA_TYPE_DEAD)
        return score, deadCount
    
    def onNotifySettlementResult(self, box, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards, goldPassRewards, dungeonRewards):
        LOG_INFO("onNotifySettlementResult::", opUUId, uniqueId, playMode, spaceNo, dungeonNo, win, extra, firstPassRewards, goldPassRewards, dungeonRewards)
        dungeonRewardData = self.dungeonRewardDatas.get(extra['gbId'])
        if not dungeonRewardData:
            return

        data = DungeonSettlement.DungeonSettlementData()
        data.gbId = extra['gbId']
        data.name = extra['name']
        data.rank = extra['rank']
        data.score = extra['score']
        data.level = extra['level']
        data.school = extra['school']
        data.sex = extra['sex']
        data.dungeonRewards = dungeonRewards
        data.firstPassRewards = firstPassRewards
        data.goldPassRewards = goldPassRewards

        dungeonRewardData['wait'] = False
        dungeonRewardData['client'] = data.toClientData()
        dungeonRewardData['entity'] = box

    def doDungeonMonsterBorn(self, monsterGID, createTime):
        LOG_INFO("doDungeonMonsterBorn::", monsterGID, createTime, self.dungeonPlayMode.spaceUUID, self.spaceNo, self.dungeonPlayMode.playMode)
        if not monsterGID:
            return
        uniqueID = 0
        if formula.inTeamDungeonScene(self.spaceNo):
            uniqueID = self.dungeonPlayMode.teamUUID
        elif formula.inRaidDungeonScene(self.spaceNo):
            uniqueID = self.dungeonPlayMode.raidUUID
        else:
            return
        
        monsterData = CBD.datas.get(monsterGID)
        if monsterData and monsterData['nameSuffixID'] == gameconst.MonsterSuffix.BOSS:
            LogTrackingMgr.LogTrackingMgr.Dungeon_Boss_Born(
                'DungeonSpaceMgr',
                '',
                uniqueID,
                self.dungeonPlayMode.playMode,
                formula.parseDungeonNoBySpaceNo(self.spaceNo),
                self.dungeonPlayMode.spaceUUID,
                self.spaceNo,
                monsterGID,
                createTime,
                self.dungeonPlayMode.tCreate
            )

    def doDungeonMonsterDead(self, monsterGID, createTime):
        LOG_INFO("doDungeonMonsterDead::", monsterGID, createTime, self.dungeonPlayMode.spaceUUID, self.spaceNo, self.dungeonPlayMode.playMode)
        if not monsterGID:
            return
        uniqueID = 0
        if formula.inTeamDungeonScene(self.spaceNo):
            uniqueID = self.dungeonPlayMode.teamUUID
        elif formula.inRaidDungeonScene(self.spaceNo):
            uniqueID = self.dungeonPlayMode.raidUUID
        else:
            return
        
        monsterData = CBD.datas.get(monsterGID)
        if monsterData and monsterData['nameSuffixID'] == gameconst.MonsterSuffix.BOSS:
            LogTrackingMgr.LogTrackingMgr.Dungeon_Boss_Dead(
                'DungeonSpaceMgr',
                '',
                uniqueID,
                self.dungeonPlayMode.playMode,
                formula.parseDungeonNoBySpaceNo(self.spaceNo),
                self.dungeonPlayMode.spaceUUID,
                self.spaceNo,
                monsterGID,
                createTime,
                utils.curTS(),
                self.dungeonPlayMode.tCreate
            )

    def recordAutoFightTimes(self, gbId, state, times):
        LOG_INFO("recordAutoFightTimes::", gbId, state, times, self.dungeonPlayMode.spaceUUID, self.spaceNo, self.dungeonPlayMode.playMode)
        self.dungeonAutoBattleTimes[gbId] = self.dungeonAutoBattleTimes.get(gbId, 0) + times

    def notifyInnerDemonData(self, dungeonNo, spaceNo):
        if self.dungeonPlayMode.playMode != gameconst.DungeonPlayModeEnum.INNER_DEMON:
            LOG_ERR('notifyInnerDemonData: err')
            return
        
        opUUID = int(self.singleDungeonBelongPlayerGBID)
        _now = utils.curTS()
        innerDemonTime = max(self.dungeonPlayMode.challengeEndTime - _now, 0)
        elapsedTime = _now - self.dungeonPlayMode.tCreate
        self.dungeonSettlementDataCache['innerDemonTime'] = innerDemonTime

        cliDungeonData = {}
        cliDungeonData['win'] = 1
        cliDungeonData['elapsedTime'] = elapsedTime
        cliDungeonData['endTime'] = _now + 1800
        cliDungeonData['dungeonNo'] = dungeonNo
        cliDungeonData['playMode'] = self.dungeonPlayMode.playMode
        cliDungeonData['rankCount'] = 0
        cliDungeonData['rewardCount'] = 1
        cliDungeonData['innerDemonTime'] = innerDemonTime
        LOG_INFO("notifyInnerDemonData", opUUID, cliDungeonData)
        self.syncPlayer(lambda box: box.client.onDungeonCompleteDungeonData(opUUID, cliDungeonData))

    def sendDungeonProps(self, box):
        if self.dungeonPlayMode.playMode != gameconst.DungeonPlayModeEnum.INNER_DEMON:
            LOG_INFO("sendDungeonProps not inner demon mode")
            return
        
        score = self.dungeonSettlementDataCache.get('innerDemonTime', -1)
        LOG_INFO("sendDungeonProps", score)
        box.client.changeDungeonChallengeRemainTime(self.spaceNo, self.dungeonPlayMode.challengeEndTime, score)
