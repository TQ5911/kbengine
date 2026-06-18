# coding: utf-8
from KBEDebug import *

import math

import gameconst
import dataUtils

import AvatarScores
import gameengine

import fightProp_define as FPD

class IScore(object):
    """ score AIO """

    def __init__(self):
        # init score
        self.initAvatarScores()

    def initAvatarScores(self):
        LOG_INFO('initAvatarScores')
        self.scoreInitFinished = False
        self.totalScore = 0
        m_dict = {i: False for i in AvatarScores.AvatarScores.__attrs__}
        self.setTempMiscProp(gameconst.EntityPropsEnum.avatarScoresInitChecklist, m_dict)
        self._initAvatarCellScores()
        self.base.initAvatarBaseScores()
        self.asyncCallbackAfter(10).checkInitScoreTimeout()

    def _initAvatarCellScores(self):
        self.updateSelfLevelScore()
        self.updateEquipmentScore()
        self.updateAwardFightPropScore()
        self.updateGuildScoreFromInit()

    def onInitAvatarBaseScores(self, data):
        LOG_INFO('onInitAvatarBaseScores::', data)
        data = data or {}
        for k, v in data.items():
            self._changeScore(k, v)

    def checkInitScoreTimeout(self):
        if self.scoreInitFinished:
            return
        gameengine.panicStack('checkInitScoreTimeout:', self.getTempMiscProp(gameconst.EntityPropsEnum.avatarScoresInitChecklist))
        self.scoreInitFinished = True
        self.onAllAvatarScoreBeInited(timeout=True)

    def onAllAvatarScoreBeInited(self, timeout=False):
        LOG_INFO("onAllAvatarScoreBeInited, timeout:", timeout)
        self.scoreInitFinished = True
        self.popTempMiscProp(gameconst.EntityPropsEnum.avatarScoresInitChecklist)
        self.client.onAvatarTotalScoreInitCompleted()

    def markAvatarScoreBeInited(self, key):
        if self.scoreInitFinished:
            return
        m_avatarScoresInitChecklist = self.getTempMiscProp(gameconst.EntityPropsEnum.avatarScoresInitChecklist)
        if not m_avatarScoresInitChecklist:
            gameengine.panicStack('markAvatarScoreBeInited, no avatarScoresInitChecklist cache')
            return
        if key not in m_avatarScoresInitChecklist:
            LOG_ERR("markAvatarScoreBeInited:: un-known key", key)
            return
        LOG_INFO('markAvatarScoreBeInited, score has init:', key)
        m_avatarScoresInitChecklist[key] = True
        if not all(m_avatarScoresInitChecklist.values()):
            return
        # 战力全部初始化完成
        self.onAllAvatarScoreBeInited()

    def getTotalScore(self):
        return self.scoresInfo.totalScore

    # --------------------------------------------------------------
    # SCORE CALC.
    def getSelfLevelScore(self):
        changeAffactProp = FPD.datas['level']['changeAffactProp']
        score = 0
        for propName in changeAffactProp.split(';'):
            propValue = getattr(self, propName)
            if propValue > 0:
                score += dataUtils.calcFightPropScore(self.school, propName, propValue)
        return score

    def getTotalEquipmentsScore(self):
        totalScore = 0
        for equipObj in self.bodyEquipData.equips_map.values():
            totalScore += equipObj.getEquipScore()
        
        for attrName, attrValue in self.bodyEquipData.blessAttrs.items():
            totalScore += dataUtils.calcFightPropScore(self.school, attrName, attrValue)
        return totalScore

    # --------------------------------------------------------------

    # --------------------------------------------------------------
    # UPDATE FUNC

    def _changeScore(self, key, val):
        oldTotalScore = self.totalScore
        setattr(self.scoresInfo, key, val)
        # 每次重新计算祝福评分
        oldBlessScore = self.scoresInfo.bless
        blessScore = dataUtils.calcAvatarBlessScore(self)
        blessScore = math.floor(blessScore)
        if blessScore >= 0 and blessScore != oldBlessScore:
            setattr(self.scoresInfo, 'bless', blessScore)
            self.base.baseScoreChanged(self.scoreInitFinished, 'bless', blessScore)
        
        self.scoresInfo = self.scoresInfo
        self.totalScore = self.getTotalScore()
        if oldTotalScore != self.totalScore:
            self.base.baseScoreChanged(self.scoreInitFinished, key, val)
        self.markAvatarScoreBeInited(key)

    def _onScoreChange(self):
        pass

    def updateSelfLevelScore(self):
        self._changeScore("level", math.floor(self.getSelfLevelScore()))
        self._onScoreChange()

    def updateEquipmentScore(self):
        self._changeScore("equipments", math.floor(self.getTotalEquipmentsScore()))
        self._onScoreChange()
        self.syncBodyEquipDressData()

    def onUpdateRewardFightProp(self, newScore):
        self._changeScore("rewardFightProp", math.floor(newScore))
        self._onScoreChange()

    def onUpdateMountScore(self, newScore):
        self._changeScore("mount", math.floor(newScore))
        self._onScoreChange()

    def onUpdatePetScore(self, newScore):
        self._changeScore("pet", math.floor(newScore))
        self._onScoreChange()

    def onUpdateSkillScore(self, newScore):
        self._changeScore("skill", math.floor(newScore))
        self._onScoreChange()

    def onUpdateGuildTrainScore(self, newScore):
        self._changeScore("guildtrain", math.floor(newScore))
        self._onScoreChange()

    def onUpdateMeridianScore(self, newScore):
        self._changeScore("meridian", math.floor(newScore))
        self._onScoreChange()
    # --------------------------------------------------------------

    # --------------------------------------------------------------
    # GM

#     def gmTotalScoreDebugMsg(self):
#         s = self.scoresInfo
#         _msg = ''' --- 玩家评分 ---
# 装备: {0}
# 等级: {1}
# 怪物图鉴: {2}
# 万象法阵: {3}
# 小世界怪物: {4}
# 小世界建筑: {5}
# 小世界气数: {6}
# 帮会修炼: {7}
# 灵兽: {8}
# 技能点: {9}
# 魂卡点: {10}
# 总分: {11}
# '''.format(s.equipments, s.level, s.monstermanual, s.wanxiang, s.homecreep, s.homebuilding,
#            s.homeqishu, s.guildtrain, s.lingshou, s.skillpoints, s.soulCards, s.totalScore)
#
#         _info = utils.buildChatChannelAvatarData(
#             self.id, self.gbId, self.school, self.name, self.level, self.sex, self.appearance.outfitData.picFrameId)
#
#         import gameengine
#         gameengine.broadcastBaseapp('onBroadcastToAllClients',
#                                         ('onRecvAvatarChannelMsg',
#                                          (gameconst.ChatChannelEnum.WORLD, _info, _msg), ()))

