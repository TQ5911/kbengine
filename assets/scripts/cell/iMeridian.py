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
    
    def onMeridianAward(self, propIndexList, opUUID = 0):
        LOG_DBG('onMeridianAward', propIndexList, opUUID)

        propDict = {}
        for index in propIndexList:
            config = MMD.datas.get(index, None)
            if config is None:
                config = MAD.datas.get(index, None)
            if config is None:
                continue

            needList = [0, self.school]
            for val in needList:
                propKey = 'prop{}'.format(val)
                propList = config.get(propKey, None)
                if propList:
                    for prop in propList:
                        propDict.setdefault(prop[0], 0)
                        propDict[prop[0]] += prop[1]

        self._addAwardMeridianPropsCell(propDict, opUUID)

    def _addAwardMeridianPropsCell(self, syncPropDict, opUUID):
        addScore = 0
        for propName, val in syncPropDict.items():
            self.addProp(propName, val, gameconst.SourceType.SrcTpMeridianProp)
            addScore += dataUtils.calcFightPropScore(self.school, propName, val)
            # LOG_DBG('add prop by meridian', propName, ', val', val)

        newScore = self.scoresInfo.meridian + addScore
        LOG_DBG('add score by meridian', self.scoresInfo.meridian, ', val', addScore)
        self.onUpdateMeridianScore(newScore, opUUID)