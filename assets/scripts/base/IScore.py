# coding: utf-8
from KBEDebug import *
import KBEngine

import math
import gameengine
import gameconst
import gametimer
import utils


import const_const as CONST
import formula_generalFormula as FML_G
import skillRelevant_skillScore as SKILL_PP
import character_charData as CHAR_CD
import gametlog
import actionContext



class IScore(object):

    def initAvatarBaseScores(self):
        DEBUG_MSG('initAvatarBaseScores')
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
            if skillId in CHAR_CD.datas[school]['build']:
                skillScore += SKILL_PP.datas[skillLv]['score']

            elif utils.hasSkillTag(skillId, gameconst.SkillTag.UltraSkill):
                skillScore += SKILL_PP.datas[skillLv]['score2']

        return skillScore
    # --------------------------------------------------------------

    # --------------------------------------------------------------
    # UPDATE FUNC

    def getTotalScore(self):
        return self.baseScoreInfo.totalScore

    def baseScoreChanged(self, scoreInitFinished, scoreKey, scoreVal):
        oldTotalScore = self.getTotalScore()
        oldScoreVal = getattr(self.baseScoreInfo, scoreKey)
        self.baseScoreInfo.updateScore(scoreKey, scoreVal)
        totalScore = self.getTotalScore()
        self.updateScoreToRedis(totalScore)

        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.SCORE,
            actionContext.AchievementCtx())

        if not scoreInitFinished:
            return

        if not self.updateScoreTimerId:
            self._notifyScoreChange()

        self.guildBox and self.guildBox.onGuildMemberPropUpdate(self.gbID, 'score', totalScore)
        self.propChangedTimes[gameconst.LeaderBoardType.AVATAR_SCORE] = utils.getNow()


    def _notifyScoreChange(self):
        self.updateScoreTimerId = 0
        now = utils.getNow()

        if self.lastNotifyScoreTime + 55 > now:
            self.updateScoreTimerId = self._callback(
                self.lastNotifyScoreTime + 60 - now,
                '_notifyScoreChange',
                (),
                gametimer.TIMER_TAG_UPDATE_SCORE
            )
            return
        # if self.guildBoxBase:
        #     self.guildBoxBase.onUpdateAttrAndDiffNotify(self.gbID, {
        #         'battleEffect': totalScore
        #     })

        self.lastNotifyScoreTime = now

    def _offlineNotifyScore(self):
        if not self.updateScoreTimerId:
            return

        self._cancelCallback(self.updateScoreTimerId, gametimer.TIMER_TAG_UPDATE_SCORE)
        self.updateScoreTimerId = 0

        totalScore = self.getTotalScore()
        self.updateScoreToRedis(totalScore)
        # if self.guildBoxBase:
        #     self.guildBoxBase.onUpdateAttrAndDiffNotify(self.gbID, {
        #         'battleEffect': totalScore
        #     })
        self.lastNotifyScoreTime = utils.getNow()

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
        self.cell.onUpdateSkillScore(newScore)
    # --------------------------------------------------------------
