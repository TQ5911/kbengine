# coding: utf-8

from KBEDebug import *

import KBEngine
import gameclass
import dropAward
import utils
import wonderLand_config as WL_CD
import wonderLand_floor as WL_FD
import gameengine
import gameconst
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import itemData_itemData as ID_IDD
import activityControl_config as AC_CD
import gamedecorator
import LogTrackingMgr
import visible_visible as V_VD
import creep_base as CBD
import activityControl_activityTicket as AC_AT


class IWonderLandBase(object):
    def __init__(self):
        pass

    def _wonderLandRefreshDaily(self, *args):
        tType = args[0] if len(args) >= 1 else 0
        LOG_INFO("IWonderLandBase::_wonderLandRefreshDaily", tType)
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            freeLeftNum, paidLeftNum = self.leftWonderLandDailyUseCoinFreeNum
            LOG_INFO("IWonderLandBase::_wonderLandRefreshDaily", freeLeftNum, paidLeftNum)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, gameconst.RecoveryTicketSubType.WONDER_LAND, freeLeftNum, gameconst.FreeTicketUpdateType.UPDATE)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, gameconst.RecoveryTicketSubType.WONDER_LAND, paidLeftNum, gameconst.FreeTicketUpdateType.UPDATE)

        self.wonderLandAddTimes = len(AC_AT.ticketIdDic[gameconst.RecoveryTicketSubType.WONDER_LAND])

    @property
    def leftWonderLandDailyUseCoinFreeNum(self):
        LOG_INFO("IWonderLandBase::leftWonderLandDailyUseCoinFreeNum", self.wonderLandAddTimes)
        if not self.wonderLandAddTimes:
            return 0, 0
        leftFreeNum = 0
        leftPaidNum = 0
        for times in range(self.wonderLandAddTimes, 0, -1): 
            res, beFree = utils.isOriginaCoinCostBeFree(gameconst.RecoveryTicketSubType.WONDER_LAND, times)
            if not res:
                LOG_ERR("IWonderLandBase::leftWonderLandDailyUseCoinFreeNum error", times)
                continue
            if beFree:
                leftFreeNum += 1
            else:
                leftPaidNum += 1
        return leftFreeNum, leftPaidNum

    def updateWonderLandUseCoinTimesTicketInfo(self, time, level):
        self.wonderLandCoinTicketData.clear()
        for times in range(len(AC_AT.ticketIdDic[gameconst.RecoveryTicketSubType.WONDER_LAND]), 0, -1): 
            itemId, itemNum, discountType = utils.getCoinCostInfo(self, gameconst.RecoveryTicketSubType.WONDER_LAND, times, time, level)
            self.wonderLandCoinTicketData.append(itemId, itemNum, discountType)
        LOG_INFO("IWonderLandBase::updateWonderLandUseCoinTimesTicketInfo", time, self.wonderLandAddTimes, level, self.wonderLandCoinTicketData)
        self.sendWonderLandUseCoinTimesTicketInfo()

    def sendWonderLandUseCoinTimesTicketInfo(self):
        self.client.onUseCoinTimesTicketDatas(gameconst.RecoveryTicketSubType.WONDER_LAND, self.wonderLandCoinTicketData.getClientDatas())

    def tryAddWonderLandUseCoinTimesFreeTicket(self):
        LOG_INFO("IWonderLandBase::tryAddWonderLandUseCoinTimesFreeTicket", self.wonderLandTicket, self.wonderLandAddTimes)
        if self.wonderLandTicket > 0:
            LOG_DBG("IWonderLandBase::tryAddWonderLandUseCoinTimesFreeTicket has coin free ticket")
            return
        if self.wonderLandAddTimes <= 0:
            LOG_DBG("IWonderLandBase::tryAddWonderLandUseCoinTimesFreeTicket wonderLandAddTimes <= 0 ")
            return
        itemId, itemNum, discountType = self.wonderLandCoinTicketData.getTicketInfo(self.wonderLandAddTimes)
        if not itemId:
            LOG_ERR("IWonderLandBase:tryAddWonderLandUseCoinTimesFreeTicket error", self.wonderLandCoinTicketData)
            return
        if itemNum:
            LOG_DBG("IWonderLandBase::tryAddWonderLandUseCoinTimesFreeTicket not free")
            return
        self.doAddWonderLandTicket(gameconst.CUBE_ADD_TIMES_TYPE_COIN, [(itemId, itemNum, 1)], 1, 
                                 False, True, gameconst.WonderAddTicketReason.ADD_FREE, KBEngine.genUUID64())

    def sumWonderLandTicket(self):
        return self.wonderLandTicket + self.paidWonderLandTicket

    def checkAndEnterWonderLand(self, floor, bossMutexLine=0xFFFF):
        if self.sumWonderLandTicket() <= 0:
            LOG_WARN('IWonderLandBase::checkAndEnterWonderLand: self.sumWonderLandTicket <= 0')
            return

        mapId = WL_FD.datas[floor]['ID']
        extra = {
            'enterWonderLandType': gameconst.WONDER_LAND_ENTER_TYPE_TICKET,
            'floor': floor,
        }
        # 0xFFFF 表示无优先分线
        if bossMutexLine != 0xFFFF:
            extra['bossMutexLine'] = bossMutexLine
        gameengine.getWonderLandStub(mapId).doEnterWonderLand(self, self.gbID, extra)

    def afterEnterWonderLandDeductTimes(self, extra):
        floor = extra.get('floor', 0)
        freeNum, paidNum = self.modifyWonderLandTicket(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_ENTER_WONDER_LAND, KBEngine.genUUID64(), gameconst.addTicketTimesType.NULL)
        ticketType = gameconst.WONDER_LAND_ENTER_TICKET_FREE if freeNum else gameconst.WONDER_LAND_ENTER_TICKET_PAID
        if floor:
            LogTrackingMgr.LogTrackingMgr.wonderland_enter(
                self.gbID,
                self.accountEntity.clientDistinctId, 
                floor,
                utils.curTS(),
                ticketType,
                1,
            )

    @gamedecorator.checkGameconfigEnable('wonderLand')
    def addWonderLandTicket(self, exposed, addType, num, isAddDuration):
        LOG_INFO('IWonderLandBase::addWonderLandTicket: addType: {}, num: {}, isAddDuration: {} {}'.format(addType, num, isAddDuration, self.wonderLandAddTimes))
        if not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']) and isAddDuration:
            self.onMessagePre(AC_CD.datas['activity_notOpen']['value'], [])
            return
        if addType not in gameconst.VALID_ADD_TIMES_TYPE:
            LOG_INFO('IWonderLandBase::addWonderLandTicket error addType')
            return

        _opUUID = KBEngine.genUUID64()
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_NULL:
            if self.sumWonderLandTicket() <= 0:
                LOG_ERR('IWonderLandBase::addWonderLandTicket: sumWonderLandTicket <= 0')
                return

            freeNum, paidNum = self.modifyWonderLandTicket(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_ADD_WONDER_LAND_TIMES, _opUUID, gameconst.addTicketTimesType.NULL)
            self.cell.directlyAddWonderLandDuration('addWonderLandDurationFailedRewindTimes', (_opUUID, freeNum, paidNum, ))
            return

        costList = []
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            itemId = WL_CD.datas['wonderLandNumItem']['value']
            itemNum = 1
            costList.append((itemId, itemNum, num))
        else:
            num = min(num, self.wonderLandAddTimes)
            if num <= 0:
                LOG_ERR('addWonderLandTicket: num <= 0')
                return
            for times in range(self.wonderLandAddTimes, (self.wonderLandAddTimes - num), -1):
                itemId, itemNum, discountType = self.wonderLandCoinTicketData.getTicketInfo(times)
                if not itemId:
                    LOG_ERR('addWonderLandTicket: invalid wonderLandAddTimes', times)
                    return
                costList.append((itemId, itemNum, 1))
        LOG_INFO('IWonderLandBase::addWonderLandTicket: addType: {}, costList: {}, num: {}'.format(addType, costList, num))
        self.doAddWonderLandTicket(addType, costList, num, isAddDuration, False, gameconst.WonderAddTicketReason.FROM_CLIENT, _opUUID)

    def modifyWonderLandTicket(self, delta, freeNum, paidNum, src, opUUID, attType=gameconst.addTicketTimesType.NULL):
        befPaidWonderLandTicket = self.paidWonderLandTicket
        befWonderLandTicket = self.wonderLandTicket
        if delta > 0:
            if attType == gameconst.addTicketTimesType.COIN:
                self.wonderLandTicket = min(1000000000, self.wonderLandTicket + freeNum)
                self.paidWonderLandTicket = min(1000000000, self.paidWonderLandTicket + paidNum)
            else:
                self.paidWonderLandTicket = min(1000000000, self.paidWonderLandTicket + delta)

        else:
            if attType == gameconst.addTicketTimesType.COIN:
                self.wonderLandTicket = max(0, self.wonderLandTicket + freeNum)
                self.paidWonderLandTicket = max(0, self.paidWonderLandTicket + paidNum)
            else:
                if self.wonderLandTicket >= -delta:
                    self.wonderLandTicket += delta

                else:
                    self.paidWonderLandTicket = max(0, self.paidWonderLandTicket + self.wonderLandTicket + delta)
                    self.wonderLandTicket = 0

        LogTrackingMgr.LogTrackingMgr.WonderLand_Ticket(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            src,
            delta,
            self.wonderLandTicket,
            self.paidWonderLandTicket,
            opUUID,
        )
        LOG_INFO('modifyWonderLandTicket:', attType, delta, freeNum, paidNum, src, befPaidWonderLandTicket, self.paidWonderLandTicket, befWonderLandTicket, self.wonderLandTicket)
        return befWonderLandTicket - self.wonderLandTicket, befPaidWonderLandTicket - self.paidWonderLandTicket

    def doAddWonderLandTicket(self, addType, costList, num, isAddDuration, hasCheckCell, reason, opUUID):
        LOG_INFO('IWonderLandBase::doAddWonderLandTicket: addType: {}, costList: {}, num: {}, isAddDuration: {}, hasCheckCell: {}, reason: {}'.format(addType, costList, num, isAddDuration, hasCheckCell, reason))
        if isAddDuration and num != 1:
            LOG_ERR('IWonderLandBase::addWonderLandTicket: invalid num: {}'.format(num))
            return

        if isAddDuration and not hasCheckCell:
            self.cell.checkAddWonderLandDurationCondition(addType, costList, num, opUUID)
            return

        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            if num > self.wonderLandAddTimes:
                LOG_ERR('IWonderLandBase::addWonderLandTicket: num > wonderLandAddTimes')
                return

        elif addType == gameconst.CUBE_ADD_TIMES_TYPE_ITEM:
            pass

        else:
            LOG_ERR('IWonderLandBase::addWonderLandTicket: invalid addType: {}'.format(addType))
            return

        _award = dropAward.DeductWealthVal()
        for (itemId, itemNum, n) in costList:
            _award.addWealthByItemId(itemId, itemNum * n)

        res = self.canDeductWealth(_award)
        if not res:
            LOG_WARN('IWonderLandBase::addWonderLandTicket: can not deduct wealth', res())
            return

        _src = AAC_AACDD.datas.BONUS_SRC_ADD_WONDER_LAND_TIMES
        _detail = gameclass.AwardDetailCls()
        self.deductWealth(_src, _award, opUUID, _detail)

        freeNum = 0
        paidNum = 0
        attType = gameconst.addTicketTimesType.NULL
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.wonderLandAddTimes -= num
            attType = gameconst.addTicketTimesType.COIN
            for (itemId, itemNum, n) in costList:
                if not itemNum:
                    freeNum += n
                else:
                    paidNum += n
                    self.addGuildCommissionGold(itemId, n * itemNum)
        else:
            paidNum = num
            attType = gameconst.addTicketTimesType.TOKEN_ITEM

        if isAddDuration:
            self.cell.directlyAddWonderLandDuration('addWonderLandDurFailed', (opUUID, addType, costList, num))
        else:
            self.modifyWonderLandTicket(num, freeNum, paidNum, _src, opUUID, attType)
        LogTrackingMgr.LogTrackingMgr.wonderland_ticket_buy(
            self.gbID,
            self.accountEntity.clientDistinctId,
            addType,
            num,
        )

    def addWonderLandDurFailed(self, opUUID, addType, costList, num):
        _award = dropAward.AwardVal()
        _src = AAC_AACDD.datas.BONUS_SRC_ADD_WONDER_LAND_TIMES
        _detail = gameclass.AwardDetailCls(reason='add wonderland duration failed')
        for (itemId, itemNum, n) in costList:
            _award.addWealthByItemId(itemId, itemNum * n)

        self.addWealth(_src, _award, opUUID, _detail)
        if addType == gameconst.CUBE_ADD_TIMES_TYPE_COIN:
            self.wonderLandAddTimes += num

    def checkSummonWonderLandBossBase(self, itemId, itemNum, bossId):
        _deductAward = dropAward.DeductWealthVal()
        _deductAward.addWealthByItemId(itemId, itemNum)

        res = self.canDeductWealth(_deductAward)
        if not res:
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                return False
            _msgId = WL_CD.datas['wonderLand_summoningFailed2']['value']
            _bossName = CBD.datas[bossId]['name']
            _args = [str(itemId), str(itemNum)]
            self.onMessagePre(_msgId, _args)
            return False

        return True

    def summonWonderLandBossBase(self, gid, itemId, itemNum, collectionId):
        _deductAward = dropAward.DeductWealthVal()
        _deductAward.addWealthByItemId(itemId, itemNum)

        res = self.canDeductWealth(_deductAward)
        if not res:
            LOG_WARN('IWonderLandBase::summonWonderLandBossBase: can not deduct wealth', res())
            return False

        _src = AAC_AACDD.datas.BONUS_SRC_SUMMON_BOOSS
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetailCls(reason='summon wonderland boss')

        self.deductWealth(_src, _deductAward, _opUUID, _detail)

        self.cell.summonWonderLandBossFromBase(gid, itemId, collectionId, _opUUID)
        return True

    def summonWonderLandBossBaseFailed(self, opUUID, itemId):
        _award = dropAward.AwardVal()
        _src = AAC_AACDD.datas.BONUS_SRC_SUMMON_BOOSS
        _detail = gameclass.AwardDetailCls(reason='summon wonderland boss failed')

        _award.addWealthByItemId(itemId, 1)

        self.addWealth(_src, _award, opUUID, _detail)

    def autoRenewWonderLand(self, switchData):
        if not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']):
            LOG_INFO('IWonderLandBase::autoRenewWonderLand: wonderLandActID not open')
            return

        _opUUID = KBEngine.genUUID64()
        if self.sumWonderLandTicket() > 0:
            freeNum, paidNum = self.modifyWonderLandTicket(-1, 0, 0, AAC_AACDD.datas.BONUS_SRC_WONDER_LAND_AUTO_RENEW, _opUUID, gameconst.addTicketTimesType.NULL)
            self.cell.directlyAddWonderLandDuration('addWonderLandDurationFailedRewindTimes', (_opUUID, freeNum, paidNum, ))
            return

        if self.wonderLandAddTimes > 0:
            if switchData['coinSwitch']:
                coinType, coinNum, discountType = self.wonderLandCoinTicketData.getTicketInfo(self.wonderLandAddTimes)
                if not coinType:
                    LOG_ERR('autoRenewWonderLand: invalid wonderLandAddTimes', self.wonderLandAddTimes)
                    return  
                _deductVal = dropAward.DeductWealthVal()
                _deductVal.addWealthByItemId(coinType, coinNum)
                res = self.canDeductWealth(_deductVal)
                if res:
                    self.doAddWonderLandTicket(
                        gameconst.CUBE_ADD_TIMES_TYPE_COIN,
                        [(coinType, coinNum, 1)],
                        1,
                        True,
                        True,
                        gameconst.WonderAddTicketReason.RENEW_USE_COIN,
                        _opUUID,
                    )
                    return
                elif res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                    return

        if not switchData['itemSwitch']:
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(WL_CD.datas['wonderLandNumItem']['value'], 1)
        if not self.canDeductWealth(_deductVal):
            return

        self.doAddWonderLandTicket(
            gameconst.CUBE_ADD_TIMES_TYPE_ITEM,
            [(WL_CD.datas['wonderLandNumItem']['value'], 1, 1)],
            1,
            True,
            True,
            gameconst.WonderAddTicketReason.RENEW_USE_ITEM,
            _opUUID
        )

    def addWonderLandDurationFailedRewindTimes(self, opUUID, freeNum, paidNum):
        self.modifyWonderLandTicket(1, freeNum, paidNum, AAC_AACDD.datas.BONUS_SRC_WONDER_LAND_FAILED_REWIND, opUUID, gameconst.addTicketTimesType.COIN)

    def sendWonderLandLoginData(self):
        self.cell.doSendWonderLandLoginData()

    def onLogonEnterWonderLandGetSpaceBox(self, spaceBox, spaceMgrBoxCellId):
        self.addCreateCellCB('onLogonEnterWonderLandCB', (spaceMgrBoxCellId,))
        spaceBox.createCellNearSelf(self)

