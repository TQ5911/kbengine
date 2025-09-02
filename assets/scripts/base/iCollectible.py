# coding: utf-8
from KBEDebug import *
import KBEngine
import gameconst
import gameclass
import dropAward
import gameengine
import collect_details as  PDETAIL
import prop_fightprop  as  PPROPERTY
import collect_nodes   as  PSCORE
from avatarCollectInfo import collectItem
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

class ICollectible(object):
    def collectOnLogin(self):
        DEBUG_MSG('call collectOnLogin')
        self._refreshProperty()

    def _refreshProperty(self):
        # 每次登录重新计算当前收集项的属性加成
        self.collectScore = {}
        propIndexList = []
        for collectId, collectData in self.collectibleData.collectibleDict.items():
            info = PDETAIL.datas.get(collectId, None)
            if not info:
                continue
            equipment_len = len(info['equipment']) if info['equipment'] else 0
            prop_len = len(info['props']) if info['props'] else 0
            if not collectData.isCompleteAll(equipment_len + prop_len):
                continue
            self.collectScore.setdefault(info['type1'], 0)
            self.collectScore[info['type1']] += info['progress']
            propIndex = info['prop']
            propIndexList.append(propIndex)
        # 重新计算收集分数对应的二次奖励
        for item in PSCORE.datas.values():
            self.collectScore.setdefault(item['type1'], 0)
            if self.collectScore[item['type1']] < item['progress']:
                continue
            propIndex = item['prop']
            propIndexList.append(propIndex)
        self.cell.onCollectAward(propIndexList)
        DEBUG_MSG('call _refreshProperty done', self.collectScore)

    def sendCollectInfo(self):
        # 发送当前属性信息和收集情况
        clientData = []
        for item in self.collectibleData.collectibleDict.values():
            clientData.append(
                item.toSavedDict()
            )
        self.client.onGetCollectInfo(clientData)
        DEBUG_MSG('call sendCollectInfo done', self.collectibleData.collectibleDict.items())

    def reqMark(self, collectID, isMark):
        # 标记收集项高亮显示
        DEBUG_MSG('begin reqMark collectID', collectID, ' isMark', isMark)
        info = PDETAIL.datas.get(collectID, None)
        if not info:
            gameengine.reportCritical('in reqCollect, collectID not exist in table, id :', collectID)
            return
        self.collectibleData.collectibleDict.setdefault(collectID, collectItem(collectID))
        self.collectibleData.collectibleDict[collectID].onMark(isMark)
        self.client.onGetCollectInfo([self.collectibleData.collectibleDict[collectID].toSavedDict()])
        DEBUG_MSG('call reqMark done', self.collectibleData.collectibleDict[collectID].toSavedDict())

    def reqCollect(self, bagType, bagGridID, itemUniqueID, useBind, collectID, collectGridID):
        # 获取收集项的要求
        DEBUG_MSG('begin reqCollect bagType', bagType, ' bagGridID', bagGridID, ' itemUniqueID', itemUniqueID, ' collectID', collectID, ' collectGridID', collectGridID)
        info = PDETAIL.datas.get(collectID, None)
        if not info:
            gameengine.reportCritical('in reqCollect, collectID not exist in table, id :', collectID)
            return
        # 由于策划分表，这里的 equipment + props 两个表共用了一个index (collectGridID)
        equipment_len = len(info['equipment']) if info['equipment'] else 0
        prop_len = len(info['props']) if info['props'] else 0
        propGridID = collectGridID - equipment_len
        if propGridID < 0:
            itemID = info['equipment'][collectGridID][0]
            enhanceLevel =  info['equipment'][collectGridID][1]
        elif propGridID < prop_len:
            itemID = info['props'][propGridID]
            enhanceLevel =  None
        else:
            WARNING_MSG('in reqCollect, propGridID not exist in table, id :', propGridID, ' collectGridID: ', collectGridID)
            return
        self.collectibleData.collectibleDict.setdefault(collectID, collectItem(collectID))
        if self.collectibleData.collectibleDict[collectID].isCompleteAt(collectGridID):
            WARNING_MSG('in reqCollect, already complete ??? id :', itemID, ' itemUniqueID: ', itemUniqueID, ' collectGridID', collectGridID)
            return
        if self.collectibleData.collectibleDict[collectID].isCompleteAll(equipment_len + prop_len):
            WARNING_MSG('in reqCollect, already complete ??? id :', itemID, ' itemUniqueID: ', itemUniqueID)
            return
        # 进行收集，扣除物品
        success = self._completeCollect(bagType, bagGridID, itemID, itemUniqueID, useBind, enhanceLevel)
        if not success:
            WARNING_MSG('in reqCollect, _completeCollect not succeed, bagType', bagType, 'bagGridID', bagGridID, 'itemID', itemID, 'enhanceLevel', enhanceLevel)
            return
        # 更新收集进度
        DEBUG_MSG('before update, collectID ', collectID, ' state ', self.collectibleData.collectibleDict[collectID].state)
        self.collectibleData.collectibleDict[collectID].onComplete(collectGridID)
        if not self.collectibleData.collectibleDict[collectID].isCompleteAll(equipment_len + prop_len):
            DEBUG_MSG('reqCollect not Complete, collectID ', collectID, ' state ', self.collectibleData.collectibleDict[collectID].state)
            self.client.onGetCollectInfo([self.collectibleData.collectibleDict[collectID].toSavedDict()])
            return
        # 获得本次收集项对应的奖励
        collectProp = info['prop']
        # 获得积分
        score = info['progress']
        scoreType = info['type1']
        # 检查积分是否满足升级奖励
        self.collectScore.setdefault(scoreType, 0)
        oldSet = self._findSet(self.collectScore[scoreType], scoreType)
        # 更新积分
        self.collectScore[scoreType] += score
        newSet = self._findSet(self.collectScore[scoreType], scoreType)
        # 获得奖励
        self._onScore(newSet - oldSet, collectProp)
        # 发送进度信息给客户端
        self.client.onGetCollectInfo([self.collectibleData.collectibleDict[collectID].toSavedDict()])
        DEBUG_MSG('reqCollect Complete, collectID ', collectID, ' state ', self.collectibleData.collectibleDict[collectID].state)
        self.triggerAchievement(gameconst.AchieveType.COLLECT)

    def _completeCollect(self, bagType, bagGridID, itemID, itemUniqueID, useBind, enhanceLevel):
        itemCount = 1
        # 检查需要物品itemID是否存在
        bag = self.getBagByType(bagType)
        if not bag:
            WARNING_MSG('in _completeCollect, bag not found, bagType', bagType, 'bagGridID', bagGridID, 'itemID', itemID, 'enhanceLevel', enhanceLevel)
            return False
        if bag.isLocked():
            WARNING_MSG('in _completeCollect, bag is locked, bagType', bagType, 'bagGridID', bagGridID, 'itemID', itemID, 'enhanceLevel', enhanceLevel)
            return False
        # 检查需要物品itemID是否存在
        if bagGridID < 0:
            WARNING_MSG('in _completeCollect, can NOT UseGridItem, bagType', bagType, 'bagGridID', bagGridID, 'itemID', itemID, 'enhanceLevel', enhanceLevel, 'reason',  bag.canUseGridItem(self, bagGridID, itemID, itemCount))
            return False
        deductWealthVal = dropAward.DeductWealthVal()
        # 是否是装备，是否达到了强化的等级
        if enhanceLevel:
            bagEquipItem = self.bagData.getItemObjByGridId(bagGridID)
            if not bagEquipItem:
                WARNING_MSG('     in _completeCollect, item not found:', bagGridID)
                return False
            if bagEquipItem.uniqueId != itemUniqueID:
                WARNING_MSG('     in _completeCollect, uniqueId not matched:', bagEquipItem.uniqueId, 'given ', itemUniqueID)
                return False
            if bagEquipItem.getEnhanceLevel() != enhanceLevel:
                WARNING_MSG('     in _completeCollect, getEnhanceLevel() not matched:', bagEquipItem.getEnhanceLevel(), ' item level', enhanceLevel)
                return False
            # 装备每个格子都只有一个
            if bagEquipItem.itemNum != itemCount:
                WARNING_MSG('     in _completeCollect, bagEquipItem.itemCount() not matched:', bagEquipItem.itemNum, ' itemCount', itemCount)
                return False
            deductWealthVal.addWealthByObjList([bagEquipItem])
        else:
            DEBUG_MSG(' try use item ', itemID, ' itemCount ', itemCount, ' useBind', useBind)
            if useBind == gameconst.ItemBindType.BIND:
                deductWealthVal.addWealthByItemId(itemID, itemCount, gameconst.ItemBindType.BIND)
            elif useBind == gameconst.ItemBindType.NORMAL:
                deductWealthVal.addWealthByItemId(itemID, itemCount, gameconst.ItemBindType.NORMAL)
            else:
                WARNING_MSG('     in _completeCollect, useBind not matched:', useBind)
                return False

        # 扣除物品（要求物品必须一次扣除，不存在扣除一部分的情况）
        if not self.canDeductWealth(deductWealthVal):
            WARNING_MSG('     in _completeCollect, canDeductWealth fail')
            return False
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_COLLECTIBLE
        detail = gameclass.AwardDetail(costItemId=itemID, costItemNum=itemCount)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
        return True

    def _findSet(self, score, scoreType):
        result = set()
        for key, value in PSCORE.datas.items():
            if score >= value['progress'] and scoreType == value['type1']:
                result.add(key)
        return result

    def _onScore(self, awardBox, collectProp):
        propIndexList = [collectProp] if collectProp else []
        for awardID in awardBox:
            item = PSCORE.datas[awardID]
            propIndex = item['prop']
            propIndexList.append(propIndex)

        self.cell.onCollectAward(propIndexList)
        DEBUG_MSG('_onScore, awardBox ', awardBox, ' propList ', propIndexList)


