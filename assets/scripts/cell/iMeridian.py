# coding: utf-8
from KBEDebug import *

import gameconst
import dataUtils

import prop_fightprop  as  PPROPERTY
import meridian_meridian as  MMD
import meridian_acupoint as MAD

class IMeridian(object):
    """ 
        经脉系统接口
    """
    
    def onMeridianAward(self, propIndexList):
        DEBUG_MSG('onMeridianAward', propIndexList)

        for index in propIndexList:
            config = MMD.datas.get(index, None)
            if config is None:
                config = MAD.datas.get(index, None)
            if config is None:
                continue

            propDict = {}
            needList = [0, self.school]
            for val in needList:
                propKey = 'prop{}'.format(val)
                propList = config.get(propKey, None)
                if propList:
                    for prop in propList:
                        propDict[prop[0]] = prop[1]

            self._addAwardMeridianPropsCell(propDict)

    def _addAwardMeridianPropsCell(self, syncPropDict):
        addScore = 0
        for propName, val in syncPropDict.items():
            self.addProp(propName, val, gameconst.SourceType.MeridianProp)
            addScore += int(round(dataUtils.filterFightPropScore(self.school, propName) * val))
            # DEBUG_MSG('add prop by meridian', propName, ', val', val)

        if addScore:
            newScore = self.scoresInfo.rewardFightProp + addScore
            # DEBUG_MSG('add score by meridian', self.scoresInfo.rewardFightProp, ', val', addScore)
            self.onUpdateRewardFightProp(newScore)