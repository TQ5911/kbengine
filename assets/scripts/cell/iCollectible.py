# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst
import dataUtils
import LogTrackingMgr
import json

import prop_fightprop  as  PPROPERTY
import collect_details as  PDETAIL

class ICollectible(object):
    def onCollectAward(self, propIndexList, opUUID):
        DEBUG_MSG('onCollectAward', propIndexList, opUUID)
        for propIndex in propIndexList:
            propList = PDETAIL.datas.get(propIndex, {}).get('propList', {})
            propChange = self._addAwardCollectPropsCell(propList)
            if not opUUID:
                continue
            LogTrackingMgr.LogTrackingMgr.Collectible_Detail(
                self.gbId,
                propIndex,
                gameconst.CollectibleDetailStatus.COLLECTED,
                propChange,
                opUUID,
            )

    def _addAwardCollectPropsCell(self, syncPropDict):
        addScore = 0
        propChange = {}
        for propName, val in syncPropDict.items():
            bef = self.getProp(propName)
            self.addProp(propName, val, gameconst.SourceType.CollectProp)
            addScore += dataUtils.calcFightPropScore(self.school, propName, val)
            aft = self.getProp(propName)
            propChange[propName] = {'bef': bef, 'aft': aft}
            DEBUG_MSG('add prop by collect', propName, ', val', val)

        if addScore:
            newScore = self.scoresInfo.rewardFightProp + addScore
            DEBUG_MSG('add score by collect', self.scoresInfo.rewardFightProp, ', val', addScore)
            self.onUpdateRewardFightProp(newScore)

        return propChange
