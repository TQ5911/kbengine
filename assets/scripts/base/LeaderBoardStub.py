# coding: utf-8

import KBEngine
from KBEDebug import *
import gameglobal
import gameconst
import gameengine
import gametimer
import gamesql
import utils
import time
import iTimer
import iGlobal
import iBaseNoCell
import iScoreRushRank
import rank_rankConfig as R_RCD
import rank_Rank as R_RD
import character_charData as C_CDD
from datetime import datetime
import welfare_config as W_CDD
import iCycleEvent
import redisUtils
import json
import gameconfig
import experience_config as E_CDD
import formula
import iRouter

class LeaderBoardStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell,
                            iTimer.ITimer, iCycleEvent.ICycleEventMixin,
                            iScoreRushRank.IScoreRushRank):
    def __init__(self):
        LOG_INFO('LeaderBoardAvatarStub init')

        iCycleEvent.ICycleEventMixin.__init__(self)
        iScoreRushRank.IScoreRushRank.__init__(self)

        self.leaderBoardList.leaderBoardType = self.leaderBoardType
        self.leaderBoardCache = {}
        _dur = R_RCD.datas['refreshCD']['value']
        self.leaderBoardRefreshTimerId = self.pyAddTimer(_dur, _dur, gametimer.LEADER_BOARD_REFRESH)

        _globalName = '{}{}'.format(self.__class__.__name__, self.leaderBoardType)
        gameengine.setGlobalData(_globalName, self)
        self.leaderBoardIdx = 1
        
        self.initDatetimeTimerTick()
        self.registerDailyEvent('_recalDynamicWorldLevel')
        self.onDailyEvent()
        self._syncWorldLevelToGlobal()

        if self.leaderBoardType == gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK:
            delta = utils.curTS() % 3600
            self.pyAddTimer(3600 - delta, 3600, gametimer.GEN_RUSH_RANK_DATA)
            self._genRushRankData()
            self._checkRushRankRefresh()

        if self.leaderBoardType == gameconst.LeaderBoardType.AVATAR_SCORE:
            self._checkScoreRankFinalize()

    def doNext(self):
        LOG_INFO('LeaderBoardAvatarStub doNext')
        # gameglobal.localBaseApp.fullPrepare(self.classname())
        super().doNext()

    def onFirstCreate(self):
        LOG_INFO('LeaderBoardAvatarStub onFirstCreate')
        self.writeToDB(self._onWriteToDB)

    def _onWriteToDB(self, ok, entity):
        LOG_INFO('LeaderBoardAvatarStub _onWriteToDB')
        if not ok:
            LOG_ERR('LeaderBoardAvatarStub _onWriteToDB failed')
        else:
            gamesql.recordLeaderBoardStub(self.leaderBoardType, self.databaseID, self._onRecordLeaderBoardStubCB)

    def _onRecordLeaderBoardStubCB(self, *args):
        LOG_INFO('LeaderBoardAvatarStub _onRecordLeaderBoardStubCB')

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.LEADER_BOARD_REFRESH:
            self._onLeaderBoardRefresh()
            self._checkRushRankRefresh()
        elif userArg == gametimer.GEN_RUSH_RANK_DATA:
            self._genRushRankData()
        elif userArg == gametimer.TIMER_CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
            self._samplePeakOnlineNum()
        else:
            self._onTimerTrigger(tid, userArg)

    def onGetLeaderBoardCache(self, lbacVal):
        self.leaderBoardCache[lbacVal.key] = lbacVal

    def toCacheDic(self):
        _cacheDic = self.leaderBoardCache
        for _lbcVal in self.leaderBoardList:
            if _lbcVal.key in _cacheDic:
                continue

            _cacheDic[_lbcVal.key] = _lbcVal

        return _cacheDic

    def _needRefresh(self):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK:
            return True
        
        dateStr = W_CDD.datas['LevelRankDeadLine']['value']
        date = datetime.strptime(dateStr, "%Y%m%d%H%M")
        date = int(date.timestamp())
        LOG_INFO("rush rank need refresh: ", utils.curTS(), date)
        EPS = 2 * 60
        if utils.curTS() <= date or abs(utils.curTS() - date) <= EPS:
            return True

        LOG_INFO("rush rank out of time", utils.curTS(), date)
        return False
    
    def _genRushRankData(self):
        key = gameconst.RedisKey.LEVEL_RUSH_RANK_DATA_KEY + str(gameconfig.serverId()) + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(utils.curTS()))
        LOG_INFO("gen rush rank data key: ", key)
        
        td = time.time()
        redisUtils.RedisUtils.cmdSet(key, json.dumps(self.leaderBoardList.toLeaderBoardListSavedDict(), separators=(',', ':'), indent=None), self._onGenRushRankDataCB)
        LOG_INFO("gen rush rank data time: ", time.time() - td, "len: ", len(self.leaderBoardList))

    def _checkRushRankRefresh(self):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK:
            return
        
        if not self._needRefresh():
            return
        
        dateStr = W_CDD.datas['LevelRankDeadLine']['value']
        date = datetime.strptime(dateStr, "%Y%m%d%H%M")
        date = int(date.timestamp())
        now = utils.curTS()
        _dur = R_RCD.datas['refreshCD']['value']
        if date > now and date - now < _dur:
            LOG_INFO("rush rank make callback", now, date, _dur)
            self.addTimerCB(date - now, '_onLeaderBoardRefresh', (), gametimer.TIMER_TAG_RUSH_RANK_REFRESH)

    def _onGenRushRankDataCB(self, ok, data):
        if not ok:
            LOG_INFO("gen rush rank data failed")
        else:
            LOG_INFO("gen rush rank data success", data)

    def _onLeaderBoardRefresh(self):
        LOG_INFO('LeaderBoardAvatarStub _onLeaderBoardRefresh')

        if not self._needRefresh():
            return

        _cacheDic = self.toCacheDic()
        lbList = list(_cacheDic.values())

        _cls = self.leaderBoardList.instaniateCls()

        if not _cls:
            LOG_WARN("LeaderBoardAvatarStub _onLeaderBoardRefresh _cls is None", self.leaderBoardType)
            return
        sortedList = sorted(lbList, key=_cls.sortKeyFunc())
        self.leaderBoardList.clear()

        _maxNum = R_RD.datas[self.leaderBoardType]['maxNum'] if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK else 3000
        self.leaderBoardList.extend(sortedList[:_maxNum])

        # 玩家数据需要考虑根据不同职业的分榜，其他如帮会数据就不需要
        if _cls.calcSchool():
            _schoolsData = {}
            for _school in C_CDD.datas:
                _schoolsData[_school] = []

            for _lbcVal in sortedList:
                if not _schoolsData:
                    break

                if _lbcVal.school not in _schoolsData:
                    continue

                _schoolsData[_lbcVal.school].append(_lbcVal)
                if len(_schoolsData[_lbcVal.school]) >= _maxNum:
                    self.leaderBoardList.replaceSchoolData(_lbcVal.school, _schoolsData[_lbcVal.school])
                    _schoolsData.pop(_lbcVal.school)

            for _school, _listData in _schoolsData.items():
                self.leaderBoardList.replaceSchoolData(_school, _listData)

        self.leaderBoardCache = {}
        self.leaderBoardIdx += 1

        # 玩家数据需要计算成就，所以要通知到每个玩家
        if _cls.calcSchool() or self.leaderBoardType == gameconst.LeaderBoardType.GUILD:
            _iter = self._sendLeaderBoardRankIdx()
            self.batchlyCall(_iter, 1, 0.1)

        _iter = self._doLeaderBoardLogIter()
        self.batchlyCall(_iter, 1, 0.1)

    def _doLeaderBoardLogIter(self):
        _idx = 0
        while _idx < len(self.leaderBoardList):
            if _idx + 1 > gameconst.LEADER_BOARD_MAX_LOG_SIZE:
                break

            _lbcVal = self.leaderBoardList[_idx]
            _lbcVal.leaderBoardLog(self.leaderBoardType, _idx + 1)
            yield utils.emptyFunc
            _idx += 1

    def _sendLeaderBoardRankIdx(self):
        _idx = 0
        while _idx < len(self.leaderBoardList):
            _lbcVal = self.leaderBoardList[_idx]
            if self.leaderBoardType == gameconst.LeaderBoardType.GUILD:
                gameengine.getGlobalBase('GuildStub').callOnGuild(
                    _lbcVal.guildUUID,
                    'onLeaderBoardRank',
                    (self.leaderBoardType, _idx + 1),
                    None, '', ())
            else:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [_lbcVal.gbId, ],
                    'onLeaderBoardRank',
                    (self.leaderBoardType, _idx + 1),
                    None, '', ())

            yield lambda *args: args
            _idx += 1

    def _getRankIdx(self, key, lbList):
        if not key:
            return 0, None

        for _idx, _lbcVal in enumerate(lbList):
            if _lbcVal.key == key:
                return _idx + 1, _lbcVal

        return 0, None

    def doGetLeaderBoardGuildList(self, box, leaderBoardIdx, guildUUID, page):
        if leaderBoardIdx >= self.leaderBoardIdx:
            box.client.leaderBoardNotChanged(self.leaderBoardType, leaderBoardIdx, 0)
            return

        _list = self.leaderBoardList

        if page == 0:
            # 第一页特殊处理一下，把玩家排名塞里面
            # 1.如果玩家在排行榜，那么第一页额外在最后一位塞当前玩家数据
            _rank, _lbcVal = self._getRankIdx(guildUUID, _list)

        else:
            _rank, _lbcVal = 0, None

        _func = self.leaderBoardList.instaniateCls().funcName()
        _start = page * gameconst.LEADER_BOARD_PAGE_SIZE
        _end = _start + gameconst.LEADER_BOARD_PAGE_SIZE
        displayNum = R_RD.datas[self.leaderBoardType]['displayNum'] if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK else 100
        maxEnd = min(len(_list), displayNum)
        _isEnd = _end >= maxEnd
        _list = _list[_start : _end]

        if _lbcVal is not None:
            _list.append(_lbcVal)

        getattr(box.client, _func)(self.leaderBoardIdx, _list, page, _isEnd, _rank)

    def doGetLeaderBoardList(self, box, gbId, leaderBoardIdx, school, page):
        if leaderBoardIdx >= self.leaderBoardIdx:
            box.client.leaderBoardNotChanged(self.leaderBoardType, leaderBoardIdx, school)
            return

        if not school:
            _list = self.leaderBoardList
        else:
            _list = self.leaderBoardList.getSchoolData(school)

        if page == 0:
            # 第一页特殊处理一下，把玩家排名塞里面
            # 1.如果玩家在排行榜，那么第一页额外在最后一位塞当前玩家数据
            _rank, _lbcVal = self._getRankIdx(gbId, _list)

        else:
            _rank, _lbcVal = 0, None

        _func = self.leaderBoardList.instaniateCls().funcName()
        _start = page * gameconst.LEADER_BOARD_PAGE_SIZE
        _end = _start + gameconst.LEADER_BOARD_PAGE_SIZE
        displayNum = R_RD.datas[self.leaderBoardType]['displayNum'] if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK else 100
        maxEnd = min(len(_list), displayNum)
        _isEnd = _end >= maxEnd
        _list = _list[_start : _end]

        if _lbcVal is not None:
            _list.append(_lbcVal)

        getattr(box.client, _func)(self.leaderBoardIdx, _list, school, page, _isEnd, _rank)
        box.onGetLeaderBoardList(_func, self.leaderBoardIdx, _list, school, page, _isEnd, _rank)

    def _samplePeakOnlineNum(self):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            return

        today = utils.getIntDateTime(utils.curTS(), 0)
        if self.peakOnlineDate and self.peakOnlineDate != today:
            self.yesterdayPeakOnlineNum = self.peakOnlineNum
            self.peakOnlineNum = 0
            LOG_INFO("resetDailyPeakOnline", self.yesterdayPeakOnlineNum, today)
        self.peakOnlineDate = today

        onlineNum = 0
        if gameglobal.localLoginStub:
            onlineNum = gameglobal.localLoginStub.getGlobalAccountNum()
        if onlineNum > self.peakOnlineNum:
            self.peakOnlineNum = onlineNum

    def _recalDynamicWorldLevel(self, *args):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            return

        if len(self.leaderBoardList) > 0:
            self._samplePeakOnlineNum()
            peakOnlineNum = self.yesterdayPeakOnlineNum or self.peakOnlineNum
            if peakOnlineNum <= 0:
                LOG_INFO("recalDynamicWorldLevel skip, peakOnlineNum is 0", self.dynamicWorldLevel)
            else:
                rankPercent = E_CDD.datas['rankWorldLevel']['value']
                rank = max(1, formula.round2(peakOnlineNum * rankPercent / 100.0))
                rankIdx = min(rank, len(self.leaderBoardList)) - 1
                newLevel = self.leaderBoardList[rankIdx].level
                self.dynamicWorldLevel = max(self.dynamicWorldLevel, newLevel)
                LOG_INFO("recalDynamicWorldLevel", self.dynamicWorldLevel, peakOnlineNum, rankPercent, rank)

        self._syncWorldLevelToGlobal()
        # 只有跨服去收各服世界等级，算出后广播，保证组内 crossWorldLevel 一致
        if gameconfig.isCrossServer():
            self.addTimerCB(10, '_collectGroupWorldLevel', (), gametimer.TIMER_TAG_CROSS_WORLD_LEVEL)

    def _getGroupGameServerIds(self):
        sid = gameconfig.serverId()
        if sid not in gameglobal.mapleServerInfo:
            return []
        groupId = gameglobal.mapleServerInfo[sid]['server_group']
        crossId = int(gameconfig.getCrossServerId())
        return [int(s) for s in utils.group2ServerIds(groupId) if int(s) != crossId]

    def _collectGroupWorldLevel(self):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            return
        if not gameconfig.isCrossServer():
            return

        self._crossWorldLevelApplied = False
        self._groupWorldLevelMap = {}
        serverIds = self._getGroupGameServerIds()

        if not serverIds:
            LOG_INFO("collectGroupWorldLevel skip, no game servers")
            return
        
        stubName = 'LeaderBoardStub' + str(gameconst.LeaderBoardType.AVATAR_LEVEL)
        for sid in serverIds:
            iRouter.RemoteServerStubEntityCall(sid, stubName).onReqServerWorldLevel(int(gameconfig.serverId()))

        self.addTimerCB(20, '_applyCrossWorldLevel', (), gametimer.TIMER_TAG_CROSS_WORLD_LEVEL)

    def onReqServerWorldLevel(self, fromServerId):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            return
        stubName = 'LeaderBoardStub' + str(gameconst.LeaderBoardType.AVATAR_LEVEL)
        iRouter.RemoteServerStubEntityCall(int(fromServerId), stubName).onAckServerWorldLevel(
            int(gameconfig.serverId()), self.dynamicWorldLevel)

    def onAckServerWorldLevel(self, serverId, level):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            return
        if getattr(self, '_crossWorldLevelApplied', False):
            return
        if not hasattr(self, '_groupWorldLevelMap'):
            self._groupWorldLevelMap = {}
        self._groupWorldLevelMap[int(serverId)] = level
        if len(self._groupWorldLevelMap) >= len(self._getGroupGameServerIds()):
            self._applyCrossWorldLevel()

    def _applyCrossWorldLevel(self):
        if getattr(self, '_crossWorldLevelApplied', False):
            return
        levels = list(getattr(self, '_groupWorldLevelMap', {}).values())
        if not levels:
            LOG_INFO("applyCrossWorldLevel skip, no levels")
            return

        self._crossWorldLevelApplied = True
        avgLevel = formula.round2(sum(levels) / float(len(levels)))
        self.crossWorldLevel = max(self.crossWorldLevel, avgLevel)
        self.dynamicWorldLevel = self.crossWorldLevel
        LOG_INFO("applyCrossWorldLevel", avgLevel, self.crossWorldLevel, self.dynamicWorldLevel, levels)
        self._syncWorldLevelToGlobal()

        stubName = 'LeaderBoardStub' + str(gameconst.LeaderBoardType.AVATAR_LEVEL)
        for sid in self._getGroupGameServerIds():
            iRouter.RemoteServerStubEntityCall(sid, stubName).onSyncCrossWorldLevel(self.crossWorldLevel)

    def onSyncCrossWorldLevel(self, level):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            return
        if gameconfig.isCrossServer():
            return

        self.crossWorldLevel = max(self.crossWorldLevel, level)
        if utils.getSvrOpenDays() >= E_CDD.datas['activateCrossWorldLevel']['value']:
            maxDelta = E_CDD.datas['activateCrossWorldLevelMax']['value']
            if self.crossWorldLevel - self.dynamicWorldLevel > maxDelta:
                self.dynamicWorldLevel = self.dynamicWorldLevel + maxDelta
            else:
                self.dynamicWorldLevel = max(self.dynamicWorldLevel, self.crossWorldLevel)
        LOG_INFO("onSyncCrossWorldLevel", level, self.crossWorldLevel, self.dynamicWorldLevel)
        self._syncWorldLevelToGlobal()

    def getDynamicWorldLevel(self, box):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            LOG_ERR("getDynamicWorldLevel failed, leaderBoardType is not AVATAR_LEVEL", self.leaderBoardType)
            return

        box.onGetDynamicWorldLevel(self.dynamicWorldLevel)

    def _syncWorldLevelToGlobal(self):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            return
        gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_WORLD_LEVEL, self.dynamicWorldLevel)
        gameglobal.worldLevel = self.dynamicWorldLevel
        gameengine.setGlobalData(gameconst.GLOBALDATA_KEY_CROSS_WORLD_LEVEL, self.crossWorldLevel)
        gameglobal.crossWorldLevel = self.crossWorldLevel
        LOG_INFO("syncWorldLevelToGlobal", self.dynamicWorldLevel, self.crossWorldLevel)

    def gmSetDynamicWorldLevel(self, level):
        self.dynamicWorldLevel = level
        LOG_WARN("gmSetDynamicWorldLevel", self.dynamicWorldLevel)
        self._syncWorldLevelToGlobal()