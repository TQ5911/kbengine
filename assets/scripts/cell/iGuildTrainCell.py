#coding=utf-8
from KBEDebug import *
import KBEngine
import gameconst
import dataUtils

import guildTrain_guildTrain as GT_GTD
import formula_generalFormula as F_GFD


class IGuildTrainCell(object):
    def initGuildTrainProps(self):
        trainList = self.popTempMiscProp(gameconst.AvatarProps.guildTrainInitCell, [])
        score = 0
        for trainId, level in trainList:
            gtData = GT_GTD.datas.get(trainId)
            if gtData is None:
                continue

            func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
            if callable(func):
                propName = gtData['fightProp']
                ret = func(level)

                if isinstance(ret, int):
                    propVal = ret
                    scoreTmp = dataUtils.getPropBaseScore(propName) * propVal
                elif isinstance(ret, float):
                    propVal = int(ret)
                    scoreTmp = dataUtils.getPropBaseScore(propName) * propVal
                else:
                    propVal, scoreTmp = ret

                score += scoreTmp
                self.addProp(propName, propVal, gameconst.SourceType.GuildTrain)

        self.setTempMiscProp(gameconst.AvatarProps.guildTrainInitScore, score)

    def updateGuildScoreFromInit(self):
        score = self.popTempMiscProp(gameconst.AvatarProps.guildTrainInitScore, 0)
        self.onUpdateGuildTrainScore(score)

    def onUpgradeTrainLevel(self, trainId, targetLevel, score):
        gtData = GT_GTD.datas[trainId]
        func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
        self.client.onRecordFightProps()

        lastLevel = targetLevel - 1
        if lastLevel:
            curValue = func(lastLevel)
        else:
            curValue = 0
        targetValue = func(targetLevel)
        propName = gtData['fightProp']

        DEBUG_MSG('onUpgradeTrainLevel:', propName, targetValue, curValue, trainId, targetLevel)
        self.addProp(propName, targetValue - curValue, gameconst.SourceType.GuildTrain)

        self.onUpdateGuildTrainScore(score)
        # self.base.showCombatScoreTip()

    def onResetGuildTrain(self, syncDic):
        for trainId, level in syncDic.items():
            gtData = GT_GTD.datas[trainId]
            func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
            propVal = func(level)
            propName = gtData['fightProp']
            self.addProp(propName, -propVal, gameconst.SourceType.GuildTrainReset)

        self.client.onGuildTrainResetClient()
        self.client.onRecordFightProps()
        self.onUpdateGuildTrainScore(0)
        # self.base.showCombatScoreTip()

    def gmAddGuildTrainLevelCell(self, trainId, curLevel, targetLevel):
        gtData = GT_GTD.datas[trainId]
        func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
        if curLevel:
            curVal, _ = func(curLevel)
        else:
            curVal = 0
        targetVal, _ = func(targetLevel)
        propName = gtData['fightProp']
        self.addProp(propName, targetVal - curVal, gameconst.SourceType.GuildTrain)

