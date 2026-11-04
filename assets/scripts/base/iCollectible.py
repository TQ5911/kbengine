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
import collect_equipIndex as CEIDX
import character_charData as CCDATA

class ICollectible(object):
    def collectOnLogin(self):
        LOG_INFO('call collectOnLogin')
        self._refreshProperty()
        if not self.hasPersistentMiscProp(gameconst.EntityPropsEnum.completeCollectNum):
            _collectNum = 0
            for _achieveId in self.achievementInfo.typeDic.get(gameconst.AchieveType.COLLECT, ()):
                _achieveVal = self.achievementInfo.achieveDic.get(_achieveId)
                if _achieveVal and _achieveVal.step > _collectNum:
                    _collectNum = _achieveVal.step
            self.setPersistentMiscProp(gameconst.EntityPropsEnum.completeCollectNum, _collectNum)

    def _refreshProperty(self):
        # 每次登录重新计算当前收集项的属性加成
        propIndexList = []
        for collectId, collectData in self.collectibleData.collectibleDict.items():
            info = PDETAIL.datas.get(collectId, None)
            if not info:
                continue
            if self._checkInUnavailableClass(info, collectId):
                continue
            equipment_len = len(info['equip']) if info['equip'] else 0
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

        schoolIdx = 0
        if self.getAvatarSchool() not in CCDATA.allSchoolList:
            LOG_ERR('in reqCollect, school not exist in table, school :', self.getAvatarSchool())
            return

        schoolIdx = CCDATA.allSchoolList.index(self.getAvatarSchool())
        # 由于策划分表，这里的 equip + props 两个表共用了一个index (collectGridID)
        equipment_len = len(info['equip']) if info['equip'] else 0
        prop_len = len(info['props']) if info['props'] else 0
        propGridID = collectGridID - equipment_len
        if propGridID < 0:
            indexId = info['equip'][collectGridID]
            equipInfo = CEIDX.datas.get(indexId, None)
            if not equipInfo:
                LOG_ERR('in reqCollect, indexId not exist in table, id :', propGridID, ' collectGridID: ', collectGridID)
                return
            if schoolIdx >= len(equipInfo['propList']):
                LOG_ERR('in reqCollect, school not exist in table, id :', propGridID, ' collectGridID: ', collectGridID, ' schoolIdx: ', schoolIdx)
                return
            itemID = equipInfo['propList'][schoolIdx]
            enhanceLevel = info['equipLevel'][collectGridID]
            gradeLevel = info['equipGrade'][collectGridID]
        elif propGridID < prop_len:
            itemID = info['props'][propGridID]
            enhanceLevel =  None
            gradeLevel = None
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
        success = self._completeCollect(bagType, bagGridID, itemID, itemUniqueID, useBind, enhanceLevel, gradeLevel, opUUID)
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

        _collectNum = self.getPersistentMiscProp(gameconst.EntityPropsEnum.completeCollectNum, 0) + 1
        self.setPersistentMiscProp(gameconst.EntityPropsEnum.completeCollectNum, _collectNum)
        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.COLLECT,
            actionContext.AchievementCtx()
        )

        # 完成了某个品质的收集
        self.beginnerJourney_onTaskEvent(
            gameconst.BjTaskType.BJ_TASK_TYPE_COLLECTION_STAT,
            delta=1, quality=info['type'])

        # 发送进度信息给客户端
        self.client.onGetCollectInfo([self.collectibleData.collectibleDict[collectID].toStreamSavedDic()])
        LOG_INFO('reqCollect Complete, collectID ', collectID, ' state ', self.collectibleData.collectibleDict[collectID].state)

    def _completeCollect(self, bagType, bagGridID, itemID, itemUniqueID, useBind, enhanceLevel, gradeLevel, opUUID):
        LOG_INFO('in _completeCollect ', bagType, bagGridID, itemID, itemUniqueID, useBind, enhanceLevel, gradeLevel, opUUID)
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

            if gradeLevel is None:
                LOG_WARN('     in _completeCollect, item grade is none:', bagGridID)
                return False

            if bagItem.itemId != itemID:
                LOG_WARN('     in _completeCollect, itemId not matched:', bagItem.itemId, itemID)
                return False

            if bagItem.getEnhanceLevel() != enhanceLevel:
                LOG_WARN('     in _completeCollect, getEnhanceLevel() not matched:', bagItem.getEnhanceLevel(), ' item level', enhanceLevel)
                return False

            if bagItem.getGrade() != gradeLevel:
                LOG_WARN('     in _completeCollect, getGrade() not matched:', bagItem.getGrade(), ' item grade', gradeLevel)
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

    # --------------------------------------------------------------
    # GM

    def _getCollectTotalGrids(self, info):
        # 由于策划分表, equip + props 两个表共用了一个index (collectGridID)
        equipment_len = len(info['equip']) if info['equip'] else 0
        prop_len = len(info['props']) if info['props'] else 0
        return equipment_len + prop_len

    def _checkCollectGridValid(self, info, collectGridID):
        """校验格子配置对本职业有效(与gmFinishCollect口径一致), 仅设完成时需要"""
        school = self.getAvatarSchool()
        if school not in CCDATA.allSchoolList:
            return False
        schoolIdx = CCDATA.allSchoolList.index(school)
        equipment_len = len(info['equip']) if info['equip'] else 0
        propGridID = collectGridID - equipment_len
        if propGridID < 0:
            indexId = info['equip'][collectGridID]
            equipInfo = CEIDX.datas.get(indexId, None)
            if not equipInfo or schoolIdx >= len(equipInfo['propList']):
                return False
        return True

    def _gmRefreshCollectBjCache(self):
        """刷新新手历程收集统计缓存(累积型, 按当前已集齐的收集项重放)"""
        self.clearBeginnerJourneyBehaviorStatusEx([gameconst.BjTaskType.BJ_TASK_TYPE_COLLECTION_STAT])
        for collectId, collectData in self.collectibleData.collectibleDict.items():
            info = PDETAIL.datas.get(collectId, None)
            if not info:
                continue
            if not collectData.isCompleteAll(self._getCollectTotalGrids(info)):
                continue
            self.beginnerJourney_onTaskEvent(
                gameconst.BjTaskType.BJ_TASK_TYPE_COLLECTION_STAT,
                delta=1,
                quality=info['type'])

    def gmSetCollectGrid(self, collectId, gridId, op):
        """GM设置收集项格子状态: gridId=-1表示整项, op=1完成/0清除(支持回退); 收藏位(bit15)不动"""
        LOG_INFO('gmSetCollectGrid', collectId, gridId, op)
        info = PDETAIL.datas.get(collectId, None)
        if not info:
            LOG_ERR('gmSetCollectGrid collectId not exist', collectId)
            return False, 'collectId not exist'
        if op not in (0, 1):
            LOG_ERR('gmSetCollectGrid op invalid', op)
            return False, 'op invalid, 0 clear / 1 complete'
        total_len = self._getCollectTotalGrids(info)
        if gridId != -1 and not 0 <= gridId < total_len:
            LOG_ERR('gmSetCollectGrid gridId invalid', collectId, gridId, total_len)
            return False, 'gridId invalid, range -1~%d' % (total_len - 1)

        if op == 1:
            if self._checkInUnavailableClass(info, collectId):
                LOG_ERR('gmSetCollectGrid unavailable for school', collectId)
                return False, 'collectId unavailable for school'
            gridList = [gridId] if gridId != -1 else list(range(total_len))
            for gid in gridList:
                if not self._checkCollectGridValid(info, gid):
                    LOG_ERR('gmSetCollectGrid grid invalid for school', collectId, gid)
                    return False, 'grid %d invalid for school' % gid
        else:
            gridList = [gridId] if gridId != -1 else list(range(total_len))

        collectData = self.collectibleData.collectibleDict.setdefault(collectId, collectItem(collectId))
        wasCompleteAll = collectData.isCompleteAll(total_len)
        for gid in gridList:
            if op == 1:
                collectData.onComplete(gid)
            else:
                collectData.state &= ~(1 << gid)
        isCompleteAll = collectData.isCompleteAll(total_len)

        # 集齐状态发生翻转时同步cell属性(属性与集齐绑定)
        opUUID = KBEngine.genUUID64()
        if not wasCompleteAll and isCompleteAll:
            self.cell.onCollectAward([collectId], opUUID)
        elif wasCompleteAll and not isCompleteAll:
            self.cell.gmRemoveCollectAward([collectId], opUUID)

        # 重赋值触发持久化; 客户端onGetCollectInfo为按id增量更新
        self.collectibleData = self.collectibleData
        self.client.onGetCollectInfo([collectData.toStreamSavedDic()])
        self._gmRefreshCollectBjCache()
        return True, ''

    def gmResetCollect(self, collectId):
        """GM重置收集项: collectId=0表示全部; 清掉全部进度位(保留收藏位), 已集齐项回收cell属性"""
        LOG_INFO('gmResetCollect', collectId)
        if collectId != 0 and collectId not in PDETAIL.datas:
            LOG_ERR('gmResetCollect collectId not exist', collectId)
            return False, 'collectId not exist'

        if collectId == 0:
            targetItems = list(self.collectibleData.collectibleDict.items())
        else:
            collectData = self.collectibleData.collectibleDict.get(collectId, None)
            targetItems = [(collectId, collectData)] if collectData else []

        removeIndexList = []
        for cid, collectData in targetItems:
            info = PDETAIL.datas.get(cid, None)
            if not info:
                continue
            if collectData.isCompleteAll(self._getCollectTotalGrids(info)):
                removeIndexList.append(cid)
            # 清进度位(bit0~14), 保留收藏位(bit15)
            collectData.state &= (1 << 15)

        if removeIndexList:
            self.cell.gmRemoveCollectAward(removeIndexList, KBEngine.genUUID64())

        self.collectibleData = self.collectibleData
        self.sendCollectInfo()
        self._gmRefreshCollectBjCache()
        return True, ''
