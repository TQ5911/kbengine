# coding: utf-8

import KBEngine
from KBEDebug import *
import gameglobal
import gameconst
import gameengine
import gametimer
import gamesql
import utils

import iTimer
import iGlobal
import iBaseNoCell
import rank_rankConfig as R_RCD
import rank_Rank as R_RD
import character_charData as C_CDD


class LeaderBoardStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell,
                            iTimer.ITimer):
    def __init__(self):
        DEBUG_MSG('LeaderBoardAvatarStub init')
        self.leaderBoardList.leaderBoardType = self.leaderBoardType
        self.leaderBoardCache = {}
        _dur = R_RCD.datas['refreshCD']['value']
        self.pyAddTimer(_dur, _dur, gametimer.LEADER_BOARD_REFRESH)

        _globalName = '{}{}'.format(self.__class__.__name__, self.leaderBoardType)
        gameengine.setGlobalData(_globalName, self)
        self.leaderBoardIdx = 1

    def doNext(self):
        DEBUG_MSG('LeaderBoardAvatarStub doNext')
        # gameglobal.localBaseApp.fullPrepare(self.classname())
        super().doNext()

    def onFirstCreate(self):
        DEBUG_MSG('LeaderBoardAvatarStub onFirstCreate')
        self.writeToDB(self._onWriteToDB)

    def _onWriteToDB(self, ok, entity):
        DEBUG_MSG('LeaderBoardAvatarStub _onWriteToDB')
        if not ok:
            ERROR_MSG('LeaderBoardAvatarStub _onWriteToDB failed')
        else:
            gamesql.recordLeaderBoardStub(self.leaderBoardType, self.databaseID, self._onRecordLeaderBoardStubCB)

    def _onRecordLeaderBoardStubCB(self, *args):
        INFO_MSG('LeaderBoardAvatarStub _onRecordLeaderBoardStubCB')

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.LEADER_BOARD_REFRESH:
            self._onLeaderBoardRefresh()
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

    def _onLeaderBoardRefresh(self):
        DEBUG_MSG('LeaderBoardAvatarStub _onLeaderBoardRefresh')

        _cacheDic = self.toCacheDic()
        lbList = list(_cacheDic.values())

        sortedList = sorted(lbList, key=self.leaderBoardList.instaniateCls().sortKeyFunc())
        self.leaderBoardList.clear()

        _maxNum = R_RD.datas[self.leaderBoardType]['displayNum']
        _schoolsData = {}
        for _school in C_CDD.datas:
            _schoolsData[_school] = []

        for _lbcVal in sortedList:
            if len(self.leaderBoardList) >= _maxNum\
                    and not _schoolsData:
                break

            if len(self.leaderBoardList) < _maxNum:
                self.leaderBoardList.append(_lbcVal)

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

        _iter = self._sendLeaderBoardRankIdx()
        self.batchlyCall(_iter, 1, 0.1)

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

    def doGetLeaderBoardList(self, box, leaderBoardIdx, school):
        if leaderBoardIdx >= self.leaderBoardIdx:
            box.client.leaderBoardNotChanged(self.leaderBoardType ,leaderBoardIdx, school)
            return

        if not school:
            _list = self.leaderBoardList
        else:
            _list = self.leaderBoardList.getSchoolData(school)

        _func = self.leaderBoardList.instaniateCls().funcName()
        getattr(box.client, _func)(self.leaderBoardIdx, _list, school)

