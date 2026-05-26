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
import message_Message_def as MMD


class IResourceRecovery(object):
    def __init__(self):
        LOG_DBG("IResourceRecovery::__init__")

    def resourceRecoveryOnLogin(self):
        LOG_INFO("IResourceRecovery::resourceRecoveryOnLogin")

        subType = gameconst.FreeTicketSubType.WONDER_LAND
        self.updateFreeTicketInfo(subType, self.wonderLandTicket, gameconst.FreeTicketUpdateType.LOGIN)
        subType = gameconst.FreeTicketSubType.CUBE
        self.updateFreeTicketInfo(subType, self.leftCubeTimes, gameconst.FreeTicketUpdateType.LOGIN)

    def resourceRecoveryOnOffline(self):
        LOG_INFO("IResourceRecovery::resourceRecoveryOnOffline")

        subType = gameconst.FreeTicketSubType.WONDER_LAND
        self.updateFreeTicketInfo(subType, self.wonderLandTicket, gameconst.FreeTicketUpdateType.OFFLINE, self.tLastUpdateTime)
        subType = gameconst.FreeTicketSubType.CUBE
        self.updateFreeTicketInfo(subType, self.leftCubeTimes, gameconst.FreeTicketUpdateType.OFFLINE, self.tLastUpdateTime)

    def getCfgNumByDateTime(self, subType, dateTime):
        cfgList = gameglobal.freeTicketNumConfig.get(subType, [])
        for cfgIdx, cfgInfo in enumerate(cfgList):
            if cfgList[cfgIdx][0] <= dateTime and cfgIdx + 1 < len(cfgList) and dateTime < cfgList[cfgIdx + 1][0]:
                return cfgList[cfgIdx][1]
        return 0

    def updateFreeTicketInfo(self, subType, leftNum, reason, now=0):
        now = now if now else utils.curTS()
        curDateTime = utils.getIntDateTime(now)
        LOG_INFO("IResourceRecovery::updateFreeTicketInfo", now, curDateTime, subType, leftNum, reason)
        LOG_INFO("IResourceRecovery::updateFreeTicketInfo", gameglobal.freeTicketNumConfig.get(subType, []))
        LOG_INFO("IResourceRecovery::updateFreeTicketInfo", self.freeTicketUseInfo.get(subType, []))
        return
        infoList = self.freeTicketUseInfo.setdefault(subType, [])
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo2", infoList)
        lastData = infoList[-1] if infoList else None

        if reason == gameconst.FreeTicketUpdateType.LOGIN or reason == gameconst.FreeTicketUpdateType.OFFLINE:
            LOG_WARN("IResourceRecovery::updateFreeTicketInfo3", lastData, curDateTime)
            if not lastData or lastData[0] < curDateTime:
                infoList.append([curDateTime, leftNum])
            elif lastData[0] == curDateTime:
                lastData[1] = leftNum
            else:
                return
        elif reason == gameconst.FreeTicketUpdateType.RESET or reason == gameconst.FreeTicketUpdateType.UPDATE:
            curDataTimestamp = utils.getIntTimestamp(str(curDateTime) + gameconst.RESOURCE_RECOVER_TIME_POINT_STR)
            preDataTimestamp = curDataTimestamp - 86400
            preDataTime = utils.getIntDateTime(preDataTimestamp)
            LOG_DBG("IResourceRecovery::updateFreeTicketInfo5", lastData, preDataTime)
            if not lastData or lastData[0] < preDataTime:
                infoList.append([preDataTime, leftNum])
            elif lastData[0] == preDataTime:
                lastData[1] = leftNum
            else:
                return

        LOG_DBG("IResourceRecovery::updateFreeTicketInfo6", infoList)

        cfgList = gameglobal.freeTicketNumConfig.get(subType, [])
        if not cfgList:
            LOG_WARN("IResourceRecovery::updateFreeTicketInfo6")
            return
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
                    break
                else:
                    adjIdx += 1

        self.freeTicketUseInfo[subType] = adjInfoList
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo11", self.freeTicketUseInfo[subType])
    
    def updateFreeTicketRecoveryInfo(self, subType):
        cfgData = W_RR.datas.get(subType + 1, {})
        if not cfgData:
            LOG_ERR("IResourceRecovery::updateFreeTicketRecoveryInfo no cfg", subType + 1)
            return
        LOG_INFO("IResourceRecovery::updateFreeTicketRecoveryInfo", self.freeTicketUseInfo[subType], cfgData)
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

    def reqFreeTicketRecovery(self, exposed, subType, num):
        LOG_INFO("IResourceRecovery::reqFreeTicketRecovery", num, subType - 1)
        subType -= 1
        if subType not in gameconst.FreeTicketSubType.VALID_SUB_TYPE:
            LOG_ERR("IResourceRecovery::reqFreeTicketRecovery error type", subType)
            return
        if num <= 0:
            LOG_WARN("IResourceRecovery::reqFreeTicketRecovery num", num)
            return

        leftNum = num
        costInfo = []
        deductWealthVal = dropAward.DeductWealthVal()
        recoveryInfo = self.freeTickeRecoveryInfo.get(subType, [])
        copyRecoveryInfo = copy.deepcopy(recoveryInfo)
        for info in copyRecoveryInfo:
            if info[1] <= 0:
                continue
            n = min(leftNum, info[1])
            leftNum -= n
            info[1] -= n
            if info[2] and info[3]:
                deductWealthVal.addWealthByItemId(info[2], n * info[3])
            costInfo.append([info[0], n, info[2], info[3]])
            if leftNum <= 0:
                break

        if leftNum == num:
            return
        
        if not self.canDeductWealth(deductWealthVal):
            self.onMessagePre(MMD.datas.workShop_currencyLack, [])
            LOG_INFO("IResourceRecovery::reqFreeTicketRecovery cannot deductWealth", costInfo)
            return
        
        detail = gameclass.AwardDetail()
        opUUID = KBEngine.genUUID64()
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, deductWealthVal, opUUID, detail)
        LOG_DBG("IResourceRecovery::reqFreeTicketRecovery deductWealth", costInfo)

        infoList = self.freeTicketUseInfo.get(subType, [])
        for cInfo in costInfo:
            for info in infoList:
                if cInfo[0] != info[0]:
                    continue
                info[1] -= cInfo[1]
                break

        addNum = num - leftNum
        if subType == gameconst.FreeTicketSubType.WONDER_LAND:
            self.modifyWonderLandTicket(addNum, AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, opUUID)
        elif subType == gameconst.FreeTicketSubType.CUBE:
            self.modifyLeftCubeTimes(addNum, AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, opUUID)

        self.updateFreeTicketRecoveryInfo(subType)

    def onUpdateFreeTicketNumConfig(self, subType):
        LOG_INFO("IResourceRecovery::onUpdateFreeTicketNumConfig", subType)
        leftNum = 0
        if subType == gameconst.FreeTicketSubType.WONDER_LAND:
            leftNum = self.wonderLandTicket
        elif subType == gameconst.FreeTicketSubType.CUBE:
            leftNum = self.leftCubeTimes
        self.updateFreeTicketInfo(subType, leftNum, gameconst.FreeTicketUpdateType.UPDATE)