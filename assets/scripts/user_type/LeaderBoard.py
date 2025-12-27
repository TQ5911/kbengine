import gameconst
import LeaderBoardAvatarCacheInfo
import LeaderBoardAvatarScoreInfo
import LeaderBoardGuildInfo
import LeaderBoardAvatarLevelRushRankInfo

TypeToDic = {
    gameconst.LeaderBoardType.AVATAR_LEVEL: LeaderBoardAvatarCacheInfo.LeaderBoardAvatarCacheVal,
    gameconst.LeaderBoardType.AVATAR_SCORE: LeaderBoardAvatarScoreInfo.LeaderBoardAvatarScoreVal,
    gameconst.LeaderBoardType.GUILD: LeaderBoardGuildInfo.LeaderBoardGuildVal,
    gameconst.LeaderBoardType.AVATAR_LEVEL_RUSH_RANK: LeaderBoardAvatarLevelRushRankInfo.LeaderBoardAvatarLevelRushRankVal,
}
