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

class DungeonCompleteDelayNotifyMixin(object):
    def __init__(self):
        if not hasattr(self, 'dungeonCompleteDelayNotifyTimer'):
            self.dungeonCompleteDelayNotifyTimer = 0
    
    def cancelCompleteDelayNotifyTimer(self, owner, tag):
        INFO_MSG('cancelCompleteDelayNotifyTimer~', owner, tag)
        if self.dungeonCompleteDelayNotifyTimer:
            owner._cancelCallback(self.dungeonCompleteDelayNotifyTimer, tag)
        self.clearCompleteDelayNotifyTimer()

    def clearCompleteDelayNotifyTimer(self):
        self.dungeonCompleteDelayNotifyTimer = 0

    def getCompleteDelayNotifyTime(self):
        return int(TMMCD.datas['copySettlementInterval']['value'])


class DungeonSpaceMgr(iCell.ICell, iTimer.ITimer, iSpaceMgr.ISpaceMgr, DungeonPlayerReliveRecordMixin, DungeonCompleteDelayNotifyMixin):
    def __init__(self):
        INFO_MSG("DungeonSpaceMgr#__init__", self.spaceNo, self.spaceID)

        iCell.ICell.__init__(self)
        iSpaceMgr.ISpaceMgr.__init__(self)
        # 副本不用定刷
        #self.addDatetimeTimerTick()

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
    def guildBossDungeonBelongGuildUUID(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.guildBossDungeonBelongGuildUUID, 0)
    
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
        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
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
        INFO_MSG('resetStartNodeByStage::', dungeonStageID)
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
        # 帮会副本直接开始流程
        if formula.isGuildBossDungeonSpace(self.spaceNo):
            self.flowController.trigger_now()
            return
        
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
        INFO_MSG('changeDungeonStageSet::', newStageID)
        oldStageID = self.dungeonStage
        self._changeDungeonStageSet(oldStageID, newStageID, toClient=True)

    def _changeDungeonStageSet(self, oldStageID, newStageID, toClient=False, now=None):
        INFO_MSG('in _changeDungeonStageSet:', oldStageID, newStageID, self.dungeonPlayMode.__dict__)
        self.dungeonStage = newStageID
        self.dungeonStageStartT = now or utils.getNow()

    def onDungeonStarted(self, tCreate):
        INFO_MSG('onDungeonStarted::', tCreate, self.dungeonPlayMode.playMode)
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
            stub.completeTeamDungeon(self.spaceNo, self.teamDungeonBelongTeamUUID, False, delay, gameconst.DunegonCompleteReasonType.TIMEOUT)
        elif formula.isRaidDungeonSpace(self.spaceNo):
            stub.completeRaidDungeon(self.spaceNo, self.raidDungeonBelongRaidUUID, False, delay, gameconst.DunegonCompleteReasonType.TIMEOUT)
        elif formula.isGuildBossDungeonSpace(self.spaceNo):
            stub.completeGuildBossDungeon(self.spaceNo, self.guildBossDungeonBelongGuildUUID, False, delay, gameconst.DunegonCompleteReasonType.TIMEOUT)

    def onSingleDungeonCompleted(self, spaceNo, playerGbId, win, delay, elapsedTime):
        INFO_MSG('onSingleDungeonCompleted::', spaceNo, playerGbId, win, delay, elapsedTime)
        self._onDungeonCompleted(spaceNo, win, delay, elapsedTime, playerGbId)

    def onTeamDungeonCompleted(self, spaceNo, teamUUID, win, delay, elapsedTime, playerGbId, completedReasonType):
        INFO_MSG('onTeamDungeonCompleted::', spaceNo, teamUUID, win, delay, elapsedTime, playerGbId, completedReasonType)

        self._doDungeonPreSettlement(teamUUID, spaceNo, win, delay, elapsedTime, gameconst.DungeonPlayModeEnum.CRUSADE, completedReasonType)

    def finishGuildDungeonTask(self):
        self.syncPlayer(lambda box: box.doFinishGuildDungeonTask())

    def onRaidDungeonCompleted(self, spaceNo, raidUUID, win, delay, creepBaseKillDic, playerGbidAndNameList, elapsedTime, playerGbId, completedReasonType):
        INFO_MSG('onRaidDungeonCompleted::', spaceNo, raidUUID, win, delay, creepBaseKillDic, len(playerGbidAndNameList), elapsedTime, playerGbId, completedReasonType)

        self._doDungeonPreSettlement(raidUUID, spaceNo, win, delay, elapsedTime, gameconst.DungeonPlayModeEnum.CHIEF, completedReasonType)

    def onGuildBossDungeonCompleted(self, spaceNo, guildUUID, win, delay, elapsedTime, completedReasonType):
        INFO_MSG('onGuildBossDungeonCompleted::', spaceNo, guildUUID, win, delay, elapsedTime, completedReasonType)
        # 标记结算阶段
        self.guildBox.onGuildChallengeDungeonSettlement(utils.getNow())

        self._doDungeonPreSettlement(guildUUID, spaceNo, win, delay, elapsedTime, gameconst.DungeonPlayModeEnum.GUILD_BOSS, completedReasonType)
    # 副本预结算
    def _doDungeonPreSettlement(self, uniqueID, spaceNo, win, delay, elapsedTime, playMode, completedReasonType):
        opUUID = uniqueID
        INFO_MSG('_doDungeonPreSettlement:: start settlement 1', opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playMode, completedReasonType)
        if playMode not in gameconst.DungeonPlayModeEnum.COLL_ALL:
            INFO_MSG('_doDungeonPreSettlement::unknow play mode ', opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playMode)
            return
        
        _now = utils.getNow()
        _endT = int(_now + delay)
        players = {}
        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
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
            WARNING_MSG('_doDungeonPreSettlement::no player is left in dungeon ', opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playMode)
            return
        
        # 记录异步操作需要的缓存数据
        self.dungeonSettlementDataCache = {}
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
            self.dungeonSettlementDataCache['statisticTypes'] = [gameconst.StatisticType.STA_TYPE_DAMAGE]
        elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE or playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            self.dungeonSettlementDataCache['statisticTypes'] = [
                gameconst.StatisticType.STA_TYPE_DAMAGE,
                gameconst.StatisticType.STA_TYPE_HEAL,
                gameconst.StatisticType.STA_TYPE_HURT,
                gameconst.StatisticType.STA_TYPE_DEAD,
            ]

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
        INFO_MSG('_doDungeonPreSettlement:: start settlement 2', opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playMode, totalBatchCount, batchSize, allCount, players.keys(), self.dungeonSettlementDataCache)
        # 发送玩家副本结束消息
        def _notifyDungeonCompleted(allCount, batchSize):
            for idx in range(0, allCount, batchSize):
                entities = validEntities[idx:idx+batchSize]
                for entity in entities:
                    entity.client and entity.client.onDungeonCompleted(dungeonNo, win, elapsedTime, _endT)
                INFO_MSG('_doDungeonPreSettlement:: do settlement', opUUID, uniqueID, spaceNo, allCount, totalBatchCount, batchSize, idx, len(entities))
                yield lambda *args:None
            # 通知完成之后开始请求排名数据    
            self._doDungeonStartSettlement(opUUID, uniqueID, spaceNo, win, delay, elapsedTime, 0, playMode)
        # 间隔0.1秒处理一次
        self.batchlyCall(_notifyDungeonCompleted(allCount, batchSize), 1, 0.1)
                                  
    def _doDungeonStartSettlement(self, opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playerGbId, playMode):
        INFO_MSG("_doDungeonStartSettlement::", opUUID, uniqueID, spaceNo, win, delay, elapsedTime, playerGbId, playMode)
        # 通知统计数据stub获取数据
        self._callback(0.1, '_getDungeonRankData', (opUUID, uniqueID, spaceNo), gametimer.TIMER_TAG_DUNGEON_SETTLEMENT_TIMER)

    def _getDungeonRankData(self, opUUID, uniqueID, spaceNo):
        INFO_MSG("_getDungeonRankData::", opUUID, uniqueID, spaceNo)
        if len(self.dungeonSettlementDataCache['statisticTypes']) == 0:
            self._doDungeonEndSettlement(opUUID, uniqueID, spaceNo)
            return
        
        statisticDataType = self.dungeonSettlementDataCache['statisticTypes'].pop(0) 
        stub = gameengine.getStatisticStub(self.spaceNo)
        stub.getDungeonStatisticData(spaceNo, opUUID, self, statisticDataType)

    def _doDungeonEndSettlement(self, opUUID, uniqueID, spaceNo):
        INFO_MSG("_doDungeonEndSettlement::", opUUID, uniqueID, spaceNo, len(self.dungeonSettlementDataCache))
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
            INFO_MSG("_doDungeonEndSettlement:: 1", opUUID, uniqueID, statisticType, rankCountList[statisticType])
        # 公会副本需要支持拉取伤害排名
        if playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            records = list(self.dungeonStatisticRecords.get(gameconst.StatisticType.STA_TYPE_DAMAGE, {}).values())
            self.dungeonStatisticSortedRecords[gameconst.StatisticType.STA_TYPE_DAMAGE] = sorted(records, key=lambda v: v['rank'])
        
        # 根据排名计算奖励
        self._callback(0.1, '_doDungeonCalcReward', (opUUID, uniqueID, players, dungeonNo, spaceNo, elapsedTime, endTime, win, True), gametimer.TIMER_TAG_DUNGEON_SETTLEMENT_TIMER)

    def _doDungeonCalcReward(self, opUUID, uniqueID, players, dungeonNo, spaceNo, elapsedTime, endTime, win, needDungeonData):
        INFO_MSG("_doDungeonCalcReward::", opUUID, uniqueID, players, dungeonNo, spaceNo, elapsedTime, endTime, win, needDungeonData)
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
                        WARNING_MSG("_calcReward::  player extra data is missing", opUUID, uniqueID, entity.gbId, self.spaceNo)
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
                INFO_MSG('_calcReward', opUUID, uniqueID, allCount, totalBatchCount, batchSize, self.spaceNo)
                yield lambda *args:None
            # 通知完成之后开始请求排名数据    
            self._doCheckSettlementData(opUUID, uniqueID)
        # 间隔0.1秒处理一次
        self.batchlyCall(_calcReward(allCount, batchSize), 1, 0.1)

    def _doCheckSettlementData(self, opUUID, uniqueID):
        INFO_MSG("_doCheckSettlementData::", opUUID, uniqueID)
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
        INFO_MSG("_doDungeonRewards::", opUUID, uniqueID)
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
        if playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
            # 公会副本只需要展示自己的奖励
            cliDungeonData['rewardCount'] = 1
            # 通知客户端伤害排行榜数量
            rankCountList = self.dungeonSettlementDataCache.get('rankCountList')
            cliDungeonData['rankCount'] = rankCountList.get(gameconst.StatisticType.STA_TYPE_DAMAGE)
        elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE or playMode == gameconst.DungeonPlayModeEnum.CHIEF:
            rankCountList = self.dungeonSettlementDataCache.get('rankCountList')
            rewardCount = 0
            for count in rankCountList.values():
                if count > rewardCount:
                    rewardCount = count
            cliDungeonData['rewardCount'] = rewardCount

        if playMode == gameconst.DungeonPlayModeEnum.GUILD_BOSS:
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
            INFO_MSG("_doDungeonRewards::", opUUID, uniqueID, allCount, totalBatchCount, batchSize)
            # 发送玩家副本结束消息
            def _notifyDungeonSettlement(allCount, batchSize):
                for idx in range(0, allCount, batchSize):
                    datas = gbIds[idx:idx+batchSize]
                    for gbId in datas:
                        settlementData = self.dungeonRewardDatas.get(gbId)
                        entity = settlementData['entity']
                        clientData = settlementData['client']
                        entity.client.onDungeonCompleteDungeonData(opUUID, cliDungeonData)
                        entity.client.changeDungeonRemainTime(spaceNo, endTime)
                        entity.client.onDungeonCompleteSettlementData(opUUID, [clientData])
                    INFO_MSG('_doDungeonRewards', allCount, totalBatchCount, batchSize, self.spaceNo)
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
            INFO_MSG("_doDungeonRewards::", opUUID, uniqueID, allCount, totalBatchCount, batchSize)
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
                            INFO_MSG('_doDungeonRewards', allCount, totalBatchCount, batchSize, self.spaceNo)
                            sendCount += 1
                            # 这里如果大于batchSize
                            if sendCount > batchSize:
                                sendCount = 0
                                INFO_MSG('_doDungeonRewards 1', allCount, totalBatchCount, batchSize, self.spaceNo)
                                yield lambda *args:None
                    yield from _notifyDungeonSettlement(allCount, batchSize)
            # 间隔0.01秒处理一次
            self.batchlyCall(_doDungeonFinalReward(), 1, 0.1)

    def _onDungeonCompleted(self, spaceNo, win, delay, elapsedTime, playerGbId):
        INFO_MSG("_onDungeonCompleted::", spaceNo, win, delay, elapsedTime, playerGbId)
        self.isDungeonWin = win
        _now = utils.getNow()
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

                dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
                INFO_MSG("_onDungeonCompleted:: 0", dungeonNo, spaceNo, win, elapsedTime, _endT, playerGbId)
                pEnt.client.changeDungeonRemainTime(spaceNo, _endT)
                pids.append(pid)
            else:
                self.players.pop(pid, None)
                
        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        # 延迟通知客户端副本结束
        completeDelayNotifyTime = self.getCompleteDelayNotifyTime()
        if delay > 0 and delay > completeDelayNotifyTime:
            INFO_MSG("_onDungeonCompleted:: 1", dungeonNo, spaceNo, win, elapsedTime, _endT, delay, completeDelayNotifyTime, playerGbId)
            self._callback(completeDelayNotifyTime, '_onDungenCompleteDelayNotifyCallback',
                (pids, dungeonNo, win, elapsedTime, _endT, playerGbId), gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
        else:
            INFO_MSG("_onDungeonCompleted:: 2", dungeonNo, spaceNo, win, elapsedTime, _endT, delay, completeDelayNotifyTime, playerGbId)
            self._onDungenCompleteDelayNotifyCallback(pids, dungeonNo, win, elapsedTime, _endT, playerGbId)
                
    def _onDungenCompleteDelayNotifyCallback(self, pids, dungeonNo, win, elapsedTime, _endT, playerGbId):
        self.clearCompleteDelayNotifyTimer()
        temp = {'dmgList':[], 'healList': [], 'hurtList': [], 'deadList': []}
        for pid in pids:
            pEnt = KBEngine.entities.get(pid)
            if pEnt and pEnt.isReal():
                if playerGbId and pEnt.gbId != playerGbId:
                    continue
                INFO_MSG("_onDungenCompleteDelayNotifyCallback:: ", pid, dungeonNo, win, elapsedTime, _endT, playerGbId)
                pEnt.client and pEnt.client.onDungeonCompleted(dungeonNo, win, elapsedTime, _endT)

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
        # 记录组队副本结算需要的相关数据
        data = DungeonSettlement.DungeonExtraData()
        data.loadDatas(extra)
        self.notifyDungeonExtarData(playerGBID, data)

        playerBox.cell.doEnterTeamDungeon(self.spaceNo, spaceUUID, spaceBox, self.base, extra)

    def enterRaidDungeonDirectly(self, playerBox, playerGBID, spaceUUID, spaceBox, src, extraProps):
        INFO_MSG("enterRaidDungeonDirectly::", playerBox, playerGBID, spaceUUID, spaceBox, src, extraProps)
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

    @property
    def breakStuckPos(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.breakStuckPos, None)
    
    @breakStuckPos.setter
    def breakStuckPos(self, newVal):
        INFO_MSG('set breakStuckPos:', newVal)
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.breakStuckPos, newVal)

    @property
    def breakStuckDir(self):
        return self.getTempMiscProp(gameconst.DungeonSpaceMgrProps.breakStuckDir, 0)
    
    @breakStuckDir.setter
    def breakStuckDir(self, newVal):
        self.setTempMiscProp(gameconst.DungeonSpaceMgrProps.breakStuckDir, newVal)

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

    def doEnterGuildBossDungeon(self, playerBox, playerGBID, spaceUUID, spaceBox, extra):
        INFO_MSG("doEnterGuildBossDungeon::", playerBox, playerGBID, spaceUUID, spaceBox, extra)
        dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
        if DDI.datas[dungeonNo]['enterBlockByCombat']:
            for pid in self.players:
                pEnt = KBEngine.entities.get(pid)
                if not pEnt:
                    continue
                if pEnt.hasState(gameconst.State.Fighting):
                    WARNING_MSG("doEnterGuildBossDungeon:: failed, player is in fighting state", self.spaceNo)
                    return
        playerBox.cell.doEnterGuildBossDungeon(self.spaceNo, spaceUUID, spaceBox, self.base, extra)

    def onDungeonStatisticData(self, totalBatchCount, currentBatchID, spaceNo, uniqueID, statisticType, dungeonStatisticRecords):
        INFO_MSG("onDungeonStatisticData::",self.dungeonSettlementDataCache['opUUID'], uniqueID, totalBatchCount, currentBatchID, self.spaceNo, spaceNo, statisticType, dungeonStatisticRecords)
        if totalBatchCount == 0:
            rankCountList = self.dungeonSettlementDataCache.setdefault('rankCountList', {})
            rankCountList[statisticType] = 0
            self._callback(0.1, '_getDungeonRankData', (self.dungeonSettlementDataCache['opUUID'], uniqueID, spaceNo), gametimer.TIMER_TAG_DUNGEON_SETTLEMENT_TIMER)
            return
        
        dataRecords = self.dungeonStatisticRecords.setdefault(statisticType, {})
        for dungeonStatisticRecord in dungeonStatisticRecords:
            dataRecords[dungeonStatisticRecord['gbId']] = dungeonStatisticRecord
        
        self.dungeonStatisticBatchCount += 1
        if totalBatchCount == self.dungeonStatisticBatchCount:
            rankCountList = self.dungeonSettlementDataCache.setdefault('rankCountList', {})
            rankCountList[statisticType] = len(dataRecords)
            self.dungeonStatisticBatchCount = 0
            self._callback(0.1, '_getDungeonRankData', (self.dungeonSettlementDataCache['opUUID'], uniqueID, spaceNo), gametimer.TIMER_TAG_DUNGEON_SETTLEMENT_TIMER)
            return

    def setGuildBox(self, box, opUUID):
        INFO_MSG("setGuildBox::", opUUID, self.spaceNo)
        self.guildBox = box
        self.opUUID = opUUID
    
    def getGuildBox(self):
        return self.guildBox
    
    def dungeonCompleted(self):
        INFO_MSG("dungeonCompleted::", self.spaceNo)
        self.guildBox.onGuildChallengeDungeonCompleted()

    def notifyDungeonExtarData(self, gbId, datas):
        self.dungeonExtraDatas[gbId] = datas
        
    def onGetSettlementRankList(self, rankType, spaceNo, uniqueID, playerBox, gbID, idx, offset):
        INFO_MSG("onGetSettlementRankList:: 1", self.dungeonSettlementDataCache['opUUID'], uniqueID, rankType, spaceNo, playerBox, gbID, idx, offset)
        results = []
        rankDatas = self.dungeonStatisticSortedRecords.get(rankType)
        if not rankDatas:
            WARNING_MSG("onGetSettlementRankList:: 2 no rank data, ", self.dungeonSettlementDataCache['opUUID'], uniqueID, rankType, spaceNo, playerBox, gbID, idx, offset)
            playerBox.client.onGetSettlementRankList(rankType, dungeonNo, idx, offset, results)
            return
        # 限制单次拉取的最大数量
        if offset > 10:
            offset = 10

        datas = rankDatas[idx:idx+offset]

        INFO_MSG("onGetSettlementRankList:: 3", self.dungeonSettlementDataCache['opUUID'], uniqueID, rankType, spaceNo, playerBox, gbID, idx, offset, len(datas), len(rankDatas))

        for data in datas:
            result = {
                'name':data['name'],
                'rank':data['rank'],
                'dmg':data['statisticsNum']
            }
            results.append(result)

        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        playerBox.client.onGetSettlementRankList(rankType, dungeonNo, idx, offset, results)
    
    def _calcPointsRanking(self, playMode, statisticType):
        INFO_MSG('_calcPointsRanking: 1', playMode, statisticType)
        results = {}
        statisticRecords = self.dungeonStatisticRecords.setdefault(statisticType, {})
        if len(statisticRecords) == 0:
            INFO_MSG('_calcPointsRanking: 2', playMode, statisticType)
            return results
        
        playerDiedScore = int(TM_PR.datas['playerDiedScore']['value'])
        if statisticType == gameconst.StatisticType.STA_TYPE_DEAD:
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
            DEBUG_MSG('_calcPointsRanking: 3', curRank, data, playMode, statisticType)
            # 首次找
            if rankCfgData is None:
                DEBUG_MSG('_calcPointsRanking: 4', curRank, playMode, statisticType)
                rankCfgData = self._doGetValidPointRankCfg(curRank, playMode, statisticType)
                if not rankCfgData:
                    return results
            DEBUG_MSG('_calcPointsRanking: 5', curRank, rankCfgData, data, playMode, statisticType)
            # 不在范围，重新找
            if not (curRank >= rankCfgData[0] and curRank <= rankCfgData[1]):
                DEBUG_MSG('_calcPointsRanking: 6', curRank, rankCfgData, data, playMode, statisticType)
                rankCfgData = self._doGetValidPointRankCfg(curRank, playMode, statisticType)
                if not rankCfgData:
                    return results
            DEBUG_MSG('_calcPointsRanking: 7', curRank, rankCfgData, data, playMode, statisticType)
            # 首个区间计算
            if lastMinScore is None:
                DEBUG_MSG('_calcPointsRanking: 8', curRank, rankCfgData, data, playMode, statisticType)
                results[data['gbId']] = rankCfgData[2]
            else:
                if data['statisticsNum'] > 0:
                    if data['statisticsNum'] >= rankDiffRatio * lastMinScore:
                        DEBUG_MSG('_calcPointsRanking: 9', curRank, rankCfgData, data, playMode, statisticType)
                        results[data['gbId']] = rankCfgData[2]
                    else:
                        DEBUG_MSG('_calcPointsRanking: 10', curRank, rankCfgData, data, playMode, statisticType)
                        results[data['gbId']] = rankCfgData[3]
                else:
                    DEBUG_MSG('_calcPointsRanking: 11', curRank, rankCfgData, data, playMode, statisticType)
                    results[data['gbId']] = 0
                
            # 当前范围的最后一名，更新一下上个区间的最小值                
            if curRank == rankCfgData[1]:
                DEBUG_MSG('_calcPointsRanking: 12', curRank, rankCfgData, data, playMode, statisticType)
                lastMinScore = data['statisticsNum']

        return results
    
    def _calcDeadCount(self, gbId, playMode, statisticType):
        INFO_MSG('_calcDeadCount: 1', gbId, playMode, statisticType)
        statisticRecords = self.dungeonStatisticRecords.setdefault(statisticType, {})
        if len(statisticRecords) == 0:
            INFO_MSG('_calcDeadCount: 2', gbId, playMode, statisticType)
            return 0
        
        for data in statisticRecords.values():
            if data['gbId'] == gbId:
                DEBUG_MSG('_calcDeadCount: 3', gbId, playMode, statisticType, data['statisticsNum'])
                return data['statisticsNum']
        return 0
        
    def _doGetValidPointRankCfg(self, rank, playMode, statisticType):
        rankCfgDatas = self.getStatisticRankCfg(playMode, statisticType)
        if not rankCfgDatas:
            ERROR_MSG("_doGetValidPointRankCfg:: no rank cfg data, ", rank, playMode, statisticType)
            return None
        
        for rankCfgData in rankCfgDatas:
            if len(rankCfgData) != 4:
                ERROR_MSG("_doGetValidPointRankCfg:: wrong rank cfg data, ", rank, playMode, statisticType, rankCfgDatas, rankCfgData)
                return None
            if rank >= rankCfgData[0] and rank <= rankCfgData[1]:
                return rankCfgData
        WARNING_MSG("_doGetValidPointRankCfg:: no rank cfg data, ", rank, playMode, statisticType, rankCfgDatas)
        return None
        
    def getStatisticRankCfg(self, playMode, statisticType):
        if statisticType == gameconst.StatisticType.STA_TYPE_DAMAGE:
            if playMode == gameconst.DungeonPlayModeEnum.CHIEF:
                return self._doGetStatisticRankCfg('dmg_level2Score15')
            elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
                return self._doGetStatisticRankCfg('dmg_level2Score5')
        elif statisticType == gameconst.StatisticType.STA_TYPE_HEAL:
            if playMode == gameconst.DungeonPlayModeEnum.CHIEF:
                return self._doGetStatisticRankCfg('addHp_level2Score_15')
            elif playMode == gameconst.DungeonPlayModeEnum.CRUSADE:
                return self._doGetStatisticRankCfg('addHp_level2Score_5')
        elif statisticType == gameconst.StatisticType.STA_TYPE_HURT:
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
        self.dungeonSettlementDataCache['dmgPoints'] = self._calcPointsRanking(playMode, gameconst.StatisticType.STA_TYPE_DAMAGE)
        self.dungeonSettlementDataCache['healPoints'] = self._calcPointsRanking(playMode, gameconst.StatisticType.STA_TYPE_HEAL)
        self.dungeonSettlementDataCache['hurtPoints'] = self._calcPointsRanking(playMode, gameconst.StatisticType.STA_TYPE_HURT)
        self.dungeonSettlementDataCache['deadPoints'] = self._calcPointsRanking(playMode, gameconst.StatisticType.STA_TYPE_DEAD)
    
    def _calcPlayerStatisticScore(self, playMode, gbId):
        score = self.dungeonSettlementDataCache['dmgPoints'].get(gbId, 0) \
                + self.dungeonSettlementDataCache['healPoints'].get(gbId, 0) \
                + self.dungeonSettlementDataCache['hurtPoints'].get(gbId, 0) \
                + self.dungeonSettlementDataCache['deadPoints'].get(gbId, 0)
        deadCount = self._calcDeadCount(gbId, playMode, gameconst.StatisticType.STA_TYPE_DEAD)
        return score, deadCount
    
    def onNotifySettlementResult(self, box, playMode, spaceNo, dungeonNo, opUUId, uniqueId, win, extra, firstPassRewards, goldPassRewards, dungeonRewards):
        INFO_MSG("onNotifySettlementResult::", opUUId, uniqueId, playMode, spaceNo, dungeonNo, win, extra, firstPassRewards, goldPassRewards, dungeonRewards)
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
        INFO_MSG("doDungeonMonsterBorn::", monsterGID, createTime, self.dungeonPlayMode.spaceUUID, self.spaceNo, self.dungeonPlayMode.playMode)
        if not monsterGID:
            return
        uniqueID = 0
        if formula.isTeamDungeonSpace(self.spaceNo):
            uniqueID = self.dungeonPlayMode.teamUUID
        elif formula.isRaidDungeonSpace(self.spaceNo):
            uniqueID = self.dungeonPlayMode.raidUUID
        else:
            return
        
        monsterData = CBD.datas.get(monsterGID)
        if monsterData and monsterData['nameSuffixID'] == gameconst.MonsterSuffix.BOSS:
            LogTrackingMgr.LogTrackingMgr.Dungeon_Boss_Born(
                uniqueID,
                self.dungeonPlayMode.playMode,
                formula.getDungeonNoBySpaceNo(self.spaceNo),
                self.dungeonPlayMode.spaceUUID,
                self.spaceNo,
                monsterGID,
                createTime,
                self.dungeonPlayMode.tCreate
            )

    def doDungeonMonsterDead(self, monsterGID, createTime):
        INFO_MSG("doDungeonMonsterDead::", monsterGID, createTime, self.dungeonPlayMode.spaceUUID, self.spaceNo, self.dungeonPlayMode.playMode)
        if not monsterGID:
            return
        uniqueID = 0
        if formula.isTeamDungeonSpace(self.spaceNo):
            uniqueID = self.dungeonPlayMode.teamUUID
        elif formula.isRaidDungeonSpace(self.spaceNo):
            uniqueID = self.dungeonPlayMode.raidUUID
        else:
            return
        
        monsterData = CBD.datas.get(monsterGID)
        if monsterData and monsterData['nameSuffixID'] == gameconst.MonsterSuffix.BOSS:
            LogTrackingMgr.LogTrackingMgr.Dungeon_Boss_Dead(
                uniqueID,
                self.dungeonPlayMode.playMode,
                formula.getDungeonNoBySpaceNo(self.spaceNo),
                self.dungeonPlayMode.spaceUUID,
                self.spaceNo,
                monsterGID,
                createTime,
                utils.getNow(),
                self.dungeonPlayMode.tCreate
            )

    def recordAutoFightTimes(self, gbId, state, times):
        INFO_MSG("recordAutoFightTimes::", gbId, state, times, self.dungeonPlayMode.spaceUUID, self.spaceNo, self.dungeonPlayMode.playMode)
        self.dungeonAutoBattleTimes[gbId] = self.dungeonAutoBattleTimes.get(gbId, 0) + times
