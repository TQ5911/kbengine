# coding: utf-8
from KBEDebug import *
import KBEngine

import prop_fightprop  as  PPROPERTY
from avatarCollectInfo import collectItem
import gameconst
import fightProp_define as FPDD



class ICollectible(object):
    def onCollectAward(self, propIndexList):
        DEBUG_MSG('onCollectAward', propIndexList)
        for propIndex in propIndexList:
            propList = PPROPERTY.datas.get(propIndex, {}).get('propList', {})
            self._addAwardCollectPropsCell(propList)

    def _addAwardCollectPropsCell(self, syncPropDict):
        addScore = 0
        for propName, val in syncPropDict.items():
            self.addProp(propName, val, gameconst.SourceType.CollectProp)
            addScore += int(round(FPDD.datas[propName]['perPropertyScore'] * val))
            DEBUG_MSG('add prop by collect', propName, ', val', val)

        if addScore:
            newScore = self.scoresInfo.rewardFightProp + addScore
            DEBUG_MSG('add score by collect', self.scoresInfo.rewardFightProp, ', val', addScore)
            self.onUpdateRewardFightProp(newScore)