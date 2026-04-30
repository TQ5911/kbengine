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
import rank_rankConfig as R_RCD
import rank_Rank as R_RD
import character_charData as C_CDD
from datetime import datetime
import welfare_config as W_CDD
import iCycleEvent
import redisUtils
import json
import gameconfig

class LeaderBoardStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell,
                            iTimer.ITimer, iCycleEvent.ICycleEvent):
    def __init__(self):
        LOG_IFO('LeaderBoardAvatarStub init')

        iCycleEvent.ICycleEvent.__init__(self)
        self.leaderBoardList.leaderBoardType = self.leaderBoardType
        self.leaderBoardCache = {}
        _dur = R_RCD.datas['refreshCD']['value']
        self.pyAddTimer(_dur, _dur, gametimer.LEADER_BOARD_REFRESH)

        _globalName = '{}{}'.format(self.__class__.__name__, self.leaderBoardType)
        gameengine.setGlobalData(_globalName, self)
        self.leaderBoardIdx = 1
        
        self.registerDailyEvent('_recalDynamicWorldLevel')
        self.onDailyEvent()

        if self.leaderBoardType == gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK:
            delta = utils.curTS() % 3600
            self.pyAddTimer(3600 - delta, 3600, gametimer.GEN_RUSH_RANK_DATA)
            self._genRushRankData()
            self._checkRushRankRefresh()

    def doNext(self):
        LOG_IFO('LeaderBoardAvatarStub doNext')
        # gameglobal.localBaseApp.fullPrepare(self.classname())
        super().doNext()

    def onFirstCreate(self):
        LOG_IFO('LeaderBoardAvatarStub onFirstCreate')
        self.writeToDB(self._onWriteToDB)

    def _onWriteToDB(self, ok, entity):
        LOG_IFO('LeaderBoardAvatarStub _onWriteToDB')
        if not ok:
            LOG_ERR('LeaderBoardAvatarStub _onWriteToDB failed')
        else:
            gamesql.recordLeaderBoardStub(self.leaderBoardType, self.databaseID, self._onRecordLeaderBoardStubCB)

    def _onRecordLeaderBoardStubCB(self, *args):
        LOG_IFO('LeaderBoardAvatarStub _onRecordLeaderBoardStubCB')

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
        elif userArg == gametimer.CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        else:
            self._onTimer(tid, userArg)

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
        LOG_IFO("rush rank need refresh: ", utils.curTS(), date)
        EPS = 2 * 60
        if utils.curTS() <= date or abs(utils.curTS() - date) <= EPS:
            return True

        LOG_IFO("rush rank out of time", utils.curTS(), date)
        return False
    
    def _genRushRankData(self):
        key = gameconst.RedisKey.LEVEL_RUSH_RANK_DATA_KEY + str(gameconfig.serverId()) + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(utils.curTS()))
        LOG_IFO("gen rush rank data key: ", key)
        
        td = time.time()
        redisUtils.RedisUtils.set(key, json.dumps(self.leaderBoardList.toLeaderBoardListSavedDict(), separators=(',', ':'), indent=None), self._onGenRushRankDataCB)
        LOG_IFO("gen rush rank data time: ", time.time() - td, "len: ", len(self.leaderBoardList))

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
            LOG_IFO("rush rank make callback", now, date, _dur)
            self.addTimerCB(date - now, '_onLeaderBoardRefresh', (), gametimer.TIMER_TAG_RUSH_RANK_REFRESH)

    def _onGenRushRankDataCB(self, ok, data):
        if not ok:
            LOG_IFO("gen rush rank data failed")
        else:
            LOG_IFO("gen rush rank data success", data)

    def _onLeaderBoardRefresh(self):
        LOG_IFO('LeaderBoardAvatarStub _onLeaderBoardRefresh')

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
        if _cls.calcSchool():
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

    def _recalDynamicWorldLevel(self):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            return
        
        _list = self.leaderBoardList
        if len(_list) < 100:
            return

        avgLevel = int(sum(x.level for x in _list[:100]) / 100)
        self.dynamicWorldLevel = avgLevel
        LOG_IFO("recalDynamicWorldLevel", self.dynamicWorldLevel)

    def getDynamicWorldLevel(self, box):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_LEVEL:
            LOG_ERR("getDynamicWorldLevel failed, leaderBoardType is not AVATAR_LEVEL", self.leaderBoardType)
            return

        box.onGetDynamicWorldLevel(self.dynamicWorldLevel)