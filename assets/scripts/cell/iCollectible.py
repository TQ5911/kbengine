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

    def gmRemoveCollectAward(self, propIndexList, opUUID):
        # GM回退收集: 按propList负向回收战斗属性(rewardFightProp为共享评分桶, 只能差量回退), 并清除客户端冗余标记
        LOG_INFO('gmRemoveCollectAward', propIndexList, opUUID)
        syncPropDict = {}
        simpleDataChanged = False
        for propIndex in propIndexList:
            info = PDETAIL.datas.get(propIndex, None)
            if not info:
                continue
            propList = info.get('propList', {})
            for propName, val in propList.items():
                syncPropDict[propName] = syncPropDict.get(propName, 0) + val
            coType = info.get('type', '')
            if coType in self.collectibleSimpleClientData and \
                    propIndex in self.collectibleSimpleClientData[coType]:
                self.collectibleSimpleClientData[coType].pop(propIndex)
                simpleDataChanged = True

        removeScore = 0
        for propName, val in syncPropDict.items():
            self.addProp(propName, -val, gameconst.SourceType.SrcTpCollectProp)
            removeScore += dataUtils.calcFightPropScore(self.school, propName, val)
            LOG_DBG('remove prop by collect', propName, ', val', val)

        if removeScore:
            newScore = self.scoresInfo.rewardFightProp - removeScore
            LOG_DBG('remove score by collect', self.scoresInfo.rewardFightProp, ', val', removeScore)
            self.onUpdateRewardFightProp(newScore, opUUID)

        if simpleDataChanged:
            # PY_DICT嵌套修改后重赋值以触发持久化
            self.collectibleSimpleClientData = self.collectibleSimpleClientData
