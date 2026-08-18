# coding: utf-8

import gameconfig
import gameconst
import gametimer
import actionContext
import gameengine
import gamedecorator
import gameglobal
import LeaderBoardAvatarCacheInfo
import LeaderBoardAvatarScoreInfo
import LeaderBoardAvatarLevelRushRankInfo
import LeaderBoardAvatarAchievementInfo
from KBEDebug import *

import rank_Rank as R_RD
import rank_rankConfig as R_RCD


class ILeaderBoard(object):
    def __init__(self):
        _dur = max(1, R_RCD.datas['refreshCD']['value'] - 5)
        self.pyAddTimer(
            30, # 大概等 score 更新完毕
            _dur,
            gametimer.UPDATE_AVATAR_LEADERBOARD)

    @gamedecorator.checkGameconfigEnable('rank')
    @gamedecorator.crossServer
    def getLeaderBoardList(self, exposed, leaderBoardType, leaderBoardIdx, school, page):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_getLeaderBoardList', (leaderBoardType, leaderBoardIdx, school, page))
        else:
            self._getLeaderBoardList(leaderBoardType, leaderBoardIdx, school, page)

    def _getLeaderBoardList(self, leaderBoardType, leaderBoardIdx, school, page):
        if leaderBoardType == gameconst.LeaderBoardType.GUILD:
            gameengine.getLeaderStub(leaderBoardType).doGetLeaderBoardGuildList(
                self,
                leaderBoardIdx,
                self.guildUUIDBase,
                page,
            )

            return

        return gameengine.getLeaderStub(leaderBoardType).doGetLeaderBoardList(
            self,
            self.gbID,
            leaderBoardIdx,
            school,
            page)

    def onGetLeaderBoardList(self, funcName, leaderBoardIdx, _list, school, page, _isEnd, _rank):
        if self.isCrossServerInLocalServer:
            self.syncMethodCallToCrossServerBase('_onGetLeaderBoardList', (funcName, leaderBoardIdx, _list, school, page, _isEnd, _rank))

    def _onGetLeaderBoardList(self, funcName, leaderBoardIdx, _list, school, page, _isEnd, _rank):
        getattr(self.client, funcName)(leaderBoardIdx, _list, school, page, _isEnd, _rank)

    @gamedecorator.checkGameconfigEnable('rank')
    def getLevelRushRankList(self, exposed, leaderBoardType, leaderBoardIdx, school, page):
        return gameengine.getLeaderStub(leaderBoardType).doGetLeaderBoardList(
            self,
            self.gbID,
            leaderBoardIdx,
            school,
            page)

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('rank')
    def getScoreRushRankSelf(self, exposed):
        gameengine.getLeaderStub(gameconst.LeaderBoardType.AVATAR_SCORE).getScoreRushRankSelf(self, self.gbID)

    @gamedecorator.limitcall(2)
    @gamedecorator.checkGameconfigEnable('rank')
    def getScoreRushRankList(self, exposed, page):
        gameengine.getLeaderStub(gameconst.LeaderBoardType.AVATAR_SCORE).getScoreRushRankList(self, self.gbID, page)

    def toLeaderBoardAvatarCache(self):
        roleInfo = gameglobal.roleCache.get(self.id, None)
        return LeaderBoardAvatarCacheInfo.LeaderBoardAvatarCacheVal(
            self.gbID,
            roleInfo['name'],
            roleInfo['level'],
            roleInfo['school'],
            self.propChangedTimes.get(gameconst.LeaderBoardType.AVATAR_LEVEL, 0),
            self.guildNameBase,
            self.guildUUIDBase,
            )

    def toLeaderBoardAvatarScore(self):
        roleInfo = gameglobal.roleCache.get(self.id, None)
        return LeaderBoardAvatarScoreInfo.LeaderBoardAvatarScoreVal(
            self.gbID,
            roleInfo['name'],
            self.getTotalScore(),
            self.propChangedTimes.get(gameconst.LeaderBoardType.AVATAR_SCORE, 0),
            roleInfo['level'],
            roleInfo['school'],
            self.guildNameBase,
            self.guildUUIDBase,
            )

    def toLeaderBoardAvatarLevelRushRank(self):
        roleInfo = gameglobal.roleCache.get(self.id, None)
        return LeaderBoardAvatarLevelRushRankInfo.LeaderBoardAvatarLevelRushRankVal(
            self.gbID,
            roleInfo['name'],
            roleInfo['level'],
            roleInfo['school'],
            self.propChangedTimes.get(gameconst.LeaderBoardType.AVATAR_LEVEL, 0),
            self.guildNameBase,
            self.guildUUIDBase,
            self.accountName,
            self.accountEntity.phone,
            )
    
    def toLeaderBoardAvatarAchievement(self):
        roleInfo = gameglobal.roleCache.get(self.id, None)
        return LeaderBoardAvatarAchievementInfo.LeaderBoardAvatarAchievementVal(
            self.gbID,
            roleInfo['name'],
            roleInfo['level'],
            roleInfo['school'],
            self.propChangedTimes.get(gameconst.LeaderBoardType.ACHIEVEMENT, 0),
            self.guildNameBase,
            self.guildUUIDBase,
            self.accountName,
            self.achievementInfo.sumPoint,
            )

    def _updateLeaderBoardAvatar(self):
        if not gameglobal.roleCache.get(self.id, None):
            return
        _level = self.getRoleCacheAttr('level')
        if _level >= R_RD.datas[gameconst.LeaderBoardType.AVATAR_LEVEL]['minLevel']:
            _lbacVal = self.toLeaderBoardAvatarCache()
            gameengine.getLeaderStub(gameconst.LeaderBoardType.AVATAR_LEVEL).onGetLeaderBoardCache(_lbacVal)

        if _level >= R_RD.datas[gameconst.LeaderBoardType.ACHIEVEMENT]['minLevel']:
            if self.achievementInfo.sumPoint > 0:
                _lbacVal = self.toLeaderBoardAvatarAchievement()
                gameengine.getLeaderStub(gameconst.LeaderBoardType.ACHIEVEMENT).onGetLeaderBoardCache(_lbacVal)
        
        _lbacVal = self.toLeaderBoardAvatarLevelRushRank()
        gameengine.getLeaderStub(gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK).onGetLeaderBoardCache(_lbacVal)

    def onLocalServerScoreRankSync(self, rank):
        LOG_INFO("onLocalServerScoreRankSync", rank)
        self.avatarScoreRank = rank
        self.cell.syncAvatarScoreRank(rank)

    def onLeaderBoardRank(self, leaderBoardType, rank):
        if gameconfig.isCrossServer():
            return

        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.LEADER_BOARD,
            actionContext.AchievementCtx(lbType=leaderBoardType, rank=rank))

        if leaderBoardType == gameconst.LeaderBoardType.AVATAR_SCORE:
            self.syncMethodCallToCrossServerBase("onLocalServerScoreRankSync", (rank,))
            self.avatarScoreRank = rank
            self.cell.syncAvatarScoreRank(rank)
        
        self.avatarRankData[leaderBoardType] = rank
