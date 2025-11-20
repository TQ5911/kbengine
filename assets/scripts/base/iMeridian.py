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

import meridian_config as  MCD
import meridian_meridian as MMD
import meridian_acupoint as MAD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

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
    
    def _getPropListFromConfig(self, config):
        """从配置表中获取属性列表"""
        propIndexList = []
        schoolList = [0, self.getAvatarSchool()]
        propDict = config.get('prop', {})
        for sch in schoolList:
            if sch in propDict.keys():
                propIndexList.append(propDict[sch])
        return propIndexList

    def _refreshMeridianProperty(self):
        """刷新经脉属性加成"""
        if not self.checkMeridianLimit():
            return

        propIndexList = []
        for slotIdx, slotVal in self.meridianData.slotDict.items():
            for pointIdx, pointVal in slotVal.pointDict.items():
                level = pointVal.getCurLevel()
                if level <= 0:
                    continue
                config = self._getPropFromPointConfig(slotIdx, pointIdx, level)
                tempList = self._getPropListFromConfig(config)
                propIndexList.extend(tempList)
            
            if slotVal.hasEnhance:
                config = self._getPropFromSlotConfig(slotIdx)
                tempList = self._getPropListFromConfig(config)
                propIndexList.extend(tempList)

        self.cell.onMeridianAward(propIndexList)
        # INFO_MSG("IMeridian._refreshMeridianProperty: {}".format(propIndexList))


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

        srcType = AAC_AACDD.datas.BONUS_SRC_RANDOM_SYNTHESIS
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
            propIndexList = self._getPropListFromConfig(config)
            self.cell.onMeridianAward(propIndexList)
            self.client.onLeveUpMeridianPointTo(slotIdx, pointIdx, newLevel)
            
            self._syncMeridianDataToClient()
        else:
            DEBUG_MSG("IMeridian.reqLevelUpMeridianPoint: level up failed {}, {}, {}".format(
                slotIdx, pointIdx, ret))
        

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

        srcType = AAC_AACDD.datas.BONUS_SRC_RANDOM_SYNTHESIS
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
            propIndexList = self._getPropListFromConfig(slotConfig)
            self.cell.onMeridianAward(propIndexList)
            self.client.onEnhanceMeridian(slotIdx)
            
            self._syncMeridianDataToClient()
        else:
            DEBUG_MSG("IMeridian.reqEnhanceMeridianSlot: enhance failed {}".format(slotIdx))

