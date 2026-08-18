# coding: utf-8
from KBEDebug import *
import KBEngine
import gameconst
import gameclass
import dropAward
import gameengine
import gamedecorator
import collect_details as  PDETAIL
from avatarCollectInfo import collectItem
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import LogTrackingMgr
import actionContext

class ICollectible(object):
    def collectOnLogin(self):
        LOG_INFO('call collectOnLogin')
        self._refreshProperty()

    def _refreshProperty(self):
        # 每次登录重新计算当前收集项的属性加成
        propIndexList = []
        for collectId, collectData in self.collectibleData.collectibleDict.items():
            info = PDETAIL.datas.get(collectId, None)
            if not info:
                continue
            if self._checkInUnavailableClass(info, collectId):
                continue
            equipment_len = len(info['equipment']) if info['equipment'] else 0
            prop_len = len(info['props']) if info['props'] else 0
            if not collectData.isCompleteAll(equipment_len + prop_len):
                continue
            propIndex = collectId
            propIndexList.append(propIndex)

        self.cell.onCollectAward(propIndexList, 0)
        LOG_INFO('call _refreshProperty done')

    def sendCollectInfo(self):
        # 发送当前属性信息和收集情况
        clientData = []
        for item in self.collectibleData.collectibleDict.values():
            clientData.append(
                item.toStreamSavedDic()
            )
        self.client.onGetCollectInfo(clientData)
        LOG_INFO('call sendCollectInfo done', self.collectibleData.collectibleDict.items())

    @gamedecorator.checkGameconfigEnable('collection')
    def reqMark(self, exposed, collectID, isMark):
        # 标记收集项高亮显示
        LOG_INFO('begin reqMark collectID', collectID, ' isMark', isMark)
        info = PDETAIL.datas.get(collectID, None)
        if not info:
            gameengine.panicStack('in reqMark, collectID not exist in table, id :', collectID)
            return
        if self._checkInUnavailableClass(info, collectID):
            return

        self.collectibleData.collectibleDict.setdefault(collectID, collectItem(collectID))
        self.collectibleData.collectibleDict[collectID].onMark(isMark)
        self.client.onGetCollectInfo([self.collectibleData.collectibleDict[collectID].toStreamSavedDic()])
        LOG_INFO('call reqMark done', self.collectibleData.collectibleDict[collectID].toStreamSavedDic())

    @gamedecorator.checkGameconfigEnable('collection')
    def reqCollect(self, exposed, bagType, bagGridID, itemUniqueID, useBind, collectID, collectGridID):
        # 获取收集项的要求
        LOG_INFO('begin reqCollect bagType', bagType, ' bagGridID', bagGridID, ' itemUniqueID', itemUniqueID, ' collectID', collectID, ' collectGridID', collectGridID)
        info = PDETAIL.datas.get(collectID, None)
        if not info:
            gameengine.panicStack('in reqCollect, collectID not exist in table, id :', collectID)
            return

        if self._checkInUnavailableClass(info, collectID):
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
            LOG_WARN('in reqCollect, propGridID not exist in table, id :', propGridID, ' collectGridID: ', collectGridID)
            return
        self.collectibleData.collectibleDict.setdefault(collectID, collectItem(collectID))
        if self.collectibleData.collectibleDict[collectID].isCompleteAt(collectGridID):
            LOG_WARN('in reqCollect, already complete ??? id :', itemID, ' itemUniqueID: ', itemUniqueID, ' collectGridID', collectGridID)
            return
        if self.collectibleData.collectibleDict[collectID].isCompleteAll(equipment_len + prop_len):
            LOG_WARN('in reqCollect, already complete ??? id :', itemID, ' itemUniqueID: ', itemUniqueID)
            return
        # 进行收集，扣除物品
        opUUID = KBEngine.genUUID64()
        success = self._completeCollect(bagType, bagGridID, itemID, itemUniqueID, useBind, enhanceLevel, opUUID)
        if not success:
            LOG_WARN('in reqCollect, _completeCollect not succeed, bagType', bagType, 'bagGridID', bagGridID, 'itemID', itemID, 'enhanceLevel', enhanceLevel)
            return
        # 更新收集进度
        LOG_INFO('before update, collectID ', collectID, ' state ', self.collectibleData.collectibleDict[collectID].state)
        self.collectibleData.collectibleDict[collectID].onComplete(collectGridID)
        if not self.collectibleData.collectibleDict[collectID].isCompleteAll(equipment_len + prop_len):
            LOG_INFO('reqCollect not Complete, collectID ', collectID, ' state ', self.collectibleData.collectibleDict[collectID].state)
            self.client.onGetCollectInfo([self.collectibleData.collectibleDict[collectID].toStreamSavedDic()])
            LogTrackingMgr.LogTrackingMgr.collectible_detail(
                self.gbID,
                self.accountEntity.clientDistinctId, 
                collectID,
                "",
                gameconst.CollectibleDetailStatus.COLLECTING,
                opUUID,
            )
            return
        # 获得本次收集项对应的奖励
        collectProp = collectID
        # 获得奖励
        self._onScore(collectProp, opUUID)
        # 发送进度信息给客户端
        self.client.onGetCollectInfo([self.collectibleData.collectibleDict[collectID].toStreamSavedDic()])
        LOG_INFO('reqCollect Complete, collectID ', collectID, ' state ', self.collectibleData.collectibleDict[collectID].state)

        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.COLLECT,
            actionContext.AchievementCtx()
        )

    def _completeCollect(self, bagType, bagGridID, itemID, itemUniqueID, useBind, enhanceLevel, opUUID):
        itemCount = 1
        # 检查需要物品itemID是否存在
        bag = self.getBagByType(bagType)
        if not bag:
            LOG_WARN('in _completeCollect, bag not found, bagType', bagType, 'bagGridID', bagGridID, 'itemID', itemID, 'enhanceLevel', enhanceLevel)
            return False
        if bag.isLocked():
            LOG_WARN('in _completeCollect, bag is locked, bagType', bagType, 'bagGridID', bagGridID, 'itemID', itemID, 'enhanceLevel', enhanceLevel)
            return False
        # 检查需要物品itemID是否存在
        if bagGridID < 0:
            LOG_WARN('in _completeCollect, can NOT UseGridItem, bagType', bagType, 'bagGridID', bagGridID, 'itemID', itemID, 'enhanceLevel', enhanceLevel, 'reason',  bag.canUseGridItem(self, bagGridID, itemID, itemCount))
            return False
        deductWealthVal = dropAward.DeductWealthVal()
        # 是否是装备，是否达到了强化的等级
        bagItem = bag.getItemObjByGridId(bagGridID)
        if not bagItem:
            LOG_WARN('     in _completeCollect, item not found:', bagGridID)
            return False

        if bagItem.uniqueId != itemUniqueID:
            LOG_WARN('     in _completeCollect, uniqueId not matched:', bagItem.uniqueId, 'given ', itemUniqueID)
            return False

        if bagItem.isLocked():
            LOG_WARN('     in _completeCollect, item is locked:', bagGridID)
            return False

        if bagItem.isEquipmentItem():
            if not bagItem.isGood(self.gbID):
                LOG_WARN('     in _completeCollect, item is not good:', bagGridID)
                return False

            if enhanceLevel is None:
                LOG_WARN('     in _completeCollect, item level is none:', bagGridID)
                return False

            if bagItem.getEnhanceLevel() != enhanceLevel:
                LOG_WARN('     in _completeCollect, getEnhanceLevel() not matched:', bagItem.getEnhanceLevel(), ' item level', enhanceLevel)
                return False
            # 装备每个格子都只有一个
            if bagItem.itemNum != itemCount:
                LOG_WARN('     in _completeCollect, bagItem.itemCount() not matched:', bagItem.itemNum, ' itemCount', itemCount)
                return False
            deductWealthVal.addWealthByObjList([bagItem])
        else:
            LOG_INFO(' try use item ', itemID, ' itemCount ', itemCount, ' useBind', useBind)
            if useBind == gameconst.ItemBindType.BIND:
                deductWealthVal.addWealthByItemId(itemID, itemCount, gameconst.ItemBindType.BIND)
            elif useBind == gameconst.ItemBindType.NORMAL:
                deductWealthVal.addWealthByItemId(itemID, itemCount, gameconst.ItemBindType.NORMAL)
            else:
                LOG_WARN('     in _completeCollect, useBind not matched:', useBind)
                return False

        # 扣除物品（要求物品必须一次扣除，不存在扣除一部分的情况）
        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_WARN('     in _completeCollect, canDeductWealth fail', res())
            return False
        srcType = AAC_AACDD.datas.BONUS_SRC_COLLECTIBLE
        detail = gameclass.AwardDetailCls(costItemId=itemID, costItemNum=itemCount)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)
        return True

    def _onScore(self, collectProp, opUUID):
        propIndexList = [collectProp] if collectProp else []

        self.cell.onCollectAward(propIndexList, opUUID)
        LOG_INFO('_onScore propList ', propIndexList)


    def _checkInUnavailableClass(self, info, collectID):
        unavailableClass = info.get('unavailableClass', [])
        if not unavailableClass:
            return False
        school = self.getAvatarSchool()
        if school in unavailableClass:
            LOG_WARN('in _checkInUnavailableClass, school in unavailableClass:', collectID, school, unavailableClass)
            return True

        return False
