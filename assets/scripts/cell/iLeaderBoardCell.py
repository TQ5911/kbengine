# coding=utf-8

import gameconst
import gametimer
import utils
import gameengine
import gameglobal
import LeaderBoardAvatarCacheInfo
import LeaderBoardAvatarScoreInfo
import LeaderBoardAvatarLevelRushRankInfo

import rank_rankConfig as R_RCD
import rank_Rank as R_RD


class ILeaderBoardCell(object):
    def __init__(self):
        pass
        # _dur = max(1, R_RCD.datas['refreshCD']['value'] - 5)
        # self.pyAddTimer(
        #     10, # 大概等 score 更新完毕
        #     _dur,
        #     gametimer.UPDATE_AVATAR_LEADERBOARD)

