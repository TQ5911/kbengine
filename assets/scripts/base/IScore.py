# coding: utf-8
from KBEDebug import *
import KBEngine

import math
import gameengine
import gameconst
import gametimer
import gameglobal
import utils


import const_const as CONST
import formula_generalFormula as FML_G
import skillRelevant_skillScore as SKILL_PP
import character_charData as CHAR_CD
import actionContext
import rank_Rank as R_RD



class IScore(object):

    def initAvatarBaseScores(self):
        LOG_DBG('initAvatarBaseScores')
        data = {'mount': math.floor(self.getTotalMountScore()),
                'pet': math.floor(self.getTotalPetScore()),
                'skill': math.floor(self.getTotalSkillScore())}
        self.cell.onInitAvatarBaseScores(data)
    # --------------------------------------------------------------
    # SCORE CALC.

    def getTotalSkillScore(self):
        skillScore = 0
        school = self.getAvatarSchool()
        for skillId, skillLv in self.buildDic.skillLevels.items():
            LOG_DBG('getTotalSkillScore', skillId, skillLv)
            if skillId in CHAR_CD.datas[school]['build']:
                skillScore += SKILL_PP.datas[skillLv]['score']

            elif utils.hasSkillTagById(skillId, gameconst.SkillTagEnum.UltraSkill):
                skillScore += SKILL_PP.datas[skillLv]['score2']
                
        LOG_DBG('getTotalSkillScore ', skillScore)
        return skillScore
    # --------------------------------------------------------------

    # --------------------------------------------------------------
    # UPDATE FUNC

    def getTotalScore(self):
        return self.baseScoreInfo.totalScore
    
    def baseScoreChanged(self, scoreInitFinished, scoreKey, scoreVal):
        self.baseScoreInfo.updateScore(scoreKey, scoreVal)
        totalScore = self.getTotalScore()
        self.updateScoreToRedis(totalScore)

        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.SCORE,
            actionContext.AchievementCtx())

        if not scoreInitFinished:
            return

        self.guildBox and self.guildBox.onGuildMemberPropUpdate(self.gbID, 'score', totalScore)
        self.propChangedTimes[gameconst.LeaderBoardType.AVATAR_SCORE] = utils.curTS()
        self._schedulePushScoreToLeaderBoard()

    def _schedulePushScoreToLeaderBoard(self):
        """战力变动即推送战力榜，0.1s 防抖合并，任意时刻至多一个待执行推送"""
        if getattr(self, '_scoreLBPushTimerId', 0):
            return
        self._scoreLBPushTimerId = self.addTimerCB(
            0.1, '_pushScoreToLeaderBoard', (),
            gametimer.TIMER_TAG_PUSH_SCORE_TO_LEADERBOARD,
            varTimerID='_scoreLBPushTimerId'
        )

    def _pushScoreToLeaderBoard(self):
        LOG_DBG('_pushScoreToLeaderBoard')
        if not gameglobal.roleCache.get(self.id, None):
            return
        _level = self.getRoleCacheAttr('level')
        if _level >= R_RD.datas[gameconst.LeaderBoardType.AVATAR_SCORE]['minLevel']:
            gameengine.getLeaderStub(gameconst.LeaderBoardType.AVATAR_SCORE).onGetLeaderBoardCache(self.toLeaderBoardAvatarScore())

    def onAllScoreInitFinished(self):
        self.commonFlagBase = utils.bset(self.commonFlagBase, gameconst.BASE_COMMON_FLAG_INIT_SCORE)

    def _offlineNotifyScore(self):
        totalScore = self.getTotalScore()
        self.updateScoreToRedis(totalScore)

    def updateScoreToRedis(self, battleEffect):
        self._modifyRedisAttr({
            'battleEffect': battleEffect
        })

    def updateMountScore(self):
        newScore = math.floor(self.getTotalMountScore())
        self.cell.onUpdateMountScore(newScore)

    def updatePetScore(self):
        newScore = math.floor(self.getTotalPetScore())
        self.cell.onUpdatePetScore(newScore)

    def updateSkillScore(self):
        newScore = math.floor(self.getTotalSkillScore())
        LOG_DBG('updateSkillScore ', newScore)
        self.cell.onUpdateSkillScore(newScore)
    # --------------------------------------------------------------
