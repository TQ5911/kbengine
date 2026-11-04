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

    def onUpgradeTrainLevel(self, trainId, targetLevel, score, opUUID):
        gtData = GT_GTD.datas[trainId]
        func = F_GFD.datas[gtData['valueFormula']]['serverFormula']

        lastLevel = targetLevel - 1
        if lastLevel:
            curValue = func(lastLevel)
        else:
            curValue = 0
        targetValue = func(targetLevel)
        propName = gtData['fightProp']

        LOG_INFO('onUpgradeTrainLevel:', propName, targetValue, curValue, trainId, targetLevel, score)
        self.addProp(propName, targetValue - curValue, gameconst.SourceType.SrcTpGuildTrain)
        self.onUpdateGuildTrainScore(score, opUUID)

    def onResetGuildTrain(self, syncDic, opUUID = 0):
        for trainId, level in syncDic.items():
            gtData = GT_GTD.datas[trainId]
            func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
            propVal = func(level)
            propName = gtData['fightProp']
            self.addProp(propName, -propVal, gameconst.SourceType.SrcTpGuildTrainReset)

        self.client.onGuildTrainResetClient()
        self.onUpdateGuildTrainScore(0, opUUID)

    def gmAddGuildTrainLevelCell(self, trainId, curLevel, targetLevel):
        gtData = GT_GTD.datas[trainId]
        _func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
        if curLevel:
            curVal, _ = _func(curLevel)
        else:
            curVal = 0
        _targetVal, _ = _func(targetLevel)
        propName = gtData['fightProp']
        self.addProp(propName, _targetVal - curVal, gameconst.SourceType.SrcTpGuildTrain)

    def _calcGuildTrainPropVal(self, func, level):
        """按等级取修炼属性值, 兼容公式返回标量(int/float)与二元组(propVal, score)两种形式。"""
        if not level:
            return 0
        ret = func(level)
        if isinstance(ret, (int, float)):
            return ret
        return ret[0]

    def gmSetGuildTrainLevelCell(self, trainId, curLevel, targetLevel):
        """GM 直设修炼等级(支持降级, delta 可为负)。"""
        gtData = GT_GTD.datas[trainId]
        _func = F_GFD.datas[gtData['valueFormula']]['serverFormula']
        propName = gtData['fightProp']
        curVal = self._calcGuildTrainPropVal(_func, curLevel)
        targetVal = self._calcGuildTrainPropVal(_func, targetLevel)
        LOG_INFO('gmSetGuildTrainLevelCell:', propName, curVal, targetVal, trainId, curLevel, targetLevel)
        self.addProp(propName, targetVal - curVal, gameconst.SourceType.SrcTpGuildTrain)

