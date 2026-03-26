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

class IMeridian(object):
    """ 
        经脉系统接口
    """
    def __init__(self):
        #self.setPersistentMiscProp(gameconst.AvatarProps.meridianInitRecord, 0)
        pass

    def checkMeridianLimit(self):
        # if self.getPersistentMiscProp(gameconst.AvatarProps.meridianInitRecord) == 0:
        #     return False
        return True

    def meridianOnLogin(self):
        """经脉系统登录处理"""
        if not self.checkMeridianLimit():
            return
        # INFO_MSG("IMeridian.meridianOnLogin")
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

        self.cell.onMeridianAward(indexList)
        # INFO_MSG("IMeridian._refreshMeridianProperty: {}".format(indexList))

    @gamedecorator.checkGameconfigEnable('UIPracticePanel')
    def reqGetMeridianData(self, exposed):
        """
            客户端请求获取经脉数据
        """
        if not self.checkMeridianLimit():
            WARNING_MSG("IMeridian.reqGetMeridianData: meridian system not init")
            return
        
        self._syncMeridianDataToClient()
        
    def _syncMeridianDataToClient(self, login=False):
        """
            同步经脉数据到客户端
        """
        meridianData = self.meridianData.toClientDict()
        if login:
            INFO_MSG("IMeridian._syncMeridianDataToClient: {}".format(meridianData))
        self.client.onGetMeridianData(meridianData['curSlot'], meridianData['maxSlots'], meridianData['slots'])

    @gamedecorator.checkGameconfigEnable('UIPracticePanel')
    def reqLevelUpMeridianPoint(self, exposed, slotIdx, pointIdx, bagType, itemInfoList):
        """
            客户端请求经脉穴位升级
        """
        if not self.checkMeridianLimit():
            WARNING_MSG("IMeridian.reqLevelUpMeridianPoint: meridian system not init")
            return
        
        if not self.meridianData.canLevelUpSlotPoint(slotIdx, pointIdx):
            WARNING_MSG("IMeridian.reqLevelUpMeridianPoint: can not level up {}, {}".format(slotIdx, pointIdx))
            # self.client.onRespLevelUpMeridianPoint(False, slotIdx, pointIdx, 0)
            return
        
        curLevel = self.meridianData.getCurrSlotPointLevel(slotIdx, pointIdx)
        if curLevel is None:
            WARNING_MSG("IMeridian.reqLevelUpMeridianPoint: point level error {}, {}, {}".format(
                slotIdx, pointIdx, curLevel))
            # self.client.onRespLevelUpMeridianPoint(False, slotIdx, pointIdx, 0)
            return
        
        config = self._getPropFromPointConfig(slotIdx, pointIdx, curLevel+1)
        pointItems = config.get('needItems', None)
        if pointItems is None:
            WARNING_MSG("IMeridian.reqLevelUpMeridianPoint: point items not found {}, {}, {}".format(
                slotIdx, pointIdx, config))
            return
        pointCoins = config.get('needCoins', None)
        if pointCoins is None:
            WARNING_MSG("IMeridian.reqLevelUpMeridianPoint: point coins not found {}, {}, {}".format(
                slotIdx, pointIdx, config))
            return
        pointItems = copy.deepcopy(pointItems._data)
        pointItems.append(copy.deepcopy(pointCoins._data))
        
        needItems = {}
        for itemInfo in pointItems:
            itemId = itemInfo[0]
            itemNum = itemInfo[1]
            needItems[itemId] = needItems.get(itemId, 0) + itemNum

        srcType = AAC_AACDD.datas.BONUS_SRC_LEVEL_UP_MERIDIAN
        deductVal = dropAward.DeductWealthVal()
        detail = gameclass.AwardDetail()
        opUUID = KBEngine.genUUID64()
        
        for itemId, itemNum in needItems.items():
            deductVal.addWealthByItemId(itemId, itemNum)
            
        if not self.canDeductWealth(deductVal):
            WARNING_MSG("IMeridian.reqLevelUpMeridianPoint: cost not enough {}, {}, {}, {}".format(
                slotIdx, pointIdx, bagType, needItems))
            return

        self.deductWealth(srcType, deductVal, opUUID, detail)
        ret, newLevel = self.meridianData.levelUpPoint(slotIdx, pointIdx)
        INFO_MSG("IMeridian.reqLevelUpMeridianPoint: {}, {}, {}, {}".format(slotIdx, pointIdx, ret, newLevel))
        if ret:
            self.cell.onMeridianAward([self.getConfigId(slotIdx, pointIdx, newLevel)])
            self.client.onLeveUpMeridianPointTo(slotIdx, pointIdx, newLevel)
            
            self._syncMeridianDataToClient()
            
            LogTrackingMgr.LogTrackingMgr.Meridian_UpGrade(opUUID, self.gbID, slotIdx, pointIdx, newLevel)
        else:
            DEBUG_MSG("IMeridian.reqLevelUpMeridianPoint: level up failed {}, {}, {}".format(
                slotIdx, pointIdx, ret))
        
    @gamedecorator.checkGameconfigEnable('UIPracticePanel')
    def reqEnhanceMeridianSlot(self, exposed, slotIdx, bagType, itemInfoList):
        """
            客户端请求经脉强化
        """
        if not self.checkMeridianLimit():
            WARNING_MSG("IMeridian.reqEnhanceMeridianSlot: meridian system not init")
            return
        if not self.meridianData.canEnhanceCurSlot(slotIdx):
            WARNING_MSG("IMeridian.reqEnhanceMeridianSlot: can not enhance slot {}".format(slotIdx))
            # self.client.onRespEnhanceMeridianSlot(False, slotIdx)
            return
        
        slotConfig = self._getPropFromSlotConfig(slotIdx)
        slotItems = slotConfig.get('needItems', None)
        if slotItems is None:
            WARNING_MSG("IMeridian.reqEnhanceMeridianSlot: slot items not found {}".format(
                slotIdx))
            return
        slotCoins = slotConfig.get('needCoins', None)
        if slotCoins is None:
            WARNING_MSG("IMeridian.reqEnhanceMeridianSlot: slot coins not found {}".format(
                slotIdx))
            return
        slotItems = copy.deepcopy(slotItems._data)
        slotItems.append(copy.deepcopy(slotCoins._data))
        
        needItems = {}
        for itemInfo in slotItems:
            itemId = itemInfo[0]
            itemNum = itemInfo[1]
            needItems[itemId] = needItems.get(itemId, 0) + itemNum

        srcType = AAC_AACDD.datas.BONUS_SRC_ENHANCE_MERIDIAN
        deductVal = dropAward.DeductWealthVal()
        detail = gameclass.AwardDetail()
        opUUID = KBEngine.genUUID64()
        
        for itemId, itemNum in needItems.items():
            deductVal.addWealthByItemId(itemId, itemNum)
            
        if not self.canDeductWealth(deductVal):
            WARNING_MSG("IMeridian.reqEnhanceMeridianSlot: cost not enough {}, {}, {}".format(
                slotIdx, bagType, needItems))
            return
            
        self.deductWealth(srcType, deductVal, opUUID, detail)
        ret, newSlot = self.meridianData.doEnhanceCurSlot(slotIdx)
        INFO_MSG("IMeridian.reqEnhanceMeridianSlot: {}, {}, {}".format(slotIdx, ret, newSlot))
        if ret:
            self.cell.onMeridianAward([slotIdx])
            self.client.onEnhanceMeridian(slotIdx)
            
            self._syncMeridianDataToClient()
            
            LogTrackingMgr.LogTrackingMgr.Meridian_Enhance(opUUID, self.gbID, slotIdx)
        else:
            DEBUG_MSG("IMeridian.reqEnhanceMeridianSlot: enhance failed {}".format(slotIdx))


    def gmLevelUpMeridianPoint(self, slotIdx, pointIdx, full, show=True):
        """GM命令：经脉穴位升级"""
        if not self.checkMeridianLimit():
            WARNING_MSG("IMeridian.gmLevelUpMeridianPoint: meridian system not init")
            return
        
        num = 1
        if full:
            num = MeridianInfo.MeridianPointVal().maxLevel

        for _ in range(num):
            ret, newLevel = self.meridianData.levelUpPoint(slotIdx, pointIdx)
            INFO_MSG("IMeridian.gmLevelUpMeridianPoint: {}, {}, {}, {}".format(slotIdx, pointIdx, ret, newLevel))
            if ret:
                self.cell.onMeridianAward([self.getConfigId(slotIdx, pointIdx, newLevel)])
                self.client.onLeveUpMeridianPointTo(slotIdx, pointIdx, newLevel)
            else:
                DEBUG_MSG("IMeridian.gmLevelUpMeridianPoint: level up failed {}, {}, {}".format(
                    slotIdx, pointIdx, ret))
                
        if show:
            self._syncMeridianDataToClient()

    def gmEnhanceMeridianSlot(self, slotIdx, show=True):
        """GM命令：经脉槽位强化"""
        if not self.checkMeridianLimit():
            WARNING_MSG("IMeridian.gmLevelUpMeridianSlot: meridian system not init")
            return
        
        ret, newSlot = self.meridianData.doEnhanceCurSlot(slotIdx)
        INFO_MSG("IMeridian.gmLevelUpMeridianSlot: {}, {}, {}".format(slotIdx, ret, newSlot))
        if ret:
            self.cell.onMeridianAward([slotIdx])
            self.client.onEnhanceMeridian(slotIdx)
            
            if show:
                self._syncMeridianDataToClient()
        else:
            DEBUG_MSG("IMeridian.gmLevelUpMeridianSlot: enhance failed {}".format(slotIdx))

    def gmLevelUpMeridianSlot(self, slotIdx, show=True):
        num = MeridianInfo.MeridianSlotVal().maxPoints
        for pointIdx in range(1, num + 1):
            self.gmLevelUpMeridianPoint(slotIdx, pointIdx, True, show)

        self.gmEnhanceMeridianSlot(slotIdx, show)

    def gmUnlockAllMeridian(self):
        """GM命令：解锁所有经脉槽位"""
        maxSlots = MeridianInfo.MeridianVal().maxSlots
        for slotIdx in range(1, maxSlots + 1):
            if self.meridianData.curSlot > slotIdx:
                continue
            self.gmLevelUpMeridianSlot(slotIdx)

    def gmResetMeridian(self):
        """GM命令：重置经脉系统"""
        self.meridianData = MeridianInfo.MeridianVal()
        self._syncMeridianDataToClient()
        

    

    
    