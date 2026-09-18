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
            gameconst.RecoveryTicketSubType.CUBE            :   [
                                                                lambda self: self.leftCubeDailyUseCoinFreeNum,
                                                                lambda self: self.modifyLeftCubeTimes, 
                                                                lambda self: self._cubeDailyRefresh,
                                                                lambda self: self.updateCubeUseCoinTimesTicketInfo,
                                                                lambda self: self.tryAddCubeUseCoinTimesFreeTicket,
                                                                lambda self: self.sendCubeUseCoinTimesTicketInfo,
                                                            ],
            gameconst.RecoveryTicketSubType.WONDER_LAND     :   [
                                                                lambda self: self.leftWonderLandDailyUseCoinFreeNum, 
                                                                lambda self: self.modifyWonderLandTicket, 
                                                                lambda self: self._wonderLandRefreshDaily,
                                                                lambda self: self.updateWonderLandUseCoinTimesTicketInfo,
                                                                lambda self: self.tryAddWonderLandUseCoinTimesFreeTicket,
                                                                lambda self: self.sendWonderLandUseCoinTimesTicketInfo,
                                                            ],
            gameconst.RecoveryTicketSubType.ABYSS           :   [
                                                                lambda self: self.leftAbyssDailyUseCoinFreeNum, 
                                                                lambda self: self.modifyAbyssTicket, 
                                                                lambda self: self._abyssRefreshDaily,
                                                                lambda self: self.updateAbyssUseCoinTimesTicketInfo,
                                                                lambda self: self.tryAddAbyssUseCoinTimesFreeTicket,
                                                                lambda self: self.sendAbyssUseCoinTimesTicketInfo,
                                                            ],
            gameconst.RecoveryTicketSubType.CRUSADE         :   [
                                                                lambda self: self.leftCrusadDailyUseCoinFreeNum, 
                                                                lambda self: self.onUseCoinToIncreaseCrusadeRewardNumber, 
                                                                lambda self: self.onCrusadeDailyRewardNumUpdate,
                                                                lambda self: self.updateCrusadeUseCoinTimesTicketInfo,
                                                                lambda self: self.tryAddCrusadeUseCoinTimesFreeTicket,
                                                                lambda self: self.sendCrusadeUseCoinTimesTicketInfo,
                                                            ],
            gameconst.RecoveryTicketSubType.CHIEF           :   [
                                                                lambda self: self.leftChiefDailyUseCoinFreeNum, 
                                                                lambda self: self.onUseCoinToIncreaseChiefRewardNumber, 
                                                                lambda self: self.onChiefDailyRewardNumUpdate,
                                                                lambda self: self.updateChiefUseCoinTimesTicketInfo,
                                                                lambda self: self.tryAddChiefUseCoinTimesFreeTicket,
                                                                lambda self: self.sendChiefUseCoinTimesTicketInfo,
                                                            ],
        }

    def freeTicketDailyRefresh(self):
        # 兼容已开服的情况
        if self.tRecoveryLastUpdateTime == 0 and self.tLastUpdateTime != 0:
            self.tRecoveryLastUpdateTime = self.tLastUpdateTime
        LOG_INFO("IResourceRecovery::freeTicketDailyRefresh", self.tRecoveryLastUpdateTime)
        if self.tRecoveryLastUpdateTime <= 0:
            self.tRecoveryLastUpdateTime = utils.curTS()
            return
        if not utils.checkDiffDay(utils.curTS(), self.tRecoveryLastUpdateTime, gameconst.GENERAL_CYCLE_TIME):
            return
        
        LOG_INFO("IResourceRecovery::freeTicketDailyRefresh LOGIN")
        self.onResetFreeTicketNum(list(gameconst.RecoveryTicketSubType.VALID_SUB_TYPE), gameconst.CycleEventTriggerType.LOGIN)

    def sendAllRecoveryInfo(self):
        LOG_INFO("IResourceRecovery::sendAllRecoveryInfo")
        for subType in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            self.updateFreeTicketRecoveryInfo(gameconst.RecoveryTicketType.FREE_TICKET, subType)
            self.updateFreeTicketRecoveryInfo(gameconst.RecoveryTicketType.PAID_TICKET, subType)

    def resourceRecoveryOnLogin(self):
        cellNovice = self.getTempMiscProp(gameconst.EntityPropsEnum.cellNovice, 0)
        LOG_INFO("IResourceRecovery::resourceRecoveryOnLogin cellNovice", cellNovice)
        if cellNovice:
            return
        LOG_INFO("IResourceRecovery::resourceRecoveryOnLogin", self.tRecoveryLastUpdateTime)
        now = self.tRecoveryLastUpdateTime if self.tRecoveryLastUpdateTime else utils.curTS()
        level = self.getRoleCacheAttr('level')
        for subType in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.UPDATE_USE_COIN_TICKET_INFO_FUNC](self)(now, level)
            freeLeftNum, paidLeftNum = self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.LEFT_USE_COIN_NUM_ATTR](self)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, subType, freeLeftNum, gameconst.FreeTicketUpdateType.LOGIN)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, subType, paidLeftNum, gameconst.FreeTicketUpdateType.LOGIN)

    def resourceRecoveryOnOffline(self):
        LOG_INFO("IResourceRecovery::resourceRecoveryOnOffline")
        for subType in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            freeLeftNum, paidLeftNum = self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.LEFT_USE_COIN_NUM_ATTR](self)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, subType, freeLeftNum, gameconst.FreeTicketUpdateType.OFFLINE, self.tRecoveryLastUpdateTime)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, subType, paidLeftNum, gameconst.FreeTicketUpdateType.OFFLINE, self.tRecoveryLastUpdateTime)

    def getCfgNumByDateTime(self, mainType, subType, dateTime):
        cfgList = gameglobal.freeTicketNumConfig.get(mainType, {}).get(subType, [])
        for cfgIdx, cfgInfo in enumerate(cfgList):
            if cfgList[cfgIdx][0] <= dateTime and cfgIdx + 1 < len(cfgList) and dateTime < cfgList[cfgIdx + 1][0]:
                return cfgList[cfgIdx][1]
        return 0

    def checkFreeTicketNumConfig(self, mainType, subType):
        if not gameglobal.freeTicketNumConfig.get(mainType, {}).get(subType, []):
            LOG_WARN("IResourceRecovery::checkFreeTicketNumConfig not serverOpenTime", mainType, subType)
            return False
        return True

    def checkRRGameConfigEnable(self, subType):
        cfgData = W_RR.datas.get(subType, {})
        if not cfgData:
            LOG_ERR("IResourceRecovery::checkRRGameConfigEnable no cfg", subType)
            return False
        condition = cfgData['condition']
        conditionType = V_VD.datas.get(condition).get("type", "")
        if not gameconfig.visibleConfigEnabled(conditionType):
            LOG_WARN("IResourceRecovery::checkRRGameConfigEnable not open", conditionType)
            return False
        if not self._isUIVisibleStr(condition):
            LOG_WARN("IResourceRecovery::checkRRGameConfigEnable not lock", condition)
            return False

        return True

    def updateFreeTicketInfo(self, mainType, subType, leftNum, reason, now=0):
        if not self.checkFreeTicketNumConfig(mainType, subType):
            return
        now = now if now else utils.curTS()
        curDateTime = utils.getIntDateTime(now)
        LOG_INFO("IResourceRecovery::updateFreeTicketInfo", now, curDateTime, mainType, subType, leftNum, reason)
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo", gameglobal.freeTicketNumConfig.get(mainType, {}).get(subType, []))
        LOG_DBG("IResourceRecovery::updateFreeTicketInfo", self.freeTicketUseInfo.get(mainType, {}).get(subType, []))
        infoList = self.freeTicketUseInfo.setdefault(mainType, {}).setdefault(subType, [])
        cfgList = gameglobal.freeTicketNumConfig.get(mainType, {}).get(subType, [])
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

        self.freeTicketUseInfo[mainType][subType] = adjInfoList
        LOG_INFO("IResourceRecovery::updateFreeTicketInfo11", self.freeTicketUseInfo[mainType][subType])
        self.updateFreeTicketRecoveryInfo(mainType, subType)
    
    def updateFreeTicketRecoveryInfo(self, mainType, subType):
        if not self.checkFreeTicketNumConfig(mainType, subType):
            return
        cfgData = W_RR.datas.get(subType, {})
        if not cfgData:
            LOG_ERR("IResourceRecovery::updateFreeTicketRecoveryInfo no cfg", subType)
            return
        LOG_DBG("IResourceRecovery::updateFreeTicketRecoveryInfo", self.freeTicketUseInfo.get(mainType, {}).get(subType, []), cfgData)
        infoList = self.freeTicketUseInfo.get(mainType, {}).get(subType, [])
        costCfg = tuple(cfgData['cost'][mainType - 1])
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
        self.freeTickeRecoveryInfo.setdefault(mainType, {})[subType] = recoveryInfoList
        
        LOG_DBG("IResourceRecovery::updateFreeTicketRecoveryInfo recoveryInfoList", self.freeTickeRecoveryInfo[mainType][subType])
        LOG_INFO("IResourceRecovery::updateFreeTicketRecoveryInfo clientDataList", clientDataList)
        self.client.onFreeTicketRecoveryInfo(subType, clientDataList, mainType)

    def calFreeTicketRecovery(self, mainType, subType, num, deductWealthVal, costInfo, checkRTypeFunc=None):
        leftNum = num
        freeAddNum = 0
        paidAddNum = 0
        recoveryInfo = self.freeTickeRecoveryInfo.get(mainType, {}).get(subType, [])
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
                paidAddNum += n
            else:
                freeAddNum += n
            costInfo.append([info[0], n, info[2], info[3]])
            if leftNum <= 0:
                break

        return leftNum, freeAddNum, paidAddNum

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('welfare_resourceRecovery')
    def reqFreeTicketRecovery(self, exposed, subType, num, mainType):
        LOG_INFO("IResourceRecovery::reqFreeTicketRecovery", num, mainType, subType)
        if mainType not in gameconst.RecoveryTicketType.VALID_TYPE:
            LOG_ERR("IResourceRecovery::reqFreeTicketRecovery error mainType", mainType)
            return
        if subType not in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            LOG_ERR("IResourceRecovery::reqFreeTicketRecovery error subType", subType)
            return
        if num <= 0:
            LOG_WARN("IResourceRecovery::reqFreeTicketRecovery num", num)
            return
        if not self.checkRRGameConfigEnable(subType):
            return
        if not self.checkFreeTicketNumConfig(mainType, subType):
            return

        deductWealthVal = dropAward.DeductWealthVal()
        costInfo = []
        leftNum, freeAddNum, paidAddNum = self.calFreeTicketRecovery(mainType, subType, num, deductWealthVal, costInfo, None)
        if leftNum == num:
            return
        
        addNum = num - leftNum
        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_INFO("IResourceRecovery::reqFreeTicketRecovery cannot deductWealth", costInfo, res())
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                return
            self.onMessagePre(MMD.datas.workShop_currencyLack, [])
            return
        
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, deductWealthVal, opUUID, detail)
        LOG_DBG("IResourceRecovery::reqFreeTicketRecovery deductWealth", costInfo)

        clientDataList = []
        clientDataList.append({'subType': subType, 'num': addNum, 'mainType': mainType})
        self.recoveryFreeTicket(mainType, subType, addNum, costInfo, opUUID, freeAddNum, paidAddNum)
        LOG_INFO("IResourceRecovery::reqFreeTicketRecovery clientDataList", clientDataList)
        self.client.onFreeTicketOneClickRecoveryInfo(clientDataList)

    def recoveryFreeTicket(self, mainType, subType, addNum, costInfo, opUUID, freeAddNum, paidAddNum):
        durationCostList = []
        infoList = self.freeTicketUseInfo.get(mainType, {}).get(subType, [])
        for cInfo in costInfo:
            for idx, info in enumerate(infoList):
                if cInfo[0] != info[0]:
                    continue
                info[1] -= cInfo[1]
                durationCostList.append([len(infoList) - idx - 1, cInfo[1], cInfo[2], cInfo[1] * cInfo[3]])
                break

        if subType in (gameconst.RecoveryTicketSubType.CRUSADE, gameconst.RecoveryTicketSubType.CHIEF):
            self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.MODIFY_TICKET_NUM_FUNC](self)(addNum, addNum, {}, freeAddNum, paidAddNum, gameconst.addTicketTimesType.RECOVERY, False)
        else:
            self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.MODIFY_TICKET_NUM_FUNC](self)(addNum, freeAddNum, paidAddNum, AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, opUUID, gameconst.addTicketTimesType.RECOVERY)

        self.updateFreeTicketRecoveryInfo(mainType, subType)
        LogTrackingMgr.LogTrackingMgr.resource_recovery(
            self.gbID,
            self.accountEntity.clientDistinctId,
            subType,
            addNum,
            durationCostList,
            mainType,
        )

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('welfare_resourceRecovery')
    def reqFreeTicketOneClickRecovery(self, exposed, rType, mainType):
        LOG_INFO("IResourceRecovery::reqFreeTicketOneClickRecovery", rType, mainType)
        if mainType not in gameconst.RecoveryTicketType.VALID_TYPE:
            LOG_ERR("IResourceRecovery::reqFreeTicketOneClickRecovery error mainType", mainType)
            return
        if rType not in gameconst.FreeTicketOneClickRecoveryType.VALID_ONE_CLICK_TYPE:
            LOG_ERR("IResourceRecovery::reqFreeTicketOneClickRecovery error rType", rType)
            return
        
        checkRTypeFunc = None
        recoveryDict = {}
        costInfoDict = {}
        deductWealthVal = dropAward.DeductWealthVal()
        if rType == gameconst.FreeTicketOneClickRecoveryType.FREE:
            checkRTypeFunc = lambda val: val == 0
        elif rType == gameconst.FreeTicketOneClickRecoveryType.PAID:
            checkRTypeFunc = lambda val: val > 0
        for subType in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            if not self.checkFreeTicketNumConfig(mainType, subType):
                continue
            if not self.checkRRGameConfigEnable(subType):
                continue
            num = gameconst.UINT32_MAX
            costInfo = []
            leftNum, freeAddNum, paidAddNum = self.calFreeTicketRecovery(mainType, subType, num, deductWealthVal, costInfo, checkRTypeFunc)
            if leftNum == num:
                continue
            addNum = num - leftNum
            recoveryDict[subType] = (addNum, freeAddNum, paidAddNum)
            costInfoDict[subType] = costInfo

        if not recoveryDict:
            self.client.onFreeTicketOneClickRecoveryInfo([])
            return

        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_INFO("IResourceRecovery::reqFreeTicketOneClickRecovery cannot deductWealth", costInfoDict, res())
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                return
            self.onMessagePre(MMD.datas.workShop_currencyLack, [])
            return

        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        self.deductWealth(AAC_AACDD.datas.BONUS_SRC_RECOVERY_TICKET, deductWealthVal, opUUID, detail)
        LOG_DBG("IResourceRecovery::reqFreeTicketOneClickRecovery deductWealth", costInfoDict)

        clientDataList = []
        for subType, (addNum, freeAddNum, paidAddNum) in recoveryDict.items():
            costInfo = costInfoDict[subType]
            self.recoveryFreeTicket(mainType, subType, addNum, costInfo, opUUID, freeAddNum, paidAddNum)
            clientDataList.append({'subType': subType, 'num': addNum, 'mainType': mainType})
        LOG_INFO("IResourceRecovery::reqFreeTicketOneClickRecovery clientDataList", clientDataList)
        self.client.onFreeTicketOneClickRecoveryInfo(clientDataList)

    def onUpdateFreeTicketNumConfig(self, subTypeList):
        LOG_INFO("IResourceRecovery::onUpdateFreeTicketNumConfig", subTypeList)
        self.onResetFreeTicketNum(subTypeList, gameconst.CycleEventTriggerType.UPDATE)

    def onResetFreeTicketNum(self, subTypeList, tType):
        LOG_INFO("IResourceRecovery::onResetFreeTicketNum", subTypeList, tType)
        now = utils.curTS()
        level = self.getRoleCacheAttr('level')
        for subType in subTypeList:
            self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.DAILY_REFRESH_FUNC](self)(tType)
            self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.UPDATE_USE_COIN_TICKET_INFO_FUNC](self)(now, level)
        self.tRecoveryLastUpdateTime = now

    def onUpdateUseCoinTimesTicketInfoCross(self):
        self.onUpdateUseCoinTimesTicketInfo(self.getRoleCacheAttr('level'))

    def onUpdateUseCoinTimesTicketInfo(self, level):
        LOG_INFO("IResourceRecovery::onUpdateUseCoinTimesTicketInfo", level)
        now = self.tRecoveryLastUpdateTime if self.tRecoveryLastUpdateTime else utils.curTS()
        for subType in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.UPDATE_USE_COIN_TICKET_INFO_FUNC](self)(now, level)

    def onTryAddUseCoinTimesFreeTicket(self, subType):
        LOG_INFO("IResourceRecovery::onTryAddUseCoinTimesFreeTicket", subType)
        if subType not in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            return
        self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.TRY_ADD_USE_COIN_FREE_TICKET_FUNC](self)()

    def onSendUseCoinTimesTicketInfo(self):
        LOG_INFO("IResourceRecovery::onSendUseCoinTimesTicketInfo")
        for subType in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
            self.subType2FreeTicketInfo[subType][gameconst.SubType2TicketInfoIdx.SEND_USE_COIN_TICKET_INFO_FUNC](self)()