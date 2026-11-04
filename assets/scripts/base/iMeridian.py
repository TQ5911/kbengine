# coding: utf-8
import KBEngine
from KBEDebug import *

import utils
import gameglobal
import gameengine
import gameconst
import MeridianInfo
import dropAward
import gameclass
import copy
import gamedecorator

import meridian_config as  MCD
import meridian_meridian as MMD
import meridian_acupoint as MAD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import LogTrackingMgr
import actionContext

class IMeridian(object):
    """ 
        经脉系统接口
    """
    def __init__(self):
        #self.setPersistentMiscProp(gameconst.EntityPropsEnum.meridianInitRecord, 0)
        pass

    def checkMeridianLimit(self):
        # if self.getPersistentMiscProp(gameconst.EntityPropsEnum.meridianInitRecord) == 0:
        #     return False
        return True

    def meridianOnLogin(self):
        """经脉系统登录处理"""
        if not self.checkMeridianLimit():
            return
        # LOG_INFO("IMeridian.meridianOnLogin")
        self._refreshMeridianProperty()
        
        #
        self._syncMeridianDataToClient(True)
    
    def getConfigId(self, slotIdx, pointIdx, level):
        """获取经脉穴位配置ID"""
        return slotIdx * 10000 + pointIdx * 100 + level

    def _getPropFromPointConfig(self, slotIdx, pointIdx, level):
        """从配置表中获取个穴位配置"""
        configId = self.getConfigId(slotIdx, pointIdx, level)
        config = MAD.datas.get(configId, {})
        
        return config
        
    def _getPropFromSlotConfig(self, slotIdx):
        """从配置表中获取经脉槽位配置"""
        slotConfig = MMD.datas.get(slotIdx, {})
        return slotConfig

    def _refreshMeridianProperty(self):
        """刷新经脉属性加成"""
        if not self.checkMeridianLimit():
            return

        indexList = []
        for slotIdx, slotVal in self.meridianData.slotDict.items():
            for pointIdx, pointVal in slotVal.pointDict.items():
                level = pointVal.getCurLevel()
                if level <= 0:
                    continue
                for lv in range(1, level + 1):
                    indexList.append(self.getConfigId(slotIdx, pointIdx, lv))
            
            if slotVal.hasEnhance:
                indexList.append(slotIdx)

            self.cell.onMeridianAward(indexList, 0)
            # LOG_INFO("IMeridian._refreshMeridianProperty: {}".format(indexList))
            indexList = []

    @gamedecorator.checkGameconfigEnable('UIPracticePanel')
    @gamedecorator.crossServer
    def reqGetMeridianData(self, exposed):
        """
            客户端请求获取经脉数据
        """
        if not self.checkMeridianLimit():
            LOG_WARN("IMeridian.reqGetMeridianData: meridian system not init")
            return
        
        self._syncMeridianDataToClient()
        
    def _syncMeridianDataToClient(self, login=False):
        """
            同步经脉数据到客户端
        """
        meridianData = self.meridianData.toClientDict()
        if login:
            LOG_INFO("IMeridian._syncMeridianDataToClient: {}".format(meridianData))
        self.client.onGetMeridianData(meridianData['curSlot'], meridianData['maxSlots'], meridianData['slots'])

    @gamedecorator.checkGameconfigEnable('UIPracticePanel')
    def reqLevelUpMeridianPoint(self, exposed, slotIdx, pointIdx, bagType, itemInfoList):
        """
            客户端请求经脉穴位升级
        """
        if not self.checkMeridianLimit():
            LOG_WARN("IMeridian.reqLevelUpMeridianPoint: meridian system not init")
            return
        
        if not self.meridianData.canLevelUpSlotPoint(slotIdx, pointIdx):
            LOG_WARN("IMeridian.reqLevelUpMeridianPoint: can not level up {}, {}".format(slotIdx, pointIdx))
            # self.client.onRespLevelUpMeridianPoint(False, slotIdx, pointIdx, 0)
            return
        
        curLevel = self.meridianData.getCurrSlotPointLevel(slotIdx, pointIdx)
        if curLevel is None:
            LOG_WARN("IMeridian.reqLevelUpMeridianPoint: point level error {}, {}, {}".format(
                slotIdx, pointIdx, curLevel))
            # self.client.onRespLevelUpMeridianPoint(False, slotIdx, pointIdx, 0)
            return
        
        # 当前这条经脉对应的等级条件
        slotConfig = self._getPropFromSlotConfig(slotIdx)
        needLevel = slotConfig['needLevel']
        playerLevel = gameglobal.roleCache[self.id]['level']
        if playerLevel < needLevel:
            LOG_WARN("IMeridian.reqLevelUpMeridianPoint: player is not enough {}, {}, {}, {}, {}".format(
                slotIdx, pointIdx, slotConfig, playerLevel, needLevel))
            return
        
        config = self._getPropFromPointConfig(slotIdx, pointIdx, curLevel+1)
        pointItems = config.get('needItems', None)
        if pointItems is None:
            LOG_WARN("IMeridian.reqLevelUpMeridianPoint: point items not found {}, {}, {}".format(
                slotIdx, pointIdx, config))
            return
        
        pointCoins = config.get('needCoins', None)
        if pointCoins is None:
            LOG_WARN("IMeridian.reqLevelUpMeridianPoint: point coins not found {}, {}, {}".format(
                slotIdx, pointIdx, config))
            return
        
        needItems = {}
        for itemInfo in pointItems:
            itemId = itemInfo[0]
            itemNum = itemInfo[1]
            needItems[itemId] = needItems.get(itemId, 0) + itemNum
        itemId, itemNum = pointCoins
        needItems[itemId] = needItems.get(itemId, 0) + itemNum

        srcType = AAC_AACDD.datas.BONUS_SRC_LEVEL_UP_MERIDIAN
        deductVal = dropAward.DeductWealthVal()
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        
        for itemId, itemNum in needItems.items():
            deductVal.addWealthByItemId(itemId, itemNum)
            
        res = self.canDeductWealth(deductVal)
        if not res:
            LOG_WARN("IMeridian.reqLevelUpMeridianPoint: cost not enough {}, {}, {}, {}, {}".format(
                slotIdx, pointIdx, bagType, needItems, res()))
            return

        self.deductWealth(srcType, deductVal, opUUID, detail)
        ret, newLevel = self.meridianData.levelUpPoint(slotIdx, pointIdx)
        LOG_INFO("IMeridian.reqLevelUpMeridianPoint: {}, {}, {}, {}".format(slotIdx, pointIdx, ret, newLevel))
        if ret:
            self.cell.onMeridianAward([self.getConfigId(slotIdx, pointIdx, newLevel)], opUUID)
            self.client.onLeveUpMeridianPointTo(slotIdx, pointIdx, newLevel)
            
            self._syncMeridianDataToClient()
            
            LogTrackingMgr.LogTrackingMgr.Meridian_UpGrade(self.gbID, self.accountEntity.clientDistinctId, opUUID, self.gbID, slotIdx, pointIdx, newLevel, needItems)
            self.triggerAchievementWithCtx(gameconst.AchieveType.MERIDIAN, actionContext.AchievementCtx(slotIdx=slotIdx))
        else:
            LOG_DBG("IMeridian.reqLevelUpMeridianPoint: level up failed {}, {}, {}".format(
                slotIdx, pointIdx, ret))
        
    @gamedecorator.checkGameconfigEnable('UIPracticePanel')
    def reqEnhanceMeridianSlot(self, exposed, slotIdx, bagType, itemInfoList):
        """
            客户端请求经脉强化
        """
        if not self.checkMeridianLimit():
            LOG_WARN("IMeridian.reqEnhanceMeridianSlot: meridian system not init")
            return
        
        if not self.meridianData.canEnhanceCurSlot(slotIdx):
            LOG_WARN("IMeridian.reqEnhanceMeridianSlot: can not enhance slot {}".format(slotIdx))
            # self.client.onRespEnhanceMeridianSlot(False, slotIdx)
            return
        
        # 贯通静脉需要判断下一条静脉的开启条件
        slotConfig = self._getPropFromSlotConfig(slotIdx + 1)
        if slotConfig:
            needLevel = slotConfig['needLevel']
            playerLevel = gameglobal.roleCache[self.id]['level']
            if playerLevel < needLevel:
                LOG_WARN("IMeridian.reqEnhanceMeridianSlot: player level is not enough {}, {}, {}, {}".format(
                    slotIdx, playerLevel, needLevel, slotConfig))
                return
            
        slotConfig = self._getPropFromSlotConfig(slotIdx)
        pointItems = slotConfig.get('needItems', None)
        if pointItems is None:
            LOG_WARN("IMeridian.reqEnhanceMeridianSlot: slot items not found {}".format(
                slotIdx))
            return
        
        pointCoins = slotConfig.get('needCoins', None)
        if pointCoins is None:
            LOG_WARN("IMeridian.reqEnhanceMeridianSlot: slot coins not found {}".format(
                slotIdx))
            return
        
        needItems = {}
        for itemInfo in pointItems:
            itemId = itemInfo[0]
            itemNum = itemInfo[1]
            needItems[itemId] = needItems.get(itemId, 0) + itemNum
        itemId, itemNum = pointCoins
        needItems[itemId] = needItems.get(itemId, 0) + itemNum

        srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_MERIDIAN
        deductVal = dropAward.DeductWealthVal()
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        
        for itemId, itemNum in needItems.items():
            deductVal.addWealthByItemId(itemId, itemNum)
            
        res = self.canDeductWealth(deductVal)
        if not res:
            LOG_WARN("IMeridian.reqEnhanceMeridianSlot: cost not enough {}, {}, {}, {}".format(
                slotIdx, bagType, needItems, res()))
            return
            
        self.deductWealth(srcType, deductVal, opUUID, detail)
        ret, newSlot = self.meridianData.doEnhanceCurSlot(slotIdx)
        LOG_INFO("IMeridian.reqEnhanceMeridianSlot: {}, {}, {}".format(slotIdx, ret, newSlot))
        if ret:
            self.cell.onMeridianAward([slotIdx], opUUID)
            self.client.onEnhanceMeridian(slotIdx)
            
            self._syncMeridianDataToClient()
            self.beginnerJourney_onTaskEvent(
                    gameconst.BjTaskType.BJ_TASK_TYPE_MERIDIAN,
                    delta=1, level=newSlot)
            LogTrackingMgr.LogTrackingMgr.Meridian_Enhance(self.gbID, self.accountEntity.clientDistinctId, opUUID, self.gbID, slotIdx, needItems)
        else:
            LOG_DBG("IMeridian.reqEnhanceMeridianSlot: enhance failed {}".format(slotIdx))


    def gmLevelUpMeridianPoint(self, slotIdx, pointIdx, full, show=True):
        """GM命令：经脉穴位升级"""
        if not self.checkMeridianLimit():
            LOG_WARN("IMeridian.gmLevelUpMeridianPoint: meridian system not init")
            return
        
        num = 1
        if full:
            num = MeridianInfo.MeridianPointVal().maxLevel

        for _ in range(num):
            ret, newLevel = self.meridianData.levelUpPoint(slotIdx, pointIdx)
            LOG_INFO("IMeridian.gmLevelUpMeridianPoint: {}, {}, {}, {}".format(slotIdx, pointIdx, ret, newLevel))
            if ret:
                self.cell.onMeridianAward([self.getConfigId(slotIdx, pointIdx, newLevel)], 0)
                self.client.onLeveUpMeridianPointTo(slotIdx, pointIdx, newLevel)
            else:
                LOG_DBG("IMeridian.gmLevelUpMeridianPoint: level up failed {}, {}, {}".format(
                    slotIdx, pointIdx, ret))
                
        if show:
            self._syncMeridianDataToClient()

    def gmEnhanceMeridianSlot(self, slotIdx, show=True):
        """GM命令：经脉槽位强化"""
        if not self.checkMeridianLimit():
            LOG_WARN("IMeridian.gmLevelUpMeridianSlot: meridian system not init")
            return
        
        ret, newSlot = self.meridianData.doEnhanceCurSlot(slotIdx)
        LOG_INFO("IMeridian.gmLevelUpMeridianSlot: {}, {}, {}".format(slotIdx, ret, newSlot))
        if ret:
            self.cell.onMeridianAward([slotIdx], 0)
            self.client.onEnhanceMeridian(slotIdx)
            
            if show:
                self._syncMeridianDataToClient()
        else:
            LOG_DBG("IMeridian.gmLevelUpMeridianSlot: enhance failed {}".format(slotIdx))

    def gmLevelUpMeridianSlot(self, slotIdx, show=True):
        num = MeridianInfo.MeridianSlotVal().maxPoints
        for pointIdx in range(1, num + 1):
            self.gmLevelUpMeridianPoint(slotIdx, pointIdx, True, show)

        self.gmEnhanceMeridianSlot(slotIdx, show)

    def gmUnlockAllMeridian(self):
        """GM命令：解锁所有经脉槽位（全部穴位满级并贯通）

        旧实现逐槽逐穴逐级升级：20 槽 x 8 穴 x 5 级 = 800 次，每次都会
        cell.onMeridianAward + client.onLeveUpMeridianPointTo + 一次全量
        _syncMeridianDataToClient，全部压进同一个 tick（客户端读不过来会直接断连，
        压测时也足以打满一个 BaseApp 的 tick）。
        改为构造「全满」的 MeridianVal 一次性走 gmSetMeridianData：
        cell 侧只收到一次差量加减属性调用，客户端只收到一次全量同步，最终状态与逐级升级一致。
        """
        if not self.checkMeridianLimit():
            LOG_WARN("IMeridian.gmUnlockAllMeridian: meridian system not init")
            return
        maxSlots = MeridianInfo.MeridianVal().maxSlots
        newVal = MeridianInfo.MeridianVal()
        newVal.slotDict = {}
        for slotIdx in range(1, maxSlots + 1):
            slotVal = MeridianInfo.MeridianSlotVal(slotIdx=slotIdx)
            for pointVal in slotVal.pointDict.values():
                pointVal.level = pointVal.maxLevel
            slotVal.hasEnhance = True
            newVal.slotDict[slotIdx] = slotVal
        # curSlot 对应的槽位必须存在（toClientDict 依赖），全部贯通时放一个空槽位，与正常流程一致
        newVal.slotDict[maxSlots + 1] = MeridianInfo.MeridianSlotVal(slotIdx=maxSlots + 1)
        newVal.curSlot = maxSlots + 1
        self.gmSetMeridianData(newVal)

    def gmResetMeridian(self):
        """GM命令：重置经脉系统(统一走gmSetMeridianData, 同步回退cell属性与评分)"""
        self.gmSetMeridianData(MeridianInfo.MeridianVal())
        return True, ''

    def _collectMeridianConfigIds(self, meridianVal):
        """遍历出经脉配置ID全集(穴位每级一个ID, 贯通槽位为slotIdx), 与_refreshMeridianProperty口径一致"""
        indexList = []
        for slotIdx, slotVal in meridianVal.slotDict.items():
            for pointIdx, pointVal in slotVal.pointDict.items():
                level = pointVal.getCurLevel()
                for lv in range(1, level + 1):
                    indexList.append(self.getConfigId(slotIdx, pointIdx, lv))
            if slotVal.hasEnhance:
                indexList.append(slotIdx)
        return indexList

    def gmSetMeridianData(self, newVal):
        """GM设置经脉数据统一入口: cell侧按差量加减属性, 评分按新数据全量重算"""
        oldIndexSet = set(self._collectMeridianConfigIds(self.meridianData))
        newIndexSet = set(self._collectMeridianConfigIds(newVal))
        addIndexList = list(newIndexSet - oldIndexSet)
        removeIndexList = list(oldIndexSet - newIndexSet)
        LOG_INFO("IMeridian.gmSetMeridianData: add {}, remove {}".format(addIndexList, removeIndexList))

        self.meridianData = newVal
        self.cell.gmSetMeridianProps(addIndexList, removeIndexList, list(newIndexSet), KBEngine.genUUID64())
        self._syncMeridianDataToClient()

        # 刷新新手历程经脉缓存(属性查询型, level=已贯通层数)
        self.clearBeginnerJourneyBehaviorStatusEx([gameconst.BjTaskType.BJ_TASK_TYPE_MERIDIAN])
        self.beginnerJourney_onTaskEvent(
            gameconst.BjTaskType.BJ_TASK_TYPE_MERIDIAN,
            delta=1,
            level=newVal.curSlot - 1)

    def gmSetMeridianSlot(self, slotId):
        """GM设置当前经脉层数: 1~slotId-1层全满并贯通, slotId层0级未贯通, 更高层删除; slotId=maxSlots+1表示全部贯通"""
        LOG_INFO("IMeridian.gmSetMeridianSlot: {}".format(slotId))
        if not self.checkMeridianLimit():
            return False, 'meridian system not init'
        maxSlots = MeridianInfo.MeridianVal().maxSlots
        if slotId < 1 or slotId > maxSlots + 1:
            LOG_ERR("IMeridian.gmSetMeridianSlot: slotId invalid {}".format(slotId))
            return False, 'slotId invalid, range 1~%d' % (maxSlots + 1)
        for idx in range(1, slotId):
            if idx not in MMD.datas:
                LOG_ERR("IMeridian.gmSetMeridianSlot: slot config not found {}".format(idx))
                return False, 'slot config not found: %d' % idx

        newVal = MeridianInfo.MeridianVal()
        newVal.slotDict = {}
        for idx in range(1, slotId):
            slotVal = MeridianInfo.MeridianSlotVal(slotIdx=idx)
            for pointVal in slotVal.pointDict.values():
                pointVal.level = pointVal.maxLevel
            slotVal.hasEnhance = True
            newVal.slotDict[idx] = slotVal
        # curSlot对应的槽位必须存在(toClientDict依赖), 全部贯通时为空槽位, 与正常流程一致
        newVal.slotDict[slotId] = MeridianInfo.MeridianSlotVal(slotIdx=slotId)
        newVal.curSlot = slotId
        self.gmSetMeridianData(newVal)
        return True, ''

    def gmSetMeridianPoint(self, slotId, pointId, level):
        """GM设置指定经脉穴位等级(0~5, 支持降级); 已贯通经脉不允许降低穴位等级, 请用gmSetMeridianSlot整层回退"""
        LOG_INFO("IMeridian.gmSetMeridianPoint: {}, {}, {}".format(slotId, pointId, level))
        if not self.checkMeridianLimit():
            return False, 'meridian system not init'
        maxLevel = MeridianInfo.MeridianPointVal().maxLevel
        if level < 0 or level > maxLevel:
            LOG_ERR("IMeridian.gmSetMeridianPoint: level invalid {}".format(level))
            return False, 'level invalid, range 0~%d' % maxLevel
        slotVal = self.meridianData.slotDict.get(slotId, None)
        if slotVal is None:
            LOG_ERR("IMeridian.gmSetMeridianPoint: slot not opened {}".format(slotId))
            return False, 'slot not opened: %d' % slotId
        if pointId not in slotVal.pointDict:
            LOG_ERR("IMeridian.gmSetMeridianPoint: pointId invalid {}".format(pointId))
            return False, 'pointId invalid: %d' % pointId
        if slotVal.hasEnhance and level < maxLevel:
            LOG_ERR("IMeridian.gmSetMeridianPoint: slot already enhanced {}, {}".format(slotId, level))
            return False, 'slot already enhanced, use gmSetMeridianSlot to rollback'
        if level >= 1 and self.getConfigId(slotId, pointId, level) not in MAD.datas:
            LOG_ERR("IMeridian.gmSetMeridianPoint: point config not found {}, {}, {}".format(slotId, pointId, level))
            return False, 'point config not found'

        newVal = copy.deepcopy(self.meridianData)
        newVal.slotDict[slotId].pointDict[pointId].level = level
        self.gmSetMeridianData(newVal)
        return True, ''
        

    

    
    
