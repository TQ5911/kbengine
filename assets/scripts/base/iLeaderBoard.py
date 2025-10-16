# coding: utf-8

import gameconst
import gametimer
import actionContext
import gameengine
import gameglobal
import LeaderBoardAvatarCacheInfo
import LeaderBoardAvatarScoreInfo

import rank_Rank as R_RD
import rank_rankConfig as R_RCD


class ILeaderBoard(object):
    def __init__(self):
        _dur = max(1, R_RCD.datas['refreshCD']['value'] - 5)
        self.pyAddTimer(
            30, # 大概等 score 更新完毕
            _dur,
            gametimer.UPDATE_AVATAR_LEADERBOARD)

    def getLeaderBoardList(self, exposed, leaderBoardType, leaderBoardIdx, school, page):
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

    def _updateLeaderBoardAvatar(self):
        _level = self.getRoleCacheAttr('level')
        if _level >= R_RD.datas[gameconst.LeaderBoardType.AVATAR_LEVEL]['minLevel']:
            _lbacVal = self.toLeaderBoardAvatarCache()
            gameengine.getLeaderStub(gameconst.LeaderBoardType.AVATAR_LEVEL).onGetLeaderBoardCache(_lbacVal)

        if _level >= R_RD.datas[gameconst.LeaderBoardType.AVATAR_SCORE]['minLevel']:
            _lbacVal = self.toLeaderBoardAvatarScore()
            gameengine.getLeaderStub(gameconst.LeaderBoardType.AVATAR_SCORE).onGetLeaderBoardCache(_lbacVal)

    def onLeaderBoardRank(self, leaderBoardType, rank):
        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.LEADER_BOARD,
            actionContext.AchievementCtx(lbType=leaderBoardType, rank=rank))

