# coding: utf-8

from KBEDebug import *

import KBEngine
import gameclass
import dropAward
import gameglobal
import utils
import gameengine
import gameconst
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemData as ID_IDD
import activityControl_config as AC_CD
import gamedecorator
import LogTrackingMgr
import visible_visible as V_VD
import creep_base as CBD
import welfare_resourceRecovery as W_RR
import copy
import gameconfig
import message_Message_def as MMD


class IResourceRecovery(object):
    def __init__(self):
        LOG_DBG("IResourceRecovery::__init__")
        self.setTempMiscProp(gameconst.EntityPropsEnum.cellNovice, self.getCellData('novice', 1))
        self.subType2FreeTicketInfo = {
            gameconst.FreeTicketSubType.CUBE            :   [lambda self: self.leftCubeTimes, lambda self: self.modifyLeftCubeTimes, lambda self: self._cubeDailyRefresh],
            gameconst.FreeTicketSubType.WONDER_LAND     :   [lambda self: self.wonderLandTicket, lambda self: self.modifyWonderLandTicket, lambda self: self._wonderLandRefreshDaily],
            gameconst.FreeTicketSubType.ABYSS           :   [lambda self: self.abyssTicket, lambda self: self.modifyAbyssTicket, lambda self: self._abyssRefreshDaily],
            gameconst.FreeTicketSubType.CRUSADE         :   [lambda self: self.crusadeInfo.leftDailyRewardNum, lambda self: self.onUseCoinToIncreaseCrusadeRewardNumber, lambda self: self.onCrusadeDailyRewardNumUpdate],
            gameconst.FreeTicketSubType.CHIEF           :   [lambda self: self.chiefInfo.leftDailyRewardNum, lambda self: self.onUseCoinToIncreaseChiefRewardNumber, lambda self: self.onChiefDailyRewardNumUpdate],
        }

    def sendAllRecoveryInfo(self):
        LOG_INFO("IResourceRecovery::sendAllRecoveryInfo")
        for subType in gameconst.FreeTicketSubType.VALID_SUB_TYPE:
            self.updateFreeTicketRecoveryInfo(subType)

    def resourceRecoveryOnLogin(self):
        cellNovice = self.getTempMiscProp(gameconst.EntityPropsEnum.cellNovice, 0)
        LOG_INFO("IResourceRecovery::resourceRecoveryOnLogin cellNovice", cellNovice)
        if cellNovice:
            return
        LOG_INFO("IResourceRecovery::resourceRecoveryOnLogin")
        for subType in gameconst.FreeTicketSubType.VALID_SUB_TYPE:
            self.updateFreeTicketInfo(subType, self.subType2FreeTicketInfo[subType][0](self), gameconst.FreeTicketUpdateType.LOGIN)

    def resourceRecoveryOnOffline(self):
        LOG_INFO("IResourceRecovery::resourceRecoveryOnOffline")
        for subType in gameconst.FreeTicketSubType.VALID_SUB_TYPE:
            self.updateFreeTicketInfo(subType, self.subType2FreeTicketInfo[subType][0](self), gameconst.FreeTicketUpdateType.OFFLINE, self.tLastUpdateTime)

    def getCfgNumByDateTime(self, subType, dateTime):
        cfgList = gameglobal.freeTicketNumConfig.get(subType, [])
        for cfgIdx, cfgInfo in enumerate(cfgList):
            if cfgList[cfgIdx][0] <= dateTime and cfgIdx + 1 < len(cfgList) and dateTime < cfgList[cfgIdx + 1][0]:
                return cfgList[cfgIdx][1]
        return 0

    def checkFreeTicketNumConfig(self, subType):
        if not gameglobal.freeTicketNumConfig.get(subType, []):
            LOG_WARN("IResourceRecovery::checkFreeTicketNumConfig not serverOpenTime", subType)
            return False
        return True

    def checkGameConfigEnable(self, subType):
        cfgData = W_RR.datas.get(subType + 1, {})
        if not cfgData:
            LOG_ERR("IResourceRecovery::checkGameConfigEnable no cfg", subType + 1)
            return False
        condition = cfgData['condition']
        conditionType = V_VD.datas.get(condition).get("type", "")
        if not gameconfig.visibleConfigEnabled(conditionType):
            LOG_WARN("IResourceRecovery::checkGameConfigEnable not open", conditionType)
            return False
        
        return True

    def updateFreeTicketInfo(self, subType, leftNum, reason, now=0):
        if not self.checkFreeTicketNumConfig(subType):
            return
        now = now if now else utils.curTS()
        curDateTime = utils.getIntDateTime(now)
        LOG_INFO("IResourceRecovery::updateFreeTicketInfo", now, curDateTime, subType, leftNum, reason)
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo", gameglobal.freeTicketNumConfig.get(subType, []))
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo", self.freeTicketUseInfo.get(subType, []))
        infoList = self.freeTicketUseInfo.setdefault(subType, [])
        cfgList = gameglobal.freeTicketNumConfig.get(subType, [])
        LOG_INFO("IResourceRecovery::updateFreeTicketInfo2", infoList)
        lastData = infoList[-1] if infoList else None
        lastCfgData = cfgList[-1]

        if reason == gameconst.FreeTicketUpdateType.LOGIN or reason == gameconst.FreeTicketUpdateType.OFFLINE:
            LOG_INFO("IResourceRecovery::updateFreeTicketInfo3", lastData, curDateTime)
            if not lastData or lastData[0] < curDateTime:
                infoList.append([curDateTime, leftNum])
            elif lastData[0] == curDateTime:
                lastData[1] = leftNum
                if lastCfgData[0] == lastData[0]:
                    return
            else:
                return
        elif reason == gameconst.FreeTicketUpdateType.TIMED or reason == gameconst.FreeTicketUpdateType.UPDATE:
            curDataTimestamp = utils.getIntTimestamp(str(curDateTime) + gameconst.RESOURCE_RECOVER_TIME_POINT_STR)
            preDataTimestamp = curDataTimestamp - 86400
            preDataTime = utils.getIntDateTime(preDataTimestamp)
            LOG_INFO("IResourceRecovery::updateFreeTicketInfo5", lastData, preDataTime)
            if not lastData or lastData[0] < preDataTime:
                infoList.append([preDataTime, leftNum])
            elif lastData[0] == preDataTime:
                lastData[1] = leftNum
            else:
                return

        LOG_DBG("IResourceRecovery::updateFreeTicketInfo6", infoList)

        idx = 0
        while infoList:
            if idx >= len(infoList):
                break
            if infoList[idx][0] >= cfgList[0][0]:
                LOG_DBG("IResourceRecovery::updateFreeTicketInfo7", infoList[0], cfgList[0])
                break
            idx += 1
        infoList = infoList[idx:]
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo8", idx, infoList)

        adjInfoList = copy.deepcopy(cfgList)
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo10", infoList, adjInfoList, cfgList)

        adjIdx = 0
        for info in infoList:
            while adjIdx < len(adjInfoList):
                if adjInfoList[adjIdx][0] == info[0]:
                    adjInfoList[adjIdx][1] = info[1]
                    adjIdx += 1
                    break
                else:
                    adjIdx += 1

        self.freeTicketUseInfo[subType] = adjInfoList
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo11", self.freeTicketUseInfo[subType])
        self.updateFreeTicketRecoveryInfo(subType)
    
    def updateFreeTicketRecoveryInfo(self, subType):
        if not self.checkFreeTicketNumConfig(subType):
            return
        cfgData = W_RR.datas.get(subType + 1, {})
        if not cfgData:
            LOG_ERR("IResourceRecovery::updateFreeTicketRecoveryInfo no cfg", subType + 1)
            return
        LOG_DBG("IResourceRecovery::updateFreeTicketRecoveryInfo", self.freeTicketUseInfo.get(subType, []), cfgData)
        infoList = self.freeTicketUseInfo.get(subType, [])
        costCfg = cfgData['cost']
        recoveryInfoList = []
        clientDataList = []
        for idx, info in enumerate(reversed(infoList)):
            if idx <= 0:
                LOG_DBG("IResourceRecovery::updateFreeTicketRecoveryInfo info", info)
                continue
            for cost in costCfg:
                if idx > cost[0]:
                    continue
                recoveryInfoList.append([info[0], info[1], cost[1], cost[2]])
                clientDataList.append({'num': info[1], 'itemId': cost[1], 'itemNum': cost[2]})
                break
        self.freeTickeRecoveryInfo[subType] = recoveryInfoList
        
        LOG_DBG("IResourceRecovery::updateFreeTicketRecoveryInfo recoveryInfoList", self.freeTickeRecoveryInfo[subType])
        LOG_DBG("IResourceRecovery::updateFreeTicketRecoveryInfo clientDataList", clientDataList)
        self.client.onFreeTicketRecoveryInfo(subType + 1, clientDataList)

    def calFreeTicketRecovery(self, subType, num, deductWealthVal, costInfo, checkRTypeFunc=None):
        leftNum = num
        recoveryInfo = self.freeTickeRecoveryInfo.get(subType, [])
        copyRecoveryInfo = copy.deepcopy(recoveryInfo)
        for info in copyRecoveryInfo:
            if info[1] <= 0:
                continue
            if checkRTypeFunc and not checkRTypeFunc(info[3]):
                continue
            n = min(leftNum, info[1])
            leftNum -= n
            info[1] -= n
            if info[2] and info[3]:
                deductWealthVal.addWealthByItemId(info[2], n * info[3])
            costInfo.append([info[0], n, info[2], info[3]])
            if leftNum <= 0:
                break

        return leftNum

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('welfare_resourceRecovery')
    def reqFreeTicketRecovery(self, exposed, subType, num):
        LOG_INFO("IResourceRecovery::reqFreeTicketRecovery", num, subType - 1)
        subType -= 1
        if subType not in gameconst.FreeTicketSubType.VALID_SUB_TYPE:
            LOG_ERR("IResourceRecovery::reqFreeTicketRecovery error type", subType)
            return
        if num <= 0:
            LOG_WARN("IResourceRecovery::reqFreeTicketRecovery num", num)
            return
        if not self.checkGameConfigEnable(subType):
            return
        if not self.checkFreeTicketNumConfig(subType):
            return

        deductWealthVal = dropAward.DeductWealthVal()
        costInfo = []
        leftNum = self.calFreeTicketRecovery(subType, num, deductWealthVal, costInfo, None)
        if leftNum == num:
            return
        
        addNum = num - leftNum
        if not self.canDeductWealth(deductWealthVal):
            self.onMessagePre(MMD.datas.workShop_currencyLack, [])
            LOG_INFO("IResourceRecovery::reqFreeTicketRecovery cannot deductWealth", costInfo)
            return
        
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, deductWealthVal, opUUID, detail)
        LOG_DBG("IResourceRecovery::reqFreeTicketRecovery deductWealth", costInfo)

        clientDataList = []
        clientDataList.append({'subType': subType + 1, 'num': addNum})
        self.recoveryFreeTicket(subType, addNum, costInfo, opUUID)
        LOG_DBG("IResourceRecovery::reqFreeTicketRecovery clientDataList", clientDataList)
        self.client.onFreeTicketOneClickRecoveryInfo(clientDataList)

    def recoveryFreeTicket(self, subType, addNum, costInfo, opUUID):
        durationCostList = []
        infoList = self.freeTicketUseInfo.get(subType, [])
        for cInfo in costInfo:
            for idx, info in enumerate(infoList):
                if cInfo[0] != info[0]:
                    continue
                info[1] -= cInfo[1]
                durationCostList.append([len(infoList) - idx - 1, cInfo[1], cInfo[2], cInfo[1] * cInfo[3]])
                break

        if subType in (gameconst.FreeTicketSubType.CRUSADE, gameconst.FreeTicketSubType.CHIEF):
            self.subType2FreeTicketInfo[subType][1](self)(0, addNum, {}, False)
        else:
            self.subType2FreeTicketInfo[subType][1](self)(addNum, AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, opUUID)

        self.updateFreeTicketRecoveryInfo(subType)
        LogTrackingMgr.LogTrackingMgr.resource_recovery(
            self.gbID,
            self.accountEntity.clientDistinctId,
            subType + 1,
            addNum,
            durationCostList,
        )

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('welfare_resourceRecovery')
    def reqFreeTicketOneClickRecovery(self, exposed, rType):
        LOG_INFO("IResourceRecovery::reqFreeTicketOneClickRecovery", rType)
        if rType not in gameconst.FreeTicketOneClickRecoveryType.VALID_ONE_CLICK_TYPE:
            LOG_ERR("IResourceRecovery::reqFreeTicketOneClickRecovery error type", rType)
            return
        
        checkRTypeFunc = None
        recoveryDict = {}
        costInfoDict = {}
        deductWealthVal = dropAward.DeductWealthVal()
        if rType == gameconst.FreeTicketOneClickRecoveryType.FREE:
            checkRTypeFunc = lambda val: val == 0
        elif rType == gameconst.FreeTicketOneClickRecoveryType.PAID:
            checkRTypeFunc = lambda val: val > 0
        for subType in gameconst.FreeTicketSubType.VALID_SUB_TYPE:
            if not self.checkFreeTicketNumConfig(subType):
                continue
            if not self.checkGameConfigEnable(subType):
                continue
            num = gameconst.UINT32_MAX
            costInfo = []
            leftNum = self.calFreeTicketRecovery(subType, num, deductWealthVal, costInfo, checkRTypeFunc)
            if leftNum == num:
                continue
            addNum = num - leftNum
            recoveryDict[subType] = addNum
            costInfoDict[subType] = costInfo

        if not recoveryDict:
            self.client.onFreeTicketOneClickRecoveryInfo([])
            return

        if not self.canDeductWealth(deductWealthVal):
            self.onMessagePre(MMD.datas.workShop_currencyLack, [])
            LOG_INFO("IResourceRecovery::reqFreeTicketOneClickRecovery cannot deductWealth", costInfoDict)
            return

        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, deductWealthVal, opUUID, detail)
        LOG_DBG("IResourceRecovery::reqFreeTicketOneClickRecovery deductWealth", costInfoDict)

        clientDataList = []
        for subType, addNum in recoveryDict.items():
            costInfo = costInfoDict[subType]
            self.recoveryFreeTicket(subType, addNum, costInfo, opUUID)
            clientDataList.append({'subType': subType + 1, 'num': addNum})
        LOG_DBG("IResourceRecovery::reqFreeTicketOneClickRecovery clientDataList", clientDataList)
        self.client.onFreeTicketOneClickRecoveryInfo(clientDataList)

    def onUpdateFreeTicketNumConfig(self, subType):
        leftNum = self.subType2FreeTicketInfo[subType][0](self)
        LOG_INFO("IResourceRecovery::onUpdateFreeTicketNumConfig", subType, leftNum)
        self.subType2FreeTicketInfo[subType][2](self)(gameconst.CycleEventTriggerType.UPDATE)
