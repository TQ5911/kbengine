#coding=utf-8
from KBEDebug import *
import KBEngine
import gameconst
import dataUtils

import guildTrain_guildTrain as GT_GTD
import formula_generalFormula as F_GFD


class IGuildTrainCell(object):
    def initGuildTrainProps(self):
        trainList = self.popTempMiscProp(gameconst.EntityPropsEnum.guildTrainInitCell, [])
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
                    scoreTmp = dataUtils.calcFightPropScore(self.school, propName, propVal)
                elif isinstance(ret, float):
                    propVal = ret
                    scoreTmp = dataUtils.calcFightPropScore(self.school, propName, propVal)
                else:
                    propVal, scoreTmp = ret

                score += scoreTmp
                self.addProp(propName, propVal, gameconst.SourceType.SrcTpGuildTrain)

        self.setTempMiscProp(gameconst.EntityPropsEnum.guildTrainInitScore, score)

    def updateGuildScoreFromInit(self):
        score = self.popTempMiscProp(gameconst.EntityPropsEnum.guildTrainInitScore, 0)
        self.onUpdateGuildTrainScore(score)

    def onUpgradeTrainLevel(self, trainId, targetLevel, score):
        gtData = GT_GTD.datas[trainId]
        func = F_GFD.datas[gtData['valueFormula']]['serverFormula']

        lastLevel = targetLevel - 1
        if lastLevel:
            curValue = func(lastLevel)
        else:
            curValue = 0
        targetValue = func(targetLevel)
        propName = gtData['fightProp']

        LOG_IFO('onUpgradeTrainLevel:', propName, targetValue, curValue, trainId, targetLevel, score)
        self.addProp(propName, targetValue - curValue, gameconst.SourceType.SrcTpGuildTrain)
        self.onUpdateGuildTrainScore(score)

    def onResetGuildTrain(self, syncDic):
        for trainId, level in syncDic.items():
            gtData = GT_GTD.datas[trainId]
            func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
            propVal = func(level)
            propName = gtData['fightProp']
            self.addProp(propName, -propVal, gameconst.SourceType.SrcTpGuildTrainReset)

        self.client.onGuildTrainResetClient()
        self.onUpdateGuildTrainScore(0)

    def gmAddGuildTrainLevelCell(self, trainId, curLevel, targetLevel):
        gtData = GT_GTD.datas[trainId]
        func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
        if curLevel:
            curVal, _ = func(curLevel)
        else:
            curVal = 0
        targetVal, _ = func(targetLevel)
        propName = gtData['fightProp']
        self.addProp(propName, targetVal - curVal, gameconst.SourceType.SrcTpGuildTrain)

