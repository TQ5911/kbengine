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
        LOG_DBG('onCollectAward', propIndexList, opUUID)
        syncPropDict = {}
        for propIndex in propIndexList:
            propList = PDETAIL.datas.get(propIndex, {}).get('propList', {})
            for propName, val in propList.items():
                syncPropDict[propName] = syncPropDict.get(propName, 0) + val
            coType = PDETAIL.datas.get(propIndex, {}).get('type', '')
            self.collectibleSimpleClientData.setdefault(coType, {}).setdefault(propIndex, True)

        propChange = self._addAwardCollectPropsCell(syncPropDict, opUUID)
        if opUUID:
            LogTrackingMgr.LogTrackingMgr.collectible_detail(
                self.gbId,
                self.clientDistinctIdCell,
                propIndex,
                propChange,
                gameconst.CollectibleDetailStatus.COLLECTED,
                opUUID,
            )

    def _addAwardCollectPropsCell(self, syncPropDict, opUUID):
        addScore = 0
        propChange = {}
        for propName, val in syncPropDict.items():
            bef = self.getProp(propName)
            self.addProp(propName, val, gameconst.SourceType.SrcTpCollectProp)
            addScore += dataUtils.calcFightPropScore(self.school, propName, val)
            aft = self.getProp(propName)
            propChange[propName] = {'bef': bef, 'aft': aft}
            LOG_DBG('add prop by collect', propName, ', val', val)

        if addScore:
            newScore = self.scoresInfo.rewardFightProp + addScore
            LOG_DBG('add score by collect', self.scoresInfo.rewardFightProp, ', val', addScore)
            self.onUpdateRewardFightProp(newScore, opUUID)

        return propChange
