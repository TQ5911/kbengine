# coding: utf-8

from KBEDebug import *
import gameconst
import gameengine
import gametimer
import gameglobal
import utils
import json
import gameconfig
import rank_rankConfig as R_RCD
import rank_Rank as R_RD
import LeaderBoardAvatarScoreInfo
import welfare_config as W_CDD
from datetime import datetime


class IScoreRushRank(object):
    """冲刺战力榜定榜：到达 ScoreRankDeadLine 时对战力榜做最终重排并快照，
    之后定榜界面固定展示快照数据（仅 AVATAR_SCORE 类型的 Stub 生效）"""

    def __init__(self):
        self.scoreRankSnapshot = {}
        self.scoreRankSnapshotList = []
        self.scoreRankFinalized = False

    def _getScoreRankDeadline(self):
        dateStr = W_CDD.datas['ScoreRankDeadLine']['value']
        date = datetime.strptime(dateStr, "%Y%m%d%H%M")
        return int(date.timestamp())

    def _getScoreRankFinalRedisKey(self):
        return gameconst.RedisKey.SCORE_RANK_FINAL_DATA_KEY + str(gameconfig.serverId())

    def _getScoreRankDisplayNum(self):
        # 定榜后对外展示的榜单人数（配置的100名）
        return R_RD.datas[gameconst.LeaderBoardType.AVATAR_SCORE]['displayNum']

    def _checkScoreRankFinalize(self):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_SCORE:
            return

        LOG_INFO('_checkScoreRankFinalize')
        if self.scoreRankFinalized:
            return

        _deadline = self._getScoreRankDeadline()
        if utils.curTS() < _deadline:
            self._datetimeCallback(_deadline, '_finalizeScoreRank', (), gametimer.TIMER_TAG_SCORE_RANK_FINALIZE)
        else:
            # 已过截止时间，尝试从 redis 恢复定榜快照
            self._recoverScoreRankSnapshot()

    def _recoverScoreRankSnapshot(self):
        gameglobal.localBaseApp.getRedisClient().get(self._getScoreRankFinalRedisKey(), self._onRecoverScoreRankSnapshot)

    def _onRecoverScoreRankSnapshot(self, cid, err, res):
        if err or not res:
            LOG_WARN('LeaderBoardStub recover score rank snapshot failed, do finalize instead', err)
            # self._finalizeScoreRank()
            return

        try:
            _data = json.loads(res.decode())
            for _idx, _row in enumerate(_data):
                self.scoreRankSnapshot[_row['gbId']] = (_idx + 1, _row['score'])
            _displayNum = self._getScoreRankDisplayNum()
            self.scoreRankSnapshotList = [
                LeaderBoardAvatarScoreInfo.LeaderBoardAvatarScoreVal(**_row) for _row in _data[:_displayNum]
            ]
            self.scoreRankFinalized = True
            LOG_INFO('LeaderBoardStub recover score rank snapshot success', len(self.scoreRankSnapshot))
        except Exception as _e:
            LOG_ERR('LeaderBoardStub recover score rank snapshot parse failed', _e)
            # self._finalizeScoreRank()

    def _onSaveScoreRankSnapshotCB(self, cid, err, res):
        if err:
            LOG_ERR('LeaderBoardStub save score rank snapshot failed', err)
        else:
            LOG_INFO('LeaderBoardStub save score rank snapshot success', len(self.scoreRankSnapshot))

    def _finalizeScoreRank(self):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_SCORE:
            return

        if self.scoreRankFinalized:
            return

        LOG_INFO('LeaderBoardStub _finalizeScoreRank')

        # 停掉固定刷新定时器，结算完再重启，避免刚结算完又触发固定刷新
        if self.leaderBoardRefreshTimerId:
            self.pyDelTimer(self.leaderBoardRefreshTimerId, gametimer.LEADER_BOARD_REFRESH)
            self.leaderBoardRefreshTimerId = 0

        self._onLeaderBoardRefresh()

        self.scoreRankSnapshot = {}
        for _idx, _lbcVal in enumerate(self.leaderBoardList):
            self.scoreRankSnapshot[_lbcVal.gbId] = (_idx + 1, _lbcVal.score)

        self.scoreRankSnapshotList = list(self.leaderBoardList[:self._getScoreRankDisplayNum()])

        _snapshotJson = json.dumps([_lbcVal.toLeaderBoardCacheSavedDict() for _lbcVal in self.leaderBoardList], separators=(',', ':'), indent=None)
        # LOG_INFO('LeaderBoardStub _finalizeScoreRank result', len(self.scoreRankSnapshot), _snapshotJson)
        gameglobal.localBaseApp.getRedisClient().cmdSet(
            self._getScoreRankFinalRedisKey(),
            _snapshotJson,
            self._onSaveScoreRankSnapshotCB
        )

        self.scoreRankFinalized = True
        gameengine.broadcastBaseapp('onBroadcastToAllClients', ('onScoreRushRankFinalized', ()))

        _dur = R_RCD.datas['refreshCD']['value']
        self.leaderBoardRefreshTimerId = self.pyAddTimer(_dur, _dur, gametimer.LEADER_BOARD_REFRESH)

    def gmFinalizeScoreRank(self, force):
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_SCORE:
            LOG_WARN('gmFinalizeScoreRank failed, leaderBoardType is not AVATAR_SCORE', self.leaderBoardType)
            return

        if self.scoreRankFinalized and not force:
            LOG_WARN('gmFinalizeScoreRank failed, already finalized')
            return

        LOG_WARN('gmFinalizeScoreRank', force)
        self.scoreRankFinalized = False
        self._finalizeScoreRank()

    def getScoreRushRankSelf(self, box, gbId):
        LOG_DBG('getScoreRushRankSelf:', gbId)
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_SCORE:
            LOG_ERR('getScoreRushRankSelf failed, leaderBoardType is not AVATAR_SCORE', self.leaderBoardType)
            return

        if self.scoreRankFinalized:
            _rank, _score = self.scoreRankSnapshot.get(gbId, (0, 0))
            box.client.onScoreRushRankSelf(gameconst.ScoreRushRankState.FINALIZED, _rank, _score)
        elif utils.curTS() < self._getScoreRankDeadline():
            # 未定榜，返回实时榜中的自己排名和战力
            _rank, _lbcVal = self._getRankIdx(gbId, self.leaderBoardList)
            _score = _lbcVal.score if _lbcVal else 0
            box.client.onScoreRushRankSelf(gameconst.ScoreRushRankState.NOT_FINAL, _rank, _score)
        else:
            box.client.onScoreRushRankSelf(gameconst.ScoreRushRankState.FINALIZING, 0, 0)

    def getScoreRushRankList(self, box, gbId, page):
        LOG_DBG('getScoreRushRankList:', gbId, page)
        if self.leaderBoardType != gameconst.LeaderBoardType.AVATAR_SCORE:
            LOG_ERR('getScoreRushRankList failed, leaderBoardType is not AVATAR_SCORE', self.leaderBoardType)
            return

        if not self.scoreRankFinalized:
            LOG_ERR('getScoreRushRankList failed, score rank not finalized', gbId)
            return

        # 定榜后只提供配置的 displayNum（100名）榜单，分页大小固定
        _start = page * gameconst.LEADER_BOARD_PAGE_SIZE
        _end = _start + gameconst.LEADER_BOARD_PAGE_SIZE
        _isEnd = _end >= len(self.scoreRankSnapshotList)
        _list = self.scoreRankSnapshotList[_start:_end]
        box.client.onScoreRushRankList(_list, page, _isEnd)
